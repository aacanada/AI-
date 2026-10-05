// Generates compositions/frames/*.html (one <template> fragment per storyboard frame).
import { writeFileSync, readFileSync } from "node:fs";
const META = JSON.parse(readFileSync("audio_meta.json", "utf8"));
const V = Object.fromEntries(META.voices.map(v => [v.frame, v]));
const D = (n) => V[n].duration_s;                       // frame duration = real voice length
const c = (n, i, off = 0) => +(V[n].words[i].start + off).toFixed(3); // word-cue time

const RED = "#D8000F", INK = "#1C1410", BG = "#FFFFFF", LIGHT = "#F5F2EF";
const TOTAL = 8;

const fonts = [400, 700, 900].map(w => `@font-face{font-family:"Noto Sans KR";font-weight:${w};font-style:normal;src:url("assets/fonts/NotoSansKR-${w}.ttf") format("truetype");}`).join("\n");

const baseCss = (p) => `
${fonts}
#root{position:absolute;inset:0;overflow:hidden;font-family:"Noto Sans KR",sans-serif;color:${INK};container-type:size;}
#root .${p}-bg{position:absolute;inset:0;background:${BG};}
#root .${p}-bg.red{background:${RED};}
#root .${p}-label{position:absolute;left:90px;top:170px;font-weight:700;font-size:30px;letter-spacing:6px;color:${RED};}
#root .${p}-label.inv{color:${BG};}
#root .${p}-pbar-track{position:absolute;left:90px;right:90px;top:1588px;height:12px;background:rgba(28,20,16,.08);}
#root .${p}-pbar-track.inv{background:rgba(255,255,255,.25);}
#root .${p}-pbar{position:absolute;left:0;top:0;bottom:0;background:${RED};transform-origin:left center;}
#root .${p}-pbar.inv{background:${BG};}
#root .${p}-count{position:absolute;right:90px;top:1538px;font-weight:700;font-size:28px;letter-spacing:4px;color:${INK};}
#root .${p}-count.inv{color:${BG};}
#root .${p}-blk{position:absolute;display:block;z-index:2;}
#root .${p}-label,#root .${p}-count,#root .${p}-pbar-track{z-index:2;}
`;

function chrome(p, n, inv) {
  const c = inv ? " inv" : "";
  return `
  <div class="${p}-label${c}" id="${p}-label">AA CANADA · 자녀무상교육</div>
  <div class="${p}-count${c}" id="${p}-count">0${n} / 0${TOTAL}</div>
  <div class="${p}-pbar-track${c}"><div class="${p}-pbar${c}" id="${p}-pbar" style="width:${(n / TOTAL) * 100}%"></div></div>`;
}
function chromeTl(p, n) {
  return `
  tl.fromTo("#${p}-label",{opacity:0,y:-20},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0);
  tl.fromTo("#${p}-count",{opacity:0},{opacity:1,duration:0.5},0.1);
  tl.fromTo("#${p}-pbar",{scaleX:${((n - 1) / n).toFixed(3)}},{scaleX:1,duration:0.8,ease:"power3.out"},0.1);`;
}

function frame({ id, p, n, dur, inv, css, html, js }) {
  const out = `<template>
<style>
${baseCss(p)}
${css}
</style>
<div id="root" data-composition-id="${id}" data-width="1080" data-height="1920" data-duration="${dur}">
  <div id="${p}-bg" class="clip ${p}-bg${inv ? " red" : ""}" data-start="0" data-duration="${dur}" data-track-index="0"></div>
  ${chrome(p, n, inv)}
  ${html}
</div>
<script>
(function(){
  const tl = gsap.timeline({ paused: true });
  ${chromeTl(p, n)}
  ${js}
  window.__timelines["${id}"] = tl;
})();
</script>
</template>
`;
  writeFileSync(`compositions/frames/${id}.html`, out);
}

const SHADOW = "4px 4px 0 rgba(28,20,16,.25), 8px 8px 0 rgba(28,20,16,.18), 12px 12px 0 rgba(28,20,16,.12)";

