"""pipe_delay: q equals d from two rising edges earlier."""
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


@cocotb.test(timeout_time=100, timeout_unit="us")
async def two_cycle_delay(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    rng = random.Random(7)
    hist = []
    for cyc in range(300):
        await FallingEdge(dut.clk)
        if len(hist) >= 2:
            assert int(dut.q.value) == hist[-2], f"cycle {cyc}: q {int(dut.q.value)}, want {hist[-2]}"
        v = rng.randrange(16)
        dut.d.value = v
        hist.append(v)
