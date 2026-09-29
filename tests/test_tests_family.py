"""Invariants for the stage-aligned tests family (scheme / case-design / plan)."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "templates/tests"
SCHEMES = ('unit-test-scheme', 'module-test-scheme', 'subsystem-test-scheme', 'system-test-scheme')
DESIGNS = ('unit-test-design', 'module-test-design', 'subsystem-test-design', 'system-test-design')
PLANS = ('unit-test-plan', 'module-test-plan', 'subsystem-test-plan', 'system-test-plan')
ALL = SCHEMES + DESIGNS + PLANS


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        self.policy = json.loads((ROOT / "templates/path-policy.json").read_text())

    def test_all_twelve_registered_with_paths_and_versions(self):
        for name in ALL:
            tid = "tests." + name
            self.assertEqual(self.catalog["templates"][tid], "tests/" + name + ".md", tid)
            self.assertIn(tid, self.catalog["template_versions"], tid)
            expected = ("docs/70_verification/schemes" if name in SCHEMES else
                        "docs/70_verification/specifications" if name in DESIGNS else
                        "docs/70_verification/plans")
            self.assertEqual(self.policy["default_paths"][tid], expected, tid)

    def test_major_restructure_versions(self):
        v = self.catalog["template_versions"]
        self.assertEqual(v["tests.unit-test-design"], "2.0.0")
        self.assertEqual(v["tests.module-test-design"], "2.0.0")
        for name in SCHEMES:
            self.assertEqual(v["tests." + name], "0.1.0")


class FormatInvariants(unittest.TestCase):
    def test_legend_blue_guidance_gray_examples_every_file(self):
        for name in ALL:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("**格式说明**", text)
                self.assertEqual(text.count("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->"),
                                 text.count("<!-- STD_TEMPLATE_EXAMPLE_END -->"))
                kept = re.sub(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->.*?<!-- STD_TEMPLATE_EXAMPLE_END -->",
                              "", text, flags=re.S)
                self.assertNotIn("附录 A", kept)
                self.assertNotIn("<details>", kept)
                lines = kept.splitlines()
                idx = next(i for i, l in enumerate(lines)
                           if l.strip() == "<!-- STD_DOCUMENT_COVER_END -->")
                follow = next(l for l in lines[idx + 1:] if l.strip())
                self.assertTrue(follow.startswith('<span style="color:#1f6feb"><em>'), name)
                for i, line in enumerate(lines):
                    if line.startswith(("## ", "### ")):
                        nxt = next(l for l in lines[i + 1:] if l.strip())
                        self.assertTrue(nxt.startswith('<span style="color:#1f6feb"><em>'),
                                        f"{name}: {line}")
                for block in re.findall(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->\n(.*?)<!-- STD_TEMPLATE_EXAMPLE_END -->",
                                        text, flags=re.S):
                    first = next(l for l in block.splitlines()
                                 if l.strip() and not l.startswith("###"))
                    self.assertTrue(first.startswith('<span style="color:#6e7681">'), name)


class RoleInvariants(unittest.TestCase):
    def test_schemes_own_the_inventory(self):
        for name in SCHEMES:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("| 来源 ID / 固定版本 | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |", text)
                self.assertIn("唯一登记处", text)
                self.assertIn("`Designed` / `Gap`（具名缺口）/ `Tailored-N/A`", text)

    def test_designs_are_one_case_per_document(self):
        for name in DESIGNS:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("一 Case 一文档", text)
                self.assertIn("Document ID＝Case ID", text)
                self.assertIn("`Planned` / `Implemented`", text)
                self.assertIn("仅 Run 报告", text)
                self.assertNotIn("`Designed` / `Gap`", text)

    def test_plans_index_without_duplicating(self):
        for name in PLANS:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("`Planned`", text)
                self.assertIn("`Deferred`", text)
                self.assertIn("`Blocked`", text)
                self.assertIn("test-scheme", text)
                self.assertIn("test-design", text)


if __name__ == "__main__":
    unittest.main()
