"""Video: Self-Healing, the safety net under a self-improving codebase.

Render (after `python narration.py` has written voice/durations.json):
    manim -r 1920,1080 --fps 30 self_healing.py SelfHealing
Then `python music.py` and `python mix.py media/videos/self_healing/1080p30/SelfHealing.mp4`.

Each scene lasts as long as its narration; `self.cue(phrase)` waits until the
narrator reaches that phrase (estimated from its position in the text). The
render writes scene_times.json and beats.json, which the score follows.

The three bugs are real and were found by verify-agent-server's first full
agentic run (OpenHands/software-agent-sdk):
- goal chip stuck on "running" after a restart: issue #5627, fixed by #5772 (merged)
- a failed run froze the server for ~5 s: issue #5633, fixed by #5780 (merged)
- a cipher key change let a settings save erase stored keys: issue #5622, PR #5758 (open)
The probe timings come from the map runs recorded in #5780.
"""

import json
import textwrap

from manim import *

from narration import SCENES

config.background_color = "#111318"

SERIF = "Liberation Serif"
SANS = "Inter"
MONO = "DejaVu Sans Mono"

BLUE_3B = "#58C4DD"
YELLOW_3B = "#FFD84D"
GREEN_3B = "#83C167"
RED_3B = "#FC6255"
GREY_3B = "#8A8F98"
TEAL_3B = "#5CD0B3"
ORANGE_3B = "#F0A35E"
PURPLE_3B = "#B48EF0"
CARD_BG = "#181B22"
CARD_EDGE = "#2A2F3A"
DIM = "#3A3F4B"

DURATIONS = json.load(open("voice/durations.json"))
GAP = 0.9  # silence between scenes
GAPS = {"closing": 1.8}  # a longer breath before the credits line
KEEP = {"closing"}  # scenes whose picture stays up into the next one


def prose(s, size=34, color=WHITE, **kw):
    return Text(s, font=SERIF, font_size=size, color=color, **kw)


def label(s, size=26, color=GREY_3B, **kw):
    return Text(s, font=SANS, font_size=size, color=color, **kw)


def mono(s, size=20, color=WHITE, **kw):
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def wrap(s, width):
    return "\n".join(textwrap.wrap(s, width))


def para(s, width=60, size=22, color=WHITE, font=SANS):
    return Text(wrap(s, width), font=font, font_size=size, color=color, line_spacing=0.9)


def card(content, buff=0.4, edge=CARD_EDGE):
    box = SurroundingRectangle(content, buff=buff, corner_radius=0.14, color=edge,
                               fill_color=CARD_BG, fill_opacity=1, stroke_width=2)
    return VGroup(box, content)


def pill(text, color, size=20):
    t = label(text, size=size, color=color, weight=SEMIBOLD)
    r = RoundedRectangle(width=t.width + 0.45, height=t.height + 0.3, corner_radius=0.2,
                         stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
    return VGroup(r, t.move_to(r))


def window(w, h, title="", color=CARD_EDGE):
    """A browser-like window: frame, title bar, three dots."""
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color,
                             stroke_width=2, fill_color=CARD_BG, fill_opacity=1)
    bar = Line(frame.get_corner(UL) + DOWN * 0.38, frame.get_corner(UR) + DOWN * 0.38,
               stroke_width=1.5, color=color)
    dots = VGroup(*[Dot(radius=0.05, color=c) for c in (RED_3B, YELLOW_3B, GREEN_3B)])
    dots.arrange(RIGHT, buff=0.1).move_to(frame.get_corner(UL) + RIGHT * 0.38 + DOWN * 0.19)
    g = VGroup(frame, bar, dots)
    if title:
        g.add(label(title, size=14).move_to(frame.get_top() + DOWN * 0.19))
    g.frame = frame
    return g


def server_box(text="agent-server", color=BLUE_3B, w=3.0, h=2.0):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color,
                           stroke_width=3, fill_color=color, fill_opacity=0.08)
    t = label(text, size=24, color=color, weight=SEMIBOLD).move_to(box)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def person(color=WHITE):
    head = Circle(radius=0.2, color=color, stroke_width=3)
    body = Arc(radius=0.38, start_angle=PI * 0.15, angle=PI * 0.7, color=color, stroke_width=3)
    body.next_to(head, DOWN, buff=0.05)
    return VGroup(head, body)


def robot(color=TEAL_3B):
    head = RoundedRectangle(width=0.62, height=0.48, corner_radius=0.1, color=color, stroke_width=3)
    eyes = VGroup(Dot(radius=0.05, color=color), Dot(radius=0.05, color=color)).arrange(RIGHT, buff=0.18)
    eyes.move_to(head)
    ant = Line(head.get_top(), head.get_top() + UP * 0.16, color=color, stroke_width=3)
    tip = Dot(ant.get_end(), radius=0.04, color=color)
    return VGroup(head, eyes, ant, tip)


def spinner(radius=0.13, color=YELLOW_3B):
    s = Arc(radius=radius, start_angle=0, angle=PI * 1.4, color=color, stroke_width=3.5)
    s.add_updater(lambda m, dt: m.rotate(-dt * 5))
    return s


