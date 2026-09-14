"""Software-system scaffolding regressions, not a substantive design approval."""

import hashlib
import json
import re
import runpy
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/design/software-system-design.md"


class SoftwareSystemTemplateTests(unittest.TestCase):
    def command(self, directory, name="example-software"):
        return [str(ROOT / "scripts/new-design"), "--project", "example", "--template",
                "design.software-system", "--name", name, "--project-root", directory,
                "--title", "示例软件系统设计说明书", "--owner", "Example Owner",
                "--author", "Example Author", "--repository", "example/repo"]

    def test_outline_and_every_section_have_paragraph_guidance(self):
        text = TEMPLATE.read_text()
        chapters = re.findall(r"(?m)^## (\d+)\. (.+)$", text)
        self.assertEqual([int(number) for number, _ in chapters], list(range(1, 18)))
        sections = re.split(r"(?m)^#{2,3} ", text)[1:]
        self.assertEqual(len(sections), 57)
        for section in sections:
            with self.subTest(section=section.splitlines()[0]):
                self.assertEqual(section.count("<details>"), 1)
                self.assertEqual(section.count("</details>"), 1)
                for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
                    self.assertIn(f"**{label}**", section)
                norm = section.split("**编写规范**：", 1)[1].split("\n\n", 1)[0]
                self.assertGreater(len(norm), 55)
                self.assertGreaterEqual(norm.count("。"), 2)
                self.assertTrue(section.split("</details>", 1)[1].strip())
        titles = [title for _, title in chapters]
        for needed in ("系统概览", "子系统与直属模块概要设计", "运行组织与部署设计", "重要过程",
                       "配置与环境管理设计", "开发、构建与交付设计"):
            self.assertIn(needed, titles)
        for removed in ("硬件实现方案", "可编程逻辑与专用处理单元", "结构、热、工艺与安全设计"):
            self.assertNotIn(removed, titles)

    def test_architecture_precedes_functions_and_object_detail(self):
        text = TEMPLATE.read_text()
        ordered = ("## 3. 系统概览", "### 3.1 软件系统架构",
                   "![虚构软件系统的直属组成]", "### 3.2 组成与职责",
                   "### 3.3 总体方案、选择依据与替代方案",
                   "### 3.4 约束分配与下游保证", "### 3.5 机制清单与文档映射",
                   "## 4. 功能与用户交互设计", "## 5. 子系统与直属模块概要设计",
                   "### 5.1 直属对象概要设计", "## 6. 运行组织与部署设计")
        positions = [text.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(text.count("software-design-composition.svg"), 1)
        self.assertEqual(text.count("| 对象 ID / 类型 / 父对象 |"), 1)
        runtime = text.index("software-design-runtime.svg")
        self.assertGreater(runtime, text.index("## 6. 运行组织与部署设计"))
        self.assertLess(runtime, text.index("## 7. 重要过程"))
        guide = (ROOT / "docs/ai-guides/software-system.md").read_text()
        self.assertIn("全系统架构图放在模板 §3.1 正文开头", guide)
        self.assertIn("对象总表在 §3.2 唯一维护", guide)
        for stale in ("§5 讲静态组成", "§3.2 → §5.1", "§5 直属组成"):
            self.assertNotIn(stale, guide)
        selection = (ROOT / "docs/template-selection.md").read_text()
        for route in ("软件系统模板 §3.5", "软件系统 §9", "软件系统模板 §3.4",
                      "纯软件顶层的跨组件机制也使用 `design.system-mechanism`"):
            self.assertIn(route, selection)

    def test_cross_references_and_assets_resolve(self):
        text = TEMPLATE.read_text()
        headings = set(re.findall(r"(?m)^#{2,3} (\d+(?:\.\d+)*)\.? ", text))
        # Source-derivation references point to the original template, not this outline.
        body = text.split("派生来源：", 1)[0]
        for ref in re.findall(r"§(\d+(?:\.\d+)*)", body):
            self.assertIn(ref, headings)
        self.assertEqual(text.count("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->"), 11)
        self.assertEqual(text.count("<!-- STD_TEMPLATE_EXAMPLE_END -->"), 11)
        for ref in re.findall(r"\]\(([^)]+)\)", text):
            self.assertTrue((TEMPLATE.parent / ref).resolve().is_file(), ref)

    def test_practical_design_obligations_survive_derivation(self):
        text = TEMPLATE.read_text()
        for term in ("parent_document_id 可为空", "design_level=system", "不递归软件子系统",
                     "S01", "M201", "M001", "上级 Mechanism ID", "前置依赖", "预设计",
                     "自由度", "结果已知性", "访问安全", "操作终态", "资源释放", "重新准入",
                     "旧执行者停止或已隔离", "事实来源", "独立 Oracle", "prompt",
                     "并发测试与环境隔离", "自动化", "回滚", "指标", "日志", "自检",
                     "全部必需消费者", "request/response", "NOT_IMPLEMENTED", "唯一机器定义",
                     "Modeled/Simulated/Measured", "普通操作系统", "公共库"):
            self.assertIn(term, text)
        self.assertIn("格式工具 PASS 不证明设计质量", text)
        guide = (ROOT / "docs/ai-guides/software-system.md").read_text()
        for term in ("纯软件项目顶层", "总体系统的软件领域设计", "不重跑完整写作流程",
                     "逐能力", "事实来源", "不可", "全部必需消费者", "真实项目"):
            self.assertIn(term, guide)

    def test_generated_top_level_defaults_short_cover_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            generated = subprocess.run(self.command(directory), capture_output=True, text=True)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            base = Path(directory) / "docs/20_system_design"
            meta = json.loads((base / "example-software.metadata.json").read_text())
            md = (base / "example-software.md").read_text()
            self.assertEqual(meta["template_id"], "design.software-system")
            self.assertEqual(meta["document_type"], "design.software-system")
            self.assertEqual(meta["template_version"], "0.3.2")
            self.assertEqual(meta["template_sha256"], hashlib.sha256(TEMPLATE.read_bytes()).hexdigest())
            self.assertEqual(meta["design_level"], "system")
            self.assertEqual(meta["domain"], ["software"])
            self.assertIsNone(meta["parent_document_id"])
            self.assertEqual(meta["status"], "draft")
            self.assertNotIn("std_version", meta)
            for removed in ("{{", "EX-SOFTWARE-LAYERS", "../diagrams/", "派生来源：", "dead7e7"):
                self.assertNotIn(removed, md)
            cover = md.split("<!-- STD_DOCUMENT_COVER_END -->", 1)[0]
            self.assertEqual(len(re.findall(r"^\| [A-Z][^|]+ \|", cover, re.M)), 8)
            self.assertNotIn("| Authority |", cover)
            self.assertIn("| Authority |", md.split("## 附录 B.", 1)[1])
            self.assertIn("**编写规范**", md)
            checked = subprocess.run([str(ROOT / "scripts/validate-design"), directory,
                                      "--check-design-hierarchy", "--json"], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["design_parent_links"], {})

    def test_domain_mode_generation_and_parent_chain(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = self.command(directory, "example-total")
            parent[parent.index("design.software-system")] = "design.system"
            self.assertEqual(subprocess.run(parent, capture_output=True).returncode, 0)
            child = subprocess.run(self.command(directory) + ["--parent-document-id", "example-total"],
                                   capture_output=True, text=True)
            self.assertEqual(child.returncode, 0, child.stderr)
            checked = subprocess.run([str(ROOT / "scripts/validate-design"), directory,
                                      "--check-design-hierarchy", "--json"], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["design_parent_links"],
                             {"example-software": "example-total"})

    def test_wrong_level_does_not_write_even_with_output_override(self):
        with tempfile.TemporaryDirectory() as directory:
            for level in ("module", "subsystem", "cross-level"):
                generated = subprocess.run(self.command(directory) + ["--level", level, "--output", directory],
                                           capture_output=True, text=True)
                self.assertNotEqual(generated.returncode, 0)
                self.assertIn("必须使用 system", generated.stderr)
                self.assertEqual(list(Path(directory).iterdir()), [])

    def test_hierarchy_rejects_wrong_software_role_and_parent(self):
        audit = runpy.run_path(str(ROOT / "scripts/validate-design"))["validate_design_hierarchy"]
        node = {"document_id": "SW", "template_id": "design.software-system", "design_level": "module",
                "parent_document_id": None, "project": "example"}
        errors, _ = audit([(Path("sw.json"), node)])
        self.assertIn("hierarchy.type", {e["code"] for e in errors})
        node.update(design_level="system", parent_document_id="MOD")
        parent = {"document_id": "MOD", "template_id": "design.definition", "design_level": "module",
                  "parent_document_id": None, "project": "example"}
        errors, _ = audit([(Path("sw.json"), node), (Path("mod.json"), parent)])
        self.assertIn("hierarchy.parent-type", {e["code"] for e in errors})

    def test_catalog_navigation_and_pending_markers_are_updated(self):
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        self.assertEqual(catalog["templates"]["design.software-system"], "design/software-system-design.md")
        self.assertEqual(catalog["template_versions"]["design.software-system"], "0.3.2")
        for name in ("README.md", "docs/template-selection.md", "docs/ai-system-design-authoring-guide.md",
                     "docs/ai-guides/unit-design.md"):
            text = (ROOT / name).read_text()
            self.assertIn("design.software-system", text)
            self.assertNotIn("软件系统专用模板待建立", text)
            self.assertNotIn("软件系统专用模板尚待建立", text)


    def test_architecture_method_separates_layers_objects_and_names(self):
        guide = (ROOT / "docs/ai-guides/software-system.md").read_text()
        for term in ("先形成架构，再选择样式", "先定视图和边界", "先识别真实组成",
                     "用一致的架构依据分层", "框内写具体英文组件名", "图后说明，再做语义复审",
                     "直属模块", "内部子系统", "都不能作为上下架构层", "不强制四层",
                     "WebUI", "CLI", "不以英文字符或色块数量自动判合格"):
            self.assertIn(term, guide)
        chapter = TEMPLATE.read_text().split("### 3.1 软件系统架构", 1)[1].split("### 3.2", 1)[0]
        self.assertIn("软件系统 AI 指南 §4", chapter)
        self.assertIn("不能用“直属模块、内部子系统、既有公共支撑”", chapter)
        self.assertLess(chapter.index("software-system-layered-example.png"),
                        chapter.index("software-design-composition.svg"))
        self.assertIn("不是完整软件架构范例", chapter)

    def test_new_layer_sample_has_actual_english_component_names(self):
        import xml.etree.ElementTree as ET
        svg = ROOT / "templates/diagrams/software-system-layered-example.svg"
        tree = ET.parse(svg)
        ns = {"s": "http://www.w3.org/2000/svg"}
        names = ["".join(node.itertext()) for node in tree.findall('.//s:text[@class="name"]', ns)]
        self.assertEqual(names, ["WebUI", "CLI", "InspectionService", "ImageAnalyzer",
                                 "CameraDriver", "AcquisitionDriver", "Bootloader", "BSP"])
        self.assertTrue(all(name.isascii() for name in names))
        self.assertIn("按需定制", svg.read_text())
        self.assertIn("普通操作系统不作为自研组件展开", svg.read_text())
        self.assertTrue(svg.with_suffix(".png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
