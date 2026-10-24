"""Gate self-test: hand-written candidate fixes with a known right answer.

A gate that never rejects anything looks exactly like a gate that works. This proves each check
catches the failure it exists for. No model involved, so CI runs it on every push.

    python agent/selftest.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gate import judge  # noqa: E402

DEMO = HERE.parent / "demo"

# case directory -> (expected verdict, the check that must decide it)
EXPECTED = {
    "sat_add_correct":          ("kept",     "equivalence"),
    "pipe_delay_correct":       ("kept",     "equivalence"),
    "sat_add_dropped_carry":    ("rejected", "tests"),
    "bcd_counter_deleted_port": ("rejected", "ports"),
    "edge_det_waiver":          ("rejected", "waivers"),
    "edge_det_reset_changed":   ("review",   "equivalence"),
    "prio_enc_default":         ("review",   "equivalence"),
    "signed_mac_zero_extend":   ("rejected", "tests"),
    "avg2_extra_cycle":         ("rejected", "tests"),
    "round_div16_sized_literal": ("rejected", "tests"),
}


def main():
    failures = 0
    for case, (want, deciding) in EXPECTED.items():
        cand = next((HERE / "selftest" / case).glob("*.sv"))
        top = cand.stem
        v = judge(DEMO / f"{top}.sv", cand, top, DEMO / "tests")
        ok = v["verdict"] == want and deciding in v["checks"]
        last = list(v["checks"])[-1] if v["checks"] else "-"
        ok = ok and last == deciding
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {case:26} {v['verdict']:9} decided by {last:12} {v['reason']}")
    print(f"\n{len(EXPECTED) - failures}/{len(EXPECTED)} gate checks behaved as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
