"""Real local Docker lifecycle checks using frozen-source verification image.
No credentials are printed. Launches and cleans only its own runs.
"""
import json, os, subprocess, sys, time, uuid
from pathlib import Path
import httpx
from openhands.sdk.workspace import RemoteWorkspace

CLI = '/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts/control-agent-server'
CHECKOUT = '/workspace/agent-sdk-verify'
IMAGE = os.environ.get('QA_DOCKER_IMAGE', 'qa-agent-server:acca181a-local-uid')
mode = sys.argv[1]
owned = []
records = []

def emit(**record):
    records.append(record)
    print(json.dumps(record, sort_keys=True), flush=True)

def command(*args):
    p = subprocess.run([CLI,*args],capture_output=True,text=True,timeout=180)
    if p.returncode:
        # CLI ordinary-mode output redacts run-owned credentials.
        raise RuntimeError('CLI failed: '+p.stdout[-1000:]+' '+p.stderr[-1000:])
    return p.stdout.strip()

def launch(suffix, policies):
    config = dict(conversation_runtime='docker',conversation_image=IMAGE,
                  conversation_container_memory='1g',conversation_container_cpus=1,
                  conversation_container_pids_limit=256, **policies)
    run = Path(command('launch','--new','--name', 'f31-'+suffix if mode=='storage' else 'f33-'+suffix,
                        '--checkout', CHECKOUT,'--env','DOCKER_HOST=unix:///var/run/docker.sock',
                        '--config-json',json.dumps(config),'--print-run'))
    owned.append(run)
    info = json.loads((run/'run.json').read_text())
    key = (run/'private/session_api_key').read_text().strip()
    client = httpx.Client(base_url=info['url'],headers={'X-Session-API-Key':key},timeout=180)
    client.get('/openapi.json').raise_for_status()
    command('doctor','--run',str(run))
    emit(stage='launched',run=str(run),image=IMAGE,policy=policies)
    return run,client,key

def request(client,method,path,status=200,**kw):
    response=client.request(method,path,**kw)
    assert response.status_code==status, (method,path,response.status_code,response.text[:1000])
    return response.json() if response.content else None

def create(client):
    # Docker fills an omitted workspace with its own /workspace mount.
    body={'agent_settings':{'agent_kind':'openhands','llm':{'model':'openai/qa-placeholder',
          'api_key':'qa-placeholder','base_url':'http://127.0.0.1:9/v1','num_retries':0},'tools':[]},'autotitle':False}
    response=client.post('<redacted:session-cookie>',json=body)
    assert response.status_code in (200,201),(response.status_code,response.text[:1000])
    return response.json()['id']

