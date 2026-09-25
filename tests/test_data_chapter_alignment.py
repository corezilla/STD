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
    "公共基础类型与枚举（适用时）",
    "业务与操作数据结构（适用时）",
    "配置与规则数据结构（适用时）",
    "通信报文结构（适用时）",
    "设备与 FPGA 表项结构（适用时）",
    "运行状态数据结构（适用时）",
    "数据库表结构（适用时）",
    "错误码与错误结构（适用时）",
)


class DataChapterAlignmentTests(unittest.TestCase):
    def test_six_software_templates_share_chapter_and_base_sections(self):
        for filename, chapter in TEMPLATES.items():
            with self.subTest(template=filename):
                text = (ROOT / "templates/design" / filename).read_text()
                self.assertIn(f"## {chapter}. 数据结构设计\n", text)
                headings = re.findall(rf"^### {chapter}\.(\d+) (.+)$", text, re.M)
                self.assertEqual(
                    headings[:8],
                    [(str(index), title) for index, title in enumerate(SHARED_SECTIONS, 1)],
                )
                numbers = [number for number, _ in headings]
                self.assertEqual(len(numbers), len(set(numbers)))
                chapter_text = text.split(f"## {chapter}. 数据结构设计\n", 1)[1].split(
                    "\n## ", 1
                )[0]
                for term in ("Data/Type ID", "唯一来源", "合法", "拒绝"):
                    self.assertIn(term, chapter_text)

    def test_system_error_catalogs_remain_in_data_chapters(self):
        for filename, chapter, subsection in (
            ("architecture-design.md", 9, 8),
            ("software-system-design.md", 8, 8),
        ):
            with self.subTest(template=filename):
                text = (ROOT / "templates/design" / filename).read_text()
                data_chapter = text.split(f"## {chapter}. 数据结构设计\n", 1)[1].split(
                    "\n## ", 1
                )[0]
                self.assertIn(
                    f"### {chapter}.{subsection} 错误码与错误结构（适用时）",
                    data_chapter,
                )
                self.assertIn("STD_PUBLIC_ERROR_CATALOG_BEGIN", data_chapter)

    def test_data_dictionary_keeps_each_structure_in_one_category(self):
        text = (ROOT / "templates/design/data-dictionary.md").read_text()
        self.assertIn("## 3. 数据结构设计\n", text)
        headings = re.findall(r"^### 3\.(\d+) (.+)$", text, re.M)
        self.assertEqual(
            headings,
            [(str(index), title) for index, title in enumerate(SHARED_SECTIONS, 1)],
        )
        self.assertNotIn("Entity / Object Catalog", text)
        self.assertNotIn("## 4. Field Dictionary", text)
        self.assertIn("在同一处写完定义、字段、约束", text)
        self.assertIn("不拥有操作接口", text)

    def test_standard_maps_shared_and_specialized_sections(self):
        standard = (ROOT / "docs/design-data-interface-format.md").read_text()
        for title in SHARED_SECTIONS:
            self.assertIn(f"**{title.split('（', 1)[0]}**", standard)
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
