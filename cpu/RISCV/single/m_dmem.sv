module m_dmem #(parameter int MEM_SIZE = 1024 // 4KB memory
)
(
    input  logic clk_i,
    input  logic write_enable_i,
    input  logic [3:0] byte_enable_i,
    input  logic [31:0] addr_i,      // byte address
    input  logic [31:0] write_data_i,
    output logic [31:0] read_data_o,
);

    logic [31:0] memory [0:MEM_SIZE-1];
    wire [29:0] word_index = addr_i[31:2];

    assign read_data_o = memory[word_index];

    always_ff @(posedge clk_i) begin
        if (write_enable_i) begin
            if (byte_enable_i[0]) begin
                memory[word_index][7:0] <= write_data_i[7:0];
            end
            if (byte_enable_i[1]) begin
                memory[word_index][15:8] <= write_data_i[15:8];
            end
            if (byte_enable_i[2]) begin
                memory[word_index][23:16] <= write_data_i[23:16];
            end
            if (byte_enable_i[3]) begin
                memory[word_index][31:24] <= write_data_i[31:24];
            end
        end
    end        
endmodule
