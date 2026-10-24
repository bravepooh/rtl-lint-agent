"""The gate: decides whether a candidate fix is kept. The model never gets a vote.

Order matters: cheap checks first, formal last.

    1. compiles and lint improves:  fewer warnings than the original, no new warning codes
    2. no waivers:                  the candidate may not add lint_off / verilator pragmas
    3. interface frozen:            same ports, same directions, same widths
    4. behavior tests pass:         the module's cocotb tests, run on the candidate
    5. formal equivalence:          Yosys proves candidate == original

Verdicts:
    kept      all five pass
    review    1-4 pass, equivalence not proven. Behavior differs somewhere the tests do not look
              (a latch's don't-care states, a reset value, an unreachable state). A person decides.
    rejected  any of 1-4 fails
"""

import re
from collections import Counter
from pathlib import Path

from checks import equivalent, ports, run_tests
from lint import lint

WAIVER = re.compile(r"(lint_off|verilator\s+(coverage|tracing)_off|/\*\s*verilator\b|//\s*verilator\b)", re.I)


def judge(original, candidate, top, tests_dir):
    original, candidate = Path(original), Path(candidate)
    result = {"top": top, "checks": {}}
    chk = result["checks"]

    def reject(reason):
        result.update(verdict="rejected", reason=reason)
        return result

    before, after = lint(original), lint(candidate)
    result["warnings_before"], result["warnings_after"] = len(before), len(after)
    if any(w["code"] == "ERROR" for w in after):
        chk["lint"] = "fail"
        return reject("does not compile: " + next(w["message"] for w in after if w["code"] == "ERROR"))
    new_codes = sorted(set(Counter(w["code"] for w in after)) - set(w["code"] for w in before))
    if new_codes:
        chk["lint"] = "fail"
        return reject(f"introduced new warning types: {', '.join(new_codes)}")
    if len(after) >= len(before):
        chk["lint"] = "fail"
        return reject(f"warnings not reduced ({len(before)} to {len(after)})")
    chk["lint"] = "pass"

    added = [ln for ln in candidate.read_text().splitlines() if WAIVER.search(ln)]
    orig_waivers = [ln for ln in original.read_text().splitlines() if WAIVER.search(ln)]
    if len(added) > len(orig_waivers):
        chk["waivers"] = "fail"
        return reject("silenced the warning with a waiver pragma instead of fixing it")
    chk["waivers"] = "pass"

    try:
        p_before, p_after = ports(original, top), ports(candidate, top)
    except RuntimeError as e:
        chk["ports"] = "fail"
        return reject(f"interface could not be read: {e}")
    if p_before != p_after:
        diff = sorted(set(p_before.items()) ^ set(p_after.items()))
        chk["ports"] = "fail"
        return reject(f"changed the module interface: {diff}")
    chk["ports"] = "pass"

    ok, log = run_tests(candidate, top, tests_dir)
    if not ok:
        chk["tests"] = "fail"
        result["test_log"] = log
        return reject("behavior tests failed")
    chk["tests"] = "pass"

    proven, log = equivalent(original, candidate, top)
    chk["equivalence"] = "proven" if proven else "not proven"
    if not proven:
        result.update(verdict="review",
                      reason="tests pass but formal equivalence not proven: behavior changed "
                             "somewhere the tests do not check", equiv_log=log)
        return result
    result.update(verdict="kept", reason="lint improved, interface unchanged, tests pass, "
                                         "formally equivalent")
    return result
