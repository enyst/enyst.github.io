# F31 metadata takeover setup adaptation

The frozen recipe fails before its bug assertion when this container's PID 1 leaves the SIGKILLed server as a zombie. kill(pid, 0) reports the zombie PID exists, and the product uses the same existence check for lease liveness. This supplementary copy preserves the metadata assertion exactly. It records the old owner status with psutil (must be zombie, dead, or gone), waits until the existing lease expires, then makes the second server load the conversation and verifies generation 2 before checking the title.

Only a recipe copy under harness-f29-f34 changes; frozen checkout and product source remain unchanged. The full first-pass F31.json continues to report the original result. Reproduction uses the copied launcher and --checkout /workspace/agent-sdk-verify so every product process remains frozen at acca181af1f353975965bcf6486e1d0a58f444c0.

A second setup adaptation replaces the invalid-startup recipe's two runs.alive checks (kill-zero based and true for zombies) with explicit psutil zombie/dead/gone plus closed-port checks. It retains both startup-failure and error-log expectations and warms OpenAPI before the final doctor. The first supplementary attempt preserves the original liveness-check failure; the second attempt and a later targeted check use this setup correction.

The tmux-cleanup setup also cannot rely on stop.server == terminated: the CLI reports killed when the already gracefully stopped server remains a zombie. Its replacement keeps stop successful and asserts the server's Application shutdown complete log before the unchanged directory-removal bug assertion. Both original supplementary attempts retain the earlier stop-label failure; targeted new fresh repeats apply this observation correction.
