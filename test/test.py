# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0



import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    """Testbench for DUT using cocotb"""

    dut._log.info("Starting testbench...")

    # Set up a clock with 10us period (i.e., 100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply Reset (active low)
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1  # Deassert reset
    dut._log.info("Reset deasserted.")

    # Wait for reset to propagate
    await ClockCycles(dut.clk, 2)

    # === Test Case 1: ui_in + uio_in = 50 ===
    dut.ui_in.value = 20
    dut.uio_in.value = 30
    await ClockCycles(dut.clk, 1)

    expected = 50
    actual = dut.uo_out.value.integer
    dut._log.info(f"Test Case 1: ui_in=20, uio_in=30 => uo_out={actual}")
    assert actual == expected, f"Test Case 1 Failed: expected {expected}, got {actual}"

    # === Test Case 2: ui_in + uio_in = 20 ===
    dut.ui_in.value = 15
    dut.uio_in.value = 5
    await ClockCycles(dut.clk, 1)

    expected = 20
    actual = dut.uo_out.value.integer
    dut._log.info(f"Test Case 2: ui_in=15, uio_in=5 => uo_out={actual}")
    assert actual == expected, f"Test Case 2 Failed: expected {expected}, got {actual}"

    # === Test Case 3: Edge Case - Zero ===
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)

    expected = 0
    actual = dut.uo_out.value.integer
    dut._log.info(f"Test Case 3: ui_in=0, uio_in=0 => uo_out={actual}")
    assert actual == expected, f"Test Case 3 Failed: expected {expected}, got {actual}"

    # === Test Case 4: Max values (255 + 255 = 510 mod 256 = 254) ===
    dut.ui_in.value = 255
    dut.uio_in.value = 255
    await ClockCycles(dut.clk, 1)

    expected = (255 + 255) % 256  # In case DUT is 8-bit adder
    actual = dut.uo_out.value.integer
    dut._log.info(f"Test Case 4: ui_in=255, uio_in=255 => uo_out={actual}")
    assert actual == expected, f"Test Case 4 Failed: expected {expected}, got {actual}"

    dut._log.info("All tests completed successfully.")