try:
    if mode=='lifecycle':
        run,client,server_key=launch('sdk-lifecycle',{})
        cid=create(client)
        ws=RemoteWorkspace(host=str(client.base_url).rstrip('/'),api_key=server_key,
                           working_dir='/workspace',runtime_conversation_id=uuid.UUID(cid))
        worker_key=ws.get_runtime_session_key()
        assert worker_key and worker_key!=server_key
        os.environ['OPENHANDS_API_KEY']=worker_key
        before=request(client,'GET',f'<redacted:session-cookie>/{cid}/runtime')
        assert before['runtime_status']=='available'
        count=request(client,'GET',f'<redacted:session-cookie>/{cid}/events/count')
        ws.release_runtime()
        after=request(client,'GET',f'<redacted:session-cookie>/{cid}/runtime')
        history=request(client,'GET',f'<redacted:session-cookie>/{cid}')
        assert after['runtime_status']=='missing' and after['can_resume'] is True,after
        assert request(client,'GET',f'<redacted:session-cookie>/{cid}/events/count')==count
        assert history['id']==cid
        emit(stage='sdk-runtime-lifecycle',cid=cid,key_present=True,key_differs_from_server=True,
             released=True,runtime_status=after['runtime_status'],can_resume=after['can_resume'],history_readable=True)
        print('QA_F33_RUNTIME_LIFECYCLE_VERIFIED',flush=True)
    elif mode=='storage':
        retention,rc,_=launch('retention',{'conversation_storage_retention_days':0.00002})
        budget,bc,_=launch('budget',{'conversation_storage_disk_budget':0.01})
        rid=create(rc);bid=create(bc)
        rpath=f'<redacted:session-cookie>/{rid}';bpath=f'<redacted:session-cookie>/{bid}'
        request(rc,'POST',rpath+'/events',json={'role':'user','content':[{'type':'text','text':'QA_F31_ARCHIVE_KEEP_EVENT'}],'run':False})
        initial_count=request(rc,'GET',rpath+'/events/count')
        request(rc,'DELETE',rpath+'/runtime',status=204)
        request(bc,'DELETE',bpath+'/runtime',status=204)
        root=budget/'home/.openhands/runtime-data'/bid.replace('-','')/'workspace'
        assert root.is_dir()
        subprocess.run(['git','init','-q',str(root)],check=True)
        (root/'.gitignore').write_text('node_modules/\n.venv/\n')
        (root/'tracked.txt').write_text('tracked-preserved\n')
        (root/'untracked.txt').write_text('untracked-preserved\n')
        subprocess.run(['git','-C',str(root),'add','.gitignore','tracked.txt'],check=True)
        for name in ['node_modules','.venv']:
            (root/name).mkdir();(root/name/'rebuildable').write_bytes(b'x'*1024)
        archive=retention/'home/.openhands/runtime-control'/(rid.replace('-','')+'.archived.json')
        rdata=retention/'home/.openhands/runtime-data'/rid.replace('-','')
        deadline=time.monotonic()+380
        while time.monotonic()<deadline and (not archive.exists() or (root/'node_modules').exists() or (root/'.venv').exists()):
            emit(stage='waiting-for-real-300s-maintenance',archive_marker=archive.exists(),dependencies_remain=(root/'node_modules').exists() or (root/'.venv').exists())
            time.sleep(20)
        assert archive.is_file(), 'retention marker absent after maintenance window'
        assert not rdata.exists(), 'archived runtime directory remains'
        runtime=request(rc,'GET',rpath+'/runtime')
        assert runtime['runtime_status']=='missing' and runtime['can_resume'] is False,runtime
        assert request(rc,'GET',rpath+'/events/count')==initial_count
        request(rc,'GET',rpath+'/events/search')
        request(rc,'GET',rpath)
        for route,body in [('/run',None),('/events',{'role':'user','content':[{'type':'text','text':'should-not-append'}],'run':False}),('/runtime/reprovision',None)]:
            response=request(rc,'POST',rpath+route,status=410,json=body)
            assert response['detail']=='Conversation runtime was archived; its history is read-only',response
        assert request(rc,'GET',rpath+'/events/count')==initial_count
        assert not (root/'node_modules').exists() and not (root/'.venv').exists()
        assert (root/'tracked.txt').read_text()=='tracked-preserved\n'
        assert (root/'untracked.txt').read_text()=='untracked-preserved\n'
        assert (root/'.gitignore').is_file() and (root/'.git').is_dir()
        for run in [retention,budget]:
            command('logs','--run',str(run),'--grep','Conversation storage: freed','--expect-min','1')
        emit(stage='storage-retention-and-budget',retention_run=str(retention),budget_run=str(budget),
             archive_marker=True,runtime_directory_removed=True,history_readable=True,
             archived_writes_status=410,event_count_preserved=True,ignored_dirs_removed=True,
             tracked_and_untracked_files_preserved=True,maintenance_seconds=300)
        print('QA_F31_STORAGE_VERIFIED',flush=True)
    else:
        raise ValueError(mode)
finally:
    for run in reversed(owned):
        result=subprocess.run([CLI,'stop','--run',str(run)],capture_output=True,text=True,timeout=90)
        emit(stage='own-run-cleanup',run=str(run),cli_exit=result.returncode)
    destination=Path(os.environ['AGENT_SERVER_VERIFY_RUN'])/'fixtures'/('docker-'+mode+'-results.json')
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(records,indent=2)+'\n')
