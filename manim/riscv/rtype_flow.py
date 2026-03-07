from manim import *

class RTypeFlow(Scene):
    def construct(self):
        # --- 1. CPUコンポーネントの定義と配置 ---
        pc = Rectangle(height=1, width=1.5, color=WHITE).shift(LEFT*5)
        pc_text = Text("PC", font_size=24).move_to(pc)

        imem = Rectangle(height=3, width=2, color=GREEN).shift(LEFT*2.5)
        imem_text = Text("Inst\nMem", font_size=24).move_to(imem)

        regfile = Rectangle(height=4, width=2, color=YELLOW).shift(RIGHT*1)
        reg_text = Text("Register\nFile", font_size=24).move_to(regfile)

        # 本格的なV字型ALU
        alu = Polygon(
            UP*1.5 + LEFT*1, UP*0.5 + RIGHT*1, DOWN*0.5 + RIGHT*1,
            DOWN*1.5 + LEFT*1, DOWN*0.5 + LEFT*1, ORIGIN + LEFT*0.5, UP*0.5 + LEFT*1,
            color=RED, fill_opacity=0.2
        ).shift(RIGHT*5)
        alu_text = Text("ALU", font_size=24).move_to(alu)

        # 画面に表示
        self.play(FadeIn(VGroup(pc, pc_text, imem, imem_text, regfile, reg_text, alu, alu_text)))
        self.wait(0.5)

        # --- 2. R-Type (add rd, rs1, rs2) のデータフロー ---
        
        # [Step 1] PC -> Inst Mem
        flow_pc_imem = Arrow(pc.get_right(), imem.get_left(), buff=0.1, color=BLUE)
        lbl_pc = Text("Address", font_size=16, color=BLUE).next_to(flow_pc_imem, UP)
        self.play(GrowArrow(flow_pc_imem), FadeIn(lbl_pc))
        
        # [Step 2] Inst Mem -> Reg File
        flow_imem_reg = Arrow(imem.get_right(), regfile.get_left(), buff=0.1, color=BLUE)
        lbl_inst = Text("Instruction (R-Type)", font_size=16, color=BLUE).next_to(flow_imem_reg, UP)
        self.play(GrowArrow(flow_imem_reg), FadeIn(lbl_inst))
        
        # [Step 3] Reg File -> ALU (rs1 & rs2)
        flow_rs1 = Arrow(regfile.get_right() + UP*1, alu.get_left() + UP*1, buff=0.1, color=ORANGE)
        lbl_rs1 = Text("rs1 data", font_size=16, color=ORANGE).next_to(flow_rs1, UP)
        flow_rs2 = Arrow(regfile.get_right() + DOWN*1, alu.get_left() + DOWN*1, buff=0.1, color=ORANGE)
        lbl_rs2 = Text("rs2 data", font_size=16, color=ORANGE).next_to(flow_rs2, DOWN)
        self.play(GrowArrow(flow_rs1), GrowArrow(flow_rs2), FadeIn(lbl_rs1), FadeIn(lbl_rs2))
        
        # [Step 4] ALU -> Reg File (Write Back)
        wb_path = CurvedArrow(alu.get_right(), regfile.get_top(), angle=-PI/2, color=PINK)
        lbl_wb = Text("rd data (Write Back)", font_size=16, color=PINK).next_to(wb_path, UP)
        self.play(Create(wb_path), FadeIn(lbl_wb))
        
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))