// ---------- 01 hook ----------
frame({ id: "01-hook", p: "hook", n: 1, dur: D(1),
  css: `
#root .hook-l1{left:90px;right:90px;top:330px;font-size:110px;font-weight:900;letter-spacing:-4px;line-height:1.1;}
#root .hook-l2{left:90px;right:90px;top:470px;font-size:96px;font-weight:900;letter-spacing:-4px;line-height:1.1;white-space:nowrap;}
#root .hook-l2 b{color:${RED};}
#root .hook-big{left:70px;top:680px;font-size:190px;font-weight:900;color:${RED};letter-spacing:-8px;line-height:1.1;transform-origin:left center;white-space:nowrap;}
#root .hook-tail{left:96px;top:960px;font-size:110px;font-weight:900;letter-spacing:-4px;line-height:1.1;}
#root .hook-rule{left:90px;top:1170px;width:900px;height:22px;background:${INK};transform-origin:left center;}
#root .hook-tag{left:90px;top:1260px;padding:18px 34px;border:4px solid ${INK};font-size:48px;font-weight:900;color:${INK};}
#root .hook-tag b{color:${RED};}`,
  html: `
  <div class="hook-blk hook-l1" id="hook-l1">캐나다</div>
  <div class="hook-blk hook-l2" id="hook-l2">자녀무상교육 <b>조건,</b></div>
  <div class="hook-blk hook-big" id="hook-big">지역별 차이</div>
  <div class="hook-blk hook-tail" id="hook-tail">알고 가시나요?</div>
  <div class="hook-blk hook-rule" id="hook-rule"></div>
  <div class="hook-blk hook-tag" id="hook-tag"><b>1분</b> 정리</div>`,
  js: `
  tl.fromTo("#hook-l1",{opacity:0,y:80},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(1,0,-0.1)});
  tl.fromTo("#hook-l2",{opacity:0,y:80},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(1,1,-0.1)});
  tl.fromTo("#hook-big",{opacity:0,scale:1.35,rotation:-5},{opacity:1,scale:1,rotation:-5,duration:0.55,ease:"expo.out"},${c(1,3,-0.1)});
  tl.fromTo("#hook-tail",{opacity:0,x:-50},{opacity:1,x:0,duration:0.45,ease:"power3.out"},${c(1,5,-0.1)});
  tl.fromTo("#hook-rule",{scaleX:0},{scaleX:1,duration:0.5,ease:"power3.inOut"},${c(1,6)});
  tl.fromTo("#hook-tag",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${c(1,6,0.3)});`
});

