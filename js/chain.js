/* Markov chain walk */
(function(){
  const svg=$('#chainsvg');if(!svg)return;const NS='http://www.w3.org/2000/svg';
  const S=[{n:'Unaware',x:100,y:175},{n:'Aware',x:300,y:120},{n:'Interested',x:500,y:175},{n:'Considering',x:700,y:120},{n:'Customer',x:900,y:175}];
  const LOST={n:'Lost',x:500,y:345};
  const MODES={A:[.28,.34,.30,.22],B:[.64,.58,.52,.46]};
  let mode='A',tally={w:0,t:0};
  const R=n=>n===4?42:36;
  const el=(t,a={},p=svg)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e};
  const fwd=[],drop=[],nodes=[],lblF=[],lblD=[];
  function fPath(i){const a=S[i],b=S[i+1],cx=(a.x+b.x)/2,cy=Math.min(a.y,b.y)-34;return `M${a.x},${a.y} Q${cx},${cy} ${b.x},${b.y}`}
  function dPath(i){const a=S[i];return `M${a.x},${a.y} Q${a.x},${LOST.y} ${LOST.x},${LOST.y}`}
  for(let i=0;i<4;i++){fwd.push(el('path',{d:fPath(i),class:'cs-edge'}));}
  for(let i=0;i<4;i++){drop.push(el('path',{d:dPath(i),class:'cs-edge',style:'stroke-dasharray:3 6;opacity:.7'}))}
  const place=(p,t)=>{const L=p.getTotalLength(),pt=p.getPointAtLength(L*t);return pt};
  for(let i=0;i<4;i++){const q=place(fwd[i],.5);lblF.push(el('text',{class:'cs-p',x:q.x,y:q.y-12}))}
  for(let i=0;i<4;i++){const q=place(drop[i],.5);const dx=i<2?-18:18;lblD.push(el('text',{class:'cs-p',x:q.x+(i===2?20:dx),y:q.y+(i===2?0:2),style:'opacity:.75'}))}
  S.forEach((s,i)=>{const g=el('g',{class:'cs-node',transform:`translate(${s.x},${s.y})`});el('circle',{r:R(i)},g);el('text',{y:5},g).textContent=s.n.length>9?s.n:s.n;nodes.push(g);g.querySelector('text').setAttribute('y',R(i)+26)});
  /* labels sit under nodes, so put names below */
  const gl=el('g',{class:'cs-node',transform:`translate(${LOST.x},${LOST.y})`});el('circle',{r:30},gl);const lt=el('text',{y:56},gl);lt.textContent='Lost';nodes.push(gl);
  /* inner glyphs: small dot in each node */
  S.forEach((s,i)=>{const c=nodes[i].querySelector('circle');});
  const tok=el('circle',{r:7,class:'cs-token',cx:S[0].x,cy:S[0].y});

  function paint(){
    const p=MODES[mode];
    p.forEach((v,i)=>{lblF[i].textContent=v.toFixed(2);lblD[i].textContent=(1-v).toFixed(2)});
    const chance=p.reduce((a,b)=>a*b,1)*100;
    tweenRate(chance);
  }
  let shown=0,tw=0;
  function tweenRate(to){
    cancelAnimationFrame(tw);const from=shown,t0=performance.now();
    if(reduce){shown=to;$('#rate').textContent=to.toFixed(1)+'%';return}
    (function s(t){const p=clamp((t-t0)/700),e=1-Math.pow(1-p,3);shown=from+(to-from)*e;$('#rate').textContent=shown.toFixed(1)+'%';if(p<1)tw=requestAnimationFrame(s)})(t0);
  }
  /* walker */
  let state='idle',path=null,pt0=0,dur=720,cur=0,visible=true,gen=0,wait=0;
  const hotClear=()=>{svg.querySelectorAll('.hot').forEach(e=>e.classList.remove('hot'))};
  function setTok(p,t){const L=p.getTotalLength(),q=p.getPointAtLength(L*t);tok.setAttribute('cx',q.x);tok.setAttribute('cy',q.y)}
  function startRun(){hotClear();cur=0;nodes[0].classList.add('hot');tok.setAttribute('cx',S[0].x);tok.setAttribute('cy',S[0].y);wait=500;state='wait';next=stepFrom}
  let next=startRun;
  function stepFrom(){
    const p=MODES[mode][cur],win=Math.random()<p;
    path=win?fwd[cur]:drop[cur];path.classList.add('hot');pt0=performance.now();dur=win?640:560;state='move';
    path._to=win?cur+1:-1;
  }
  function arrive(){
    const to=path._to;
    if(to<0){nodes[5].classList.add('hot');tok.setAttribute('cx',LOST.x);tok.setAttribute('cy',LOST.y);tally.w++;end()}
    else{cur=to;nodes[cur].classList.add('hot');if(cur===4){tally.w++;tally.t++;end()}else{wait=180;state='wait';next=stepFrom}}
  }
  function end(){state='wait';wait=1100;next=startRun;$('#tally').textContent=`${tally.w} walks so far, ${tally.t} reached Customer.`}
  let last=0;
  function loop(ts){
    const dt=ts-last;last=ts;
    if(visible&&!document.hidden){
      if(state==='wait'){wait-=dt;if(wait<=0)next()}
      else if(state==='move'){const t=clamp((ts-pt0)/dur),e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;setTok(path,e);if(t>=1)arrive()}
    }
    requestAnimationFrame(loop);
  }
  function setMode(m){
    mode=m;$('#mA').setAttribute('aria-pressed',m==='A');$('#mB').setAttribute('aria-pressed',m==='B');
    tally={w:0,t:0};$('#tally').textContent='Starting a fresh set of walks.';paint();state='wait';wait=300;next=startRun;
  }
  $('#mA').onclick=()=>setMode('A');$('#mB').onclick=()=>setMode('B');
  const note=$('.panel .note');note.innerHTML='Illustrative probabilities for explaining the idea. Not client results. <span id="tally"></span>';
  paint();
  if(reduce){nodes.forEach(n=>n.classList.add('hot'));fwd.forEach(f=>f.classList.add('hot'));$('#tally').textContent='Motion is reduced. Switch views to compare the chance of reaching Customer.'}
  else{
    if('IntersectionObserver' in window)new IntersectionObserver(es=>{visible=es[0].isIntersecting}).observe(svg);
    startRun();requestAnimationFrame(loop);
  }
})();

