// RULE: no silent zero-extension.
// A 4-bit value lands in an 8-bit port. Usually harmless, sometimes it hides a sign bug.
module width_expand (
  input  logic [3:0] narrow,
  output logic [7:0] wide
);
  assign wide = narrow;
endmodule
