"""Navigation and method-boundary regressions; not a writing-quality verdict."""

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def heading_slugs(content):
    """GitHub-style anchors for the plain headings used by these guides."""
    slugs = set()
    seen = Counter()
    for heading in re.findall(r"^#{1,6} (.+)$", content, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = seen[slug]
        seen[slug] += 1
        slugs.add(slug if count == 0 else f"{slug}-{count}")
    return slugs


class AIAuthoringGuidesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = json.loads((ROOT / "docs/ai-authoring-guides.json").read_text())
        cls.catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        cls.common_path = ROOT / cls.mapping["common_guide"]
        cls.common = cls.common_path.read_text()
        cls.guides = [cls.common_path] + [ROOT / f["guide"] for f in cls.mapping["families"]]

    def test_each_catalog_template_has_exactly_one_primary_specialist(self):
        families = self.mapping["families"]
        assigned = [tid for family in families for tid in family["template_ids"]]
        self.assertEqual(set(assigned), set(self.catalog["templates"]))
        self.assertEqual(set(Counter(assigned).values()), {1})
        self.assertEqual(len({f["id"] for f in families}), len(families))
        self.assertEqual(len({f["guide"] for f in families}), len(families))
        for family in families:
            self.assertTrue(family["template_ids"])
            self.assertNotIn("template_versions", family)  # no duplicate version registry
            for tid in family["template_ids"]:
                self.assertTrue((ROOT / "templates" / self.catalog["templates"][tid]).is_file())

    def test_human_routes_match_machine_navigation(self):
        for family in self.mapping["families"]:
            guide = ROOT / family["guide"]
            self.assertTrue(guide.is_file())
            relative = guide.relative_to(self.common_path.parent).as_posix()
            row = next(line for line in self.common.splitlines() if f"]({relative}) |" in line)
            self.assertEqual(set(re.findall(r"`([^`]+)`", row)), set(family["template_ids"]))
            content = guide.read_text()
            for tid in family["template_ids"]:
                self.assertIn(f"`{tid}`", content)
            self.assertIn("通用 AI 编写指南", content)
            self.assertIn("ai-authoring-guide.md", content)
            self.assertIsNotNone(re.search(r"^版本：\d+\.\d+\.\d+-draft\.\d+", content, re.M), guide.name)

    def test_local_links_and_guide_section_targets_exist(self):
        for path in self.guides:
            for reference in re.findall(r"\]\(([^\s)]+)\)", path.read_text()):
                if "://" in reference:
                    continue
                dest, _, fragment = reference.partition("#")
                target = (path.parent / dest).resolve() if dest else path
                with self.subTest(source=path.name, reference=reference):
                    self.assertTrue(target.is_file())
                    if fragment and target in self.guides:
                        self.assertIn(fragment, heading_slugs(target.read_text()))

    def test_common_method_keeps_scope_evidence_and_permission_boundaries(self):
        for term in ("一个主专项指南", "不重跑完整写作流程", "资料缺失不是 N/A",
                     "输入与约束 → 真实可行选项", "报告不能用预设计补造历史测量",
                     "共享预算不能重复分配", "不作为训练材料提交", "不由写作任务或通过检查自动授权",
                     "不主动检查模板是否有新版", "待各类实际写作任务验证"):
            self.assertIn(term, self.common)
        self.assertNotIn("Planned / Implemented / Verified", self.common)

    def test_specialists_have_inputs_workflow_examples_and_handoff(self):
        # These headings ensure the scaffolding survives; prose still needs human/content review.
        for family in self.mapping["families"]:
            if family["id"] == "system":
                continue  # mature system guide keeps its existing chapter anchors
            content = (ROOT / family["guide"]).read_text()
            for term in ("## 1. 输入与边界", "## 2. 专项执行顺序",
                         "## 4. 写法示例" if family["id"] == "mechanism" else "## 4. 图例与写法示例",
                         "## 5. 完成检查与下游承接", "虚构"):
                self.assertIn(term, content, family["id"])

    def test_specialist_plan_report_and_constraint_distinctions_remain(self):
        checks = {
            "hardware": ("Constraint ID", "可返修边界", "不是制造用 CAD", "上电许可"),
            "fpga": ("自己编写的 FPGA 程序", "目标频率代替收敛结果", "系统验证"),
            "verification": ("独立 Oracle", "缺测或不可复现", "报告完整可以包含 FAIL"),
            "review": ("不能早于该内容", "不代签批准", "局部结论不能自动合成发布批准"),
            "operations": ("不能在手册里创造新命令", "文档任务自动操作环境", "用户数据必须保留"),
        }
        for fid, terms in checks.items():
            path = next(ROOT / f["guide"] for f in self.mapping["families"] if f["id"] == fid)
            text = path.read_text()
            for term in terms:
                self.assertIn(term, text)

    def test_mechanism_chapter_routes_match_actual_template(self):
        template = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        writing = (ROOT / "docs/design-writing-guide.md").read_text()
        count = len(re.findall(r"^## \d+\.", template, re.M))
        self.assertEqual(count, 16)
        self.assertIn(f"沿其 {count} 章主线", writing)
        self.assertIn("维护入口在 §12.2、测试在 §15", writing)
        self.assertRegex(template, r"(?m)^### 12\.2 .*维护")
        self.assertRegex(template, r"(?m)^## 15\. .*验证")
        for path in [ROOT / "docs/design-writing-guide.md", *self.guides]:
            text = path.read_text()
            self.assertNotIn("沿其 15 章主线", text)
            self.assertNotIn("维护入口在 §11.2", text)
            self.assertNotIn("包含 15 章写作顺序", text)

    def test_mechanism_parent_tree_is_not_the_dependency_graph(self):
        template = (ROOT / "templates/design/architecture-design.md").read_text()
        section = template.split("### 3.4 系统机制清单与文档映射", 1)[1].split("## 4.", 1)[0]
        examples = {}
        for line in section.splitlines():
            if line.startswith("| M-"):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                examples[cells[0].split(" / ")[0]] = cells[1]
        self.assertEqual(examples, {"M-DELIVERY": "none", "M-EXPORT": "M-DELIVERY", "M-OBS": "none"})
        for child, parent in examples.items():
            seen = {child}
            while parent != "none":
                self.assertIn(parent, examples)
                self.assertNotIn(parent, seen)
                seen.add(parent)
                parent = examples[parent]
        self.assertIn("写作前置 M-OBS", section)
        for relative in ("docs/interface-data-mapping-standard.md", "docs/ai-system-design-authoring-guide.md",
                         "docs/ai-guides/system-mechanism.md", "templates/design/system-mechanism-design.md"):
            text = (ROOT / relative).read_text()
            self.assertIn("上级 Mechanism ID", text)
            self.assertIn("前置依赖", text)
            self.assertIn("循环", text)


if __name__ == "__main__":
    unittest.main()
