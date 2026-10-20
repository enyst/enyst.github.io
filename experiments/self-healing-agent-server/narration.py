"""Narration for self_healing.py, spoken by Kokoro-82M (Apache-2.0, open weights).

Writes voice/<scene>.wav and voice/durations.json. The scene script reads the
durations so each scene lasts as long as its narration.
Run with a Python that has `kokoro` and `soundfile` installed.
"""

import json
import os

VOICE = "af_heart"
SPEED = 0.94
SR = 24000

SCENES = {
    "opening": (
        "Codebases are starting to improve themselves. "
        "Agents write code, review it, and ship it, faster than any of us can read it. "
        "A software factory. And in a factory, some things will break. So we need safety nets."
    ),
    "nets": (
        "There are a few. The first is design review, done by people, when it matters: not "
        "every line, but the choices that shape everything else. The second is constraints: "
        "linters, types, rules about what code is even allowed to look like. Most mistakes "
        "stop there. But some slip through both. Self-healing is the last net. When the code "
        "breaks anyway, it catches the break, and turns it into a guard."
    ),
    "door": (
        "To see what that means, start with the person who feels a break. Someone sits in "
        "front of a user interface, like Agent Canvas. Every button they press becomes a "
        "request, over REST, to the OpenHands agent server. Agents reach the same server "
        "through a command line tool, control agent server. Different hands, same door. "
        "So when the server breaks, people feel it."
    ),
    "promise": (
        "Now, the smallest piece. A feature is a promise. If I stop a goal, it stops. If I "
        "save one setting, my other settings stay. We write each promise down as one line, "
        "with a stable name, and a short recipe that checks it, the way a client would. "
        "Put every promise in a row, and you get a map. The agent server's map has more than nine hundred of these promises, organized in thirty-"
        "four families."
    ),
    "walk": (
        "Then an agent walks the map. A real server, a real model, one recipe after "
        "another. Most lines turn green. Some turn red. A red line is a broken promise, and "
        "every red line has a story. Here are three examples."
    ),
    "goal": (
        "The first. You give the agent a goal: write a story, in up to three tries. The "
        "interface shows a small chip: goal, running. Now the server restarts, gracefully, "
        "as servers do. When it comes back, nothing is running. But the chip still says "
        "running. You press stop. The server answers: success. And the chip keeps "
        "spinning, forever."
    ),
    "goal_fix": (
        "Why? The server keeps a timeline of events, and the interface draws the last goal "
        "event it finds. At shutdown, the loop was cancelled, but because the server was "
        "closing, it skipped writing the one word that mattered: interrupted. After the "
        "restart, nothing corrected the old line. The fix is a small act of honesty. When a "
        "conversation loads, and its last goal says running with no loop behind it, the "
        "server writes interrupted. The chip now says what is true, and offers to resume."
    ),
    "proof": (
        "How does the net know a fix is real? While the bug is open, its line in the map "
        "carries a marker, with a precise description of today's broken behavior. On main, "
        "the line must fail in exactly that way, twice. On the fix branch, it must pass, "
        "twice. Then the marker comes off, and the line becomes an ordinary check. The "
        "break has become a guard. And the map runs again every day, so if the bug ever "
        "comes back, the net catches it again."
    ),
    "freeze": (
        "The second story is about time. Picture a server with several conversations open, "
        "each in its own window. One run fails, because its model can't be reached. And "
        "for about five seconds, every window freezes. Every request, every live update, "
        "waits."
    ),
    "freeze_fix": (
        "The server does its work on a single lane, an event loop, where every task takes a "
        "short turn. When the run failed, the server logged it, with a beautiful, colorful "
        "traceback, about a thousand lines, drawn right there in the lane. Nothing else "
        "could pass until it was done, and that takes time. The agents running the map caught it with a stopwatch: the slowest "
        "health check took more than four and a half seconds. The fix is funnily simple: log the same "
        "traceback as plain text. Now the slowest check takes about a tenth of a second."
    ),
    "secrets": (
        "The third story is the quietest, and the one that hurts most. The server keeps "
        "your A P I keys and secrets locked, with a secret key of its own. Suppose that key "
        "changes, say during a redeploy. The server can no longer open the old locks. So it "
        "reads your saved keys as empty. Nothing looks wrong yet."
    ),
    "secrets_fix": (
        "Then you flip an unrelated switch in your settings, and press save. The server "
        "writes everything back, including the empty values, right over your real keys. "
        "Two hundred, okay. Even when the old key returns, your secrets are gone. The fix "
        "has two parts. First, if a value can't be opened, refuse the write, and say why. "
        "Second, real key rotation: the server keeps a list of previous keys, reads old "
        "values with them, and quietly locks everything again with the new one."
    ),
    "decide": (
        "Fixes like these come with choices. Should a refused secrets write answer four oh "
        "nine, like settings, or keep today's code? That is not the agent's call. So each "
        "such pull request opens with a section called Decision needed: what was built, and "
        "the alternative, with its cost. The agent does the work. The people who maintain "
        "the project keep the choices."
    ),
    "closing": (
        "Agentic Engineering. Review the designs that matter. Constrain the code. And when "
        "it breaks anyway, a net that catches the break, proves the fix, and keeps the "
        "guard."
    ),
    # the credits line: its own clip, after a pause, slower and a little softer
    "credits": (
        "The map, the tools, the fixes, and even this voice, an open-weight model, "
        "are all in the open, for anyone to run again."
    ),
}

# per-scene speaking speed (default SPEED) and loudness in the mix (default 1.0)
SPEEDS = {"credits": 0.84}
GAINS = {"credits": 0.8}

if __name__ == "__main__":
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    os.makedirs("voice", exist_ok=True)
    pipe = KPipeline(lang_code="a")
    durations = {}
    for name, text in SCENES.items():
        audio = np.concatenate([a for _, _, a in pipe(text, voice=VOICE, speed=SPEEDS.get(name, SPEED))])
        sf.write(f"voice/{name}.wav", audio, SR)
        durations[name] = round(len(audio) / SR, 2)
        print(name, durations[name])
    json.dump(durations, open("voice/durations.json", "w"), indent=1)
