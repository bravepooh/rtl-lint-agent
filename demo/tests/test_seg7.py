"""seg7: the ten BCD digits. Inputs 10..15 are don't-care and not checked."""
import cocotb
from cocotb.triggers import Timer

SEG = [0b0111111, 0b0000110, 0b1011011, 0b1001111, 0b1100110,
       0b1101101, 0b1111101, 0b0000111, 0b1111111, 0b1101111]


@cocotb.test(timeout_time=100, timeout_unit="us")
async def digits(dut):
    for _ in range(3):
        for d in range(10):
            dut.bcd.value = d
            await Timer(1, unit="ns")
            assert int(dut.seg.value) == SEG[d], f"digit {d}: seg {int(dut.seg.value):07b}"