// ---------- 02 concept ----------
frame({ id: "02-concept", p: "con", n: 2, dur: D(2),
  css: `
#root .con-q{left:90px;top:300px;font-size:64px;font-weight:700;}
#root .con-old{left:90px;top:440px;font-size:120px;font-weight:900;letter-spacing:-4px;line-height:1.1;font-family:"Noto Sans KR";}
#root .con-oldk{left:94px;top:590px;font-size:64px;font-weight:700;color:#8a8580;}
#root .con-strike{left:80px;top:518px;width:860px;height:18px;background:${RED};transform-origin:left center;}
#root .con-arrow{left:90px;top:700px;line-height:1;font-size:64px;font-weight:900;color:${INK};}
#root .con-new{left:90px;top:840px;line-height:1.1;font-size:100px;font-weight:900;letter-spacing:-4px;}
#root .con-big{left:80px;top:1080px;font-size:250px;font-weight:900;color:${RED};letter-spacing:-12px;line-height:1;transform-origin:left center;white-space:nowrap;}
#root .con-sub{left:96px;top:1400px;font-size:54px;font-weight:700;border-left:10px solid ${RED};padding-left:28px;}`,
  html: `
  <div class="con-blk con-q" id="con-q">흔히 부르는 말</div>
  <div class="con-blk con-old" id="con-old">Free education</div>
  <div class="con-blk con-oldk" id="con-oldk">무상교육</div>
  <div class="con-blk con-strike" id="con-strike"></div>
  <div class="con-blk con-arrow" id="con-arrow">↓ 정확한 개념</div>
  <div class="con-blk con-new" id="con-new">Tuition exemption</div>
  <div class="con-blk con-big" id="con-big">학비면제</div>
  <div class="con-blk con-sub" id="con-sub">학비를 ‘면제’받는 제도</div>`,
  js: `
  tl.fromTo("#con-q",{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.05);
  tl.fromTo(["#con-old","#con-oldk"],{opacity:0,y:60},{opacity:1,y:0,duration:0.55,ease:"power3.out",stagger:0.15},${c(2,1,-0.15)});
  tl.fromTo("#con-strike",{scaleX:0},{scaleX:1,duration:0.45,ease:"power3.inOut"},${c(2,2)});
  tl.to(["#con-old","#con-oldk"],{opacity:0.3,duration:0.4},${c(2,2,0.35)});
  tl.fromTo("#con-arrow",{opacity:0,y:-30},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${c(2,3,-0.1)});
  tl.fromTo("#con-big",{opacity:0,scale:1.35,rotation:-4},{opacity:1,scale:1,rotation:-4,duration:0.6,ease:"expo.out"},${c(2,5,-0.1)});
  tl.fromTo("#con-new",{opacity:0,y:60},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(2,6,-0.1)});
  tl.fromTo("#con-sub",{opacity:0,x:-40},{opacity:1,x:0,duration:0.5,ease:"power3.out"},${c(2,7,0.5)});`
});

// ---------- 03 split ----------
frame({ id: "03-split", p: "spl", n: 3, dur: D(3),
  css: `
#root .spl-h{left:90px;right:90px;top:290px;font-size:62px;white-space:nowrap;font-weight:900;letter-spacing:-2px;line-height:1.25;}
#root .spl-h b{color:${RED};}
#root .spl-node{left:390px;top:540px;width:300px;height:130px;border:6px solid ${INK};display:flex;align-items:center;justify-content:center;font-size:60px;font-weight:900;background:${BG};}
#root .spl-svg{left:0;top:670px;width:1080px;height:200px;overflow:visible;}
#root .spl-card{top:870px;width:430px;height:600px;padding:44px 36px;}
#root .spl-card .en{font-size:46px;font-weight:900;line-height:1.15;letter-spacing:-1px;}
#root .spl-card .ko{font-size:40px;font-weight:700;margin-top:14px;}
#root .spl-card .hr{height:4px;margin:40px 0 36px;}
#root .spl-card .res{font-size:40px;font-weight:700;}
#root .spl-card .val{font-size:120px;font-weight:900;line-height:1.1;margin-top:10px;letter-spacing:-4px;}
#root .spl-left{left:90px;border:6px solid ${INK};background:${BG};}
#root .spl-left .hr{background:${INK};}
#root .spl-left .ko{color:#8a8580;}
#root .spl-right{left:560px;background:${RED};color:${BG};transform-origin:center center;}
#root .spl-right .hr{background:${BG};}
#root .spl-right .val{text-shadow:${SHADOW};}`,
  html: `
  <div class="spl-blk spl-h" id="spl-h">교육청은 학생을 <b>두 가지</b>로 나눠요</div>
  <div class="spl-blk spl-node" id="spl-node">학생</div>
  <svg class="spl-blk spl-svg" id="spl-svg" viewBox="0 0 1080 200">
    <path id="spl-pl" d="M540 0 V90 H305 V200" fill="none" stroke="${INK}" stroke-width="6"/>
    <path id="spl-pr" d="M540 0 V90 H775 V200" fill="none" stroke="${RED}" stroke-width="6"/>
  </svg>
  <div class="spl-blk spl-card spl-left" id="spl-left">
    <div class="en">International students</div><div class="ko">국제학생</div>
    <div class="hr"></div><div class="res">학비</div><div class="val">납부</div>
  </div>
  <div class="spl-blk spl-card spl-right" id="spl-right">
    <div class="en">Residents</div><div class="ko">거주자</div>
    <div class="hr" style="margin-top:94px"></div><div class="res">학비</div><div class="val">면제</div>
  </div>`,
  js: `
  tl.fromTo("#spl-h",{opacity:0,y:50},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.05);
  tl.fromTo("#spl-node",{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.5,ease:"back.out(1.6)"},${c(3,1,-0.1)});
  tl.fromTo(["#spl-pl","#spl-pr"],{strokeDasharray:600,strokeDashoffset:600},{strokeDashoffset:0,duration:0.8,ease:"power2.inOut"},${c(3,2)});
  tl.fromTo("#spl-left",{opacity:0,y:80},{opacity:1,y:0,duration:0.55,ease:"power3.out"},${c(3,5,-0.1)});
  tl.fromTo("#spl-right",{opacity:0,y:80},{opacity:1,y:0,duration:0.55,ease:"power3.out"},${c(3,8,-0.1)});
  tl.fromTo("#spl-right",{scale:1},{scale:1.04,duration:0.5,ease:"power3.out",immediateRender:false},${c(3,10)});`
});

