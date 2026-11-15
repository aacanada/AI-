// node scripts/gen.mjs → compositions/*.html + index.html (scenes.mjs + assets/voice 기준)
// 장면 길이 = 내레이션 실제 길이 + 앞 0.5s + 뒤 0.8s. 애니메이션·효과음은 내레이션 단어 타이밍(cue)에 맞춘다.
import { writeFileSync, mkdirSync, existsSync, readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { SCENES, BC, ON } from "./scenes.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
mkdirSync(join(ROOT, "compositions"), { recursive: true });
const W = 1920;
const H = 1080;
const LEAD = 0.5;
const TAIL = 0.8;
const r2 = (n) => Math.round(n * 100) / 100;
const probe = (p) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", join(ROOT, p)]).toString());
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

// ── HeyGen 인트로·아웃트로 (영상이 올라오면 자동 사용)
// HeyGen 음성의 실제 문장 구간(초) — silencedetect(-35dB, 0.25s)로 측정한 쉼 사이
const AVATAR_SEGS = {
  intro: [
    [0.1, 2.15, "안녕하세요, 에이에이캐나다입니다."],
    [2.89, 6.63, "고1 마치고 캐나다로 가면 졸업까지 어떻게 될까요?"],
    [7.22, 9.46, "BC와 온타리오를 비교해 드릴게요."],
  ],
  outro: [
    [0.1, 3.17, "우리 아이 성적표로는 어느 주가 더 유리할지,"],
    [3.69, 6.21, "에이에이캐나다에서 일대일로 확인해 보세요."],
    [6.7, 7.32, "감사합니다."],
  ],
};

// ── 내레이션 정렬 정보
for (const s of SCENES) {
  if (s.layout === "avatar") {
    const v = `assets/heygen/${s.id}.mp4`;
    s.video = existsSync(join(ROOT, v)) ? v : null;
    s.dur = s.video ? r2(probe(v) + 0.4) : 9;
    continue;
  }
  const a = JSON.parse(readFileSync(join(ROOT, `assets/voice/${s.id}.align.json`), "utf8"));
  s.chars = a.characters;
  s.cs = a.character_start_times_seconds;
  s.ce = a.character_end_times_seconds;
  s.text = s.chars.join("");
  s.voiceDur = probe(`assets/voice/${s.id}.mp3`);
  s.dur = r2(LEAD + s.voiceDur + TAIL + (s.layout === "caution" ? 3 : 0));
}
let acc = 0;
for (const s of SCENES) {
  s.start = r2(acc);
  acc += s.dur;
}
const TOTAL = r2(acc);

// cue: "단어" | ["단어", +초] | 숫자(장면 내 절대초)
function cueTime(s, cue) {
  if (typeof cue === "number") return cue;
  let off = 0;
  if (Array.isArray(cue)) [cue, off] = cue;
  const i = s.text.indexOf(cue);
  if (i < 0) throw new Error(`cue "${cue}" not found in ${s.id}`);
  return r2(LEAD + s.cs[i] + off);
}

// ── 장면별 큐 (내레이션 단어에 맞춘 등장 시점)
const CUES = {
  s01: { stamp: "고1을", rq: "같은", rbc: "BC로", ron: "온타리오로" },
  s02: { big: { bc: "80학점", on: "30학점" }, land: { bc: [["open", "80학점"]], on: [["open", "30학점"]] }, notes: { bc: ["4학점"], on: ["1학점"] } },
  s03: { land: { bc: [["req", "필수 52"], ["elec", "선택 28"]] }, notes: { bc: ["필수 52", "16학점", "원주민"] } },
  s04: { dim: "세 개", exams: ["세 개", ["세 개", 0.35], ["세 개", 0.7]], stat: ["반드시", "면제를", ["반드시", 0.4]] },
  s05: { land: { on: [["req", "OSSD"], ["elec", "선택 13"]] }, notes: { on: ["필수 17", ["필수 17", 1.6], "영어는"] } },
  s06: { dim: 0.4, exams: ["OSSLT", "봉사활동", "온라인"], stat: [["OSSLT", 0.4], ["봉사활동", 0.4], ["온라인", 0.4]] },
  s07: { land: { bc: [["eq", "이퀴벌런시"]] }, notes: { bc: ["이퀴벌런시", "번역 공증", ["번역 공증", 1.6]] } },
  s08: { land: { bc: [["lock", "일곱 과목"]] }, notes: { bc: ["입국 전", "직접", ["직접", 1.2]] } },
  s09: { land: { on: [["eq", "교장이"], ["local", "최소 14학점"]] }, notes: { on: ["교장이", "최소 14학점", "영어 두"] } },
  s10: { dim: 0.4, exams: ["문해력", "금융문해", "봉사시간", "온라인"], stat: [["문해력", 0.4], ["면제", 0], ["교장이", 0], ["교장이", 0.3]] },
  s11: { land: { bc: [["y11", "11학년과"], ["y12", "12학년 2년"]] }, notes: { bc: ["핵심 과목", "졸업 평가", "바로"] }, chime: "12학년으로" },
  s12: { land: { on: [["y11", "14학점"], ["y12", ["14학점", 0.9]]] }, notes: { on: ["나눠", "관리 포인트"] }, chime: "관리 포인트" },
  s13: { notes: { bc: ["BC는", "핵심 과목", "현지에서"], on: ["온타리오는", "인정 폭", "남은 학점"] } },
  s14: {},
};

// ── 스타일
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
.panel { position: relative; flex: none; height: 100%; background: var(--bg); padding: 44px 64px 0 96px; overflow: hidden; }
.panel.on { padding-left: 64px; border-left: 6px solid #F4F6F8; }
.ph { display: flex; align-items: baseline; gap: 18px; white-space: nowrap; }
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
.notes.ex { gap: 20px; }
.note { border-left: 8px solid var(--c); padding: 4px 0 4px 22px; }
.note.red { border-left-color: #D52B1E; }
.nk { font-size: 36px; font-weight: 900; line-height: 1.22; color: #16202B; }
.ns { font-size: 28px; font-weight: 700; line-height: 1.3; color: #4A5562; margin-top: 8px; }
.note.red .nk { color: #B21F14; }
.small .note { padding: 2px 0 2px 18px; }
.small .nk { font-size: 32px; }
.small .notes { gap: 16px; }
.big { font-size: 132px; font-weight: 900; color: var(--c); line-height: 1; margin-top: 26px; letter-spacing: -0.04em; }
.exam { background: #fff; border-radius: 12px; padding: 18px 26px; display: flex; justify-content: space-between; align-items: center; gap: 22px;
  box-shadow: 0 6px 18px rgba(16, 32, 48, .08); }
.ek { font-size: 36px; font-weight: 900; }
.es { font-size: 28px; font-weight: 700; color: #4A5562; margin-top: 6px; }
.st { flex: none; font-size: 28px; font-weight: 900; padding: 8px 16px; border-radius: 8px; }
.st-must { background: var(--c); color: #fff; }
.st-waive { border: 3px solid #C77700; color: #9A5B00; }
.st-free { background: #E3E7EC; color: #3D4752; }
.mini .cell { border-radius: 6px; font-size: 0; }
.mini .cell .badge, .mini .cell .lk { display: none; }
.mini .pd { display: none; }
.miniNote { font-size: 30px; font-weight: 700; color: var(--c2); margin-top: 26px; opacity: .7; }
.doc { position: absolute; left: 120px; top: 200px; width: 820px; height: 730px; background: #fff; border-radius: 14px;
  box-shadow: 0 22px 50px rgba(16, 32, 48, .14); padding: 40px 56px; }
.dt { font-size: 40px; font-weight: 900; }
.dm { font-size: 28px; font-weight: 700; color: #4A5562; margin-top: 10px; padding-bottom: 22px; border-bottom: 3px solid #16202B; }
.row { display: flex; justify-content: space-between; font-size: 30px; font-weight: 700; padding: 10px 4px; border-bottom: 1px solid #DDE2E8; }
.row b { color: #1F5FAD; font-weight: 800; }
.stamp { position: absolute; right: 36px; top: 14px; width: 180px; height: 180px; border-radius: 50%; border: 9px solid #D52B1E;
  color: #D52B1E; display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: 900; line-height: 1.1; text-align: center; background: rgba(255,255,255,.6); }
.routes { position: absolute; left: 1040px; top: 300px; width: 780px; display: flex; flex-direction: column; gap: 40px; }
.rq { font-size: 64px; font-weight: 900; line-height: 1.2; }
.route { display: flex; align-items: center; gap: 24px; background: var(--c); color: #fff; border-radius: 14px; padding: 30px 36px; }
.route .rn { font-size: 50px; font-weight: 900; }
.route .rg { font-size: 34px; font-weight: 700; opacity: .9; }
.av { position: absolute; top: 220px; width: 640px; height: 640px; border-radius: 50%; background: #DDE3EA; border: 12px solid #fff;
  box-shadow: 0 22px 50px rgba(16, 32, 48, .16); display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden; }
.av video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.av .ph2 { font-size: 34px; font-weight: 800; color: #5B6673; line-height: 1.4; border: 3px dashed #9AA5B1; border-radius: 50%;
  width: 520px; height: 520px; display: flex; align-items: center; justify-content: center; }
.at { position: absolute; top: 280px; width: 960px; }
.ak { font-size: 34px; font-weight: 800; color: #D52B1E; }
.al { font-size: 92px; font-weight: 900; line-height: 1.15; margin-top: 18px; }
.as { font-size: 52px; font-weight: 800; margin-top: 30px; }
.as .b { color: #1F7A4D; } .as .o { color: #1F5FAD; }
.brand { font-size: 96px; font-weight: 900; color: #D52B1E; margin-top: 34px; letter-spacing: -0.03em; }
.cau { position: absolute; left: 160px; top: 270px; width: 1500px; padding-left: 62px; }
.cbar { position: absolute; left: 0; top: 0; bottom: 0; width: 14px; background: #D52B1E; transform-origin: top; }
.cau .ck { font-size: 34px; font-weight: 800; color: #D52B1E; }
.cau .cm { font-size: 72px; font-weight: 900; line-height: 1.25; margin-top: 18px; }
.src { position: absolute; left: 222px; top: 690px; width: 1500px; font-size: 28px; font-weight: 700; color: #5B6673; line-height: 1.6; }
`;

// 1920x1080 원본을 0.6배(1152x648)로 놓고 얼굴 중심(원본 약 1000,440)을 둥근 창(616px) 중앙에
const AV_CROP = "width:1152px;height:648px;left:-292px;top:-10px;inset:auto;object-fit:fill;";

// ── 마크업
function grid(sid, prov, state, prev, opts = {}) {
  const cw = opts.cw ?? (prov.key === "bc" ? 150 : 124);
  const ch = opts.ch ?? (prov.key === "bc" ? 112 : 88);
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
      const changed = prev && prev[c.id] !== st ? ` data-to="${st}"` : "";
      return `<div class="cell s-${st}"${changed}>${esc(c.t)}${extra}</div>`;
    })
    .join("");
  return `<div class="grid" id="${sid}-${prov.key}-grid" style="grid-template-columns: repeat(${prov.cols}, ${cw}px); --ch: ${ch}px;${opts.fs ? ` --fs: ${opts.fs}px;` : ""}${opts.dim ? " opacity:.32;" : ""}">${cells}</div>`;
}
const notesHtml = (sid, key, list = []) =>
  `<div class="notes">${list
    .map((n, i) => `<div class="note${n.tone === "red" ? " red" : ""}" id="${sid}-${key}-n${i}"><div class="nk">${esc(n.k)}</div>${n.s ? `<div class="ns">${esc(n.s)}</div>` : ""}</div>`)
    .join("")}</div>`;
const examsHtml = (sid, list) => {
  const lab = { must: "필수", waive: "확인", free: "면제" };
  return `<div class="notes ex">${list
    .map(
      (e, i) =>
        `<div class="exam" id="${sid}-x${i}"><div><div class="ek">${esc(e.k)}</div><div class="es">${esc(e.s)}</div></div><div class="st st-${e.st}" id="${sid}-x${i}s">${lab[e.st]}</div></div>`,
    )
    .join("")}</div>`;
};

const modeOf = (focus, key) => (focus === "both" ? "both" : focus === key ? "focus" : "mini");
const widthsOf = (f) => (f === "both" ? { bc: 960, on: 960 } : f === "bc" ? { bc: 1440, on: 480 } : { bc: 480, on: 1440 });

function panel(sc, prov, mode, prev) {
  const sid = sc.id;
  const head = `<div class="ph"><div class="pn">${prov.name}</div><div class="pd">${prov.diploma}</div></div>`;
  const state = sc.state[prov.key];
  const w = widthsOf(sc.focus)[prov.key];
  if (mode === "mini") {
    const cw = prov.key === "bc" ? 56 : 46;
    const ch = prov.key === "bc" ? 40 : 30;
    return `<div class="panel ${prov.key} mini" id="${sid}-${prov.key}" style="width:${w}px">${head}<div class="body" id="${sid}-${prov.key}-body">${grid(sid, prov, state, null, { cw, ch, dim: true })}</div><div class="miniNote">${prov.city}에서</div></div>`;
  }
  if (mode === "focus") {
    const right = sc.exams ? examsHtml(sid, sc.exams) : notesHtml(sid, prov.key, sc.notes?.[prov.key]);
    return `<div class="panel ${prov.key}" id="${sid}-${prov.key}" style="width:${w}px">${head}<div class="body" id="${sid}-${prov.key}-body">${grid(sid, prov, state, prev)}${right}</div></div>`;
  }
  const cw = sc.small ? (prov.key === "bc" ? 104 : 86) : prov.key === "bc" ? 150 : 124;
  const ch = sc.small ? (prov.key === "bc" ? 56 : 44) : prov.key === "bc" ? 96 : 76;
  const fs = sc.small ? 20 : 24;
  const big = sc.big ? `<div class="big" id="${sid}-${prov.key}-big">0학점</div>` : "";
  return `<div class="panel ${prov.key}${sc.small ? " small" : ""}" id="${sid}-${prov.key}" style="width:${w}px">${head}${big}<div class="body" id="${sid}-${prov.key}-body" style="flex-direction:column;gap:${sc.small ? 26 : 34}px">${grid(sid, prov, state, prev, { cw, ch, fs })}${notesHtml(sid, prov.key, sc.notes?.[prov.key])}</div></div>`;
}

// ── 장면별 HTML + 타임라인
const SFX = []; // {file, t(abs), vol}
const sfx = (sc, file, t, vol = 0.45) => SFX.push({ file, t: r2(sc.start + t), vol });

let prevSplit = null;
let prevHead = null;
const tw = []; // per-scene tween lines

function wipe(sel, t, d = 0.5) {
  tw.push(`tl.fromTo(${JSON.stringify(sel)}, { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: ${d}, ease: "power3.out" }, ${r2(t)});`);
}
function headAnim(sc) {
  const same = prevHead && prevHead.hl === sc.headline;
  const sameAct = prevHead && prevHead.act === sc.act;
  if (!sameAct) wipe(`#${sc.id}-act`, 0.1, 0.4);
  if (!same) wipe(`#${sc.id}-hl`, sameAct ? 0.1 : 0.25, 0.55);
  prevHead = { hl: sc.headline, act: sc.act };
}
const headHtml = (sc) => `<div class="head"><div class="act" id="${sc.id}-act">${esc(sc.act)}</div><div class="hl" id="${sc.id}-hl">${esc(sc.headline)}</div></div>`;

function splitScene(sc) {
  const sid = sc.id;
  const cues = CUES[sid] ?? {};
  const prev = prevSplit;
  const pw = prev ? widthsOf(prev.focus) : widthsOf(sc.focus);
  const nw = widthsOf(sc.focus);
  let html = headHtml(sc) + `<div class="panels">`;
  for (const prov of [BC, ON]) {
    const mode = modeOf(sc.focus, prov.key);
    const pmode = prev ? modeOf(prev.focus, prov.key) : null;
    const sameLayout = pmode === mode && !(prev?.small !== sc.small && mode === "both");
    const prevState = prev && sameLayout ? prev.state[prov.key] : prev ? null : Object.fromEntries(prov.cells.map((c) => [c.id, "__none"]));
    html += panel(sc, prov, mode, mode === "mini" ? null : prevState ?? (prev ? prev.state[prov.key] : null));
    // 패널 폭 전환
    if (pw[prov.key] !== nw[prov.key]) {
      tw.push(`tl.fromTo("#${sid}-${prov.key}", { width: ${pw[prov.key]} }, { width: ${nw[prov.key]}, duration: 0.8, ease: "power2.inOut" }, 0);`);
    }
    if (!sameLayout) {
      tw.push(`tl.fromTo("#${sid}-${prov.key}-body", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, ${pw[prov.key] !== nw[prov.key] ? 0.6 : 0.15});`);
    }
    // 블록 착지
    for (const [st, cue] of cues.land?.[prov.key] ?? []) {
      const t = cueTime(sc, cue);
      const sel = `#${sid}-${prov.key}-grid .cell[data-to="${st}"]`;
      tw.push(`tl.fromTo(${JSON.stringify(sel)}, { y: -36, scale: 0.86, opacity: 0.15 }, { y: 0, scale: 1, opacity: 1, duration: 0.42, ease: "back.out(1.6)", stagger: 0.05 }, ${t});`);
      sfx(sc, st === "lock" ? "click.mp3" : "pop.mp3", t + 0.05, st === "lock" ? 0.55 : 0.4);
      if (st === "lock") sfx(sc, "click.mp3", t + 0.3, 0.45);
    }
    // 메모
    (cues.notes?.[prov.key] ?? []).forEach((cue, i) => {
      const t = cueTime(sc, cue);
      tw.push(`tl.fromTo("#${sid}-${prov.key}-n${i}", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.55, ease: "power3.out" }, ${t});`);
    });
    // 큰 숫자 카운트업
    if (cues.big?.[prov.key]) {
      const t = cueTime(sc, cues.big[prov.key]);
      const to = Number(sc.big[prov.key].replace(/\D/g, ""));
      tw.push(`(() => { const el = document.querySelector("#${sid}-${prov.key}-big"); const o = { v: 0 }; tl.fromTo(o, { v: 0 }, { v: ${to}, duration: 0.9, ease: "power2.out", onUpdate: () => { el.textContent = Math.round(o.v) + "학점"; } }, ${t}); })();`);
      sfx(sc, "pop.mp3", t + 0.85, 0.4);
    }
  }
  html += `</div>`;
  // 평가 카드
  if (sc.exams) {
    const key = sc.focus;
    if (cues.dim !== undefined && !(prev && prev.exams && prev.focus === sc.focus)) {
      tw.push(`tl.fromTo("#${sid}-${key}-grid", { opacity: 1 }, { opacity: 0.32, duration: 0.5, ease: "power2.out" }, ${cueTime(sc, cues.dim)});`);
    }
    sc.exams.forEach((e, i) => {
      const t = cueTime(sc, cues.exams[i]);
      tw.push(`tl.fromTo("#${sid}-x${i}", { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, ${t});`);
      const ts = cueTime(sc, cues.stat[i]);
      tw.push(`tl.fromTo("#${sid}-x${i}s", { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }, ${Math.max(ts, t + 0.2)});`);
      sfx(sc, "click-soft.mp3", Math.max(ts, t + 0.2), 0.5);
    });
  }
  if (prev && prev.focus !== sc.focus) sfx(sc, "whoosh-short.mp3", 0.05, 0.35);
  if (cues.chime) sfx(sc, "chime.mp3", cueTime(sc, cues.chime) - 0.2, 0.3);
  headAnim(sc);
  prevSplit = sc;
  return html;
}

function transcriptScene(sc) {
  const sid = sc.id;
  const c = CUES[sid];
  const rows = ["국어", "수학", "영어", "한국사", "통합사회", "통합과학", "과학탐구실험", "체육", "예술"]
    .map((r) => `<div class="row"><span>${r}</span><b>이수</b></div>`)
    .join("");
  tw.push(`tl.fromTo("#${sid}-doc", { x: -80, opacity: 0, rotation: -2 }, { x: 0, opacity: 1, rotation: 0, duration: 0.7, ease: "power3.out" }, 0.1);`);
  tw.push(`tl.fromTo("#${sid}-doc .row", { opacity: 0 }, { opacity: 1, duration: 0.25, stagger: 0.05 }, 0.4);`);
  const ts = cueTime(sc, c.stamp);
  tw.push(`tl.fromTo("#${sid}-stamp", { scale: 2.2, opacity: 0, rotation: -34 }, { scale: 1, opacity: 1, rotation: -14, duration: 0.28, ease: "power4.in" }, ${ts});`);
  sfx(sc, "impact-bass-1.mp3", ts + 0.24, 0.5);
  wipe(`#${sid}-rq`, cueTime(sc, c.rq), 0.6);
  for (const k of ["bc", "on"]) {
    const t = cueTime(sc, k === "bc" ? c.rbc : c.ron);
    tw.push(`tl.fromTo("#${sid}-r${k}", { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, ${t});`);
    sfx(sc, "whoosh-short.mp3", t, 0.35);
  }
  prevHead = null;
  wipe(`#${sid}-act`, 0.1, 0.4);
  wipe(`#${sid}-hl`, 0.25, 0.55);
  prevHead = { hl: sc.headline, act: sc.act };
  return `${headHtml(sc)}
<div class="doc" id="${sid}-doc"><div class="dt">학교생활기록부 · 교과 성적</div><div class="dm">김민준 (가명) · 고등학교 1학년</div>${rows}<div class="stamp" id="${sid}-stamp">고1<br/>수료</div></div>
<div class="routes"><div class="rq" id="${sid}-rq">같은 성적표,<br/>두 갈래 길</div>
<div class="route bc" id="${sid}-rbc"><span class="rn">BC주</span><span class="rg">Grade 11 편입</span></div>
<div class="route on" id="${sid}-ron"><span class="rn">온타리오주</span><span class="rg">Grade 11 편입</span></div></div>`;
}

function avatarScene(sc) {
  const sid = sc.id;
  const left = sc.side === "left";
  const avX = left ? 150 : W - 150 - 640;
  const tX = left ? 900 : 120;
  const sub = sid === "intro" ? `<div class="as" id="${sid}-sub"><span class="b">BC주</span> vs <span class="o">온타리오주</span></div>` : `<div class="brand" id="${sid}-sub">AA Canada</div>`;
  const inner = sc.video
    ? `<video id="${sid}-vid" class="clip" src="${sc.video}" data-start="0" data-duration="${r2(sc.dur - 0.4)}" muted data-track-index="2" playsinline style="${AV_CROP}"></video>`
    : `<div class="ph2">HeyGen 대표님 영상<br/>assets/heygen/${sid}.mp4<br/>(업로드 예정)</div>`;
  if (sid === "intro") {
    tw.push(`tl.fromTo("#${sid}-av", { scale: 0.96 }, { scale: 1, duration: 0.8, ease: "power3.out" }, 0);`);
  } else {
    tw.push(`tl.fromTo("#${sid}-av", { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out" }, 0);`);
    wipe(`#${sid}-k`, 0.5, 0.45);
    wipe(`#${sid}-l`, 0.8, 0.7);
  }
  tw.push(`tl.fromTo("#${sid}-sub", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, ${Math.min(3.5, sc.dur * 0.45)});`);
  if (sid === "outro") sfx(sc, "chime.mp3", Math.min(3.5, sc.dur * 0.45), 0.25);
  prevHead = null;
  prevSplit = null;
  return `<div class="av" id="${sid}-av" style="left:${avX}px">${inner}</div>
<div class="at" style="left:${tX}px"><div class="ak" id="${sid}-k">${esc(sc.kicker)}</div><div class="al" id="${sid}-l">${sc.lines.map(esc).join("<br/>")}</div>${sub}</div>`;
}

function cautionScene(sc) {
  const sid = sc.id;
  tw.push(`tl.fromTo("#${sid}-bar", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power3.out" }, 0.15);`);
  wipe(`#${sid}-ck`, 0.3, 0.4);
  wipe(`#${sid}-cm`, 0.5, 0.8);
  tw.push(`tl.fromTo("#${sid}-src", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.9);`);
  return `<div class="cau"><div class="cbar" id="${sid}-bar"></div><div class="ck" id="${sid}-ck">꼭 확인하세요</div><div class="cm" id="${sid}-cm">최종 인정 학점은<br/>학교와 교육청의 평가에 따라 달라집니다</div></div>
<div class="src" id="${sid}-src">출처 · BC Graduation Requirements · BC International Student Graduation Credit Policy<br/>Ontario: Earning your high school diploma · Ontario Schools K-12: Student records and transfers</div>`;
}

for (const sc of SCENES) {
  tw.length = 0;
  const body =
    sc.layout === "transcript" ? transcriptScene(sc) : sc.layout === "avatar" ? avatarScene(sc) : sc.layout === "caution" ? cautionScene(sc) : splitScene(sc);
  const html = `<template>
<style>${CSS}</style>
<div id="root" data-composition-id="${sc.id}" data-width="${W}" data-height="${H}">
${body}
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  ${tw.join("\n  ")}
  tl.set({}, {}, ${sc.dur});
  window.__timelines["${sc.id}"] = tl;
</script>
</template>
`;
  writeFileSync(join(ROOT, "compositions", `${sc.id}.html`), html);
}

// ── 자막 (내레이션 글자 타이밍 → 4~5어절 묶음)
const CAPS = [];
const toScreen = (t) => t.replace(/에이에이캐나다/g, "AA Canada");
for (const sc of SCENES) {
  if (sc.layout === "avatar") {
    // HeyGen 영상: 문장 구간 안에서 4어절 이하로 나누고 글자 수 비례로 시간 배분
    for (const [a, b, sent] of AVATAR_SEGS[sc.id]) {
      const groups = [];
      let g = [];
      for (const w of sent.split(" ")) {
        g.push(w);
        if (g.length >= 4 || g.join(" ").length >= 18 || /[,]$/.test(w)) (groups.push(g.join(" ")), (g = []));
      }
      if (g.length) groups.push(g.join(" "));
      const total = groups.reduce((n, x) => n + x.length, 0);
      let t = a;
      for (const x of groups) {
        const d = ((b - a) * x.length) / total;
        CAPS.push({ s: r2(sc.start + t - 0.05), e: r2(sc.start + t + d + 0.15), text: toScreen(x).replace(/[.]$/, "") });
        t += d;
      }
    }
    continue;
  }
  const words = [];
  let cur = null;
  const startIdx = sc.text.indexOf("]") + 1;
  for (let i = startIdx; i < sc.chars.length; i++) {
    const ch = sc.chars[i];
    if (ch === " ") {
      if (cur) words.push(cur), (cur = null);
      continue;
    }
    if (!cur) cur = { w: "", s: sc.cs[i], e: sc.ce[i] };
    cur.w += ch;
    cur.e = sc.ce[i];
  }
  if (cur) words.push(cur);
  let g = [];
  const flush = () => {
    if (!g.length) return;
    CAPS.push({ s: r2(sc.start + LEAD + g[0].s - 0.05), e: r2(sc.start + LEAD + g[g.length - 1].e + 0.15), text: toScreen(g.map((x) => x.w).join(" ").replace(/[.]$/, "")) });
    g = [];
  };
  for (const w of words) {
    g.push(w);
    const len = g.map((x) => x.w).join(" ").length;
    if (/[.,?!]$/.test(w.w) || g.length >= 5 || len >= 20) flush();
  }
  flush();
}
for (let i = 0; i < CAPS.length - 1; i++) if (CAPS[i].e > CAPS[i + 1].s - 0.02) CAPS[i].e = r2(CAPS[i + 1].s - 0.02);

const capHtml = CAPS.map((c, i) => `<div class="cg" id="cap${i}"><span>${esc(c.text)}</span></div>`).join("\n");
const capTw = CAPS.map(
  (c, i) =>
    `tl.set("#cap${i}", { opacity: 1, visibility: "visible" }, ${c.s}); tl.to("#cap${i}", { opacity: 0, duration: 0.1, ease: "power2.in" }, ${r2(c.e - 0.1)}); tl.set("#cap${i}", { opacity: 0, visibility: "hidden" }, ${c.e});`,
).join("\n  ");
writeFileSync(
  join(ROOT, "compositions/captions.html"),
  `<template>
<style>
@font-face { font-family: "Pretendard"; font-weight: 800; src: url("assets/fonts/Pretendard-ExtraBold.woff2") format("woff2"); }
#root { position: absolute; inset: 0; pointer-events: none; font-family: "Pretendard", sans-serif; }
#root .cg { position: absolute; left: 0; right: 0; bottom: 64px; text-align: center; opacity: 0; visibility: hidden; overflow: visible; word-break: keep-all; }
#root .cg span { display: inline-block; max-width: 1500px; background: rgba(16, 24, 32, .84); color: #fff; font-size: 42px; font-weight: 800;
  letter-spacing: -0.02em; line-height: 1.3; padding: 10px 28px; border-radius: 10px; }
</style>
<div id="root" data-composition-id="captions" data-width="${W}" data-height="${H}">
${capHtml}
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  ${capTw}
  tl.set({}, {}, ${TOTAL});
  window.__timelines["captions"] = tl;
</script>
</template>
`,
);

// ── 루트 index.html: 장면 + 자막 + 내레이션 + BGM + 효과음
const hosts = SCENES.map(
  (sc) =>
    `      <div id="${sc.id}" data-composition-id="${sc.id}" data-composition-src="compositions/${sc.id}.html" data-start="${sc.start}" data-duration="${sc.dur}" data-track-index="1" data-track-kind="graphics" data-width="${W}" data-height="${H}" style="z-index:1"></div>`,
).join("\n");
const vo = SCENES.filter((s) => s.layout !== "avatar" || s.video)
  .map((s) =>
    s.layout === "avatar"
      ? `      <audio id="vo-${s.id}" src="assets/voice/${s.id}-heygen.mp3" data-start="${s.start}" data-duration="${r2(probe(`assets/voice/${s.id}-heygen.mp3`) - 0.08)}" data-track-index="10" data-volume="1.35"></audio>`
      : `      <audio id="vo-${s.id}" src="assets/voice/${s.id}.mp3" data-start="${r2(s.start + LEAD)}" data-duration="${r2(s.voiceDur - 0.08)}" data-track-index="10" data-volume="1"></audio>`,
  )
  .join("\n");
const sfxDur = { "pop.mp3": 0.72, "click.mp3": 0.36, "click-soft.mp3": 0.36, "whoosh-short.mp3": 0.57, "impact-bass-1.mp3": 2.1, "chime.mp3": 2.5, "ping.mp3": 1.3 };
const sfxHtml = SFX.map(
  (x, i) => `      <audio id="sfx${i}" src="assets/sfx/${x.file}" data-start="${x.t}" data-duration="${sfxDur[x.file]}" data-track-index="${20 + (i % 3)}" data-volume="${x.vol}"></audio>`,
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
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="${TOTAL}" data-track-index="5" data-track-kind="captions" data-width="${W}" data-height="${H}" style="z-index:5"></div>
${vo}
      <audio id="bgm" src="assets/music/bgm.mp3" data-start="0" data-duration="${Math.min(TOTAL, 205)}" data-track-index="15" data-volume="0.22" data-fade-in="1.5" data-fade-out="4"></audio>
${sfxHtml}
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
writeFileSync(join(ROOT, "scripts/.timing.json"), JSON.stringify({ total: TOTAL, scenes: SCENES.map((s) => ({ id: s.id, start: s.start, dur: s.dur })), captions: CAPS.length, sfx: SFX.length }, null, 1));
console.log(`total ${TOTAL}s, captions ${CAPS.length}, sfx ${SFX.length}`);
console.log(SCENES.map((s) => `${s.id} ${s.start}+${s.dur}`).join("  "));
