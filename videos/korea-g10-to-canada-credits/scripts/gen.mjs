// node scripts/gen.mjs → compositions/*.html + index.html 을 scenes.mjs 에서 생성
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { SCENES, TOTAL, BC, ON } from "./scenes.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
mkdirSync(join(ROOT, "compositions"), { recursive: true });

const W = 1920;
const H = 1080;

const LOCK_SVG = `<svg class="lk" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="12" rx="2" fill="currentColor"/><path d="M8 10V7a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="2.6"/></svg>`;

const CSS = `
@font-face { font-family: "Pretendard"; font-weight: 500; src: url("assets/fonts/Pretendard-Medium.woff2") format("woff2"); }
@font-face { font-family: "Pretendard"; font-weight: 700; src: url("assets/fonts/Pretendard-Bold.woff2") format("woff2"); }
@font-face { font-family: "Pretendard"; font-weight: 800; src: url("assets/fonts/Pretendard-ExtraBold.woff2") format("woff2"); }
@font-face { font-family: "Pretendard"; font-weight: 900; src: url("assets/fonts/Pretendard-Black.woff2") format("woff2"); }
#root { position: absolute; inset: 0; overflow: hidden; background: #F4F6F8; color: #16202B;
  font-family: "Pretendard", sans-serif; letter-spacing: -0.02em; word-break: keep-all; }
#root * { box-sizing: border-box; margin: 0; padding: 0; }
.bc { --c: #1F7A4D; --c2: #0F4A2D; --lt: #CFE6D8; --bg: #E7F1EB; }
.on { --c: #1F5FAD; --c2: #10386B; --lt: #CFDDF0; --bg: #E6EDF7; }
.head { position: absolute; left: 96px; top: 54px; right: 96px; }
.act { font-size: 28px; font-weight: 700; color: #5B6673; }
.hl { font-size: 60px; font-weight: 900; line-height: 1.15; margin-top: 6px; }
.panels { position: absolute; left: 0; right: 0; top: 214px; bottom: 0; display: flex; }
.panel { position: relative; height: 100%; background: var(--bg); padding: 44px 64px 0 96px; overflow: hidden; }
.panel.on { padding-left: 64px; }
.panel + .panel { border-left: 6px solid #F4F6F8; }
.ph { display: flex; align-items: baseline; gap: 18px; }
.pn { font-size: 48px; font-weight: 900; color: var(--c2); }
.pd { font-size: 30px; font-weight: 700; color: var(--c); }
.body { display: flex; gap: 56px; margin-top: 34px; align-items: flex-start; }
.grid { display: grid; gap: 10px; flex: none; }
.cell { position: relative; height: var(--ch); border-radius: 10px; display: flex; align-items: center; justify-content: center;
  font-size: var(--fs, 24px); font-weight: 800; text-align: center; line-height: 1.1; padding: 0 4px; }
.s-open { border: 2px dashed color-mix(in srgb, var(--c) 45%, transparent); color: color-mix(in srgb, var(--c2) 45%, transparent); }
.s-req { background: var(--c); color: #fff; }
.s-elec { background: var(--lt); color: var(--c2); }
.s-eq { background: repeating-linear-gradient(135deg, #FFFFFF 0 10px, #E3E7EC 10px 20px); border: 2px solid #9AA5B1; color: #3D4752; }
.s-lock { background: #fff; border: 3px solid #D52B1E; color: #B21F14; }
.s-local { background: #fff; border: 3px solid var(--c); color: var(--c); }
.s-y11 { background: var(--c); color: #fff; }
.s-y12 { background: var(--c2); color: #fff; }
.badge { position: absolute; top: 5px; right: 7px; font-size: 15px; font-weight: 800; opacity: .9; letter-spacing: 0; }
.lk { position: absolute; top: 6px; right: 7px; width: 18px; height: 18px; color: #D52B1E; }
.notes { display: flex; flex-direction: column; gap: 30px; min-width: 0; }
.note { border-left: 8px solid var(--c); padding: 4px 0 4px 22px; }
.note.red { border-left-color: #D52B1E; }
.nk { font-size: 36px; font-weight: 900; line-height: 1.22; color: #16202B; }
.ns { font-size: 28px; font-weight: 700; line-height: 1.3; color: #4A5562; margin-top: 8px; }
.note.red .nk { color: #B21F14; }
.big { font-size: 132px; font-weight: 900; color: var(--c); line-height: 1; margin-top: 26px; letter-spacing: -0.04em; }
.exam { background: #fff; border-radius: 12px; padding: 22px 26px; display: flex; justify-content: space-between; align-items: center; gap: 22px;
  box-shadow: 0 6px 18px rgba(16, 32, 48, .08); }
.ek { font-size: 36px; font-weight: 900; }
.es { font-size: 28px; font-weight: 700; color: #4A5562; margin-top: 6px; }
.st { flex: none; font-size: 28px; font-weight: 900; padding: 8px 16px; border-radius: 8px; }
.st-must { background: var(--c); color: #fff; }
.st-waive { border: 3px solid #C77700; color: #9A5B00; }
.st-free { background: #E3E7EC; color: #3D4752; }
.dim { opacity: .32; }
.mini .cell { border-radius: 6px; font-size: 0; }
.mini .cell .badge, .mini .cell .lk { display: none; }
.mini .pd { display: none; }
.ph { white-space: nowrap; }
.miniNote { font-size: 30px; font-weight: 700; color: var(--c2); margin-top: 26px; opacity: .7; }
/* transcript */
.doc { position: absolute; left: 120px; top: 214px; width: 820px; height: 800px; background: #fff; border-radius: 14px;
  box-shadow: 0 22px 50px rgba(16, 32, 48, .14); padding: 48px 56px; }
.dt { font-size: 40px; font-weight: 900; }
.dm { font-size: 28px; font-weight: 700; color: #4A5562; margin-top: 10px; padding-bottom: 22px; border-bottom: 3px solid #16202B; }
.row { display: flex; justify-content: space-between; font-size: 30px; font-weight: 700; padding: 13px 4px; border-bottom: 1px solid #DDE2E8; }
.row b { color: #1F5FAD; font-weight: 800; }
.stamp { position: absolute; right: 36px; top: 14px; width: 180px; height: 180px; border-radius: 50%; border: 9px solid #D52B1E;
  color: #D52B1E; display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: 900; line-height: 1.1; text-align: center; transform: rotate(-14deg); background: rgba(255,255,255,.6); }
.routes { position: absolute; left: 1040px; top: 300px; width: 780px; display: flex; flex-direction: column; gap: 40px; }
.rq { font-size: 64px; font-weight: 900; line-height: 1.2; }
.route { display: flex; align-items: center; gap: 24px; background: var(--c); color: #fff; border-radius: 14px; padding: 30px 36px; }
.route .rn { font-size: 50px; font-weight: 900; }
.route .rg { font-size: 34px; font-weight: 700; opacity: .9; }
/* avatar */
.av { position: absolute; top: 220px; width: 640px; height: 640px; border-radius: 50%; background: #DDE3EA; border: 12px solid #fff;
  box-shadow: 0 22px 50px rgba(16, 32, 48, .16); display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden; }
.av .ph2 { font-size: 34px; font-weight: 800; color: #5B6673; line-height: 1.4; border: 3px dashed #9AA5B1; border-radius: 50%;
  width: 520px; height: 520px; display: flex; align-items: center; justify-content: center; }
.at { position: absolute; top: 300px; width: 960px; }
.ak { font-size: 34px; font-weight: 800; color: #D52B1E; }
.al { font-size: 92px; font-weight: 900; line-height: 1.15; margin-top: 18px; }
.as { font-size: 52px; font-weight: 800; margin-top: 30px; }
.as .b { color: #1F7A4D; } .as .o { color: #1F5FAD; }
.brand { font-size: 96px; font-weight: 900; color: #D52B1E; margin-top: 34px; letter-spacing: -0.03em; }
/* caution */
.cau { position: absolute; left: 160px; top: 270px; width: 1500px; border-left: 14px solid #D52B1E; padding-left: 48px; }
.cau .ck { font-size: 34px; font-weight: 800; color: #D52B1E; }
.cau .cm { font-size: 72px; font-weight: 900; line-height: 1.25; margin-top: 18px; }
.src { position: absolute; left: 222px; top: 700px; width: 1500px; font-size: 28px; font-weight: 700; color: #5B6673; line-height: 1.6; }
`;

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

