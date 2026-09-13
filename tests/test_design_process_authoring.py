"""Guard writing requirements and teaching links, not design or runtime quality."""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DesignProcessAuthoringTests(unittest.TestCase):
    def test_example_routing_and_existing_outline_quality_rules(self):
        guide = (ROOT / "docs/ai-guides/software-system.md").read_text()
        self.assertNotIn("虚构完整主线示例", guide)
        self.assertIn("虚构场景摘要（不是完整设计）", guide)
        self.assertIn("不涵盖控制进程崩溃后的持久任务恢复", guide)
        self.assertIn("保持现有模板目录", guide)
        link = "../examples/mechanism-side-effect-example.md"
        self.assertIn(link, guide)
        self.assertTrue((ROOT / "docs/ai-guides" / link).resolve().is_file())
        norm = (ROOT / "docs/design-writing-guide.md").read_text()
        self.assertIn("在既有目录内完成设计", norm)
        self.assertIn("不是机械查找", norm)
        self.assertIn("不能为了显得具体而编造", norm)

    def test_readme_common_guide_version_matches(self):
        guide = (ROOT / "docs/ai-authoring-guide.md").read_text()
        version = re.search(r"版本：([^ ]+)", guide).group(1)
        readme = (ROOT / "README.md").read_text()
        self.assertIn(f"（`{version}`）", readme)

    def test_problem_solving_loop_and_replay_are_required(self):
        for name in ("docs/design-writing-guide.md", "docs/ai-authoring-guide.md",
                     "docs/ai-guides/software-system.md",
                     "templates/design/software-system-design.md"):
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                self.assertIn("问题 → 选定方案 → 具体输入推演 → 失败推演 → 下游承接", text)
                self.assertIn("无口头补充复演", text)
                self.assertIn("职责表", text)

    def test_process_diagram_requirement_is_explicit_at_writing_entries(self):
        for name in (
            "docs/design-writing-guide.md",
            "docs/ai-authoring-guide.md",
            "docs/ai-guides/software-system.md",
            "templates/design/software-system-design.md",
            "templates/design/subsystem-design.md",
        ):
            with self.subTest(name=name):
                self.assertIn("每个重要流程必须有流程图或时序图", (ROOT / name).read_text())
        norm = (ROOT / "docs/design-writing-guide.md").read_text()
        for term in ("Stage DAG", "图文核对", "多个过程可以共用一张图", "设计缺口"):
            self.assertIn(term, norm)

    def test_complete_sample_is_reachable_and_teaching_only(self):
        sample = ROOT / "docs/examples/software-startup-design-example.md"
        for name in ("README.md", "docs/design-writing-guide.md",
                     "docs/ai-guides/software-system.md",
                     "templates/design/software-system-design.md"):
            path = ROOT / name
            links = re.findall(r"\]\(([^)]+software-startup-design-example\.md)\)", path.read_text())
            self.assertTrue(links, name)
            for link in links:
                self.assertEqual((path.parent / link).resolve(), sample)
        text = sample.read_text()
        for term in ("本例全部虚构", "Target", "Planned", "NOT_RUN", "```mermaid",
                     "P-START", "S1", "S5", "F1", "W1", "事实", "哈希不符",
                     "退出确认", "迟到 READY", "下游", "以上用例尚未执行"):
            self.assertIn(term, text)

    def test_guides_require_substantive_trial_not_structure_pass(self):
        text = (ROOT / "docs/ai-guides/software-system.md").read_text()
        for term in ("先完成一节，再扩写整篇", "具体输入", "事实来源",
                     "不是运行 PASS", "不能把它评为设计完成"):
            self.assertIn(term, text)
        common = (ROOT / "docs/ai-authoring-guide.md").read_text()
        self.assertIn("legacy-mapped", common)
        self.assertIn("不能将", common)

    def test_template_ends_with_visible_prose_and_flow_example(self):
        text = (ROOT / "templates/design/software-system-design.md").read_text()
        sample = text.rsplit("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->", 1)[1]
        self.assertTrue(text.rstrip().endswith("<!-- STD_TEMPLATE_EXAMPLE_END -->"))
        for term in ("完整写法示例", "**用途与方案**", "**过程图**", "```mermaid",
                     "**正常路径及就绪判据**", "**失败与恢复**", "代表输入 / 故障",
                     "EX-SEARCH/v1", "实际测试尚未执行"):
            self.assertIn(term, sample)

    def test_generator_keeps_requirement_without_filling_project_design(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([
                str(ROOT / "scripts/new-design"), "--project", "example",
                "--template", "design.software-system", "--name", "process-check",
                "--project-root", directory, "--title", "示例软件系统设计",
                "--owner", "Example Owner", "--author", "Example Author",
                "--repository", "example/repo",
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            files = list(Path(directory).rglob("process-check.md"))
            self.assertEqual(len(files), 1)
            text = files[0].read_text()
            self.assertIn("每个重要流程必须有流程图或时序图", text)
            self.assertIn("图号 / 图内路径 / 正文位置", text)
            self.assertNotIn("EX-SEARCH", text)
            self.assertNotIn("software-startup-design-example.md", text)


if __name__ == "__main__":
    unittest.main()
