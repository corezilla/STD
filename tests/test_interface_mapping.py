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

    def test_signature_roles_and_completeness_cannot_drift(self):
        op = next(m for m in self.catalog["members"] if m["name"] == "prepare")
        baseline = copy.deepcopy(op["bindings"])
        variants = {}
        swapped = copy.deepcopy(baseline)
        for binding in swapped:
            if binding["role"] in ("request", "response"):
                binding["role"] = {"request": "response", "response": "request"}[binding["role"]]
        variants["swapped roles"] = swapped
        for role in ("request", "response"):
            variants["missing " + role] = [b for b in baseline if b["role"] != role]
        variants["missing args"] = [b for b in baseline if b["selector"]["value"] != "/args"]
        disguised = copy.deepcopy(baseline)
        disguised[0].update(role="alias", mapping="Not a replacement for the actual signature")
        variants["disguised as alias"] = disguised
        variants["duplicate response"] = baseline + [next(b for b in baseline if b["role"] == "response")]
        extra = copy.deepcopy(baseline[0])
        extra["role"] = "event"
        variants["invented event"] = baseline + [extra]
        for label, bindings in variants.items():
            with self.subTest(mutation=label):
                op["bindings"] = bindings
                self.assertTrue(any(e.startswith("signature:") for e in self.errors()))

    def test_one_way_and_nested_signature_slots_use_only_actual_source(self):
        derive = validator.signature_bindings
        self.assertEqual(derive({"request": {"$ref": "#/Request"}}), {("request", "json_pointer", "/request")})
        self.assertEqual(derive({"event": {"$ref": "#/Event"}}), {("event", "json_pointer", "/event")})
        self.assertEqual(derive({"response": {"oneOf": [{"$ref": "#/Ok"}, {"$ref": "#/Error"}]}}),
                         {("response", "json_pointer", "/response/oneOf/0"), ("response", "json_pointer", "/response/oneOf/1")})
        for value in ({"input": {"$ref": "#/Request"}}, {"request": {"type": "object"}}, {}):
            with self.subTest(unsupported=value), self.assertRaises(ValueError):
                derive(value)

    def test_one_way_operation_passes_catalog_without_invented_response(self):
        definition = self.contract["x-operations"]["prepare"]
        definition.pop("response")
        definition["mode"] = "one-way"
        member = next(m for m in self.catalog["members"] if m["name"] == "prepare")
        member["bindings"] = [b for b in member["bindings"] if b["role"] != "response"]
        member["reading_view"] = None  # This temporary source declares no generated reading projection.
        self.changed_contract()
        self.assertEqual(self.errors(), [])

    def test_prose_cover_metadata_and_catalog_are_one_identity(self):
        path = self.root / "docs/examples/mechanism-side-effect-example.md"
        sidecar = path.with_suffix(".metadata.json")
        original_text = path.read_text()
        original_metadata = json.loads(sidecar.read_text())
        version = original_metadata["document_version"]
        self.assertNotIn("<!-- Document Version:", original_text)
        self.assertEqual(self.errors(), [])  # no hidden ID/version needed
        mutations = (
            ("cover version", lambda s: s.replace(f'| Document Version | `{version}` |', '| Document Version | `4.0.0` |'), None),
            ("metadata version", lambda s: s, {"document_version": "4.0.0"}),
            ("cover ID", lambda s: s.replace('`EX-EXPORT-DESIGN`', '`OTHER-DESIGN`'), None),
            ("metadata ID", lambda s: s, {"document_id": "OTHER-DESIGN"}),
            ("metadata path", lambda s: s, {"source_path": "wrong.md"}),
            ("metadata repo", lambda s: s, {"source_repository": "fiction/other"}),
            ("stale hidden mirror", lambda s: s + '\n<!-- Document Version: 4.0.0 -->\n', None),
        )
        for label, edit, data in mutations:
            with self.subTest(mutation=label):
                path.write_text(edit(original_text))
                sidecar.write_text(json.dumps(original_metadata | (data or {})))
                self.assertTrue(any(e.startswith("prose:") for e in self.errors()))
        path.write_text(original_text)
        sidecar.write_text(json.dumps(original_metadata))
        for field, wrong in (("version", "4.0.0"), ("document_id", "OTHER-DESIGN")):
            member = self.catalog["members"][0]
            previous = member["prose"][field]
            member["prose"][field] = wrong
            self.assertTrue(any("catalog document ID/version" in e for e in self.errors()))
            member["prose"][field] = previous

    def test_legacy_comments_cannot_replace_metadata_or_cover(self):
        path = self.root / "docs/examples/mechanism-side-effect-example.md"
        sidecar = path.with_suffix(".metadata.json")
        metadata = json.loads(sidecar.read_text())
        text = path.read_text() + f'\n<!-- Document ID: {metadata["document_id"]} -->\n<!-- Document Version: {metadata["document_version"]} -->\n'
        path.write_text(text)
        self.assertEqual(self.errors(), [])  # matching old mirrors are checked, not required
        path.write_text(text + f'\n<!-- Document Version: {metadata["document_version"]} -->\n')
        self.assertTrue(any("duplicated" in e for e in self.errors()))
        path.write_text(text.replace("STD_DOCUMENT_COVER_BEGIN", "NO_COVER"))
        self.assertTrue(any("cover.markers" in e for e in self.errors()))
        path.write_text(text)
        sidecar.unlink()
        self.assertTrue(any("missing file" in e for e in self.errors()))

    def test_identity_check_accepts_normal_generated_design_without_new_markers(self):
        dest = self.root / "docs/generated"
        result = subprocess.run([sys.executable, str(ROOT / "scripts/new-design"), "--template", "design.system-mechanism",
                                 "--project", "example", "--name", "real-design", "--project-root", str(self.root), "--output", str(dest),
                                 "--owner", "Example", "--author", "Example", "--repository", "corezilla/STD"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        path = dest / "real-design.md"
        path.write_text(path.read_text() + '\n<a id="bound-data"></a>\n')
        data = json.loads(path.with_suffix(".metadata.json").read_text())
        self.catalog["members"][0]["prose"] = {"repository": data["source_repository"], "path": data["source_path"],
                                               "document_id": data["document_id"], "version": data["document_version"], "anchor": "bound-data"}
        self.assertEqual(self.errors(), [])
        # Identity validation must not silently require the latest adopted template.
        current_template = data["template_version"]
        data["template_version"] = "1.5.1"
        path.with_suffix(".metadata.json").write_text(json.dumps(data))
        path.write_text(path.read_text().replace(f'| Template Version | `{current_template}` |', '| Template Version | `1.5.1` |'))
        self.assertEqual(self.errors(), [])

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
                self.assertIn("上级 Mechanism ID", body)
                self.assertIn("前置依赖（类别）", body)
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
