"""Structural invariants specific to the unit test design template."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/tests/unit-test-design.md"


class UnitTestDesignTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEMPLATE.read_text()
        cls.catalog = json.loads((ROOT / "templates/catalog.json").read_text())

    def test_registered_with_independent_version_and_default_path(self):
        self.assertEqual(self.catalog["templates"].get("tests.unit-test-design"),
                         "tests/unit-test-design.md")
        self.assertEqual(self.catalog["template_versions"].get("tests.unit-test-design"), "0.2.0")
        policy = json.loads((ROOT / "templates/path-policy.json").read_text())
        self.assertEqual(policy["default_paths"]["tests.unit-test-design"],
                         "docs/70_verification/specifications")

    def test_state_semantics_separate_four_states(self):
        block = self.text.split("### 状态语义：四种状态分开", 1)[1].split("## 1.", 1)[0]
        for state in ("Case 设计状态", "测试代码实现状态", "执行状态", "实际判定 Verdict"):
            self.assertIn(state, block)
        self.assertIn("仅 Run 报告", block)
        self.assertNotIn("Planned", block.split("| 实际判定 Verdict |", 1)[1].split("\n", 1)[0])

    def test_chapter5_applicability_is_fact_gated(self):
        block = self.text.split("## 5. 状态、并发与故障测试", 1)[1].split("## 6.", 1)[0]
        self.assertIn("模块事实（引用设计章节）", block)
        self.assertIn("Transition / Invariant ID", block)
        self.assertIn("尚未设计", block)

    def test_coverage_records_carry_design_state_column(self):
        block = self.text.split("## 2. 测试依据与正向覆盖", 1)[1].split("## 3.", 1)[0]
        self.assertIn("| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |", block)

    def test_teaching_appendix_is_fully_inside_example_markers(self):
        begin = self.text.index("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->")
        end = self.text.rindex("<!-- STD_TEMPLATE_EXAMPLE_END -->")
        appendix = self.text.index("## 附录 A.")
        self.assertGreater(appendix, begin)
        self.assertLess(appendix, end)
        inner = self.text[begin:end]
        self.assertEqual(inner.count("STD_TEMPLATE_EXAMPLE_BEGIN"), 1)
        kept = self.text[:begin] + self.text[end:]
        self.assertNotIn("见附录 A.1。", kept)


if __name__ == "__main__":
    unittest.main()
