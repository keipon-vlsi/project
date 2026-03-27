from manim import *

class RISCVDataPath(Scene):
    def construct(self):
        # --- 1. 要素の定義 ---
        
        # PC
        pc_box = Rectangle(width=1.5, height=0.8, color=GREEN, fill_opacity=0.8)
        pc_text = Text("PC", font_size=24, color=WHITE).move_to(pc_box)
        pc = VGroup(pc_box, pc_text)

        # PC Adder (+)
        pc_adder = Polygon(
            [-0.8, 0.4, 0], [0.8, 0.4, 0], [0.5, -0.4, 0], [-0.5, -0.4, 0],
            color=RED, fill_opacity=0.8
        )
        pc_adder_text = Text("+", font_size=36, color=WHITE).move_to(pc_adder)
        adder = VGroup(pc_adder, pc_adder_text)

        # Instruction Memory
        imem_box = Rectangle(width=2, height=3, color=GREEN, fill_opacity=0.8)
        imem_text = Text("IMEM", font_size=24, color=WHITE).move_to(imem_box)
        imem = VGroup(imem_box, imem_text)

        # Control Unit
        cu_box = Rectangle(width=1.5, height=2.5, color=BLUE, fill_opacity=0.8)
        cu_text = Text("CU", font_size=24, color=WHITE).move_to(cu_box)
        cu = VGroup(cu_box, cu_text)

        # Register File
        reg_box = Rectangle(width=2, height=3, color=GREEN, fill_opacity=0.8)
        reg_text = Text("Reg", font_size=24, color=WHITE).move_to(reg_box)
        regfile = VGroup(reg_box, reg_text)

        # Imm Sign Extend
        ise_ellipse = Ellipse(width=2, height=1.5, color=BLUE, fill_opacity=0.8)
        ise_text = Text("ISE", font_size=24, color=WHITE).move_to(ise_ellipse)
        ise = VGroup(ise_ellipse, ise_text)

        # MUX作成関数
        def create_mux(label):
            mux_poly = Polygon(
                [-0.4, 0.8, 0], [0.4, 0.5, 0], [0.4, -0.5, 0], [-0.4, -0.8, 0],
                color="#8C5A3C", fill_opacity=0.9  # 茶色系
            )
            mux_text = Text(label, font_size=18, color=WHITE).rotate(PI/2).move_to(mux_poly)
            return VGroup(mux_poly, mux_text)

        mux_port_a = create_mux("MUX")
        mux_port_b = create_mux("MUX")
        mux_pc = create_mux("PC MUX")
        mux_rd = create_mux("RD MUX")

        # ALU
        alu_poly = Polygon(
            [-0.8, 1.5, 0], [-0.8, 0.2, 0], [-0.4, 0, 0], [-0.8, -0.2, 0], [-0.8, -1.5, 0],
            [0.8, -0.5, 0], [0.8, 0.5, 0],
            color=RED, fill_opacity=0.8
        )
        alu_text = Text("ALU", font_size=24, color=WHITE).move_to(alu_poly)
        alu = VGroup(alu_poly, alu_text)

        # Comparator Unit (BCU)
        bcu_poly = Polygon( 
             [-0.6, 1.0, 0], [-0.6, -1.0, 0], [0.6, -0.5, 0], [0.6, 0.5, 0],
            color=RED, fill_opacity=0.8
        )
        bcu_text = Text("BCU", font_size=20, color=WHITE).move_to(bcu_poly)
        bcu = VGroup(bcu_poly, bcu_text)
        
        # Load/Store Unit
        lsu_box = Rectangle(width=1.8, height=1.5, color=YELLOW, fill_opacity=0.8)
        lsu_text = Text("LSU", font_size=24, color=BLACK).move_to(lsu_box)
        lsu = VGroup(lsu_box, lsu_text)

        # Data Memory
        dmem_box = Rectangle(width=2, height=2.5, color=GREEN, fill_opacity=0.8)
        dmem_text = Text("DMEM", font_size=24, color=WHITE).move_to(dmem_box)
        dmem = VGroup(dmem_box, dmem_text)


        # --- 2. 配置 (画像に基づく相対配置) ---
        
        imem.move_to(LEFT * 4 + UP * 0.5)
        
        pc.next_to(imem, LEFT, buff=1.5).shift(UP * 1.5)
        adder.next_to(pc, DOWN, buff=1.0)
        mux_pc.next_to(adder, DOWN, buff=1.0).align_to(pc, LEFT)

        regfile.next_to(imem, RIGHT, buff=1.5).align_to(imem, DOWN)
        cu.next_to(regfile, UP, buff=0.8)
        ise.next_to(regfile, DOWN, buff=0.8)

        mux_port_a.next_to(regfile, RIGHT, buff=1.0).shift(UP * 0.5)
        mux_port_b.next_to(regfile, RIGHT, buff=1.0).shift(DOWN * 1.5)

        alu.next_to(mux_port_b, RIGHT, buff=1.0).align_to(mux_port_b, DOWN)
        # 【修正】BCUを上にシフトしてALUとの被りをなくす
        bcu.next_to(mux_port_a, RIGHT, buff=1.2).align_to(mux_port_a, UP).shift(UP * 1.0)

        dmem.next_to(alu, RIGHT, buff=2.0).shift(UP * 1.5)
        lsu.next_to(dmem, DOWN, buff=0.5)
        
        mux_rd.next_to(lsu, DOWN, buff=0.5).shift(RIGHT * 1.0)


        # 【修正】全体をグループ化して画面サイズに確実に収まるようスケールダウン
        all_elements = VGroup(
            pc, adder, imem, cu, regfile, ise, 
            mux_port_a, mux_port_b, mux_pc, mux_rd, 
            alu, bcu, dmem, lsu
        )
        all_elements.scale(0.65).move_to(ORIGIN)


        # --- 3. アニメーション: シーン1 (要素の出現) ---
        self.play(FadeIn(all_elements), run_time=1.5)
        self.wait(0.5)

        # --- 4. 矢印とテキストの生成関数 ---
        def add_path(start_obj, end_obj, text, path_color=WHITE, text_color=YELLOW, offset=ORIGIN, direction=UP):
            # Arrowを使ってエラーを回避
            arrow = Arrow(start_obj.get_center(), end_obj.get_center(), buff=0.5)
            arrow.set_color(path_color)
            
            # 【修正】文字色を黄色にし、黒い半透明の背景をつけて線との被りを回避
            label = Text(text, font_size=18, color=text_color)
            label.add_background_rectangle(color=BLACK, opacity=0.8)
            label.next_to(arrow.get_center(), direction, buff=0.0).shift(offset)
            
            return arrow, label

        # 主要なデータパスの定義
        path_pc_imem, text_pc_imem = add_path(pc, imem, "PC [31:0]", direction=UP)
        path_imem_reg, text_imem_reg = add_path(imem, regfile, "instruction [31:0]", direction=UP)
        path_reg_alu_a, text_reg_alu_a = add_path(regfile, mux_port_a, "RS1", direction=UP)
        path_reg_alu_b, text_reg_alu_b = add_path(regfile, mux_port_b, "RS2", direction=DOWN)
        path_ise_mux, text_ise_mux = add_path(ise, mux_port_b, "IMM", direction=DOWN, offset=DOWN*0.3)
        
        # MUXからALUへの入力（直接配置で微調整）
        arrow_muxA_alu = Arrow(mux_port_a.get_right(), alu.get_left() + UP*0.5, buff=0.1)
        arrow_muxB_alu = Arrow(mux_port_b.get_right(), alu.get_left() + DOWN*0.5, buff=0.1)

        path_alu_dmem, text_alu_dmem = add_path(alu, dmem, "alu_output", direction=UP)
        
        # 制御信号の例 (CU -> ALU) / CurvedArrowを使用
        path_cu_alu = CurvedArrow(cu.get_right(), alu.get_top(), angle=-PI/4)
        path_cu_alu.set_color(BLUE)
        text_cu_alu = Text("alu_op_sel", font_size=18, color=BLUE)
        text_cu_alu.add_background_rectangle(color=BLACK, opacity=0.8)
        text_cu_alu.next_to(path_cu_alu, UP, buff=0.0)


        # --- 5. アニメーション: シーン2 (パスの描画) ---
        # 【修正】GrowArrowによるエラーを避けるため全てCreateに変更
        
        # PC -> IMEM
        self.play(Create(path_pc_imem), FadeIn(text_pc_imem))
        
        # IMEM -> RegFile, CU, ISE
        self.play(Create(path_imem_reg), FadeIn(text_imem_reg))
        
        # Decode & Read Registers
        self.play(
            Create(path_reg_alu_a), FadeIn(text_reg_alu_a),
            Create(path_reg_alu_b), FadeIn(text_reg_alu_b),
            Create(path_ise_mux), FadeIn(text_ise_mux)
        )
        
        # Execute (MUX -> ALU, and Control Signal)
        self.play(
            Create(arrow_muxA_alu),
            Create(arrow_muxB_alu),
            Create(path_cu_alu), FadeIn(text_cu_alu)
        )
        
        # ALU -> Memory/WriteBack
        self.play(Create(path_alu_dmem), FadeIn(text_alu_dmem))

        self.wait(2)