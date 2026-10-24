# Run 2026-10-24 · Haiku

Backend `claude-cli`, model `haiku`.

| | count |
|---|---|
| Attempts | 27 |
| Kept (formally equivalent) | 19 |
| Sent to human review | 6 |
| Rejected | 2 |
| &nbsp;&nbsp;introduced new warning types | 2 |

| File | Attempt | Warnings | Verdict | Reason |
|---|---|---|---|---|
| `demo/avg2.sv` | 1 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/bcd_counter.sv` | 1 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/edge_det.sv` | 1 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/pipe_delay.sv` | 1 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/prio_enc.sv` | 1 | 2 to 0 | review | tests pass but formal equivalence not proven: behavior changed somewhere the tests do not check |
| `demo/round_div16.sv` | 1 | 1 to 1 | rejected | introduced new warning types: UNUSEDSIGNAL |
| `demo/sat_add.sv` | 1 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/seg7.sv` | 1 | 2 to 0 | review | tests pass but formal equivalence not proven: behavior changed somewhere the tests do not check |
| `demo/signed_mac.sv` | 1 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/avg2.sv` | 2 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/bcd_counter.sv` | 2 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/edge_det.sv` | 2 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/pipe_delay.sv` | 2 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/prio_enc.sv` | 2 | 2 to 0 | review | tests pass but formal equivalence not proven: behavior changed somewhere the tests do not check |
| `demo/round_div16.sv` | 2 | 1 to 1 | rejected | introduced new warning types: UNUSEDSIGNAL |
| `demo/sat_add.sv` | 2 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/seg7.sv` | 2 | 2 to 0 | review | tests pass but formal equivalence not proven: behavior changed somewhere the tests do not check |
| `demo/signed_mac.sv` | 2 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/avg2.sv` | 3 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/bcd_counter.sv` | 3 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/edge_det.sv` | 3 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/pipe_delay.sv` | 3 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/prio_enc.sv` | 3 | 2 to 0 | review | tests pass but formal equivalence not proven: behavior changed somewhere the tests do not check |
| `demo/round_div16.sv` | 3 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/sat_add.sv` | 3 | 2 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
| `demo/seg7.sv` | 3 | 2 to 0 | review | tests pass but formal equivalence not proven: behavior changed somewhere the tests do not check |
| `demo/signed_mac.sv` | 3 | 1 to 0 | kept | lint improved, interface unchanged, tests pass, formally equivalent |
