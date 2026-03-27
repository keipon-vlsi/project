module m_pc #(parameter int XLEN=32)
(
    input  logic clk_i,
    input  logic reset_i,
    input  logic [XLEN-1:0] pc_next_i, 
    output logic [XLEN-1:0] pc_o          
);

    always_ff @(posedge clk_i or posedge reset_i) begin
        if (reset_i) begin
            pc_o <= 0;
        end
        else begin
            pc_o <= pc_next_i;
        end
    end

endmodule
