"""Tool-neutral STD entry links must survive generation and cover synchronization."""
import json
import re
import runpy
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


class STDEntryTests(unittest.TestCase):
    def test_every_registered_cover_links_to_main_readme(self):
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        sync = runpy.run_path(str(ROOT / "scripts/sync-template-covers"))
        front, back = sync["split_cover"]((ROOT / "templates/_shared/document-cover.md").read_text())
        self.assertIn("> STD 使用入口：", front)
        self.assertNotIn("> STD 使用入口：", back)
        for relative in catalog["templates"].values():
            path = ROOT / "templates" / relative
            text = path.read_text()
            cover = text.split("<!-- STD_DOCUMENT_COVER_END -->", 1)[0]
            with self.subTest(template=relative):
                self.assertEqual(text.count("> STD 使用入口："), 1)
                self.assertIn("[STD 主说明与执行流程](../../README.md)", cover)
                self.assertEqual((path.parent / "../../README.md").resolve(), ROOT / "README.md")

    def test_all_generated_covers_keep_portable_navigation_not_instructions(self):
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project with spaces"
            project.mkdir()
            readme = project / "README.md"
            readme.write_text('# Example\n<a id="std-entry"></a>\n')
            for template_id in catalog["templates"]:
                with self.subTest(template=template_id):
                    output = project / "custom docs" / template_id
                    result = subprocess.run([str(ROOT / "scripts/new-design"),
                        "--template", template_id, "--name", "example", "--project", "example",
                        "--project-root", str(project), "--output", str(output),
                        "--owner", "owner", "--author", "author", "--repository", "example/repo"],
                        capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    text = (output / "example.md").read_text()
                    cover = text.split("<!-- STD_DOCUMENT_COVER_END -->", 1)[0]
                    link = re.search(r"\[项目采用说明与标准导航\]\(([^)]+)\)", cover)[1]
                    self.assertTrue(link.endswith("#std-entry"))
                    self.assertEqual((output / unquote(link.split('#')[0])).resolve(), readme.resolve())
                    self.assertNotIn("作者先读入口", text)
            self.assertEqual(readme.read_text(), '# Example\n<a id="std-entry"></a>\n')

    def test_readme_scaffold_and_execution_entry(self):
        text = (ROOT / "templates/_shared/project-readme.md").read_text()
        self.assertLess(text.index('id="std-entry"'), text.index("## 快速开始"))
        self.assertIn("blob/{{std_source_revision}}/README.md", text)
        self.assertIn("STD `{{adopted_std_version}}`", text)
        main = (ROOT / "README.md").read_text()
        self.assertLess(main.index('id="std-entry"'), main.index("## 核心规则"))
        for term in ("确认采用来源", "选择正确的文档", "读取编写方法", "检查实际交付", "按授权交付"):
            self.assertIn(term, main)
