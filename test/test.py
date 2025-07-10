# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0



import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def test_project(dut):
    """Cocotb test for tt_um_gene_matcher"""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())  # 100 MHz clock
    dut._log.info("Starting testbench...")

    dut.ena.value = 1
    dut.rst_n.value = 0
    await Timer(20, units="ns")
    dut.rst_n.value = 1
    dut._log.info("Reset deasserted.")

    # Helper function
    async def check_match(ui, ref, expected):
        dut.ui_in.value = ui
        dut.uio_in.value = ref
        await Timer(20, units="ns")
        actual = dut.uo_out.value.integer & 1
        assert actual == expected, f"Expected {expected}, got {actual}"

    # Test cases
    await check_match(0b00011011, 0b00011011, 1)  # ACGT vs ACGT
    await check_match(0b00011011, 0b01011011, 0)  # ACGT vs CCGT
    await check_match(0b00000000, 0b00000000, 1)  # all zeros
    await check_match(0b11111111, 0b11111111, 1)  # all ones
    await check_match(0b10101010, 0b11111111, 0)  # mismatch

    dut._log.info("All tests passed!")
