from manim import *

class RTypeFlow(Scene):
    def construct(self):
        # 背景を黒い矩形で塗りつぶす（透過による市松模様を防ぐため）
        self.add(Rectangle(width=config.frame_width, height=config.frame_height, color=BLACK, fill_opacity=1))
        # --- 1. CPUコンポーネントの定義と配置 ---
        # 配置座標の調整（重なり防止のため間隔を広げる）
        pc = Rectangle(height=1, width=1.5, color=WHITE).shift(LEFT*6)
        pc_text = Text("PC", font_size=24).move_to(pc)

        imem = Rectangle(height=3, width=2, color=GREEN).shift(LEFT*2.5)
        imem_text = Text("Inst\nMem", font_size=24).move_to(imem)

        regfile = Rectangle(height=4, width=2.5, color=YELLOW).shift(RIGHT*1.5)
        reg_text = Text("Register\nFile", font_size=24).move_to(regfile)

        # 本格的なV字型ALU
        alu = Polygon(
            UP*1.5 + LEFT*1, UP*0.5 + RIGHT*1, DOWN*0.5 + RIGHT*1,
            DOWN*1.5 + LEFT*1, DOWN*0.5 + LEFT*1, ORIGIN + LEFT*0.5, UP*0.5 + LEFT*1,
            color=BLUE, fill_opacity=0.2
        ).shift(RIGHT*6)
        alu_text = Text("ALU", font_size=24).move_to(alu).shift(RIGHT*0.2)

        # --- ポートの追加 ---
        def get_port(mobj, direction, offset=ORIGIN, color=WHITE):
            return Dot(radius=0.08, color=color).move_to(mobj.get_edge_center(direction) + offset)

        pc_port_out = get_port(pc, RIGHT)
        imem_port_in = get_port(imem, LEFT)
        imem_port_out = get_port(imem, RIGHT)
        
        rf_port_in = get_port(regfile, LEFT)
        rf_port_out1 = get_port(regfile, RIGHT, offset=UP*1, color=ORANGE)
        rf_port_out2 = get_port(regfile, RIGHT, offset=DOWN*1, color=ORANGE)
        rf_port_wd = get_port(regfile, UP, color=PINK)

        alu_port_in1 = get_port(alu, LEFT, offset=UP*1, color=ORANGE)
        alu_port_in2 = get_port(alu, LEFT, offset=DOWN*1, color=ORANGE)
        alu_port_out = get_port(alu, RIGHT, color=BLUE)

        ports = VGroup(
            pc_port_out, imem_port_in, imem_port_out, 
            rf_port_in, rf_port_out1, rf_port_out2, rf_port_wd,
            alu_port_in1, alu_port_in2, alu_port_out
        )

        # 画面に表示
        self.play(FadeIn(VGroup(pc, pc_text, imem, imem_text, regfile, reg_text, alu, alu_text, ports)))
        self.wait(0.5)

        # --- ヘルパー関数: バス幅ラベル ---
        def get_bus_label(arrow, text, font_size=14):
            slash = Line(DOWN*0.15, UP*0.15, stroke_width=2).rotate(PI/4).move_to(arrow.get_center())
            label = Text(text, font_size=font_size).next_to(slash, UP, buff=0.05)
            return VGroup(slash, label)

        # --- 2. R-Type (add rd, rs1, rs2) のデータフロー ---
        
        # [Step 1] PC -> Inst Mem
        flow_pc_imem = Arrow(pc_port_out.get_center(), imem_port_in.get_center(), buff=0, color=BLUE)
        lbl_pc = Text("Address", font_size=16, color=BLUE).next_to(flow_pc_imem, UP)
        bus_pc = get_bus_label(flow_pc_imem, "32")
        self.play(GrowArrow(flow_pc_imem), FadeIn(lbl_pc), FadeIn(bus_pc))
        
        # [Step 2] Inst Mem -> Reg File
        flow_imem_reg = Arrow(imem_port_out.get_center(), rf_port_in.get_center(), buff=0, color=BLUE)
        lbl_inst = Text("Instruction", font_size=16, color=BLUE).next_to(flow_imem_reg, UP)
        bus_inst = get_bus_label(flow_imem_reg, "32")
        self.play(GrowArrow(flow_imem_reg), FadeIn(lbl_inst), FadeIn(bus_inst))
        
        # [Step 3] Reg File -> ALU (rs1 & rs2)
        flow_rs1 = Arrow(rf_port_out1.get_center(), alu_port_in1.get_center(), buff=0, color=ORANGE)
        lbl_rs1 = Text("rs1 data", font_size=16, color=ORANGE).next_to(flow_rs1, UP)
        bus_rs1 = get_bus_label(flow_rs1, "32")

        flow_rs2 = Arrow(rf_port_out2.get_center(), alu_port_in2.get_center(), buff=0, color=ORANGE)
        lbl_rs2 = Text("rs2 data", font_size=16, color=ORANGE).next_to(flow_rs2, DOWN)
        bus_rs2 = get_bus_label(flow_rs2, "32")

        self.play(
            GrowArrow(flow_rs1), GrowArrow(flow_rs2), 
            FadeIn(lbl_rs1), FadeIn(lbl_rs2),
            FadeIn(bus_rs1), FadeIn(bus_rs2)
        )
        
        # [Step 4] ALU -> Reg File (Write Back)
        # 直角に曲がるパス
        p0 = alu_port_out.get_center()
        p1 = p0 + RIGHT * 0.5
        p2 = p1 + UP * 2.5
        p3 = rf_port_wd.get_center() + UP * 0.5
        p4 = rf_port_wd.get_center()
        
        # VMobject.add_tip() が使えないため、LineとArrowで構成
        wb_path = VGroup(
            Line(p0, p1, color=PINK),
            Line(p1, p2, color=PINK),
            Line(p2, p3, color=PINK),
            Arrow(p3, p4, color=PINK, buff=0)
        )
        lbl_wb = Text("rd data (Write Back)", font_size=16, color=PINK).next_to(wb_path[2], UP, buff=0.1)
        
        wb_slash = Line(DOWN*0.15, UP*0.15, stroke_width=2).rotate(PI/4).move_to(wb_path[2].get_center())
        wb_bus_text = Text("32", font_size=14).next_to(wb_slash, UP, buff=0.05)
        bus_wb = VGroup(wb_slash, wb_bus_text)

        self.play(Create(wb_path), FadeIn(lbl_wb), FadeIn(bus_wb))
        
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))