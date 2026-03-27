module m_alu_control (
    input  alu_op_main_e alu_op_i;   // From main_control. Roughly classify instructions.
    input  logic [2:0]   funct3_i;   // instruction[14:12]. More detailed classification within R-type and I-type.
    input  logic         funct7_5_i, // instruction[30]. Choose ADD or SUB, SRA or SRL.
    input  logic         opcode_5_i, // instruction[5]. Is R-type or I-type?
    
    output alu_op_e      alu_control_o
);
    always_comb begin
        alu_op_o = ALU_ADD;

        case (alu_op_i)
            // Load/Store, ADD to calculate address
            ALU_LOAD_STORE: alu_op_o = ALU_ADD;

            // Branch, SUB to compare
            ALU_BRANCH: alu_op_o = ALU_SUB;

            // R-type or I-type. Need to decode funct3 and instruction[30]
            ALU_R_I: begin
                case (funct3_i)
                    3'b000: begin
                        if (funct7_5_i == 1'b1 && opcode5_i ==1'b1) begin
                            alu_op_o = ALU_SUB;
                        end
                        else begin
                            alu_op_o = ALU_ADD;
                        end
                    end
                    3'b001: alu_control_o = ALU_SLL;
                    3'b010: alu_control_o = ALU_SLT;
                    3'b011: alu_control_o = ALU_SLTU;
                    3'b100: alu_control_o = ALU_XOR;
                    3'b101: begin
                        // SRL or SRA
                        if (funct7_5_i == 1'b1) begin
                            alu_control_o = ALU_SRA;
                        end
                        else begin
                            alu_control_o = ALU_SRL;
                        end
                    end
                    3'b110: alu_control = ALU_OR;
                    3'b111: alu_control = ALU_AND;
                endcase
            end

            default: alu_control_o = ALU_ADD;
        endcase
    end
endmodule
