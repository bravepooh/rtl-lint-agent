"""sat_add: exhaustive over all 65,536 input pairs."""
import cocotb
from cocotb.triggers import Timer


@cocotb.test(timeout_time=5, timeout_unit="ms")
async def exhaustive(dut):
    for a in range(256):
        for b in range(256):
            dut.a.value = a
            dut.b.value = b
            await Timer(1, unit="ns")
            want = min(a + b, 255)
            assert int(dut.sum.value) == want, f"{a}+{b}: sum {int(dut.sum.value)}, want {want}"
            assert int(dut.sat.value) == (a + b > 255), f"{a}+{b}: sat {dut.sat.value}"
