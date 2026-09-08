#!/usr/bin/env python3
"""Regression tests for validate-design discovery and read diagnostics."""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, script_name: str):
    loader = importlib.machinery.SourceFileLoader(
        module_name, str(ROOT / "scripts" / script_name)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def load_validator():
    return load_script("std_validate_design", "validate-design")


class ValidateDesignDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_suffix_directory_is_not_discovered_as_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime" / "case-design.md").mkdir(parents=True)
            actual = root / "docs" / "actual.md"
            actual.parent.mkdir()
            actual.write_text("# Actual\n")
            excluded = root / "node_modules" / "ignored.md"
            excluded.parent.mkdir()
            excluded.write_text("# Ignored\n")

            self.assertEqual(self.validator.discover(root, ".md"), [actual])

    def test_markdown_read_failure_becomes_structured_issue(self):
        path = Path("unreadable.md")
        with mock.patch.object(Path, "read_text", side_effect=OSError("denied")):
            issues = self.validator.validate_markdown(path, None)

        self.assertEqual(issues[0]["code"], "markdown.read")
        self.assertIn("denied", issues[0]["message"])

    def test_cover_fields_are_read_only_between_cover_markers(self):
        metadata = {
            "document_id": "example",
            "document_version": "0.1.0-draft.1",
            "status": "review",
            "project": "example",
            "authority": "example",
            "document_owner": "Example Owner",
            "authors": ["Example Author"],
            "created_at": "2026-09-08",
            "last_modified_at": "2026-09-08",
            "std_version": "0.1.0-draft.19",
            "template_id": "design.definition",
            "template_version": "0.1.0",
            "template_conformance": "legacy-mapped",
            "tailoring_ref": None,
            "migration_map_ref": "docs/migration-map.json",
            "source_repository": "example/repository",
            "source_path": "docs/example.md",
            "supersedes": None,
        }
        cover_rows = {
            field: self.validator.expected_cover_value(field, metadata)
            for field in self.validator.COVER_MAP
        }
        cover = "\n".join(f"| {field} | {value} |" for field, value in cover_rows.items())

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            path.write_text(
                "<!-- STD_DOCUMENT_COVER_BEGIN -->\n"
                "# Example\n\n"
                f"{cover}\n"
                "<!-- STD_DOCUMENT_COVER_END -->\n\n"
                "## Runtime result\n\n"
                "| Status | FAIL |\n"
            )
            issues = self.validator.validate_markdown(path, metadata)

        self.assertFalse([item for item in issues if item["code"] == "cover.mismatch"])

    def test_template_versions_are_independent_and_complete(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())

        self.assertEqual(set(catalog["templates"]), set(catalog["template_versions"]))
        for version in catalog["template_versions"].values():
            self.assertRegex(version, r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")

    def test_template_covers_use_template_version_not_std_version(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())

        for relative in catalog["templates"].values():
            content = (ROOT / "templates" / relative).read_text()
            self.assertIn("| Template Version | `{{template_version}}` |", content)
            self.assertNotIn("| STD Version |", content)

    def test_document_std_provenance_does_not_follow_unrelated_std_changes(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())
        template_id = "design.system"
        template_path = ROOT / "templates" / catalog["templates"][template_id]

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "example.md"
            metadata_path = root / "example.metadata.json"
            document.write_text("# Example\n")
            metadata_path.write_text(json.dumps({
                "document_id": "example",
                "document_type": template_id,
                "std_version": "0.1.0-draft.7",
                "template_id": template_id,
                "template_version": catalog["template_versions"][template_id],
                "template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
                "source_path": "example.md",
            }))

            issues, _, _ = self.validator.validate_metadata(
                metadata_path, {}, catalog, None, {}, {"std_version": "9.9.9"}
            )

        self.assertFalse([item for item in issues if "std-version" in item["code"]])

    def test_readme_adoption_is_checked_against_project_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text(
                "This project adopts STD `0.1.0-draft.18`.\n"
            )
            (docs / "std.lock.json").write_text(json.dumps({
                "schema_version": "std-lock.v1",
                "std_version": "0.1.0-draft.18",
                "source_repository": "corezilla/STD",
                "source_revision": None,
                "source_tag": None,
                "source_manifest_path": "docs/std-source-manifest.json",
                "adopted_at": "2026-09-09",
                "project_profile": "software",
                "enabled_domains": ["software"],
            }))

            issues, _, _ = self.validator.validate_project_control(root, False)

            (root / "README.md").write_text(
                "This project adopts STD `0.1.0-draft.17`.\n"
            )
            mismatch, _, _ = self.validator.validate_project_control(root, False)

        self.assertFalse([item for item in issues if item["code"] == "readme.std-version"])
        self.assertTrue([item for item in mismatch if item["code"] == "readme.std-version"])

    def test_new_design_renders_independent_template_version(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            subprocess.run([
                str(ROOT / "scripts" / "new-design"),
                "--project", "example",
                "--template", "design.system",
                "--name", "system-design",
                "--output", str(output),
                "--repository", "example/repository",
                "--owner", "Example Owner",
                "--author", "Example Author",
            ], check=True, capture_output=True, text=True)

            markdown = (output / "system-design.md").read_text()
            metadata = json.loads((output / "system-design.metadata.json").read_text())

        self.assertIn("| Template Version | `0.1.0` |", markdown)
        self.assertNotIn("| STD Version |", markdown)
        self.assertEqual(metadata["template_version"], "0.1.0")


class SourceManifestDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_script("std_build_source_manifest", "build-source-manifest")
        cls.verifier = load_script("std_verify_source_manifest", "verify-source-manifest")
        cls.validator = load_validator()

    def test_git_ignored_platform_metadata_is_not_a_source_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".DS_Store\n")
            template = root / "templates" / "kept.md"
            template.parent.mkdir()
            template.write_text("# Kept\n")
            ignored = root / "templates" / ".DS_Store"
            ignored.write_bytes(b"platform metadata")
            guide = root / "docs" / "guide.md"
            guide.parent.mkdir()
            guide.write_text("# Guide\n")
            subprocess.run(["git", "-C", str(root), "add", ".gitignore", "templates/kept.md"], check=True)

            expected = {"docs/guide.md", "templates/kept.md"}
            excluded = root / "outside-manifest.json"
            built = {path.relative_to(root).as_posix() for path in self.builder.source_paths(root, excluded)}

            self.assertEqual(built, expected)
            self.assertEqual(self.verifier.expected_paths(root), expected)
            self.assertEqual(self.validator.expected_source_paths(root), expected)

    def test_non_git_fallback_excludes_platform_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guide = root / "docs" / "guide.md"
            guide.parent.mkdir()
            guide.write_text("# Guide\n")
            (root / "docs" / ".DS_Store").write_bytes(b"platform metadata")
            cached = root / "scripts" / "__pycache__" / "cached.pyc"
            cached.parent.mkdir(parents=True)
            cached.write_bytes(b"cache")

            expected = {"docs/guide.md"}
            excluded = root / "outside-manifest.json"
            built = {path.relative_to(root).as_posix() for path in self.builder.source_paths(root, excluded)}

            self.assertEqual(built, expected)
            self.assertEqual(self.verifier.expected_paths(root), expected)
            self.assertEqual(self.validator.expected_source_paths(root), expected)


class RagManifestVersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_script("std_build_rag_manifest", "build-rag-manifest")

    def test_catalog_template_uses_its_independent_version(self):
        catalog = {
            "templates": {"design.system": "design/system-design.md"},
            "template_versions": {"design.system": "2.3.4"},
        }

        self.assertEqual(
            self.builder.versions_for(
                "templates/design/system-design.md", "9.9.9", catalog
            ),
            ("2.3.4", "2.3.4"),
        )

    def test_guidance_uses_std_version(self):
        catalog = {"templates": {}, "template_versions": {}}

        self.assertEqual(
            self.builder.versions_for("docs/versioning.md", "9.9.9", catalog),
            ("9.9.9", "9.9.9"),
        )

if __name__ == "__main__":
    unittest.main()
