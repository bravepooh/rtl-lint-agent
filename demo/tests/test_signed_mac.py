"""signed_mac: random signed operands, clears and enables against a Python model."""
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


def wrap20(v):
    v &= (1 << 20) - 1
    return v - (1 << 20) if v & (1 << 19) else v


@cocotb.test(timeout_time=100, timeout_unit="us")
async def accumulate(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.clr.value = 0
    dut.en.value = 0
    dut.a.value = 0
    dut.b.value = 0
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    rng = random.Random(11)
    acc = 0
    for cyc in range(600):
        await FallingEdge(dut.clk)
        assert dut.acc.value.to_signed() == acc, f"cycle {cyc}: acc {dut.acc.value.to_signed()}, want {acc}"
        a, b = rng.randint(-128, 127), rng.randint(-128, 127)
        clr, en = int(rng.random() < 0.03), int(rng.random() < 0.8)
        dut.a.value, dut.b.value, dut.clr.value, dut.en.value = a & 0xFF, b & 0xFF, clr, en
        await RisingEdge(dut.clk)
        acc = 0 if clr else wrap20(acc + a * b) if en else acc
