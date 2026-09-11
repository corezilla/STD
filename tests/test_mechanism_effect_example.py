"""EX-EXPORT-01 teaching model: no socket, file, worker or real access enforcement.

Checks the documented example's logical guards and JSON fixtures. Model PASS is
not EX-ENV-P evidence, a proof of concurrency safety, or closure of EX-V6.
"""

import base64
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "docs/examples/mechanism-side-effect-example.md"
PROTOCOL = "EX-EXPORT-01/v1"


def request(op, args=None, oid="op-001", rid="test"):
    return dict(protocol=PROTOCOL, request_id=rid, agent_instance="agent-a1",
                operation_id=oid, op=op, args={} if args is None else args)


def check_response(req, response):
    """Consumer-side correlation and relevant cross-field checks, not JSON Schema."""
    association = {"protocol", "request_id", "agent_instance", "operation_id"}
    assert all(response[k] == req[k] for k in association)
    assert type(response["ok"]) is bool
    if not response["ok"]:
        assert set(response) == association | {"ok", "error"}
        assert set(response["error"]) == {"code"}
        return
    assert set(response) == association | {"ok", "state", "output"}
    s = response["state"]
    assert set(s) == {"phase", "result", "access", "evidence", "disposition", "resource", "admission"}
    assert s["phase"] in ("PREPARED", "EXECUTING", "STOPPING", "STOPPED", "FINALIZED", "RELEASED")
    assert s["result"] in ("NOT_STARTED", "UNKNOWN", "SUCCEEDED", "FAILED")
    assert s["access"] in ("OPEN", "CLOSING", "FENCED")
    assert s["evidence"] in ("PENDING", "CAPTURED", "UNRECOVERABLE")
    assert s["disposition"] in (None, "deliver", "discard")
    released = s["phase"] == "RELEASED"
    assert s["resource"] == ("RELEASED" if released else "HELD")
    assert s["admission"] == ("ELIGIBLE" if released else "BLOCKED")
    if s["phase"] in ("STOPPED", "FINALIZED", "RELEASED"):
        assert s["access"] == "FENCED"
    if s["phase"] in ("FINALIZED", "RELEASED"):
        assert s["evidence"] != "PENDING" and s["disposition"] is not None
    else:
        assert s["disposition"] is None
    if s["phase"] == "PREPARED":
        assert (s["result"], s["access"], s["evidence"]) == ("NOT_STARTED", "OPEN", "PENDING")
    out = response["output"]
    delivering = req["op"] == "finalize" and req["args"].get("disposition") == "deliver"
    assert (out is not None) == delivering
    if out is not None:
        assert set(out) == {"encoding", "data", "sha256"} and out["encoding"] == "base64"
        assert (s["result"], s["evidence"], s["disposition"]) == ("SUCCEEDED", "CAPTURED", "deliver")
        data = base64.b64decode(out["data"], validate=True)
        assert len(data) <= 4096 and hashlib.sha256(data).hexdigest() == out["sha256"]


