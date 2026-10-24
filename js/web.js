/* hero web canvas */
(function(){
  const cv=$('#web');if(!cv)return;const ctx=cv.getContext('2d'),hero=cv.closest('.hero,.phero,.nf');
  const touch=matchMedia('(pointer:coarse)').matches;
  let W=0,H=0,dpr=1,nodes=[],adj=[],sparks=[],rings=[],lit=new Map(),litN=[],mouse={x:-9999,y:-9999},run=true,last=0,auto=0;
  const rnd=(a,b)=>a+Math.random()*(b-a);
  function init(){
    const n=Math.max(touch?18:26,Math.min(touch?64:88,Math.round(W*H/(touch?22000:15500))));
    nodes=[];for(let i=0;i<n;i++){const hub=Math.random()<.09;nodes.push({x:rnd(0,W),y:rnd(0,H),vx:rnd(-.22,.22),vy:rnd(-.22,.22),r:hub?rnd(6,10):rnd(1.8,3.6),hub})}
    lit.clear();litN=new Array(n).fill(0);sparks=[];rings=[];
  }
  function size(){
    const r=cv.getBoundingClientRect();dpr=Math.min(touch?1.4:2,devicePixelRatio||1);W=r.width;H=r.height;
    cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);init();draw(0);
  }
  function nearest(x,y){let b=0,bd=1e9;nodes.forEach((n,i)=>{const d=(n.x-x)**2+(n.y-y)**2;if(d<bd){bd=d;b=i}});return b}
  function ignite(i){
    const a=i,nb=adj[a]||[];if(!nb.length)return;
    sparks.push({a,b:nb[Math.floor(Math.random()*nb.length)],t:0,hops:0,prev:-1});litN[a]=1;
  }
  function draw(dt){
    ctx.clearRect(0,0,W,H);
    const maxD=Math.min(175,Math.max(110,W/7));
    adj=nodes.map(()=>[]);
    for(const n of nodes){
      if(!reduce){n.x+=n.vx*dt*.06;n.y+=n.vy*dt*.06}
      if(n.x<-20)n.x=W+20;if(n.x>W+20)n.x=-20;if(n.y<-20)n.y=H+20;if(n.y>H+20)n.y=-20;
      const dx=mouse.x-n.x,dy=mouse.y-n.y,d=Math.hypot(dx,dy);
      if(d<220&&d>1&&!reduce){const f=(1-d/220)*.018*dt*.06;n.x+=dx*f;n.y+=dy*f}
    }
    ctx.lineWidth=1;
    for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
      const a=nodes[i],b=nodes[j],d=Math.hypot(a.x-b.x,a.y-b.y);
      if(d<maxD){adj[i].push(j);adj[j].push(i);
        const al=(1-d/maxD);ctx.strokeStyle=`rgba(112,112,122,${al*.42})`;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
        const k=i+'-'+j,L=lit.get(k);if(L>0.02){ctx.strokeStyle=`rgba(10,10,11,${L*.9})`;ctx.lineWidth=1.8;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.lineWidth=1;lit.set(k,L*Math.pow(.985,dt/16))}
      }
    }
    for(let i=0;i<nodes.length;i++){
      const n=nodes[i],md=Math.hypot(mouse.x-n.x,mouse.y-n.y);
      if(md<200){ctx.strokeStyle=`rgba(10,10,11,${(1-md/200)*.5})`;ctx.beginPath();ctx.moveTo(n.x,n.y);ctx.lineTo(mouse.x,mouse.y);ctx.stroke()}
      const L=litN[i]=Math.max(0,litN[i]*Math.pow(.99,dt/16)),near=md<200?(1-md/200):0,t=Math.max(L,near*.8);
      ctx.beginPath();ctx.arc(n.x,n.y,n.r+(t*3),0,6.283);
      if(n.hub){ctx.fillStyle=t>.05?`rgba(10,10,11,${.25+t*.75})`:'rgba(190,190,198,.55)';ctx.fill()}
      else{ctx.fillStyle=`rgba(${Math.round(160-t*150)},${Math.round(160-t*150)},${Math.round(168-t*150)},${.7+t*.3})`;ctx.fill()}
    }
    for(const s of sparks){
      const a=nodes[s.a],b=nodes[s.b];if(!a||!b){s.dead=1;continue}
      const len=Math.hypot(b.x-a.x,b.y-a.y)||1;s.t+=(dt*.35)/len;
      if(s.t>=1){const key=Math.min(s.a,s.b)+'-'+Math.max(s.a,s.b);lit.set(key,1);litN[s.b]=1;s.hops++;
        const nb=(adj[s.b]||[]).filter(k=>k!==s.a);
        if(s.hops>18||!nb.length){s.dead=1;continue}
        s.prev=s.a;s.a=s.b;s.b=nb[Math.floor(Math.random()*nb.length)];s.t=0;
        if(s.hops%5===0&&nb.length>1){sparks.push({a:s.a,b:nb[Math.floor(Math.random()*nb.length)],t:0,hops:s.hops+4,prev:s.prev})}
        continue}
      const x=a.x+(b.x-a.x)*s.t,y=a.y+(b.y-a.y)*s.t;
      ctx.strokeStyle='rgba(10,10,11,.9)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(x,y);ctx.stroke();ctx.lineWidth=1;
      ctx.fillStyle='#0a0a0b';ctx.beginPath();ctx.arc(x,y,3.6,0,6.283);ctx.fill();
    }
    sparks=sparks.filter(s=>!s.dead).slice(-40);
    for(const r of rings){r.t+=dt/900;ctx.strokeStyle=`rgba(10,10,11,${(1-r.t)*.4})`;ctx.beginPath();ctx.arc(r.x,r.y,r.t*160,0,6.283);ctx.stroke()}
    rings=rings.filter(r=>r.t<1);
  }
  function loop(ts){
    const dt=Math.min(50,ts-last||16);last=ts;
    if(run&&!document.hidden){
      auto-=dt;if(auto<=0&&adj.length){ignite(Math.floor(Math.random()*nodes.length));auto=rnd(1800,3200)}
      draw(dt);
    }
    requestAnimationFrame(loop);
  }
  const rect=()=>cv.getBoundingClientRect();
  hero.addEventListener('mousemove',e=>{const r=rect();mouse.x=e.clientX-r.left;mouse.y=e.clientY-r.top});
  hero.addEventListener('mouseleave',()=>{mouse.x=mouse.y=-9999});
  hero.addEventListener('click',e=>{if(e.target.closest('a,button'))return;const r=rect(),x=e.clientX-r.left,y=e.clientY-r.top;rings.push({x,y,t:0});const i=nearest(x,y);ignite(i);ignite(i)});
  hero.addEventListener('touchstart',e=>{const t=e.touches[0],r=rect();mouse.x=t.clientX-r.left;mouse.y=t.clientY-r.top},{passive:true});
  if('IntersectionObserver' in window)new IntersectionObserver(es=>{run=es[0].isIntersecting}).observe(hero);
  addEventListener('resize',size);
  size();
  if(reduce){for(let k=0;k<6;k++)ignite(Math.floor(Math.random()*nodes.length));for(let k=0;k<30;k++)draw(60)}
  else requestAnimationFrame(loop);
})();

