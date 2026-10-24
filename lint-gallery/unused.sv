// RULE: no unused or undriven signals.
// spare is never read and dbg is never driven. Both usually mean a forgotten connection.
module unused (
  input  logic a,
  input  logic spare,
  output logic y,
  output logic dbg
);
  assign y = a;
endmodule
