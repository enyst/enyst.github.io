"""Self-Healing explainer. Manim Community Edition.

Each narration segment is a wav with sentence timings (timings.json, from tts.py).
`cue(key)` waits until the sentence containing `key` starts, so the pictures
follow the voice.
"""
import json
import os

import numpy as np
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = {s["id"]: s for s in json.load(open(os.path.join(HERE, "timings.json")))}
ONLY = {int(x) for x in os.environ.get("SEGS", "").split(",") if x}

BG = "#14161b"
PANEL = "#1f232b"
PANEL2 = "#2a2f39"
EDGE = "#4a5160"
BLUE = "#58C4DD"
YEL = "#F4D35E"
GRN = "#83C167"
RED = "#FC6255"
ORA = "#F59E4B"
GREY = "#8a90a0"
INK = "#E8EAF0"
FONT = "Inter"
MONO = "DejaVu Sans Mono"

config.background_color = BG

# Pillow 12 refuses the float pixel arrays ImageMobject.interpolate_color leaves
# behind during fades; cast them back to uint8.
_interp = ImageMobject.interpolate_color


def _interp_uint8(self, m1, m2, alpha):
    _interp(self, m1, m2, alpha)
    self.pixel_array = np.clip(self.pixel_array, 0, 255).astype(np.uint8)
    return self


ImageMobject.interpolate_color = _interp_uint8


def txt(s, size=32, color=INK, weight=NORMAL, font=FONT):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def check(size=0.5, color=GRN, width=8):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([[-0.5, 0, 0], [-0.15, -0.38, 0], [0.55, 0.45, 0]])
    return m.scale(size)


def cross(size=0.5, color=RED, width=8):
    a = Line([-0.4, -0.4, 0], [0.4, 0.4, 0], stroke_color=color, stroke_width=width)
    b = Line([-0.4, 0.4, 0], [0.4, -0.4, 0], stroke_color=color, stroke_width=width)
    return VGroup(a, b).scale(size / 0.8)


def window(w=8.0, h=5.0):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.18,
                            fill_color=PANEL, fill_opacity=1, stroke_color=EDGE, stroke_width=2)
    bar = Line(body.get_corner(UL) + DOWN * 0.45, body.get_corner(UR) + DOWN * 0.45,
               stroke_color=EDGE, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.06, color=c) for c in (RED, YEL, GRN)]).arrange(RIGHT, buff=0.12)
    dots.next_to(body.get_corner(UL), DR, buff=0.17)
    return VGroup(body, bar, dots)


def dialog(title, w=5.0, h=3.0, accent=BLUE):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.14,
                            fill_color=PANEL2, fill_opacity=1, stroke_color=accent, stroke_width=3)
    t = txt(title, 26, INK, BOLD).next_to(body.get_corner(UL), DR, buff=0.28).align_to(body, LEFT).shift(RIGHT * 0.3)
    fields = VGroup(*[RoundedRectangle(width=w - 0.8, height=0.32, corner_radius=0.06,
                                       fill_color=PANEL, fill_opacity=1, stroke_width=0)
                      for _ in range(2)]).arrange(DOWN, buff=0.22)
    fields.next_to(t, DOWN, buff=0.3).align_to(t, LEFT)
    return VGroup(body, t, fields)


def keycap(label="Esc"):
    k = RoundedRectangle(width=1.2, height=0.85, corner_radius=0.12,
                         fill_color=PANEL2, fill_opacity=1, stroke_color=INK, stroke_width=2.5)
    return VGroup(k, txt(label, 28, INK, BOLD).move_to(k))


