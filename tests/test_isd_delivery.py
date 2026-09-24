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
        data_rows = cells if cells and isinstance(cells[0], list) else [cells]
        headers = headers or ["column" + str(i) for i in range(len(data_rows[0]))]
        return "| " + " | ".join(headers) + " |\n" + \
               "|" + "---|" * len(headers) + "\n" + "".join(
                   "| " + " | ".join(row) + " |\n" for row in data_rows)

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
                    ("输入 / 故障 / 环境", "input"), ("独立 Oracle / Expected", "expected"),
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
                text += record("7.2.2 Schema policy", [
                    ("Schema authority / 当前版本事实来源", "schema table"),
                    ("允许的升级模式", "initialize only"),
                    ("明确不接受的迁移模式", "no incremental upgrade"),
                    ("兼容边界", "same version only"),
                    ("失败后的系统状态与责任方", "refuse start / owner"),
                ])
                text += record("7.2.2.1 S1", [
                    ("原规则", "schema v1"), ("升级 / 降级策略", "none"),
                    ("接受 / 拒绝条件", "accept v1; reject other"),
                    ("源 / 目标版本与转换函数", "v1 / v1 / none"),
                    ("拒绝后如何处理", "refuse start"), ("验证项", "V1"),
                ])
                text += self.table(
                    [["空库", "no tables", "initialize", "yes after cleanup"],
                     ["版本匹配", "version=v1", "start", "not needed"],
                     ["版本不匹配", "version!=v1", "refuse", "no"],
                     ["无版本表旧库", "tables without version", "refuse", "no"],
                     ["部分初始化", "subset of tables", "refuse", "after cleanup"],
                     ["完整性失败", "integrity check fails", "refuse", "after restore"]],
                    ["库状态", "判定事实", "启动结果", "是否允许重跑及条件"])
            elif item == "functions":
                text += record("5.1.1 F1", [
                    ("文件 / symbol / 可见性", "store.py/open/public"),
                    ("原成员 ID 或私有来源", "IF-1"),
                    ("完整签名与 caller", "open(path) / host"),
                    ("前置条件与校验顺序", "validate path then open"),
                    ("返回 / 错误优先级", "handle / path before storage"),
                    ("输入参数 / 数据结构 authority", "path / PathSpec IF-1"),
                    ("输入约束 / 校验顺序 / 失败映射", "non-empty then normalized / E1"),
                    ("成功输出 / 数据结构 / 后置条件", "StorageHandle / database open"),
                    ("错误输出 / 触发条件 / 优先级", "E1 INVALID_PATH before E2 STORAGE_BUSY"),
                    ("副作用 / 执行上下文 / 幂等性", "opens DB / caller thread / idempotent"),
                    ("输入输出 ownership 与寿命", "caller path / module handle"),
                    ("不可改变的规则 / Constraint ID", "CON-M201-001"),
                    ("实现自由度", "private connection helper"),
                    ("Thread-safe / reentrant", "yes / no"),
                    ("Nested-call policy", "forbidden inside transaction"),
                    ("Transaction participation", "creates new"),
                    ("Blocking / timeout / cancellation", "blocking / 1s / none"),
                    ("实现状态 / 验证项", "Planned / V1"),
                ])
                text += record("5.2.1 E1", [
                    ("底层异常 / 失败事实", "database locked"),
                    ("模块是否处理及处理函数", "translate in open"),
                    ("Typed 异常与原生异常所有权", "module owns StorageBusy"),
                    ("宿主 / public payload 或状态码", "SERVICE_BUSY"),
                    ("日志级别 / 脱敏 / 关联字段", "warning / redact path / request_id"),
                    ("是否可重试及前提", "yes after backoff"),
                    ("状态与副作用影响 / 验证项", "no commit / V1"),
                ])
            elif item == "security":
                text += record("7.3.1.1 S1", [
                    ("原规则", "R1"), ("可信输入 / 敏感字段 / 检查对象", "request"),
                    ("检查函数 / 时点", "check before write"),
                    ("拒绝 / 宿主交付出口", "reject"), ("脱敏 / 禁止输出", "redact"),
                    ("日志 / 指标 / trace 口径及触发", "counter on reject"),
                    ("验证项", "V1"),
                ])
            elif item == "algorithms":
                text += "```mermaid\nflowchart TD\nA[request] --> B[validate]\nB --> C[result]\n```\n"
            elif item == "resources":
                text += record("8.1 Configuration", [
                    ("适用性 / 固定 authority", "applicable / MOD#configuration"),
                    ("配置 key / 来源 / 优先级", "db.path / file then CLI"),
                    ("类型 / 单位 / 默认值 / 范围 / 字段约束", "path / none / existing parent"),
                    ("读取 / 解析 / 校验 symbol", "load_config / validate_path"),
                    ("生效点 / reload / 原子性 / 在途操作", "startup / no reload / atomic snapshot"),
                    ("缺失 / 非法 / 部分更新的错误出口", "E1 / no state change"),
                    ("敏感值存储 / 日志脱敏", "path redacted"),
                    ("验证项", "V1"),
                ])
            else:
                text += "decode receives immutable input and returns the first validated frame.\n"
        text += '\n<a id="isd-status"></a>\n' + record("10.2.1 ST1", [
            ("上游承接状态 / 固定来源", "MOD draft / MOD#status"),
            ("本层派生状态 / 事实依据", "PLANNED / no source yet"),
            ("§2 Current / Target", "N/A / target specified"),
            ("§3 / §5 文件与函数状态", "PLANNED"),
            ("§9 任务 / Actual / Verdict / Run", "PLANNED / NOT_RUN / NOT_RUN / NOT_RUN"),
            ("§10 汇总状态", "PLANNED / NOT_RUN"),
            ("差异解释 / Owner / 收敛动作", "none / Owner / implement"),
        ])
        (self.root / (doc + ".md")).write_text(text)

    def codes(self):
        return {e["code"] for e in self.validator.validate_isd_delivery(self.records)}

    def test_separate_and_embedded_are_valid(self):
        self.assertEqual(self.codes(), set())

    def test_fixed_record_delivery_is_valid(self):
        self.view["template_version"] = "0.4.0"
        self.write_fixed_body("ISD")
        self.assertEqual(self.codes(), set())

    def test_version_03_requires_function_schema_and_state_records(self):
        self.view["template_version"] = "0.3.0"
        self.write_fixed_body("ISD")
        path = self.root / "ISD.md"
        original = path.read_text()
        cases = [
            ("Thread-safe / reentrant**：yes / no", "Thread-safe / reentrant**：TODO",
             "isd.function-contract"),
            ("底层异常 / 失败事实**：database locked", "底层异常 / 失败事实**：TODO",
             "isd.error-propagation"),
            ("允许的升级模式**：initialize only", "允许的升级模式**：TODO",
             "isd.schema-policy"),
            ("| 完整性失败 | integrity check fails | refuse | after restore |",
             "| 完整性失败 | TODO | refuse | after restore |", "isd.schema-states"),
        ]
        for old, new, code in cases:
            with self.subTest(code=code):
                path.write_text(original.replace(old, new))
                self.assertIn(code, self.codes())
        path.write_text(original)

    def test_version_04_requires_constraint_freedom_independent_oracle_and_status_lineage(self):
        self.view["template_version"] = "0.4.0"
        self.write_fixed_body("ISD")
        path = self.root / "ISD.md"
        original = path.read_text()
        cases = [
            ("不可改变的规则 / Constraint ID**：CON-M201-001",
             "不可改变的规则 / Constraint ID**：TODO", "isd.function-contract"),
            ("独立 Oracle / Expected**：expected", "独立 Oracle / Expected**：TODO",
             "isd.verification"),
            ("本层派生状态 / 事实依据**：PLANNED / no source yet",
             "本层派生状态 / 事实依据**：TODO", "isd.status-lineage"),
        ]
        for old, new, code in cases:
            with self.subTest(code=code):
                path.write_text(original.replace(old, new))
                self.assertIn(code, self.codes())
        path.write_text(original)

    def test_version_05_requires_io_contract_diagram_and_configuration(self):
        self.view["template_version"] = "0.5.0"
        self.write_fixed_body("ISD")
        path = self.root / "ISD.md"
        original = path.read_text()
        cases = [
            ("输入参数 / 数据结构 authority**：path / PathSpec IF-1",
             "输入参数 / 数据结构 authority**：TODO", "isd.function-contract"),
            ("```mermaid\nflowchart TD", "```text\nflowchart TD", "isd.process-diagram"),
            ("配置 key / 来源 / 优先级**：db.path / file then CLI",
             "配置 key / 来源 / 优先级**：TODO", "isd.configuration"),
        ]
        for old, new, code in cases:
            with self.subTest(code=code):
                path.write_text(original.replace(old, new))
                self.assertIn(code, self.codes())
        path.write_text(original)

    def test_pre_03_isd_keeps_legacy_delivery_compatibility(self):
        self.view["template_version"] = "0.2.1"
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
