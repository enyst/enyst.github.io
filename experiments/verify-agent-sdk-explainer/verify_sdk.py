"""Explainer video: verifying the OpenHands agent SDK.

Render: manim -qh verify_sdk.py VerifySDK
Numbers come from software-agent-sdk PR #5621 (.pr/verify-agent-server-replay.md,
feature-map/README.md) and umbrella issue #5653, as of 2026-10-11.
"""

from manim import *

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


def prose(s, size=34, color=WHITE, **kw):
    return Text(s, font=SERIF, font_size=size, color=color, **kw)


def label(s, size=26, color=GREY_3B, **kw):
    return Text(s, font=SANS, font_size=size, color=color, **kw)


class Counter(VGroup):
    """Integer display without LaTeX: a Text that tracks a ValueTracker."""

    def __init__(self, value=0, font_size=48, color=WHITE, anchor=LEFT):
        super().__init__()
        self.tracker = ValueTracker(value)
        self.font_size_ = font_size
        self.color_ = color
        self.anchor = anchor
        self.text = self._make()
        self.add(self.text)
        self.add_updater(lambda m: m._refresh())

    def _make(self):
        return Text(str(int(round(self.tracker.get_value()))), font=SANS,
                    font_size=self.font_size_, color=self.color_, weight=BOLD)

    def _refresh(self):
        new = self._make()
        if self.anchor is None:
            new.move_to(self.text)
        else:
            new.move_to(self.text, aligned_edge=self.anchor)
        self.text.become(new)

    def count_to(self, n, **kw):
        return self.tracker.animate(**kw).set_value(n)


def code_block(lines, size=20, width=None):
    """A terminal-like block. Lines starting with '#' are comments; a trailing
    '# bug' is highlighted in red."""
    rows = VGroup()
    for line in lines:
        if line.strip().startswith("#"):
            t = Text(line, font=MONO, font_size=size, color=GREY_3B)
        elif line.endswith("# bug"):
            head = Text(line[:-5], font=MONO, font_size=size, color=WHITE)
            tail = Text("# bug", font=MONO, font_size=size, color=RED_3B, weight=BOLD)
            t = VGroup(head, tail).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        else:
            parts = line.split(" ", 1)
            head = Text(parts[0], font=MONO, font_size=size, color=BLUE_3B)
            if len(parts) > 1:
                tail = Text(parts[1], font=MONO, font_size=size, color=WHITE)
                t = VGroup(head, tail).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
            else:
                t = head
        rows.add(t)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    for line, t in zip(lines, rows):
        indent = len(line) - len(line.lstrip(" "))
        if indent:
            t.shift(RIGHT * indent * size * 0.0105)
    box = SurroundingRectangle(
        rows, buff=0.35, corner_radius=0.12, color="#2A2F3A", fill_color="#181B22", fill_opacity=1
    )
    if width:
        box.stretch_to_fit_width(width).align_to(rows, LEFT).shift(LEFT * 0.35)
    return VGroup(box, rows)


