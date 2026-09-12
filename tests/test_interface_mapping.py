"""Catalog/projection regressions and fictional contract checks, not service validation."""

import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REL = Path("docs/examples/interfaces")
loader = importlib.machinery.SourceFileLoader("interface_validator", str(ROOT / "scripts/validate-interface-catalog"))
spec = importlib.util.spec_from_loader(loader.name, loader)
validator = importlib.util.module_from_spec(spec)
loader.exec_module(validator)


class InterfaceMappingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "docs/examples", self.root / "docs/examples")
        self.catalog = validator.read_json(self.root / REL / "catalog.json")
        self.contract_path = self.root / REL / "ex-export-v1.schema.json"
        self.contract = validator.read_json(self.contract_path)

    def errors(self):
        return validator.validate(self.catalog, {"corezilla/STD": self.root})[0]

    def changed_contract(self):
        self.contract_path.write_text(json.dumps(self.contract, ensure_ascii=False, indent=2) + "\n")
        digest = hashlib.sha256(self.contract_path.read_bytes()).hexdigest()

        def refresh(item):
            if isinstance(item, dict):
                if item.get("path") == str(REL / "ex-export-v1.schema.json"):
                    item["sha256"] = digest
                if "source_sha256" in item:
                    item["source_sha256"] = digest
                for child in item.values():
                    refresh(child)
            elif isinstance(item, list):
                for child in item:
                    refresh(child)
        refresh(self.catalog)

    def test_complete_scope_and_bidirectional_lookup(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(len(self.catalog["members"]), 32)
        op = next(m for m in self.catalog["members"] if m["id"] == "IF-EXPORT#OP01")
        request_id = next(b["target"] for b in op["bindings"] if b["role"] == "request")
        request = next(m for m in self.catalog["members"] if m["id"] == request_id)
        request_def = validator.pointer(self.contract, request["source"]["selector"]["value"])
        self.assertEqual(request_def["properties"]["operation_id"], {"$ref": "#/$defs/Id"})
        self.assertEqual(self.contract["$defs"]["Id"]["pattern"], "^[A-Za-z][A-Za-z0-9-]{0,63}$")
        self.assertEqual(op["prose"]["anchor"], "contract-behavior")
        self.assertEqual({d["role"] for d in op["downstream"]}, {"provider", "consumer"})
        error = next(m for m in self.catalog["members"] if m["name"] == "CONFLICT")
        self.assertEqual(error["prose"]["anchor"], "error-actions")
        self.assertEqual(error["id"], "IF-EXPORT#ERR06")

    def test_duplicate_member_is_rejected(self):
        self.catalog["members"].append(copy.deepcopy(self.catalog["members"][0]))
        self.assertTrue(any("id.duplicate" in e for e in self.errors()))

    def test_unknown_fields_and_missing_baseline_are_rejected(self):
        self.catalog["members"][0]["fake_pass"] = True
        del self.catalog["members"][0]["source"]["version"]
        self.assertTrue(all(e.startswith("schema:") for e in self.errors()))

    def test_complete_coverage_cannot_drop_a_member(self):
        self.catalog["members"].pop()
        self.assertTrue(any("coverage:" in e for e in self.errors()))

    def test_invented_complete_scope_is_rejected(self):
        self.catalog["families"][0]["coverage"]["inventory"] = []
        self.assertTrue(any("coverage:" in e for e in self.errors()))

    def test_planned_source_or_stale_pointer_is_not_a_definition(self):
        self.catalog["members"][0]["source"]["selector"]["value"] = "/TODO"
        self.assertTrue(any(e.startswith("source:") for e in self.errors()))

    def test_hash_and_declared_version_are_checked(self):
        self.catalog["members"][0]["source"]["sha256"] = "0" * 64
        self.assertTrue(any("hash mismatch" in e for e in self.errors()))
        self.catalog["members"][0]["source"]["sha256"] = hashlib.sha256(self.contract_path.read_bytes()).hexdigest()
        self.catalog["members"][0]["source"]["version"] = "v2"
        self.assertTrue(any("version mismatch" in e for e in self.errors()))

    def test_stale_anchor_or_prose_version_is_rejected(self):
        self.catalog["members"][0]["prose"]["anchor"] = "removed-anchor"
        self.catalog["members"][1]["prose"]["version"] = "obsolete"
        self.assertGreaterEqual(sum(e.startswith("prose:") for e in self.errors()), 2)

    def test_unresolved_shared_type_is_rejected(self):
        self.contract["$defs"]["Request"]["properties"]["operation_id"]["$ref"] = "#/$defs/Unknown"
        self.changed_contract()
        self.assertTrue(any("unknown type reference" in e for e in self.errors()))

    def test_signature_binding_cannot_point_to_different_type(self):
        op = next(m for m in self.catalog["members"] if m["kind"] == "operation")
        op["bindings"][0]["target"] = "IF-EXPORT#TYPE01"
        self.assertTrue(any(e.startswith("binding:") for e in self.errors()))

    def test_operation_cannot_omit_all_type_bindings(self):
        op = next(m for m in self.catalog["members"] if m["kind"] == "operation")
        op["bindings"] = []
        self.assertTrue(any("requires applicable" in e for e in self.errors()))

    def test_native_source_reports_semantic_check_limit(self):
        p = self.root / "native.proto"
        p.write_text('version: v1\nrevision: 1\nmessage Existing {}\n')
        family = copy.deepcopy(self.catalog["families"][0])
        family["coverage"] = {"level": "selected_members", "scope": "One native declaration", "excluded_scope": "Other declarations", "inventory": []}
        member = copy.deepcopy(self.catalog["members"][0])
        native = copy.deepcopy(member["source"])
        native.update(path="native.proto", selector={"kind": "literal", "value": "message Existing {}"},
                      version="version: v1", revision="revision: 1",
                      version_selector={"kind": "literal", "value": "version: v1"},
                      revision_selector={"kind": "literal", "value": "revision: 1"},
                      sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        member.update(source=native, downstream=[], reading_view=None)
        family["source"] = native
        self.catalog.update(families=[family], members=[member])
        errors, limits = validator.validate(self.catalog, {"corezilla/STD": self.root})
        self.assertEqual(errors, [])
        self.assertTrue(any("native field/signature" in e for e in limits))

    def test_integer_source_revision_is_not_reformatted(self):
        self.contract["x-revision"] = 3
        self.changed_contract()
        def revise(node):
            if isinstance(node, dict):
                if "revision" in node:
                    node["revision"] = 3
                for value in node.values():
                    revise(value)
            elif isinstance(node, list):
                for value in node:
                    revise(value)
        revise(self.catalog)
        self.assertEqual(self.errors(), [])

    def test_full_projection_detects_field_rules_enums_and_signature_drift(self):
        baseline = copy.deepcopy(self.contract)
        mutations = [
            lambda c: c["$defs"]["Id"].update(default="new-default"),
            lambda c: c["$defs"]["Payload"].update(type=["string", "null"]),
            lambda c: c["$defs"]["Payload"].update({"x-max-utf8-bytes": 8192}),
            lambda c: c["$defs"]["Error"]["properties"]["code"]["enum"].append("NEW_ERROR"),
            lambda c: c["x-operations"]["prepare"]["request"].update({"$ref": "#/$defs/Response"}),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.contract = copy.deepcopy(baseline)
                mutate(self.contract)
                self.changed_contract()
                self.assertTrue(any(e.startswith("projection:") for e in self.errors()))

    def test_consumer_baseline_mismatch_is_rejected(self):
        self.catalog["members"][0]["downstream"][1]["revision"] = "2"
        self.assertTrue(any("baseline mismatch" in e for e in self.errors()))

    def test_backend_pass_does_not_close_unimplemented_backend(self):
        m = self.catalog["members"][0]
        m["status"]["verification"] = "pass"
        m["downstream"][0]["verification"] = "pass"
        self.assertTrue(any("aggregate PASS" in e for e in self.errors()))
        self.assertTrue(any("unimplemented backend" in e for e in self.errors()))

    def test_deprecated_id_requires_valid_replacement_and_design_state(self):
        m = self.catalog["members"][0]
        m["evolution"] = {"state": "deprecated", "replaced_by": "IF-EXPORT#MISSING", "compatibility": "Removed"}
        self.assertTrue(any("invalid replacement" in e for e in self.errors()))

    def test_safe_paths_and_explicit_repository_mapping(self):
        for path in ("../outside", "/tmp/secret", "https://example.invalid/file"):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    validator.safe_path(self.root, path)
        (self.root / "link").symlink_to(self.contract_path)
        with self.assertRaises(ValueError):
            validator.safe_path(self.root, "link")
        self.catalog["members"][0]["source"]["repository"] = "unmapped"
        self.assertTrue(any("unmapped repository" in e for e in self.errors()))

    def test_duplicate_json_keys_and_bad_pointer_are_rejected(self):
        p = self.root / "duplicate.json"
        p.write_text('{"id":1,"id":2}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            validator.read_json(p)
        with self.assertRaises(ValueError):
            validator.pointer({}, "/invalid~escape")
        self.assertEqual(validator.pointer({"a/b": {"~x": 3}}, "/a~1b/~0x"), 3)

    def test_all_existing_public_json_examples_match_real_schema(self):
        schema = self.contract
        jsonschema.Draft202012Validator.check_schema(schema)
        check = jsonschema.Draft202012Validator(schema)
        text = (self.root / "docs/examples/mechanism-side-effect-example.md").read_text()
        instances = []
        for block in re.findall(r"```json\n(.*?)\n```", text, re.S):
            for line in block.splitlines():
                value = json.loads(line)
                if "protocol" in value:
                    instances.append(value)
        self.assertGreaterEqual(len(instances), 17)
        for value in instances:
            self.assertEqual(list(check.iter_errors(value)), [], value)
        self.assertEqual(set(schema["x-errors"]), set(schema["$defs"]["Error"]["properties"]["code"]["enum"]))

    def test_invalid_cross_field_envelopes_are_rejected(self):
        request = {"protocol": "EX-EXPORT-01/v1", "request_id": "q1", "agent_instance": "a1", "operation_id": "op1", "op": "execute", "args": {}}
        check = jsonschema.Draft202012Validator(self.contract)
        self.assertEqual(list(check.iter_errors(request)), [])
        for args in ({"payload": "demo", "slot_id": "slot-1"}, {"unknown": 1}, None):
            request["args"] = args
            self.assertTrue(list(check.iter_errors(request)))
        state = {"phase": "RELEASED", "result": "UNKNOWN", "access": "FENCED", "evidence": "PENDING", "disposition": "discard", "resource": "RELEASED", "admission": "ELIGIBLE"}
        self.assertTrue(list(jsonschema.Draft202012Validator(self.contract["$defs"]["State"]).iter_errors(state)))

    def test_generated_templates_keep_mapping_after_help_removed(self):
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        self.assertIn("包含 16 章写作顺序", guide)
        self.assertIn("| 跨单元机制 `design.system-mechanism` | §3.1；§15 验证 |", guide)
        for tid, heading in (("design.system", "3.4 系统机制清单与文档映射"), ("design.system-mechanism", "4. 数据结构设计")):
            dest = self.root / tid
            result = subprocess.run([sys.executable, str(ROOT / "scripts/new-design"), "--template", tid,
                                     "--project", "example", "--name", "design", "--output", str(dest),
                                     "--owner", "Example", "--author", "Example", "--repository", "fiction/example"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (dest / "design.md").read_text()
            body = re.sub(r"<details>.*?</details>", "", text, flags=re.S)
            self.assertIn(heading, body)
            self.assertIn("成员 ID", body)
            if tid == "design.system":
                self.assertIn("Document ID / 预定仓库相对文件名或实际链接", body)
                self.assertNotIn("EX-EXPORT-DESIGN", body)
            else:
                self.assertIn("## 5. 接口设计", body)
                self.assertIn("必填/默认/null", body)
                self.assertIn("request/response/event 类型 ID", body)

    def test_cli_is_read_only_and_reports_runtime_not_run(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate-interface-catalog"),
                                 "--project-root", str(self.root), "--catalog", str(self.root / REL / "catalog.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["runtime_validation"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
