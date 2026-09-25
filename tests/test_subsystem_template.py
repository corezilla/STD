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
        self.assertEqual(len(sections), 47)  # 14 chapters, two appendices, thirty-one subsection guides
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
            (Path(directory) / "README.md").write_text('# Example\n<a id="std-entry"></a>\n')
            result = subprocess.run(self.command(directory), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            base = Path(directory) / "docs/30_subsystem_design"
            md = (base / "example-subsystem.md").read_text()
            meta = json.loads((base / "example-subsystem.metadata.json").read_text())
            self.assertEqual(meta["design_level"], "subsystem")
            self.assertEqual(meta["template_id"], "design.subsystem")
            self.assertEqual(meta["template_version"], "0.8.0")
            self.assertEqual(meta["template_sha256"], hashlib.sha256(TEMPLATE.read_bytes()).hexdigest())
            self.assertEqual(meta["source_path"], "docs/30_subsystem_design/example-subsystem.md")
            self.assertNotIn("{{", md)
            self.assertNotIn("EX-JOB", md)
            self.assertNotIn("EX-SOFTWARE-LAYERS", md)
            self.assertNotIn("../diagrams/", md)
            self.assertIn("## 14. 实现与下游详细设计", md)
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

    def test_chapter_order_references_and_three_view_positions(self):
        text = TEMPLATE.read_text()
        # Migration table intentionally records old chapter numbers, not active references.
        active = re.sub(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->.*?<!-- STD_TEMPLATE_EXAMPLE_END -->",
                        "", text, flags=re.S)
        numbers = re.findall(r"(?m)^#{2,3} (\d+(?:\.\d+)*)\.? ", active)
        self.assertEqual(len(numbers), len(set(numbers)))
        keys = [tuple(map(int, n.split("."))) for n in numbers]
        self.assertEqual(keys, sorted(keys))
        for reference in re.findall(r"§(\d+(?:\.\d+)*)", active):
            self.assertIn(reference, numbers)
        for chapter, image in (("1.2", "context"), ("2", "overall-architecture"), ("3", "module-breakdown")):
            section = re.search(r"(?ms)^#{2,3} " + re.escape(chapter) +
                                r"\.? .+?(?=^## |^### |\Z)", text)[0]
            self.assertIn(f"subsystem-{image}.png", section)
            self.assertIn(f"subsystem-{image}.svg", section)
        self.assertIn("| 本地 Capability ID / 功能 | 需求 ID / 要求 |", text)
        self.assertIn("0.5.0 → 0.6.0", text)
        self.assertIn("| §5–15 | §4–14", text)

    def test_continuous_figures_share_boundary_groups_and_real_modules(self):
        roots = {name: ET.parse(ROOT / f"templates/diagrams/subsystem-{name}.svg").getroot()
                 for name in ("context", "overall-architecture", "module-breakdown")}
        for name, root in roots.items():
            objects = [n for n in root.iter() if n.get("data-object-id")]
            subsystem = [n for n in objects if n.get("data-object-id") == "S02"]
            self.assertEqual(len(subsystem), 1)
            self.assertEqual(subsystem[0].get("data-parent-id"), "SW-P")
            self.assertEqual(subsystem[0].get("data-object-type"), "subsystem")
            self.assertIn("EX-JOB/v2", "".join(root.itertext()))
            # PNG export must preserve the full SVG aspect ratio, not a cropped square thumbnail.
            png = (ROOT / f"templates/diagrams/subsystem-{name}.png").read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual((int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")), (1200, 720))
        external = lambda root: {n.get("data-external-id") for n in root.iter() if n.get("data-external-id")}
        self.assertEqual(external(roots["context"]), {"CALLER", "ADMIN", "EXEC"})
        self.assertEqual(external(roots["context"]), external(roots["overall-architecture"]))
        groups = lambda root: {n.get("data-group-id") for n in root.iter() if n.get("data-group-id")}
        self.assertEqual(groups(roots["context"]), set())
        self.assertEqual(groups(roots["overall-architecture"]), {"entry", "orchestration", "execution", "shared"})
        self.assertEqual(groups(roots["overall-architecture"]), groups(roots["module-breakdown"]))
        expected = {"entry": {"M201"}, "orchestration": {"M202", "M204"}, "execution": {"M203"}, "shared": {"M205"}}
        for group in roots["module-breakdown"].iter():
            if group.get("data-group-id"):
                modules = [n for n in group.iter() if n.get("data-object-id")]
                self.assertEqual({n.get("data-object-id") for n in modules}, expected[group.get("data-group-id")])
                for module in modules:
                    self.assertEqual(module.get("data-parent-id"), "S02")
                    self.assertEqual(module.get("data-object-type"), "module")
                    self.assertIn("(" + module.get("data-object-id") + ")", "".join(module.itertext()))
        self.assertFalse(any(n.tag.endswith("}line") for n in roots["module-breakdown"].iter()))

    def test_outline_centers_preliminary_design_not_file_handoff(self):
        text = TEMPLATE.read_text()
        headings = re.findall(r"(?m)^## (\d+)\. (.+)$", text)
        self.assertEqual([int(n) for n, _ in headings], list(range(1, 15)))
        self.assertIn("总体架构设计（第 0 层）", headings[1][1])
        self.assertIn("分层与模块设计（第 1 层）", headings[2][1])
        self.assertEqual(headings[3][1], "运行设计")
        for term in ("模块处理概要", "运行单元、调度与通信", "配置管理设计",
                     "可调试性设计", "可维护性与升级设计", "不是函数、类或源文件的详细设计",
                     "工厂装载/自检", "通用 OS/运行库", "上下文图例"):
            self.assertIn(term, text)
        guide = (ROOT / "docs/ai-guides/unit-design.md").read_text()
        self.assertIn("第 0 层整体架构 → 第 1 层分层与模块设计 → 运行与接口设计", guide)
        self.assertIn("§14 下游详细设计", guide)

    def test_system_alignment_sections_have_concrete_obligations(self):
        text = TEMPLATE.read_text()
        expected = {
            "1.6": ("Process/Step ID", "不要求照搬章号", "系统已定内容"),
            "5.5": ("逻辑键", "私有字段", "不为模板新增数据库"),
            "5.6": ("Data/Stage ID", "实际复制", "前后形态"),
            "9.1": ("身份传播", "更新", "失败", "本地检查"),
            "10.1": ("客户端", "生效", "恢复责任"),
            "11.1": ("窗口", "代次", "不重新定义同名信号"),
            "11.2": ("检查 ID", "未执行", "退出恢复"),
            "11.3": ("§13.1", "用户数据", "回滚"),
            "12.2": ("Oracle", "NOT_RUN", "分母"),
            "12.3": ("串行", "撤销", "复位域"),
            "12.4": ("Run", "清理失败", "不覆盖首次失败"),
            "13.1": ("§11.3", "唯一", "固定单实例", "不兼容"),
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

    def test_current_design_taxonomy_and_names_are_consistent(self):
        selection = (ROOT / "docs/template-selection.md").read_text()
        for name in ("总体系统设计", "软件系统设计", "软件子系统设计", "软件模块设计",
                     "固件系统设计", "FPGA 程序顶层设计", "RTL 功能模块设计", "硬件系统设计",
                     "板卡设计", "电路功能单元设计", "总体系统机制设计", "design.software-system"):
            self.assertIn(name, selection)
        mapping = json.loads((ROOT / "docs/ai-authoring-guides.json").read_text())
        self.assertIn('"title": "总体系统设计"', json.dumps(mapping, ensure_ascii=False))
        self.assertIn('"title": "总体系统机制设计"', json.dumps(mapping, ensure_ascii=False))
        self.assertIn("软件子系统概要设计", TEMPLATE.read_text())
        self.assertNotIn("subsystem_depths", (ROOT / "scripts/validate-design").read_text())
        for name in ("subsystem-recursive-composition.svg", "subsystem-recursive-runtime.svg"):
            self.assertFalse((ROOT / "templates/diagrams" / name).exists())

    def test_software_hierarchy_figures_preserve_object_identity_and_type(self):
        expected = {"SW-P": ("system", "SYS-EX"), "SUB-C": ("subsystem", "SW-P"),
                    "MOD-D": ("module", "SW-P")}
        for name in ("composition", "runtime"):
            tree = ET.parse(ROOT / f"templates/diagrams/software-design-{name}.svg")
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
        # The software system is distinct from the total system and the software subsystem.
        return [node("DOC-SYS", "system", None, "design.system"),
                node("DOC-P", "system", "DOC-SYS", "design.software-system"),
                node("DOC-C", "subsystem", "DOC-P", "design.subsystem"),
                node("DOC-D", "module", "DOC-P", "design.definition")]

    def test_software_system_subsystem_and_direct_module(self):
        errors, links = self.audit(self.records())
        self.assertEqual(errors, [])
        self.assertEqual(links, {"DOC-P": "DOC-SYS", "DOC-C": "DOC-P", "DOC-D": "DOC-P"})
        records = self.records()
        records[2][1]["template_id"] = "design.definition"  # existing adopted subsystem remains valid
        self.assertEqual(self.audit(records), ([], links))

    def test_recursive_subsystem_is_rejected(self):
        records = self.records()
        records[1][1].update(template_id="design.subsystem", design_level="subsystem")
        errors, links = self.audit(records)
        self.assertIn("hierarchy.parent-type", {e["code"] for e in errors})
        self.assertNotIn("DOC-C", links)

    def test_subsystem_can_contain_software_module(self):
        records = self.records()
        records[3][1]["parent_document_id"] = "DOC-C"
        errors, links = self.audit(records)
        self.assertEqual(errors, [])
        self.assertEqual(links["DOC-D"], "DOC-C")

    def test_missing_self_cycle_type_and_project_are_rejected(self):
        cases = [
            (2, "parent_document_id", None, "hierarchy.parent-required"),
            (2, "parent_document_id", "ABSENT", "hierarchy.parent-missing"),
            (2, "parent_document_id", "DOC-C", "hierarchy.cycle"),
            (1, "parent_document_id", "DOC-C", "hierarchy.cycle"),
            (2, "parent_document_id", "DOC-D", "hierarchy.parent-type"),
            (1, "project", "other", "hierarchy.project"),
            (2, "design_level", "module", "hierarchy.type"),
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
        errors, links = self.audit(records + [records[1]])
        self.assertIn("hierarchy.ambiguous-id", {e["code"] for e in errors})
        self.assertEqual(links, {})
        records[0][1]["design_level"] = "module"
        errors, links = self.audit(records)
        self.assertIn("hierarchy.parent-type", {e["code"] for e in errors})
        self.assertNotIn("DOC-C", links)
        # Legacy generic system metadata still needs a valid root, not just a locally valid edge.
        records[1][1]["template_id"] = "design.system"
        errors, links = self.audit(records)
        self.assertIn("hierarchy.root", {e["code"] for e in errors})
        self.assertNotIn("DOC-C", links)

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
            self.assertEqual(json.loads(check.stdout)["design_parent_links"], {"DOC-P": "DOC-SYS", "DOC-C": "DOC-P", "DOC-D": "DOC-P"})
            selfcheck = subprocess.run(command + ["--parent-document-id", item["document_id"]],
                                       capture_output=True, text=True)
            self.assertNotEqual(selfcheck.returncode, 0)
            self.assertIn("不能是文档自身", selfcheck.stderr)


if __name__ == "__main__":
    unittest.main()
