// RULE: no implicit nets.
// tmp is never declared. Verilog quietly creates a 1-bit wire, so a typo becomes a bug.
module implicit_net (
  input  logic a, b,
  output logic y
);
  and u_and (tmp, a, b);
  assign y = tmp;
endmodule
