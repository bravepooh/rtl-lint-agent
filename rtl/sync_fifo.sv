// Synchronous FIFO, first-word fall-through.
//
// - Pointers carry one extra MSB, so full and empty are told apart without a separate flag:
//   equal pointers = empty, equal low bits with different MSB = full.
// - dout always shows the oldest entry while !empty (no read latency).
// - A push while full is dropped, a pop while empty is ignored. A push and pop on the same
//   cycle when full drops the push (simple and safe; documented rather than optimized).
// - DEPTH must be a power of two.

module sync_fifo #(
  parameter int WIDTH = 8,
  parameter int DEPTH = 8
) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   push,
  input  logic [WIDTH-1:0]       din,
  input  logic                   pop,
  output logic [WIDTH-1:0]       dout,
  output logic                   full,
  output logic                   empty,
  output logic [$clog2(DEPTH):0] count
);

  localparam int AW = $clog2(DEPTH);

  logic [WIDTH-1:0] mem [DEPTH];
  logic [AW:0]      wptr, rptr;
  logic             do_push, do_pop;

  assign do_push = push && !full;
  assign do_pop  = pop  && !empty;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      wptr <= '0;
      rptr <= '0;
    end else begin
      if (do_push) wptr <= wptr + (AW+1)'(1);
      if (do_pop)  rptr <= rptr + (AW+1)'(1);
    end
  end

  always_ff @(posedge clk) begin
    if (do_push) mem[wptr[AW-1:0]] <= din;
  end

  assign dout  = mem[rptr[AW-1:0]];
  assign count = wptr - rptr;
  assign empty = (wptr == rptr);
  assign full  = (wptr[AW] != rptr[AW]) && (wptr[AW-1:0] == rptr[AW-1:0]);

`ifdef FORMAL
  // Properties proven by SymbiYosys (formal/sync_fifo.sby). Immediate assertions with $past,
  // the subset open-source Yosys supports.
  localparam logic [AW:0] F_DEPTH = (AW+1)'(DEPTH);
  logic f_past_valid = 1'b0;
  always_ff @(posedge clk) f_past_valid <= 1'b1;

  initial assume (!rst_n);

  always_comb begin
    if (rst_n) begin
      assert (!(full && empty));                 // P1: never full and empty together
      assert (count <= F_DEPTH);                 // P2: occupancy within bounds
      assert (full  == (count == F_DEPTH));      // P3: full means exactly DEPTH entries
      assert (empty == (count == '0));           // P4: empty means zero entries
    end
  end

  always_ff @(posedge clk) begin
    if (f_past_valid && $past(rst_n) && rst_n) begin
      // P5: occupancy moves only by accepted pushes and pops, never by more than one
      assert (count == $past(count) + (AW+1)'($past(do_push)) - (AW+1)'($past(do_pop)));
      // P6: a push into a full FIFO is dropped (count does not grow past DEPTH)
      if ($past(full) && !$past(pop)) assert (count == $past(count));
      // P7: data written is held until it is read: the head entry is stable while not popped
      if (!$past(empty) && !$past(pop)) assert (dout == $past(dout));
    end
  end

  always_ff @(posedge clk) begin
    if (rst_n) begin
      cover (full);                              // full is reachable
      cover (f_past_valid && $past(full) && !full);   // and it drains again
    end
  end
`endif

endmodule
