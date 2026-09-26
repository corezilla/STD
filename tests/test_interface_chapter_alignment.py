"""Guard the common interface-design entry across software template levels."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "architecture-design.md": 10,
    "software-system-design.md": 8,
    "system-mechanism-design.md": 5,
    "subsystem-design.md": 6,
    "design-definition.md": 9,
    "implementation-design.md": 5,
}
SHARED_SECTIONS = (
    "API（适用时）",
    "消息与数据流接口（适用时）",
    "硬件与固件接口（适用时）",
    "人机与维护接口（适用时）",
)


class InterfaceChapterAlignmentTests(unittest.TestCase):
    def test_six_software_templates_share_chapter_and_base_sections(self):
        for filename, chapter in TEMPLATES.items():
            with self.subTest(template=filename):
                source = (ROOT / "templates/design" / filename).read_text()
                marker = f"## {chapter}. 接口设计\n"
                self.assertIn(marker, source)
                body = source.split(marker, 1)[1].split("\n## ", 1)[0]
                headings = re.findall(rf"^### {chapter}\.(\d+) (.+)$", body, re.M)
                self.assertEqual(
                    headings[:4],
                    [(str(index), title) for index, title in enumerate(SHARED_SECTIONS, 1)],
                )
                for term in ("Interface/Member ID", "唯一", "错误", "验证"):
                    self.assertIn(term, body)
                self.assertNotRegex(body, rf"(?m)^### {chapter}\.\d+ 接口清单$")
                communication = body.split(f"### {chapter}.2 消息与数据流接口（适用时）\n", 1)[1].split(f"### {chapter}.3 ", 1)[0]
                self.assertIn("内部协作即使使用 HTTP/RPC", communication)

    def test_standard_maps_shared_and_specialized_sections(self):
        standard = (ROOT / "docs/design-data-interface-format.md").read_text()
        for title in SHARED_SECTIONS:
            self.assertIn(f"**{title.split('（')[0]}**", standard)
        for template_id in (
            "design.system", "design.software-system", "design.system-mechanism",
            "design.subsystem", "design.definition", "design.implementation",
        ):
            self.assertIn(f"| `{template_id}` |", standard)
        self.assertIn("不逐接口维护全量调用函数反向索引", standard)
        self.assertIn("不把同一接口的定义、交互、异常和示例拆散", standard)
        self.assertIn("不能只按传输协议判断类别", standard)


if __name__ == "__main__":
    unittest.main()
