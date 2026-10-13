"""Run pytest with a Linux subreaper to isolate PID-1 zombie effects."""
import ctypes
import os
import subprocess
import sys
import threading
import time

import psutil

libc = ctypes.CDLL(None, use_errno=True)
if libc.prctl(36, 1, 0, 0, 0) != 0:
    raise OSError(ctypes.get_errno(), "PR_SET_CHILD_SUBREAPER failed")
done = threading.Event()


def reap():
    while not done.is_set():
        for child in psutil.Process().children():
            try:
                if child.status() == psutil.STATUS_ZOMBIE and child.name() == "sleep":
                    os.waitpid(child.pid, os.WNOHANG)
            except (psutil.NoSuchProcess, ChildProcessError):
                pass
        done.wait(0.02)


thread = threading.Thread(target=reap, daemon=True)
thread.start()
try:
    result = subprocess.run(sys.argv[1:])
    sys.exit(result.returncode)
finally:
    done.set()
    thread.join()