def chip(text, color, with_spinner=True):
    t = label(text, size=18, color=color, weight=SEMIBOLD)
    parts = [t]
    if with_spinner:
        parts.insert(0, spinner(color=color))
    else:
        parts.insert(0, Dot(radius=0.07, color=color))
    row = VGroup(*parts).arrange(RIGHT, buff=0.15)
    r = RoundedRectangle(width=row.width + 0.4, height=0.5, corner_radius=0.25,
                         stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
    return VGroup(r, row.move_to(r))


def button(text, color=WHITE, size=17):
    t = label(text, size=size, color=color, weight=MEDIUM)
    r = RoundedRectangle(width=t.width + 0.4, height=0.42, corner_radius=0.08,
                         stroke_color=color, stroke_width=1.6)
    return VGroup(r, t.move_to(r))


def lock(color=BLUE_3B, open_=False):
    body = RoundedRectangle(width=0.36, height=0.28, corner_radius=0.05, color=color,
                            fill_color=color, fill_opacity=0.35, stroke_width=2.5)
    shackle = Arc(radius=0.12, start_angle=0, angle=PI, color=color, stroke_width=2.5)
    shackle.next_to(body, UP, buff=0)
    if open_:
        shackle.shift(UP * 0.08 + RIGHT * 0.1)
    return VGroup(body, shackle)


def key_icon(text, color):
    bow = Circle(radius=0.16, color=color, stroke_width=3)
    shaft = Line(bow.get_right(), bow.get_right() + RIGHT * 0.5, color=color, stroke_width=3)
    teeth = VGroup(
        Line(shaft.get_end(), shaft.get_end() + DOWN * 0.12, color=color, stroke_width=3),
        Line(shaft.get_end() + LEFT * 0.14, shaft.get_end() + LEFT * 0.14 + DOWN * 0.1,
             color=color, stroke_width=3),
    )
    t = label(text, size=18, color=color, weight=SEMIBOLD).next_to(bow, DOWN, buff=0.08)
    return VGroup(bow, shaft, teeth, t)


def toggle(on, color=GREEN_3B):
    track = RoundedRectangle(width=0.7, height=0.36, corner_radius=0.18,
                             stroke_color=color if on else GREY_3B, stroke_width=2,
                             fill_color=color if on else GREY_3B, fill_opacity=0.3)
    knob = Dot(radius=0.13, color=WHITE).move_to(track.get_right() + LEFT * 0.18 if on
                                                  else track.get_left() + RIGHT * 0.18)
    return VGroup(track, knob)


class SelfHealing(Scene):
    # -- timing helpers -----------------------------------------------------
    def cue(self, phrase):
        """Wait until the narrator reaches `phrase` in the current scene."""
        text = SCENES[self.scene_name]
        i = text.find(phrase)
        assert i >= 0, (self.scene_name, phrase)
        at = DURATIONS[self.scene_name] * i / len(text)
        now = self.renderer.time - self.scene_start
        if at > now + 0.05:
            self.wait(at - now)

    def beat(self, kind):
        self.beats.setdefault(kind, []).append(round(self.renderer.time, 2))

    def finish(self):
        now = self.renderer.time - self.scene_start
        rest = DURATIONS[self.scene_name] + GAPS.get(self.scene_name, GAP) - 0.8 - now
        if rest > 0.05:
            self.wait(rest)
        if self.scene_name in KEEP:
            self.wait(0.8)
            return
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        for m in self.mobjects:
            self.remove(m)

    def construct(self):
        marks = []
        self.beats = {}
        for name in SCENES:
            self.scene_name = name
            self.scene_start = self.renderer.time
            marks.append((name, self.scene_start))
            getattr(self, name)()
            self.finish()
        marks.append(("end", self.renderer.time))
        with open("scene_times.json", "w") as f:
            json.dump(marks, f)
        with open("beats.json", "w") as f:
            json.dump(self.beats, f)

    def title(self, s, size=42):
        h = prose(s, size=size, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(h), run_time=1.0)
        return h

    def badge(self, text, color, anchor):
        b = pill(text, color, 18).next_to(anchor, DOWN, buff=0.25)
        self.play(FadeIn(b), run_time=0.5)
        return b

    # 1 -------------------------------------------------------------------
    def opening(self):
        t = prose("Self-Healing", size=84)
        sub = label("a safety net for codebases that improve themselves", size=26)
        g = VGroup(t, sub).arrange(DOWN, buff=0.4)
        self.play(Write(t), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.cue("Agents write code")
        self.play(g.animate.scale(0.5).to_edge(UP, buff=0.5))

        # the factory: three stations, a belt, blocks of code moving along it
        belt = Line(LEFT * 6.2, RIGHT * 6.2, color=GREY_3B, stroke_width=3).shift(DOWN * 0.8)
        rollers = VGroup(*[Circle(radius=0.12, color=GREY_3B, stroke_width=2).move_to(
            belt.point_from_proportion(i / 16) + DOWN * 0.16) for i in range(17)])
        stations = VGroup()
        for x, name in [(-3.8, "write"), (0, "review"), (3.8, "ship")]:
            r = robot().scale(1.2).move_to([x, 1.0, 0])
            stations.add(VGroup(r, label(name, size=20).next_to(r, UP, buff=0.15)))
        self.play(Create(belt), FadeIn(rollers), LaggedStart(*[FadeIn(s, shift=DOWN * 0.2)
                                                                 for s in stations], lag_ratio=0.3),
                  run_time=1.5)
        blocks = VGroup(*[RoundedRectangle(width=0.7, height=0.45, corner_radius=0.06,
                                           stroke_color=BLUE_3B, fill_color=BLUE_3B,
                                           fill_opacity=0.25, stroke_width=2) for _ in range(7)])
        for i, b in enumerate(blocks):
            b.move_to(belt.get_start() + RIGHT * (0.2 - i * 1.6) + UP * 0.25)
        self.add(blocks)
        self.cue("A software factory")
        self.play(blocks.animate.shift(RIGHT * 8.0), run_time=4.0, rate_func=linear)
        self.cue("some things will break")
        bad = blocks[3]
        crack = VGroup(Line(bad.get_corner(UL) + RIGHT * 0.2, bad.get_center(), color=RED_3B, stroke_width=3),
                       Line(bad.get_center(), bad.get_corner(DR) + LEFT * 0.15, color=RED_3B, stroke_width=3))
        self.play(bad.animate.set_stroke(RED_3B).set_fill(RED_3B, 0.3), Create(crack), run_time=0.6)
        self.beat("sour")
        self.play(Wiggle(VGroup(bad, crack)), run_time=0.8)
        self.cue("safety nets")
        self.play(VGroup(blocks, crack).animate.shift(RIGHT * 3).set_opacity(0.3), run_time=1.2)

    # 2 -------------------------------------------------------------------
    def nets(self):
        head = self.title("Three safety nets")
        specs = [
            ("Design review", "by people, when it matters", PURPLE_3B, 1.4, [2, 6, 8]),
            ("Constraints", "linters, types, rules on possible code", BLUE_3B, -0.4, [1, 6]),
            ("Self-healing", "when it breaks anyway", GREEN_3B, -2.3, []),
        ]
        x0, x1, n_seg = -1.0, 6.0, 10
        w = (x1 - x0) / n_seg
        nets = []
        for name, sub, color, y, holes in specs:
            segs = VGroup()
            for k in range(n_seg):
                if k in holes:
                    continue
                p = np.array([x0 + k * w, y, 0])
                segs.add(ArcBetweenPoints(p, p + RIGHT * w, angle=-PI / 5, color=color, stroke_width=3))
            t = label(name, size=26, color=color, weight=SEMIBOLD)
            s = label(sub, size=18)
            txt = VGroup(t, s).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            txt.move_to([-4.2, y, 0]).align_to(np.array([-6.6, 0, 0]), LEFT)
            nets.append((segs, txt, holes, y, color))

        def drop(cols, upto):
            """Bugs fall from the top; each stops on the first net without a hole under it."""
            balls = VGroup(*[Dot(radius=0.12, color=RED_3B).move_to([x0 + (c + 0.5) * w, 3.0, 0]) for c in cols])
            stops = []
            for c in cols:
                j = next(j for j in range(upto + 1) if c not in nets[j][2])
                stops.append(j)
            self.play(LaggedStart(*[b.animate(rate_func=rate_functions.ease_in_quad).set_y(nets[j][3] + 0.16)
                                    for b, j in zip(balls, stops)], lag_ratio=0.25), run_time=1.3)
            for _ in cols:
                self.beat("catch")
            self.play(*[b.animate.set_color(nets[j][4]).scale(0.7) for b, j in zip(balls, stops)], run_time=0.4)

        self.cue("The first is design review")
        self.play(Create(nets[0][0]), FadeIn(nets[0][1], shift=RIGHT * 0.2), run_time=1.0)
        drop([3, 9], 0)
        self.cue("The second is constraints")
        self.play(Create(nets[1][0]), FadeIn(nets[1][1], shift=RIGHT * 0.2), run_time=1.0)
        self.cue("Most mistakes")
        drop([2, 8, 4], 1)
        self.cue("But some slip")
        slip = Dot(radius=0.14, color=RED_3B).move_to([x0 + 6.5 * w, 3.0, 0])
        self.play(FadeIn(slip, scale=0.5), run_time=0.3)
        self.play(slip.animate(rate_func=rate_functions.ease_in_quad).set_y(-1.4), run_time=1.3)
        self.cue("Self-healing is the last net")
        self.play(Create(nets[2][0]), FadeIn(nets[2][1], shift=RIGHT * 0.2), run_time=1.0)
        self.play(slip.animate(rate_func=rate_functions.ease_in_quad).set_y(nets[2][3] + 0.18), run_time=0.6)
        self.beat("catch")
        self.cue("When the code")
        shield = RegularPolygon(6, color=GREEN_3B, stroke_width=3, fill_color=GREEN_3B,
                                fill_opacity=0.25).scale(0.32).move_to(slip)
        g_lab = label("guard", size=14, color=GREEN_3B, weight=SEMIBOLD).next_to(shield, DOWN, buff=0.1)
        self.cue("turns it into a guard")
        self.play(Flash(slip, color=GREEN_3B), ReplacementTransform(slip, shield), run_time=0.8)
        self.beat("fix")
        self.play(FadeIn(g_lab), Indicate(nets[2][0], color=GREEN_3B, scale_factor=1.03), run_time=1.0)

    # 3 -------------------------------------------------------------------
    def door(self):
        head = self.title("Who feels a break")
        ui = window(4.6, 3.0, "Agent Canvas").move_to([-4.0, 0.9, 0])
        p = person().scale(0.8).next_to(ui, LEFT, buff=0.25).shift(DOWN * 0.6)
        msg1 = RoundedRectangle(width=2.6, height=0.4, corner_radius=0.12, stroke_width=0,
                                fill_color=DIM, fill_opacity=1)
        msg2 = RoundedRectangle(width=1.8, height=0.4, corner_radius=0.12, stroke_width=0,
                                fill_color=BLUE_3B, fill_opacity=0.35)
        msg1.move_to(ui.frame.get_left() + RIGHT * 1.6 + UP * 0.45)
        msg2.move_to(ui.frame.get_right() + LEFT * 1.2 + DOWN * 0.15)
        btn = button("Stop goal", YELLOW_3B).move_to(ui.frame.get_bottom() + UP * 0.45)
        srv = server_box(w=3.0, h=2.6).move_to([3.9, 0.0, 0])
        door = Rectangle(width=0.16, height=0.8, stroke_color=YELLOW_3B, stroke_width=2,
                         fill_color=YELLOW_3B, fill_opacity=0.4).move_to(srv.box.get_left())
        self.cue("Someone sits")
        self.play(FadeIn(ui), FadeIn(p, shift=RIGHT * 0.2), run_time=1.0)
        self.play(FadeIn(msg1), FadeIn(msg2), FadeIn(btn), run_time=0.6)
        self.cue("Every button")
        self.play(FadeIn(srv), FadeIn(door), run_time=0.8)
        self.play(Indicate(btn, color=YELLOW_3B), run_time=0.6)
        a1 = Arrow(ui.frame.get_right() + DOWN * 0.3, door.get_left() + UP * 0.15, buff=0.1,
                   color=YELLOW_3B, stroke_width=4)
        req = mono("POST .../goal/stop", size=16, color=YELLOW_3B)
        req.next_to(a1, UP, buff=0.12)
        rest = label("REST", size=20, color=YELLOW_3B, weight=BOLD).next_to(req, UP, buff=0.1)
        self.cue("over REST")
        self.play(GrowArrow(a1), FadeIn(req), FadeIn(rest), run_time=1.0)
        pkt = Dot(radius=0.08, color=YELLOW_3B).move_to(a1.get_start())
        self.play(MoveAlongPath(pkt, Line(a1.get_start(), a1.get_end())), run_time=0.8)
        self.remove(pkt)
        term = card(VGroup(mono("$ control-agent-server", size=17, color=TEAL_3B),
                           mono("  api POST .../goal/stop", size=17, color=TEAL_3B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1), buff=0.25)
        term.move_to([-3.6, -2.4, 0])
        bot = robot().next_to(term, LEFT, buff=0.3)
        self.cue("Agents reach")
        self.play(FadeIn(term, shift=UP * 0.2), FadeIn(bot), run_time=0.8)
        a2 = Arrow(term.get_right(), door.get_left() + DOWN * 0.2, buff=0.1, color=TEAL_3B, stroke_width=4)
        self.play(GrowArrow(a2), run_time=0.8)
        self.cue("Different hands")
        self.play(Indicate(p, color=WHITE), Indicate(bot, color=TEAL_3B), run_time=0.8)
        self.play(Flash(door, color=YELLOW_3B, line_length=0.3), door.animate.set_fill(opacity=0.9))
        self.cue("So when the server breaks")
        self.play(srv.box.animate.set_stroke(RED_3B).set_fill(RED_3B, 0.15),
                  srv.text.animate.set_color(RED_3B), run_time=0.6)
        self.beat("sour")
        self.play(ui.frame.animate.set_stroke(RED_3B, width=3), Wiggle(p), run_time=1.0)

    # 4 -------------------------------------------------------------------
    def promise(self):
        head = self.title("A feature is a promise")
        p1 = prose("“If I stop a goal, it stops.”", size=36)
        p2 = prose("“If I save one setting, my other settings stay.”", size=36)
        ps = VGroup(p1, p2).arrange(DOWN, buff=0.4).shift(UP * 0.8)
        self.cue("If I stop")
        self.play(Write(p1), run_time=1.2)
        self.cue("save one setting")
        self.play(Write(p2), run_time=1.4)

        self.cue("We write each")
        name = mono("F11.goal-stop", size=24, color=BLUE_3B)
        desc = label("stop a running goal; its status becomes interrupted", size=20, color=WHITE)
        line = VGroup(name, desc).arrange(RIGHT, buff=0.5)
        line_c = card(line, buff=0.3).move_to(UP * 0.4)
        self.play(FadeOut(p2), ReplacementTransform(p1, line_c), run_time=1.2)
        self.cue("with a stable name")
        self.play(Circumscribe(name, color=BLUE_3B), run_time=1.0)
        self.cue("and a short recipe")
        steps = VGroup(
            label("1   start a goal", size=22, color=WHITE),
            label("2   stop it", size=22, color=WHITE),
            label("3   check: the last goal status says interrupted", size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(line_c, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in steps], lag_ratio=0.4), run_time=1.8)

        self.cue("Put every promise")
        small = VGroup(line_c, steps)
        self.play(small.animate.scale(0.35).move_to([-5.6, 2.1, 0]).set_opacity(0.0), run_time=0.8)
        self.remove(small)
        cols = VGroup()
        rng = np.random.default_rng(7)
        heights = rng.integers(14, 42, size=34)
        heights = (heights * 931 / heights.sum()).astype(int)
        for k, h in enumerate(heights):
            col = VGroup(*[Line(LEFT * 0.13, RIGHT * 0.13, stroke_width=2.2, color=BLUE_3B)
                           for _ in range(h)]).arrange(DOWN, buff=0.07)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.1, aligned_edge=UP).move_to(DOWN * 0.3)
        cols.scale_to_fit_width(12.6)
        if cols.height > 4.8:
            cols.stretch_to_fit_height(4.8)
        cols.next_to(head, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cols], lag_ratio=0.05), run_time=2.2)
        self.cue("thirty")
        tag = VGroup(label("34 families", size=28, color=WHITE, weight=SEMIBOLD),
                     label("·", size=28), label("900+ promises", size=28, color=WHITE, weight=SEMIBOLD)
                     ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(tag, shift=UP * 0.2))
        self.cols = cols

    # 5 -------------------------------------------------------------------
    def walk(self):
        head = self.title("An agent walks the map")
        rows, colsn = 24, 38
        grid = VGroup(*[Square(0.2, stroke_width=0, fill_color=DIM, fill_opacity=1)
                        for _ in range(rows * colsn)])
        grid.arrange_in_grid(rows=rows, cols=colsn, buff=0.06).next_to(head, DOWN, buff=0.35)
        grid.scale_to_fit_height(min(grid.height, 5.4)).next_to(head, DOWN, buff=0.35)
        bot = robot().scale(0.9).next_to(grid, LEFT, buff=0.3).align_to(grid, UP)
        self.play(FadeIn(grid), FadeIn(bot), run_time=0.8)
        rng = np.random.default_rng(11)
        red_idx = set(rng.choice(rows * colsn, size=40, replace=False).tolist())
        # three of them are the stories that follow
        stories = sorted(list(red_idx))[5], sorted(list(red_idx))[19], sorted(list(red_idx))[33]
        self.cue("A real server")
        anims = []
        for r in range(rows):
            row_anims = []
            for c in range(colsn):
                i = r * colsn + c
                row_anims.append(grid[i].animate.set_fill(RED_3B if i in red_idx else GREEN_3B, 1))
            anims.append(AnimationGroup(*row_anims))
        t0 = self.renderer.time
        for k in range(rows):
            self.beats.setdefault("tick", []).append(round(t0 + k * 0.28, 2))
        self.play(LaggedStart(*anims, lag_ratio=1.0), run_time=rows * 0.28)
        self.cue("Most lines")
        greens = VGroup(*[grid[i] for i in range(rows * colsn) if i not in red_idx])
        self.play(Indicate(greens, color=GREEN_3B, scale_factor=1.0), run_time=0.8)
        self.cue("Some turn red")
        reds = VGroup(*[grid[i] for i in red_idx])
        self.play(greens.animate.set_fill(opacity=0.25), reds.animate.scale(1.25), run_time=0.8)
        self.cue("every red line")
        self.beat("arp")
        self.cue("Here are three")
        picks = VGroup(*[grid[i] for i in stories])
        others = VGroup(*[grid[i] for i in red_idx if i not in stories])
        targets = [LEFT * 3, ORIGIN, RIGHT * 3]
        labels = VGroup(label("the stuck goal", size=22, color=WHITE),
                        label("the frozen windows", size=22, color=WHITE),
                        label("the vanished keys", size=22, color=WHITE))
        self.play(FadeOut(greens), FadeOut(others), FadeOut(bot),
                  *[picks[k].animate.scale(4).move_to(targets[k] + DOWN * 0.3) for k in range(3)],
                  run_time=1.2)
        for k in range(3):
            labels[k].next_to(picks[k], DOWN, buff=0.3)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels], lag_ratio=0.3))

    # 6 -------------------------------------------------------------------
    def goal(self):
        head = self.title("Story 1: the goal that never ends")
        ui = window(6.0, 4.2, "Agent Canvas").move_to([-3.2, -0.6, 0])
        goal_txt = label("Goal: write a story  (up to 3 tries)", size=18, color=WHITE)
        goal_txt.move_to(ui.frame.get_top() + DOWN * 0.85)
        run_chip = chip("Goal · running", YELLOW_3B).next_to(goal_txt, DOWN, buff=0.35)
        stop = button("Stop", RED_3B).move_to(ui.frame.get_corner(DR) + UL * 0.45 + LEFT * 0.2)
        srv = server_box(w=3.6, h=2.4).move_to([4.0, -0.6, 0])
        loop = VGroup(spinner(0.22), label("goal loop", size=16, color=YELLOW_3B)).arrange(RIGHT, buff=0.15)
        loop.next_to(srv.text, DOWN, buff=0.3)
        self.cue("You give")
        self.play(FadeIn(ui), FadeIn(srv), run_time=0.8)
        self.play(FadeIn(goal_txt, shift=UP * 0.1))
        self.cue("The interface shows")
        self.play(FadeIn(run_chip), FadeIn(loop), run_time=0.8)
        self.cue("Now the server restarts")
        restart = label("restarting…", size=22, color=GREY_3B).move_to(srv.box)
        self.play(srv.box.animate.set_stroke(GREY_3B).set_fill(GREY_3B, 0.05),
                  FadeOut(srv.text), FadeOut(loop), FadeIn(restart), run_time=0.8)
        self.wait(0.8)
        self.cue("When it comes back")
        idle = label("nothing running", size=18, color=GREY_3B).next_to(srv.text, DOWN, buff=0.3)
        self.play(FadeOut(restart), srv.box.animate.set_stroke(BLUE_3B).set_fill(BLUE_3B, 0.08),
                  FadeIn(srv.text), FadeIn(idle), run_time=0.8)
        self.cue("But the chip")
        self.play(Circumscribe(run_chip, color=YELLOW_3B), run_time=1.0)
        self.cue("You press stop")
        self.play(FadeIn(stop), run_time=0.3)
        self.play(Indicate(stop, color=RED_3B), run_time=0.6)
        a = Arrow(stop.get_right(), srv.box.get_left() + DOWN * 0.5, buff=0.1, color=RED_3B, stroke_width=3)
        self.play(GrowArrow(a), run_time=0.5)
        self.cue("The server answers")
        ok = pill("200  {\"success\": true}", GREEN_3B, 18).next_to(srv, UP, buff=0.3)
        self.play(FadeIn(ok, shift=DOWN * 0.15), FadeOut(a), run_time=0.6)
        self.beat("sour")
        self.cue("And the chip keeps")
        self.play(run_chip.animate.scale(1.25), run_time=0.8)
        self.play(run_chip.animate.scale(1 / 1.25), run_time=0.8)
        fb = label("#5627  ·  map line F11.goal-restart-active", size=18).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(fb))
        self.goal_ui = (ui, goal_txt, run_chip, stop)

    # 7 -------------------------------------------------------------------
    def goal_fix(self):
        head = self.title("The bug: why the chip kept spinning")
        y = 0.9

        def ev(text, color, dashed=False):
            t = label(text, size=17, color=color, weight=MEDIUM)
            if dashed:
                r = DashedVMobject(RoundedRectangle(width=t.width + 0.35, height=0.6, corner_radius=0.1,
                                                    color=color, stroke_width=2), num_dashes=30)
            else:
                r = RoundedRectangle(width=t.width + 0.35, height=0.6, corner_radius=0.1, stroke_color=color,
                                     stroke_width=2, fill_color=color, fill_opacity=0.12)
            return VGroup(r, t.move_to(r))

        timeline = Arrow(LEFT * 6.6, RIGHT * 6.6, color=GREY_3B, stroke_width=2, buff=0).shift(UP * (y - 0.6))
        tl_lab = label("the conversation's timeline of events", size=18).next_to(timeline, DOWN, buff=0.15).to_edge(LEFT, buff=0.6)
        evs = VGroup(ev("message", WHITE), ev("goal: running", YELLOW_3B), ev("agent: step", WHITE))
        evs.arrange(RIGHT, buff=0.25).move_to([-3.6, y, 0])
        self.cue("The server keeps")
        self.play(GrowArrow(timeline), FadeIn(tl_lab), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in evs], lag_ratio=0.3), run_time=1.2)

        ui_chip = chip("Goal · running", YELLOW_3B).move_to([-3.6, -2.2, 0])
        ui_lab = label("the interface", size=18).next_to(ui_chip, LEFT, buff=0.3)
        self.cue("and the interface draws")
        reads = CurvedArrow(evs[1].get_bottom() + DOWN * 0.05, ui_chip.get_top() + UP * 0.05, angle=0.4,
                            color=YELLOW_3B, stroke_width=3)
        self.play(FadeIn(ui_chip), FadeIn(ui_lab), Create(reads), run_time=1.0)

        self.cue("At shutdown")
        cut = DashedLine([-0.72, y + 0.9, 0], [-0.72, y - 1.0, 0], color=RED_3B, stroke_width=3)
        cut_l = label("shutdown", size=18, color=RED_3B).next_to(cut, UP, buff=0.1)
        self.play(Create(cut), FadeIn(cut_l), run_time=0.7)
        ghost = ev("goal: interrupted", GREY_3B, dashed=True).next_to(evs, RIGHT, buff=0.5)
        self.cue("it skipped")
        self.play(FadeIn(ghost), run_time=0.6)
        skip = label("closing, so skipped", size=16, color=RED_3B).next_to(ghost, UP, buff=0.12)
        self.play(FadeIn(skip), ghost.animate.set_opacity(0.3), run_time=0.6)
        self.cue("interrupted. After")
        self.play(Indicate(ghost, color=GREY_3B), run_time=0.6)

        self.cue("After the restart")
        restart = DashedLine([2.7, y + 0.9, 0], [2.7, y - 1.0, 0], color=BLUE_3B, stroke_width=3)
        restart_l = label("restart", size=18, color=BLUE_3B).next_to(restart, DOWN, buff=0.1)
        self.play(Create(restart), FadeIn(restart_l), run_time=0.7)

        self.cue("The fix is")
        fix = ev("goal: interrupted", GREEN_3B).move_to([4.6, y, 0])
        check = label("on load: last goal says running, no loop behind it", size=16, color=GREEN_3B)
        check.next_to(fix, UP, buff=0.45).align_to(np.array([6.7, 0, 0]), RIGHT)
        self.cue("When a")
        self.play(FadeIn(check), run_time=0.6)
        self.cue("the server writes interrupted")
        self.play(FadeIn(fix, shift=DOWN * 0.2), run_time=0.7)
        self.beat("fix")
        new_reads = CurvedArrow(fix.get_bottom() + DOWN * 0.05, ui_chip.get_right() + RIGHT * 0.05, angle=-0.5,
                                color=GREEN_3B, stroke_width=3)
        self.play(FadeOut(reads), Create(new_reads), run_time=0.8)
        self.cue("The chip now")
        done = chip("Goal · interrupted", GREEN_3B, with_spinner=False).move_to(ui_chip)
        resume = button("Resume", GREEN_3B).next_to(done, RIGHT, buff=0.35)
        self.play(ReplacementTransform(ui_chip, done), FadeIn(resume, shift=LEFT * 0.1), run_time=0.8)
        b = pill("fix #5772  ·  merged", PURPLE_3B, 18).to_corner(DR, buff=0.4)
        self.play(FadeIn(b))

    # 8 -------------------------------------------------------------------
    def proof(self):
        head = self.title("How a break becomes a guard")
        name = mono("F11.goal-restart-active", size=22, color=BLUE_3B)
        marker = mono("# bug: last goal status is still running", size=20, color=RED_3B, weight=BOLD)
        line = card(VGroup(name, marker).arrange(RIGHT, buff=0.5), buff=0.3).next_to(head, DOWN, buff=0.5)
        sch = label("schematic", size=14).next_to(line, DOWN, buff=0.1).align_to(line, RIGHT)
        self.cue("While the bug")
        self.play(FadeIn(line[0]), FadeIn(name), FadeIn(sch), run_time=0.6)
        self.cue("carries a marker")
        self.play(Write(marker), run_time=1.2)

        def runs(where, res, color, sub):
            n = label(where, size=26, color=WHITE, weight=SEMIBOLD)
            r = VGroup(*[pill(x, color) for x in res]).arrange(RIGHT, buff=0.25)
            s = label(sub, size=18)
            return VGroup(n, r, s).arrange(DOWN, buff=0.25)

        main = runs("main", ["fails", "fails"], RED_3B, "exactly as the marker says")
        branch = runs("fix branch", ["passes", "passes"], GREEN_3B, "the marker no longer holds")
        done = runs("marker removed", ["check"], BLUE_3B, "an ordinary check")
        steps = VGroup(main, branch, done).arrange(RIGHT, buff=1.0).shift(DOWN * 0.6)
        arrows = VGroup(Arrow(main.get_right(), branch.get_left(), buff=0.2, color=GREY_3B),
                        Arrow(branch.get_right(), done.get_left(), buff=0.2, color=GREY_3B))
        self.cue("On main")
        self.play(FadeIn(main[0]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in main[1]], lag_ratio=0.5), FadeIn(main[2]), run_time=1.0)
        self.cue("On the fix branch")
        self.play(GrowArrow(arrows[0]), FadeIn(branch[0]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in branch[1]], lag_ratio=0.5), FadeIn(branch[2]), run_time=1.0)
        self.cue("Then the marker")
        strike = Line(marker.get_left(), marker.get_right(), color=WHITE, stroke_width=3)
        self.play(Create(strike), marker.animate.set_opacity(0.3), run_time=0.7)
        self.play(GrowArrow(arrows[1]), FadeIn(done, shift=UP * 0.2), run_time=0.8)
        self.cue("The break has become")
        self.beat("fix")
        shield = RegularPolygon(6, color=GREEN_3B, stroke_width=3, fill_color=GREEN_3B,
                                fill_opacity=0.25).scale(0.45).next_to(done, UP, buff=0.25)
        self.play(GrowFromCenter(shield), run_time=0.6)
        self.cue("And the map runs")
        loop = CurvedArrow(done.get_bottom() + DOWN * 0.15, main.get_bottom() + DOWN * 0.15, angle=-TAU / 6,
                           color=YELLOW_3B, stroke_width=3)
        daily = label("every day", size=20, color=YELLOW_3B).next_to(loop, DOWN, buff=0.1)
        self.play(Create(loop), FadeIn(daily), run_time=1.2)
        self.cue("so if the bug")
        self.play(Indicate(shield, color=GREEN_3B, scale_factor=1.3), run_time=1.0)

    # 9 -------------------------------------------------------------------
    def freeze(self):
        head = self.title("Story 2: the frozen windows")
        wins = VGroup()
        bars = VGroup()
        for k in range(4):
            w = window(3.2, 1.9, f"conversation {k + 1}")
            wins.add(w)
        wins.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.45)).next_to(head, DOWN, buff=0.45).shift(LEFT * 1.6)
        for w in wins:
            track = Line(LEFT * 1.1, RIGHT * 1.1, color=DIM, stroke_width=6).move_to(w.frame.get_center() + DOWN * 0.15)
            prog = Line(LEFT * 1.1, LEFT * 1.1 + RIGHT * 0.01, color=BLUE_3B, stroke_width=6).move_to(
                track.get_start(), aligned_edge=LEFT)
            bars.add(VGroup(track, prog))
        srv = server_box(w=2.6, h=2.2).next_to(wins, RIGHT, buff=1.0)
        self.cue("Picture")
        self.play(LaggedStart(*[FadeIn(w) for w in wins], lag_ratio=0.2), FadeIn(bars), FadeIn(srv), run_time=1.4)
        progress = [ValueTracker(0.05) for _ in range(4)]
        for b, v in zip(bars, progress):
            b[1].add_updater(lambda m, v=v, b=b: m.put_start_and_end_on(
                b[0].get_start(), b[0].get_start() + RIGHT * 2.2 * min(v.get_value(), 1) + RIGHT * 0.001))
        self.play(*[v.animate.set_value(x) for v, x in zip(progress, [0.4, 0.3, 0.5, 0.25])], run_time=2.0,
                  rate_func=linear)
        self.cue("One run fails")
        err = pill("model unreachable", RED_3B, 16).move_to(wins[1].frame.get_center() + DOWN * 0.15)
        self.play(FadeOut(bars[1]), FadeIn(err, scale=0.8), wins[1].frame.animate.set_stroke(RED_3B), run_time=0.6)
        self.beat("sour")
        self.cue("And for about")
        clock_v = ValueTracker(0)
        clock = VGroup(Text("0.0", font=SANS, font_size=60, color=RED_3B),
                       label("seconds", size=22, color=RED_3B))
        clock.arrange(RIGHT, buff=0.2, aligned_edge=DOWN).next_to(srv, DOWN, buff=0.4)
        anchor = clock[0].get_right()

        def tick_clock(m):
            m.become(Text(f"{clock_v.get_value():.1f}", font=SANS, font_size=60, color=RED_3B)
                     .move_to(anchor, aligned_edge=RIGHT))

        clock[0].add_updater(tick_clock)
        frozen = [0, 2, 3]
        overlays = VGroup(*[wins[k].frame.copy().set_fill(BLACK, 0.55).set_stroke(width=0) for k in frozen])
        ice = VGroup(*[label("waiting…", size=18, color=GREY_3B).move_to(wins[k].frame.get_center() + UP * 0.35)
                       for k in frozen])
        self.add(clock)
        self.play(FadeIn(overlays), FadeIn(ice), clock_v.animate.set_value(5.0),
                  *[progress[k].animate.set_value(progress[k].get_value() + 0.001) for k in frozen],
                  run_time=5.0, rate_func=linear)
        clock[0].clear_updaters()
        self.cue("Every request")
        self.play(Indicate(ice, color=WHITE), run_time=1.0)
        for b in bars:
            b[1].clear_updaters()

    # 10 ------------------------------------------------------------------
    def freeze_fix(self):
        head = self.title("The bug: one lane, one long log line")
        lane_y = 1.2
        top = Line([-6.6, lane_y + 0.45, 0], [6.6, lane_y + 0.45, 0], color=GREY_3B, stroke_width=2)
        bot = Line([-6.6, lane_y - 0.45, 0], [6.6, lane_y - 0.45, 0], color=GREY_3B, stroke_width=2)
        lab = label("the event loop: every task takes a short turn", size=18).next_to(bot, DOWN, buff=0.15)
        self.cue("The server does")
        self.play(Create(top), Create(bot), FadeIn(lab), run_time=0.8)
        colors = [BLUE_3B, TEAL_3B, PURPLE_3B, BLUE_3B, TEAL_3B, ORANGE_3B, BLUE_3B, PURPLE_3B]
        tasks = VGroup(*[RoundedRectangle(width=0.55, height=0.5, corner_radius=0.08, stroke_width=0,
                                          fill_color=c, fill_opacity=0.7) for c in colors])
        for i, t in enumerate(tasks):
            t.move_to([-6.2 - i * 0.85, lane_y, 0])
        self.add(tasks)
        self.cue("where every task")
        self.play(tasks.animate.shift(RIGHT * 7.0), run_time=2.5, rate_func=linear)
        self.cue("the server logged it")
        tb_lines = VGroup(*[Line(LEFT * 1.1, LEFT * 1.1 + RIGHT * w, stroke_width=3,
                                 color=[RED_3B, ORANGE_3B, YELLOW_3B, PURPLE_3B][i % 4])
                            for i, w in enumerate(np.random.default_rng(3).uniform(0.6, 2.1, 12))])
        tb_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        tb = card(tb_lines, buff=0.15, edge=RED_3B).scale(0.8).move_to([2.6, lane_y, 0])
        tb_l = label("traceback, ~1000 lines, drawn in the lane", size=16, color=RED_3B).next_to(top, UP, buff=0.12).set_x(2.6)
        self.play(FadeIn(tb, scale=0.6), FadeIn(tb_l), run_time=0.8)
        # tasks pile up behind it
        front = [t for t in tasks if t.get_x() < 1.4]
        passed = [t for t in tasks if t.get_x() >= 1.4]
        self.cue("Nothing else")
        anims = [t.animate.set_x(1.4 - 0.62 * k - 0.3) for k, t in
                 enumerate(sorted(front, key=lambda m: -m.get_x()))]
        anims += [t.animate.shift(RIGHT * 4) for t in passed]
        self.play(*anims, run_time=1.5)
        self.play(Wiggle(tb), run_time=0.8)

        self.cue("The agents running")
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 5000, 1000], x_length=6.5, y_length=2.7,
                  axis_config={"color": GREY_3B, "include_ticks": False}).move_to([-2.6, -2.1, 0])
        ylab = label("slowest health check, ms", size=16).next_to(ax.y_axis, UP, buff=0.1)
        thr = DashedLine(ax.c2p(0, 1500), ax.c2p(4, 1500), color=YELLOW_3B, stroke_width=2)
        data = [(0.6, 4540, RED_3B), (1.4, 4791, RED_3B), (2.6, 142, GREEN_3B), (3.4, 93, GREEN_3B)]
        bars, nums = VGroup(), VGroup()
        for x, v, c in data:
            b = Rectangle(width=0.55, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.03),
                          fill_color=c, fill_opacity=0.85, stroke_width=0)
            b.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            bars.add(b)
            nums.add(label(f"{v}", size=16, color=c).next_to(b, UP, buff=0.06))
        lm = label("before", size=18, color=WHITE).next_to(VGroup(bars[0], bars[1]), DOWN, buff=0.15)
        lb = label("after", size=18, color=WHITE).next_to(VGroup(bars[2], bars[3]), DOWN, buff=0.15)
        self.play(Create(ax), FadeIn(ylab), Create(thr), run_time=0.8)
        self.cue("took more than")
        self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(nums[:2]), FadeIn(lm), run_time=1.2)
        self.cue("The fix is funnily")
        plain = card(VGroup(*[Line(LEFT * 0.9, LEFT * 0.9 + RIGHT * w, stroke_width=2, color=GREY_3B)
                              for w in (1.6, 1.2, 1.4)]).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
                     buff=0.1).move_to([4.4, -1.7, 0])
        plain_l = label("plain text, written in a blink", size=16, color=GREEN_3B).next_to(plain, DOWN, buff=0.12)
        self.play(FadeOut(tb), FadeOut(tb_l), FadeIn(plain), FadeIn(plain_l), run_time=0.8)
        self.play(*[t.animate.shift(RIGHT * 9) for t in tasks], run_time=1.6, rate_func=linear)
        self.beat("fix")
        self.cue("Now the slowest")
        self.play(GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN), FadeIn(nums[2:]), FadeIn(lb), run_time=1.0)
        b = pill("fix #5780  ·  merged", PURPLE_3B, 18).to_corner(DR, buff=0.4)
        self.play(FadeIn(b))

    # 11 ------------------------------------------------------------------
    def secrets(self):
        head = self.title("Story 3: the vanished keys")
        names = ["LLM API key", "GITHUB_TOKEN", "QA_TOKEN"]
        boxes = VGroup()
        for n in names:
            r = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.12, stroke_color=BLUE_3B,
                                 stroke_width=2, fill_color=BLUE_3B, fill_opacity=0.08)
            t = label(n, size=18, color=WHITE).move_to(r.get_top() + DOWN * 0.3)
            l = lock(BLUE_3B).move_to(r.get_center() + DOWN * 0.2)
            boxes.add(VGroup(r, t, l))
        boxes.arrange(RIGHT, buff=0.4).move_to([1.6, 0.6, 0])
        srv_lab = label("stored by agent-server", size=18).next_to(boxes, UP, buff=0.25)
        key_a = key_icon("key A", BLUE_3B).move_to([-4.6, 0.6, 0])
        holder = label("the server's own key", size=18).next_to(key_a, UP, buff=0.3)
        self.cue("The server keeps")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.25), FadeIn(srv_lab), run_time=1.4)
        self.cue("with a secret key")
        self.play(FadeIn(key_a, shift=RIGHT * 0.2), FadeIn(holder), run_time=0.8)
        self.cue("Suppose that key")
        key_b = key_icon("key B", ORANGE_3B).move_to(key_a)
        self.play(FadeOut(key_a, shift=DOWN * 0.4), FadeIn(key_b, shift=DOWN * 0.4), run_time=0.9)
        self.cue("The server can no longer")
        tries = VGroup(*[Arrow(key_b.get_right(), b[2].get_left(), buff=0.15, color=ORANGE_3B, stroke_width=2,
                               max_tip_length_to_length_ratio=0.06) for b in boxes])
        self.play(LaggedStart(*[GrowArrow(a) for a in tries], lag_ratio=0.2), run_time=1.0)
        xs = VGroup(*[Cross(b[2], stroke_color=RED_3B, stroke_width=3).scale(0.8) for b in boxes])
        self.play(FadeIn(xs), run_time=0.5)
        self.cue("So it reads")
        self.play(FadeOut(tries), FadeOut(xs), run_time=0.4)
        ui = window(5.0, 2.0, "Settings").move_to([1.6, -2.3, 0])
        fields = VGroup(*[VGroup(label(n, size=16, color=WHITE), label("not set", size=16, color=GREY_3B))
                          .arrange(RIGHT, buff=0.4) for n in names[:2]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fields.move_to(ui.frame.get_center() + DOWN * 0.15)
        self.play(FadeIn(ui), FadeIn(fields), run_time=0.8)
        self.cue("Nothing looks wrong")
        self.play(Indicate(fields, color=GREY_3B, scale_factor=1.03), run_time=1.0)
        self.sec = (boxes, key_b, ui, fields, srv_lab, head)

    # 12 ------------------------------------------------------------------
    def secrets_fix(self):
        head = self.title("The bug: a save erases them")
        names = ["LLM API key", "GITHUB_TOKEN", "QA_TOKEN"]
        boxes = VGroup()
        for n in names:
            r = RoundedRectangle(width=2.4, height=1.2, corner_radius=0.12, stroke_color=BLUE_3B,
                                 stroke_width=2, fill_color=BLUE_3B, fill_opacity=0.08)
            t = label(n, size=17, color=WHITE).move_to(r.get_top() + DOWN * 0.28)
            l = lock(BLUE_3B).move_to(r.get_center() + DOWN * 0.18)
            boxes.add(VGroup(r, t, l))
        boxes.arrange(RIGHT, buff=0.35).move_to([2.2, 1.3, 0])
        key_b = key_icon("key B", ORANGE_3B).move_to([-4.8, 1.3, 0])
        ui = window(4.4, 2.3, "Settings").move_to([-3.6, -1.7, 0])
        sw_lab = label("Show tips", size=18, color=WHITE)
        sw = toggle(False)
        row = VGroup(sw_lab, sw).arrange(RIGHT, buff=0.5).move_to(ui.frame.get_center() + UP * 0.05)
        save = button("Save", BLUE_3B).next_to(row, DOWN, buff=0.3)
        self.add(boxes, key_b)
        self.play(FadeIn(boxes), FadeIn(key_b), FadeIn(ui), FadeIn(row), FadeIn(save), run_time=0.8)
        self.cue("Then you flip")
        sw_on = toggle(True).move_to(sw)
        self.play(Transform(sw, sw_on), run_time=0.5)
        self.cue("and press save")
        self.play(Indicate(save, color=BLUE_3B), run_time=0.5)
        a = Arrow(ui.frame.get_right(), boxes.get_bottom() + LEFT * 1.0, buff=0.15, color=BLUE_3B, stroke_width=3)
        self.play(GrowArrow(a), run_time=0.5)
        self.cue("The server writes")
        nulls = VGroup(*[mono("null", size=22, color=RED_3B).move_to(b[2]) for b in boxes])
        self.play(*[FadeOut(b[2], scale=0.5) for b in boxes], *[b[0].animate.set_stroke(RED_3B).set_fill(RED_3B, 0.06)
                                                               for b in boxes], run_time=0.8)
        self.play(LaggedStart(*[FadeIn(nl, scale=1.3) for nl in nulls], lag_ratio=0.25), run_time=0.9)
        self.beat("sour")
        self.cue("Two hundred")
        ok = pill("200 OK", GREEN_3B, 20).next_to(a, RIGHT, buff=0.2)
        self.play(FadeIn(ok), run_time=0.4)
        self.cue("Even when")
        key_a = key_icon("key A", BLUE_3B).next_to(key_b, DOWN, buff=0.5)
        self.play(FadeIn(key_a, shift=RIGHT * 0.2), run_time=0.6)
        gone = label("gone for good", size=22, color=RED_3B, weight=SEMIBOLD).next_to(boxes, UP, buff=0.25)
        self.play(FadeIn(gone), run_time=0.5)

        self.cue("The fix has two parts")
        self.play(*[FadeOut(m) for m in [a, ok, gone, nulls, key_a, ui, row, save, sw]], run_time=0.6)
        for b in boxes:
            nl = lock(BLUE_3B).move_to(b[0].get_center() + DOWN * 0.18)
            b.remove(b[2])
            b.add(nl)
        self.play(*[b[0].animate.set_stroke(BLUE_3B).set_fill(BLUE_3B, 0.08) for b in boxes],
                  *[FadeIn(b[2]) for b in boxes], run_time=0.6)
        self.cue("First, if")
        refuse = card(VGroup(label("1  Refuse the write", size=22, color=WHITE, weight=SEMIBOLD),
                             mono("409  a stored value can't be decrypted:", size=15, color=YELLOW_3B),
                             mono("     restore the key, or list it as previous", size=15, color=YELLOW_3B)
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.12), buff=0.25)
        refuse.move_to([-3.4, -1.6, 0])
        self.play(FadeIn(refuse, shift=UP * 0.2), run_time=0.8)
        self.cue("Second, real key rotation")
        ring = VGroup(key_icon("key B · current", ORANGE_3B), key_icon("key A · previous", BLUE_3B)).arrange(DOWN, buff=0.35)
        ring.move_to([3.4, -1.9, 0])
        rot_t = label("2  Rotate", size=22, color=WHITE, weight=SEMIBOLD).next_to(ring, LEFT, buff=0.5)
        self.play(FadeOut(key_b), FadeIn(ring), FadeIn(rot_t), run_time=0.8)
        self.cue("reads old values")
        self.play(*[b[2].animate.become(lock(BLUE_3B, open_=True).move_to(b[2])) for b in boxes], run_time=0.7)
        self.cue("and quietly")
        self.play(*[b[2].animate.become(lock(ORANGE_3B).move_to(b[2])) for b in boxes],
                  *[b[0].animate.set_stroke(ORANGE_3B).set_fill(ORANGE_3B, 0.08) for b in boxes], run_time=0.9)
        self.beat("fix")
        b = pill("PR #5758  ·  open, in review", BLUE_3B, 18).to_corner(DR, buff=0.3)
        self.play(FadeIn(b))

    # 13 ------------------------------------------------------------------
    def decide(self):
        head = self.title("The choices stay with people")
        q = para("A refused secrets write: answer 409 like settings, or keep today's code?",
                 width=70, size=22, color=WHITE)
        imp_tag = label("Implemented", size=21, color=GREEN_3B, weight=BOLD)
        imp = para("keep the existing mapping: 409 for settings, 500 for secrets.", width=64, size=21)
        alt_tag = label("Alternative", size=21, color=ORANGE_3B, weight=BOLD)
        alt = para("409 for secrets too, so the guidance reaches the client.", width=64, size=21, color="#D7D9DE")
        dh = Text("Decision needed", font=SANS, font_size=30, color=YELLOW_3B, weight=BOLD)
        rule = Line(LEFT, RIGHT, stroke_width=1.5, color=GREY_3B)
        imp_row = VGroup(imp_tag, imp).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        alt_row = VGroup(alt_tag, alt).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        body = VGroup(dh, rule, q, imp_row, alt_row).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        rule.set_width(max(q.width, imp.width, alt.width)).align_to(dh, LEFT)
        dc = card(body, buff=0.4, edge=YELLOW_3B).next_to(head, DOWN, buff=0.4)
        src = label("from the description of PR #5758", size=16).next_to(dc, DOWN, buff=0.15)
        self.cue("Fixes like these")
        self.play(FadeIn(dc[0]), run_time=0.5)
        self.cue("Should a refused")
        self.play(FadeIn(q), run_time=0.7)
        self.cue("Decision needed")
        self.play(Write(dh), Create(rule), FadeIn(src), run_time=0.9)
        self.cue("what was built")
        self.play(FadeIn(imp_row, shift=RIGHT * 0.2), run_time=0.6)
        self.cue("and the alternative")
        self.play(FadeIn(alt_row, shift=RIGHT * 0.2), run_time=0.6)
        self.cue("The agent does")
        self.play(dc.animate.scale(0.7).shift(UP * 0.35), FadeOut(src), run_time=0.7)
        bot = robot().scale(1.3)
        p = person().scale(1.2)
        lt = label("does the work", size=22, color=TEAL_3B)
        rt = label("keep the choices", size=22, color=WHITE)
        left = VGroup(bot, lt).arrange(DOWN, buff=0.25)
        right = VGroup(p, rt).arrange(DOWN, buff=0.25)
        both = VGroup(left, right).arrange(RIGHT, buff=3.0).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(left, shift=UP * 0.2), run_time=0.7)
        self.cue("The people")
        self.play(FadeIn(right, shift=UP * 0.2), run_time=0.7)
        arr = Arrow(dc.get_bottom(), right.get_top(), buff=0.15, color=YELLOW_3B, stroke_width=3)
        self.play(GrowArrow(arr), run_time=0.6)

    # 14 ------------------------------------------------------------------
    def closing(self):
        t = prose("Agentic Engineering", size=60)
        t.to_edge(UP, buff=0.6)
        self.play(Write(t), run_time=1.2)
        items = [("Review the designs that matter", PURPLE_3B, "Review the designs"),
                 ("Constrain the code", BLUE_3B, "Constrain the code"),
                 ("Catch the break, prove the fix, keep the guard", GREEN_3B, "a net that catches")]
        rows = VGroup()
        for text, color, _ in items:
            arc = VGroup(*[ArcBetweenPoints(np.array([k * 0.5, 0, 0]), np.array([(k + 1) * 0.5, 0, 0]),
                                            angle=-PI / 5, color=color, stroke_width=3) for k in range(4)])
            rows.add(VGroup(arc, label(text, size=26, color=color, weight=SEMIBOLD)).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(t, DOWN, buff=0.6)
        for (text, color, phrase), r in zip(items, rows):
            self.cue(phrase)
            self.play(Create(r[0]), FadeIn(r[1], shift=RIGHT * 0.2), run_time=0.8)
        self.cue("keeps the guard")
        self.beat("fix")
        self.play(Indicate(rows[2], color=GREEN_3B, scale_factor=1.04), run_time=1.2)

    # 15 ------------------------------------------------------------------
    def credits(self):
        self.cue("The map, the tools")
        foot = VGroup(
            label("Map + CLI + fixes: github.com/OpenHands/software-agent-sdk", size=20, color=WHITE),
            label("Voice: Kokoro-82M (open weights, Apache-2.0), af_heart  ·  Animation: Manim", size=18),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(foot, shift=UP * 0.2), run_time=1.4)
