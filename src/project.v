/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none


module tt_um_gene_matcher (
    input  wire [7:0] ui_in,    // Dedicated inputs (gene_sequence)
    output wire [7:0] uo_out,   // Dedicated outputs (match flag on bit 0)
    input  wire [7:0] uio_in,   // IOs: Input path (reference_sequence)
    output wire [7:0] uio_out,  // IOs: Output path (not used)
    output wire [7:0] uio_oe,   // IOs: Enable path (all input => 0)
    input  wire       ena,      // always 1 when the design is powered
    input  wire       clk,      // clock (not used)
    input  wire       rst_n     // reset_n (not used)
);

    // Compare the sequences
    wire match = (ui_in == uio_in);

    // Output match result on uo_out[0], other bits are 0
    assign uo_out  = {7'b0000000, match};
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Prevent unused warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
