// Asynchronous (dual-clock) FIFO, Cummings style.
//
// - Each side keeps a binary pointer (to address memory) and a Gray copy (to cross domains).
//   Gray code changes one bit per increment, so a two-flop synchronizer can only ever see the
//   old or the new value, never a mix.
// - full is computed in the write domain against the synchronized read pointer;
//   empty in the read domain against the synchronized write pointer. Both are pessimistic
//   (a pointer seen late makes the FIFO look fuller or emptier, never the reverse), which is safe.
// - full: next write Gray equals the read Gray with its top two bits inverted.
// - First-word fall-through: dout shows the head entry while !empty.
// - DEPTH must be a power of two, at least 4.

module async_fifo #(
  parameter int WIDTH = 8,
  parameter int DEPTH = 8
) (
  // write domain
  input  logic             wclk,
  input  logic             wrst_n,
  input  logic             push,
  input  logic [WIDTH-1:0] din,
  output logic             full,
  // read domain
  input  logic             rclk,
  input  logic             rrst_n,
  input  logic             pop,
  output logic [WIDTH-1:0] dout,
  output logic             empty
);

  localparam int AW = $clog2(DEPTH);

  logic [WIDTH-1:0] mem [DEPTH];

  logic [AW:0] wbin, wgray, wbin_next, wgray_next;
  logic [AW:0] rbin, rgray, rbin_next, rgray_next;
  logic [AW:0] rgray_w1, rgray_w2;   // read pointer synchronized into the write domain
  logic [AW:0] wgray_r1, wgray_r2;   // write pointer synchronized into the read domain

  // ---------------- write domain ----------------
  assign wbin_next  = wbin + (AW+1)'(push && !full);
  assign wgray_next = wbin_next ^ (wbin_next >> 1);   // binary to Gray

  always_ff @(posedge wclk or negedge wrst_n) begin
    if (!wrst_n) begin
      wbin  <= '0;
      wgray <= '0;
    end else begin
      wbin  <= wbin_next;
      wgray <= wgray_next;
    end
  end

  always_ff @(posedge wclk) begin
    if (push && !full) mem[wbin[AW-1:0]] <= din;
  end

  always_ff @(posedge wclk or negedge wrst_n) begin
    if (!wrst_n) begin
      rgray_w1 <= '0;
      rgray_w2 <= '0;
    end else begin
      rgray_w1 <= rgray;
      rgray_w2 <= rgray_w1;
    end
  end

  always_ff @(posedge wclk or negedge wrst_n) begin
    if (!wrst_n) full <= 1'b0;
    else         full <= (wgray_next == {~rgray_w2[AW:AW-1], rgray_w2[AW-2:0]});
  end

  // ---------------- read domain ----------------
  assign rbin_next  = rbin + (AW+1)'(pop && !empty);
  assign rgray_next = rbin_next ^ (rbin_next >> 1);

  always_ff @(posedge rclk or negedge rrst_n) begin
    if (!rrst_n) begin
      rbin  <= '0;
      rgray <= '0;
    end else begin
      rbin  <= rbin_next;
      rgray <= rgray_next;
    end
  end

  always_ff @(posedge rclk or negedge rrst_n) begin
    if (!rrst_n) begin
      wgray_r1 <= '0;
      wgray_r2 <= '0;
    end else begin
      wgray_r1 <= wgray;
      wgray_r2 <= wgray_r1;
    end
  end

  always_ff @(posedge rclk or negedge rrst_n) begin
    if (!rrst_n) empty <= 1'b1;
    else         empty <= (rgray_next == wgray_r2);
  end

  assign dout = mem[rbin[AW-1:0]];

endmodule