class VerifySDK(Scene):
    def clear_scene(self, run_time=0.8):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    def construct(self):
        import json
        marks = []
        for name in ["opening", "idea", "map_numbers", "map_example", "cli_commands",
                     "recipe", "the_run", "bugs", "closing"]:
            marks.append((name, self.renderer.time))
            getattr(self, name)()
        marks.append(("end", self.renderer.time))
        with open("scene_times.json", "w") as f:
            json.dump(marks, f)

    # 1 -------------------------------------------------------------------
    def opening(self):
        q = prose("What does an agent actually see", size=46)
        q2 = prose("when it uses the OpenHands SDK?", size=46)
        g = VGroup(q, q2).arrange(DOWN, buff=0.25)
        self.play(Write(q), run_time=1.6)
        self.play(Write(q2), run_time=1.4)
        self.wait(1.2)
        sub = label("Not what a handler returned. Not that CI passed.", size=28)
        sub.next_to(g, DOWN, buff=0.7)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(sub), g.animate.scale(0.6).to_edge(UP))
        title = prose("Verifying the agent SDK", size=60, color=YELLOW_3B)
        self.play(FadeTransform(g, title))
        repo = label("OpenHands / software-agent-sdk", size=26).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(repo))
        self.wait(1.5)
        self.clear_scene()

    # 2 -------------------------------------------------------------------
    def idea(self):
        head = prose("The idea", size=48, color=YELLOW_3B).to_edge(UP, buff=0.6)
        self.play(Write(head))

        def node(text, sub, color):
            c = Circle(radius=1.05, color=color, stroke_width=5)
            t = prose(text, size=34, color=color).move_to(c)
            s = label(sub, size=20).next_to(c, DOWN, buff=0.3)
            return VGroup(c, t, s)

        m = node("Map", "every agent-facing\nbehavior, with IDs", BLUE_3B)
        cli = node("CLI", "one command\nper API step", GREEN_3B)
        ev = node("Evidence", "saved exchanges\nand a ledger", TEAL_3B)
        ev[1].scale(0.8)
        row = VGroup(m, cli, ev).arrange(RIGHT, buff=1.6).shift(DOWN * 0.75)
        for n in row:
            self.play(Create(n[0]), Write(n[1]), FadeIn(n[2]), run_time=0.9)
        a1 = Arrow(m[0].get_right(), cli[0].get_left(), buff=0.15, color=WHITE)
        a2 = Arrow(cli[0].get_right(), ev[0].get_left(), buff=0.15, color=WHITE)
        self.play(GrowArrow(a1), GrowArrow(a2))
        back = CurvedArrow(
            ev[0].get_top() + UP * 0.05, m[0].get_top() + UP * 0.05, angle=TAU / 8, color=YELLOW_3B
        )
        back_lbl = label("a fix flips a known bug to a pass", size=20, color=YELLOW_3B)
        back_lbl.next_to(back, UP, buff=0.1)
        self.play(Create(back), FadeIn(back_lbl))
        self.wait(1.0)
        note = prose("A real server, a real model, driven the way an agent drives it.", size=28)
        note.to_edge(DOWN, buff=0.35)
        self.play(Write(note), run_time=1.8)
        self.wait(2.2)
        self.clear_scene()

    # 3 -------------------------------------------------------------------
    def map_numbers(self):
        head = prose("The feature map, in numbers", size=44, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(head))

        grid = VGroup(
            *[
                RoundedRectangle(width=0.62, height=0.62, corner_radius=0.08,
                                 stroke_color=BLUE_3B, stroke_width=2,
                                 fill_color=BLUE_3B, fill_opacity=0.15)
                for _ in range(34)
            ]
        ).arrange_in_grid(rows=5, cols=7, buff=0.14)
        for i, sq in enumerate(grid):
            sq.add(Text(f"F{i + 1:02d}", font=MONO, font_size=14, color=BLUE_3B).move_to(sq))
        grid.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in grid], lag_ratio=0.04), run_time=2.2)

        def stat(n, text, color):
            num = Counter(n, font_size=58, color=color)
            t = label(text, size=24, color=WHITE)
            return VGroup(num, t).arrange(RIGHT, buff=0.35, aligned_edge=DOWN), n

        s1, n1 = stat(34, "families of behavior", BLUE_3B)
        s2, n2 = stat(931, "sub-features with stable IDs", GREEN_3B)
        s3, n3 = stat(193, "of 203 routes driven live", TEAL_3B)
        stats = VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        stats.next_to(grid, RIGHT, buff=0.9)
        for s, n in [(s1, n1), (s2, n2), (s3, n3)]:
            s[0].tracker.set_value(0)
            s[0].update()
            self.add(s[0])
            self.play(FadeIn(s[1]), s[0].count_to(n), run_time=1.3)
        foot = label("10 routes excluded, each with a written reason", size=20)
        foot.next_to(stats, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(FadeIn(foot))
        self.wait(1.5)

        # names of a few families
        names = [
            (1, "server status"), (5, "run, pause, interrupt"), (13, "bash"),
            (18, "settings and secrets"), (19, "MCP"), (25, "skills"), (34, "TypeScript client"),
        ]
        for idx, nm in names:
            sq = grid[idx - 1]
            tag = label(nm, size=18, color=YELLOW_3B).next_to(grid, DOWN, buff=0.25)
            self.play(sq.animate.set_fill(YELLOW_3B, 0.5), FadeIn(tag), run_time=0.3)
            self.play(FadeOut(tag), run_time=0.25)
        caption = prose("REST, WebSocket, SDK client and TypeScript client: one map.", size=26)
        caption.to_edge(DOWN, buff=0.45)
        self.play(Write(caption), run_time=1.5)
        self.wait(1.2)

        sdk = label("Next: a map for the in-process SDK, 21 families, being drafted now",
                    size=22, color=YELLOW_3B)
        sdk.move_to(caption)
        self.play(FadeOut(caption), run_time=0.5)
        self.play(FadeIn(sdk, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()

    # 4 -------------------------------------------------------------------
    def map_example(self):
        head = prose("Example: entry F06", size=44, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(head))
        fam = label("F06  ·  Conversation events", size=28, color=BLUE_3B)
        fam.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(fam, shift=RIGHT * 0.2))

        rows = [
            ("Sub-features", "F06.search-kind-short  ·  F06.ws-delete-close  ·  ..."),
            ("How to get to it", "GET /api/conversations/{id}/events/search"),
            ("Driving it", "exact control-agent-server commands"),
            ("Gotchas", "what fooled the last agent who tried"),
        ]
        items = VGroup()
        for k, v in rows:
            kk = Text(k, font=SANS, font_size=24, color=GREEN_3B, weight=SEMIBOLD)
            vv = Text(v, font=MONO if "/" in v or "." in v else SANS, font_size=21, color=WHITE)
            items.add(VGroup(kk, vv).arrange(RIGHT, buff=0.5))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(fam, DOWN, buff=0.55, aligned_edge=LEFT)
        keys = VGroup(*[i[0] for i in items])
        for it in items:
            it[1].align_to(keys.get_right() + RIGHT * 0.5, LEFT)
        for it in items:
            self.play(FadeIn(it[0]), Write(it[1]), run_time=0.9)
        self.wait(1.0)
        rule = prose("Each sub-feature is proved by a second, read-only view.", size=26, color=GREY_3B)
        rule.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(rule))
        self.wait(2.2)
        self.clear_scene()

    # 5 -------------------------------------------------------------------
    def cli_commands(self):
        head = prose("The CLI: control-agent-server", size=44, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(head))
        steps = ["launch", "doctor", "drive", "evidence", "stop"]
        dots = VGroup(*[label(s, size=24, color=WHITE) for s in steps]).arrange(RIGHT, buff=0.9)
        dots.next_to(head, DOWN, buff=0.45)
        arrows = VGroup(*[
            Arrow(dots[i].get_right(), dots[i + 1].get_left(), buff=0.1, stroke_width=3,
                  max_tip_length_to_length_ratio=0.25, color=GREY_3B)
            for i in range(len(steps) - 1)
        ])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15), Create(arrows))

        lines = [
            "control-agent-server launch --new --print-run",
            "control-agent-server doctor",
            "control-agent-server llm preset deepseek",
            "control-agent-server conversation start --prompt 'Create hello.txt' --wait",
            "control-agent-server api GET /api/conversations/$CID --expect 200",
            "control-agent-server evidence add --feature F03.get --result pass",
            "control-agent-server stop",
        ]
        block = code_block(lines, size=19).next_to(dots, DOWN, buff=0.5)
        self.play(FadeIn(block[0]))
        highlight_for = [0, 1, 2, 2, 2, 3, 4]
        for i, row in enumerate(block[1]):
            self.play(
                AddTextLetterByLetter(row, time_per_char=0.012) if not isinstance(row, VGroup)
                else FadeIn(row, shift=RIGHT * 0.15),
                dots.animate.set_color(WHITE),
                run_time=0.6,
            )
            self.play(dots[highlight_for[i]].animate.set_color(YELLOW_3B), run_time=0.2)
        self.wait(0.8)
        note = label("Every command prints one JSON object. Exit 0 ok, 1 failed, 2 usage, 3 environment.",
                     size=20)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(2.2)
        self.clear_scene()

    # 6 -------------------------------------------------------------------
    def recipe(self):
        head = prose("Example: a recipe that caught a bug", size=44, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(head))
        idl = label("F06.search-kind-short", size=24, color=BLUE_3B).next_to(head, DOWN, buff=0.35)
        self.play(FadeIn(idl))
        lines = [
            "# the full class path finds both messages",
            "control-agent-server api GET .../events/search \\",
            "    --query kind=openhands.sdk.event...MessageEvent --check items len-eq 2",
            "# the short name the docs and TS client use",
            "control-agent-server api GET .../events/search \\",
            "    --query kind=MessageEvent --check items len-eq 2  # bug",
        ]
        block = code_block(lines, size=19).next_to(idl, DOWN, buff=0.45)
        self.play(FadeIn(block[0]))
        for row in block[1]:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.55)
        self.wait(0.8)

        exp = VGroup(
            label("expected", size=22, color=GREEN_3B), Text("2 messages", font=MONO, font_size=22),
        ).arrange(RIGHT, buff=0.3)
        got = VGroup(
            label("today", size=22, color=RED_3B), Text("items: []", font=MONO, font_size=22),
        ).arrange(RIGHT, buff=0.3)
        res = VGroup(exp, got).arrange(RIGHT, buff=1.4).next_to(block, DOWN, buff=0.5)
        self.play(FadeIn(exp))
        self.play(FadeIn(got))
        self.wait(1.0)
        issue = label("Filed as #5631. When it is fixed, this line reports an unexpected pass.",
                      size=21, color=WHITE).to_edge(DOWN, buff=0.35)
        self.play(Write(issue), run_time=1.4)
        self.wait(2.2)
        self.clear_scene()

    # 7 -------------------------------------------------------------------
    def the_run(self):
        head = prose("Then we ran all of it", size=46, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(head))
        cmd = code_block(["control-agent-server map run --all --fresh --keep-going --record"], size=21)
        cmd.next_to(head, DOWN, buff=0.45)
        self.play(FadeIn(cmd))
        sub = label("34 families, each on its own fresh server, with a real model", size=22)
        sub.next_to(cmd, DOWN, buff=0.3)
        self.play(FadeIn(sub))

        total = 771 + 156 + 6
        bar_w = 11.0
        y = DOWN * 1.0
        parts = [(771, GREEN_3B, "pass"), (156, RED_3B, "known bug reproduced"), (6, GREY_3B, "blocked")]
        segs = VGroup()
        for n, col, _ in parts:
            segs.add(Rectangle(width=max(bar_w * n / total, 0.08), height=0.8,
                               fill_color=col, fill_opacity=0.85, stroke_width=0))
        segs.arrange(RIGHT, buff=0.03).move_to(y)
        for s in segs:
            self.play(GrowFromEdge(s, LEFT), run_time=0.9)
        nums = VGroup()
        for (n, col, txt), s, d in zip(parts, segs, [UP, DOWN, UP]):
            num = Text(str(n), font=SANS, font_size=40, color=col, weight=BOLD)
            t = label(txt, size=20, color=col)
            g = VGroup(num, t).arrange(DOWN, buff=0.1)
            g.next_to(s, d, buff=0.25)
            nums.add(g)
        nums[2].shift(RIGHT * 0.4)
        self.play(LaggedStart(*[FadeIn(g) for g in nums], lag_ratio=0.3))
        verdict = prose("No failures. No unexpected passes.", size=30, color=WHITE).to_edge(DOWN, buff=0.45)
        self.play(Write(verdict))
        self.wait(1.0)
        blk = label("Blocked = needs Docker, a GitHub token, VS Code server or a human sign-in",
                    size=18).next_to(verdict, UP, buff=0.25)
        self.play(FadeIn(blk))
        self.wait(2.4)
        self.clear_scene()

    # 8 -------------------------------------------------------------------
    def bugs(self):
        head = prose("And what it found", size=46, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(head))

        big = Counter(0, font_size=140, color=RED_3B, anchor=None).shift(UP * 0.4)
        self.add(big)
        cap = prose("new bugs filed or fixed", size=30).next_to(big, DOWN, buff=0.3)
        self.play(big.count_to(35), run_time=2.2, rate_func=smooth)
        big.clear_updaters()
        self.play(FadeIn(cap))
        self.wait(0.8)

        parts = VGroup(
            VGroup(Text('31', font=SANS, font_size=38, color=RED_3B, weight=BOLD), label("issues filed (1 high, 30 medium)", 22, WHITE)),
            VGroup(Text('4', font=SANS, font_size=38, color=YELLOW_3B, weight=BOLD), label("security fixes, as their own PRs", 22, WHITE)),
            VGroup(Text('6', font=SANS, font_size=38, color=BLUE_3B, weight=BOLD), label("known issues reproduced on demand", 22, WHITE)),
            VGroup(Text('116', font=SANS, font_size=38, color=ORANGE_3B, weight=BOLD), label("low-severity bugs, kept as known-bug checks", 22, WHITE)),
        )
        for p in parts:
            p.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(VGroup(big, cap).animate.scale(0.7).to_edge(LEFT, buff=0.8).shift(UP * 0.3))
        parts.next_to(VGroup(big, cap), RIGHT, buff=0.7)
        if parts.get_right()[0] > config.frame_width / 2 - 0.4:
            parts.scale((config.frame_width / 2 - 0.4 - parts.get_left()[0]) / parts.width, about_edge=LEFT)
        parts[2:].shift(DOWN * 0.35)
        also = label("also", size=18).next_to(parts[2], UP, aligned_edge=LEFT, buff=0.12)
        rule = Line(parts.get_left(), parts.get_left() + RIGHT * parts.width, stroke_width=1.5,
                    color=GREY_3B).move_to(also.get_top() + UP * 0.12, aligned_edge=LEFT)
        for p in parts[:2]:
            self.play(FadeIn(p, shift=LEFT * 0.2), run_time=0.7)
        self.play(Create(rule), FadeIn(also), run_time=0.5)
        for p in parts[2:]:
            self.play(FadeIn(p, shift=LEFT * 0.2), run_time=0.7)
        self.wait(1.0)
        foot = label("Umbrella issue #5653 tracks them. Two are already fixed on main (#5514, #5623).",
                     size=21).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(foot))
        self.wait(3.0)
        self.clear_scene()

    # 9 -------------------------------------------------------------------
    def closing(self):
        l1 = prose("A map anyone can rerun,", size=44)
        l2 = prose("in the open.", size=44, color=YELLOW_3B)
        g = VGroup(l1, l2).arrange(DOWN, buff=0.3)
        self.play(Write(l1), run_time=1.4)
        self.play(Write(l2), run_time=1.0)
        self.wait(1.0)
        nxt = label("Next: the core SDK map, and a daily replay so regressions surface on their own.",
                    size=22).next_to(g, DOWN, buff=0.8)
        self.play(FadeIn(nxt, shift=UP * 0.2))
        src = label("github.com/OpenHands/software-agent-sdk  ·  PR #5621  ·  issue #5653",
                    size=18).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(src))
        self.wait(3.0)
        self.clear_scene(run_time=1.2)
