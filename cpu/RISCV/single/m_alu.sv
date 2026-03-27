// Choose 1 of 10 operations and execute it
// SUB is executed for branch instructions. If the result is 0, zero_o is set.

module m_alu #(parameter int XLEN=32)
(
    input  logic    [XLEN-1:0] a_i, b_i,
    input  alu_op_e            alu_op_i,
    
    output logic    [XLEN-1:0] alu_result_o,
);
    always_comb begin

        alu_result_o = {XLEN{1'b0}};

        unique case(alu_op_i) 
            ALU_ADD:  alu_result_o = a_i + b_i;
            ALU_SUB:  alu_result_o = a_i - b_i;

            // shift operations only consider the lower 5 bits of the shift amount for RV32I
            ALU_SLL:  alu_result_o = a_i << b_i[4:0];
            ALU_SRL:  alu_result_o = a_i >> b_i[4:0];
            ALU_SRA:  alu_result_o = $signed(a_i) >>> b_i[4:0];

            // comparison operations. a < b -> 1, otherwise -> 0
            ALU_SLT:  alu_result_o = {{(XLEN-1){1'b0}}, ($signed(a_i) < ($signed(b_i)))};
            ALU_SLTU: alu_result_o = {{(XLEN-1){1'b0}}, (a_i < b_i)};

            // logical operations
            ALU_XOR:  alu_result_o = a_i ^ b_i;
            ALU_OR:   alu_result_o = a_i | b_i;
            ALU_AND:  alu_result_o = a_i & b_i;

            default:  alu_result_o = {XLEN{1'b0}};
        endcase
    end
endmodule
