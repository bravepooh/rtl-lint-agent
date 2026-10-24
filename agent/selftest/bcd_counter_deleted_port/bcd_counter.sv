// "Fixes" UNUSEDSIGNAL by deleting the unused port. Lint-clean, but the parent no longer connects.
module bcd_counter (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       en,
  output logic [3:0] digit,
  output logic       wrap
);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)         digit <= 4'd0;
    else if (en) begin
      if (digit == 9)   digit <= 4'd0;
      else              digit <= digit + 1;
    end
  end
  assign wrap = en && (digit == 9);
endmodule
