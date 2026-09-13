"""Subsystem scaffolding/generation checks, not a substantive design approval."""

import hashlib
import json
import re
import runpy
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/design/subsystem-design.md"


class SubsystemTemplateTests(unittest.TestCase):
    def command(self, directory):
        return [str(ROOT / "scripts/new-design"), "--project", "example",
                "--template", "design.subsystem", "--name", "example-subsystem",
                "--project-root", directory, "--repository", "example/repository",
                "--owner", "Example Owner", "--author", "Example Author"]

    def test_every_section_has_paragraph_guidance_and_completion(self):
        text = TEMPLATE.read_text()
        sections = re.split(r"(?m)^#{2,3} ", text)[1:]
        self.assertEqual(len(sections), 40)  # 15 chapters, two appendices, twenty-three subsection guides
        for section in sections:
            with self.subTest(heading=section.splitlines()[0]):
                self.assertEqual(section.count("<details>"), 1)
                self.assertEqual(section.count("</details>"), 1)
                for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
                    self.assertIn(f"**{label}**", section)
        for term in ("上级 Mechanism ID", "共享预算", "独立 Oracle", "NOT_IMPLEMENTED",
                     "全部必需消费者", "Guard 的事实来源", "重新准入", "计划文件名",
                     "不伪造审批", "组合验证", "prompt"):
            self.assertIn(term, text)

    def test_generated_subsystem_default_path_identity_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(self.command(directory), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            base = Path(directory) / "docs/30_subsystem_design"
            md = (base / "example-subsystem.md").read_text()
            meta = json.loads((base / "example-subsystem.metadata.json").read_text())
            self.assertEqual(meta["design_level"], "subsystem")
            self.assertEqual(meta["template_id"], "design.subsystem")
            self.assertEqual(meta["template_version"], "0.4.0")
            self.assertEqual(meta["template_sha256"], hashlib.sha256(TEMPLATE.read_bytes()).hexdigest())
            self.assertEqual(meta["source_path"], "docs/30_subsystem_design/example-subsystem.md")
            self.assertNotIn("{{", md)
            self.assertNotIn("EX-JOB", md)
            self.assertNotIn("EX-RECURSIVE", md)
            self.assertNotIn("../diagrams/", md)
            self.assertIn("## 15. 实现与下游详细设计", md)
            self.assertNotIn("```mermaid", md)  # explicitly marked fictional context example removed
            self.assertIn("**编写规范**", md)
            cover = md.split("<!-- STD_DOCUMENT_COVER_END -->")[0]
            self.assertEqual(len(re.findall(r"^\| [A-Z][^|]+ \|", cover, re.M)), 8)
            self.assertNotIn("| Authority |", cover)
            self.assertIn("| Authority |", md.split("## B.")[1])
            checked = subprocess.run([str(ROOT / "scripts/validate-design"), directory, "--json"],
                                     capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["issues"], [])

    def test_wrong_level_rejected_even_with_output_override(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(self.command(directory) + ["--level", "module", "--output", directory],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("必须使用 subsystem", result.stderr)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_outline_centers_preliminary_design_not_file_handoff(self):
        text = TEMPLATE.read_text()
        headings = re.findall(r"(?m)^## (\d+)\. (.+)$", text)
        self.assertEqual([int(n) for n, _ in headings], list(range(1, 16)))
        self.assertIn("总体方案（第 0 层设计）", headings[2][1])
        self.assertIn("软件架构与模块分解（第 1 层设计）", headings[3][1])
        self.assertEqual(headings[4][1], "运行设计")
        for term in ("直属组成概要设计", "运行单元、调度与通信", "配置管理设计",
                     "可调试性设计", "可维护性与升级设计", "不是函数、类或源文件的详细设计",
                     "工厂装载/自检", "通用 OS/运行库", "上下文图例"):
            self.assertIn(term, text)
        guide = (ROOT / "docs/ai-guides/unit-design.md").read_text()
        self.assertIn("第 0 层整体方案 → 第 1 层架构与模块概要 → 运行与接口设计", guide)
        self.assertIn("§15 下游详细设计", guide)

    def test_system_alignment_sections_have_concrete_obligations(self):
        text = TEMPLATE.read_text()
        expected = {
            "2.2": ("Process/Step ID", "不要求照搬章号", "系统已定内容"),
            "6.1": ("逻辑键", "私有字段", "不为模板新增数据库"),
            "6.2": ("Data/Stage ID", "实际复制", "前后形态"),
            "10.1": ("身份传播", "更新", "失败", "本地检查"),
            "11.1": ("客户端", "生效", "恢复责任"),
            "12.1": ("窗口", "代次", "不重新定义同名信号"),
            "12.2": ("检查 ID", "未执行", "退出恢复"),
            "12.3": ("§14.1", "用户数据", "回滚"),
            "13.2": ("Oracle", "NOT_RUN", "分母"),
            "13.3": ("串行", "撤销", "复位域"),
            "13.4": ("Run", "清理失败", "不覆盖首次失败"),
            "14.1": ("§12.3", "唯一", "固定单实例", "不兼容"),
        }
        for number, terms in expected.items():
            section = re.search(r"(?ms)^### " + re.escape(number) + r" .+?(?=^## |^### |\Z)", text)
            self.assertIsNotNone(section, number)
            for term in terms:
                self.assertIn(term, section[0], number)
        guide = (ROOT / "docs/ai-guides/unit-design.md").read_text()
        for term in ("系统已决定 / 本地细化 / 下级自由度 / 差异待决", "不要求升级上级模板",
                     "同名指标", "不比系统更宽", "局部与系统组合验证分别反馈"):
            self.assertIn(term, guide)

    def test_composition_svg_has_no_flow_arrows_and_links_exist(self):
        svg = ROOT / "templates/diagrams/subsystem-layered-architecture.svg"
        root = ET.fromstring(svg.read_text())
        tags = [node.tag.split("}")[-1] for node in root.iter()]
        for tag in ("line", "polyline", "path", "marker", "image"):
            self.assertNotIn(tag, tags)
        self.assertIn("title", tags)
        self.assertIn("desc", tags)
        for target in re.findall(r"\]\(([^)]+)\)", TEMPLATE.read_text()):
            self.assertTrue((TEMPLATE.parent / target).resolve().is_file(), target)

    def test_recursive_figures_preserve_object_identity_and_type(self):
        expected = {"SUB-P": ("subsystem", "SYS-EX"), "SUB-C": ("subsystem", "SUB-P"),
                    "MOD-D": ("module", "SUB-P")}
        for name in ("composition", "runtime"):
            tree = ET.parse(ROOT / f"templates/diagrams/subsystem-recursive-{name}.svg")
            nodes = [n for n in tree.iter() if "data-object-id" in n.attrib]
            self.assertEqual(len(nodes), 3)
            self.assertEqual({n.attrib["data-object-id"]: (n.attrib["data-object-type"], n.attrib["data-parent-id"])
                              for n in nodes}, expected)
            lines = [n for n in tree.iter() if n.tag.endswith("}line")]
            self.assertEqual(len(lines), 0 if name == "composition" else 2)
        text = TEMPLATE.read_text()
        for term in ("规格或机器定义缺失是设计/规格缺口", "被测对象 ID / 类型 / 父对象 ID",
                     "系统公共 / 本层直属 / 下级私有", "子级 PASS", "parent_document_id"):
            self.assertIn(term, text)


class DesignHierarchyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = staticmethod(runpy.run_path(str(ROOT / "scripts/validate-design"))["validate_design_hierarchy"])

    def records(self):
        def node(id, level, parent, template):
            return Path(id + ".metadata.json"), {"document_id": id, "design_level": level,
                "parent_document_id": parent, "template_id": template, "project": "example"}
        return [node("DOC-SYS", "system", None, "design.system"),
                node("DOC-P", "subsystem", "DOC-SYS", "design.subsystem"),
                node("DOC-C", "subsystem", "DOC-P", "design.subsystem"),
                node("DOC-D", "module", "DOC-P", "design.definition")]

    def test_recursive_subsystems_and_direct_module(self):
        errors, depths = self.audit(self.records())
        self.assertEqual(errors, [])
        self.assertEqual(depths, {"DOC-P": 1, "DOC-C": 2})
        records = self.records()
        records[1][1]["template_id"] = "design.definition"  # existing adopted subsystem remains valid
        self.assertEqual(self.audit(records), ([], depths))

    def test_missing_self_cycle_type_and_project_are_rejected(self):
        cases = [
            (2, "parent_document_id", None, "hierarchy.parent-required"),
            (2, "parent_document_id", "ABSENT", "hierarchy.parent-missing"),
            (2, "parent_document_id", "DOC-C", "hierarchy.cycle"),
            (1, "parent_document_id", "DOC-C", "hierarchy.cycle"),
            (2, "parent_document_id", "DOC-D", "hierarchy.parent-type"),
            (1, "project", "other", "hierarchy.project"),
            (1, "design_level", "module", "hierarchy.type"),
            (0, "template_id", "review.packet", "hierarchy.parent-type"),
        ]
        for index, field, value, code in cases:
            with self.subTest(case=(index, field, value)):
                records = self.records()
                records[index][1][field] = value
                errors, _ = self.audit(records)
                self.assertIn(code, {e["code"] for e in errors})

    def test_duplicate_and_incomplete_root_are_not_silently_resolved(self):
        records = self.records()
        errors, depths = self.audit(records + [records[1]])
        self.assertIn("hierarchy.ambiguous-id", {e["code"] for e in errors})
        self.assertEqual(depths, {})
        records[1][1]["parent_document_id"] = None
        errors, depths = self.audit(records)
        self.assertIn("hierarchy.root", {e["code"] for e in errors})
        self.assertNotIn("DOC-C", depths)

    def test_cli_generation_parent_chain_and_explicit_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            for _, item in self.records():
                command = [str(ROOT / "scripts/new-design"), "--project", "example", "--output", directory,
                           "--name", item["document_id"], "--template", item["template_id"],
                           "--level", item["design_level"], "--owner", "Example Owner", "--author", "Example Author",
                           "--repository", "example/repo"]
                if item["parent_document_id"]:
                    command += ["--parent-document-id", item["parent_document_id"]]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            check = subprocess.run([str(ROOT / "scripts/validate-design"), directory,
                                    "--check-design-hierarchy", "--json"], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            self.assertEqual(json.loads(check.stdout)["subsystem_depths"], {"DOC-P": 1, "DOC-C": 2})
            selfcheck = subprocess.run(command + ["--parent-document-id", item["document_id"]],
                                       capture_output=True, text=True)
            self.assertNotEqual(selfcheck.returncode, 0)
            self.assertIn("不能是文档自身", selfcheck.stderr)


if __name__ == "__main__":
    unittest.main()
