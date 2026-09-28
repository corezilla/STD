"""Structural invariants for the module-level test design and plan templates."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "templates/tests/module-test-design.md"
PLAN = ROOT / "templates/tests/module-test-plan.md"


class ModuleTestTemplateRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        cls.policy = json.loads((ROOT / "templates/path-policy.json").read_text())

    def test_module_test_design_registered(self):
        self.assertEqual(self.catalog["templates"].get("tests.module-test-design"),
                         "tests/module-test-design.md")
        self.assertEqual(self.catalog["template_versions"].get("tests.module-test-design"), "0.4.0")
        self.assertEqual(self.policy["default_paths"]["tests.module-test-design"],
                         "docs/70_verification/specifications")

    def test_module_test_plan_registered(self):
        self.assertEqual(self.catalog["templates"].get("tests.module-test-plan"),
                         "tests/module-test-plan.md")
        self.assertEqual(self.catalog["template_versions"].get("tests.module-test-plan"), "0.4.0")
        self.assertEqual(self.policy["default_paths"]["tests.module-test-plan"],
                         "docs/70_verification/plans")

    def test_every_numbered_chapter_has_a_fictional_example(self):
        for name in ("unit-test-design.md", "module-test-design.md", "module-test-plan.md"):
            text = (ROOT / "templates/tests" / name).read_text()
            chapters = re.split(r"(?m)^(## \d+\..*)$", text)
            for i in range(1, len(chapters), 2):
                with self.subTest(template=name, chapter=chapters[i]):
                    self.assertRegex(chapters[i + 1], "抽象示例|虚构示例|虚构 Case")


class ModuleTestDesignTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DESIGN.read_text()

    def test_positioning_splits_unit_module_and_contract_layers(self):
        block = cls_block = self.text.split("### 模板定位", 1)[1].split("## 1.", 1)[0]
        self.assertIn("tests.unit-test-design", block)
        self.assertIn("内部单元", block)
        self.assertIn("替身不证明真实依赖协议", block or self.text)

    def test_state_semantics_reuse_four_state_model(self):
        block = self.text.split("### 状态语义：四种状态分开", 1)[1].split("## 1.", 1)[0]
        for state in ("Case 设计状态", "测试代码实现状态", "执行状态", "实际判定 Verdict"):
            self.assertIn(state, block)

    def test_case_prefix_and_code_location(self):
        self.assertIn("`MT-<MODULE>-<NNN>`", self.text)
        self.assertIn("tests/unit/<module>/", self.text)

    def test_examples_are_inline_strippable_and_guidance_visible(self):
        begin = self.text.count("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->")
        end = self.text.count("<!-- STD_TEMPLATE_EXAMPLE_END -->")
        self.assertGreater(begin, 0)
        self.assertEqual(begin, end)
        self.assertNotIn("附录 A", self.text)
        self.assertNotIn("<details>", self.text)


class ModuleTestPlanTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PLAN.read_text()

    def test_plan_never_carries_execution_conclusions(self):
        block = self.text.split("### 计划条目状态语义", 1)[1].split("## 1.", 1)[0]
        for state in ("Planned", "Deferred", "Blocked"):
            self.assertIn(state, block)
        self.assertIn("Run 报告", block)

    def test_plan_indexes_design_docs_without_case_duplication(self):
        self.assertIn("tests.unit-test-design", self.text)
        self.assertIn("tests.module-test-design", self.text)
        self.assertIn("不复制", self.text)

    def test_examples_are_inline_strippable_and_guidance_visible(self):
        begin = self.text.count("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->")
        end = self.text.count("<!-- STD_TEMPLATE_EXAMPLE_END -->")
        self.assertGreater(begin, 0)
        self.assertEqual(begin, end)
        self.assertNotIn("附录 A", self.text)
        self.assertNotIn("<details>", self.text)
        chapters = re.split(r"(?m)^(## \d+\..*)$", self.text)
        for i in range(1, len(chapters), 2):
            with self.subTest(chapter=chapters[i]):
                self.assertIn("STD_TEMPLATE_EXAMPLE_BEGIN", chapters[i + 1])
                self.assertIn('<span style="color:#1f6feb"><em>**本节目的**', chapters[i + 1])


if __name__ == "__main__":
    unittest.main()
