const root=document.getElementById("ROOT");
const q=s=>root.querySelector(s), qa=s=>Array.from(root.querySelectorAll(s));
const tl=gsap.timeline({paused:true});
function E(el){return typeof el==='string'?q(el):el;}
function inn(el,at,o){o=o||{};el=E(el);
  tl.fromTo(el,{opacity:0,x:o.x||0,y:(o.y===undefined?30:o.y),scale:(o.s===undefined?1:o.s),rotation:(o.r0===undefined?(o.r||0):o.r0)},
  {opacity:1,x:0,y:0,scale:1,rotation:o.r||0,duration:o.d||0.6,ease:o.e||'power3.out'},at);}
function whip(el,at,dy){el=E(el);tl.set(el,{opacity:0},0);tl.set(el,{opacity:1,y:dy||70},at);tl.to(el,{y:0,duration:0.45,ease:'power4.out'},at);}
function pop(el,at,o){o=o||{};el=E(el);tl.fromTo(el,{opacity:0,scale:0},{opacity:1,scale:1,duration:o.d||0.5,ease:o.e||'back.out(2)'},at);}
function pol(el,at,rot){el=E(el);
  tl.fromTo(el,{opacity:0,y:-180,rotation:rot*2.4,scale:1.06},{opacity:1,y:0,rotation:rot,scale:1,duration:0.85,ease:'power3.out'},at);}
function kb(el,at,dur,a,b){el=E(el);a=a||{};b=b||{};
  tl.fromTo(el,{scale:a.s||1,xPercent:a.x||0,yPercent:a.y||0},{scale:b.s||1.07,xPercent:b.x||0,yPercent:b.y||0,duration:dur,ease:'none'},at);}
function count(el,from,to,at,dur,fmt){el=E(el);const st={v:from};el.textContent=fmt(from);
  tl.fromTo(st,{v:from},{v:to,duration:dur,ease:'power2.out',immediateRender:false,onUpdate:()=>{el.textContent=fmt(st.v);}},at);}
function grow(el,at,d,origin){el=E(el);
  tl.fromTo(el,{scaleX:0,transformOrigin:origin||'0% 50%'},{scaleX:1,duration:d||0.8,ease:'power3.inOut'},at);}
function growY(el,at,d){el=E(el);
  tl.fromTo(el,{scaleY:0,transformOrigin:'50% 100%'},{scaleY:1,duration:d||0.8,ease:'power3.out'},at);}
function draw(path,at,d){path=E(path);const L=path.getTotalLength();path.style.strokeDasharray=L+' '+L;
  tl.fromTo(path,{strokeDashoffset:L},{strokeDashoffset:0,duration:d||1,ease:'power2.inOut'},at);}
function outt(el,at,o){o=o||{};el=E(el);tl.to(el,{opacity:0,y:o.y||0,x:o.x||0,duration:o.d||0.4,ease:'power2.in'},at);}
function ambient(D){
  qa('.ghost').forEach((g,i)=>tl.fromTo(g,{x:0},{x:(i%2?160:-160),duration:D,ease:'none'},0));
  qa('.glow').forEach((g,i)=>{const c=4+i;const n=Math.max(0,Math.floor(D/c)-1);
    tl.fromTo(g,{scale:0.92},{scale:1.08,duration:c/2,ease:'sine.inOut',yoyo:true,repeat:n},0);});
}