// ---------- 04 resident ----------
frame({ id: "04-resident", p: "res", n: 4, dur: D(4),
  css: `
#root .res-h{left:90px;top:290px;font-size:110px;font-weight:900;color:${RED};letter-spacing:-4px;line-height:1;}
#root .res-hk{left:96px;top:420px;font-size:56px;font-weight:700;}
#root .res-card{left:90px;right:90px;border-left:14px solid ${RED};padding:26px 0 26px 40px;}
#root .res-card .t{font-size:62px;font-weight:900;letter-spacing:-2px;}
#root .res-card .d{font-size:44px;font-weight:400;margin-top:12px;color:#4a423d;}
#root .res-c1{top:560px;}
#root .res-c2{top:800px;}
#root .res-chips{display:flex;gap:24px;margin-top:22px;}
#root .res-chip{position:relative;padding:16px 30px;border:5px solid ${INK};font-size:48px;font-weight:900;}
#root .res-chipfill{position:absolute;inset:-5px;background:${RED};transform-origin:left center;}
#root .res-chiptxt{position:relative;}
#root .res-banner{left:90px;right:90px;top:1180px;height:300px;background:${INK};color:${BG};padding:44px 50px;clip-path:inset(0 100% 0 0);}
#root .res-banner .a{font-size:50px;font-weight:700;}
#root .res-banner .b{font-size:92px;font-weight:900;letter-spacing:-3px;margin-top:16px;}
#root .res-banner .b span{color:${RED};}`,
  html: `
  <div class="res-blk res-h" id="res-h">Residents</div>
  <div class="res-blk res-hk" id="res-hk">거주자는 두 종류</div>
  <div class="res-blk res-card res-c1" id="res-c1"><div class="t">영구거주자</div><div class="d">시민권자 · 영주권자</div></div>
  <div class="res-blk res-card res-c2" id="res-c2"><div class="t">임시거주자</div><div class="d">부모가 이 비자를 가진 경우</div>
    <div class="res-chips"><div class="res-chip" id="res-chip1"><span class="res-chiptxt">Work permit</span></div>
    <div class="res-chip" id="res-chip2"><div class="res-chipfill" id="res-chipfill"></div><span class="res-chiptxt" id="res-chip2t">Study permit</span></div></div>
  </div>
  <div class="res-blk res-banner" id="res-banner"><div class="a">부모 학생비자 = 동반자녀는</div><div class="b"><span>Resident</span> → 학비 0</div></div>`,
  js: `
  tl.fromTo("#res-h",{opacity:0,x:-80},{opacity:1,x:0,duration:0.55,ease:"power3.out"},0.05);
  tl.fromTo("#res-hk",{opacity:0,y:30},{opacity:1,y:0,duration:0.45,ease:"power3.out"},0.35);
  tl.fromTo("#res-c1",{opacity:0,x:-60},{opacity:1,x:0,duration:0.5,ease:"power3.out"},${c(4,1,-0.1)});
  tl.fromTo("#res-c2",{opacity:0,x:-60},{opacity:1,x:0,duration:0.5,ease:"power3.out"},${c(4,5,-0.1)});
  tl.fromTo("#res-chip1",{opacity:0,y:20},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${c(4,6,-0.05)});
  tl.fromTo("#res-chip2",{opacity:0,y:20},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${c(4,7,-0.05)});
  tl.fromTo("#res-chipfill",{scaleX:0},{scaleX:1,duration:0.45,ease:"power3.inOut"},${c(4,12,-0.1)});
  tl.fromTo("#res-chip2t",{color:"${INK}"},{color:"${BG}",duration:0.2},${c(4,12,0.05)});
  tl.to("#res-chip1",{opacity:0.35,duration:0.4},${c(4,12)});
  tl.fromTo("#res-banner",{clipPath:"inset(0 100% 0 0)"},{clipPath:"inset(0 0% 0 0)",duration:0.7,ease:"power3.inOut"},${c(4,15,-0.1)});`
});

