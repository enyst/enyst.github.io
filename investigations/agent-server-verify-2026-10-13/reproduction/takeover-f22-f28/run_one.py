#!/usr/bin/env python3
"""Doctor, drive one official map subset, doctor, stop; preserve all evidence."""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path

CLI = '/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts/control-agent-server'
HERE = Path(__file__).resolve().parent

def command(args, target):
    result = subprocess.run([CLI, *args], cwd='/workspace/agent-sdk-verify',
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    target.write_text(result.stdout)
    target.with_suffix('.stderr.txt').write_text(result.stderr)
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument('family'); p.add_argument('only'); p.add_argument('--file')
    p.add_argument('--tag', default='confirm'); p.add_argument('--attempts', type=int, default=1)
    a = p.parse_args()
    os.environ['AGENT_SERVER_VERIFY_HOME'] = '/workspace/verification-artifacts/runs'
    os.environ['UV_CACHE_DIR'] = '/workspace/.cache/uv'
    os.environ['npm_config_cache'] = '/workspace/.cache/npm'
    os.environ['PATH'] = '/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:' + os.environ['PATH']
    results = []
    for i in range(a.attempts):
        stem = f'{a.family}-{a.tag}-{i + 1}'
        out = HERE / 'results'
        launch = subprocess.run([CLI, 'launch', '--new', '--name', stem, '--print-run'],
                                cwd='/workspace/agent-sdk-verify', text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if launch.returncode:
            (out / (stem + '-launch-error.json')).write_text(launch.stdout)
            raise RuntimeError(f'{stem} launch failed')
        run = launch.stdout.strip()
        (out / (stem + '.run')).write_text(run + '\n')
        try:
            doctor = command(['doctor', '--run', run], out / (stem + '-doctor-before.json'))
            if doctor.returncode:
                time.sleep(2)
                doctor = command(['doctor', '--run', run], out / (stem + '-doctor-before-retry.json'))
            if doctor.returncode:
                raise RuntimeError(f'{stem} doctor failed; no product assertions driven')
            print(json.dumps({'phase': 'drive', 'family': a.family, 'run': run}), flush=True)
            result = command(['map', 'run', '--file', a.file or a.family,
                              '--only', a.only, '--run', run, '--record', '--keep-going'],
                             out / (stem + '.json'))
            parsed = json.loads(result.stdout)
            after = command(['doctor', '--run', run], out / (stem + '-doctor-after.json'))
            results.append({'run': run, 'exit_code': result.returncode,
                            'summary': parsed.get('summary'), 'doctor_after_exit': after.returncode,
                            'results': str(out / (stem + '.json'))})
            print(json.dumps({'phase': 'done', **results[-1]}), flush=True)
        finally:
            command(['stop', '--run', run], out / (stem + '-stop.json'))
    (HERE / 'results' / (f'{a.family}-{a.tag}-combined.json')).write_text(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
