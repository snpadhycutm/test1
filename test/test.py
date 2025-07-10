# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0



import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock


@cocotb.test()
async def test_project(dut):
    """Cocotb test for tt_um_gene_matcher"""

    dut._log.info("Starting testbench...")
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())  # 100MHz clock

    # Apply initial values
    dut.rst_n.value = 0
    dut.ena.value = 1
    await Timer(20, units="ns")
    dut.rst_n.value = 1
    dut._log.info("Reset deasserted.")

    # Helper function
    async def run_test(ui, ref):
        dut.ui_in.value = ui
        dut.uio_in.value = ref
        await Timer(20, units="ns")
        expected = 1 if ui == ref else 0
        actual = dut.uo_out.value.integer & 1
        dut._log.info(f"ui_in={ui}, uio_in={ref} => uo_out={actual}")
        assert actual == expected, f"Mismatch: expected {expected}, got {actual}"

    # DNA Match Test Cases
    await run_test(0b00011011, 0b00011011)  # ACGT vs ACGT => Match
    await run_test(0b00011011, 0b01011011)  # ACGT vs CCGT => No match
    await run_test(0b00000000, 0b00000000)  # All zeros => Match
    await run_test(0b11111111, 0b11111111)  # All ones => Match
    await run_test(0b10101010, 0b11111111)  # Mismatch => No match

    dut._log.info("All tests passed!")

