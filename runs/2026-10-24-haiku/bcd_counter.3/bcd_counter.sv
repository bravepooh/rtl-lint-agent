// Decimal counter 0..9 with enable and wrap flag. dbg_en is reserved for a debug hook that is not
// wired yet; the port must stay (the parent instantiates it).
module bcd_counter (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       en,
  input  logic       dbg_en,
  output logic [3:0] digit,
  output logic       wrap
);
  // Reserved for the debug hook: read here so the port is used, no effect on behavior.
  logic unused_dbg_en;
  assign unused_dbg_en = dbg_en;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)         digit <= 4'd0;
    else if (en) begin
      if (digit == 9)   digit <= 4'd0;
      else              digit <= digit + 1;
    end
  end
  assign wrap = en && (digit == 9);
endmodule
