"""Write the slides (Paper palette) as HTML; shoot.js renders them to 1920x1080 PNGs."""
CSS = """
body{margin:0;width:1920px;height:1080px;background:#F4EFE6;color:#2b2722;font-family:'DejaVu Sans',sans-serif;}
.s{box-sizing:border-box;width:1920px;height:1080px;padding:110px 140px;display:flex;flex-direction:column;justify-content:center}
.k{font-family:'DejaVu Sans Mono',monospace;font-size:26px;letter-spacing:.12em;text-transform:uppercase;color:#a0583a;margin-bottom:22px}
h1{font-family:'DejaVu Serif',serif;font-weight:400;font-size:84px;line-height:1.1;margin:0 0 30px}
p{font-size:38px;line-height:1.45;color:#4a433c;margin:0 0 18px;max-width:1500px}
code{font-family:'DejaVu Sans Mono',monospace;font-size:.86em;background:#e9e1d3;padding:2px 10px;border-radius:6px}
ul{margin:10px 0 0;padding-left:40px} li{font-size:36px;line-height:1.5;color:#4a433c;margin-bottom:10px}
.bar{display:flex;gap:28px;margin-top:30px}
.box{flex:1;background:#fbf8f2;border:2px solid #ddd3c2;border-left:8px solid #4f8f80;border-radius:14px;padding:26px 30px;font-size:32px;line-height:1.4}
.box b{display:block;font-size:24px;letter-spacing:.08em;text-transform:uppercase;color:#7a7067;margin-bottom:8px;font-family:'DejaVu Sans Mono',monospace}
.amber{border-left-color:#c08a3e}.grey{border-left-color:#b9ae9c}
.foot{position:absolute;bottom:60px;left:140px;font-size:24px;color:#8a8076;font-family:'DejaVu Sans Mono',monospace}
"""
S = {
"intro": """<div class=k>software-agent-sdk #6602 · fresh read</div><h1>What could split out<br>of the Projects PR</h1>
<p>82 files · ~16,800 lines added · 8,400 code · 7,200 tests</p><p>Which pieces are worth something on <code>main</code> with Projects off?</p>""",
"test": """<div class=k>The test</div><h1>Three checks for each piece</h1>
<div class=bar><div class=box><b>1 · Value</b>main gets something from it today</div><div class=box><b>2 · Size</b>reviewable on its own</div><div class=box><b>3 · Clean cut</b>no project code comes along</div></div>
<p style="margin-top:40px">Three pass · one to check · the rest stays</p>""",
"guard": """<div class=k>Split 1 · recommended · after #6912</div><h1>Messages from someone<br>other than the user</h1>
<ul><li><code>admission_refusal</code> · <code>HeldForUser</code> · typed run refusals</li><li><code>refuse_pending_confirmation</code> + <code>sender_conversation_id</code> on POST /events</li><li>A response that says whether the message ran</li></ul>
<div class=bar><div class=box><b>Why on main</b>Insider Cat already sends these fields; a released server ignores them</div><div class="box grey"><b>Stays in #6602</b>project-only sender rule, wake-up helpers</div></div>""",
"ask": """<div class=k>Split 2 · recommended · small</div><h1>Find the open question<br>without reading the whole log</h1>
<p><code>find_pending_ask_back</code> · newest first, stops early</p>
<ul><li>main: <code>local_conversation.py</code> ×3 read the whole branch</li><li>main: <code>event_service.py</code> goal check, <code>goal/runner.py</code> the whole log</li><li>#6602 fixes one call · a PR from main fixes all five</li></ul>""",
"tags": """<div class=k>Split 3 · recommended · bug fix</div><h1>Show new tags as soon<br>as they are saved</h1>
<p>Commit <code>81147dd</code> · 8 lines + test</p><p>PATCH writes <code>meta.json</code> at once; <code>base_state.json</code> waits for the run to release its lock. Read tags from the metadata.</p>""",
"check": """<div class=k>Check first</div><h1>A shutdown pause is not a crash</h1>
<p><code>.paused_by_shutdown</code> mark · load as PAUSED, not ERROR</p><div class=bar><div class="box amber"><b>Projects</b>coordinator names the restart, doesn't blame the user</div><div class="box amber"><b>main</b>close() already pauses: reproduce before splitting</div></div>""",
"keep": """<div class=k>Keep in #6602</div><h1>Plumbing only Projects calls</h1>
<ul><li><code>scan_events</code>, <code>subscribe_internal</code>, <code>list_tagged_conversations</code>, <code>start_copied_child</code></li><li><code>prompt_preset</code>, <code>project_context</code>, <code>withheld_tools</code></li><li>Project prompt sections · <code>AskUserForConversationAction</code> · <code>TooLarge</code></li><li>Auto-resolve judge (as decided before)</li></ul>""",
"close": """<div class=k>Suggested order</div><h1>Now: tags, then the ask lookup.<br>After #6912: guarded messages.</h1>
<p>What stays is Projects itself, behind its flag.</p><p style="font-size:30px;color:#8a8076">Suggestions only · no PRs opened · #6602 ba97cee vs main f1eedd7</p>""",
}

for k, h in S.items():
    open(f"slide-{k}.html","w").write(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class=s>{h}</div></body></html>")
