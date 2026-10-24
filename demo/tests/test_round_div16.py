"""round_div16: exhaustive over all 4096 inputs, including the top of the range."""
import cocotb
from cocotb.triggers import Timer


@cocotb.test(timeout_time=1, timeout_unit="ms")
async def exhaustive(dut):
    for x in range(4096):
        dut.x.value = x
        await Timer(1, unit="ns")
        want = (x + 8) // 16
        assert int(dut.q.value) == want, f"x={x}: q {int(dut.q.value)}, want {want}"
