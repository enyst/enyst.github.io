"""Video: agent reactions in OpenHands (software-agent-sdk #6609, OpenHands #19503).

Render (after `python narration.py` wrote voice/durations.json):
    manim -t -r 1920,1080 --fps 30 reactions.py Reactions
`-t` renders with a transparent background: compose.py lays the screen
recordings under this layer, so the frames and highlights sit on top of them.
"""

import json

from manim import *

from narration import SCENES
from plan import CLIP_SCALE, CLIP_X, CLIP_Y, DUR, ORDER, moments, px, scene_len, timeline

BG = "#111318"
SERIF = "Liberation Serif"
SANS = "Inter"
MONO = "DejaVu Sans Mono"
BLUE_3B = "#58C4DD"
YELLOW_3B = "#FFD84D"
GREEN_3B = "#83C167"
RED_3B = "#FC6255"
GREY_3B = "#8A8F98"
CARD_BG = "#181B22"
CARD_EDGE = "#2A2F3A"
PAPER = "#EFEAE0"

THUMB = "emoji/1f44d.svg"
HEART = "emoji/2764.svg"
EYES = "emoji/1f440.svg"


def emoji(path, h=0.6):
    return SVGMobject(path).set(height=h)


def label(s, size=26, color=GREY_3B, font=SANS, **kw):
    return Text(s, font=font, font_size=size, color=color, **kw)


def bubble(text, width_chars, color, fill, size=24, align_right=False):
    import textwrap
    t = Text("\n".join(textwrap.wrap(text, width_chars)), font=SANS, font_size=size,
             color=color, line_spacing=0.85)
    box = RoundedRectangle(corner_radius=0.22, width=t.width + 0.6, height=t.height + 0.5,
                           fill_color=fill, fill_opacity=1, stroke_width=0)
    t.move_to(box)
    return VGroup(box, t)


