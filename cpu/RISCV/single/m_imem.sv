module m_imem #(parameter int MEM_SIZE = 1024 // 4KB memory
)
(
    input  logic [31:0] addr_i,
    output logic [31:0] data_o
);

    logic [31:0] memory [0:MEM_SIZE-1];

    wire [29:0] word_index = addr_i[31:2];

    assign data_o = memory[word_index];

    initial begin
        $readmesh("program.hex", memory);
    end

endmodule
