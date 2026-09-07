#!/usr/bin/env python3
"""Regression tests for validate-design discovery and read diagnostics."""

from __future__ import annotations

import importlib.machinery
import importlib.util
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


if __name__ == "__main__":
    unittest.main()
