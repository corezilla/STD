"""Invariants for the stage-aligned tests family (scheme/case-design/plan/report/asset)."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "templates/tests"
STAGES = ("unit", "module", "subsystem", "system")
SCHEMES = tuple(s + "-test-scheme" for s in STAGES)
DESIGNS = tuple(s + "-case" for s in STAGES)
PLANS = tuple(s + "-test-plan" for s in STAGES)
REPORTS = tuple(s + "-test-report" for s in STAGES)
ASSET = "asset-design"
ALL = SCHEMES + DESIGNS + PLANS + REPORTS + (ASSET,)


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        self.policy = json.loads((ROOT / "templates/path-policy.json").read_text())

    def _expected_path(self, name):
        if name == ASSET:
            return "docs/70_verification/assets"
        stage = name.split("-")[0]
        if name in SCHEMES or name in PLANS:
            return f"docs/70_verification/{stage}"
        if name in DESIGNS:
            return f"docs/70_verification/{stage}/cases"
        return {
            "unit": "tests/unit",
            "module": "tests/unit",
            "subsystem": "tests/integration/reports",
            "system": "tests/system/reports",
        }[stage]

    def test_all_seventeen_registered_with_paths(self):
        for name in ALL:
            tid = "tests." + name
            self.assertEqual(self.catalog["templates"][tid], "tests/" + name + ".md", tid)
            self.assertIn(tid, self.catalog["template_versions"], tid)
            self.assertEqual(self.policy["default_paths"][tid],
                             self._expected_path(name), tid)

    def test_key_versions(self):
        v = self.catalog["template_versions"]
        self.assertEqual(v["tests.unit-case"], "2.3.2")
        self.assertEqual(v["tests.module-test-plan"], "0.9.2")
        self.assertEqual(v["tests.asset-design"], "0.2.2")
        self.assertEqual(v["tests.unit-test-report"], "0.3.1")


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
                self.assertNotIn("见附录 A", kept)
                if name not in SCHEMES:
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
                blocks = re.findall(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->\n(.*?)<!-- STD_TEMPLATE_EXAMPLE_END -->",
                                    text, flags=re.S)
                self.assertTrue(blocks, name)
                for block in blocks:
                    first = next(l for l in block.splitlines()
                                 if l.strip() and not l.startswith("###"))
                    self.assertTrue(first.startswith('<span style="color:#6e7681">'), name)


class RoleInvariants(unittest.TestCase):
    def test_schemes_own_the_inventory(self):
        for name in SCHEMES:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("| 来源 ID / 固定版本 | 设计验证项 ID | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |", text)
                self.assertIn("唯一登记处", text)
                self.assertNotIn("`PASS`", text)

    def test_designs_are_one_case_per_document_with_asset_links(self):
        for name in DESIGNS:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("一 Case 一文档", text)
                self.assertIn("Document ID＝Case ID", text)
                self.assertIn("tests.asset-design", text)
                self.assertIn("唯一 authority", text)
                self.assertIn("仅 Run 报告", text)
                self.assertIn("llm-testing.md", text)

    def test_plans_are_executable_with_asset_step_zero(self):
        for name in PLANS:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("可执行作业指令", text)
                self.assertIn("资产就位", text)
                self.assertIn("Step 0", text)
                self.assertIn("tests.asset-design", text)
                self.assertIn("Go / No-Go", text)
                self.assertIn("test-report", text)
                self.assertNotIn("`PASS` / `FAIL`", text)

    def test_hifm_feedback_folded_in(self):
        for name in DESIGNS:
            self.assertIn("规模（数量、分页、复杂度）", (DIR / (name + ".md")).read_text())
            self.assertIn("分项判据", (DIR / (name + ".md")).read_text())
        for name in PLANS:
            text = (DIR / (name + ".md")).read_text()
            self.assertIn("构建接线", text)
            self.assertIn("阶段门", text)
            self.assertIn("复位阶梯", text)
        for name in REPORTS:
            text = (DIR / (name + ".md")).read_text()
            self.assertIn("待重验", text)
            self.assertIn("未复现/未关闭", text)
        self.assertIn("预定义故障场景", (DIR / "asset-design.md").read_text())
        for name in SCHEMES:
            self.assertIn("设计验证项 ID", (DIR / (name + ".md")).read_text())
            self.assertIn("至少一个 Case", (DIR / (name + ".md")).read_text())
        for name in DESIGNS:
            self.assertIn("设计验证项", (DIR / (name + ".md")).read_text())
            self.assertIn("VRC）为唯一权威", (DIR / (name + ".md")).read_text())
        for name in REPORTS:
            self.assertIn("设计验证项 ID", (DIR / (name + ".md")).read_text())

    def test_reports_own_verdicts(self):
        for name in REPORTS:
            text = (DIR / (name + ".md")).read_text()
            with self.subTest(template=name):
                self.assertIn("Verdict 唯一持有", text)
                self.assertIn("`PASS` / `FAIL`", text)
                self.assertIn("覆盖复算", text)
                self.assertIn("不越权", text)
                self.assertIn("Run 证据", text)

    def test_asset_design_holds_contract_authority(self):
        text = (DIR / (ASSET + ".md")).read_text()
        self.assertIn("唯一 authority", text)
        self.assertIn("消费方索引", text)
        self.assertIn("不替产品补可测试性", text)
        self.assertIn("`Unverified` / `Verified`", text)
        self.assertIn("自检", text)


if __name__ == "__main__":
    unittest.main()