function grid(prov, state, opts = {}) {
  const cw = opts.cw ?? (prov.key === "bc" ? 150 : 124);
  const ch = opts.ch ?? (prov.key === "bc" ? 112 : 88);
  const cls = `grid${opts.dim ? " dim" : ""}`;
  const cells = prov.cells
    .map((c) => {
      const st = state[c.id];
      let extra = "";
      if (st === "lock") extra = LOCK_SVG;
      else if (st === "y11") extra = `<span class="badge">G11</span>`;
      else if (st === "y12") extra = `<span class="badge">G12</span>`;
      else if (st === "eq") extra = `<span class="badge">인정</span>`;
      else if (st === "local") extra = `<span class="badge">현지</span>`;
      else if (st === "req" && c.g12) extra = `<span class="badge">12</span>`;
      return `<div class="cell s-${st}">${esc(c.t)}${extra}</div>`;
    })
    .join("");
  return `<div class="${cls}" style="grid-template-columns: repeat(${prov.cols}, ${cw}px); --ch: ${ch}px;${opts.fs ? ` --fs: ${opts.fs}px;` : ""}">${cells}</div>`;
}

function notesHtml(list = []) {
  return `<div class="notes">${list
    .map((n) => `<div class="note${n.tone === "red" ? " red" : ""}"><div class="nk">${esc(n.k)}</div>${n.s ? `<div class="ns">${esc(n.s)}</div>` : ""}</div>`)
    .join("")}</div>`;
}