class ExportModel:
    """Deterministic single-thread model; simulated events explicitly injected."""

    def __init__(self):
        self.records = {}
        self.slot_owner = None
        self.starts = 0
        self.cleanup_fails = False

    def begin_write(self, oid):
        r = self.records[oid]
        if r["state"]["phase"] != "EXECUTING" or r["state"]["access"] != "OPEN":
            return False
        r["inflight"] += 1
        return True

    def end_write(self, oid):
        r = self.records[oid]
        assert r["inflight"] > 0
        r["inflight"] -= 1

    def worker_finished(self, oid, data=b"demo", succeeded=True, lose_completion=False):
        """Worker event; optional transport loss before A accepts the receipt."""
        r = self.records[oid]
        if r["state"]["phase"] not in ("EXECUTING", "STOPPING"):
            return False  # Fenced results cannot upgrade frozen knowledge.
        assert len(data) <= 4096
        if succeeded:
            assert data == r["input"]["payload"].encode("utf-8")
        if lose_completion:
            return True  # Input fault, not an injected evidence-state conclusion.
        r["state"]["result"] = "SUCCEEDED" if succeeded else "FAILED"
        r["receipt"] = dict(protocol=PROTOCOL, request_id=r["execute_request_id"],
            agent_instance="agent-a1", operation_id=oid, slot_id=r["input"]["slot_id"],
            payload_sha256=hashlib.sha256(r["input"]["payload"].encode()).hexdigest(),
            result=r["state"]["result"],
            output=(dict(encoding="base64", data=base64.b64encode(data).decode(),
                         sha256=hashlib.sha256(data).hexdigest()) if succeeded else None))
        return True

    def lose_completion_receipt(self, oid):
        """Fault injection: erase raw receipt before the authoritative source seals."""
        r = self.records[oid]
        assert r["seal"] is None
        r["receipt"] = None

    def corrupt_completion_receipt(self, oid, field, value):
        """Fault injection: change a raw receipt field, never evidence/result state."""
        r = self.records[oid]
        assert r["seal"] is None and r["receipt"] is not None
        r["receipt"][field] = value

    def set_evidence_source_available(self, oid, available):
        """Model the completion/failure of a bounded source read, not wall time."""
        self.records[oid]["source_available"] = available

    def evidence_audit(self, oid):
        """Read-only test observation of A's decision provenance; not a new RPC."""
        return copy.deepcopy(self.records[oid]["evidence_audit"])

    def _valid_receipt(self, oid, r, seal):
        receipt = seal["receipt"]
        expected = dict(protocol=PROTOCOL, request_id=r["execute_request_id"],
            agent_instance="agent-a1", operation_id=oid, slot_id=r["input"]["slot_id"],
            payload_sha256=hashlib.sha256(r["input"]["payload"].encode()).hexdigest(),
            result=seal["result"])
        if (not isinstance(receipt, dict) or set(receipt) != set(expected) | {"output"}
                or any(receipt[k] != value for k, value in expected.items())):
            return False
        if receipt["result"] == "FAILED":
            return receipt["output"] is None
        if receipt["result"] != "SUCCEEDED":
            return False
        data = r["input"]["payload"].encode()
        return receipt["output"] == dict(encoding="base64", data=base64.b64encode(data).decode(),
                                         sha256=hashlib.sha256(data).hexdigest())

    def _collect(self, oid, r):
        """EX-R5: derive the conclusion from a sealed, successfully read source."""
        s, seal = r["state"], r["seal"]
        if s["evidence"] != "PENDING":
            return
        if (not r["source_available"] or seal is None or not seal["closed"]
                or seal["agent_instance"] != "agent-a1" or seal["operation_id"] != oid):
            r["evidence_audit"] = {"reason": "SOURCE_UNVERIFIABLE"}
            return  # Not readable is not confirmed absent. Never release on timeout.
        if not seal["executed"] and seal["result"] == "NOT_STARTED":
            evidence, reason = "CAPTURED", "NOT_STARTED_AT_SEAL"
        elif seal["receipt"] is None:
            evidence, reason = "UNRECOVERABLE", "NO_COMPLETION_AT_SEAL"
        elif self._valid_receipt(oid, r, seal):
            evidence, reason = "CAPTURED", "VALID_COMPLETION_AT_SEAL"
            r["output"] = copy.deepcopy(seal["receipt"]["output"])
        else:
            evidence, reason = "UNRECOVERABLE", "INVALID_COMPLETION_AT_SEAL"
        r["evidence_audit"] = dict(reason=reason, source_closed=seal["closed"],
            executed=seal["executed"], receipt_present=seal["receipt"] is not None,
            receipt_valid=(self._valid_receipt(oid, r, seal) if seal["receipt"] is not None else None),
            result_at_seal=seal["result"])
        s["evidence"] = evidence

    def call(self, req, peer_uid=1000):
        association = dict(protocol=PROTOCOL, **{k: req.get(k) for k in
                           ("request_id", "agent_instance", "operation_id")})

        def error(code):
            return dict(association, ok=False, error={"code": code})

        if peer_uid != 1000:
            return error("FORBIDDEN")
        op, args, oid = req.get("op"), req.get("args"), req.get("operation_id")
        shapes = {"prepare": {"slot_id", "payload"}, "execute": set(), "inspect": set(),
                  "stop": set(), "collect": set(), "finalize": {"disposition"}, "release": set()}
        identifiers = ("request_id", "agent_instance", "operation_id")
        if (set(req) != {"protocol", *identifiers, "op", "args"} or req["protocol"] != PROTOCOL
                or any(not isinstance(req[k], str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,63}", req[k])
                       for k in identifiers)
                or not isinstance(op, str) or op not in shapes
                or not isinstance(args, dict) or set(args) != shapes[op]):
            return error("BAD_REQUEST")
        if op == "prepare" and (args["slot_id"] != "slot-1" or not isinstance(args["payload"], str)
                                or len(args["payload"].encode()) > 4096):
            return error("BAD_REQUEST")
        if op == "finalize" and args["disposition"] not in ("deliver", "discard"):
            return error("BAD_REQUEST")
        if req["agent_instance"] != "agent-a1":
            return error("INSTANCE_MISMATCH")
        if op == "prepare":
            if oid in self.records:
                if self.records[oid]["input"] != args:
                    return error("CONFLICT")
            else:
                if self.slot_owner is not None:
                    return error("BUSY")
                if len(self.records) >= 16:
                    return error("LEDGER_FULL")
                self.slot_owner = oid
                self.records[oid] = dict(input=copy.deepcopy(args), inflight=0, receipt=None, output=None,
                    execute_request_id=None, seal=None, source_available=True, evidence_audit=None,
                    state=dict(phase="PREPARED", result="NOT_STARTED", access="OPEN", evidence="PENDING",
                               disposition=None, resource="HELD", admission="BLOCKED"))
        if oid not in self.records:
            return error("NOT_FOUND")
        r = self.records[oid]
        s = r["state"]
        output = None
        if op == "execute":
            if s["phase"] == "PREPARED":
                s.update(phase="EXECUTING", result="UNKNOWN")
                r["execute_request_id"] = req["request_id"]
                self.starts += 1
            elif s["phase"] != "EXECUTING":
                return error("CLOSED")
        elif op == "stop" and s["access"] != "FENCED":
            s.update(phase="STOPPING", access="CLOSING")
            if r["inflight"] == 0:
                # Models one atomic critical section with completion acceptance.
                r["seal"] = dict(closed=True, agent_instance="agent-a1", operation_id=oid,
                    executed=r["execute_request_id"] is not None, result=s["result"],
                    receipt=copy.deepcopy(r["receipt"]))
                s.update(phase="STOPPED", access="FENCED")
        elif op == "collect":
            if s["access"] != "FENCED":
                return error("NOT_SAFE")
            self._collect(oid, r)
        elif op == "finalize":
            selected = args["disposition"]
            if s["access"] != "FENCED":
                return error("NOT_SAFE")
            if s["evidence"] == "PENDING":
                return error("EVIDENCE_PENDING")
            if s["disposition"] not in (None, selected):
                return error("CONFLICT")
            if selected == "deliver":
                if s["result"] != "SUCCEEDED" or s["evidence"] != "CAPTURED" or r["output"] is None:
                    return error("RESULT_UNAVAILABLE")
                output = r["output"]
            if s["disposition"] is None:
                s.update(phase="FINALIZED", disposition=selected)
        elif op == "release":
            if s["phase"] not in ("FINALIZED", "RELEASED"):
                return error("NOT_FINALIZED")
            if s["phase"] == "FINALIZED" and not self.cleanup_fails:
                assert self.slot_owner == oid
                self.slot_owner = None
                s.update(phase="RELEASED", resource="RELEASED", admission="ELIGIBLE")
        return copy.deepcopy(dict(association, ok=True, state=s, output=output))


