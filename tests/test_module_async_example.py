"""Logical event tests only; no deployed worker, real filesystem or time guarantees."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest
import jsonschema
from test_mechanism_effect_example import ExportModel, request, check_response

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "docs/examples/interfaces/ex-export-v1.schema.json").read_text())


def validate_type(value, name):
    schema = dict(SCHEMA)
    schema.pop("oneOf", None)
    schema["$ref"] = "#/$defs/" + name
    jsonschema.Draft202012Validator(schema).validate(value)


class ModuleAsyncExampleTests(unittest.TestCase):
    def setUp(self):
        self.model = ExportModel()

    def call(self, op, args=None, oid="op-001", rid="req-1"):
        req = request(op, args, oid, rid)
        validate_type(req, "Request")
        response = self.model.call(req)
        validate_type(response, "Response")
        check_response(req, response)
        return response

    def prepare(self, oid="op-001"):
        return self.call("prepare", {"slot_id": "slot-1", "payload": "demo"}, oid)

    def test_published_request_success_and_error_vectors(self):
        text = (ROOT / "docs/examples/module-async-export-example.md").read_text()
        req, success, error = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", text, re.S)]
        validate_type(req, "Request")
        self.assertEqual(self.model.call(req), success)
        conflict = copy.deepcopy(req)
        conflict["request_id"] = "req-2"
        conflict["args"]["payload"] = "other"
        self.assertEqual(self.model.call(conflict), error)
        validate_type(success, "Response")
        validate_type(error, "Response")
        digest = hashlib.sha256((ROOT / "docs/examples/interfaces/ex-export-v1.schema.json").read_bytes()).hexdigest()
        self.assertIn(digest, text)
        catalog = json.loads((ROOT / "docs/examples/interfaces/catalog.json").read_text())
        members = {m["id"]: m for m in catalog["members"]}
        for identity in set(re.findall(r"IF-EXPORT#(?:TYPE|OP|ERR)\d+", text)):
            self.assertIn(identity, members)
            self.assertIn(members[identity]["source"]["selector"]["value"], text)

    def test_normal_complete_consume_release(self):
        self.prepare()
        self.call("execute")
        self.assertTrue(self.model.begin_write("op-001"))
        self.model.end_write("op-001")
        self.assertTrue(self.model.worker_finished("op-001", data=b"demo"))
        self.assertEqual(self.call("inspect")["state"]["resource"], "HELD")
        self.call("stop")
        self.call("collect")
        result = self.call("finalize", {"disposition": "deliver"})
        self.assertEqual(result["output"]["data"], "ZGVtbw==")
        self.assertEqual(result["output"]["sha256"], hashlib.sha256(b"demo").hexdigest())
        self.assertEqual(self.call("release")["state"]["resource"], "RELEASED")

    def test_running_replay_does_not_stop_or_execute_twice(self):
        self.prepare()
        self.call("execute")
        self.prepare()  # same full parameters; lookup precedes capacity rejection
        self.assertEqual(self.call("execute", rid="req-2")["state"]["phase"], "EXECUTING")
        self.assertEqual(self.model.starts, 1)
        self.assertTrue(self.model.begin_write("op-001"))
        self.model.end_write("op-001")

    def test_cancel_inflight_late_completion_and_release(self):
        self.prepare()
        self.call("execute")
        self.model.begin_write("op-001")
        self.assertEqual(self.call("stop")["state"]["phase"], "STOPPING")
        self.assertFalse(self.model.begin_write("op-001"))
        self.assertEqual(self.call("release")["error"]["code"], "NOT_FINALIZED")
        self.model.end_write("op-001")
        self.call("stop")
        self.assertFalse(self.model.worker_finished("op-001"))
        self.assertEqual(self.call("collect")["state"]["evidence"], "UNRECOVERABLE")
        self.call("finalize", {"disposition": "discard"})
        self.assertEqual(self.call("release")["state"]["phase"], "RELEASED")
        self.prepare("op-002")
        self.assertFalse(self.model.worker_finished("op-001"))
        self.call("release")  # old release must not free new owner
        self.assertEqual(self.prepare("op-003")["error"]["code"], "BUSY")

    def test_unverifiable_source_is_not_missing_evidence(self):
        self.prepare()
        self.call("execute")
        self.call("stop")
        self.model.set_evidence_source_available("op-001", False)
        self.assertEqual(self.call("collect")["state"]["evidence"], "PENDING")
        self.assertEqual(self.call("finalize", {"disposition": "discard"})["error"]["code"], "EVIDENCE_PENDING")
        self.assertEqual(self.call("inspect")["state"]["resource"], "HELD")

    def test_completion_before_seal_and_cancel_before_execute(self):
        self.prepare()
        self.call("execute")
        self.model.worker_finished("op-001")
        self.call("stop")
        self.assertEqual(self.call("collect")["state"]["evidence"], "CAPTURED")
        self.call("finalize", {"disposition": "discard"})
        self.call("release")
        self.prepare("op-002")
        self.call("stop", oid="op-002")
        self.assertEqual(self.call("collect", oid="op-002")["state"]["result"], "NOT_STARTED")
        self.call("finalize", {"disposition": "discard"}, oid="op-002")
        self.call("release", oid="op-002")
        self.assertEqual(self.model.starts, 1)

    def test_ledger_full_after_releasing_all_slots(self):
        for i in range(16):
            oid = f"op-{i}"
            self.prepare(oid)
            self.call("stop", oid=oid)
            self.call("collect", oid=oid)
            self.call("finalize", {"disposition": "discard"}, oid=oid)
            self.call("release", oid=oid)
        self.assertEqual(self.prepare("op-next")["error"]["code"], "LEDGER_FULL")
        self.assertEqual(self.prepare("op-0")["state"]["phase"], "RELEASED")
        self.assertEqual(self.model.starts, 0)

    def test_capacity_and_missing_field(self):
        self.prepare()
        self.assertEqual(self.prepare("op-002")["error"]["code"], "BUSY")
        self.assertEqual(self.call("inspect", oid="op-002")["error"]["code"], "NOT_FOUND")
        req = request("prepare", {"slot_id": "slot-1"}, "op-003")
        with self.assertRaises(jsonschema.ValidationError):
            validate_type(req, "Request")
        response = self.model.call(req)
        validate_type(response, "Response")
        self.assertEqual(response["error"]["code"], "BAD_REQUEST")


if __name__ == "__main__":
    unittest.main()
