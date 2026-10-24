// Fixes the latch with a default of 0 and the width with a cast. Correct per the spec
// (idx is don't-care when valid is 0) but no longer equivalent to the latch: needs a person.
module prio_enc (
  input  logic [7:0] req,
  output logic [2:0] idx,
  output logic       valid
);
  always_comb begin
    valid = 1'b0;
    idx   = 3'd0;
    for (int i = 7; i >= 0; i--) begin
      if (req[i]) begin
        idx   = 3'(i);
        valid = 1'b1;
      end
    end
  end
endmodule