function examsHtml(list) {
  const lab = { must: "필수", waive: "확인", free: "면제" };
  return `<div class="notes">${list
    .map(
      (e) =>
        `<div class="exam"><div><div class="ek">${esc(e.k)}</div><div class="es">${esc(e.s)}</div></div><div class="st st-${e.st}">${lab[e.st]}</div></div>`,
    )
    .join("")}</div>`;
}

function panel(prov, sc, mode) {
  const head = `<div class="ph"><div class="pn">${prov.name}</div><div class="pd">${prov.diploma}</div></div>`;
  const state = sc.state[prov.key];
  if (mode === "mini") {
    const cw = prov.key === "bc" ? 56 : 46;
    const ch = prov.key === "bc" ? 40 : 30;
    return `<div class="panel ${prov.key} mini" style="width:${sc._w[prov.key]}px">${head}<div class="body">${grid(prov, state, { cw, ch, dim: true })}</div><div class="miniNote">${prov.city}에서</div></div>`;
  }
  if (mode === "focus") {
    const right = sc.exams ? examsHtml(sc.exams) : notesHtml(sc.notes?.[prov.key]);
    return `<div class="panel ${prov.key}" style="width:${sc._w[prov.key]}px">${head}<div class="body">${grid(prov, state, { dim: sc.dimGrid === prov.key })}${right}</div></div>`;
  }
  // both
  const cw = sc.small ? (prov.key === "bc" ? 104 : 86) : prov.key === "bc" ? 150 : 124;
  const ch = sc.small ? (prov.key === "bc" ? 66 : 52) : prov.key === "bc" ? 96 : 76;
  const fs = sc.small ? 20 : 24;
  const big = sc.big ? `<div class="big">${sc.big[prov.key]}</div>` : "";
  return `<div class="panel ${prov.key}" style="width:${sc._w[prov.key]}px">${head}${big}<div class="body" style="flex-direction:column;gap:34px">${grid(prov, state, { cw, ch, fs })}${notesHtml(sc.notes?.[prov.key])}</div></div>`;
}

