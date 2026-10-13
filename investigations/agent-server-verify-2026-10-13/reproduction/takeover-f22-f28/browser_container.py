import json, os, pathlib, subprocess, time, socket
root=pathlib.Path('/workspace/verification-artifacts');repo=pathlib.Path('/workspace/agent-sdk-verify');here=root/'takeover-f22-f28';out=root/'family-results'
cli=str(repo/'.agents/skills/verify-agent-server/scripts/control-agent-server')
base=['env','-u','DOCKER_HOST','-u','DOCKER_CONTEXT','-u','DOCKER_TLS','-u','DOCKER_TLS_VERIFY','-u','DOCKER_CERT_PATH','docker','--host=unix:///var/run/docker.sock']
def call(cmd,save=None):
 p=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if save:save.write_text(p.stdout);save.with_suffix('.stderr.txt').write_text(p.stderr)
 if p.returncode:raise RuntimeError('command failed; see saved output: '+str(save))
 return p.stdout.strip()
results=[]
for attempt in (1,2):
 name='qa-f27-browser-path-'+str(attempt)
 run=None
 try:
  probe_socket=socket.socket();probe_socket.bind(('127.0.0.1',0));fixed_port=probe_socket.getsockname()[1];probe_socket.close()
  call(base+['run','-d','--name',name,'-p','127.0.0.1:'+str(fixed_port)+':8000','--mount','type=bind,src='+str(here/'playwright')+',dst=/qa-playwright,readonly','--mount','type=bind,src=/usr/lib/chromium/chromium,dst=/qa-real-chromium,readonly','--mount','type=bind,src=/etc/ssl/certs/ca-certificates.crt,dst=/run/qa-ca.pem,readonly','-e','SSL_CERT_FILE=/run/qa-ca.pem','-e','HOME=/tmp/qa-browser-home','-e','OH_PERSISTENCE_DIR=/tmp/qa-browser-state','-e','PLAYWRIGHT_BROWSERS_PATH=/qa-playwright','qa-agent-server:acca181a-local-layout','--host','0.0.0.0','--port','8000'],out/f'F27-browser-container-{attempt}-launch.txt')
  hostport=call(base+['port',name,'8000/tcp']).rsplit(':',1)[1]
  run=call([cli,'attach','--url','http://127.0.0.1:'+hostport,'--name',name,'--print-run'])
  rp=pathlib.Path(run);(rp/'fixtures').mkdir(exist_ok=True);(rp/'fixtures/container-name.txt').write_text(name)
  # Initial container startup may still be importing modules.
  ready_path=out/f'F27-browser-container-{attempt}-ready.json'
  for _ in range(90):
   probe=subprocess.run([cli,'api','GET','/alive','--run',run,'--expect','200','--quiet'],cwd=repo,text=True,capture_output=True)
   ready_path.write_text(probe.stdout)
   if probe.returncode==0:break
   time.sleep(1)
  else:raise RuntimeError('container did not become ready; see '+str(ready_path))
  text=call([str(repo/'.venv/bin/python'),str(here/'run-map.py'),'map','run','--file','F27-browser-container.md','--run',run,'--record','--keep-going','--timeout','180'],out/f'F27-browser-container-{attempt}.json')
  j=json.loads(text);results.append({'run':run,'summary':j['summary'],'result':str(out/f'F27-browser-container-{attempt}.json')})
 finally:
  logs=subprocess.run(base+['logs',name],cwd=repo,text=True,capture_output=True)
  (out/f'F27-browser-container-{attempt}-private-startup.log').write_text(logs.stdout+logs.stderr)
  subprocess.run(base+['rm','-f',name],cwd=repo,text=True,capture_output=True)
  if run:subprocess.run([cli,'stop','--run',run],cwd=repo,text=True,stdout=(out/f'F27-browser-container-{attempt}-stop.json').open('w'),stderr=subprocess.DEVNULL)
(out/'F27-browser-container-combined.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
