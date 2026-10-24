"""prio_enc: exhaustive over all 256 request vectors. idx is checked only when valid."""
import cocotb
from cocotb.triggers import Timer


@cocotb.test(timeout_time=100, timeout_unit="us")
async def exhaustive(dut):
    for req in list(range(256)) + list(range(255, -1, -1)):
        dut.req.value = req
        await Timer(1, unit="ns")
        assert int(dut.valid.value) == (req != 0), f"req {req:08b}: valid"
        if req:
            want = (req & -req).bit_length() - 1
            assert int(dut.idx.value) == want, f"req {req:08b}: idx {int(dut.idx.value)}, want {want}"
