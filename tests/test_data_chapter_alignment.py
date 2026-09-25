"""Keep the software design data chapter aligned across template levels."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "architecture-design.md": 9,
    "software-system-design.md": 8,
    "system-mechanism-design.md": 4,
    "subsystem-design.md": 5,
    "design-definition.md": 6,
    "implementation-design.md": 4,
}
SHARED_SECTIONS = (
    "数据结构清单",
    "数据结构定义",
    "状态、所有权与生命周期",
    "示例与验证",
)


class DataChapterAlignmentTests(unittest.TestCase):
    def test_six_software_templates_share_chapter_and_base_sections(self):
        for filename, chapter in TEMPLATES.items():
            with self.subTest(template=filename):
                text = (ROOT / "templates/design" / filename).read_text()
                self.assertIn(f"## {chapter}. 数据结构设计\n", text)
                headings = re.findall(rf"^### {chapter}\.(\d+) (.+)$", text, re.M)
                self.assertEqual(
                    headings[:4],
                    [(str(index), title) for index, title in enumerate(SHARED_SECTIONS, 1)],
                )
                chapter_text = text.split(f"## {chapter}. 数据结构设计\n", 1)[1].split(
                    "\n## ", 1
                )[0]
                for term in ("Data/Type ID", "唯一来源", "合法", "拒绝"):
                    self.assertIn(term, chapter_text)

    def test_system_error_catalogs_remain_in_data_chapters(self):
        for filename, chapter, subsection in (
            ("architecture-design.md", 9, 10),
            ("software-system-design.md", 8, 8),
        ):
            with self.subTest(template=filename):
                text = (ROOT / "templates/design" / filename).read_text()
                data_chapter = text.split(f"## {chapter}. 数据结构设计\n", 1)[1].split(
                    "\n## ", 1
                )[0]
                self.assertIn(
                    f"### {chapter}.{subsection} 系统公共错误码目录与下级承接",
                    data_chapter,
                )
                self.assertIn("STD_PUBLIC_ERROR_CATALOG_BEGIN", data_chapter)

    def test_standard_maps_shared_and_specialized_sections(self):
        standard = (ROOT / "docs/design-data-interface-format.md").read_text()
        for title in SHARED_SECTIONS:
            self.assertIn(f"**{title}**", standard)
        for template_id in (
            "design.system",
            "design.software-system",
            "design.system-mechanism",
            "design.subsystem",
            "design.definition",
            "design.implementation",
        ):
            self.assertIn(f"| `{template_id}` |", standard)


if __name__ == "__main__":
    unittest.main()
