// RULE: no combinational loops.
// x depends on y and y on x with no flop between: an oscillator or a latch, never what was meant.
module comb_loop (
  input  logic a,
  output logic y
);
  logic x;
  assign x = a & y;
  assign y = ~x;
endmodule
