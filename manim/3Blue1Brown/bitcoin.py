from manim import *

class DigitalSignature(Scene):
    def construct(self):
        # 1. 右上の数式テキスト
        sign_text = MathTex(r"\text{Sign}(\text{Message}, ", "sk", r") = ", r"\text{Signature}")
        sign_text.set_color_by_tex("sk", RED)
        sign_text.set_color_by_tex("Signature", BLUE)
        
        verify_text = MathTex(r"\text{Verify}(\text{Message}, ", r"\text{Signature}", r", ", "pk", r") = \text{T/F}")
        verify_text.set_color_by_tex("Signature", BLUE)
        verify_text.set_color_by_tex("pk", GREEN)
        
        formulas = VGroup(sign_text, verify_text).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        formulas.to_corner(UR)

        # 2. キャラクター（Pi Creatureの代用として円を使用）と名前
        # 実際にSVGを使う場合は SVGMobject("pi_creature.svg") のように読み込みます
        alice_char = VGroup(Circle(radius=0.4, color="#58C4DD", fill_opacity=1), Text("Alice", font_size=24)).arrange(DOWN)
        bob_char = VGroup(Circle(radius=0.4, color="#9A7272", fill_opacity=1), Text("Bob", font_size=24)).arrange(DOWN)
        charlie_char = VGroup(Circle(radius=0.4, color="#8C7961", fill_opacity=1), Text("Charlie", font_size=24)).arrange(DOWN)
        
        characters = VGroup(alice_char, bob_char, charlie_char).arrange(RIGHT, buff=2).to_edge(DOWN)

        # 3. 鍵情報の生成関数
        def create_key_info(pk_str, sk_str):
            pk_text = Tex("pk: ", pk_str, font_size=32)
            pk_text[0].set_color(GREEN)
            sk_text = Tex("sk: ", sk_str, font_size=32)
            sk_text[0].set_color(RED)
            
            # 秘密鍵を赤い枠で囲む
            sk_box = SurroundingRectangle(sk_text, color=RED, buff=0.1, stroke_width=2)
            sk_group = VGroup(sk_text, sk_box)
            
            # 公開鍵と秘密鍵を縦に並べる
            group = VGroup(pk_text, sk_group).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            return group

        # 各キャラクターの鍵情報を作成して配置
        alice_keys = create_key_info("01000001...", "10010110...")
        bob_keys = create_key_info("01000010...", "10010001...")
        charlie_keys = create_key_info("01000011...", "11011100...")

        alice_keys.next_to(alice_char, UP, buff=0.5)
        bob_keys.next_to(bob_char, UP, buff=0.5)
        charlie_keys.next_to(charlie_char, UP, buff=0.5)

        # Aliceの鍵全体を黄色い枠で囲む
        alice_box = SurroundingRectangle(alice_keys, color=YELLOW, buff=0.2)
        alice_keys_group = VGroup(alice_keys, alice_box)

        # 4. ドキュメント（書類）の生成関数
        def create_document(sig_str):
            doc = Rectangle(height=2.5, width=2, color=WHITE, stroke_width=2)
            # 書類の中の線（文章を表現）
            lines = VGroup(*[Line(LEFT*0.8, RIGHT*0.8, stroke_width=2) for _ in range(4)]).arrange(DOWN, buff=0.2)
            lines.move_to(doc.get_top() + DOWN*0.6)
            short_line = Line(LEFT*0.8, LEFT*0.2, stroke_width=2).next_to(lines, DOWN, buff=0.2, aligned_edge=LEFT)
            
            # 署名欄
            sig_line = Line(LEFT*0.8, RIGHT*0.8, stroke_width=1).move_to(doc.get_bottom() + UP*0.4)
            sig_text = Text(f"x {sig_str}", color="#58C4DD", font_size=16).next_to(sig_line, UP, buff=0.05, aligned_edge=LEFT)
            
            return VGroup(doc, lines, short_line, sig_line, sig_text)

        doc1 = create_document("00110001...")
        doc2 = create_document("10110000...")
        
        docs = VGroup(doc1, doc2).arrange(RIGHT, buff=0.5).to_corner(UL)

        # 5. Aliceの鍵から書類への矢印
        arrow1 = Arrow(alice_box.get_top(), doc1.get_bottom(), buff=0.1, color=WHITE)
        arrow2 = Arrow(alice_box.get_top(), doc2.get_bottom(), buff=0.1, color=WHITE)

        # --- アニメーションの実行 ---
        self.play(Write(formulas), run_time=2)
        self.play(FadeIn(characters, shift=UP))
        self.play(Write(alice_keys), Write(bob_keys), Write(charlie_keys))
        self.play(Create(alice_box))
        self.play(FadeIn(docs, shift=DOWN))
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(2)