class MechanismEffectExampleTests(unittest.TestCase):
    def setUp(self):
        self.model = ExportModel()

    def call(self, op, args=None, oid="op-001", **kwargs):
        req = request(op, args, oid)
        response = self.model.call(req, **kwargs)
        check_response(req, response)
        return response

    def prepare(self, oid="op-001"):
        return self.call("prepare", {"slot_id": "slot-1", "payload": "demo"}, oid)

    def close_discard(self):
        for op, args in (("stop", None), ("collect", None), ("finalize", {"disposition": "discard"}), ("release", None)):
            self.assertTrue(self.call(op, args)["ok"])

    def test_normal_full_json_examples_are_replayed(self):
        text = EXAMPLE.read_text()
        section = text.split("### 4.3 ", 1)[1].split("## 5.", 1)[0]
        groups = [list(map(json.loads, block.strip().splitlines()))
                  for block in re.findall(r"```json\n(.*?)\n```", section, re.S)]
        requests, responses, conflict = groups
        for req, expected in zip(requests, responses, strict=True):
            if req["op"] == "inspect":
                self.model.worker_finished("op-001")
            actual = self.model.call(req)
            check_response(req, actual)
            self.assertEqual(actual, expected)
            if actual["output"] is not None:
                self.assertEqual(base64.b64decode(actual["output"]["data"]), b"demo")
        self.assertEqual(self.model.call(conflict[0]), conflict[1])
        self.assertEqual(self.model.starts, 1)
        self.assertEqual(self.call("finalize", {"disposition": "deliver"})["output"], responses[5]["output"])

    def test_t1_identity_frozen_parameters_and_consumer_correlation(self):
        self.prepare()
        self.prepare()
        self.assertEqual(len(self.model.records), 1)
        self.assertEqual(self.call("prepare", {"slot_id": "slot-1", "payload": "changed"})["error"]["code"], "CONFLICT")
        self.call("execute")
        self.call("execute")
        self.assertEqual(self.model.starts, 1)
        req = request("inspect")
        bad = dict(req, agent_instance="agent-a2")
        self.assertEqual(self.model.call(bad)["error"]["code"], "INSTANCE_MISMATCH")
        response = self.model.call(req)
        for key in ("request_id", "agent_instance", "operation_id"):
            with self.assertRaises(AssertionError):
                check_response(req, dict(response, **{key: "wrong"}))
        forged = copy.deepcopy(response)
        forged["state"].update(phase="RELEASED", resource="RELEASED", admission="ELIGIBLE")
        with self.assertRaises(AssertionError):
            check_response(req, forged)
        self.assertEqual(self.call("inspect", peer_uid=2000)["error"]["code"], "FORBIDDEN")
        self.assertEqual(self.call("inspect", {"extra": 1})["error"]["code"], "BAD_REQUEST")

    def test_t2_stop_does_not_wait_for_collect_but_must_drain(self):
        self.prepare()
        self.call("execute")
        self.assertTrue(self.model.begin_write("op-001"))
        s = self.call("stop")["state"]
        self.assertEqual((s["phase"], s["access"], s["resource"]), ("STOPPING", "CLOSING", "HELD"))
        self.assertFalse(self.model.begin_write("op-001"))
        self.assertEqual(self.call("collect")["error"]["code"], "NOT_SAFE")
        self.assertEqual(self.call("release")["error"]["code"], "NOT_FINALIZED")
        self.model.end_write("op-001")
        self.assertEqual(self.call("stop")["state"]["access"], "FENCED")
        self.assertFalse(self.model.worker_finished("op-001"))
        self.assertEqual(self.call("inspect")["state"]["result"], "UNKNOWN")

    def test_t3_lost_reply_and_unrecoverable_evidence_can_close_safely(self):
        self.prepare()
        self.model.call(request("execute"))  # Drop reply, not the authority's control record.
        self.model.worker_finished("op-001", lose_completion=True)
        self.assertEqual(self.call("inspect")["state"]["result"], "UNKNOWN")
        self.close_discard()
        req = request("release", rid="lost7")
        expected = json.loads(re.search(r"```json\n(.*?)\n```", EXAMPLE.read_text().split("## 6.", 1)[1], re.S)[1])
        self.assertEqual(self.model.call(req), expected)
        audit = self.model.evidence_audit("op-001")
        self.assertEqual(audit["reason"], "NO_COMPLETION_AT_SEAL")
        self.assertTrue(audit["source_closed"] and audit["executed"])
        self.assertFalse(audit["receipt_present"])
        self.assertEqual(self.call("execute")["error"]["code"], "CLOSED")
        self.assertTrue(self.prepare("op-002")["ok"])
        self.call("release")  # Old tombstone cannot free the new owner's slot.
        self.assertEqual(self.model.slot_owner, "op-002")
        self.assertFalse(self.model.begin_write("op-001"))
        self.assertEqual(self.model.starts, 1)  # No hidden retry of old work.

    def test_t4_cancel_prepared_and_branch_specific_dependencies(self):
        self.prepare()
        self.close_discard()
        self.assertEqual(self.model.starts, 0)
        self.assertEqual(self.call("finalize", {"disposition": "deliver"})["error"]["code"], "CONFLICT")
        self.assertEqual(self.call("stop")["state"]["phase"], "RELEASED")

    def test_t4_cancel_executing_reaches_release_using_calls_only(self):
        """No receipt injection or internal-state assignment may unlock cancellation."""
        self.prepare()
        self.call("execute")
        self.assertEqual(self.call("stop")["state"]["access"], "FENCED")
        state = self.call("collect")["state"]
        self.assertEqual((state["result"], state["evidence"]), ("UNKNOWN", "UNRECOVERABLE"))
        self.assertTrue(self.call("finalize", {"disposition": "discard"})["ok"])
        self.assertEqual(self.call("release")["state"]["resource"], "RELEASED")
        self.assertTrue(self.prepare("op-002")["ok"])
        self.assertEqual(self.model.starts, 1)

    def test_t4_pending_evidence_and_failed_result_do_not_allow_delivery(self):
        self.prepare()
        self.call("execute")
        self.call("stop")
        self.model.set_evidence_source_available("op-001", False)
        self.assertEqual(self.call("collect")["state"]["evidence"], "PENDING")
        self.assertEqual(self.model.evidence_audit("op-001")["reason"], "SOURCE_UNVERIFIABLE")
        self.assertEqual(self.call("finalize", {"disposition": "discard"})["error"]["code"], "EVIDENCE_PENDING")
        self.assertEqual(self.call("release")["error"]["code"], "NOT_FINALIZED")
        self.model.set_evidence_source_available("op-001", True)
        self.call("collect")
        self.assertEqual(self.call("finalize", {"disposition": "deliver"})["error"]["code"], "RESULT_UNAVAILABLE")
        self.call("finalize", {"disposition": "discard"})
        failed = ExportModel()
        failed.call(request("prepare", {"slot_id": "slot-1", "payload": "demo"}))
        failed.call(request("execute"))
        failed.worker_finished("op-001", succeeded=False)
        failed.call(request("stop"))
        failed.call(request("collect"))
        self.assertEqual(failed.call(request("finalize", {"disposition": "deliver"}))["error"]["code"], "RESULT_UNAVAILABLE")

    def test_t5_cleanup_failure_holds_capacity_and_idempotent_release(self):
        self.prepare()
        self.model.cleanup_fails = True
        self.close_discard()
        self.assertEqual(self.call("inspect")["state"]["phase"], "FINALIZED")
        self.assertEqual(self.prepare("op-002")["error"]["code"], "BUSY")
        self.model.cleanup_fails = False
        self.call("release")
        self.prepare("op-002")
        self.call("release")
        self.assertEqual(self.model.slot_owner, "op-002")
        self.assertEqual(self.prepare("op-003")["error"]["code"], "BUSY")

    def test_known_result_is_not_changed_by_receipt_loss(self):
        self.prepare()
        self.call("execute")
        self.model.worker_finished("op-001")
        self.model.lose_completion_receipt("op-001")
        self.call("stop")
        state = self.call("collect")["state"]
        self.assertEqual((state["result"], state["evidence"]), ("SUCCEEDED", "UNRECOVERABLE"))
        self.assertEqual(self.call("finalize", {"disposition": "deliver"})["error"]["code"], "RESULT_UNAVAILABLE")
        self.close_discard()

    def test_t3_invalid_receipt_is_judged_from_frozen_fields(self):
        for field, bad in (("operation_id", "op-wrong"), ("request_id", "wrong-request"),
                           ("agent_instance", "agent-old"), ("payload_sha256", "0" * 64),
                           ("output", {"encoding": "base64", "data": "ZGVtbw==", "sha256": "0" * 64})):
            with self.subTest(field=field):
                self.model = ExportModel()
                self.prepare()
                self.call("execute")
                self.model.worker_finished("op-001")
                self.model.corrupt_completion_receipt("op-001", field, bad)
                self.call("stop")
                self.assertEqual(self.call("collect")["state"]["evidence"], "UNRECOVERABLE")
                self.assertEqual(self.model.evidence_audit("op-001")["reason"], "INVALID_COMPLETION_AT_SEAL")
                self.assertEqual(self.call("finalize", {"disposition": "deliver"})["error"]["code"], "RESULT_UNAVAILABLE")
                self.close_discard()

    def test_t3_late_completion_never_reopens_sealed_source(self):
        self.prepare()
        self.call("execute")
        self.call("stop")
        self.assertFalse(self.model.worker_finished("op-001"))
        first = self.call("collect")["state"]
        self.assertEqual(first["evidence"], "UNRECOVERABLE")
        audit = self.model.evidence_audit("op-001")
        self.assertFalse(self.model.worker_finished("op-001"))
        self.call("stop")
        self.assertEqual(self.call("collect")["state"], first)
        self.assertEqual(self.model.evidence_audit("op-001"), audit)
        self.close_discard()

    def test_t4_cancel_inflight_generates_seal_only_after_write_drains(self):
        self.prepare()
        self.call("execute")
        self.model.begin_write("op-001")
        self.call("stop")
        self.assertEqual(self.call("collect")["error"]["code"], "NOT_SAFE")
        self.model.end_write("op-001")  # Actual completion event, not evidence-state injection.
        self.close_discard()
        self.assertEqual(self.call("inspect")["state"]["resource"], "RELEASED")

    def test_t3_completion_accepted_before_seal_is_captured(self):
        self.prepare()
        self.call("execute")
        self.model.begin_write("op-001")
        self.call("stop")
        self.model.end_write("op-001")
        self.assertTrue(self.model.worker_finished("op-001"))
        self.call("stop")
        state = self.call("collect")["state"]
        self.assertEqual((state["result"], state["evidence"]), ("SUCCEEDED", "CAPTURED"))
        self.assertEqual(self.model.evidence_audit("op-001")["reason"], "VALID_COMPLETION_AT_SEAL")
        self.call("finalize", {"disposition": "deliver"})
        self.assertEqual(self.call("release")["state"]["resource"], "RELEASED")

    def test_record_capacity_does_not_evict_replay_protection(self):
        for n in range(16):
            oid = f"op-{n}"
            self.prepare(oid)
            for op, args in (("stop", None), ("collect", None), ("finalize", {"disposition": "discard"}), ("release", None)):
                self.call(op, args, oid)
        self.assertEqual(self.prepare("op-new")["error"]["code"], "LEDGER_FULL")
        self.assertTrue(self.prepare("op-0")["ok"])
        self.assertEqual(self.call("execute", oid="op-0")["error"]["code"], "CLOSED")

    def test_opening_and_evidence_scope_remain_explicit(self):
        text = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        opening = text.split("## 1.", 1)[1].split("## 2.", 1)[0]
        participants = text.split("## 3.", 1)[1].split("## 4.", 1)[0]
        self.assertIn("usage-overview.png", opening)
        self.assertNotIn("collaboration.png", opening)
        self.assertIn("collaboration.png", participants)
        example = EXAMPLE.read_text()
        self.assertIn("EX-V6", example)
        self.assertIn("未实现；执行 NOT_RUN", example)
        self.assertIn("模型 PASS", example)

    def test_evidence_provenance_and_applicability_are_explicit(self):
        guide = (ROOT / "docs/ai-guides/system-mechanism.md").read_text()
        template = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        self.assertIn("这个事实如何产生", guide)
        for text in (guide, template):
            compact = text.replace("\n", "")
            self.assertIn("同时涉及业务副作用、取证封结和资源收口", compact)
            self.assertIn("调用中断、迟到响应和临时资源释放", compact)
        self.assertNotIn("至少重走正常、取消及证据不可恢复但已安全停止三条路径", template)
        example = EXAMPLE.read_text()
        for reason in ("NOT_STARTED_AT_SEAL", "VALID_COMPLETION_AT_SEAL", "NO_COMPLETION_AT_SEAL",
                       "INVALID_COMPLETION_AT_SEAL"):
            self.assertIn(reason, example)
        self.assertIn("来源不可读取/核查", example)
        # Tests may inject raw faults, but cannot set receipt/evidence conclusions.
        tree = ast.parse(Path(__file__).read_text())
        tests = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == type(self).__name__)
        for node in ast.walk(tests):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant):
                        self.assertNotIn(target.slice.value, ("receipt", "evidence"))


if __name__ == "__main__":
    unittest.main()
