"""Guard the paragraph-length authoring help in compact document templates."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPACT_FAMILIES = (
    "assurance",
    "decisions",
    "evaluation",
    "hardware",
    "management",
    "operations",
    "product",
    "requirements",
    "review",
)


class CompactTemplateGuidanceTests(unittest.TestCase):
    def test_every_section_has_actionable_collapsible_guidance(self):
        for family in COMPACT_FAMILIES:
            for path in (ROOT / "templates" / family).glob("*.md"):
                lines = path.read_text(encoding="utf-8").splitlines()
                headings = [i for i, line in enumerate(lines) if line.startswith("## ")]
                self.assertTrue(headings, path)
                for index in headings:
                    with self.subTest(template=path.name, section=lines[index]):
                        following = index + 1
                        while following < len(lines) and not lines[following].strip():
                            following += 1
                        self.assertEqual(lines[following], "<details>")
                        closing = lines.index("</details>", following)
                        guidance = "\n".join(lines[following : closing + 1])
                        self.assertIn("编写建议", guidance)
                        self.assertTrue(
                            "完成检查：" in guidance or "**完成条件**" in guidance
                        )
                        self.assertGreaterEqual(len(guidance), 120)


if __name__ == "__main__":
    unittest.main()
