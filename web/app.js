const $ = id => document.getElementById(id);
const displayNames = {s1:'Alex Morgan (you)',s2:'Jamie Chen',s3:'Sam Rivera'};
const personName = id => displayNames[id] || 'Course participant';
const teamNames = {'team-a':'Team Maple','team-b':'Team Cedar','team-c':'Team Willow','team-d':'Team Birch','team-e':'Team Oak','team-f':'Team Aspen','team-g':'Team Elm','team-h':'Team Pine'};
const modules = {
workshops:{title:'Workshop Planner',heading:'Your next workshop',description:'Browse course sessions and reserve a seat.',list:'Workshop schedule',yours:'My bookings',roster:'Attendee lists',button:'Sign up',empty:'You have no workshop bookings.',context:'Alex Morgan · Available Monday 10:00 and Tuesday 14:00',steps:['Available sessions','Session order','Registration'],icon:'◷'},
reviews:{title:'Peer Review Board',heading:'The review desk',description:'Pick a project from another team and become a reviewer.',list:'Projects awaiting review',yours:'My review queue',roster:'Project reviewers',button:'Take review',empty:'Your review queue is empty.',context:'Alex Morgan · Team Maple',steps:['Reviewable projects','Project order','Assignment'],icon:'▤'},
buddies:{title:'Study Buddy Finder',heading:'Find your study circle',description:'Meet other students in a shared study group.',list:'Study groups',yours:'My groups',roster:'Group members',button:'Join group',empty:'You have not joined a group yet.',context:'Alex Morgan · Study language: English',steps:['Available groups','Group order','Membership'],icon:'◎'}
};
let task = new URLSearchParams(location.search).get('task') || 'workshops';
if (!Object.hasOwn(modules,task)) task='workshops';
let version=0, actions=[], busy=false;
function el(tag,text,cls) {const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n;}
function refusalReason(data) {
 const last=data.actions.at(-1), r=data.records.find(r=>r.item_id===last.item_id);
 const previous=data.actions.slice(0,-1).filter(a=>a.accepted).map(a=>a.item_id);
 if(previous.includes(last.item_id))return 'You already have this '+(task==='workshops'?'booking':task==='reviews'?'review assignment':'membership')+'.';
 if(previous.length>=2)return task==='workshops'?'You can book at most 2 workshops. Cancel a booking before choosing another.':task==='reviews'?'You can take at most 2 reviews. Remove an assignment before choosing another.':'You can join at most 2 groups. Leave a group before choosing another.';
 if(!r)return 'This option no longer exists.';
 if(r[data.member_field].length>=r.capacity)return task==='reviews'?'This project already has all its reviewers. There are no review slots left.':task==='buddies'?'This group is full. There are no places left.':'There are no places left.';
 if(task==='workshops'&&!['Mon 10','Tue 14'].includes(r.slot))return 'This session is outside your available hours.';
 if(task==='reviews'&&r.team==='team-a')return 'This is Team Maple’s project — your own team. Choose a project from another team.';
 if(task==='buddies'&&r.language!=='English')return `This group studies in ${r.language}. Alex speaks English. Choose an English-speaking group.`;
 return 'The request failed even though this option has space and is available to you.';
}
function paint(data){
 const m=modules[task], title=id=>data.records.find(r=>r.item_id===id)?.title||id;
 $('cards').replaceChildren();$('count').textContent=data.ranked.length;
 for(const [i,id] of data.ranked.entries()){
  const r=data.records.find(r=>r.item_id===id);if(!r)throw Error('Unknown item in list: '+id);
  const card=el('article','','card'); const members=r[data.member_field];
  const top=el('div','','card-top');top.append(el('span',m.icon,'card-icon'),el('span',r.slot||teamNames[r.team]||r.language,'badge'));card.append(top,el('h3',r.title));
  card.append(el('p',r.topic.charAt(0).toUpperCase()+r.topic.slice(1),'topic'));
  const bottom=el('div','','card-bottom');bottom.append(el('span',`${members.length} / ${r.capacity} ${task==='reviews'?'reviewers':'members'}`));
  const button=el('button',data.commitments.includes(id)?'Request again':m.button,'primary');button.disabled=busy;button.onclick=()=>refresh([...actions,id]);bottom.append(button);card.append(bottom);$('cards').append(card);
 }
 if(!data.ranked.length)$('cards').append(el('p','Nothing available right now.','empty'));
 $('commitments').replaceChildren();
 if(task==='reviews')$('student-title').textContent=`My review queue · ${data.commitments.length} / 2`;
 if(task==='buddies')$('student-title').textContent=`My groups · ${data.commitments.length} / 2`;
 for(const id of data.commitments){const row=el('div','','saved-item');row.append(el('span',title(id)));const record=data.records.find(r=>r.item_id===id);row.append(el('small',record?.slot||teamNames[record?.team]||record?.language||''));const again=el('button',task==='reviews'?'Request same review':task==='buddies'?'Request to join again':'Request again');again.onclick=()=>refresh([...actions,id]);row.append(again);const remove=el('button',task==='workshops'?'Cancel booking':task==='reviews'?'Remove assignment':'Leave group');remove.onclick=async()=>{const currentTask=task;const result=await refresh(actions.filter(action=>action!==id));if(result&&task===currentTask){const remaining=result.records.find(r=>r.item_id===id);const removed=!result.commitments.includes(id)&&!remaining?.[result.member_field].includes('s1');$('outcome').replaceChildren(el('p',removed?`${title(id)} — ${task==='workshops'?'booking cancelled':task==='reviews'?'assignment removed':'you left the group'}.`:'Could not remove this choice.',removed?'success':'failure'));}};row.append(remove);$('commitments').append(row);}
 if(!data.commitments.length)$('commitments').append(el('p',m.empty,'empty'));
 $('records').replaceChildren(...data.records.map(r=>{const row=el('div','','roster-row');row.append(el('strong',r.title),el('span',r[data.member_field].map(personName).join(', ')||'Nobody yet'));return row;}));
 $('outcome').replaceChildren();
 if(!data.actions.length){$('outcome').append(el('p','No activity yet.','muted'));return;}
 // Show the actual backend result, including an incomplete two-sided update.
 const last=data.actions.at(-1),record=data.records.find(r=>r.item_id===last.item_id);
 const saved=data.commitments.includes(last.item_id)&&record?.[data.member_field].includes('s1');
 const msg=last.accepted?(saved?`${title(last.item_id)} — ${task==='workshops'?'booking confirmed':task==='reviews'?'added to your review queue':'you joined the group'}.`:'The request was accepted, but could not be saved correctly.'):`Could not ${m.button.toLowerCase()}: ${title(last.item_id)}. ${refusalReason(data)}`;
 $('outcome').append(el('p',msg,last.accepted&&saved?'success':'failure'));
}
async function refresh(next=actions){
 const v=++version;actions=next;busy=true;$('error').hidden=true;
 document.querySelectorAll('#cards button, #commitments button').forEach(b=>b.disabled=true);
 const params=new URLSearchParams({task});actions.forEach(a=>params.append('action',a));
 try{const response=await fetch('/api/preview?'+params);const data=await response.json();if(v!==version)return;if(!response.ok)throw Error(data.error||'Unable to load data');busy=false;paint(data);actions=data.actions.filter(a=>a.accepted).map(a=>a.item_id);return data;}
 catch(e){if(v!==version)return;$('error').hidden=false;$('error').textContent='This page could not load its data. '+e.message;}
 finally{if(v===version)busy=false;}
}
function selectTask(next){task=next;actions=[];document.body.dataset.task=task;const m=modules[task];
 for(const [id,value]of Object.entries({'module-label':m.title,'flow-title':m.heading,'context':m.context,'description':m.description,'list-title':m.list,'student-title':m.yours,'record-title':m.roster}))$(id).textContent=value;
 document.querySelectorAll('[data-task]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.task===task)));
 history.replaceState(null,'','?task='+task);showPending();refresh([]);pollChecks();}
 document.querySelectorAll('[data-task]').forEach(b=>b.onclick=()=>selectTask(b.dataset.task));
 $('reset').onclick=()=>refresh([]);$('refresh').onclick=()=>refresh();
let checking = false;
let lastChecked = {};
const stepNames = ['Suitable options', 'Ordering', 'Complete the action'];
function showPending(message = 'Checking saved code...') {
  $('check-summary').textContent = message;
  $('step-status').replaceChildren();
  $('check-note').textContent = 'Checks update automatically after you save.';
  document.querySelector('.progress-panel').classList.remove('complete', 'error');
}
function renderChecks(data) {

  const panel = document.querySelector('.progress-panel');
  panel.classList.toggle('complete', Boolean(data.all_passed));
  panel.classList.toggle('error', Boolean(data.error));
  $('step-status').replaceChildren();
  for (const step of data.steps || []) {
    const box = el('div', '', 'step-state' + (step.passed ? ' passed' : ''));
    box.append(el('strong', `${step.step}. ${modules[task].steps[step.step - 1]}`));
    box.append(el('span', step.passed ? 'Passed' : 'Not yet complete'));
    $('step-status').append(box);
  }
  const completed = (data.steps || []).filter(step => step.passed).length;
  $('check-summary').textContent = data.error ? 'Checks could not finish' :
    data.all_passed ? 'All 3 subtasks passed' : `${completed} of 3 subtasks passed`;
  $('check-note').textContent = data.log_warning || (data.all_passed ?
    'Save your chat as JSON, answer the form, then continue in the order we assigned.' :
    'Checks update automatically when code is saved.');
}
async function pollChecks(retry = false) {
  if (checking) return;
  checking = true;
  const requestedTask = task;
  try {
    const response = await fetch('/api/status?task=' + requestedTask + (retry ? '&retry=1' : ''),
      {signal: AbortSignal.timeout(12000)});
    const data = await response.json();
    if (requestedTask !== task) return;
    if (!response.ok) throw new Error(data.error || 'Checks unavailable');
    if (data.stale) { showPending('Changes detected. Checking the latest saved code...'); return; }
    renderChecks(data);
    if (lastChecked[task] !== data.fingerprint) {
      lastChecked[task] = data.fingerprint;
      await refresh();
    }
  } catch (error) {
    if (requestedTask !== task) return;
    showPending('Not connected to the local app');
    $('check-note').textContent = 'Keep the Open HASE Lab task running in VS Code. The page will reconnect automatically.';
  } finally {
    checking = false;
  }
}
$('retry-checks').addEventListener('click', () => pollChecks(true));
selectTask(task);
setInterval(() => { if (!document.hidden) pollChecks(); }, 2000);
document.addEventListener('visibilitychange', () => { if (!document.hidden) pollChecks(); });