class Reactions(Scene):
    def setup(self):
        self.times = []
        self.marks = {}

    def begin(self, name):
        self.scene_name = name
        self.scene_t0 = dict(timeline())[name]  # planned start, so frame rounding never drifts
        self.times.append((name, round(self.renderer.time, 2)))

    def until(self, t):
        """Wait until t seconds into the current scene."""
        left = self.scene_t0 + t - self.renderer.time
        if left > 0.01:
            self.wait(left)

    def cue(self, phrase):
        """Seconds into the scene at which the narrator reaches `phrase` (estimate)."""
        text = SCENES[self.scene_name]
        return DUR[self.scene_name] * text.index(phrase) / len(text)

    def finish(self, *fade):
        end = scene_len(self.scene_name)
        self.until(end - 0.45)
        if fade:
            self.play(*[FadeOut(m) for m in fade], run_time=0.4)
        self.until(end)

    # A frame around where compose.py places the recording
    def screen_frame(self):
        w, h = 1600 * CLIP_SCALE / 135, 900 * CLIP_SCALE / 135
        cx = (CLIP_X + 800 * CLIP_SCALE - 960) / 135
        cy = (540 - (CLIP_Y + 450 * CLIP_SCALE)) / 135
        r = Rectangle(width=w + 0.06, height=h + 0.06, stroke_color=CARD_EDGE, stroke_width=3)
        r.move_to([cx, cy, 0])
        return r

    def caption(self, s):
        return label(s, size=22, color=GREY_3B).move_to([0, -3.7, 0])

    def construct(self):
        for name in ORDER:
            self.begin(name)
            getattr(self, "s_" + name)()
        self.times.append(("end", round(self.renderer.time, 2)))
        json.dump(self.times, open("scene_times.json", "w"))
        json.dump({**moments(), **self.marks}, open("marks.json", "w"), indent=1)
        planned = timeline()
        for (a, x), (b, y) in zip(self.times, planned):
            assert a == b and abs(x - y) < 0.1, (a, x, y)

    # ------------------------------------------------------------------ scenes
    def s_hook(self):
        bg = Rectangle(width=16, height=9.2, fill_color=BG, fill_opacity=1, stroke_width=0)
        self.add(bg)
        user = bubble("Wait, actually: not everyone had drinks. Can it take what each person "
                      "ordered, and split only the shared appetizers evenly?", 44,
                      "#1d1a16", PAPER, size=24)
        user.to_edge(RIGHT, buff=0.8).to_edge(UP, buff=0.7)
        you = label("you", 20).next_to(user, UP, buff=0.12, aligned_edge=RIGHT)
        self.play(FadeIn(user, shift=0.3 * LEFT), FadeIn(you), run_time=0.7)

        wall = ("Got it! You'd like me to change the script so that, instead of splitting "
                "the total evenly between everyone, it takes what each person ordered, "
                "because not everyone had drinks, and then splits only the shared "
                "appetizers evenly. So, to restate the new requirements: one, each person "
                "pays for their own items, including drinks; two, the shared appetizers are "
                "divided equally among all diners; three, the totals should still add up to "
                "the full bill. Before I start, let me make sure I understand correctly...")
        import textwrap
        lines = textwrap.wrap(wall, 62)
        agent = VGroup(*[Text(l, font=SANS, font_size=22, color="#C9CDD4") for l in lines])
        agent.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        agent.next_to(user, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        who = label("agent", 20).next_to(agent, UP, buff=0.12, aligned_edge=LEFT)
        nw = ValueTracker(0)
        corner = config.frame_width / 2 - 0.6, -config.frame_height / 2 + 0.6

        def make_counter():
            n = int(round(nw.get_value()))
            m = label(f"{n} word" + ("" if n == 1 else "s"), 26)
            return m.move_to([corner[0] - m.width / 2, corner[1], 0])

        counter = always_redraw(make_counter)
        self.add(who)
        n_words = len(wall.split())
        t_end = self.cue("It means well") - 0.3
        per = (t_end - (self.renderer.time - self.scene_t0)) / len(lines)
        self.add(counter)
        shown = 0
        for i, line in enumerate(agent):
            shown += len(lines[i].split())
            self.play(FadeIn(line, shift=0.08 * UP), nw.animate.set_value(shown),
                      run_time=per, rate_func=linear)
        self.play(agent.animate.set_opacity(0.35), who.animate.set_opacity(0.35), run_time=0.6)

        self.until(self.cue("a thumbs up") - 0.4)
        thumb = emoji(THUMB, 0.42)
        chip = RoundedRectangle(corner_radius=0.22, width=0.78, height=0.5, fill_color="#E4DCCB",
                                fill_opacity=1, stroke_width=0)
        chip.move_to(user.get_corner(DR) + [-0.55, 0.05, 0])
        thumb.move_to(chip)
        self.play(agent.animate.scale(0.02).move_to(chip).set_opacity(0),
                  FadeOut(who), nw.animate.set_value(1), run_time=0.45, rate_func=rush_into)
        self.marks["hook_pop"] = round(self.renderer.time, 2)
        self.play(FadeIn(chip, scale=0.3), GrowFromCenter(thumb), run_time=0.18)
        self.play(thumb.animate.scale(1.35), run_time=0.12, rate_func=there_and_back)
        title = Text("Reactions", font=SERIF, font_size=72, color=WHITE).move_to([0, -1.2, 0])
        sub = label("an experimental feature in OpenHands", 28).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=0.2 * UP), FadeIn(sub), run_time=0.8)
        self.finish(user, you, chip, thumb, title, sub, counter, bg)

    def s_flag(self):
        frame = self.screen_frame()
        cap = self.caption("Command menu  ›  Experimental  ›  Conversation reactions")
        self.play(Create(frame), FadeIn(cap), run_time=0.3)
        sw = moments()["flag_switch"] - self.scene_t0
        self.until(sw - 0.1)
        ring = Circle(radius=0.32, color=YELLOW_3B, stroke_width=5).move_to(px(706, 114))
        self.play(Create(ring), run_time=0.35)
        self.play(ring.animate.set_stroke(opacity=0), run_time=1.2)
        self.finish(frame, cap)

    def s_setup(self):
        bg = Rectangle(width=16, height=9.2, fill_color=BG, fill_opacity=1, stroke_width=0)
        self.add(bg)
        head = label("A real run  ·  Agent Canvas, Paper theme  ·  DeepSeek Flash", 26)
        head.to_edge(UP, buff=0.7)
        md = [
            ("# Team dinner tools", WHITE),
            ("", WHITE),
            ("Small scripts for our team outings.", GREY_3B),
            ("", WHITE),
            ("## Working with me", WHITE),
            ("- Keep answers short. I can read the code.", "#C9CDD4"),
            ("- If I change my mind while you're working,", "#C9CDD4"),
            ("\u00a0\u00a0don't restate what I said: react with a", "#C9CDD4"),
            ("\u00a0\u00a0thumbs up (+1) on my message and carry on.", "#C9CDD4"),
        ]
        rows = VGroup(*[Text(s, font=MONO, font_size=24, color=c) if s else
                       Text("x", font=MONO, font_size=24).set_opacity(0) for s, c in md])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        box = RoundedRectangle(corner_radius=0.14, width=rows.width + 0.9, height=rows.height + 0.8,
                               fill_color=CARD_BG, fill_opacity=1, stroke_color=CARD_EDGE)
        rows.move_to(box)
        fname = label("team-dinner/AGENTS.md", 22, font=MONO).next_to(box, UP, buff=0.15,
                                                                         aligned_edge=LEFT)
        card = VGroup(box, rows, fname).move_to([0, -0.3, 0])
        self.play(FadeIn(head), FadeIn(card, shift=0.2 * UP), run_time=0.8)
        self.until(self.cue("keep answers short") - 0.2)
        hl1 = SurroundingRectangle(rows[5], color=BLUE_3B, buff=0.08, corner_radius=0.06)
        self.play(Create(hl1), run_time=0.5)
        self.until(self.cue("if I change my mind") - 0.2)
        hl2 = SurroundingRectangle(VGroup(rows[6], rows[7], rows[8]), color=YELLOW_3B, buff=0.1,
                                   corner_radius=0.06)
        t = emoji(THUMB, 0.5).next_to(hl2, RIGHT, buff=0.25)
        self.play(ReplacementTransform(hl1, hl2), run_time=0.5)
        self.play(GrowFromCenter(t), run_time=0.3)
        self.finish(head, card, hl2, t, bg)

    def s_ask(self):
        frame = self.screen_frame()
        cap = self.caption("“Can you write a little script that splits our team dinner bill evenly?”")
        self.add(frame)
        self.play(FadeIn(cap), run_time=0.3)
        self.finish(cap)

    def s_thumbs(self):
        frame = self.screen_frame()
        self.add(frame)
        cap = self.caption("“Wait, actually: not everyone had drinks…”")
        self.play(FadeIn(cap), run_time=0.3)
        pop = moments()["thumbs_pop"] - self.scene_t0
        self.until(pop)
        where = px(1283, 287)
        ring = Circle(radius=0.36, color=YELLOW_3B, stroke_width=6).move_to(where)
        big = emoji(THUMB, 0.9).move_to(np.array(where) + [0.95, 0.55, 0])
        cap2 = label("The agent reacts, and keeps working", 22, YELLOW_3B).move_to(cap)
        self.play(GrowFromCenter(ring), GrowFromCenter(big), FadeTransform(cap, cap2), run_time=0.22)
        self.play(big.animate.scale(1.25), run_time=0.14, rate_func=there_and_back)
        self.wait(1.2)
        self.play(FadeOut(big, shift=0.3 * UP), ring.animate.set_stroke(opacity=0), run_time=0.8)
        self.finish(cap2)

    def s_done(self):
        frame = self.screen_frame()
        self.add(frame)
        cap = self.caption("Working  (sped up)")
        self.play(FadeIn(cap), run_time=0.3)
        self.until(2.7)
        cap2 = self.caption("A short answer: the options, one example run, one note")
        self.play(FadeTransform(cap, cap2), run_time=0.3)
        pop = moments()["heart_pop"] - self.scene_t0
        self.until(pop)
        where = px(351, 634)
        ring = Circle(radius=0.34, color=RED_3B, stroke_width=6).move_to(where)
        big = emoji(HEART, 0.8).move_to(np.array(where) + [0.9, 0.5, 0])
        cap3 = label("…and you love it", 22, RED_3B).move_to(cap2)
        self.play(GrowFromCenter(ring), GrowFromCenter(big), FadeTransform(cap2, cap3), run_time=0.22)
        self.play(big.animate.scale(1.25), run_time=0.14, rate_func=there_and_back)
        self.wait(1.0)
        self.play(FadeOut(big, shift=0.3 * UP), ring.animate.set_stroke(opacity=0), run_time=0.8)
        self.finish(cap3, frame)

    def s_restore(self):
        bg = Rectangle(width=16, height=9.2, fill_color=BG, fill_opacity=1, stroke_width=0)
        self.add(bg)
        cmd = Text("$ control-openhands restart", font=MONO, font_size=34, color=WHITE)
        ok = Text("✓ agent server back, same state", font=MONO, font_size=30, color=GREEN_3B)
        VGroup(cmd, ok).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(ORIGIN)
        self.play(AddTextLetterByLetter(cmd), run_time=0.9)
        spin = Arc(radius=0.22, angle=TAU * 0.75, color=BLUE_3B, stroke_width=5).next_to(cmd, RIGHT, buff=0.4)
        self.play(Rotate(spin, -TAU), run_time=0.7, rate_func=linear)
        self.play(FadeOut(spin), FadeIn(ok, shift=0.1 * UP), run_time=0.35)
        self.until(2.45)
        self.remove(bg, cmd, ok)
        frame = self.screen_frame()
        cap = label("Reopened after the restart: both reactions are still there", 22, GREY_3B)
        cap.move_to([0, -3.7, 0])
        self.add(frame)
        self.play(FadeIn(cap), run_time=0.3)
        # once the conversation is open (about 2.3 s into the recording)
        self.until(2.6 + 2.6)
        r1 = Circle(radius=0.34, color=YELLOW_3B, stroke_width=5).move_to(px(1283, 287))
        r2 = Circle(radius=0.34, color=RED_3B, stroke_width=5).move_to(px(600, 609))
        self.play(Create(r1), run_time=0.4)
        self.play(Create(r2), run_time=0.4)
        self.wait(1.4)
        self.play(r1.animate.set_stroke(opacity=0), r2.animate.set_stroke(opacity=0), run_time=0.6)
        self.finish(frame, cap)

    def s_closing(self):
        bg = Rectangle(width=16, height=9.2, fill_color=BG, fill_opacity=1, stroke_width=0)
        self.add(bg)
        a = Text("React,", font=SERIF, font_size=80, color=WHITE)
        b = Text("then do the thing.", font=SERIF, font_size=80, color=WHITE)
        line = VGroup(a, b).arrange(RIGHT, buff=0.35).move_to([0, 1.2, 0])
        self.play(FadeIn(a, shift=0.2 * UP), run_time=0.6)
        self.play(FadeIn(b, shift=0.2 * UP), run_time=0.6)
        self.until(self.cue("Fewer words") - 0.1)
        sub = label("Fewer words, same understanding.", 34, "#C9CDD4").next_to(line, DOWN, buff=0.45)
        self.play(FadeIn(sub), run_time=0.6)
        row = VGroup(emoji(EYES, 0.6), emoji(THUMB, 0.6), emoji(HEART, 0.6)).arrange(RIGHT, buff=0.6)
        row.next_to(sub, DOWN, buff=0.7)
        self.play(LaggedStart(*[GrowFromCenter(e) for e in row], lag_ratio=0.3), run_time=0.9)
        self.until(self.cue("open source") - 0.2)
        src = label("Open source:  software-agent-sdk #6609  ·  OpenHands #19503", 24).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(src), run_time=0.6)
        self.finish(line, sub, row, src, bg)
