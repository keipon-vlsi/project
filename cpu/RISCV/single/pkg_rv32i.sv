package pkg_rv32i;

localparameter int XLEN = 32;
localparameter int INST_WIDTH = 32;
localparameter int REG_ADDR_WIDTH = 5;

typedef enum logic [6:0] {
    OPCODE_LOAD   = 7'b0000011,
    OPCODE_STORE  = 7'b0100011,
    OPCODE_BRANCH = 7'b1100011,
    OPCODE_JALR   = 7'b1100111,
    OPCODE_JAL    = 7'b1101111,
    OPCODE_OP_IMM = 7'b0010011,
    OPCODE_OP     = 7'b0110011,
    OPCODE_LUI    = 7'b0110111,
    OPCODE_AUIPC  = 7'b0010111,
    OPCODE_SYSTEM = 7'b1110011
} opcode_e;

typedef enum logic [1:0] {
    ALU_LOAD_STORE = 2'b00,
    ALU_BRANCH     = 2'b01,
    ALU_R_I        = 2'b10
} alu_op_main_e;

typedef enum logic [3:0] {
    ALU_ADD,
    ALU_SUB,
    ALU_SLL,
    ALU_SRL,
    ALU_SRA,
    ALU_SLT,
    ALU_SLTU,
    ALU_XOR,
    ALU_OR,
    ALU_AND
} alu_op_e;

typedef enum logic [2:0] {
    IMM_I_TYPE,
    IMM_S_TYPE,
    IMM_B_TYPE,
    IMM_U_TYPE,
    IMM_J_TYPE,
    IMM_UNKNOWN_TYPE
} imm_type_e;

typedef enum logic [2:0] {
    BR_BEQ,
    BR_BNE,
    BR_BLT,
    BR_BGE,
    BR_BLTU,
    BR_BGEU,
    BR_NONE
} branch_type_e;

typedef enum logic [1:0] {
    WB_ALU,
    WB_MEM,
    WB_PC4,
    WB_IMM
} wb_sel_e;

endpackage