// ---------- 05 three ----------
frame({ id: "05-three", p: "thr", n: 5, dur: D(5), inv: true,
  css: `
#root .thr-a{left:90px;right:90px;top:300px;font-size:66px;font-weight:700;color:${BG};line-height:1.35;}
#root .thr-num{left:150px;top:620px;font-size:600px;font-weight:900;color:${BG};line-height:0.8;text-shadow:${SHADOW};transform-origin:center center;letter-spacing:-20px;}
#root .thr-unit{left:540px;top:860px;font-size:200px;font-weight:900;color:${BG};text-shadow:${SHADOW};}
#root .thr-sub{left:90px;right:90px;top:1300px;font-size:64px;font-weight:900;color:${BG};line-height:1.3;border-top:6px solid ${BG};padding-top:40px;}`,
  html: `
  <div class="thr-blk thr-a" id="thr-a">단, 부모가 <b>어떤 공부</b>를 하느냐에 따라</div>
  <div class="thr-blk thr-num" id="thr-num">3</div>
  <div class="thr-blk thr-unit" id="thr-unit">가지</div>
  <div class="thr-blk thr-sub" id="thr-sub">지역별 학비면제 조건이 달라요</div>`,
  js: `
  tl.fromTo("#thr-a",{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.05);
  tl.fromTo("#thr-sub",{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(5,6,-0.1)});
  tl.fromTo("#thr-num",{opacity:0,scale:1.5,rotation:-6},{opacity:1,scale:1,rotation:-6,duration:0.55,ease:"expo.out"},${c(5,8,-0.1)});
  tl.fromTo("#thr-unit",{opacity:0,x:60},{opacity:1,x:0,duration:0.4,ease:"power3.out"},${c(5,9,-0.05)});`
});

