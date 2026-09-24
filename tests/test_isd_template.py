"""ISD routing/generation regressions; not a verdict on project design quality."""

import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
import jsonschema
from pathlib import Path
from test_validate_design import load_validator

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/design/implementation-design.md"


class ISDTemplateTests(unittest.TestCase):
    def generate(self, directory, *options):
        return subprocess.run([
            sys.executable, str(ROOT / "scripts/new-design"),
            "--project", "example", "--template", "design.implementation",
            "--name", "FRAME_ISD", "--project-root", directory,
            "--repository", "example/repo", "--owner", "Owner",
            "--author", "Author", "--parent-document-id", "PARSER_DESIGN",
            *options,
        ], capture_output=True, text=True)

    def test_generation_defaults_parent_and_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.generate(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = Path(directory) / "docs/50_implementation_design"
            metadata = json.loads((output / "FRAME_ISD.isd.metadata.json").read_text())
            self.assertEqual(metadata["design_level"], "module")
            self.assertEqual(metadata["domain"], ["software"])
            self.assertEqual(metadata["parent_document_id"], "PARSER_DESIGN")
            self.assertEqual(metadata["template_version"], "0.5.0")
            digest = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()
            self.assertEqual(metadata["template_sha256"], digest)
            snapshot = output / ".std-template-references" / digest / "implementation-design.md.txt"
            self.assertEqual(snapshot.read_bytes(), TEMPLATE.read_bytes())
            document = (output / "FRAME_ISD.isd.md").read_text()
            self.assertNotIn("EX-ISD/v1", document)
            self.assertNotIn("{{", document)
            self.assertIn(".std-template-references/", document)
            self.assertEqual(len(re.findall(r"^## \d+\.", document, re.M)), 10)

    def test_invalid_object_scope_rejected_before_writes(self):
        for options in [("--level", "implementation-unit"), ("--level", "system"),
                        ("--domain", "hardware"), ("--domain", "software", "--domain", "fpga")]:
            with self.subTest(options=options), tempfile.TemporaryDirectory() as directory:
                result = self.generate(directory, *options)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("level=module", result.stderr)
                self.assertEqual(list(Path(directory).iterdir()), [])

    def test_existing_document_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.generate(directory).returncode, 0)
            path = Path(directory) / "docs/50_implementation_design/FRAME_ISD.isd.md"
            before = path.read_bytes()
            self.assertNotEqual(self.generate(directory).returncode, 0)
            self.assertEqual(path.read_bytes(), before)

    def test_metadata_validator_enforces_isd_scope(self):
        validator = load_validator()
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.generate(directory).returncode, 0)
            path = Path(directory) / "docs/50_implementation_design/FRAME_ISD.isd.metadata.json"
            original = json.loads(path.read_text())
            for level, domain, rejected in [("module", ["software"], False),
                                             ("system", ["software"], True),
                                             ("module", ["fpga"], True)]:
                data = dict(original, design_level=level, domain=domain)
                path.write_text(json.dumps(data))
                issues, _, _ = validator.validate_metadata(path, {}, catalog, Path(directory), {})
                self.assertEqual(any(item["code"] == "metadata.isd-scope" for item in issues), rejected)

    def test_template_contains_connected_example_and_implementation_details(self):
        text = TEMPLATE.read_text()
        self.assertEqual(text.count("<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->"), 5)
        self.assertEqual(text.count("<!-- STD_TEMPLATE_EXAMPLE_END -->"), 5)
        self.assertEqual(text.count("```mermaid"), 5)
        self.assertIn("frame_decoder.h", text)
        self.assertNotIn("frame_types.h", text)
        self.assertNotIn("version/kind/length或INVALID", text)
        for term in ["decode_one", "consumed=8", "INVALID VERSION", "借用", "Planned",
                     "关键函数", "错误优先级", "输入参数 / 数据结构 authority",
                     "错误输出 / 触发条件 / 优先级", "配置实现", "构建目标",
                     "NOT_RUN", "Case", "selector"]:
            self.assertIn(term, text)

    def test_standard_defines_combined_and_split_authority(self):
        text = (ROOT / "docs/isd-standard.md").read_text()
        for term in ["默认一个模块一份", "兼作ISD", "parent_document_id", "不自动搬迁或删除",
                     "每项规则只能有一个", "不填写伪造行号", "version/revision/hash"]:
            self.assertIn(term, text)

    def test_isd_parent_is_direct_software_design_not_another_module_view(self):
        validator = load_validator()
        def record(identity, template, level, parent=None, domain=None):
            return (Path(identity + ".metadata.json"), dict(
                document_id=identity, template_id=template, design_level=level,
                parent_document_id=parent, project="example", domain=domain or ["software"]))
        system = record("SYS", "design.software-system", "system")
        subsystem = record("SUB", "design.subsystem", "subsystem", "SYS")
        module = record("MOD", "design.definition", "module", "SUB")
        other_isd = record("OTHER", "design.implementation", "module", "SYS")
        hardware = record("HW", "design.system", "system", domain=["hardware"])
        legacy = record("LEGACY", "design.system", "system")
        for parent, code in [("SYS", None), ("SUB", None), ("LEGACY", None),
                             ("MOD", "hierarchy.isd-parent"),
                             ("OTHER", "hierarchy.isd-parent"),
                             ("HW", "hierarchy.isd-parent"),
                             (None, "hierarchy.isd-parent"),
                             ("MISSING", "hierarchy.parent-missing")]:
            with self.subTest(parent=parent):
                issues, links = validator.validate_design_hierarchy([
                    system, subsystem, module, other_isd, hardware, legacy,
                    record("ISD", "design.implementation", "module", parent)])
                if code:
                    self.assertIn(code, [item["code"] for item in issues])
                    self.assertNotIn("ISD", links)
                else:
                    self.assertEqual(issues, [])
                    self.assertEqual(links["ISD"], parent)

    def test_algorithm_and_budget_requirements(self):
        text = TEMPLATE.read_text()
        for term in ["每个重要算法必须", "整数提升", "单调", "冷", "共享", "LLM", "总期限"]:
            self.assertIn(term, text)
        guide = (ROOT / "docs/ai-guides/implementation-design.md").read_text()
        self.assertNotIn("排队/接管机制", guide)
        self.assertIn("isd-frame-decoder/README.md", guide)

    def test_handoff_and_security_requirements_are_connected(self):
        standard = (ROOT / "docs/isd-standard.md").read_text()
        template = TEMPLATE.read_text()
        guide = (ROOT / "docs/ai-guides/implementation-design.md").read_text()
        for text in [standard, template, guide]:
            for term in ["承接矩阵", "自由度", "宿主", "字段", "权限", "V/Case"]:
                self.assertIn(term, text)
        for term in ["上游信息项", "固定来源", "权威位置", "验证位置", "这些不能推迟"]:
            self.assertIn(term, standard)
        self.assertIn("ISD 细化内容 / 章节", template)
        self.assertIn("单位/窗口/重置", template)
        self.assertIn("location/symbol为null", guide)
        self.assertEqual(len(re.findall(r"^## \d+\.", template, re.M)), 10)

    def test_planned_example_is_exact_existing_downstream_not_second_catalog(self):
        text = (ROOT / "docs/examples/isd-planned-mapping.md").read_text()
        blocks = re.findall(r"```json\n([\s\S]*?)\n```", text)
        self.assertEqual(len(blocks), 1)
        row = json.loads(blocks[0])
        catalog = json.loads((ROOT / "docs/examples/interfaces/catalog.json").read_text())
        member = next(m for m in catalog["members"] if m["id"] == "IF-EXPORT#OP01")
        matches = [r for r in member["downstream"] if
                   (r["role"], r["module"], r["backend"]) ==
                   (row["role"], row["module"], row["backend"])]
        self.assertEqual(matches, [row])
        schema = json.loads((ROOT / "schemas/interface-catalog.schema.json").read_text())
        jsonschema.Draft202012Validator({"$defs": schema["$defs"],
                                        "$ref": "#/$defs/downstream"}).validate(row)
        self.assertEqual(row["implementation"], "not_implemented")
        self.assertIsNone(row["location"])
        self.assertIsNone(row["symbol"])
        self.assertEqual(row["verification"], "not_run")
        self.assertEqual(row["runs"], [])
        self.assertEqual(row["source_sha256"], hashlib.sha256(
            (ROOT / member["source"]["path"]).read_bytes()).hexdigest())
        for term in ["Planned", "原行", "partial或implemented", "真实Run", "不能只凭这一行"]:
            self.assertIn(term, text)

    def test_persistence_and_controlled_fault_injection_requirements(self):
        texts = [TEMPLATE.read_text(), (ROOT / "docs/isd-standard.md").read_text(),
                 (ROOT / "docs/ai-guides/implementation-design.md").read_text()]
        for text in texts:
            for term in ["事务边界", "持久提交点", "恢复入口", "源/目标",
                         "转换函数", "失败出口", "可控时钟", "调度",
                         "前置事实", "直接修改业务终态", "fixture"]:
                self.assertIn(term, text)
        guide = texts[2]
        self.assertNotIn("而不篡改内部状态？", guide)
        self.assertIn("提交前失败", guide)
        self.assertIn("持久提交后响应丢失", guide)
        self.assertIn("FrameDecoder无持久状态", guide)

    def test_stateful_software_and_readable_record_requirements(self):
        template = TEMPLATE.read_text()
        standard = (ROOT / "docs/isd-standard.md").read_text()
        guide = (ROOT / "docs/ai-guides/implementation-design.md").read_text()
        for text in (template, standard, guide):
            lowered = text.lower()
            for term in ["schema 演进", "不接受的迁移模式", "版本不匹配", "部分初始化",
                         "thread-safe", "reentrant", "nested-call", "错误传播",
                         "symlink", "磁盘耗尽", "greenfield", "brownfield"]:
                self.assertIn(term.lower(), lowered)
        for term in ["记录型 → 固定字段段落；矩阵型 → 表格", "Actual / Evidence",
                     "Metadata 与 coverage", "docs/50_implementation_design/<name>.isd.md",
                     "不可改变的规则 / Constraint ID", "实现自由度",
                     "独立 Oracle / Expected", "上游承接状态 / 固定来源",
                     "本层派生状态 / 事实依据", "风险等级 / 判定依据",
                     "PLANNED / IN_PROGRESS / IMPLEMENTED"]:
            self.assertIn(term, template)
        for header in ["| Rule/成员 |", "| 问题ID/既有台账引用 |",
                       "| 模块/原成员ID |", "| 函数/文件 |"]:
            self.assertNotIn(header, template)
        self.assertIn("| 库状态 | 判定事实 | 启动结果 | 是否允许重跑及条件 |", template)

    def test_generated_open_issues_keep_owner_gate_and_analysis_columns(self):
        columns = ["既有台账引用 / 具体缺口 / 反例", "Owner", "最晚关闭阶段 / 截止 Gate",
                   "分析 / 决策引用", "所需输入 / 下一步选择判据", "解决动作 / 完成条件"]
        with tempfile.TemporaryDirectory() as directory:
            result = self.generate(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (Path(directory) / "docs/50_implementation_design/FRAME_ISD.isd.md").read_text()
            visible = re.sub(r"<details>[\s\S]*?</details>", "", text)
            for term in columns:
                self.assertIn(term, visible)
            self.assertNotIn("直接修改业务终态", visible)
            self.assertEqual(len(re.findall(r"^## \d+\.", visible, re.M)), 10)

    def test_frame_handoff_reuses_existing_vectors_and_real_symbols(self):
        text = (ROOT / "docs/examples/isd-frame-decoder/README.md").read_text()
        source = (ROOT / "docs/examples/isd-frame-decoder/frame_decoder.cc").read_text()
        tests = (ROOT / "docs/examples/isd-frame-decoder/frame_decoder_test.cc").read_text()
        for term in ["FD-R1", "FD-R2", "FD-R3", "FD-R4", "FD-V1", "FD-V2", "FD-V3",
                     "上游模块设计片段", "不是第二个格式authority", "NOT_RUN"]:
            self.assertIn(term, text)
        for symbol in ["decode_one", "read_header"]:
            self.assertIn(symbol, text)
            self.assertIn(symbol, source)
        for vector in ["C3/v2", "C3/v4", "C4/v1"]:
            self.assertIn(vector, text)
            self.assertIn(vector, tests)

    def test_frame_decoder_compiles_and_runs_public_entry_vectors(self):
        configured = os.environ.get("CXX")
        if configured:
            compiler = shlex.split(configured)
        else:
            clt = Path("/Library/Developer/CommandLineTools/usr/bin/clang++")
            found = str(clt) if clt.is_file() else shutil.which("c++")
            if not found:
                self.skipTest("No C++ compiler: executable tutorial NOT_RUN")
            compiler = [found]
            sdk = Path("/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk")
            if clt.is_file() and sdk.is_dir():
                compiler += ["-isysroot", str(sdk)]
        source = ROOT / "docs/examples/isd-frame-decoder"
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "frame_decoder_test"
            result = subprocess.run(compiler + [
                "-std=c++20", "-Wall", "-Wextra", "-Werror", "-pedantic", "-pthread",
                str(source / "frame_decoder.cc"), str(source / "frame_decoder_test.cc"),
                "-o", str(binary)], capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS FrameDecoder", result.stdout)


if __name__ == "__main__":
    unittest.main()
