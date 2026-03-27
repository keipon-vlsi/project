module m_branch_control #(parameter XLEN=32)
(
    input  logic            branch_i,
    input  logic [2:0]      funct3_i,

    input  logic [XLEN-1:0] rs1_data_i,
    input  logic [XLEN-1:0] rs2_data_i

    output logic [XLEN-1:0] pc_src_o
);

    logic branch_taken;

    always_comb begin
        branch_taken = 1'b0;

        case (funct3_i)
            // beq
            3'b000: branch_taken = (rs1_data_i == rs2_data_i);
            // bne
            3'b001: branch_taken = (rs1_data_i != rs2_data_i);
            // blt
            3'b100: branch_taken = ($signed(rs1_data_i) < $signed(rs2_data_i));
            // bge
            3'b101: branch_taken = ($signed(rs1_data_i) >= $signed(rs2_data_i));
            // bltu
            3'b110: branch_taken = (rs1_data_i < rs2_data_i);
            //bgeu
            3'b111: branch_taken = (rs1_data_i >= rs2_data_i);

            default: branch_taken = 1'b0;
        endcase
    end

    // execute branch when the instruction type is B-type & the branch is taken
    assign pc_src_o = branch_i && branch_taken;
    
endmodule