module m_registers #(parameter int XLEN=32, parameter int REG_ADDR_WIDTH=5)
(
    input  logic                       clk_i,
    input  logic [REG_ADDR_WIDTH-1:0]  read_addr_1_i, read_addr_2_i, write_addr_i,
    input  logic [XLEN-1:0]            write_data_i,
    output logic [XLEN-1:0]            read_data_1_o, read_data_2_o,
    input  logic                       write_enable_i
);

    logic [XLEN-1:0] registers [0:(2**REG_ADDR_WIDTH)-1];

    //read out data from registers
    always_comb begin
        // port 1
        if (read_addr_1_i == 0) begin
            read_data_1_o = 0;
        end
        else begin
            read_data_1_o = registers[read_addr_1_i];
        end

        //port 2
        if (read_addr_2_i == 0) begin
            read_data_2_o = 0;
        end
        else begin
            read_data_2_o = registers[read_addr_2_i];
        end
    end

    //write data to registers
    always_ff @(posedge clk_i) begin
        if (write_enable_i && (write_addr_i != 0)) begin
            registers[write_addr_i] <= write_data_i;
        end
    end

endmodule
