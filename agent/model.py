"""Model backends. The agent only ever sees text in and text out; swapping models is one setting.

    AGENT_BACKEND=claude-cli   Claude Code CLI in headless mode, tools disabled (default)
    AGENT_BACKEND=anthropic    Anthropic API (needs ANTHROPIC_API_KEY)
    AGENT_BACKEND=ollama       a local model through Ollama, so design code never leaves the machine
    AGENT_MODEL=<name>         model for the chosen backend
"""

import json
import os
import re
import subprocess
import tempfile
import urllib.request

SYSTEM = """You fix Verilator lint warnings in SystemVerilog RTL.
Rules:
- Keep the design's behavior exactly the same. If a warning can only be fixed by changing
  behavior, make the smallest change and keep every documented behavior.
- Keep the module name, the port list, port directions and port widths exactly as they are.
- Do not add lint_off, waiver comments or any verilator pragma. Fix the code itself.
- Keep the existing comments.
Return only the complete corrected file inside one ```systemverilog code block. No other text."""

CODE = re.compile(r"```(?:systemverilog|verilog|sv)?\s*\n(.*?)```", re.S)


def prompt_for(source, warnings):
    lines = "\n".join(f"line {w['line']}: [{w['code']}] {w['message']}" for w in warnings)
    return f"Lint warnings:\n{lines}\n\nFile:\n```systemverilog\n{source}```"


def extract(text):
    m = CODE.search(text)
    if not m:
        raise ValueError("model reply had no code block")
    return m.group(1)


def _claude_cli(prompt, model):
    with tempfile.TemporaryDirectory() as cwd:  # empty cwd: no project files, no CLAUDE.md
        proc = subprocess.run(
            ["claude", "-p", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
             "--model", model, "--system-prompt", SYSTEM],
            input=prompt, capture_output=True, text=True, timeout=300, cwd=cwd,
        )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip()[-500:])
    return proc.stdout


def _anthropic(prompt, model):
    import anthropic
    msg = anthropic.Anthropic().messages.create(
        model=model, max_tokens=8000, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _ollama(prompt, model):
    body = json.dumps({"model": model, "system": SYSTEM, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["response"]


BACKENDS = {
    "claude-cli": (_claude_cli, "sonnet"),
    "anthropic": (_anthropic, "claude-sonnet-5-5"),
    "ollama": (_ollama, "qwen2.5-coder:14b"),
}


def config():
    backend = os.environ.get("AGENT_BACKEND", "claude-cli")
    fn, default_model = BACKENDS[backend]
    return backend, os.environ.get("AGENT_MODEL", default_model), fn


def propose(source, warnings):
    _, model, fn = config()
    return extract(fn(prompt_for(source, warnings), model))
