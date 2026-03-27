module m_adder #(parameter int XLEN=32)
(
    input  logic [XLEN-1:0] a_i, b_i,
    output logic [XLEN-1:0] sum_o
);

    assign sum_o = a_i + b_i;

endmodule