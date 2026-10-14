import sys,os,subprocess,json
from pathlib import Path
phase,run=sys.argv[1:3]
cli=str(Path.cwd()/'.agents/skills/verify-openhands/scripts/control-openhands')
env=os.environ.copy();env['OH_VERIFY_RUN']=run
records=[]
def call(*args):
    p=subprocess.run([cli,*args],env=env,text=True,capture_output=True)
    try: result=json.loads(p.stdout)
    except Exception: print(p.stdout,p.stderr,flush=True);raise
    if p.returncode or not result.get('ok'): print(args,result,p.stderr,flush=True);raise SystemExit(1)
    return result
def browser(*args): return call('browser',*args)
def inspect(name,selector,feature,theme):
    expression='''(() => {const e=SELECTOR;if(!e) throw Error('Missing target');const s=getComputedStyle(e);const b=[];for(let p=e;p;p=p.parentElement){const c=getComputedStyle(p);if(c.backgroundColor!=='rgba(0, 0, 0, 0)')b.push({color:c.backgroundColor,opacity:c.opacity});}return {color:s.color,border:s.borderTopColor,background:b,text:e.textContent,invalid:e.getAttribute('aria-invalid'),danger:s.getPropertyValue('--oh-color-danger'),bounds:{width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height},pageOverflow:document.documentElement.scrollWidth>innerWidth};})()'''.replace('SELECTOR',selector)
    data=browser('eval',expression)['value']
    records.append({'phase':phase,'theme':theme,'target':name,'style':data})
    if theme=='Light+' and name not in ['field-border','required-marker']:
        for vp in ['desktop','phone']:
            browser('viewport',vp)
            shot=browser('screenshot','--feature',feature,'--name',name+'-light-plus-'+vp+'-'+phase)
            print(json.dumps({'capture':shot['path']}),flush=True)
            records.append({'phase':phase,'theme':theme,'target':name,'viewport':vp,'screenshot':shot['path']})
        browser('viewport','desktop')
    print(json.dumps(records[-1] if theme!='Light+' else {'checked':name,'theme':theme,'style':data}),flush=True)
for theme in ['Light+','Solarized Light','OpenHands-Neutral','OpenHands-DeepSea','OpenHands-Neo']:
    browser('viewport','desktop');browser('goto','/settings/app');browser('choose','testid=color-theme-input',theme)
    browser('goto','/settings/agents');browser('click','testid=add-agent-profile');browser('fill','testid=agent-profile-name-input','bad name!')
    inspect('profile-name',"document.getElementById(document.querySelector('[data-testid=agent-profile-name-input]').getAttribute('aria-describedby'))",'F13.name-validation',theme)
    assert browser('attr','testid=agent-profile-name-input','aria-invalid')['aria-invalid']=='true'
    assert browser('enabled','testid=save-agent-profile-btn')['enabled'] is False
    browser('click','testid=backend-selector');browser('click','testid=manage-backends-menu-item');browser('click','testid=manage-backends-edit-Local');browser('wait','testid=edit-backend-name')
    browser('fill','testid=edit-backend-name','');browser('fill','testid=edit-backend-host','not a url');browser('press','Tab');browser('wait','testid=edit-backend-name-error')
    inspect('field-errors',"document.querySelector('[data-testid=edit-backend-name-error]')",'F25.edit-backend',theme)
    inspect('field-border',"document.querySelector('[data-testid=edit-backend-name]')",'F25.edit-backend-border',theme)
    inspect('required-marker',"document.querySelector('[data-testid=edit-backend-name]').closest('label').querySelector('[aria-hidden]')",'F25.edit-backend-marker',theme)
    browser('click','testid=edit-backend-cancel');browser('click','testid=manage-backends-done')
    browser('goto','/settings/secrets');browser('click','testid=add-secret-button');browser('fill','testid=name-input','OPENHANDS_AUTOMATION_API_KEY');browser('fill','testid=value-input','dummy-screenshot-value');browser('click','testid=submit-button');browser('wait-text','Secret already exists')
    inspect('duplicate-secret',"document.querySelector('[data-testid=add-secret-form] > p')",'F14.create-validation',theme)
Path('/tmp/odie-theme-errors-'+phase+'-evidence.json').write_text(json.dumps(records,indent=2))
print('ALL THREE VALIDATION STATES CHECKED IN ALL FIVE THEMES',flush=True)
