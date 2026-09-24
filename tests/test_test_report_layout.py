"""Test report routing follows the test owner, not a duplicated docs report tree."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReportLayoutTests(unittest.TestCase):
    def generate(self, project, *options, template="assurance.test-report"):
        return subprocess.run([str(ROOT / "scripts/new-design"), "--project", "example",
            "--template", template, "--name", "run-report", "--project-root", str(project),
            "--owner", "test-owner", "--author", "author", "--repository", "example/repo",
            *options], capture_output=True, text=True)

    def test_reports_route_by_test_type_not_design_level(self):
        for scope in ("static", "contract", "subsystem", "integration", "system", "acceptance"):
            with self.subTest(scope=scope), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                result = self.generate(root, "--test-scope", scope, "--level", "module")
                self.assertEqual(result.returncode, 0, result.stderr)
                relative = f"tests/{scope}/reports/run-report"
                self.assertTrue((root / (relative + ".md")).is_file())
                metadata = json.loads((root / (relative + ".metadata.json")).read_text())
                self.assertEqual(metadata["source_path"], relative + ".md")
                self.assertFalse((root / "docs/70_verification/reports").exists())

    def test_ambiguous_and_module_default_fail_without_writes(self):
        for options in ((), ("--test-scope", "unit")):
            with tempfile.TemporaryDirectory() as temporary:
                result = self.generate(Path(temporary), *options)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("--output", result.stderr)
                self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_module_and_owner_reports_keep_metadata_and_are_validated(self):
        for relative in ("tests/unit/task-scheduler/reports/run-001",
                         "software/task-service/tests/unit/task-scheduler/reports/run-001"):
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / "README.md").write_text('# Example\n<a id="std-entry"></a>\n')
                output = root / relative
                result = self.generate(root, "--test-scope", "unit", "--output", str(output))
                self.assertEqual(result.returncode, 0, result.stderr)
                metadata = json.loads((output / "run-report.metadata.json").read_text())
                self.assertEqual(metadata["source_path"], relative + "/run-report.md")
                checked = subprocess.run([str(ROOT / "scripts/validate-design"), str(output), "--json"],
                                         capture_output=True, text=True)
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                self.assertEqual(json.loads(checked.stdout)["checked_metadata"], 1)
                first = (output / "run-report.md").read_bytes()
                repeated = self.generate(root, "--output", str(output))
                self.assertNotEqual(repeated.returncode, 0)
                self.assertEqual((output / "run-report.md").read_bytes(), first)

    def test_acceptance_report_and_plan_have_distinct_locations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for template, relative in (("assurance.acceptance-report", "tests/acceptance/reports"),
                                       ("assurance.test-plan", "docs/70_verification/plans"),
                                       ("assurance.test-specification", "docs/70_verification/specifications"),
                                       ("assurance.test-procedure", "docs/70_verification/procedures")):
                result = self.generate(root, template=template)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((root / relative / "run-report.md").is_file())
            result = self.generate(root, "--test-scope", "system", template="assurance.test-plan")
            self.assertNotEqual(result.returncode, 0)

    def test_layout_docs_explain_files_ids_and_retention(self):
        text = (ROOT / "docs/repository-layout.md").read_text()
        for term in ("tests/system/reports/", "tests/integration/reports/", "tests/unit/<module>/reports/",
                     "src/<subsystem>/<module>/", "src/<module>/",
                     "构建/交付单元", "SYS-CANCEL-001", "system-test-report.metadata.json", "artifacts/",
                     "不要一概忽略整个", "不要求每个Case", "既有项目不自动搬迁"):
            self.assertIn(term, text)
        self.assertNotIn("tests/unit/<module-id>/", text)
        policy = json.loads((ROOT / "templates/path-policy.json").read_text())
        self.assertNotIn("docs/70_verification/reports", json.dumps(policy))
