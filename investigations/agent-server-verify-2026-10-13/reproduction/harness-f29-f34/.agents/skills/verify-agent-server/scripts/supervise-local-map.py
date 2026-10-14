"""Run one local CLI job while reaping only its adopted, exited descendants.

The controlled Popen child remains excluded so its owner retains wait/return-code
accounting. Every other direct child was adopted after an intermediate parent
exited. This helper never sends signals or reads environment/command arguments.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

import psutil

parser = argparse.ArgumentParser()
parser.add_argument("--report", required=True)
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
command = args.command[1:] if args.command[:1] == ["--"] else args.command
if not command:
    parser.error("a command is required after --")
libc = ctypes.CDLL(None, use_errno=True)
if libc.prctl(36, 1, 0, 0, 0) != 0:
    raise OSError(ctypes.get_errno(), "PR_SET_CHILD_SUBREAPER failed")

controlled = subprocess.Popen(command)
excluded = {controlled.pid}
done = threading.Event()
reaped: list[dict[str, object]] = []
owner = psutil.Process()


def adopted():
    return [child for child in owner.children(recursive=False) if child.pid not in excluded]


def reap():
    while not done.is_set():
        for child in adopted():
            try:
                if child.status() != psutil.STATUS_ZOMBIE:
                    continue
                name = child.name()
                pid, status = os.waitpid(child.pid, os.WNOHANG)
                if pid:
                    reaped.append({"pid": pid, "name": name, "wait_status": status})
            except (psutil.NoSuchProcess, psutil.AccessDenied, ChildProcessError):
                continue
        done.wait(0.02)


thread = threading.Thread(target=reap, daemon=True)
thread.start()
try:
    returncode = controlled.wait()
    deadline = time.monotonic() + 2
    while adopted() and time.monotonic() < deadline:
        time.sleep(0.02)
finally:
    done.set()
    thread.join()

remaining = []
for child in adopted():
    try:
        remaining.append({"pid": child.pid, "name": child.name(), "status": child.status()})
    except psutil.NoSuchProcess:
        pass
report = {"controlled_pid": controlled.pid, "controlled_returncode": returncode,
          "controlled_wait_owned_by_popen": True,
          "reaped_adopted_exited_children": reaped, "remaining_adopted_children": remaining,
          "signals_sent_by_supervisor": 0}
Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
print(f"local supervisor: reaped {len(reaped)} adopted exited children; {len(remaining)} remain",
      file=sys.stderr)
sys.exit(returncode if returncode else (1 if remaining else 0))
