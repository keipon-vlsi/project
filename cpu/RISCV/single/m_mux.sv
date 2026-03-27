module m_mux #(parameter int WIDTH = 32)
(
    input  logic [WIDTH-1:0] a_i, b_i,
    input  logic             sel_i,
    output logic [WIDTH-1:0] data_o
);

    assign data_o = sel_i ? b_i : a_i;

endmodule