// ---------- 06 grid ----------
const rows = [
  ["01", "정규과정", "컬리지 · 대학 학위과정", "캐나다 전 지역", "AB·SK·NB는 정규과정만 인정", false],
  ["02", "조건부입학 영어과정", "정규과정 입학 조건의 어학연수", "온타리오 · 매니토바 일부", "BC 일부는 사설도 최대 1년", false],
  ["03", "사설어학원", "목적 상관없이 학생비자만 있으면", "퀘벡 · 노바스코샤", "조건 없이 무상교육", true],
];
frame({ id: "06-grid", p: "grd", n: 6, dur: D(6),
  css: `
#root .grd-h{left:90px;right:90px;top:280px;font-size:80px;font-weight:900;letter-spacing:-3px;}
#root .grd-h b{color:${RED};}
#root .grd-box{left:90px;right:90px;top:430px;height:1110px;border:6px solid ${INK};}
#root .grd-row{position:absolute;left:0;right:0;height:366px;padding:34px 36px;}
#root .grd-row + .grd-row{border-top:3px solid ${INK};}
#root .grd-num{position:absolute;left:36px;top:30px;font-size:96px;font-weight:900;color:${RED};line-height:1;transform:rotate(-6deg);}
#root .grd-t{position:absolute;left:190px;top:34px;right:30px;font-size:60px;font-weight:900;letter-spacing:-2px;line-height:1.1;}
#root .grd-d{position:absolute;left:192px;top:112px;right:30px;font-size:38px;color:#5a524d;}
#root .grd-reg{position:absolute;left:190px;top:186px;padding:12px 24px;border:4px solid ${INK};font-size:48px;font-weight:900;}
#root .grd-note{position:absolute;left:192px;top:282px;font-size:34px;font-weight:700;color:#5a524d;}
#root .grd-row.hot .grd-reg{background:${RED};border-color:${RED};color:${BG};transform-origin:center center;}
#root .grd-row.hot .grd-note{color:${RED};font-weight:900;font-size:40px;}`,
  html: `
  <div class="grd-blk grd-h" id="grd-h">학생비자, <b>무슨 공부?</b></div>
  <div class="grd-blk grd-box" id="grd-box">
  ${rows.map((r, i) => `<div class="grd-row${r[5] ? " hot" : ""}" id="grd-r${i}" style="top:${i * 368}px">
      <div class="grd-num">${r[0]}</div><div class="grd-t">${r[1]}</div><div class="grd-d">${r[2]}</div>
      <div class="grd-reg" id="grd-reg${i}">${r[3]}</div><div class="grd-note" id="grd-note${i}">${r[4]}</div></div>`).join("\n  ")}
  </div>`,
  js: `
  tl.fromTo("#grd-h",{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.0);
  tl.fromTo("#grd-box",{clipPath:"inset(0 0 100% 0)"},{clipPath:"inset(0 0 0% 0)",duration:0.6,ease:"power3.inOut"},0.1);
  [[${c(6,0)},${c(6,6,-0.1)},${c(6,9,0.3)},0],[${c(6,10,-0.1)},${c(6,16,-0.1)},${c(6,18,0.1)},1],[${c(6,20,-0.1)},${c(6,22,-0.1)},${c(6,24,0.1)},2]].forEach(([t,tr,tn,i])=>{
    tl.fromTo("#grd-r"+i+" .grd-num, #grd-r"+i+" .grd-t, #grd-r"+i+" .grd-d",{opacity:0,x:-50},{opacity:1,x:0,duration:0.5,ease:"power3.out",stagger:0.12},t);
    tl.fromTo("#grd-reg"+i,{opacity:0,scale:i===2?1.6:0.9},{opacity:1,scale:1,duration:i===2?0.45:0.4,ease:i===2?"expo.out":"power3.out"},tr);
    tl.fromTo("#grd-note"+i,{opacity:0,y:20},{opacity:1,y:0,duration:0.4,ease:"power3.out"},tn);
  });`
});

