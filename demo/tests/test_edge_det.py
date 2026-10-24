"""edge_det: pulse == sig & ~sig_previous_cycle."""
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer


@cocotb.test(timeout_time=100, timeout_unit="us")
async def pulses(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.sig.value = 0
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    rng = random.Random(3)
    prev = 0
    for cyc in range(400):
        await FallingEdge(dut.clk)
        v = rng.randrange(2)
        dut.sig.value = v
        await Timer(1, unit="ns")
        assert int(dut.pulse.value) == (v and not prev), f"cycle {cyc}: sig {v} prev {prev}"
        await RisingEdge(dut.clk)
        prev = v
