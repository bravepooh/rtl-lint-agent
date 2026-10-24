# Bringing AI into a chip design flow

How I would approach it in a methodology team. This repo is a small worked example of the core
idea: the model proposes, deterministic checks decide.

## Where to start

Start where AI output is cheap to check and the check already exists:

1. **Lint and CDC report triage and fix suggestions.** High volume, repetitive, and every fix can be
   re-linted, re-simulated and formally compared to the original. That is what this repo does.
2. **Spec and methodology Q&A over internal documents (RAG).** Designers lose hours finding the
   right rule or the right register description. Answers cite the source paragraph, so they can be
   checked in seconds.
3. **Testbench, assertion and coverage scaffolding.** The output is code that runs. A wrong assertion
   fails loudly on known-good RTL.
4. **EDA script and flow glue.** Tcl and Python around the tools, where a mistake is visible on
   the first run.
5. **Regression and bug triage.** Clustering failures and summarizing logs and bug threads.

Generating production RTL from a spec comes last, and only inside a verification gate at least as
strong as the one for human code.

## How AI output is gated

The rule is simple: an AI change passes the same checks as a human change, in CI, and the model never
decides whether its own change is accepted. In this repo, a fix is kept only if:

- lint improves and no new warning type appears,
- no waiver pragma was added,
- the module interface is unchanged,
- the behavior tests pass,
- and Yosys formally proves the fixed module equivalent to the original.

A fix that passes the tests but is not proven equivalent goes to a person. On the latch fixes in this
demo that is exactly right: the fix is correct per the spec, but it changes outputs the tests do not
look at, and only a designer knows whether those outputs are truly don't-care.

The gate itself is tested: `agent/selftest.py` feeds it hand-written bad fixes (a dropped carry, a
deleted port, a waiver, a changed reset value) and fails CI if any slips through. A gate that never
rejects anything looks exactly like a gate that works.

## How to measure it

- A frozen benchmark from real past work (closed lint reports, solved bugs), so results compare
  across tools and model versions.
- Several runs per item, because outputs vary between runs.
- Report kept / sent to review / rejected, and the time a designer spends on review. The goal is
  designer hours saved, not model accuracy.
- Pilot with one team on one block before any rollout.

## How designers adopt it

- Start with a pain they already complain about, on their own block, with their own numbers.
- Volunteers first. One respected designer using it daily is worth more than a mandate.
- Low noise. A tool that is wrong often gets ignored, so a strict gate that sends doubtful cases to
  review is better than one that tries to auto-fix everything.
- Human approval stays on anything that changes behavior.
- Training with real examples from the team's code, including where the AI fails.

## Confidentiality

Design data is the company's most sensitive IP:

- Models run on-prem or in a private tenant. In this repo the backend is one setting
  (`AGENT_BACKEND=ollama` runs a local model, nothing leaves the machine).
- Retrieval (RAG) over internal specs rather than training on them where possible, with access control
  at the retrieval layer so a user only retrieves what they are allowed to read.
- Logs of prompts and outputs are kept like design data.

## What is published

- **ChipNeMo** (NVIDIA, 2023): domain-adapted LLMs for chip design, applied to an engineering assistant
  chatbot, EDA script generation, and bug summarization and analysis. The lesson I take: domain
  adaptation plus retrieval on internal data beats a general model on internal tasks.
- **VerilogEval** (NVIDIA, 2023): a benchmark for LLM-generated Verilog. The lesson: measure on a fixed
  benchmark before trusting a model with RTL.
- EDA vendors ship their own AI (Synopsys.ai, Cadence Cerebrus and JedAI). A methodology team's job is
  to evaluate them on the team's own benchmark, not the vendor's.
