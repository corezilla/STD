"""ISD delivery relations and filled slots; no assertion of design quality."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_validate_design import load_validator

ROOT = Path(__file__).resolve().parents[1]
ITEMS = "scope structure data functions algorithms lifecycle resources security persistence verification".split()


class ISDDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.validator = load_validator()
        self.module = dict(document_id="MOD", project="p", status="draft", design_object_id="M201",
                           parent_document_id="SYS", template_id="design.definition",
                           design_level="module", domain=["software"])
        self.view = dict(self.module, document_id="ISD", template_id="design.implementation",
                         implementation_view_of_document_id="MOD", volume_of_document_id=None)
        self.module["implementation_specification"] = dict(
            mode="separate", document_id="ISD", reason=None, decision_ref=None,
            coverage_mapping=[dict(item=i, document_id="ISD", anchor="isd-" + i,
                                   applicability="applicable", reason=None, decision_ref=None) for i in ITEMS])
        self.records = [self.record(self.module), self.record(self.view)]
        self.write_body("ISD")

    def record(self, data):
        return (self.root / (data["document_id"] + ".metadata.json"), data)

    def table(self, cells, headers=None):
        headers = headers or ["column" + str(i) for i in range(len(cells))]
        return "| " + " | ".join(headers) + " |\n" + \
               "|" + "---|" * len(cells) + "\n| " + " | ".join(cells) + " |\n"

    def write_body(self, doc):
        text = '<a id="isd-handoff"></a>\n' + self.table(["R1", "MOD v1", "decode", "source", "inline", "V1"])
        for i in ITEMS:
            text += '\n<a id="isd-' + i + '"></a>\n'
            if i == "verification":
                text += self.table(
                    ["R1", "V1/C1/v1", "input", "expected", "NOT_RUN", "NOT_RUN", "test", "NOT_RUN"],
                    ["Rule/成员", "V / Case / Vector", "输入/故障/环境", "Oracle/Expected",
                     "Actual/Evidence", "Verdict", "测试入口/清理", "Run ID/Status"])
            elif i in {"security", "persistence"}:
                text += self.table(["R1", "input", "check", "reject", "transform", "boundary", "V1"])
            else:
                text += "decode receives immutable input and returns the first validated frame.\n"
        (self.root / (doc + ".md")).write_text(text)

    def write_fixed_body(self, doc):
        def record(title, fields):
            return "#### " + title + "\n\n" + "\n".join(
                "- **" + key + "**：" + value for key, value in fields) + "\n"
        text = '<a id="isd-handoff"></a>\n' + record("1.2.1 H1", [
            ("上游信息项 / 规则 ID", "R1"),
            ("固定来源 / 版本 / 锚点 / 摘要", "MOD v1"),
            ("ISD 细化内容 / 章节", "decode"),
            ("唯一权威位置", "source"),
            ("实现自由度", "inline"),
            ("原 V/Case 及本地验证位置", "V1"),
        ])
        for item in ITEMS:
            text += '\n<a id="isd-' + item + '"></a>\n'
            if item == "verification":
                text += record("9.1.1 V1", [
                    ("Rule / 成员", "R1"), ("V / Case / Vector", "V1/C1/v1"),
                    ("输入 / 故障 / 环境", "input"), ("Oracle / Expected", "expected"),
                    ("Actual / Evidence", "NOT_RUN"), ("Verdict", "NOT_RUN"),
                    ("测试入口 / 清理", "test"), ("Run ID / Status", "NOT_RUN"),
                ])
            elif item == "persistence":
                text += record("7.2.1.1 P1", [
                    ("原规则 / 事务", "R1"), ("原子范围 / 事务外副作用", "row / none"),
                    ("开始 / 提交 / 回滚函数", "begin/commit/rollback"),
                    ("持久提交点 / 对外响应点", "commit / return"),
                    ("响应丢失后的权威核对", "read record"),
                    ("恢复入口 / 判定记录 / 重复恢复条件", "recover / ledger / idempotent"),
                    ("验证项", "V1"),
                ])
            elif item == "security":
                text += record("7.3.1.1 S1", [
                    ("原规则", "R1"), ("可信输入 / 敏感字段 / 检查对象", "request"),
                    ("检查函数 / 时点", "check before write"),
                    ("拒绝 / 宿主交付出口", "reject"), ("脱敏 / 禁止输出", "redact"),
                    ("日志 / 指标 / trace 口径及触发", "counter on reject"),
                    ("验证项", "V1"),
                ])
            else:
                text += "decode receives immutable input and returns the first validated frame.\n"
        (self.root / (doc + ".md")).write_text(text)

    def codes(self):
        return {e["code"] for e in self.validator.validate_isd_delivery(self.records)}

    def test_separate_and_embedded_are_valid(self):
        self.assertEqual(self.codes(), set())

    def test_fixed_record_delivery_is_valid(self):
        self.write_fixed_body("ISD")
        self.assertEqual(self.codes(), set())

    def test_embedded_delivery_is_valid(self):
        self.records.pop()
        spec = self.module["implementation_specification"]
        spec.update(mode="embedded", document_id="MOD")
        for row in spec["coverage_mapping"]:
            row["document_id"] = "MOD"
        self.write_body("MOD")
        self.assertEqual(self.codes(), set())

    def test_fixed_verification_record_allows_supporting_matrix(self):
        self.write_fixed_body("ISD")
        path = self.root / "ISD.md"
        body = path.read_text()
        marker = '<a id="isd-verification"></a>\n'
        matrix = self.table(["empty database", "schema absent", "initialize"])
        path.write_text(body.replace(marker, marker + matrix, 1))
        self.assertEqual(self.codes(), set())

    def test_wrong_module_project_object_or_parent_is_rejected(self):
        for field, value in [("implementation_view_of_document_id", "ABSENT"),
                             ("project", "other"), ("design_object_id", "M202"),
                             ("parent_document_id", "OTHER")]:
            with self.subTest(field=field):
                old = self.view[field]
                self.view[field] = value
                self.assertIn("isd.view-of", self.codes())
                self.view[field] = old

    def test_duplicate_root_and_missing_reverse_link(self):
        duplicate = dict(self.view, document_id="ISD2")
        self.records.append(self.record(duplicate))
        self.assertIn("isd.root-conflict", self.codes())
        self.records.pop()
        self.module["implementation_specification"]["document_id"] = "ABSENT"
        self.assertIn("isd.reciprocal", self.codes())

    def test_volume_must_be_same_object_direct_and_used(self):
        volume = dict(self.view, document_id="VOL", volume_of_document_id="ISD")
        self.records.append(self.record(volume))
        self.write_body("VOL")
        self.assertIn("isd.unused-volume", self.codes())
        self.module["implementation_specification"]["coverage_mapping"][0]["document_id"] = "VOL"
        self.assertEqual(self.codes(), set())
        volume["volume_of_document_id"] = "VOL"
        self.assertIn("isd.volume", self.codes())
        volume["volume_of_document_id"] = "ISD"
        volume["design_object_id"] = "M202"
        self.assertIn("isd.view-of", self.codes())

    def test_missing_registration_and_missing_mode(self):
        spec = self.module.pop("implementation_specification")
        self.assertIn("isd.registration", self.codes())
        self.module["implementation_specification"] = dict(spec, mode="missing")
        self.assertIn("isd.missing", self.codes())

    def test_empty_handoff_and_duplicate_coverage_rejected(self):
        path = self.root / "ISD.md"
        path.write_text(path.read_text().replace("| R1 | MOD v1 | decode | source | inline | V1 |", "| | | | | | |"))
        self.assertIn("isd.handoff", self.codes())
        mapping = self.module["implementation_specification"]["coverage_mapping"]
        mapping[-1] = copy.deepcopy(mapping[0])
        self.assertIn("isd.coverage", self.codes())

    def test_help_and_header_only_do_not_count(self):
        path = self.root / "ISD.md"
        path.write_text(path.read_text().replace(
            "decode receives immutable input and returns the first validated frame.",
            "<details>Author instructions are not design.</details>\n<!-- TODO -->"))
        self.assertIn("isd.empty", self.codes())

    def test_verdict_requires_actual_and_run_but_not_run_is_legal(self):
        self.assertEqual(self.codes(), set())
        path = self.root / "ISD.md"
        original = path.read_text()
        path.write_text(original.replace("| NOT_RUN | NOT_RUN | test | NOT_RUN |", "| NOT_RUN | PASS | test | NOT_RUN |"))
        self.assertIn("isd.evidence", self.codes())
        path.write_text(original.replace("| NOT_RUN | NOT_RUN | test | NOT_RUN |", "| observed result / evidence | PASS | test | RUN1 |"))
        self.assertEqual(self.codes(), set())
        path.write_text(original.replace("| NOT_RUN | NOT_RUN | test | NOT_RUN |", "| | NOT_RUN | test | NOT_RUN |"))
        self.assertIn("isd.verification", self.codes())

    def test_conditional_table_and_accepted_applicability(self):
        entry = next(e for e in self.module["implementation_specification"]["coverage_mapping"] if e["item"] == "persistence")
        path = self.root / "ISD.md"
        body = path.read_text()
        start = body.index('<a id="isd-persistence">')
        end = body.index('<a id="isd-verification">')
        path.write_text(body[:start] + '<a id="isd-persistence"></a>\nNo stored state.\n' + body[end:])
        self.assertIn("isd.conditional-record", self.codes())
        entry.update(applicability="not_applicable", reason="stateless library", decision_ref="TAILOR#scope")
        self.assertIn("isd.applicability", self.codes())
        d = dict(document_id="TAILOR", project="p", status="accepted", template_id="management.tailoring")
        self.records.append(self.record(d))
        (self.root / "TAILOR.md").write_text('<a id="scope"></a>\nM201 has no persistent state.\n')
        self.assertEqual(self.codes(), set())
        d["status"] = "draft"
        self.assertIn("isd.applicability", self.codes())

    def test_not_required_needs_decision(self):
        self.records.pop()
        self.module["implementation_specification"].update(mode="not_required", document_id=None,
            coverage_mapping=[], reason="External binary only", decision_ref="TAILOR#scope")
        self.assertIn("isd.exemption", self.codes())
        d = dict(document_id="TAILOR", project="p", status="accepted", template_id="management.tailoring")
        self.records.append(self.record(d))
        (self.root / "TAILOR.md").write_text('<a id="scope"></a>\nNo source implementation in this scope.\n')
        self.assertEqual(self.codes(), set())

    def test_generated_blank_isd_fails_delivery_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/new-design"),
            "--project", "p", "--template", "design.implementation", "--name", "EMPTY",
            "--project-root", str(self.root), "--owner", "o", "--author", "a", "--repository", "p/r",
            "--design-object-id", "M201", "--implementation-view-of-document-id", "MOD"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate-design"),
            str(self.root / "docs"), "--check-isd-delivery", "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["isd_delivery_checked"])
        self.assertTrue(any(i["code"] == "isd.view-of" for i in report["issues"]))
        self.assertTrue((self.root / "docs/50_implementation_design/EMPTY.isd.md").is_file())
        self.assertTrue((self.root / "docs/50_implementation_design/EMPTY.isd.metadata.json").is_file())


if __name__ == "__main__":
    unittest.main()
