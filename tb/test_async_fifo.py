"""cocotb testbench for rtl/async_fifo.sv.

Writer and reader run on unrelated clocks (periods chosen so edges drift against each other).
The scoreboard checks that every word arrives, in order, exactly once, in both speed ratios.
"""

import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge

WIDTH = 8
N_WORDS = 600


async def run(dut, wperiod, rperiod, p_push, p_pop, seed):
    rng = random.Random(seed)
    cocotb.start_soon(Clock(dut.wclk, wperiod, unit="ns").start())
    cocotb.start_soon(Clock(dut.rclk, rperiod, unit="ns").start())
    dut.push.value = 0
    dut.pop.value = 0
    dut.din.value = 0
    dut.wrst_n.value = 0
    dut.rrst_n.value = 0
    await ClockCycles(dut.wclk, 3)
    await ClockCycles(dut.rclk, 3)
    dut.wrst_n.value = 1
    dut.rrst_n.value = 1

    sent = [rng.randrange(1 << WIDTH) for _ in range(N_WORDS)]
    got = []
    seen = {"full": 0, "empty": 0}

    async def writer():
        i = 0
        while i < N_WORDS:
            await FallingEdge(dut.wclk)
            want = rng.random() < p_push
            dut.push.value = int(want)
            dut.din.value = sent[i]
            await RisingEdge(dut.wclk)
            if int(dut.full.value):
                seen["full"] += 1
            elif want:
                i += 1                      # accepted: the full flag was low at this edge
        await FallingEdge(dut.wclk)
        dut.push.value = 0

    async def reader():
        while len(got) < N_WORDS:
            await FallingEdge(dut.rclk)
            want = rng.random() < p_pop
            empty = int(dut.empty.value)
            if not empty and want:
                got.append(int(dut.dout.value))
                k = len(got) - 1
                assert got[k] == sent[k], f"word {k}: got {got[k]:#x}, sent {sent[k]:#x}"
            if empty:
                seen["empty"] += 1
            dut.pop.value = int(want and not empty)
            await RisingEdge(dut.rclk)
        await FallingEdge(dut.rclk)
        dut.pop.value = 0

    w = cocotb.start_soon(writer())
    r = cocotb.start_soon(reader())
    await w
    await r
    assert got == sent
    await ClockCycles(dut.rclk, 6)
    assert int(dut.empty.value) == 1, "FIFO not empty after all words were read"
    dut._log.info("%d words in order; write saw full %d times, read saw empty %d times",
                  len(got), seen["full"], seen["empty"])
    return seen


@cocotb.test(timeout_time=200, timeout_unit="us")   # a stuck full/empty flag must fail, not hang
async def fast_writer_slow_reader(dut):
    seen = await run(dut, wperiod=10, rperiod=23, p_push=0.9, p_pop=0.7, seed=1)
    assert seen["full"] > 0, "full never exercised"


@cocotb.test(timeout_time=200, timeout_unit="us")
async def slow_writer_fast_reader(dut):
    seen = await run(dut, wperiod=27, rperiod=10, p_push=0.6, p_pop=0.9, seed=2)
    assert seen["empty"] > 0, "empty never exercised"
