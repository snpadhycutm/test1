<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The tt_um_gene_matcher project compares two 4-base DNA sequences, each encoded into 8 bits using 2-bit representations for A (00), C (01), G (10), and T (11). The module takes these sequences as inputs through ui_in and uio_in, compares them bit-by-bit, and outputs a match result on uo_out[0], which is 1 if the sequences are identical and 0 otherwise. It operates synchronously with a clock and is enabled via an ena signal. The testbench drives various DNA input patterns and checks the output to verify that the module correctly detects matching and mismatching sequences.

## How to test

To test the tt_um_gene_matcher project, first compile and run the Verilog code using any Verilog simulator such as Icarus Verilog. The project includes a testbench (tb.v) that automatically feeds sample DNA sequences into the module, compares them, and prints whether the result matches the expected output. After running the simulation, you can check the console output to see if all test cases pass. For a more detailed view, you can open the generated waveform file (tb.vcd) using a tool like GTKWave to visually inspect signal behavior. No manual input is needed—just run the simulation and review the results.

## External hardware

NA
