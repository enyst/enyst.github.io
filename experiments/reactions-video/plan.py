"""The edit plan shared by reactions.py (Manim) and compose.py (ffmpeg).

Each scene lasts as long as its narration plus GAP, or as long as its screen
clip if that is longer. Clip segments are (source start, source end, speed),
in seconds of the recordings under clips/ (made with control-openhands
`browser record` against a live stack, see README.md).
"""

import json

GAP = 0.6
DUR = json.load(open("voice/durations.json"))

# where the 1600x900 recording sits in the 1920x1080 frame
CLIP_X, CLIP_Y, CLIP_SCALE = 240, 52, 0.9

CLIPS = {
    # Settings > Experimental through the command menu; the switch flips at 6.68 s
    "flag": dict(src="clips/flag.mp4", offset=0.3, segs=[(0.0, 9.2, 1.0)]),
    # the first message is in, the agent starts
    "ask": dict(src="clips/main.mp4", offset=0.0, segs=[(1.0, 3.76, 0.6)]),
    # "wait, actually" lands; the agent's 👍 appears at 7.4 s
    "thumbs": dict(src="clips/main.mp4", offset=0.0, segs=[(4.28, 7.4, 0.5), (7.4, 10.3, 1.0)]),
    # it works (sped up), answers at ~22 s; the person's ❤️ at 27.4 s
    "done": dict(src="clips/main.mp4", offset=0.0, segs=[(10.3, 21.0, 4.0), (21.0, 32.2, 1.25)]),
    # after `control-openhands restart`: reopen the conversation
    "restore": dict(src="clips/restore.mp4", offset=2.6, segs=[(0.0, 8.1, 1.0)]),
}

ORDER = ["hook", "flag", "setup", "ask", "thumbs", "done", "restore", "closing"]


def clip_len(name):
    c = CLIPS[name]
    return c["offset"] + sum((b - a) / s for a, b, s in c["segs"])


def src_to_scene(name, t):
    """Map a time in the source recording to seconds into the scene."""
    c = CLIPS[name]
    acc = c["offset"]
    for a, b, s in c["segs"]:
        if a <= t <= b:
            return acc + (t - a) / s
        acc += (b - a) / s
    raise ValueError(t)


def scene_len(name):
    n = DUR[name] + GAP
    if name in CLIPS:
        n = max(n, clip_len(name) + 0.4)
    if name == "closing":
        n += 2.5
    return round(n, 2)


def timeline():
    t, out = 0.0, []
    for name in ORDER:
        out.append((name, round(t, 2)))
        t += scene_len(name)
    out.append(("end", round(t, 2)))
    return out


def px(x, y):
    """A point in recording pixels -> Manim coordinates (frame 1920x1080, 135 px/unit)."""
    X = CLIP_X + x * CLIP_SCALE
    Y = CLIP_Y + y * CLIP_SCALE
    return [(X - 960) / 135, (540 - Y) / 135, 0]


# moments for sound and highlights, in seconds from the start of the film
def moments():
    tl = dict(timeline())
    return {
        "hook_pop": tl["hook"] + 11.3,
        "flag_switch": tl["flag"] + src_to_scene("flag", 6.68),
        "thumbs_pop": tl["thumbs"] + src_to_scene("thumbs", 7.4),
        "heart_pop": tl["done"] + src_to_scene("done", 27.4),
    }


if __name__ == "__main__":
    for name, t in timeline():
        print(f"{name:8s} {t:6.2f}")
    print(moments())
