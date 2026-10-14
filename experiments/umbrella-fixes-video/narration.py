"""Narration for umbrella_fixes.py, spoken by Kokoro-82M (Apache-2.0, open weights).

Writes voice/<scene>.wav and voice/durations.json. The scene script reads the
durations so each scene lasts as long as its narration.
Run with a Python that has `kokoro` and `soundfile` installed.
"""

import json
import os

VOICE = "af_heart"
SPEED = 0.95
SR = 24000

SCENES = {
    "opening": (
        "We ran every recipe in the agent server's feature map, against a real server "
        "and a real model. It found a long list of bugs. This is the story of what came "
        "next: every one of them fixed, one pull request at a time."
    ),
    "method": (
        "First, a short reminder of the method. The feature map lists everything an agent "
        "can do with the OpenHands agent server: thirty-four families, more than nine "
        "hundred sub-features, each with a stable name. The command line tool, control "
        "agent server, lets an agent drive each one, step by step, the way a real client "
        "would. And the rule is simple. Verify everything. Because once you can see every "
        "behavior, you can fix every behavior."
    ),
    "proof": (
        "Each known bug lives in the map as a line with a predicate: what the broken "
        "behavior looks like today. On main, that line must fail in exactly that way, "
        "twice. On the fix branch, it must pass, twice. Only then is the bug marker "
        "removed, and the line becomes an ordinary check that guards the fix from now on."
    ),
    "numbers": (
        "Thirteen medium bugs. Fourteen more mediums that contributors already had pull "
        "requests for, fixed again independently, so a maintainer can keep the better one. "
        "Eight older reports. And ninety-three low-severity bugs, each given its own issue "
        "first. In all, a hundred and twenty-six pull requests. Two are already merged. "
        "The rest are green, and ready for review."
    ),
    "subagent": (
        "Here is the first one to land. A sub-agent definition that named a skill which "
        "doesn't exist made the very first message of a conversation fail with a server "
        "error. The map line described it precisely: status five hundred, skill not found. "
        "The fix wraps each definition. If it can't be built, it is skipped with a warning, "
        "and everything else keeps working."
    ),
    "decision": (
        "And here is the part worth slowing down for. The issue's triage had asked a real "
        "question: should this bug be folded into a wider issue about plugin loading? "
        "That is not the agent's call. So the pull request says it up front, in a section "
        "called Decision needed: what was implemented, and the alternative, with its cost. "
        "Here, the recommended option is the one that was built: keep it separate, and "
        "small. The maintainer still sees the choice, and can change it."
    ),
    "freeze": (
        "Some bugs only show up when you measure. When a conversation run failed, the "
        "whole server froze for about five seconds: every request, every socket. The map "
        "recorded the slowest health probe while the run was failing. On main, it took "
        "more than four and a half seconds. On the fix branch, about a hundred "
        "milliseconds."
    ),
    "freeze_fix": (
        "The cause was a single log line: a rich, colorful traceback, rendered right on "
        "the event loop. The fix logs the same traceback as plain text. Again there was a "
        "real trade-off, so the pull request lays it out: plain text now, or a logging "
        "queue that keeps the pretty output, but changes logging for every S D K user. "
        "It even records what did not work: moving the call to a thread still stalled, "
        "because every log call waits on the same lock."
    ),
    "sockets": (
        "Deleting a conversation left its websockets open, and silent. Clients never "
        "learned the conversation was gone. Now the server closes them with code ten "
        "twelve, service restart. The issue had suggested a different code for delete. "
        "The pull request explains why one code is enough: after a delete, the client's "
        "reconnect gets four oh oh four, and stops. One extra reconnect, about a second, "
        "for a much smaller change. And again, the maintainer decides."
    ),
    "rotation": (
        "Sometimes the decision came straight from Engel. Changing the server's secret "
        "key used to leave every stored secret unreadable. Engel asked for real key "
        "rotation. So the cipher now carries its previous keys. It always encrypts with "
        "the current one, still reads values saved under the old ones, and re-encrypts "
        "them the next time they are saved."
    ),
    "pending": (
        "One question is still open. When a live A C P session is asked to switch to a "
        "model it does not offer, should the server check the model list itself, or ask "
        "the agent first, and only translate its error? The pull request builds the "
        "cautious option, and waits. Its description check stays red until Engel decides. "
        "That is by design."
    ),
    "closing": (
        "About fifty of these pull requests carry a Decision needed section. Each one "
        "says what was done, and what else could have been done. The agent does the "
        "work. The people who maintain the project keep the choices. A map anyone can "
        "rerun, and fixes anyone can read, all in the open."
    ),
}

if __name__ == "__main__":
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    os.makedirs("voice", exist_ok=True)
    pipe = KPipeline(lang_code="a")
    durations = {}
    for name, text in SCENES.items():
        audio = np.concatenate([a for _, _, a in pipe(text, voice=VOICE, speed=SPEED)])
        sf.write(f"voice/{name}.wav", audio, SR)
        durations[name] = round(len(audio) / SR, 2)
        print(name, durations[name])
    json.dump(durations, open("voice/durations.json", "w"), indent=1)
