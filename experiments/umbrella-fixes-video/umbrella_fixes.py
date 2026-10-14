"""Video: the umbrella fixes (OpenHands agent SDK, issue #5653).

Render (after `python narration.py` has written voice/durations.json):
    manim -r 1920,1080 --fps 30 umbrella_fixes.py UmbrellaFixes
Then `python music.py` and `sh mix.sh`.

Each scene lasts as long as its narration; `self.cue(phrase)` waits until the
narrator reaches that phrase (estimated from its position in the text).
Facts come from /mnt/project-files/notes/umbrella-fixes/final-report.md and the
PR descriptions and diffs on OpenHands/software-agent-sdk, as of 2026-10-14.
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

DURATIONS = json.load(open("voice/durations.json"))
GAP = 0.9  # silence between scenes


def prose(s, size=34, color=WHITE, **kw):
    return Text(s, font=SERIF, font_size=size, color=color, **kw)


def label(s, size=26, color=GREY_3B, **kw):
    return Text(s, font=SANS, font_size=size, color=color, **kw)


def wrap(s, width):
    return "\n".join(textwrap.wrap(s, width))


def para(s, width=60, size=22, color=WHITE, font=SANS):
    return Text(wrap(s, width), font=font, font_size=size, color=color, line_spacing=0.9)


def card(content, buff=0.4, edge=CARD_EDGE):
    box = SurroundingRectangle(content, buff=buff, corner_radius=0.14, color=edge,
                               fill_color=CARD_BG, fill_opacity=1, stroke_width=2)
    return VGroup(box, content)


def code(lines, size=19):
    """Monospace block. Diff lines: '+' green, '-' red; '#' comments grey;
    a trailing '# bug: ...' predicate is drawn in red."""
    char_w = Text("M" * 20, font=MONO, font_size=size).width / 20
    is_diff = any(line[:1] in "+-" for line in lines)
    rows = VGroup()
    for line in lines:
        prefix, body = (line[0], line[1:]) if is_diff else ("", line)
        indent = len(body) - len(body.lstrip(" "))
        body = body.strip()
        color = {"+": GREEN_3B, "-": RED_3B}.get(prefix, WHITE)
        if "# bug" in body:
            i = body.index("# bug")
            parts = [Text(x, font=MONO, font_size=size, color=c, weight=w)
                     for x, c, w in [(body[:i].rstrip(), WHITE, NORMAL), (body[i:], RED_3B, BOLD)] if x]
            t = VGroup(*parts).arrange(RIGHT, buff=char_w, aligned_edge=DOWN)
        elif body.startswith("#"):
            t = Text(body, font=MONO, font_size=size, color=GREY_3B)
        else:
            t = Text(body or ".", font=MONO, font_size=size, color=color)
            if not body:
                t.set_opacity(0)
        row = VGroup()
        if is_diff:
            row.add(Text(prefix if prefix.strip() else ".", font=MONO, font_size=size, color=color))
            if not prefix.strip():
                row[0].set_opacity(0)
        row.add(t)
        row.indent = indent
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    x0 = rows.get_left()[0]
    for row in rows:
        if is_diff:
            row[0].set_x(x0 + char_w / 2)
        row[-1].align_to(np.array([x0 + (2 * char_w if is_diff else 0) + row.indent * char_w, 0, 0]), LEFT)
    return card(rows, buff=0.3)


def pill(text, color, size=20):
    t = label(text, size=size, color=color, weight=SEMIBOLD)
    r = RoundedRectangle(width=t.width + 0.45, height=t.height + 0.3, corner_radius=0.2,
                         stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
    return VGroup(r, t.move_to(r))


def decision_card(question, implemented, alternative, width=58, extra=None, size=21):
    """The "Decision needed" section of a PR description, as a card."""
    head = Text("Decision needed", font=SANS, font_size=30, color=YELLOW_3B, weight=BOLD)
    rule = Line(LEFT, RIGHT, stroke_width=1.5, color=GREY_3B)
    q = para(question, width=width + 6, size=size, color=WHITE)
    imp_tag = label("Implemented", size=size, color=GREEN_3B, weight=BOLD)
    imp = para(implemented, width=width, size=size)
    alt_tag = label("Alternative", size=size, color=ORANGE_3B, weight=BOLD)
    alt = para(alternative, width=width, size=size, color="#D7D9DE")
    imp_row = VGroup(imp_tag, imp).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    alt_row = VGroup(alt_tag, alt).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    parts = [head, rule, q, imp_row, alt_row]
    if extra is not None:
        parts.append(extra)
    body = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    rest = VGroup(*[p for p in parts if p is not rule])
    rule.set_width(rest.width).align_to(head, LEFT)
    c = card(body, buff=0.4, edge=YELLOW_3B)
    if c.width > 13.2:
        c.scale_to_fit_width(13.2)
    c.imp, c.alt, c.q, c.head = imp_row, alt_row, q, head
    return c


class UmbrellaFixes(Scene):
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

    def finish(self):
        now = self.renderer.time - self.scene_start
        rest = DURATIONS[self.scene_name] + GAP - 0.8 - now
        if rest > 0.05:
            self.wait(rest)
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def construct(self):
        marks = []
        for name in SCENES:
            self.scene_name = name
            self.scene_start = self.renderer.time
            marks.append((name, self.scene_start))
            getattr(self, name)()
            self.finish()
        marks.append(("end", self.renderer.time))
        with open("scene_times.json", "w") as f:
            json.dump(marks, f)

    def title(self, s, size=42):
        h = prose(s, size=size, color=YELLOW_3B).to_edge(UP, buff=0.5)
        self.play(Write(h), run_time=1.0)
        return h

    # 1 -------------------------------------------------------------------
    def opening(self):
        t1 = prose("Verify everything,", size=58)
        t2 = prose("thus fix everything.", size=58, color=YELLOW_3B)
        g = VGroup(t1, t2).arrange(DOWN, buff=0.3).shift(UP * 0.4)
        self.play(Write(t1), run_time=1.3)
        self.play(Write(t2), run_time=1.3)
        sub = label("The umbrella fixes  ·  OpenHands agent SDK  ·  issue #5653", size=24)
        sub.next_to(g, DOWN, buff=0.6)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.cue("It found")
        self.play(g.animate.scale(0.55).to_edge(UP, buff=0.5), FadeOut(sub))
        dots = VGroup(*[Dot(radius=0.07, color=RED_3B) for _ in range(128)])
        dots.arrange_in_grid(rows=4, cols=32, buff=0.22).shift(DOWN * 0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.02), run_time=2.0)
        self.cue("every one of them fixed")
        self.play(LaggedStart(*[d.animate.set_color(GREEN_3B) for d in dots], lag_ratio=0.015),
                  run_time=3.0)

    # 2 -------------------------------------------------------------------
    def method(self):
        head = self.title("The method")

        def node(text, sub, color):
            c = Circle(radius=1.0, color=color, stroke_width=5)
            t = prose(text, size=32, color=color).move_to(c)
            s = label(sub, size=20).next_to(c, DOWN, buff=0.3)
            return VGroup(c, t, s)

        m = node("Map", "34 families\n931 sub-features", BLUE_3B)
        cli = node("CLI", "control-agent-server\none step at a time", GREEN_3B)
        fix = node("Fix", "verify everything,\nthus fix everything", YELLOW_3B)
        row = VGroup(m, cli, fix).arrange(RIGHT, buff=1.7).shift(DOWN * 0.4)
        a1 = Arrow(m[0].get_right(), cli[0].get_left(), buff=0.15, color=WHITE)
        a2 = Arrow(cli[0].get_right(), fix[0].get_left(), buff=0.15, color=WHITE)
        self.cue("The feature map")
        self.play(Create(m[0]), Write(m[1]), FadeIn(m[2]), run_time=1.0)
        self.cue("The command line tool")
        self.play(GrowArrow(a1), Create(cli[0]), Write(cli[1]), FadeIn(cli[2]), run_time=1.0)
        self.cue("Verify everything")
        self.play(GrowArrow(a2), Create(fix[0]), Write(fix[1]), FadeIn(fix[2]), run_time=1.0)
        self.cue("Because once")
        back = CurvedArrow(fix[0].get_top() + UP * 0.05, m[0].get_top() + UP * 0.05,
                           angle=TAU / 8, color=YELLOW_3B)
        self.play(Create(back), run_time=1.2)

    # 3 -------------------------------------------------------------------
    def proof(self):
        head = self.title("How a fix is proven")
        line = code([
            "control-agent-server api POST .../events --save F27.subagents-bad-skill/send \\",
            "    # bug: status eq 500 && body.exception contains 'not found'",
        ], size=18)
        line.next_to(head, DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.2))
        pred = line[1][1]
        self.play(Indicate(pred, color=RED_3B, scale_factor=1.04))

        def runs(where, res, color, sub):
            name = label(where, size=26, color=WHITE, weight=SEMIBOLD)
            r = VGroup(*[pill(x, color) for x in res]).arrange(RIGHT, buff=0.25)
            s = label(sub, size=18)
            return VGroup(name, r, s).arrange(DOWN, buff=0.25)

        main = runs("main", ["xfail", "xfail"], RED_3B, "fails exactly as predicted")
        branch = runs("fix branch", ["xpass", "xpass"], GREEN_3B, "the predicate no longer holds")
        done = runs("marker removed", ["pass"], BLUE_3B, "an ordinary check from now on")
        steps = VGroup(main, branch, done).arrange(RIGHT, buff=1.2).shift(DOWN * 1.2)
        arrows = VGroup(
            Arrow(main.get_right(), branch.get_left(), buff=0.2, color=GREY_3B),
            Arrow(branch.get_right(), done.get_left(), buff=0.2, color=GREY_3B),
        )
        self.cue("On main")
        self.play(FadeIn(main, shift=UP * 0.2))
        self.cue("On the fix branch")
        self.play(GrowArrow(arrows[0]), FadeIn(branch, shift=UP * 0.2))
        self.cue("Only then")
        strike = Line(pred.get_left(), pred.get_right(), color=WHITE, stroke_width=3)
        self.play(Create(strike), pred.animate.set_opacity(0.35))
        self.play(GrowArrow(arrows[1]), FadeIn(done, shift=UP * 0.2))

    # 4 -------------------------------------------------------------------
    def numbers(self):
        head = self.title("The work")
        groups = [
            (13, RED_3B, "medium bugs", "Thirteen medium"),
            (14, ORANGE_3B, "mediums with a contributor PR, fixed independently", "Fourteen more"),
            (8, PURPLE_3B, "older reports the umbrella lists", "Eight older"),
            (93, BLUE_3B, "low-severity bugs, each with its own issue first", "ninety-three"),
        ]
        grid = VGroup(*[Square(0.34, stroke_width=1.5, stroke_color=GREY_3B, fill_opacity=0)
                        for _ in range(128)])
        grid.arrange_in_grid(rows=8, cols=16, buff=0.08).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        self.play(FadeIn(grid), run_time=0.6)
        legend = VGroup()
        k = 0
        for n, color, text, phrase in groups:
            self.cue(phrase)
            sq = grid[k:k + n]
            k += n
            num = Text(str(n), font=SANS, font_size=34, color=color, weight=BOLD)
            t = label(wrap(text, 30), size=20, color=WHITE)
            row = VGroup(num, t).arrange(RIGHT, buff=0.3)
            legend.add(row)
            legend.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(grid, RIGHT, buff=0.8)
            for r in legend[:-1]:
                r[0].align_to(legend, LEFT)
            self.play(sq.animate.set_fill(color, 0.75).set_stroke(color),
                      FadeIn(row, shift=LEFT * 0.2),
                      run_time=1.0 if n > 10 else 0.7)
        for r in legend:
            r[0].align_to(legend, LEFT)
        self.cue("In all")
        self.play(FadeOut(legend), run_time=0.5)
        big = Text("126", font=SANS, font_size=120, color=WHITE, weight=BOLD)
        cap = prose("pull requests, one per bug", size=30)
        tot = VGroup(big, cap).arrange(DOWN, buff=0.2).next_to(grid, RIGHT, buff=1.2)
        self.play(FadeIn(tot, scale=0.8))
        self.cue("Two are already merged")
        p1 = pill("2 merged", PURPLE_3B, 22)
        p2 = pill("124 green and ready for review", GREEN_3B, 22)
        ps = VGroup(p1, p2).arrange(DOWN, buff=0.25).next_to(tot, DOWN, buff=0.45)
        self.play(FadeIn(p1, shift=UP * 0.2))
        self.cue("The rest")
        self.play(FadeIn(p2, shift=UP * 0.2), grid.animate.set_fill(GREEN_3B, 0.75).set_stroke(GREEN_3B))

    # 5 -------------------------------------------------------------------
    def subagent(self):
        head = self.title("A sub-agent naming a missing skill")
        badge = pill("#5754  ·  merged", PURPLE_3B, 20).next_to(head, DOWN, buff=0.3)
        self.play(FadeIn(badge))
        bug = VGroup(
            label("first message", size=22, color=WHITE),
            Arrow(LEFT, RIGHT, color=GREY_3B).scale(0.6),
            Text("500 Internal Server Error", font=MONO, font_size=22, color=RED_3B),
        ).arrange(RIGHT, buff=0.3).next_to(badge, DOWN, buff=0.5)
        self.cue("made the very first")
        self.play(FadeIn(bug, shift=RIGHT * 0.2))
        self.cue("The fix wraps")
        snippet = code([
            "+def _register_definition(agent_def, work_dir, kind) -> bool:",
            "+    try:",
            "+        factory = agent_definition_to_factory(agent_def, work_dir=work_dir)",
            "+    except ValueError as e:",
            "+        logger.warning(f\"Skipping {kind} agent '{agent_def.name}': {e}\")",
            "+        return False",
            "+    return register_agent_if_absent(name=agent_def.name, ...)",
        ], size=18)
        snippet.next_to(bug, DOWN, buff=0.5)
        self.play(FadeIn(snippet[0]))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in snippet[1]], lag_ratio=0.3),
                  run_time=2.2)
        self.cue("everything else keeps working")
        self.play(Indicate(snippet[1][3:6], color=YELLOW_3B, scale_factor=1.03))

    # 6 -------------------------------------------------------------------
    def decision(self):
        dc = decision_card(
            "Scope relative to the broader issue \"Plugin or skill loading error should not "
            "prevent conversation from starting\". Its triage asks whether it absorbs #5630.",
            "#5630 is kept separate. This PR fixes only sub-agent registration, for file-based "
            "and plugin-provided definitions, as #5630's triage scoped.",
            "fold #5630 into the broader issue. That widens this PR to plugin loading and "
            "possibly a new client-facing notice (server models, TypeScript client, UI).",
            width=64, size=21,
        ).move_to(ORIGIN)
        src = label("from the description of PR #5754", size=18).next_to(dc, DOWN, buff=0.25)
        self.play(FadeIn(dc[0]), Write(dc.head), run_time=1.0)
        self.cue("The issue's triage")
        self.play(FadeIn(dc.q), FadeIn(src))
        self.cue("Decision needed")
        self.play(Indicate(dc.head, color=YELLOW_3B))
        self.cue("what was implemented")
        self.play(FadeIn(dc.imp, shift=RIGHT * 0.2))
        self.cue("and the alternative")
        self.play(FadeIn(dc.alt, shift=RIGHT * 0.2))
        self.cue("Here, the recommended")
        check = pill("recommended option, implemented", GREEN_3B, 18)
        check.next_to(dc.imp[0], RIGHT, buff=0.4)
        self.play(FadeIn(check, scale=0.8), dc.imp.animate.set_color(GREEN_3B).set_opacity(1))
        self.cue("The maintainer still")
        self.play(Circumscribe(dc.alt, color=ORANGE_3B, time_width=0.6), run_time=1.6)

    # 7 -------------------------------------------------------------------
    def freeze(self):
        head = self.title("A failed run froze the server")
        badge = pill("#5780  ·  fixes #5633", GREEN_3B, 20).next_to(head, DOWN, buff=0.3)
        self.play(FadeIn(badge))
        line = code([
            "control-agent-server assert --value \"$SLOWEST\" --check . le 1500  # bug: value ge 3000",
        ], size=18).next_to(badge, DOWN, buff=0.4)
        self.cue("The map")
        self.play(FadeIn(line, shift=UP * 0.2))

        ax = Axes(x_range=[0, 4, 1], y_range=[0, 5000, 1000], x_length=7, y_length=3.4,
                  axis_config={"color": GREY_3B, "include_ticks": False},
                  y_axis_config={"include_ticks": True}).shift(DOWN * 1.5)
        ylab = label("slowest probe, ms", size=18).next_to(ax.y_axis, UP, buff=0.15)
        thr = DashedLine(ax.c2p(0, 1500), ax.c2p(4, 1500), color=YELLOW_3B, stroke_width=2)
        thr_l = label("1500 ms", size=16, color=YELLOW_3B).next_to(thr, RIGHT, buff=0.1)
        self.play(Create(ax), FadeIn(ylab), Create(thr), FadeIn(thr_l), run_time=1.0)
        data = [(0.6, 4540, RED_3B), (1.4, 4791, RED_3B), (2.6, 142, GREEN_3B), (3.4, 93, GREEN_3B)]
        bars = VGroup()
        nums = VGroup()
        for x, v, c in data:
            b = Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.03),
                          fill_color=c, fill_opacity=0.85, stroke_width=0)
            b.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            bars.add(b)
            nums.add(label(f"{v}", size=18, color=c).next_to(b, UP, buff=0.08))
        lm = label("main", size=20, color=WHITE).next_to(VGroup(bars[0], bars[1]), DOWN, buff=0.2)
        lb = label("fix branch", size=20, color=WHITE).next_to(VGroup(bars[2], bars[3]), DOWN, buff=0.2)
        self.cue("On main")
        self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(nums[:2]),
                  FadeIn(lm), run_time=1.4)
        self.cue("On the fix branch")
        self.play(GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN), FadeIn(nums[2:]),
                  FadeIn(lb), run_time=1.0)

    # 8 -------------------------------------------------------------------
    def freeze_fix(self):
        head = self.title("One log line")
        snippet = code([
            "-    logger.exception(\"Error during conversation run\")",
            "+    logger.error(",
            "+        \"Error during conversation run\\n%s\",",
            "+        \"\".join(traceback.format_exception(exc)).rstrip(),",
            "+    )",
        ], size=20).next_to(head, DOWN, buff=0.45)
        self.play(FadeIn(snippet[0]), FadeIn(snippet[1][0]))
        self.cue("The fix logs")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in snippet[1][1:]], lag_ratio=0.3))
        self.cue("Again there was")
        dc = decision_card(
            "How should the run-failure log keep its traceback without blocking the loop?",
            "plain-text traceback at ERROR, no exc_info. Same detail; the console loses "
            "Rich's panel.",
            "(a) one-line ERROR, traceback at DEBUG. (b) a QueueHandler around the console "
            "handler: keeps Rich, changes logging for every SDK user.",
            width=76, size=19,
            extra=para("Tried and rejected: moving the call to a thread. Probes still took "
                       "about 5 s, because every log call waits on the handler's lock.",
                       width=82, size=19, color=TEAL_3B),
        )
        self.play(snippet.animate.scale(0.85).next_to(head, DOWN, buff=0.3), run_time=0.6)
        dc.scale_to_fit_height(min(dc.height, 4.0)).next_to(snippet, DOWN, buff=0.3)
        self.play(FadeIn(dc[0]), FadeIn(dc[1][:4]))
        self.cue("or a logging queue")
        self.play(FadeIn(dc.alt))
        self.cue("It even records")
        self.play(FadeIn(dc[1][5], shift=UP * 0.15))

    # 9 -------------------------------------------------------------------
    def sockets(self):
        head = self.title("Silent sockets after a delete")
        badge = pill("#5757  ·  fixes #5635", GREEN_3B, 20).next_to(head, DOWN, buff=0.3)
        self.play(FadeIn(badge))
        y_c, y_s = 0.6, -1.0
        client = label("client", size=22, color=WHITE).move_to(LEFT * 6 + UP * y_c)
        server = label("server", size=22, color=WHITE).move_to(LEFT * 6 + UP * y_s)
        lc = Line(LEFT * 5.2 + UP * y_c, RIGHT * 6 + UP * y_c, color=GREY_3B)
        ls = Line(LEFT * 5.2 + UP * y_s, RIGHT * 6 + UP * y_s, color=GREY_3B)
        self.play(FadeIn(client), FadeIn(server), Create(lc), Create(ls), run_time=0.8)

        def msg(x0, x1, up, text, color):
            a = Arrow(RIGHT * x0 + UP * (y_s if up else y_c), RIGHT * x1 + UP * (y_c if up else y_s),
                      buff=0.05, color=color, stroke_width=4)
            t = Text(text, font=MONO, font_size=18, color=color)
            t.next_to(a.get_center(), RIGHT if up else LEFT, buff=0.15)
            return VGroup(a, t)

        delete = msg(-4.4, -4.0, False, "DELETE", WHITE)
        self.cue("Deleting a conversation")
        self.play(GrowArrow(delete[0]), FadeIn(delete[1]))
        silence = label("before: no close frame, no events", size=20, color=RED_3B)
        silence.move_to(UP * (y_c + 0.6) + LEFT * 1.0)
        self.play(FadeIn(silence))
        self.cue("Now the server")
        self.play(FadeOut(silence))
        close = msg(-2.4, -2.0, True, "close 1012", YELLOW_3B)
        self.play(GrowArrow(close[0]), FadeIn(close[1]))
        self.cue("after a delete")
        recon = msg(1.8, 2.2, False, "reconnect", WHITE)
        self.play(GrowArrow(recon[0]), FadeIn(recon[1]))
        self.cue("gets four oh oh four")
        gone = msg(4.0, 4.4, True, "4004", RED_3B)
        stop = label("stops", size=22, color=WHITE).next_to(gone[0].get_end(), UP, buff=0.3)
        self.play(GrowArrow(gone[0]), FadeIn(gone[1]), FadeIn(stop))
        self.cue("One extra reconnect")
        imp = VGroup(label("Implemented", size=20, color=GREEN_3B, weight=BOLD),
                     label("1012 for delete, pause and shutdown; one extra reconnect (~1 s)",
                           size=20, color=WHITE)).arrange(RIGHT, buff=0.3)
        alt = VGroup(label("Alternative", size=20, color=ORANGE_3B, weight=BOLD),
                     label("4004 on delete: a code threaded through every close() override",
                           size=20, color="#D7D9DE")).arrange(RIGHT, buff=0.3)
        rows = VGroup(imp, alt).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        alt[1].align_to(imp[1], LEFT)
        dc = card(rows, buff=0.3, edge=YELLOW_3B).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(dc, shift=UP * 0.2))

    # 10 ------------------------------------------------------------------
    def rotation(self):
        head = self.title("Secret key rotation")
        badge = pill("#5758  ·  asked for by Engel", YELLOW_3B, 20).next_to(head, DOWN, buff=0.3)
        self.play(FadeIn(badge))

        def key(text, color):
            k = VGroup(Circle(0.16, color=color, stroke_width=4),
                       Line(ORIGIN, RIGHT * 0.45, color=color, stroke_width=4))
            k[1].next_to(k[0], RIGHT, buff=0)
            t = Text(text, font=MONO, font_size=18, color=color).next_to(k, DOWN, buff=0.15)
            return VGroup(k, t)

        cur = key("OH_SECRET_KEY", GREEN_3B)
        old = key("OH_PREVIOUS_SECRET_KEYS", ORANGE_3B)
        keys = VGroup(cur, old).arrange(RIGHT, buff=1.8).shift(UP * 0.5)
        self.cue("Changing the server's")
        before = label("before: change the key, and every stored secret becomes unreadable",
                       size=22, color=RED_3B).next_to(badge, DOWN, buff=0.5)
        self.play(FadeIn(before))
        self.cue("So the cipher")
        self.play(FadeOut(before), FadeIn(keys))
        enc = label("encrypts", size=20, color=GREEN_3B).next_to(cur, DOWN, buff=0.25)
        dec = label("decrypts too", size=20, color=ORANGE_3B).next_to(old, DOWN, buff=0.25)
        self.cue("It always encrypts")
        self.play(FadeIn(enc))
        self.cue("still reads")
        self.play(FadeIn(dec))
        snippet = code([
            "+    def rotate(self, token: str) -> str | None:",
            "+        if self.is_current(token):",
            "+            return token",
            "+        return self._get_multi_fernet().rotate(token.encode()).decode()",
        ], size=17).to_edge(DOWN, buff=0.4)
        self.cue("and re-encrypts")
        self.play(FadeIn(snippet, shift=UP * 0.2))

    # 11 ------------------------------------------------------------------
    def pending(self):
        dc = decision_card(
            "Where to classify an unknown model in a live ACP model switch.",
            "ask the ACP server first; only a -32603 for an id that the session's "
            "available_models does not list becomes a 400. It never refuses an id the "
            "adapter would accept.",
            "check available_models before the protocol call and refuse locally: one round "
            "trip less, but it would refuse ids an adapter accepts without listing them.",
            width=66, size=20,
        )
        dc.scale_to_fit_height(min(dc.height, 5.6)).move_to(UP * 0.35)
        src = label("PR #5830  ·  L14", size=18).next_to(dc, UP, buff=0.2).align_to(dc, LEFT)
        self.play(FadeIn(dc[0]), Write(dc.head), FadeIn(src), run_time=1.0)
        self.play(FadeIn(dc.q))
        self.cue("or ask the agent")
        self.play(FadeIn(dc.imp, shift=RIGHT * 0.2))
        self.play(FadeIn(dc.alt, shift=RIGHT * 0.2))
        self.cue("Its description check")
        chk = VGroup(Dot(color=RED_3B, radius=0.1),
                     label("Validate PR description", size=20, color=WHITE))
        chk.arrange(RIGHT, buff=0.2)
        wait = pill("waiting on Engel", YELLOW_3B, 20)
        row = VGroup(chk, wait).arrange(RIGHT, buff=0.8).next_to(dc, DOWN, buff=0.35)
        self.play(FadeIn(row, shift=UP * 0.15))
        self.play(Flash(chk[0], color=RED_3B), run_time=0.8)
        self.cue("That is by design")
        self.play(Indicate(wait, color=YELLOW_3B))

    # 12 ------------------------------------------------------------------
    def closing(self):
        n = Text("~50", font=SANS, font_size=96, color=YELLOW_3B, weight=BOLD)
        c = prose("pull requests with a \"Decision needed\" section", size=32)
        g = VGroup(n, c).arrange(DOWN, buff=0.25).shift(UP * 1.4)
        self.play(FadeIn(n, scale=0.8), Write(c), run_time=1.4)
        self.cue("The agent does")
        l1 = prose("The agent does the work.", size=36)
        l2 = prose("The maintainers keep the choices.", size=36, color=YELLOW_3B)
        lines = VGroup(l1, l2).arrange(DOWN, buff=0.2).next_to(g, DOWN, buff=0.6)
        self.play(Write(l1), run_time=1.0)
        self.cue("The people")
        self.play(Write(l2), run_time=1.2)
        self.cue("A map anyone")
        last = prose("A map anyone can rerun, fixes anyone can read, in the open.",
                     size=28, color=WHITE).next_to(lines, DOWN, buff=0.6)
        src = label("github.com/OpenHands/software-agent-sdk  ·  issue #5653", size=18)
        src.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(last, shift=UP * 0.2), FadeIn(src))
        self.wait(1.5)
