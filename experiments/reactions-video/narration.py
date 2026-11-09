"""Narration for reactions.py, spoken by Kokoro-82M (Apache-2.0, open weights).

Writes voice/<scene>.wav and voice/durations.json. The edit (scenes.py) reads
the durations, so each scene lasts as long as its narration.
Run with a Python that has `kokoro` and `soundfile` installed.
"""

import json
import os

VOICE = "af_heart"
SPEED = 1.0
SR = 24000

SCENES = {
    "hook": (
        "Ask an AI agent to change one small thing, and you often get a paragraph back. "
        "Got it! You'd like me to... and then your own words, read back to you. "
        "It means well. But sometimes, a thumbs up says it all."
    ),
    "flag": (
        "OpenHands now has reactions, as an experimental feature. Open the command menu, "
        "go to Experimental, and switch on Conversation reactions."
    ),
    "setup": (
        "Here is a real run, with DeepSeek Flash driving the agent. Our little dinner repo "
        "has a note for agents: keep answers short, and if I change my mind, "
        "give me a thumbs up and carry on."
    ),
    "ask": (
        "We ask for a script that splits the team dinner bill evenly. "
        "The agent starts writing it."
    ),
    "thumbs": (
        "Then: wait, actually. Not everyone had drinks. The agent doesn't stop to say "
        "all of that back. It reacts, thumbs up, and keeps going."
    ),
    "done": (
        "When it's done, the answer is short: the new options, one example run, "
        "and a line about leftover pennies. Exactly right. That gets a heart."
    ),
    "restore": (
        "Reactions are saved with the conversation. Restart the server, open the "
        "conversation again, and they're still there: the agent's thumbs up, and our heart."
    ),
    "closing": (
        "React, then do the thing. Fewer words, same understanding. "
        "It's all open source, in the OpenHands agent S D K and Canvas."
    ),
}

if __name__ == "__main__":
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    os.makedirs("voice", exist_ok=True)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    durations = {}
    for name, text in SCENES.items():
        audio = np.concatenate([a for _, _, a in pipe(text, voice=VOICE, speed=SPEED)])
        sf.write(f"voice/{name}.wav", audio, SR)
        durations[name] = round(len(audio) / SR, 2)
        print(name, durations[name])
    json.dump(durations, open("voice/durations.json", "w"), indent=1)
