"""Narration, voiced by Kokoro-82M (Apache-2.0, open weights), voice af_heart."""
import json, os
SCENES = {
 "intro": "The Projects pull request in the agent SDK is big: about seventeen thousand lines, half of them tests. We read it fresh, with one question. Which pieces would be worth something on main, even with Projects turned off?",
 "test": "Each candidate had to pass three checks. Main gets something from it today. It can be reviewed on its own. And it can be cut from main without pulling project code along. Three pieces pass. One more might. The rest should stay.",
 "guard": "The biggest is about messages from someone other than the user. Today, a run asked for on a conversation that waits for confirmation approves its pending action. The pull request adds one rule for every sender: never approve, never resume what the user paused, and say who sent the message. The Insider Cat already asks for this guard, but a released server silently ignores the fields. This one should follow the exceptions pull request, once it merges.",
 "ask": "The second is small. Your rule says nothing reads a whole event log, yet main still does, five times, just to ask whether a question is open. The pull request has a lazy, newest first lookup, but only uses it in one place. Split out from main, it can fix all five.",
 "tags": "The third is an eight line bug fix. A tag change on a running conversation stays invisible until the run lets go of its state. Reading tags from the metadata file shows them at once.",
 "check": "One to check first. A server shutdown can come back looking like a crash. Projects needs the shutdown mark for its coordinator, but on main this may already be fine. If it reproduces, it's a small fix of its own.",
 "keep": "Everything else is plumbing that only Projects calls: event scans, internal subscribers, prompt presets, the project prompts, and the judge. Splitting them would add code with no user.",
 "close": "So: the tag fix and the question lookup now, since they depend on nothing, and the guarded messages after the exceptions change. What stays is Projects itself, behind its flag. Open source, and easier to review.",
}
if __name__ == "__main__":
    import numpy as np, soundfile as sf
    from kokoro import KPipeline
    os.makedirs("voice", exist_ok=True)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    d = {}
    for k, t in SCENES.items():
        chunks = [np.asarray(r.audio) for r in pipe(t, voice="af_heart", speed=1.0)]
        audio = np.concatenate(chunks)
        sf.write(f"voice/{k}.wav", audio, 24000); d[k] = len(audio) / 24000
        print(k, round(d[k], 2))
    json.dump(d, open("voice/durations.json", "w"), indent=1)
