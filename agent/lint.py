"""Run Verilator lint and return warnings as structured data.

    lint(path) -> list of {"file", "line", "code", "message"}

CLI:
    python agent/lint.py rtl/                print warnings for every .sv file as JSON
    python agent/lint.py rtl/ --strict       exit 1 if any file has a warning (used by CI on rtl/)
"""

import json
import re
import subprocess
import sys
from pathlib import Path

LINE = re.compile(r"^%(Warning|Error)(?:-([A-Z_0-9]+))?: (?:([^:\s]+):(\d+):(?:\d+): )?(.*)$")


def lint(path, extra_args=()):
    proc = subprocess.run(
        ["verilator", "--lint-only", "-Wall", *extra_args, str(path)],
        capture_output=True, text=True, timeout=60,
    )
    out = []
    for raw in proc.stderr.splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        kind, code, file, line, msg = m.groups()
        if kind == "Error" and msg.startswith("Exiting due to"):
            continue
        out.append({
            "file": file or str(path),
            "line": int(line) if line else 0,
            "code": code or ("ERROR" if kind == "Error" else "WARNING"),
            "message": msg.strip(),
        })
    return out


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    target = Path(argv[0])
    strict = "--strict" in argv
    files = sorted(target.glob("*.sv")) if target.is_dir() else [target]
    report = {str(f): lint(f) for f in files}
    print(json.dumps(report, indent=1))
    total = sum(len(v) for v in report.values())
    print(f"{len(files)} files, {total} warnings", file=sys.stderr)
    return 1 if strict and total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
