"""cocotb testbench for rtl/sync_fifo.sv.

Inputs are driven on the falling edge and outputs checked on the falling edge, half a cycle
after the rising edge has committed. A Python deque is the reference model.
"""

import random
from collections import deque

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge

DEPTH = 8
WIDTH = 8


async def start(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.push.value = 0
    dut.pop.value = 0
    dut.din.value = 0
    dut.rst_n.value = 0
    for _ in range(3):
        await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)
    return deque()


def check(dut, model):
    n = len(model)
    assert int(dut.count.value) == n, f"count {int(dut.count.value)} != model {n}"
    assert int(dut.empty.value) == (n == 0), f"empty={dut.empty.value} with {n} entries"
    assert int(dut.full.value) == (n == DEPTH), f"full={dut.full.value} with {n} entries"
    if n:
        assert int(dut.dout.value) == model[0], f"dout {int(dut.dout.value):#x} != head {model[0]:#x}"


async def cycle(dut, model, push=0, pop=0, data=0):
    """Check state, drive one cycle of inputs, update the model the way the RTL should."""
    check(dut, model)
    dut.push.value = push
    dut.pop.value = pop
    dut.din.value = data
    await RisingEdge(dut.clk)
    was_full, was_empty = len(model) == DEPTH, len(model) == 0
    if pop and not was_empty:
        model.popleft()
    if push and not was_full:          # RTL drops a push while full, even with a pop
        model.append(data)
    await FallingEdge(dut.clk)


@cocotb.test(timeout_time=100, timeout_unit="us")
async def fill_then_drain(dut):
    """Overfill by two (both dropped), then drain and check order."""
    model = await start(dut)
    for i in range(DEPTH + 2):
        await cycle(dut, model, push=1, data=0xA0 + i)
    assert int(dut.full.value) == 1
    for _ in range(DEPTH):
        await cycle(dut, model, pop=1)
    check(dut, model)
    assert int(dut.empty.value) == 1


@cocotb.test(timeout_time=100, timeout_unit="us")
async def pop_when_empty_is_ignored(dut):
    model = await start(dut)
    for _ in range(4):
        await cycle(dut, model, pop=1)
    await cycle(dut, model, push=1, data=0x5A)
    check(dut, model)


@cocotb.test(timeout_time=100, timeout_unit="us")
async def push_and_pop_same_cycle(dut):
    """Half full, then simultaneous push+pop keeps occupancy constant."""
    model = await start(dut)
    for i in range(DEPTH // 2):
        await cycle(dut, model, push=1, data=i)
    for i in range(20):
        await cycle(dut, model, push=1, pop=1, data=0x40 + i)
        assert len(model) == DEPTH // 2


@cocotb.test(timeout_time=100, timeout_unit="us")
async def random_traffic(dut):
    """3000 random cycles in fill-heavy and drain-heavy phases, so full and empty are both hit."""
    rng = random.Random(1234)
    model = await start(dut)
    hits = {"full": 0, "empty": 0}
    for phase in range(30):
        p_push = 0.8 if phase % 2 == 0 else 0.2
        for _ in range(100):
            push = int(rng.random() < p_push)
            pop = int(rng.random() < 1 - p_push)
            await cycle(dut, model, push=push, pop=pop, data=rng.randrange(1 << WIDTH))
            hits["full"] += len(model) == DEPTH
            hits["empty"] += len(model) == 0
    check(dut, model)
    assert hits["full"] > 0 and hits["empty"] > 0, f"coverage holes: {hits}"
    dut._log.info("cycles at full=%d, at empty=%d", hits["full"], hits["empty"])