def chip(label, color=BLUE, size=24, pad=0.22):
    t = txt(label, size, color)
    r = RoundedRectangle(width=t.width + 2 * pad, height=t.height + 1.3 * pad, corner_radius=0.12,
                         stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
    return VGroup(r, t.move_to(r))


def card(title, lines, w=4.6, color=BLUE, title_size=26, size=22):
    t = txt(title, title_size, color, BOLD)
    body = VGroup(*[txt(l, size, INK) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    inner = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    r = RoundedRectangle(width=max(w, inner.width + 0.6), height=inner.height + 0.6, corner_radius=0.16,
                         fill_color=PANEL, fill_opacity=1, stroke_color=color, stroke_width=2.5)
    inner.move_to(r)
    return VGroup(r, inner)


def agent(color=BLUE):
    head = Circle(radius=0.22, fill_color=color, fill_opacity=1, stroke_width=0)
    eyes = VGroup(Dot(radius=0.035, color=BG), Dot(radius=0.035, color=BG)).arrange(RIGHT, buff=0.1).move_to(head).shift(UP * 0.03)
    return VGroup(head, eyes)


def net(width=9.0, y=-3.15, sag=0.45, rows=3, cols=16, color=BLUE):
    def curve(dy):
        return FunctionGraph(lambda x: y + dy + sag * ((2 * x / width) ** 2 - 1),
                             x_range=[-width / 2, width / 2], color=color, stroke_width=2.5)
    hs = VGroup(*[curve(0.22 * i) for i in range(rows)])
    vs = VGroup()
    for j in range(cols + 1):
        x = -width / 2 + width * j / cols
        y0 = y + sag * ((2 * x / width) ** 2 - 1)
        vs.add(Line([x, y0, 0], [x, y0 + 0.22 * (rows - 1), 0], color=color, stroke_width=2))
    posts = VGroup(Line([-width / 2, y - 0.3, 0], [-width / 2, y + 0.9, 0], color=GREY, stroke_width=4),
                   Line([width / 2, y - 0.3, 0], [width / 2, y + 0.9, 0], color=GREY, stroke_width=4))
    return VGroup(hs, vs, posts)


def shot(name, height=3.2, color=EDGE):
    im = ImageMobject(os.path.join(HERE, name)).set(height=height)
    frame = SurroundingRectangle(im, buff=0.0, color=color, stroke_width=3, corner_radius=0.06)
    return Group(im, frame)


FAMILIES = ["First run", "App shell", "Home", "Conversation list", "Composer", "Agent activity",
            "Conversation", "Workspace", "Settings", "LLM profiles", "Providers", "Model router",
            "Agent profiles", "Secrets", "Agent behavior", "App settings", "MCP servers", "Skills",
            "Plugins", "Canvas apps", "Automations", "New automation", "Automation detail", "Git sync",
            "Backends", "Runtimes", "Workspace tools", "Automation setup"]


def feature_map(cell_w=1.75, cell_h=0.95):
    cells = VGroup()
    for i, name in enumerate(FAMILIES):
        # No fill: an animated border is redrawn on top, and a filled one would hide the label.
        r = RoundedRectangle(width=cell_w, height=cell_h, corner_radius=0.1, fill_color=PANEL,
                             fill_opacity=0, stroke_color=EDGE, stroke_width=1.5)
        fid = txt(f"F{i + 1:02d}", 18, BLUE, BOLD)
        nm = txt(name, 15, INK)
        if nm.width > cell_w - 0.2:
            nm.scale_to_fit_width(cell_w - 0.2)
        VGroup(fid, nm).arrange(DOWN, buff=0.1).move_to(r)
        cells.add(VGroup(r, fid, nm))
    cells.arrange_in_grid(rows=4, cols=7, buff=0.16)
    return cells


class SelfHealing(Scene):
    # ---------- timing ----------
    def start(self, i):
        self.i = i
        self.t0 = self.renderer.time
        self.add_sound(os.path.join(HERE, f"seg{i:02d}.wav"))

    def cue(self, key, offset=0.0):
        s = next(s for s in T[self.i]["sents"] if key in s["text"])
        dt = self.t0 + s["start"] + offset - self.renderer.time
        if dt < -0.25:
            print(f"[late] seg {self.i} cue {key!r} by {-dt:.2f}s")
        if dt > 0.02:
            self.wait(dt)

    def finish(self, clear=True):
        end = self.t0 + T[self.i]["dur"]
        if clear and self.mobjects:
            left = end - self.renderer.time
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=max(0.4, min(0.8, left)))
        dt = end - self.renderer.time
        if dt < -0.25:
            print(f"[late] seg {self.i} end by {-dt:.2f}s")
        if dt > 0.02:
            self.wait(dt)

    def construct(self):
        for i in range(1, 12):
            if ONLY and i not in ONLY:
                continue
            getattr(self, f"seg{i}")()
        self.wait(1.5)

    # ---------- 1. The factory ----------
    def seg1(self):
        self.start(1)
        base_y = -2.3
        layers = VGroup()

        def layer(k, color=BLUE):
            w = 3.2 - 0.06 * k
            r = RoundedRectangle(width=w, height=0.27, corner_radius=0.06, fill_color=color,
                                 fill_opacity=0.25, stroke_color=color, stroke_width=2)
            return r.move_to([0, base_y + 0.33 * k, 0])

        for k in range(3):
            layers.add(layer(k))
        label = txt("a codebase", 26, GREY).next_to(layers, DOWN, buff=0.3)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in layers], lag_ratio=0.3),
                  FadeIn(label), run_time=1.6)

        self.cue("Agents read code")
        bots = VGroup(agent(BLUE).move_to([-5, 0.5, 0]), agent(GRN).move_to([5, 1.2, 0]),
                      agent(YEL).move_to([-4.6, 2.4, 0]))
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in bots], lag_ratio=0.2), run_time=1)
        for k in range(3, 7):
            b = bots[k % 3]
            new = layer(k)
            pr = chip("PR", YEL, 18, 0.12).move_to(b)
            self.play(pr.animate.move_to(new.get_center()), run_time=0.5)
            self.play(FadeOut(pr), FadeIn(new, shift=DOWN * 0.15), run_time=0.35)
            layers.add(new)

        self.cue("That is a software factory")
        title = txt("a software factory", 40, INK, BOLD).to_edge(UP, buff=0.6)
        arrow = Arrow([2.4, base_y, 0], [2.4, 0.6, 0], buff=0, color=GRN, stroke_width=6)
        up_lbl = txt("self-improving", 26, GRN).next_to(arrow, RIGHT, buff=0.2)
        self.play(Write(title), GrowArrow(arrow), FadeIn(up_lbl), run_time=1.4)

        self.cue("And it runs at the speed")
        speed = txt("at the speed of agents", 34, YEL).next_to(title, DOWN, buff=0.25)
        person = VGroup(Circle(radius=0.2, color=GREY, stroke_width=3),
                        Arc(radius=0.35, start_angle=0, angle=PI, color=GREY, stroke_width=3).shift(DOWN * 0.55))
        person.move_to([-4.6, -1.6, 0])
        p_lbl = txt("one person", 20, GREY).next_to(person, DOWN, buff=0.15)
        self.play(FadeIn(speed, shift=DOWN * 0.2), FadeIn(person), FadeIn(p_lbl), run_time=0.8)
        prs = VGroup()
        for k in range(7, 11):
            new = layer(k)
            for j in range(3):
                prs.add(chip("PR", YEL, 16, 0.1).move_to(bots[j]))
            self.play(*[p.animate.move_to(new.get_center() + RIGHT * (j - 1) * 0.6)
                        for j, p in enumerate(prs[-3:])], FadeIn(new, shift=DOWN * 0.15), run_time=0.35)
            self.play(FadeOut(prs[-3:]), run_time=0.12)
            layers.add(new)
        q = txt("?", 48, GREY, BOLD).next_to(person, UP, buff=0.15)
        self.play(FadeIn(q, scale=0.5),
                  arrow.animate.put_start_and_end_on([2.4, base_y, 0], [2.4, 1.4, 0]),
                  up_lbl.animate.shift(UP * 0.4), run_time=0.6)

        self.cue("At the speed of agents, you need")
        ghost = net(width=8.0, y=-3.2, color=GREY).set_stroke(opacity=0.5)
        need = txt("needs a safety net", 34, INK).next_to(speed, DOWN, buff=0.15)
        self.play(FadeIn(need, shift=DOWN * 0.2), Create(ghost), FadeOut(q), run_time=1.2)

        self.cue("Something that notices")
        bad = layers[5]
        upper = VGroup(*layers[6:])
        self.play(bad.animate.set_stroke(RED).set_fill(RED, 0.5), run_time=0.5)
        self.play(Rotate(upper, -0.12, about_point=bad.get_right(), rate_func=there_and_back_with_pause),
                  run_time=1.0)
        self.play(Wiggle(bad), run_time=0.8)
        self.wait(1.2)
        self.play(bad.animate.set_stroke(BLUE).set_fill(BLUE, 0.25), run_time=0.8)

        self.cue("We call that")
        n = net(width=8.0, y=-3.2)
        name = txt("Self-Healing", 64, YEL, BOLD).to_edge(UP, buff=0.6)
        self.play(FadeOut(label), FadeOut(person), FadeOut(p_lbl), FadeOut(speed), FadeOut(need),
                  ReplacementTransform(ghost, n), ReplacementTransform(title, name), run_time=1.6)

        self.cue("Let's build it")
        rest = VGroup(layers, bots, arrow, up_lbl, n)
        self.play(rest.animate.set_opacity(0.15), run_time=1)
        sub = txt("from the ground up", 32, INK).next_to(name, DOWN, buff=0.3)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.finish()

    # ---------- 2. A promise ----------
    def seg2(self):
        self.start(2)
        win = window(8.8, 5.6).shift(LEFT * 1.4)
        self.play(FadeIn(win), run_time=1)

        self.cue("You open Settings")
        head = txt("Settings  ›  Application", 26, INK, BOLD)
        head.next_to(win[1], DOWN, buff=0.4).align_to(win[0], LEFT).shift(RIGHT * 0.6)

        def field(label, value):
            lab = txt(label, 20, GREY)
            box = RoundedRectangle(width=6.0, height=0.62, corner_radius=0.08, fill_color=PANEL2,
                                   fill_opacity=1, stroke_color=EDGE, stroke_width=1.5)
            val = txt(value, 24, INK).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.22)
            return VGroup(lab, VGroup(box, val).next_to(lab, DOWN, buff=0.12, aligned_edge=LEFT))

        f1, f2 = field("Git username", "QA Tester"), field("Git email", "qa-tester@example.com")
        form = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.4).align_to(head, LEFT)
        self.play(FadeIn(head), *[FadeIn(m) for m in (f1[0], f1[1][0], f2[0], f2[1][0])], run_time=0.8)
        self.play(AddTextLetterByLetter(f1[1][1], run_time=0.9))
        self.play(AddTextLetterByLetter(f2[1][1], run_time=1.3))

        self.cue("You press Save")
        save = chip("Save", YEL, 24).next_to(form, DOWN, buff=0.45).align_to(form, LEFT)
        self.play(FadeIn(save), run_time=0.4)
        self.play(save.animate.scale(0.9), run_time=0.12)
        self.play(save.animate.scale(1 / 0.9), run_time=0.15)

        self.cue("It says")
        toast = VGroup(check(0.3), txt("Settings saved", 24, INK)).arrange(RIGHT, buff=0.2)
        tb = RoundedRectangle(width=toast.width + 0.5, height=0.7, corner_radius=0.12, fill_color=PANEL2,
                              fill_opacity=1, stroke_color=GRN, stroke_width=2)
        toastg = VGroup(tb, toast.move_to(tb)).next_to(win[0].get_corner(UR), DL, buff=0.25).shift(DOWN * 0.45)
        self.play(FadeIn(toastg, shift=LEFT * 0.3), run_time=0.6)

        self.cue("Then you ask the agent")
        self.play(FadeOut(VGroup(head, form, save, toastg)), run_time=0.5)
        bubble = chip("Fix the typo, then commit it", BLUE, 24).move_to(win[0]).shift(UP * 1.4 + RIGHT * 1.0)
        bot = agent(BLUE).move_to(win[0]).shift(LEFT * 3.4 + UP * 0.2)
        self.play(FadeIn(bubble, shift=UP * 0.2), FadeIn(bot), run_time=0.7)
        commit = card("commit 3f9a2c1", ["Author: ?"], w=6.6, color=GREY, title_size=24, size=24)
        commit.move_to(win[0]).shift(RIGHT * 0.4 + DOWN * 0.5)
        self.play(FadeIn(commit, shift=RIGHT * 0.3), run_time=0.7)

        self.cue("What should happen")
        q = txt("?", 110, YEL, BOLD).next_to(win, RIGHT, buff=0.5)
        self.play(FadeIn(q, scale=0.5), run_time=0.5)

        self.cue("The commit carries")
        line = commit[1][1][0]
        author = txt("Author: QA Tester <qa-tester@example.com>", 24, GRN).move_to(line, aligned_edge=LEFT)
        self.play(Transform(line, author), commit[0].animate.set_stroke(GRN), FadeOut(q), run_time=0.9)
        ok = check(0.7).next_to(win, RIGHT, buff=0.5)
        self.play(Create(ok), run_time=0.5)

        self.cue("That is a promise")
        promise = card("A promise", ["Save your Git name in Settings:", "the agent's commits carry it."], w=6.6,
                       color=YEL, title_size=34, size=30)
        self.play(FadeOut(VGroup(win, bubble, bot, commit, ok)), FadeIn(promise, scale=0.8), run_time=1.1)

        self.cue("And a coding agent")
        self.play(Indicate(promise, color=YEL, scale_factor=1.05), run_time=1.2)
        self.promise = promise
        self.finish(clear=False)

    # ---------- 3. The map ----------
    def seg3(self):
        self.start(3)
        promise = getattr(self, "promise", None)
        recipe = VGroup(
            txt("F16 · App settings", 24, BLUE, BOLD),
            txt("Commits use the Git name from Settings", 30, INK, BOLD),
            txt("Steps", 22, GREY),
            txt("1  save Git name and email in Settings", 24, INK, font=MONO),
            txt("2  start a conversation", 24, INK, font=MONO),
            txt("3  the agent commits", 24, INK, font=MONO),
            txt("Expect", 22, GREY),
            txt("Author: QA Tester <qa-tester@example.com>", 24, GRN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for k in (2, 6):
            recipe[k].shift(DOWN * 0.12)
        box = RoundedRectangle(width=recipe.width + 0.9, height=recipe.height + 0.8, corner_radius=0.18,
                               fill_color=PANEL, fill_opacity=1, stroke_color=BLUE, stroke_width=2.5)
        recipe.move_to(box)
        rcard = VGroup(box, recipe)
        if promise is not None:
            self.play(ReplacementTransform(promise[0], box), FadeOut(promise[1]), run_time=1)
        else:
            self.play(FadeIn(box), run_time=1)

        self.cue("Give it a name")
        self.play(Write(recipe[0]), Write(recipe[1]), run_time=1.2)

        self.cue("Write the exact steps")
        self.play(FadeIn(recipe[2]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in recipe[3:6]],
                                                 lag_ratio=0.35), run_time=1.6)
        self.wait(1.4)
        self.play(FadeIn(recipe[6]), Write(recipe[7]), run_time=1.2)

        self.cue("Do that for every promise")
        fmap = feature_map().move_to(DOWN * 0.35)
        target = fmap[15]
        self.play(rcard.animate.scale(0.16).move_to(target.get_center()), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for k, c in enumerate(fmap) if k != 15], lag_ratio=0.05),
                  FadeOut(rcard), FadeIn(target), run_time=2.2)

        self.cue("The OpenHands feature map")
        head = txt("The feature map", 44, INK, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(head), run_time=1)
        for k in (0, 8, 6):
            self.play(Indicate(fmap[k], color=YEL, scale_factor=1.12), run_time=0.9)
        self.wait(0.6)
        self.finish()

    # ---------- 4. Hands ----------
    def seg4(self):
        self.start(4)
        fmap = feature_map().scale(0.55).move_to(LEFT * 3.2)
        walker = Dot(radius=0.12, color=YEL).move_to(fmap[0])
        self.play(FadeIn(fmap), run_time=0.8)
        self.play(FadeIn(walker), run_time=0.3)
        self.play(walker.animate.move_to(fmap[6]), run_time=1.2)
        self.play(walker.animate.move_to(fmap[15]), run_time=0.8)

        self.cue("So we give an agent hands")
        self.play(FadeOut(fmap), FadeOut(walker), run_time=0.6)
        term = RoundedRectangle(width=6.6, height=4.4, corner_radius=0.16, fill_color="#0c0e12",
                                fill_opacity=1, stroke_color=EDGE, stroke_width=2).move_to(LEFT * 3.3 + DOWN * 0.2)
        ttl = txt("control-openhands", 28, GRN, BOLD, MONO).next_to(term, UP, buff=0.2)
        bot = agent(BLUE).next_to(ttl, LEFT, buff=0.3)
        self.play(FadeIn(term), Write(ttl), FadeIn(bot), run_time=1.2)
        cmds = ["$ launch", "$ browser fill 'Git username' 'QA Tester'", "$ browser click 'Save'",
                "$ conversation start --wait", "$ browser screenshot"]
        lines = VGroup(*[txt(c, 19, INK, font=MONO) for c in cmds]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        lines.move_to(term).align_to(term, LEFT).shift(RIGHT * 0.3)

        app = window(5.4, 3.6).move_to(RIGHT * 3.7 + UP * 0.5)
        app_lbl = txt("the real app", 22, GREY).next_to(app, UP, buff=0.15)

        self.cue("It launches the real app")
        self.play(AddTextLetterByLetter(lines[0], run_time=0.6))
        self.play(FadeIn(app), FadeIn(app_lbl), run_time=0.6)
        self.play(AddTextLetterByLetter(lines[1], run_time=1.1))
        fbox = RoundedRectangle(width=3.8, height=0.5, corner_radius=0.06, fill_color=PANEL2, fill_opacity=1,
                                stroke_color=EDGE, stroke_width=1.5).move_to(app[0]).shift(UP * 0.4)
        fval = txt("QA Tester", 20, INK).move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * 0.15)
        cursor = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.12).rotate(0.4)
        cursor.move_to(app[0].get_corner(DR) + UL * 0.6)
        self.add(cursor)
        self.play(FadeIn(fbox), cursor.animate.move_to(fbox.get_center()), run_time=0.5)
        self.play(AddTextLetterByLetter(fval, run_time=0.5))
        self.play(AddTextLetterByLetter(lines[2], run_time=0.7))
        sv = chip("Save", YEL, 18, 0.15).next_to(fbox, DOWN, buff=0.3).align_to(fbox, LEFT)
        self.play(FadeIn(sv), cursor.animate.move_to(sv.get_center()), run_time=0.4)
        self.play(AddTextLetterByLetter(lines[3], run_time=0.9))
        self.play(AddTextLetterByLetter(lines[4], run_time=0.7))
        flash = app[0].copy().set_fill(WHITE, 0.6).set_stroke(width=0)
        self.play(FadeIn(flash, run_time=0.1))
        self.play(FadeOut(flash, run_time=0.4))
        snap = VGroup(app, fbox, fval, sv)
        thumb = snap.copy().scale(0.3)
        folder = chip("evidence/", YEL, 22).move_to(RIGHT * 3.7 + DOWN * 2.6)
        self.play(FadeIn(folder), thumb.animate.move_to(folder.get_center()).scale(0.6), run_time=0.8)
        self.play(FadeOut(thumb), run_time=0.3)

        self.cue("Not a test that says")
        self.play(*[FadeOut(m) for m in (term, ttl, bot, lines, snap, app_lbl, folder, cursor)], run_time=0.6)
        ci = VGroup(check(0.5), txt("tests passed", 34, GRN)).arrange(RIGHT, buff=0.3).move_to(LEFT * 3.8)
        self.play(FadeIn(ci), run_time=0.6)
        strike = Line(ci.get_left() + LEFT * 0.2, ci.get_right() + RIGHT * 0.2, color=GREY, stroke_width=5)
        self.play(Create(strike), ci.animate.set_opacity(0.4), run_time=0.6)

        self.cue("A picture of what")
        pic = shot("settings-saved.png", 3.8).move_to(RIGHT * 2.6)
        cap = txt("what a person sees", 24, YEL).next_to(pic, DOWN, buff=0.25)
        self.play(FadeIn(pic, scale=0.9), FadeIn(cap), run_time=1)
        self.finish()

    # ---------- 5. Every day ----------
    def seg5(self):
        self.start(5)
        main = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY, stroke_width=4).shift(UP * 2.6)
        mlabel = txt("main", 24, GREY).next_to(main, LEFT, buff=0.15).shift(RIGHT * 0.9 + UP * 0.35)
        self.play(Create(main), FadeIn(mlabel), run_time=1)

        self.cue("Every day, new code")
        days = VGroup()
        for k, x in enumerate(np.linspace(-5.5, 5.5, 6)):
            dot = Dot([x, 2.6, 0], radius=0.12, color=BLUE)
            days.add(VGroup(dot, txt(f"day {k + 1}", 18, GREY).next_to(dot, DOWN, buff=0.15)))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in days], lag_ratio=0.25), run_time=2)

        self.cue("And every day, an automation")
        fmap = feature_map().scale(0.62).move_to(DOWN * 0.9)
        self.play(FadeIn(fmap), Indicate(days[5][0], color=YEL), run_time=1)
        self.play(LaggedStart(*[c[0].animate.set_stroke(GRN, 2.5) for c in fmap], lag_ratio=0.08), run_time=3.2)

        self.cue("Sometimes, one doesn't")
        bad = fmap[15]
        self.play(bad[0].animate.set_stroke(RED, 4).set_fill(RED, 0.25), run_time=0.5)
        self.play(Indicate(bad, color=RED, scale_factor=1.25), run_time=0.9)

        self.cue("Here, the settings were saved")
        self.play(FadeOut(fmap), FadeOut(days), FadeOut(main), FadeOut(mlabel), run_time=0.5)
        left = shot("settings-saved.png", 3.4, GRN).move_to(LEFT * 3.5 + UP * 0.4)
        ll = txt("Settings saved", 24, GRN).next_to(left, DOWN, buff=0.2)
        self.play(FadeIn(left), FadeIn(ll), run_time=0.7)

        self.cue("But the agent's commit failed")
        right = shot("main-conversation.png", 3.4, RED).move_to(RIGHT * 3.5 + UP * 0.4)
        rl = chip("Author identity unknown · exit 128", RED, 22).next_to(right, DOWN, buff=0.2)
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.15, color=GREY, stroke_width=4)
        self.play(GrowArrow(arrow), FadeIn(right, shift=LEFT * 0.3), run_time=0.8)
        self.play(FadeIn(rl, shift=UP * 0.2), run_time=0.5)

        self.cue("On a machine that already")
        shots = Group(left, ll, right, rl, arrow)
        self.play(shots.animate.scale(0.5).to_edge(UP, buff=0.3).set_opacity(0.5), run_time=0.8)
        other = card("commit 3f9a2c1", ["Author: someone else"], w=5.6, color=RED, title_size=24, size=26).move_to(DOWN * 0.8)

        self.cue("The commit went through")
        self.play(FadeIn(other, shift=UP * 0.3), run_time=0.7)
        sil = txt("no error, wrong name", 24, RED).next_to(other, DOWN, buff=0.3)
        self.play(FadeIn(sil), Wiggle(other[1][1]), run_time=1.0)

        self.cue("Before calling it a bug")
        self.play(FadeOut(other), FadeOut(sil), run_time=0.5)
        a1 = VGroup(agent(BLUE), txt("first agent", 26, INK)).arrange(RIGHT, buff=0.3)
        a2 = VGroup(agent(GRN), txt("second agent, fresh app", 26, INK)).arrange(RIGHT, buff=0.3)
        rows = VGroup(a1, a2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(LEFT * 0.8 + DOWN * 0.8)
        x1 = cross(0.4).next_to(rows, RIGHT, buff=0.8).match_y(a1)
        self.play(FadeIn(a1), Create(x1), run_time=0.8)
        self.play(FadeIn(a2, shift=RIGHT * 0.2), run_time=0.6)

        self.cue("It fails the same way")
        x2 = cross(0.4).match_x(x1).match_y(a2)
        self.play(Create(x2), run_time=0.6)

        self.cue("A real failure repeats")
        real = chip("real: it repeats", RED, 26).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(real, shift=UP * 0.2), run_time=0.6)

        self.cue("A flaky one")
        flaky = VGroup(txt("flaky:", 24, GREY), cross(0.3, GREY), check(0.3, GREY)).arrange(RIGHT, buff=0.25)
        flaky.next_to(real, RIGHT, buff=0.6)
        self.play(FadeIn(flaky), run_time=0.6)
        self.finish()

    # ---------- 6. Why it hid ----------
    def pipeline(self):
        names = ["Settings", "start request", "agent server", "terminal", "git"]
        boxes = VGroup()
        for n in names:
            t = txt(n, 22, INK, BOLD)
            r = RoundedRectangle(width=2.3, height=1.0, corner_radius=0.14, fill_color=PANEL, fill_opacity=1,
                                 stroke_color=BLUE, stroke_width=2.5)
            boxes.add(VGroup(r, t.move_to(r)))
        boxes.arrange(RIGHT, buff=0.45)
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05, color=GREY,
                                stroke_width=4, max_tip_length_to_length_ratio=0.35) for k in range(4)])
        return boxes, arrows

    def seg6(self):
        self.start(6)
        q = txt("Why did it break?", 44, INK, BOLD).to_edge(UP, buff=0.6)
        self.play(Write(q), run_time=1)
        boxes, arrows = self.pipeline()

        self.cue("Follow the name")
        tok = chip("QA Tester", YEL, 24).next_to(boxes[0], UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.15),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.5)
        self.play(FadeIn(tok, shift=DOWN * 0.2), run_time=0.5)

        self.cue("It is saved in Settings")
        c0 = check(0.4).next_to(boxes[0], DOWN, buff=0.3)
        self.play(Create(c0), boxes[0][0].animate.set_stroke(GRN), run_time=0.7)

        self.cue("But when a conversation starts")
        self.play(tok.animate.move_to(arrows[0].get_center() + UP * 0.6), run_time=0.9)
        self.play(tok.animate.shift(DOWN * 2.6).set_opacity(0), arrows[0].animate.set_color(RED), run_time=1.0,
                  rate_func=rush_into)
        gap = cross(0.35).move_to(arrows[0])
        nl1 = txt("no git name", 20, RED).next_to(boxes[1], DOWN, buff=0.3)
        self.play(Create(gap), FadeIn(nl1), run_time=0.7)

        self.cue("The terminal never sees it")
        nl3 = txt("GIT_* : none", 20, RED, font=MONO).next_to(boxes[3], DOWN, buff=0.3)
        self.play(FadeIn(nl3), boxes[3][0].animate.set_stroke(RED), run_time=0.7)

        self.cue("And git, at the end")
        nl4 = txt("Author identity\nunknown", 20, RED).next_to(boxes[4], DOWN, buff=0.3)
        self.play(FadeIn(nl4), boxes[4][0].animate.set_stroke(RED).set_fill(RED, 0.2), run_time=0.7)
        self.play(Wiggle(boxes[4]), run_time=0.8)

        self.cue("Every piece looked fine")
        unit = VGroup(*[check(0.3).next_to(b, UP, buff=0.25) for b in boxes])
        ul = txt("each piece, tested alone: fine", 22, GRN).next_to(boxes, UP, buff=0.9)
        self.play(LaggedStart(*[Create(c) for c in unit], lag_ratio=0.15), FadeIn(ul), run_time=1.3)

        self.cue("The promise broke in the gaps")
        self.play(LaggedStart(*[Indicate(a, color=RED, scale_factor=1.4) for a in arrows], lag_ratio=0.2),
                  run_time=1.6)

        self.cue("Only a walk through")
        walker = Dot(radius=0.14, color=YEL).move_to(boxes[0].get_center() + DOWN * 1.6)
        path = VMobject().set_points_as_corners([boxes[k].get_center() + DOWN * 1.6 for k in range(5)])
        e2e = txt("end to end, on the real app", 26, YEL).next_to(path, DOWN, buff=0.45)
        self.play(FadeIn(walker), FadeOut(VGroup(nl1, nl3, nl4)), run_time=0.4)
        self.play(MoveAlongPath(walker, path), Create(path.copy().set_stroke(YEL, 3)), FadeIn(e2e),
                  run_time=2.2)
        self.play(Flash(walker, color=RED), run_time=0.6)
        self.finish()

    # ---------- 7. Remember the bug ----------
    def seg7(self):
        self.start(7)
        issue = card("Issue #17899", ["Git name from Settings never", "reaches agent commits"], w=5.4,
                     color=RED).move_to(LEFT * 3.2 + UP * 0.6)
        ev = shot("main-conversation.png", 1.4, RED).next_to(issue, DOWN, buff=0.3)
        clip = txt("evidence attached", 20, GREY).next_to(ev, RIGHT, buff=0.25)
        self.play(FadeIn(issue, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(ev, shift=UP * 0.2), FadeIn(clip), run_time=0.8)

        self.cue("And the map learns")
        mini = feature_map().scale(0.42).move_to(RIGHT * 3.3 + UP * 0.6)
        mini[15][0].set_stroke(RED, 3).set_fill(RED, 0.2)
        self.play(FadeIn(mini), run_time=0.8)

        self.cue("The step gets")
        tag = chip("known bug #17899", ORA, 20).next_to(mini, DOWN, buff=0.35)
        link = Arrow(tag.get_top(), mini[15].get_bottom(), buff=0.08, color=ORA, stroke_width=3)
        self.play(FadeIn(tag, shift=UP * 0.2), GrowArrow(link), run_time=0.8)
        code = txt("$ control-openhands bug run", 20, INK, font=MONO).next_to(tag, DOWN, buff=0.35)
        self.play(AddTextLetterByLetter(code, run_time=0.9))

        self.cue("Today, it is expected")
        xf = chip("xfail  ·  expected to fail", ORA, 24).next_to(code, DOWN, buff=0.35)
        self.play(FadeIn(xf, scale=0.8), run_time=0.6)

        self.cue("The day it stops")
        xp = chip("xpass  ·  it stopped failing!", GRN, 24).move_to(xf)
        self.play(Transform(xf, xp), mini[15][0].animate.set_stroke(GRN, 3).set_fill(GRN, 0.2), run_time=0.9)
        self.play(Indicate(xf, color=GRN), run_time=0.9)
        self.finish()

    # ---------- 8. The fix, with proof ----------
    def seg8(self):
        self.start(8)
        pr = card("Fix pull request", [], w=5.4, color=GRN, title_size=30)
        pr[0].stretch_to_fit_height(2.4).move_to(UP * 0.4)
        pr[1].next_to(pr[0].get_top(), DOWN, buff=0.3)
        self.play(FadeIn(pr), run_time=0.8)

        self.cue("A pull request changes")
        files = VGroup(chip("product code", BLUE), chip("tests", BLUE)).arrange(RIGHT, buff=0.35)
        files.move_to(pr[0]).shift(DOWN * 0.25)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in files], lag_ratio=0.4), run_time=1)

        self.cue("Nothing else")
        nope = chip("feature map", GREY).next_to(pr[0], RIGHT, buff=0.6)
        nx = cross(0.35).move_to(nope)
        self.play(FadeIn(nope), run_time=0.4)
        self.play(Create(nx), nope.animate.set_opacity(0.35), run_time=0.6)

        self.cue("Now the start request carries")
        self.play(FadeOut(VGroup(pr, files, nope, nx)), run_time=0.5)
        boxes, arrows = self.pipeline()
        VGroup(boxes, arrows).move_to(UP * 0.4)
        self.play(FadeIn(boxes), FadeIn(arrows), run_time=0.7)
        tok = chip("QA Tester", YEL, 24).next_to(boxes[0], UP, buff=0.3)
        self.play(FadeIn(tok, shift=DOWN * 0.2), run_time=0.4)
        for k in range(1, 5):
            self.play(tok.animate.next_to(boxes[k], UP, buff=0.3), arrows[k - 1].animate.set_color(GRN),
                      boxes[k - 1][0].animate.set_stroke(GRN), run_time=0.6)
        self.play(boxes[4][0].animate.set_stroke(GRN).set_fill(GRN, 0.2), run_time=0.4)
        env = txt("GIT_AUTHOR_NAME=QA Tester", 20, GRN, font=MONO).next_to(boxes[3], DOWN, buff=0.35)
        self.play(FadeIn(env, shift=UP * 0.2), run_time=0.6)

        self.cue("The proof is the same walk")
        self.play(FadeOut(VGroup(boxes, arrows, tok, env)), run_time=0.5)
        a = shot("main-conversation.png", 3.3, RED).move_to(LEFT * 3.4 + UP * 0.4)
        b = shot("fix-conversation.png", 3.3, GRN).move_to(RIGHT * 3.4 + UP * 0.4)
        ta = txt("old code", 26, INK, BOLD).next_to(a, UP, buff=0.2)
        tb = txt("the fix", 26, INK, BOLD).next_to(b, UP, buff=0.2)
        self.play(FadeIn(a), FadeIn(b), FadeIn(ta), FadeIn(tb), run_time=0.8)

        self.cue("Before: Author identity")
        la = chip("Author identity unknown", RED, 22).next_to(a, DOWN, buff=0.2)
        self.play(FadeIn(la, shift=UP * 0.2), Indicate(a[1], color=RED, scale_factor=1.04), run_time=0.9)

        self.cue("After: committed")
        lb = chip("committed as QA Tester", GRN, 22).next_to(b, DOWN, buff=0.2)
        self.play(FadeIn(lb, shift=UP * 0.2), Indicate(b[1], color=GRN, scale_factor=1.04), run_time=0.9)

        self.cue("And the rule is strict")
        grp = Group(a, b, ta, tb, la, lb)
        self.play(grp.animate.scale(0.55).to_edge(UP, buff=0.3), run_time=0.8)
        rows = VGroup(txt("old code", 26, GREY), txt("the fix", 26, GREY)).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        rows.move_to(LEFT * 2.2 + DOWN * 1.6)
        self.play(FadeIn(rows), run_time=0.5)

        self.cue("Twice on the old code")
        xs = VGroup(cross(0.45), cross(0.45)).arrange(RIGHT, buff=0.6).next_to(rows[0], RIGHT, buff=0.9)
        self.play(LaggedStart(*[Create(x) for x in xs], lag_ratio=0.5), run_time=1.0)

        self.cue("Twice on the fix")
        cs = VGroup(check(0.55), check(0.55)).arrange(RIGHT, buff=0.6).next_to(rows[1], RIGHT, buff=0.9).match_x(xs)
        self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.5), run_time=1.0)
        self.finish()

    # ---------- 9. One rule ----------
    def seg9(self):
        self.start(9)
        wall = DashedLine(UP * 3, DOWN * 3, color=GREY, dash_length=0.15)
        self.play(Create(wall), run_time=0.8)

        self.cue("The fix never touches")
        left = card("Map PR", ["what should be true"], w=4.6, color=YEL, title_size=32, size=26).move_to(LEFT * 3.4)
        right = card("Fix PR", ["makes it true"], w=4.6, color=GRN, title_size=32, size=26).move_to(RIGHT * 3.4)
        bridge = Arrow(right.get_left(), left.get_right(), buff=0.15, color=RED, stroke_width=5)
        bx = cross(0.45).move_to(bridge)
        self.play(FadeIn(right), run_time=0.6)
        self.play(GrowArrow(bridge), run_time=0.5)
        self.play(Create(bx), bridge.animate.set_opacity(0.3), run_time=0.5)

        self.cue("The map says")
        self.play(FadeOut(bridge), FadeOut(bx), FadeIn(left, shift=RIGHT * 0.3), run_time=0.8)

        self.cue("The fix makes it true")
        self.play(Indicate(right, color=GRN, scale_factor=1.05), run_time=1)

        self.cue("They live in separate")
        q1 = txt("the test", 28, YEL).next_to(left, DOWN, buff=0.5)
        q2 = txt("the answer", 28, GRN).next_to(right, DOWN, buff=0.5)
        self.play(Indicate(wall, color=INK), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(q1, shift=UP * 0.2), FadeIn(q2, shift=UP * 0.2), run_time=0.8)
        self.finish()

    # ---------- 10. Healed ----------
    def seg10(self):
        self.start(10)
        main = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY, stroke_width=4).shift(UP * 2.4)
        fixb = VMobject(color=GRN, stroke_width=4)
        fixb.set_points_smoothly([[-5, 2.4, 0], [-3.5, 1.5, 0], [-1.2, 1.5, 0], [0, 2.4, 0]])
        merge = Dot([0, 2.4, 0], radius=0.14, color=GRN)
        self.play(Create(main), run_time=0.6)
        self.play(Create(fixb), run_time=1)
        self.play(FadeIn(merge, scale=0.5), FadeIn(txt("merged", 20, GRN).next_to(merge, UP, buff=0.15)), run_time=0.6)
        nxt = Dot([3, 2.4, 0], radius=0.12, color=BLUE)
        nl = txt("next daily pass", 20, BLUE).next_to(nxt, UP, buff=0.15)
        self.play(FadeIn(nxt, scale=0.5), FadeIn(nl), run_time=0.6)

        self.cue("The known bug now passes")
        mini = feature_map().scale(0.48).move_to(LEFT * 2.6 + DOWN * 1.0)
        mini[15][0].set_stroke(ORA, 3).set_fill(ORA, 0.2)
        self.play(FadeIn(mini), run_time=0.6)
        self.play(Indicate(mini[15], color=GRN, scale_factor=1.3), run_time=0.9)
        self.play(mini[15][0].animate.set_stroke(GRN, 3).set_fill(GRN, 0.25), run_time=0.5)

        self.cue("So the automation closes")
        issue = card("Issue #17899", ["Git name from Settings never", "reaches agent commits"], w=4.0, color=RED, title_size=24, size=20).move_to(RIGHT * 3.6 + DOWN * 0.1)
        self.play(FadeIn(issue), run_time=0.5)
        closed = chip("CLOSED", GRN, 30).rotate(0.1).move_to(issue)
        closed[0].set_fill(BG, 0.85)
        self.play(FadeIn(closed, scale=1.5), issue[0].animate.set_stroke(GREY), run_time=0.6)
        mpr = chip("map update PR", YEL, 22).next_to(issue, DOWN, buff=0.45)
        self.play(FadeIn(mpr, shift=UP * 0.2), run_time=0.6)

        self.cue("The loop is closed")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        names = ["walk the map", "notice", "fix + prove", "heal"]
        cols = [BLUE, RED, GRN, YEL]
        nodes = VGroup()
        for k, (n, c) in enumerate(zip(names, cols)):
            ang = PI / 2 - k * PI / 2
            p = 2.3 * np.array([np.cos(ang) * 1.5, np.sin(ang), 0])
            nodes.add(chip(n, c, 28).move_to(p))
        arcs = VGroup(*[CurvedArrow(nodes[k].get_center() * 0.82, nodes[(k + 1) % 4].get_center() * 0.82,
                                    angle=-PI / 3, color=GREY, stroke_width=3) for k in range(4)])
        self.play(LaggedStart(*[AnimationGroup(FadeIn(nodes[k], scale=0.8), Create(arcs[k])) for k in range(4)],
                              lag_ratio=0.45), run_time=2.2)
        self.cue("The software broke")
        for k in (1, 2, 3):
            self.play(Indicate(nodes[k], color=cols[k], scale_factor=1.15), run_time=0.7)
        self.finish()

    # ---------- 11. The safety net ----------
    def seg11(self):
        self.start(11)
        items = [("A map of promises", YEL), ("Hands on the real app", BLUE),
                 ("A walk every day", BLUE), ("Proof before and after", GRN)]
        rows = VGroup(*[VGroup(Dot(radius=0.09, color=c), txt(s, 34, INK)).arrange(RIGHT, buff=0.3)
                        for s, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        keys = ["A map of promises", "Hands that check", "A walk every day", "Proof before"]
        for r, k in zip(rows, keys):
            self.cue(k)
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.7)

        self.cue("Self-improving code")
        self.play(rows.animate.scale(0.55).to_corner(UL, buff=0.5).set_opacity(0.6), run_time=0.8)
        base_y = -2.0
        blocks = VGroup()
        for k in range(9):
            r = RoundedRectangle(width=2.6 - 0.05 * k, height=0.32, corner_radius=0.06, fill_color=BLUE,
                                 fill_opacity=0.25, stroke_color=BLUE, stroke_width=2).move_to([0.6, base_y + 0.38 * k, 0])
            blocks.add(r)
        arrow = Arrow([2.6, base_y, 0], [2.6, base_y + 3.6, 0], buff=0, color=GRN, stroke_width=6)
        fast = txt("at the speed of agents", 26, GRN).next_to(arrow, RIGHT, buff=0.25)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in blocks], lag_ratio=0.15), GrowArrow(arrow),
                  FadeIn(fast), run_time=2)

        self.cue("Self-healing is the net")
        n = net(width=7.0, y=-2.85).shift(RIGHT * 0.6)
        self.play(Create(n), run_time=1.2)
        top = blocks[-1]
        self.play(top.animate.set_stroke(RED).set_fill(RED, 0.4), run_time=0.4)
        self.play(top.animate.move_to([3.0, -2.85 + 0.15, 0]).rotate(0.5), run_time=0.9, rate_func=rush_into)
        self.play(top.animate.shift(UP * 0.5), run_time=0.35, rate_func=rush_from)
        self.play(top.animate.shift(DOWN * 0.5), run_time=0.35, rate_func=rush_into)
        self.play(top.animate.rotate(-0.5).move_to(blocks[-2].get_center() + UP * 0.38).set_stroke(BLUE).set_fill(BLUE, 0.25),
                  run_time=1.0)

        self.cue("And all of it is open source")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        name = txt("Self-Healing", 80, YEL, BOLD).shift(UP * 0.6)
        sub = txt("open source, so anyone can read it, run it, and build on it", 28, INK).next_to(name, DOWN, buff=0.45)
        tiny = net(width=6.0, y=-1.9, sag=0.3, rows=2, cols=12)
        self.play(Write(name), run_time=1.4)
        self.play(FadeIn(sub, shift=UP * 0.2), Create(tiny), run_time=1.4)
        self.finish(clear=False)
