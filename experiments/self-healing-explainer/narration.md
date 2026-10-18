# Self-Healing — narration script (v2)

Voice: Kokoro-82M, af_heart. One paragraph per scene.

## 1. The factory
Software is starting to improve itself. Agents read code, write changes, and open pull requests, day and night. That is a software factory. And it runs at the speed of agents: more changes than any person can check. At the speed of agents, you need a safety net. Something that notices when a change breaks what people rely on, and puts it right. We call that Self-Healing. Let's build it from the ground up, one small piece at a time.

## 2. A promise
Start with something a user really relies on. You open Settings, and tell the app who you are: your name, and your email. You press Save. It says: Settings saved. Then you ask the agent to do some work, and commit it. What should happen? The commit carries your name. That is a promise. And a coding agent that breaks it fails at its most basic job.

## 3. The map
Now write that promise down. Give it a name. Write the exact steps to get there, and what you should see at the end. Do that for every promise the app makes, and you get a map. The OpenHands feature map lists every user-facing behavior, grouped into families, from onboarding, to settings, to conversations.

## 4. Hands
A map is only useful if someone can walk it. So we give an agent hands: a command line tool called control-openhands. It launches the real app, clicks the real buttons, types into the real fields, and saves screenshots and video. Not a test that says it passed. A picture of what a person would actually see.

## 5. Every day
Now add time. Every day, new code lands on main. And every day, an automation walks the map against the new app. Most promises still hold. Sometimes, one doesn't. Here, the settings were saved. But the agent's commit failed: Author identity unknown. On a machine that already had a git identity, it was worse. The commit went through, silently, under someone else's name. Before calling it a bug, a second agent tries again, on a fresh copy of the app. It fails the same way. A real failure repeats. A flaky one doesn't.

## 6. Why it hid
Why did it break? Follow the name. It is saved in Settings. But when a conversation starts, the request to the agent server never carries it. The terminal never sees it. And git, at the end of the line, has no idea who you are. Every piece looked fine on its own. The promise broke in the gaps between them. Only a walk through the real app, end to end, could catch that.

## 7. Remember the bug
A real failure becomes an issue, with the evidence attached. And the map learns about it too. The step gets a known-bug note that can run. Today, it is expected to fail. The day it stops failing, the map will notice.

## 8. The fix, with proof
Then comes the fix. A pull request changes the product code and its tests. Nothing else. Now the start request carries your name all the way down, into the terminal, as git's own variables. The proof is the same walk, on the old code and on the fix. Before: Author identity unknown. After: committed as QA Tester, exactly the name that was saved. And the rule is strict. Twice on the old code, it must fail. Twice on the fix, it must pass.

## 9. One rule
Notice one rule. The fix never touches the map. The map says what should be true. The fix makes it true. They live in separate pull requests, because the same hand should not write both the test and the answer.

## 10. Healed
When the fix merges, the next daily pass walks the same path. The known bug now passes. So the automation closes the issue, and updates the map in its own pull request. The loop is closed. The software broke, noticed, and healed.

## 11. The safety net
Put it together. A map of promises. Hands that check them on the real app. A walk every day. Proof before and after every fix. Self-improving code keeps climbing, at the speed of agents. Self-healing is the net underneath, so every step up is a safe one. And all of it is open source, so anyone can read it, run it, and build on it.
