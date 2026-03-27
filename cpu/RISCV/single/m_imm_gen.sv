module m_imm_gen #(parameter int XLEN=32)
(
    input  logic [XLEN-1:0] instruction_i,
    input  imm_type_e       imm_type_i,
    output logic [XLEN-1:0] imm_o     
);

    always_comb begin
        unique case(imm_type_i)
        IMM_TYPE_I: imm_o = 32'($signed(instruction_i[31:20]));
        IMM_TYPE_S: imm_o = 32'($signed({instruction_i[31:25], instruction_i[11:7]}));
        IMM_TYPE_B: imm_o = 32'($signed({instruction_i[31], instruction_i[7], instruction_i[30:25], instruction_i[11:8], 1'b0}));
        IMM_TYPE_U: imm_o = 32'({instruction_i[31:12], 12'b0});
        IMM_TYPE_J: imm_o = 32'($signed({instruction_i[31], instruction_i[19:12], instruction_i[20], instruction_i[30:21], 1'b0}));
        default: imm_o = 32'd0;
        endcase
    end
endmodule
