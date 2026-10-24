// 8-input priority encoder: idx = position of the lowest set bit of req, valid = |req.
// When valid is 0, idx is don't-care.
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
