`default_nettype none
`timescale 1ns / 1ps

/* Testbench for tt_um_gene_matcher.
   Use this with cocotb or Icarus Verilog to simulate matching DNA sequences.
*/
module tb ();

  // VCD dump for waveform viewing
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
  end

  // Testbench signals
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;    // gene_sequence
  reg [7:0] uio_in;   // reference_sequence
  wire [7:0] uo_out;  // match result
  wire [7:0] uio_out; // unused
  wire [7:0] uio_oe;  // unused

  // Instantiate DUT (device under test)
  tt_um_gene_matcher user_project (
      .ui_in   (ui_in),
      .uo_out  (uo_out),
      .uio_in  (uio_in),
      .uio_out (uio_out),
      .uio_oe  (uio_oe),
      .ena     (ena),
      .clk     (clk),
      .rst_n   (rst_n)
  );

  // Clock generation (100 MHz)
  initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  // Test sequence
  initial begin
    // Initial states
    ena   = 1;
    rst_n = 1;
    ui_in = 8'b00000000;
    uio_in = 8'b00000000;

    #10;

    // Test Case 1: Match (A C G T => 00 01 10 11 => 00011011)
    ui_in  = 8'b00011011;
    uio_in = 8'b00011011;
    #10;
    $display("Test 1 - Expected: 1, Actual: %b", uo_out[0]);

    // Test Case 2: No Match (ACGT vs. CCGT)
    ui_in  = 8'b00011011;
    uio_in = 8'b01011011;
    #10;
    $display("Test 2 - Expected: 0, Actual: %b", uo_out[0]);

    // Test Case 3: All zeros
    ui_in  = 8'b00000000;
    uio_in = 8'b00000000;
    #10;
    $display("Test 3 - Expected: 1, Actual: %b", uo_out[0]);

    // Test Case 4: All ones
    ui_in  = 8'b11111111;
    uio_in = 8'b11111111;
    #10;
    $display("Test 4 - Expected: 1, Actual: %b", uo_out[0]);

    // Test Case 5: Partial mismatch
    ui_in  = 8'b10101010;
    uio_in = 8'b11111111;
    #10;
    $display("Test 5 - Expected: 0, Actual: %b", uo_out[0]);

    $finish;
  end

endmodule

