module m_main_control
(
    input  logic [6:0] opcode_i,

    output logic alu_src_o,     // 1: Imm, 0: rs2
    output logic mem_to_reg_o,  // 1: load_data, 0: alu_result

    output logic reg_write_o,   // 1: write back to register
    output logic mem_read_o,    // 1: read from memory
    output logic mem_write_o,   // 1: write to memory
    output logic branch_o,      // 1: branch instruction

    output alu_op_main_e alu_op_o
);

    always_comb begin
        // default values
        alu_src_o           = 1'b0;
        mem_to_reg_o        = 1'b0;
        reg_write_o         = 1'b0;
        mem_read_o          = 1'b0;
        mem_write_o         = 1'b0;
        branch_o            = 1'b0;
        alu_op_o            = ALU_LOAD_STORE; // default value is ADD(address calculation)

        case (opcode_i)
        // R-type
        7'b0110011: begin
            reg_write_o     = 1'b1;         // write back to register
            alu_op_o        = ALU_R_I;
        end

        // I-type
        7'b0010011: begin
            alu_src_o       = 1'b1;         // Imm
            reg_write_o     = 1'b1;         // write back to register
            alu_op_o        = ALU_R_I;
        end

        // Load
        7'b0000011: begin
            alu_src_o       = 1'b1;     // Imm
            mem_to_reg_o    = 1'b1;     // load data to register
            reg_write_o     = 1'b1;     // write_back_to_register
            mem_read_o      = 1'b1;     // read from memory
            alu_op_o        = ALU_LOAD_STORE;
        end

        // Store
        7'b0100011: begin
            alu_src_o       = 1'b1;     // Imm to calculate address
            mem_write_o     = 1'b1;     // write to memory
            alu_op_o        = ALU_LOAD_STORE;
        end

        // Branch
        7'b1100011: begin
            branch_o        = 1'b1;    
            alu_op_o        = ALU_BRANCH;
        end

        default: ;
        endcase
    end

endmodule