// ---------- 07 quebec ----------
frame({ id: "07-quebec", p: "qc", n: 7, dur: D(7), inv: true,
  css: `
#root .qc-a{left:90px;right:90px;top:300px;font-size:64px;font-weight:700;color:${BG};line-height:1.35;}
#root .qc-box{left:90px;top:500px;padding:26px 44px;background:${BG};color:${RED};font-size:100px;font-weight:900;letter-spacing:-3px;clip-path:inset(0 100% 0 0);}
#root .qc-big{left:80px;top:770px;line-height:1.1;font-size:210px;font-weight:900;color:${BG};letter-spacing:-10px;line-height:1;text-shadow:${SHADOW};transform-origin:left center;white-space:nowrap;}
#root .qc-big2{left:96px;top:1030px;font-size:150px;font-weight:900;color:${BG};letter-spacing:-6px;text-shadow:${SHADOW};}
#root .qc-pin{left:90px;top:1340px;display:flex;align-items:center;gap:24px;padding:22px 36px;border:5px solid ${BG};color:${BG};font-size:54px;font-weight:900;transform-origin:left center;}
#root .qc-dot{width:30px;height:30px;border-radius:50%;background:${BG};}`,
  html: `
  <div class="qc-blk qc-a" id="qc-a">사설어학원 학생비자만 있어도</div>
  <div class="qc-blk qc-box" id="qc-box">퀘벡 · 노바스코샤</div>
  <div class="qc-blk qc-big" id="qc-big">조건 없이</div>
  <div class="qc-blk qc-big2" id="qc-big2">무상교육</div>
  <div class="qc-blk qc-pin" id="qc-pin"><div class="qc-dot"></div>몬트리올 MONTRÉAL</div>`,
  js: `
  tl.fromTo("#qc-pin",{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.5,ease:"back.out(1.7)"},${c(7,1,-0.05)});
  tl.fromTo("#qc-box",{clipPath:"inset(0 100% 0 0)"},{clipPath:"inset(0 0% 0 0)",duration:0.55,ease:"power3.inOut"},${c(7,3,-0.1)});
  tl.fromTo("#qc-a",{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(7,4,-0.1)});
  tl.fromTo("#qc-big",{opacity:0,scale:1.4,rotation:-5},{opacity:1,scale:1,rotation:-5,duration:0.55,ease:"expo.out"},${c(7,7,-0.1)});
  tl.fromTo("#qc-big2",{opacity:0,y:50},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(7,9,-0.1)});`
});

// ---------- 08 cta ----------
frame({ id: "08-cta", p: "cta", n: 8, dur: D(8),
  css: `
#root .cta-q{left:90px;right:90px;top:320px;font-size:88px;font-weight:900;letter-spacing:-3px;line-height:1.3;}
#root .cta-q b{color:${RED};}
#root .cta-big{left:70px;top:680px;font-size:180px;font-weight:900;color:${RED};letter-spacing:-10px;line-height:1;transform-origin:left center;white-space:nowrap;}
#root .cta-sub{left:96px;top:950px;font-size:58px;font-weight:700;border-left:10px solid ${RED};padding-left:28px;}
#root .cta-chips{left:90px;right:90px;top:1110px;display:flex;flex-wrap:wrap;gap:22px;}
#root .cta-chip{padding:16px 30px;border:5px solid ${INK};font-size:46px;font-weight:900;}
#root .cta-chip.hot{background:${INK};color:${BG};}
#root .cta-btn{left:90px;right:90px;top:1350px;height:140px;background:${RED};color:${BG};display:flex;align-items:center;justify-content:center;font-size:62px;font-weight:900;letter-spacing:-1px;}`,
  html: `
  <div class="cta-blk cta-q" id="cta-q"><span style="display:block">우리 아이에게 맞는</span><span style="display:block"><b>지역</b>은 어디일까?</span></div>
  <div class="cta-blk cta-big" id="cta-big">AA Canada</div>
  <div class="cta-blk cta-sub" id="cta-sub">캐나다 전문 유학원</div>
  <div class="cta-blk cta-chips" id="cta-chips"><div class="cta-chip hot">자녀무상교육</div><div class="cta-chip">유학 후 이민</div><div class="cta-chip">영주권</div></div>
  <div class="cta-blk cta-btn" id="cta-btn">프로필 링크에서 상담 신청</div>`,
  js: `
  tl.fromTo("#cta-q",{opacity:0,y:50},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.03);
  tl.fromTo("#cta-sub",{opacity:0,x:-40},{opacity:1,x:0,duration:0.45,ease:"power3.out"},${c(8,4,-0.1)});
  tl.fromTo("#cta-big",{opacity:0,scale:1.35,rotation:-5},{opacity:1,scale:1,rotation:-5,duration:0.55,ease:"expo.out"},${c(8,7,-0.1)});
  tl.fromTo("#cta-chips .cta-chip",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power3.out",stagger:0.12},${c(8,9,-0.1)});
  tl.fromTo("#cta-btn",{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},${c(8,10,0.2)});`
});
console.log("frames written");
