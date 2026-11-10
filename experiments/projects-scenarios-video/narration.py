"""Narration per section, voiced by Kokoro-82M (Apache-2.0, open weights), voice af_heart."""
import json, os, sys
SCENES = {
 "s1": "Projects is an experimental feature, so we start in Settings, Experimental, and turn on Projects and conversation reactions. Projects appears in the sidebar. The first project also creates two agent profiles: a project coordinator, with a terminal, a file editor and a task tracker but no browser, and a project worker. Every coordinator and worker the server starts gets its role in its system prompt, whatever profile it runs.",
 "s2": "A real bug bash, replayed from the software agent SDK's history: four edge case bugs from issue sixty-three forty-eight, on a local copy of the repo from before they were fixed. We name the project, pick the repo, and hand the coordinator the four reports. It starts one worker per bug and ends its turn. We click a mention to look in on one worker, and go back. The board shows four working. Each worker finds the cause, writes a regression test that fails first, fixes it, and reports back. The coordinator reviews each diff and sends us one summary, with two things to sign off. We sign off, and ask for one more test case. The coordinator forwards it to the worker that owns that branch, which wakes, adds the test and finishes. Three cards resolved themselves. We resolve the last one, and reopen another from its banner.",
 "s3": "Second project: scoped secrets, issue fifty-six seventy-two, a feature that touches the model, the prompt and the agent. We ask to approve the exact prompt text before anyone writes the rendering. The coordinator splits the work, starts the parts that don't depend on that text, and saves its proposal as a project file. We approve it with one change. Then we drop into a busy worker and say: wait, actually, also test the round trip. The message waits until the worker's test run ends, then the worker does it. It didn't react with a thumbs up; that still needs a nudge in AGENTS dot md. The coordinator reports three branches, merges them locally to check they fit together, and writes our rule into project memory.",
 "s4": "Third project, from the Insider app. We install Insider from GitHub in Customize, Apps, and trust it. Then we give the Insider Cat three fixes the review found in Insider itself, replayed on a local copy. The Cat starts a project on the server and three workers. Its board groups them the way the server does: needs you, working, resolved. One worker asks whether to merge the branches together. We open it from the card, answer in a sentence, and come back.",
 "s5": "Project files go both ways. We upload a release checklist on the project page, and ask the coordinator whether our four branches meet it. It lists the project's files, reads ours, checks every branch, and finds that no commit names the issue it fixes. Project memory works the same way: a rule we gave the coordinator in the scoped secrets project shows up in the next worker's system prompt.",
 "s6": "A long project will see a restart. We restart Agent Server while a worker is running. Projects, the board and every conversation come back. The interrupted worker shows under needs you, the coordinator is told, and a sentence from us gets the worker going again. On a second try the worker was in the middle of a test run, and it came back looking like a crash. That was fixed within the hour: now it comes back paused, and the coordinator says the restart did it, not you.",
 "s7": "Turning Projects off hides it: the sidebar entry goes, and the page says where to turn it back on. Nothing is deleted. Turn it on again, and all three projects are still there.",
}
if __name__ == "__main__":
    import numpy as np, soundfile as sf
    from kokoro import KPipeline
    os.makedirs("voice", exist_ok=True)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    d = {}
    for k, t in SCENES.items():
        chunks = [np.asarray(r.audio) for r in pipe(t, voice="af_heart", speed=1.0)]
        audio = np.concatenate(chunks); sf.write(f"voice/{k}.wav", audio, 24000); d[k] = len(audio) / 24000
        print(k, round(d[k], 2), flush=True)
    json.dump(d, open("voice/durations.json", "w"), indent=1)
