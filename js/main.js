/* Markov's site: shared behaviour (loaded on every page) */
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
document.documentElement.classList.add('js');

/* marquee */
(function(){
  const t=$('#track');if(!t)return;
  const words=['Finest creators','Finest data','Finest delivery','Finest results','Ignite your presence'];
  const one=words.map(w=>`<span>${w}</span>`).join('');
  t.innerHTML=one+one+one+one;
})();

/* reveal on scroll */
(function(){
  const els=$$('.rv');
  if(!('IntersectionObserver' in window)||reduce){els.forEach(e=>e.classList.add('in'));return}
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  els.forEach(e=>io.observe(e));
  setTimeout(()=>els.forEach(e=>{if(!e.classList.contains('in')){const r=e.getBoundingClientRect();if(r.top<innerHeight)e.classList.add('in')}}),1200);
})();

/* nav border + mobile menu */
(function(){
  const n=$('#nav');if(!n)return;
  const f=()=>n.classList.toggle('stuck',scrollY>8);addEventListener('scroll',f,{passive:true});f();
  const b=$('#menuBtn'),m=$('#mnav');if(!b||!m)return;
  const set=o=>{document.body.classList.toggle('menu-open',o);b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Close menu':'Open menu')};
  b.addEventListener('click',()=>set(!document.body.classList.contains('menu-open')));
  m.addEventListener('click',e=>{if(e.target.closest('a'))set(false)});
  addEventListener('keydown',e=>{if(e.key==='Escape')set(false)});
  addEventListener('resize',()=>{if(innerWidth>860)set(false)});
})();

/* scroll-filled statement + process rail */
(function(){
  const p=$('#stmt'),rail=$('#steps');
  let ws=[],steps=[];
  if(p){const words=p.textContent.trim().split(/\s+/);p.innerHTML=words.map(w=>`<span class="w">${w}</span>`).join(' ');ws=$$('.w',p)}
  if(rail)steps=$$('.step',rail);
  if(!p&&!rail)return;
  function tick(){
    const vh=innerHeight;
    if(p){const r=p.getBoundingClientRect();const prog=clamp((vh*0.82-r.top)/(r.height+vh*0.25));const n=Math.round(prog*ws.length);ws.forEach((w,i)=>w.classList.toggle('on',i<n))}
    if(rail){const rr=rail.getBoundingClientRect();rail.style.setProperty('--p',(clamp((vh*0.6-rr.top)/rr.height)*100).toFixed(1)+'%');steps.forEach(s=>{const d=s.getBoundingClientRect();s.classList.toggle('on',d.top+30<vh*0.62)})}
  }
  addEventListener('scroll',tick,{passive:true});addEventListener('resize',tick);tick();
})();

/* cursor ring + magnetic buttons */
(function(){
  const c=$('#cur');if(!c||!fine||reduce)return;
  let x=0,y=0,tx=0,ty=0,seen=false;
  addEventListener('mousemove',e=>{tx=e.clientX;ty=e.clientY;if(!seen){seen=true;x=tx;y=ty;c.classList.add('on')}});
  document.addEventListener('mouseleave',()=>c.classList.remove('on'));
  document.addEventListener('mouseenter',()=>seen&&c.classList.add('on'));
  (function loop(){x+=(tx-x)*.18;y+=(ty-y)*.18;c.style.transform=`translate(${x}px,${y}px)`;requestAnimationFrame(loop)})();
  $$('a,button,input,textarea,select').forEach(el=>{el.addEventListener('mouseenter',()=>c.classList.add('big2'));el.addEventListener('mouseleave',()=>c.classList.remove('big2'))});
  $$('.mag').forEach(el=>{
    el.addEventListener('mousemove',e=>{const r=el.getBoundingClientRect();el.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.28}px)`});
    el.addEventListener('mouseleave',()=>{el.style.transform=''});
  });
})();

/* copy-to-clipboard buttons: <button data-copy="text"> */
document.addEventListener('click',async e=>{
  const b=e.target.closest('[data-copy]');if(!b)return;
  const old=b.dataset.label||b.textContent;b.dataset.label=old;
  try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Copied'}catch(err){b.textContent='Press Ctrl+C'}
  setTimeout(()=>{b.textContent=old},1800);
});
