"""EX-XFER teaching model and native layout checks; no DMA/driver/RTL safety proof."""

import shutil
import struct
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TransferModel:
    """One exclusive session. External events stand for facts, not their hardware proof."""

    def __init__(self):
        self.epoch = 7
        self.records = {}
        self.slot = None
        self.reopen = False

    def submit(self, session, request_id, payload):
        if session != "S1":
            raise ValueError("FORBIDDEN")
        if not 1 <= request_id < 2**64 or not 1 <= len(payload) <= 4096:
            raise ValueError("BAD_INPUT")
        if request_id in self.records:
            record = self.records[request_id]
            if record["payload"] != payload:
                raise ValueError("CONFLICT")
            return record["handle"], record["state"]
        if self.slot is not None:
            raise ValueError("BUSY")
        if len(self.records) >= 256:
            raise ValueError("LEDGER_FULL")
        if self.reopen:
            if self.epoch == 2**32 - 1:
                raise ValueError("EPOCH_EXHAUSTED")
            self.epoch += 1
            self.reopen = False
        handle = (session, self.epoch, request_id)
        self.records[request_id] = dict(handle=handle, payload=bytes(payload), state="ACCEPTED",
                                       output=None, stopped=False, fenced=False)
        self.slot = request_id
        return handle, "ACCEPTED"

    def record(self, handle):
        if handle[0] != "S1":
            raise ValueError("FORBIDDEN")
        record = self.records.get(handle[2])
        if record is None or record["handle"] != handle:
            raise ValueError("BAD_HANDLE")
        return record

    def query(self, handle):
        r = self.record(handle)
        return r["state"], r["output"]

    def completion(self, epoch, request_id, status, bytes_done, reserved, output, visible):
        r = self.records.get(request_id)
        if (r is None or r["handle"][1] != epoch or r["state"] != "ACCEPTED"
                or not visible or reserved != 0 or status not in (0, 1)):
            return False
        if status == 0 and (bytes_done != len(r["payload"]) or len(output) != bytes_done):
            return False
        if status == 1 and bytes_done != 0:
            return False
        r["state"] = "COMPLETED" if status == 0 else "FAILED"
        r["output"] = bytes(output) if status == 0 else None
        return True

    def cancel(self, handle):
        r = self.record(handle)
        if r["state"] == "ACCEPTED":
            r["state"] = "STOPPING"
        return r["state"]

    def stop_fact(self, handle, epoch, kind, confirmed):
        r = self.record(handle)
        if kind not in ("device_stopped", "platform_drained"):
            raise ValueError("unknown fact")
        if r["state"] != "STOPPING" or epoch != handle[1] or not confirmed:
            return False
        r["stopped" if kind == "device_stopped" else "fenced"] = True
        if r["stopped"] and r["fenced"]:
            r["state"] = "SAFE_STOPPED"
        return True

    def release(self, handle):
        r = self.record(handle)
        if r["state"] == "RELEASED":
            return "RELEASED"
        if r["state"] not in ("COMPLETED", "FAILED", "SAFE_STOPPED"):
            raise ValueError("NOT_SAFE")
        self.reopen = r["state"] == "SAFE_STOPPED"
        r["state"], r["output"], self.slot = "RELEASED", None, None
        return "RELEASED"