function splitScene(sc) {
  const f = sc.focus;
  sc._w = f === "both" ? { bc: 960, on: 960 } : f === "bc" ? { bc: 1440, on: 480 } : { bc: 480, on: 1440 };
  const mb = f === "on" ? "mini" : f === "bc" ? "focus" : "both";
  const mo = f === "bc" ? "mini" : f === "on" ? "focus" : "both";
  return `<div class="head"><div class="act">${esc(sc.act)}</div><div class="hl">${esc(sc.headline)}</div></div>
<div class="panels">${panel(BC, sc, mb)}${panel(ON, sc, mo)}</div>`;
}

function transcriptScene(sc) {
  const rows = ["국어", "수학", "영어", "한국사", "통합사회", "통합과학", "과학탐구실험", "체육", "예술", "정보"]
    .map((r) => `<div class="row"><span>${r}</span><b>이수</b></div>`)
    .join("");
  return `<div class="head"><div class="act">${esc(sc.act)}</div><div class="hl">${esc(sc.headline)}</div></div>
<div class="doc"><div class="dt">학교생활기록부 · 교과 성적</div><div class="dm">김민준 (가명) · 고등학교 1학년</div>${rows}<div class="stamp">고1<br/>수료</div></div>
<div class="routes"><div class="rq">같은 성적표,<br/>두 갈래 길</div>
<div class="route bc"><span class="rn">BC주</span><span class="rg">Grade 11 편입</span></div>
<div class="route on"><span class="rn">온타리오주</span><span class="rg">Grade 11 편입</span></div></div>`;
}

function avatarScene(sc) {
  const left = sc.side === "left";
  const avX = left ? 150 : W - 150 - 640;
  const tX = left ? 900 : 120;
  const file = sc.id === "intro" ? "intro.mp4" : "outro.mp4";
  const sub = sc.id === "intro" ? `<div class="as"><span class="b">BC주</span> vs <span class="o">온타리오주</span></div>` : `<div class="brand">AA Canada</div>`;
  return `<div class="av" style="left:${avX}px"><div class="ph2">HeyGen 대표님 영상<br/>assets/heygen/${file}<br/>(업로드 예정)</div></div>
<div class="at" style="left:${tX}px"><div class="ak">${esc(sc.kicker)}</div><div class="al">${sc.lines.map(esc).join("<br/>")}</div>${sub}</div>`;
}

function cautionScene() {
  return `<div class="cau"><div class="ck">꼭 확인하세요</div><div class="cm">최종 인정 학점은<br/>학교와 교육청의 평가에 따라 달라집니다</div></div>
<div class="src">출처 · BC Graduation Requirements · BC International Student Graduation Credit Policy<br/>Ontario: Earning your high school diploma · Ontario Schools K-12: Student records and transfers</div>`;
}

for (const sc of SCENES) {
  const body =
    sc.layout === "transcript" ? transcriptScene(sc) : sc.layout === "avatar" ? avatarScene(sc) : sc.layout === "caution" ? cautionScene(sc) : splitScene(sc);
  const html = `<template>
<style>${CSS}</style>
<div id="root" data-composition-id="${sc.id}" data-width="${W}" data-height="${H}">
${body}
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  tl.set({}, {}, ${sc.dur});
  window.__timelines["${sc.id}"] = tl;
</script>
</template>
`;
  writeFileSync(join(ROOT, "compositions", `${sc.id}.html`), html);
}

const hosts = SCENES.map(
  (sc) =>
    `      <div id="${sc.id}" data-composition-id="${sc.id}" data-composition-src="compositions/${sc.id}.html" data-start="${sc.start}" data-duration="${sc.dur}" data-track-index="1" data-track-kind="graphics" data-width="${W}" data-height="${H}"></div>`,
).join("\n");

const index = `<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W}, height=${H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: #F4F6F8; }
      #root { position: relative; width: 100%; height: 100%; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${TOTAL}" data-width="${W}" data-height="${H}">
${hosts}
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
writeFileSync(join(ROOT, "index.html"), index);
console.log(`scenes: ${SCENES.length}, total ${TOTAL}s`);
console.log(SCENES.map((s) => `${s.id} ${s.start}-${s.start + s.dur}`).join("\n"));
