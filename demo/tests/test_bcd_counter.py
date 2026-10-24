"""bcd_counter: counts 0..9 on en, wraps, wrap flag on 9 with en. Port list is fixed."""
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


@cocotb.test(timeout_time=100, timeout_unit="us")
async def counts(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.en.value = 0
    dut.dbg_en.value = 0
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    rng = random.Random(5)
    model = 0
    for cyc in range(500):
        await FallingEdge(dut.clk)
        en = int(rng.random() < 0.7)
        dut.en.value = en
        dut.dbg_en.value = rng.randrange(2)
        assert int(dut.digit.value) == model, f"cycle {cyc}: digit {int(dut.digit.value)}, want {model}"
        await cocotb.triggers.Timer(1, unit="ns")
        assert int(dut.wrap.value) == (en and model == 9), f"cycle {cyc}: wrap"
        await RisingEdge(dut.clk)
        if en:
            model = 0 if model == 9 else model + 1