class HostFPGAExampleTests(unittest.TestCase):
    def setUp(self):
        self.model = TransferModel()
        self.handle, _ = self.model.submit("S1", 101, bytes.fromhex("00 01 ff"))

    def test_x_t1_normal_completion_and_independent_oracle(self):
        self.assertEqual(self.model.query(self.handle), ("ACCEPTED", None))
        self.assertTrue(self.model.completion(7, 101, 0, 3, 0, bytes.fromhex("5a 5b a5"), True))
        self.assertEqual(self.model.query(self.handle), ("COMPLETED", bytes.fromhex("5a 5b a5")))
        self.assertEqual(self.model.release(self.handle), "RELEASED")
        self.assertEqual(self.model.query(self.handle), ("RELEASED", None))

    def test_x_t2_admission_identity_and_capacity(self):
        for request_id, payload, error in [(102, b"", "BAD_INPUT"), (102, b"x"*4097, "BAD_INPUT"),
                                           (0, b"x", "BAD_INPUT"), (101, b"changed", "CONFLICT"), (102, b"x", "BUSY")]:
            with self.assertRaisesRegex(ValueError, error):
                self.model.submit("S1", request_id, payload)
        self.assertEqual(self.model.submit("S1", 101, bytes.fromhex("00 01 ff")), (self.handle, "ACCEPTED"))
        with self.assertRaisesRegex(ValueError, "FORBIDDEN"):
            self.model.query(("S2", 7, 101))
        with self.assertRaisesRegex(ValueError, "BAD_HANDLE"):
            self.model.query(("S1", 6, 101))

    def test_x_t2_invalid_or_not_visible_completion_does_not_release(self):
        for event in [(6,101,0,3,0,b"abc",True), (7,102,0,3,0,b"abc",True),
                      (7,101,0,2,0,b"ab",True), (7,101,2,3,0,b"abc",True),
                      (7,101,0,3,1,b"abc",True), (7,101,0,3,0,b"abc",False)]:
            self.assertFalse(self.model.completion(*event))
            with self.assertRaisesRegex(ValueError, "NOT_SAFE"):
                self.model.release(self.handle)
        self.assertEqual(self.model.query(self.handle), ("ACCEPTED", None))

    def test_x_t3_cancel_missing_or_stale_fact_stays_blocked(self):
        self.assertEqual(self.model.cancel(self.handle), "STOPPING")
        self.model.stop_fact(self.handle, 7, "device_stopped", True)
        self.model.stop_fact(self.handle, 6, "platform_drained", True)
        self.model.stop_fact(self.handle, 7, "platform_drained", False)
        self.assertEqual(self.model.query(self.handle), ("STOPPING", None))
        with self.assertRaisesRegex(ValueError, "NOT_SAFE"):
            self.model.release(self.handle)
        self.model.stop_fact(self.handle, 7, "platform_drained", True)
        self.assertEqual(self.model.query(self.handle), ("SAFE_STOPPED", None))
        self.assertEqual(self.model.release(self.handle), "RELEASED")

    def test_x_t3_facts_can_arrive_in_reverse_order(self):
        self.model.cancel(self.handle)
        self.model.stop_fact(self.handle, 7, "platform_drained", True)
        self.assertEqual(self.model.query(self.handle)[0], "STOPPING")
        self.model.stop_fact(self.handle, 7, "device_stopped", True)
        self.assertEqual(self.model.query(self.handle)[0], "SAFE_STOPPED")

    def test_x_t4_completion_and_cancel_have_ordered_outcomes(self):
        self.model.completion(7, 101, 0, 3, 0, b"abc", True)
        self.assertEqual(self.model.cancel(self.handle), "COMPLETED")
        self.model.release(self.handle)
        handle, _ = self.model.submit("S1", 102, b"abc")
        self.assertEqual(self.model.cancel(handle), "STOPPING")
        self.assertFalse(self.model.completion(7, 102, 0, 3, 0, b"abc", True))
        self.assertEqual(self.model.query(handle)[0], "STOPPING")

    def test_x_t4_late_old_event_cannot_complete_new_epoch_or_reexecute(self):
        self.model.cancel(self.handle)
        for kind in ("device_stopped", "platform_drained"):
            self.model.stop_fact(self.handle, 7, kind, True)
        self.model.release(self.handle)
        new_handle, _ = self.model.submit("S1", 102, b"abc")
        self.assertEqual(new_handle[1], 8)
        self.assertFalse(self.model.completion(7, 101, 0, 3, 0, b"abc", True))
        self.assertEqual(self.model.submit("S1", 101, bytes.fromhex("00 01 ff")), (self.handle, "RELEASED"))
        self.assertEqual(self.model.query(new_handle)[0], "ACCEPTED")

    def test_x_t1_native_wire_golden_bytes(self):
        descriptor = struct.pack("<QQQII", 0x1000, 0x2000, 101, 3, 7)
        self.assertEqual(descriptor.hex(), "0010000000000000002000000000000065000000000000000300000007000000")
        complete = struct.pack("<QIIII", 101, 7, 0, 3, 0)
        self.assertEqual(complete.hex(), "650000000000000007000000000000000300000000000000")

    def test_retained_identity_history_is_bounded_without_forgetting_old_ids(self):
        self.model.completion(7, 101, 0, 3, 0, b"abc", True)
        self.model.release(self.handle)
        for request_id in range(102, 357):
            handle, _ = self.model.submit("S1", request_id, b"x")
            self.model.completion(7, request_id, 0, 1, 0, b"y", True)
            self.model.release(handle)
        with self.assertRaisesRegex(ValueError, "LEDGER_FULL"):
            self.model.submit("S1", 357, b"x")
        self.assertEqual(self.model.submit("S1", 101, bytes.fromhex("00 01 ff")), (self.handle, "RELEASED"))

    def test_error_completion_requires_valid_final_record(self):
        self.assertFalse(self.model.completion(7, 101, 1, 3, 0, b"", True))
        self.assertTrue(self.model.completion(7, 101, 1, 0, 0, b"", True))
        self.assertEqual(self.model.query(self.handle), ("FAILED", None))
        self.assertEqual(self.model.release(self.handle), "RELEASED")

    def test_native_case_figure_is_local_and_has_explicit_boundaries(self):
        svg = ET.fromstring((ROOT / "docs/examples/xfer-sequence.svg").read_bytes())
        ids = [n.attrib["id"] for n in svg.iter() if "id" in n.attrib]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({"title", "desc", "legend"} <= set(ids))
        for node in svg.iter():
            self.assertNotIn(node.tag.rsplit("}", 1)[-1], ("script", "image", "foreignObject"))
            for key, value in node.attrib.items():
                self.assertFalse(key.lower().startswith("on"))
                if key.endswith("href"):
                    self.assertTrue(value.startswith("#"))
        text = " ".join(svg.itertext())
        for word in ("ACCEPTED", "COMPLETED", "RELEASED", "X-R1", "X-R2", "X-R3", "硬件 NOT_RUN"):
            self.assertIn(word, text)

    @unittest.skipUnless(shutil.which("cc"), "No C compiler: native layout not checked")
    def test_x_t1_native_c_layout_assertions(self):
        result = subprocess.run([shutil.which("cc"), "-std=c11", "-fsyntax-only", "-x", "c",
                                 str(ROOT / "docs/examples/xfer-native.h")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
