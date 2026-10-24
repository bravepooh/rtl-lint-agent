"""Deterministic checks the gate runs on a candidate fix. None of them involve the model.

    ports(path, top)                  -> {port: (direction, width)}   via Yosys
    run_tests(candidate, top, tests)  -> (passed, log_tail)          via cocotb
    equivalent(gold, gate, top)       -> (proven, log_tail)          via Yosys equiv_* (formal)
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _env():
    env = dict(os.environ)
    venv_bin = ROOT / ".venv" / "bin"
    if venv_bin.is_dir():
        env["PATH"] = f"{venv_bin}{os.pathsep}{env['PATH']}"
    return env


def _tail(text, n=25):
    return "\n".join(text.strip().splitlines()[-n:])


def ports(path, top):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "m.json"
        path = _as_star(path, Path(tmp) / "m.sv")   # see equivalent(): latches must not abort the read
        proc = subprocess.run(
            ["yosys", "-q", "-p", f"read_verilog -sv {path}; hierarchy -top {top}; proc; write_json {out}"],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0 or not out.exists():
            raise RuntimeError(_tail(proc.stdout + proc.stderr))
        mod = json.loads(out.read_text())["modules"][top]
        return {name: (p["direction"], len(p["bits"])) for name, p in mod["ports"].items()}


def run_tests(candidate, top, tests_dir):
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            ["make", "-s", "-C", str(tests_dir), f"TOP={top}", f"SRC={Path(candidate).resolve()}",
             f"SIM_BUILD={tmp}/build", f"COCOTB_RESULTS_FILE={tmp}/results.xml"],
            capture_output=True, text=True, timeout=600, env=_env(),
        )
        log = proc.stdout + proc.stderr
        passed = proc.returncode == 0 and "FAIL=0" in log and "TESTS=" in log
        return passed, _tail(log, 12)


def _as_star(src, dst):
    dst.write_text(Path(src).read_text().replace("always_comb", "always @*"))
    return dst


def equivalent(gold, gate, top, seq=8):
    """Formal equivalence of two versions of the same module (Yosys equiv_make/simple/induct).

    Proven means: for every input sequence, from matching state, the outputs and registers agree.
    Not proven means they differ somewhere, or the solver could not show they don't. Either way a
    human looks before the change is accepted.
    """
    # Yosys refuses an always_comb that infers a latch. For the comparison only, read both sides
    # as always @* so a latch is modeled (and then shows up as a difference) instead of aborting.
    tmp = tempfile.mkdtemp()
    gold, gate = _as_star(gold, Path(tmp) / "gold.sv"), _as_star(gate, Path(tmp) / "gate.sv")
    script = f"""
        read_verilog -sv {gold}; prep -top {top}; async2sync; memory_map; opt_clean
        rename {top} gold; design -stash gold
        read_verilog -sv {gate}; prep -top {top}; async2sync; memory_map; opt_clean
        rename {top} gate; design -stash gate
        design -copy-from gold -as gold gold
        design -copy-from gate -as gate gate
        equiv_make gold gate equiv
        hierarchy -top equiv
        equiv_simple -seq {seq}
        equiv_induct -seq {seq}
        equiv_status -assert
    """
    proc = subprocess.run(["yosys", "-q", "-p", script], capture_output=True, text=True, timeout=300)
    return proc.returncode == 0, _tail(proc.stdout + proc.stderr, 8)
