"""avg2: one-cycle latency, floor((a + b) / 2)."""
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


@cocotb.test(timeout_time=100, timeout_unit="us")
async def one_cycle(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    rng = random.Random(9)
    prev = None
    for cyc in range(400):
        await FallingEdge(dut.clk)
        if prev is not None:
            want = (prev[0] + prev[1]) // 2
            assert int(dut.avg.value) == want, f"cycle {cyc}: avg {int(dut.avg.value)}, want {want}"
        a, b = rng.randrange(256), rng.randrange(256)
        dut.a.value, dut.b.value = a, b
        prev = (a, b)
