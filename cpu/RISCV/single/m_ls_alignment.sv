module m_ls_alignment
(
    input  logic [1:0] addr_offset_i, // 2-bit offset for byte/halfword alignment (addr[1:0])
    input  logic [2:0] funct3_i,      // funct3 field from instruction to determine load/store type

    // For store 
    input  logic [31:0] store_data_i,
    output logic [31:0] mem_write_data_o,
    output logic [3:0]  mem_byte_enable_o,

    // For load
    input  logic [31:0] mem_read_data_i,
    output logic [31:0] load_data_o
);
    // store data alignment & byte enable generation
    always_comb begin
        mem_write_data_o = store_data_i;
        mem_byte_enable_o = 4'b0000;

        // SB:00, SH:01, SW:10
        case (funct3_i[1:0])
            2'b00: begin // store byte
                mem_write_data_o = {4{store_data_i[7:0]}};
                mem_byte_enable_o = 4'b0001 << addr_offset_i;
            end
            2'b01: begin // store halfword
                mem_write_data_o = {2{store_data_i[15:0]}};
                mem_byte_enable_o = (addr_offset_i[1] == 1'b0) ? 4'b0011 : 4'b1100;
            end
            2'b10: begin // store word
                mem_write_data_o = store_data_i;
                mem_byte_enable_o = 4'b1111;
            end
            default: ;
        endcase
    end

    // load data alignement
    logic [7:0] extracted_byte;
    logic [15:0] extracted_half;

    always_comb begin
        case (addr_offset_i)
            2'b00: extracted_byte = mem_read_data_i[7:0]; 
            2'b01: extracted_byte = mem_read_data_i[15:8];
            2'b10: extracted_byte = mem_read_data_i[23:16];
            2'b11: extracted_byte = mem_read_data_i[31:24];
        endcase

        extracted_half = (addr_offset_i[1] == 1'b0) ? mem_read_data_i[15:0] : mem_read_data_i[31:16];

        case (funct3_i)
        3'b000: load_data_o = {24{extracted_byte[7]}, extracted_byte};  // LB
        3'b001: load_data_o = {16{extracted_half[15]}, extracted_half}; // LH
        3'b010: laod_data_o = mem_read_data_i;                          // LW
        3'b100: load_data_o = {24{1'b0}, extracted_byte};               // LBU
        3'b101: load_data_o = {16{1'b0}, extracted_half};               // LHU
        default: load_data_o = 32'b0;
        endcase
    end
endmodule
