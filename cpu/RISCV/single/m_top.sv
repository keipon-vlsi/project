module m_top #(parameter int XLEN=32)
(
    input  logic clk_i,
    input  logic reset_i,

)
    // IF (Instruction Fetch)
    logic  [XLEN-1:0] pc, next_pc, pc_plus_4, pc_branch;
    logic  [31:0] instruction;

    // ID (Instruction Decode)
    logic  [XLEN-1:0] rs1_data, rs2_datqa, imm;
    logic  alu_src, mem_to_reg, reg_write, mem_read, mem_write, branch;
    alu_op_main_e alu_op_main;
    alu_op_e alu_control;

    // EX (Execute)
    logic [XLEN-1:0] alu_b, alu_result;
    logic [31:0] pc_src_ctrl;

    // MEM (Memory Access)
    logic [31:0] mem_read_data, load_data, mem_write_data;
    logic [3:0] byte_enable;

    // WB (Write Back)
    logic [XLEN-1:0] write_back_data;

endmodule
