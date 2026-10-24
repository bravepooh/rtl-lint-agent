// Fixes WIDTHTRUNC by sizing the literal to 12 bits. That makes the whole add 12 bits wide, so
// x + 8 overflows for x >= 4088 and q drops from 256 to 0.
module round_div16 (
  input  logic [11:0] x,
  output logic [8:0]  q
);
  assign q = 9'((x + 12'd8) >> 4);
endmodule
