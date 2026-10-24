# Lint rule cheat sheet

Each rule has a minimal example in `lint-gallery/` that triggers it (`make gallery` lists the codes
Verilator 5 reports). The "why it matters" column is the part that gets a designer to accept a rule.

| Rule | Verilator code | What it catches | Why it matters in silicon | Example |
|---|---|---|---|---|
| No inferred latches | `LATCH` | A signal not assigned on every path through `always_comb` | Latches are level-sensitive: static timing, scan insertion and equivalence checking all assume flops. A surprise latch is a timing hole | `latch.sv` |
| Complete case statements | `CASEINCOMPLETE` | `case` without `default` that does not cover every value | The uncovered values hold the old output, which is a latch through the back door | `case_incomplete.sv` |
| One driver per signal | `MULTIDRIVEN` | Two processes assigning the same signal | Simulation picks a winner by scheduling order; synthesis errors out or shorts outputs. Sim and silicon disagree | `multidriven.sv` |
| Non-blocking in sequential logic | `BLKSEQ` | `=` inside `always_ff` | Later statements see the new value, so pipelines collapse in simulation. Order-dependent code that synthesis may build differently | `blocking_seq.sv` |
| Blocking in combinational logic | `COMBDLY` | `<=` inside `always_comb` | Reads later in the block see stale values; simulation needs extra delta cycles and can disagree with synthesis | `nonblocking_comb.sv` |
| No silent truncation | `WIDTHTRUNC` | Assigning a wider expression to a narrower target | Drops the MSBs, often the carry or sign, with no one deciding to | `width_trunc.sv` |
| No silent extension | `WIDTHEXPAND` | Assigning a narrower expression to a wider target | Usually harmless zero-fill; hides sign-extension bugs on signed math | `width_expand.sv` |
| No unused signals | `UNUSEDSIGNAL` | A declared input or signal nobody reads | Usually a forgotten connection. When intentional (reserved port), say so explicitly, do not waive blindly | `unused.sv` |
| No undriven signals | `UNDRIVEN` | An output or wire nothing drives | Floats to X in simulation, to whatever synthesis ties it to in silicon | `unused.sv` |
| No implicit nets | `IMPLICIT` | Using an undeclared name in a port connection | Verilog quietly creates a 1-bit wire, so a typo becomes a silent bug. Use `` `default_nettype none `` | `implicit_net.sv` |
| No combinational loops | `UNOPTFLAT` | A signal that depends on itself with no flop in between | An oscillator or an unintended latch. Breaks static timing completely | `comb_loop.sv` |
| One module per file, named like the file | `DECLFILENAME` | Module name different from the file name | Tools, scripts and people find modules by filename | `filename.sv` |
| Sync or async reset, not both | `SYNCASYNCNET` | A reset used asynchronously in one place and as data in another | Reset trees, reset-domain checks and STA treat async resets specially; mixing defeats all three | `async_reset_mix.sv` |

## Rules a lint tool alone cannot check

These need structural CDC/RDC tools (or formal), and are where a methodology team earns its keep:

- **Clock domain crossing.** Single bits cross through a two-flop synchronizer (`rtl/sync_2ff.sv`);
  multi-bit values cross as Gray code or through a handshake or async FIFO (`rtl/async_fifo.sv`).
  Simulation does not model metastability, so a binary pointer crossing can pass every test.
- **Reset domain crossing.** A flop reset by one reset feeding a flop in another reset domain can go
  metastable when only one of them is asserted.
- **Reset deassertion.** Assert asynchronously, deassert synchronously (a reset synchronizer per
  domain), so all flops leave reset on the same edge.

## Running a rule set well

- **False positives kill adoption.** A rule that fires on correct code teaches designers to ignore
  the report. Tune or drop it before rolling it out.
- **Waivers are reviewed decisions,** with a reason and an owner, never a quick way to get green.
  The agent in this repo is forbidden from adding them (`agent/gate.py`).
- **Gate in CI on new warnings,** not only on the total, so a legacy block can adopt a rule without
  fixing everything on day one.
