"""Public system error records are structurally complete and indexed."""

import runpy
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
validate = runpy.run_path(str(ROOT / "scripts/validate-public-error-catalog"))[
    "validate_public_error_catalog"
]


def document(records: str, index: str) -> str:
    return (
        "## 8.4 系统公共错误码目录与下级承接\n"
        "<!-- STD_PUBLIC_ERROR_CATALOG_BEGIN -->\n" + records +
        "\n<!-- STD_PUBLIC_ERROR_CATALOG_END -->\n"
        "| Error ID | 接口成员 ID | 机制/子系统/模块及使用方式 | 设计 V / Case |\n"
        "|---|---|---|---|\n" + index + "\n## 9. 接口\n"
    )


def record(error_id="ERR-INPUT", code="E100") -> str:
    fields = {
        "定义与适用范围": "输入与既有请求冲突，不含传输失败",
        "触发条件与判定者": "入口比较已受理请求的输入摘要",
        "结果与副作用": "本次拒绝且原任务不变",
        "错误载荷": "ErrorPayload 类型及 request_id 必填",
        "调用方动作": "修正输入后以新请求标识提交",
        "模块承接": "API 产生，UI 消费并提示修正",
        "唯一来源与兼容": "errors.schema.json rev 2 / selector E100 / sha256 固定",
        "验证": "V-ERR-01 与 Case-ERR-01",
    }
    return "\n".join([f"**{error_id} · {code}**", *(
        f"- **{key}**：{value}" for key, value in fields.items()
    )])


class PublicErrorCatalogTests(unittest.TestCase):
    def test_template_entry_points_and_system_catalogs(self):
        templates = (
            "design/architecture-design.md", "design/software-system-design.md",
            "design/system-mechanism-design.md", "design/subsystem-design.md",
            "design/design-definition.md", "design/implementation-design.md",
            "design/hardware-design.md", "design/fpga-design.md",
            "design/data-dictionary.md", "contracts/contract-specification.md",
            "interfaces/interface-control.md",
        )
        for name in templates:
            with self.subTest(template=name):
                text = (ROOT / "templates" / name).read_text()
                self.assertRegex(text, r"Data/Type(?:/Error)? ID|类型成员 ID|数据结构")
                self.assertRegex(text, r"Error ID|公共错误码")
        for name in templates[:2]:
            text = (ROOT / "templates" / name).read_text()
            self.assertEqual(text.count("<!-- STD_PUBLIC_ERROR_CATALOG_BEGIN -->"), 1)
            self.assertEqual(text.count("<!-- STD_PUBLIC_ERROR_CATALOG_END -->"), 1)

    def test_complete_record_and_index(self):
        result = validate(document(record(), "| ERR-INPUT | IF-API#POST | API 产生，UI 消费 | V-ERR-01 |"))
        self.assertTrue(result["ok"], result)

    def test_missing_field_duplicate_code_and_missing_index_fail(self):
        incomplete = record().replace("- **错误载荷**：ErrorPayload 类型及 request_id 必填\n", "")
        result = validate(document(incomplete + "\n" + record("ERR-OTHER"), ""))
        self.assertFalse(result["ok"])
        self.assertTrue(any("缺少字段" in item for item in result["errors"]))
        self.assertTrue(any("重复错误代码值" in item for item in result["errors"]))
        self.assertTrue(any("缺少接口/下级/验证" in item for item in result["errors"]))

    def test_placeholder_and_unknown_reference_fail(self):
        result = validate(document(record().replace("E100", "<code>"),
                                   "| ERR-MISSING | IF-API#POST | API | V-ERR-01 |"))
        self.assertFalse(result["ok"])
        self.assertTrue(any("占位符" in item or "未填" in item for item in result["errors"]))
        self.assertTrue(any("未定义" in item for item in result["errors"]))

    def test_no_public_code_requires_tailoring(self):
        self.assertTrue(validate(document("N/A：无对外错误；tailoring decision T-01", ""))["ok"])
        self.assertFalse(validate(document("", ""))["ok"])


if __name__ == "__main__":
    unittest.main()
