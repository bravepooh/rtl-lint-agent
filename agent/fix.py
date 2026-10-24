"""The fix agent: lint each file, ask the model for a fix, let the gate decide.

    python agent/fix.py demo/                 one attempt per file
    python agent/fix.py demo/ --runs 3        three independent attempts per file (models vary)
    python agent/fix.py demo/ --apply         write kept fixes back over the originals

The originals are never touched unless --apply is given, and only for verdict "kept".
Every attempt is saved under runs/<timestamp>/ (candidate, diff, verdict) plus summary.md.
"""

import argparse
import difflib
import json
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate import judge  # noqa: E402
from lint import lint  # noqa: E402
from model import config, propose  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def attempt(src, run_dir, n, tests_dir):
    top = src.stem
    before = lint(src)
    rec = {"file": str(src.relative_to(ROOT)), "attempt": n, "warnings_before": len(before),
           "codes_before": sorted({w["code"] for w in before})}
    if not before:
        return {**rec, "verdict": "clean", "reason": "no warnings"}
    work = run_dir / f"{top}.{n}"
    work.mkdir(parents=True)
    t0 = time.time()
    try:
        fixed = propose(src.read_text(), before)
    except Exception as e:  # model or parsing failure is a rejected attempt, not a crash
        return {**rec, "verdict": "rejected", "reason": f"model error: {e}"}
    rec["model_seconds"] = round(time.time() - t0, 1)
    cand = work / f"{top}.sv"          # filename must match the module (DECLFILENAME)
    cand.write_text(fixed)
    diff = "".join(difflib.unified_diff(src.read_text().splitlines(True), fixed.splitlines(True),
                                        f"a/{src.name}", f"b/{src.name}"))
    (work / "diff.patch").write_text(diff)
    verdict = judge(src, cand, top, tests_dir)
    (work / "verdict.json").write_text(json.dumps(verdict, indent=1))
    return {**rec, **{k: verdict[k] for k in ("verdict", "reason", "checks", "warnings_after")},
            "codes_after": sorted({w["code"] for w in lint(cand)}), "dir": str(work.relative_to(ROOT))}


def summarize(records, run_dir, backend, model):
    tried = [r for r in records if r["verdict"] != "clean"]
    c = Counter(r["verdict"] for r in tried)
    why = Counter(r["reason"].split(":")[0] for r in tried if r["verdict"] == "rejected")
    lines = [f"# Run {run_dir.name}", "", f"Backend `{backend}`, model `{model}`.", "",
             "| | count |", "|---|---|",
             f"| Attempts | {len(tried)} |", f"| Kept (formally equivalent) | {c['kept']} |",
             f"| Sent to human review | {c['review']} |", f"| Rejected | {c['rejected']} |"]
    for reason, k in why.most_common():
        lines.append(f"| &nbsp;&nbsp;{reason} | {k} |")
    lines += ["", "| File | Attempt | Warnings | Verdict | Reason |", "|---|---|---|---|---|"]
    for r in tried:
        lines.append(f"| `{r['file']}` | {r['attempt']} | {r['warnings_before']} to "
                     f"{r.get('warnings_after', '-')} | {r['verdict']} | {r['reason']} |")
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", type=Path)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--tests", type=Path, default=None, help="cocotb tests dir (default <target>/tests)")
    args = ap.parse_args()

    target = args.target.resolve()
    tests_dir = (args.tests or target / "tests").resolve()
    backend, model, _ = config()
    run_dir = ROOT / "runs" / time.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True)
    files = sorted(target.glob("*.sv"))
    records = []
    for n in range(1, args.runs + 1):
        for src in files:
            rec = attempt(src, run_dir, n, tests_dir)
            records.append(rec)
            print(f"[{n}/{args.runs}] {src.name:18} {rec['verdict']:9} {rec['reason']}", flush=True)
            with open(run_dir / "results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            if args.apply and rec["verdict"] == "kept":
                shutil.copy(ROOT / rec["dir"] / src.name, src)
    print()
    print(summarize(records, run_dir, backend, model))


if __name__ == "__main__":
    main()
