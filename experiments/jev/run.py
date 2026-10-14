#!/usr/bin/env python3
"""Reproduce the notebook's bounded Jev study; no GitHub mutations.
Uses TYPESAFE_API_KEY, or macOS Keychain service openhands/account TYPESAFE_API_KEY.
python3 run.py --live | --check results.json
"""
import argparse, datetime, hashlib, json, math, os, pathlib, statistics, subprocess, time, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parent
MODEL = 'jev-1.13.0'

def validate(request, response):
    assert response['model'] == MODEL
    assert set(response['answers']) == set(request['questions'])
    for name, q in request['questions'].items():
        a = response['answers'][name]
        assert a['type'] == q['type']
        if q['type'] == 'noul':
            assert type(a['noul']) in (int,float) and math.isfinite(a['noul']) and 0 <= a['noul'] <= 1
        else:
            keys = set(q['criteria']) if q['type']=='choice' else set(map(str,range(len(q['criteria']))))
            assert set(a['probabilities']) == keys
            ps = a['probabilities']
            assert all(type(p) in (int,float) and math.isfinite(p) and 0 <= p <= 1 for p in ps.values())
            assert abs(sum(ps.values())-1) <= .0100001
            assert math.isfinite(a['confidence']) and 0 <= a['confidence'] <= 1
            if q['type']=='choice': assert a['choice'] in keys
            else:
                assert math.isfinite(a['score']) and 0 <= a['score'] <= len(keys)-1
                assert set(a['legend']) == keys
    assert response['usage']['input_tokens'] >= 0

def policy(case, answers):
    kind = case['group']
    if kind == 'triage':
        a=answers['route']
        return a['choice'] if answers['sufficient']['noul'] >= .8 and a['confidence'] >= .8 else 'human_review'
    if kind == 'security':
        # No negative score can approve code or suppress a deterministic scanner.
        return 'priority_verification' if max(answers[x]['noul'] for x in ('toctou','supply_chain')) >= .5 else 'standard_verification'
    if kind == 'interest':
        if case['state'].get('state') != 'open': return 'skip_closed'
        a=answers['interest']
        return 'shortlist' if a['score'] >= 2 and a['confidence'] >= .5 else 'keep_in_backlog'
    return 'observe_only'

def check(rows):
    checks=[]
    for row in rows:
        validate(row['request'],row['response'])
        assert row['decision']==policy(row['case'],row['response']['answers'])
        for key,expect in row['case'].get('expected',{}).items():
            a=row['response']['answers'][key]
            actual=a.get('choice',a.get('noul',a.get('score')))
            passed=(expect[0] <= actual <= expect[1]) if isinstance(expect,list) else actual==expect
            checks.append({'id':row['case']['id'],'question':key,'expected':expect,'actual':actual,'passed':passed})
    return checks

def main():
    p=argparse.ArgumentParser();p.add_argument('--live',action='store_true');p.add_argument('--check',type=pathlib.Path);args=p.parse_args()
    if args.check:
        rows=json.loads(args.check.read_text())['runs']
    elif args.live:
        key=os.environ.get('TYPESAFE_API_KEY') or subprocess.check_output(['security','find-generic-password','-s','openhands','-a','TYPESAFE_API_KEY','-w'],text=True).strip()
        rows=[]
        for c in json.loads((ROOT/'cases.json').read_text()):
            req={'model':MODEL,'state':c['state'],'questions':c['questions']}
            start=time.perf_counter()
            # Bounded retries only for provider capacity / transient server errors.
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(urllib.request.Request('https://api.typesafe.ai/v1/systemone',data=json.dumps(req).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'}),timeout=30) as r: response=json.load(r)
                    break
                except urllib.error.HTTPError as e:
                    if e.code not in (429,500,502,503,504,529) or attempt==2: raise RuntimeError(f'Provider HTTP {e.code}') from None
                    time.sleep(min(4,2**attempt))
            validate(req,response)
            row={'case':c,'request':req,'response':response,'elapsed_ms':round((time.perf_counter()-start)*1000,2),'decision':policy(c,response['answers'])}
            rows.append(row);print(c['id'],row['decision'],flush=True)
            # Save each completed request so an interrupted run leaves evidence.
            (ROOT/'results.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows},indent=2)+'\n')
    else: p.error('choose --live or --check results.json')
    checks=check(rows)
    summary={'requests':len(rows),'model':MODEL,'input_tokens':sum(r['response']['usage']['input_tokens'] for r in rows),'median_ms':statistics.median(r['elapsed_ms'] for r in rows),'p95_ms':sorted(r['elapsed_ms'] for r in rows)[math.ceil(.95*len(rows))-1],'assertions':len(checks),'passed':sum(c['passed'] for c in checks),'checks':checks,'cases_sha256':hashlib.sha256((ROOT/'cases.json').read_bytes()).hexdigest()}
    summary['estimated_input_cost_usd']=summary['input_tokens']*.042/1_000_000
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
