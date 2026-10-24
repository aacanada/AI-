#!/usr/bin/env node
// Montreal private-college card news -> two 9:16 shorts (college_a, college_b).
//   node build.mjs        -> writes college_a/index.html, college_b/index.html (+ assets/kit copies)
//   node build.mjs cover  -> also writes cover-src/ (thumbnail compositions)
// Timing comes from <short>/timing.json + assets/alignment.json (written by tools/tts.py):
// scene changes sit on script-line cues, number slams on the exact spoken word.
import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const SHARED = join(ROOT, "_shared");
const LEAD = 0.35;
const r3 = (x) => Math.round(x * 1000) / 1000;

function loadTiming(k) {
  const dir = join(ROOT, `college_${k}`);
  const tm = JSON.parse(readFileSync(join(dir, "timing.json"), "utf8"));
  const al = JSON.parse(readFileSync(join(dir, "assets/alignment.json"), "utf8")).alignment;
  const st = al.character_start_times_seconds;
  const first = al.characters.findIndex((c) => !/\s/.test(c));
  const off = st[first] - LEAD;
  let pos = 0;
  const offs = tm.cues.map((c) => { const p = pos; pos += c.spoken.length + 1; return p; });
  const c = (i) => tm.cues[i].start;
  // time of a spoken substring inside cue i (respelled text, e.g. "팔백삼십")
  const at = (i, sub) => {
    const idx = tm.cues[i].spoken.indexOf(sub);
    if (idx < 0) throw new Error(`cue ${i}: "${sub}" not in "${tm.cues[i].spoken}"`);
    return r3(st[offs[i] + idx] - off);
  };
  return { dir, cues: tm.cues, audio: tm.audioDuration, c, at };
}

// ---------- shared pieces ----------
const CSS = readFileSync(join(ROOT, "style.css"), "utf8");
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
// caption: numbers / money in mustard
const capHtml = (s) => esc(s).replace(/(\$?[0-9][0-9,.:]*(?:만\s?원대|만\s?원|달러|원|시간|세)?)/g, '<span class="n">$1</span>');

const brand = (dark) => `<div class="brand ${dark ? "on-dark" : ""}"><i></i>AA Canada</div>`;
const badge = (id, n) => `<div class="badge" id="${id}">${n}</div>`;
const lines = (id, cls, arr, top) =>
  `<div class="h1 ${cls}" id="${id}" style="top:${top}px">${arr.map((l) => `<span class="ln"><span class="m">${l}</span></span>`).join("")}</div>`;
const foot = (id, text, dark) => `<div class="foot ${dark ? "on-dark" : ""}" id="${id}">${text}</div>`;

function mapBlock(p, top) {
  return `<div class="map" id="${p}-map" style="top:${top}px">
  <div class="map-in" id="${p}-mapin"><img src="assets/kit/map.png" alt=""></div>
  <div class="ring" id="${p}-ring"></div>
  <div class="ring to" id="${p}-ring2"></div>
</div>`;
}

function ctaScene(p) {
  return `<div class="sc bg-deep" id="${p}">
  <div class="deco d1"></div><div class="deco d2"></div>
  ${brand(true)}
  <div class="pill" id="${p}-pill" style="top:300px">무료 상담</div>
  ${lines(`${p}-h`, "xl on-dark", ["우리 가족은", '<em>얼마면</em> 될까?'], 400)}
  <div class="cta-sub" id="${p}-sub">몬트리올 자녀무상교육 상담</div>
  <div class="cta-brand" id="${p}-aa"><i></i>AA Canada</div>
  <div class="kakao" id="${p}-kakao"><span class="kk">카카오톡</span> canlog</div>
  <div class="insta" id="${p}-insta">@aa.montreal</div>
</div>`;
}
function ctaAnim(p, T, cHead, cSub, tKakao) {
  return [
    `rise('#${p}-pill', ${cHead + 0.1})`,
    `mask('#${p}-h .m', ${cHead + 0.2}, 0.18)`,
    `hl('#${p}-h em', ${cHead + 0.9})`,
    `rise('#${p}-sub', ${cSub})`,
    `pop('#${p}-aa', ${cSub + 0.25})`,
    `slam('#${p}-kakao', ${tKakao})`,
    `rise('#${p}-insta', ${tKakao + 0.45})`,
    `tl.fromTo('#${p}-kakao', {scale:1}, {scale:1.04, duration:0.5, yoyo:true, repeat:3, ease:'sine.inOut'}, ${tKakao + 1.1})`,
  ];
}

function rentScene(p, top0 = 240) {
  return `<div class="sc bg-cream" id="${p}">
  ${brand(false)}
  ${top0 ? badge(`${p}-b`, "3") : ""}
  <div class="kicker" id="${p}-k" style="top:372px">캐나다 2번째 대도시인데</div>
  ${lines(`${p}-h`, "md", ['렌트는 <span class="u">중소도시 수준</span>'], 440)}
  ${mapBlock(p, 590)}
  <div class="stamp" id="${p}-stamp">토론토보다 매달 <b id="${p}-830">$830</b> 저렴</div>
  ${foot(`${p}-f`, "출처: 캐나다 통계청(Statistics Canada) 2026년 2분기 · 방 2개 평균 호가 월세 (CAD)")}
</div>`;
}
function rentAnim(p, t0, tZoom, tOut, t830) {
  return [
    `rise('#${p}-b', ${t0 + 0.35})`,
    `rise('#${p}-k', ${t0 + 0.45})`,
    `mask('#${p}-h .m', ${t0 + 0.55})`,
    `hl('#${p}-h .u', ${t0 + 1.0})`,
    `rise('#${p}-map', ${t0 + 0.7}, {y:80})`,
    `tl.fromTo('#${p}-mapin', {scale:1}, {scale:1.85, duration:1.5, ease:'power3.inOut'}, ${tZoom})`,
    `ring('#${p}-ring', ${tZoom + 1.2})`,
    `tl.to('#${p}-mapin', {scale:1, duration:1.1, ease:'power3.inOut'}, ${tOut})`,
    `tl.to('#${p}-ring', {opacity:0, duration:0.3}, ${tOut})`,
    `ring('#${p}-ring2', ${tOut + 0.9})`,
    `slam('#${p}-stamp', ${t830 - 0.15})`,
    `count('#${p}-830', ${t830 - 0.15}, 830, '$', 0.8)`,
    `rise('#${p}-f', ${t0 + 1.4})`,
  ];
}

// ---------- A: 압도적으로 저렴하게 ----------
function buildA() {
  const T = loadTiming("a");
  const { c, at } = T;
  const S = [0, c(2) - 0.3, c(6) - 0.12, c(11) - 0.3, c(13) - 0.3, c(18) - 0.12].map(r3);
  const END = r3(T.audio + 1.0);
  const scenes = [
    `<div class="sc bg-green" id="a1">
  <div class="deco d1"></div><div class="deco d2"></div><div class="deco d3"></div>
  ${brand(true)}
  <div class="pill" id="a1-pill" style="top:300px">수업 스케줄 조정 가능한 사립컬리지</div>
  <div class="h1 cover on-dark" id="a1-h" style="top:420px">
    <span class="ln s"><span class="m">캐나다 자녀무상교육</span></span>
    <span class="ln xl2"><span class="m mus">압도적으로</span></span>
    <span class="ln xl2"><span class="m mus">저렴하게</span></span>
    <span class="ln s"><span class="m">가는 방법</span></span>
  </div>
</div>`,
    `<div class="sc bg-cream" id="a2">
  ${brand(false)}
  ${badge("a2-b", "1")}
  ${lines("a2-h", "", ["학비부터", '<span class="u">확 낮췄어요</span>'], 370)}
  <div class="gcard" id="a2-card" style="top:650px">
    <div class="g-sub">부모 학비 · 1년 · 몬트리올 사립컬리지 비즈니스 과정</div>
    <div class="g-big"><span class="g-yak">약</span><span class="g-num" id="a2-1000">1,000</span><span class="g-unit">만원대</span></div>
    <div class="g-note">2년 총 CAD 22,250 기준</div>
  </div>
  <div class="check" id="a2-chk" style="top:1070px"><i>✓</i>공인 영어점수 없이 입학</div>
  <div class="zero" id="a2-zero" style="top:1160px"><span class="zl">아이 공립학교 학비</span><span class="zn" id="a2-0">0<small>원</small></span></div>
</div>`,
    `<div class="sc bg-cream" id="a3">
  ${brand(false)}
  ${badge("a3-b", "2")}
  ${lines("a3-h", "", ["아이 학교 간 사이,", '<span class="u">아르바이트</span>가 됩니다'], 370)}
  <div class="sched" id="a3-s" style="top:615px">
    <div class="lane" style="top:30px"><span class="who">아이</span><div class="blk school" id="a3-school">학교</div></div>
    <div class="lane" style="top:132px"><span class="who">부모</span>
      <div class="blk class" id="a3-class">수업</div>
      <div class="blk work" id="a3-work">아르바이트</div>
    </div>
    <div class="axis"><span>오전</span><span>오후</span><span>저녁</span></div>
  </div>
  <div class="calc" id="a3-c" style="top:905px">
    <div class="c-eq" id="a3-eq">퀘벡 최저시급 <b>$16.60</b> × 주 <b>24시간</b></div>
    <div class="c-big" id="a3-big">월 약 <span id="a3-1726">$1,726</span></div>
    <div class="c-krw" id="a3-krw">≈ 170만원 <small>(세전)</small></div>
  </div>
  ${foot("a3-f", "퀘벡 최저시급 $16.60 (2026.5.1 시행) · 학기 중 주 24시간, 풀타임 정규과정 등록 조건")}
</div>`,
    rentScene("a4"),
    `<div class="sc bg-cream" id="a5">
  ${brand(false)}
  ${badge("a5-b", "4")}
  ${lines("a5-h", "", ["아이와 함께여도", '<span class="u">차 없이</span> 사는 도시'], 370)}
  <div class="receipt" id="a5-r" style="top:625px">
    <div class="row" id="a5-r1"><span>자동차 보험료 (퀘벡 평균)</span><b>연 $1,067</b></div>
    <div class="row" id="a5-r2"><span>차량 등록비 (몬트리올)</span><b>연 $401</b></div>
    <div class="row" id="a5-r3"><span>기름값 (연 1.5만km 가정)</span><b>연 약 $2,280</b></div>
    <div class="row dim" id="a5-r4"><span>주차 (시내 실내 주차장)</span><b>월 $175~300</b></div>
    <div class="row tot" id="a5-tot"><span>차 구입비 빼고도</span><b>연 <span id="a5-3700">$3,700</span>+</b></div>
  </div>
  <div class="gpanel" id="a5-g" style="top:1040px">
    <div id="a5-g1">대신 어른 지하철·버스 정기권 <em>월 $110</em></div>
    <div id="a5-g2">만 11세 이하 아이는 보호자 동반 시 <em class="free" id="a5-free">무료</em></div>
  </div>
  ${foot("a5-f", "출처: 퀘벡 손해보험협회(GAA) 2025 평균 · SAAQ 2026 등록비 · 퀘벡 에너지청 몬트리올 휘발유 평균 189.8¢/L(2026.10.19~23), 연비 8L/100km 가정 · STM 요금표(2026.7.1 시행) · 주차비는 업계 조사 범위로 합계에서 제외")}
</div>`,
    ctaScene("a6"),
  ];
  const anim = [
    // cover
    `rise('#a1-pill', 0.15)`,
    `mask('#a1-h .ln:nth-child(1) .m', 0.3)`,
    `slam('#a1-h .ln:nth-child(2) .m', ${at(1, "압도적")})`,
    `slam('#a1-h .ln:nth-child(3) .m', ${at(1, "저렴하게")})`,
    `mask('#a1-h .ln:nth-child(4) .m', ${at(1, "가는")})`,
    // tuition
    `rise('#a2-b', ${S[1] + 0.35})`, `mask('#a2-h .m', ${S[1] + 0.45})`, `hl('#a2-h .u', ${at(2, "확")})`,
    `rise('#a2-card', ${c(3) - 0.1}, {y:80})`,
    `count('#a2-1000', ${at(3, "천만")}, 1000, '', 0.9)`, `slam('#a2-card .g-big', ${at(3, "천만")})`,
    `pop('#a2-chk', ${at(4, "공인")})`,
    `rise('#a2-zero', ${c(5) - 0.1})`, `slam('#a2-0', ${at(5, "학비가")})`,
    // work
    `rise('#a3-b', ${S[2] + 0.35})`, `mask('#a3-h .m', ${S[2] + 0.45})`, `hl('#a3-h .u', ${at(7, "아르바이트")})`,
    `rise('#a3-s', ${S[2] + 0.8}, {y:60})`,
    `grow('#a3-school', ${S[2] + 1.1})`, `grow('#a3-class', ${S[2] + 1.35})`,
    `tl.to('#a3-class', {x: 400, duration: 0.8, ease: 'power3.inOut'}, ${at(8, "조정")})`,
    `tl.fromTo('#a3-work', {opacity:0, y:-70}, {opacity:1, y:0, duration:0.55, ease:'back.out(1.8)'}, ${at(8, "조정") + 0.5})`,
    `rise('#a3-c', ${c(9) - 0.1}, {y:60})`, `rise('#a3-eq', ${c(9) + 0.1})`,
    `slam('#a3-big', ${at(10, "한 달")})`, `count('#a3-1726', ${at(10, "한 달")}, 1726, '$', 1.0)`,
    `pop('#a3-krw', ${at(10, "백칠십")})`, `rise('#a3-f', ${c(9) + 0.4})`,
    // rent
    ...rentAnim("a4", S[3], at(11, "몬트리올") + 0.2, at(12, "토론토"), at(12, "팔백삼십")),
    // car
    `rise('#a5-b', ${S[4] + 0.35})`, `mask('#a5-h .m', ${S[4] + 0.45})`, `hl('#a5-h .u', ${at(13, "차 없이")})`,
    `rise('#a5-r', ${c(14) - 0.2}, {y:60})`,
    `rise('#a5-r1', ${at(14, "보험")}, {y:20})`, `rise('#a5-r2', ${at(14, "등록비")}, {y:20})`,
    `rise('#a5-r3', ${at(15, "기름값")}, {y:20})`, `rise('#a5-r4', ${at(15, "기름값") + 0.5}, {y:20})`,
    `slam('#a5-tot', ${at(15, "삼천칠백")})`, `count('#a5-3700', ${at(15, "삼천칠백")}, 3700, '$', 0.9)`,
    `tl.to('#a5-r .row:not(.tot)', {opacity:0.4, duration:0.4}, ${c(16) + 0.1})`,
    `rise('#a5-g', ${c(16)}, {y:80})`, `rise('#a5-g1', ${c(16) + 0.15})`, `rise('#a5-g2', ${c(17)})`,
    `slam('#a5-free', ${at(17, "보호자")})`, `rise('#a5-f', ${S[4] + 1.4})`,
    // cta
    ...ctaAnim("a6", T, S[5], c(19), at(20, "카카오톡")),
  ];
  const sfx = [
    ...S.slice(1).map((t) => ["whoosh-short", t, 0.22]),
    ["impact-bass-1", at(1, "압도적"), 0.28], ["impact-bass-1", at(3, "천만"), 0.25], ["pop", at(5, "학비가"), 0.3],
    ["impact-bass-1", at(10, "한 달"), 0.22], ["impact-bass-1", at(12, "팔백삼십") - 0.15, 0.25],
    ["impact-bass-1", at(15, "삼천칠백"), 0.22], ["pop", at(17, "보호자"), 0.3], ["pop", at(20, "카카오톡"), 0.3],
  ];
  return { k: "a", T, S, END, scenes, anim, sfx, bgm: "bgm-a", title: "college_a" };
}

// ---------- B: 아이 둘 학원비로 ----------
function buildB() {
  const T = loadTiming("b");
  const { c, at } = T;
  const S = [0, c(2) - 0.3, c(6) - 0.3, c(7) - 0.3, c(9) - 0.3, c(13) - 0.3].map(r3);
  const END = r3(T.audio + 1.0);
  const scenes = [
    `<div class="sc bg-green" id="b1">
  <div class="deco d1"></div><div class="deco d2"></div><div class="deco d3"></div>
  ${brand(true)}
  <div class="pill" id="b1-pill" style="top:300px">몬트리올 사립컬리지</div>
  <div class="h1 cover on-dark" id="b1-h" style="top:420px">
    <span class="ln xl2"><span class="m">아이 둘</span></span>
    <span class="ln xl2"><span class="m mus">학원비로,</span></span>
    <span class="ln s2"><span class="m">캐나다</span></span>
    <span class="ln s2"><span class="m">자녀무상교육?</span></span>
  </div>
</div>`,
    `<div class="sc bg-cream" id="b2">
  ${brand(false)}
  <div class="kicker" id="b2-k" style="top:250px">한 달 기준</div>
  ${lines("b2-h", "md", ['학원비 <span class="vs">vs</span> 몬트리올'], 310)}
  <div class="cols" id="b2-cols">
    <div class="col" id="b2-c1" style="left:0">
      <div class="val" id="b2-v1">약 <b id="b2-121">121</b>만원</div>
      <div class="bar ink" id="b2-bar1" style="height:430px"></div>
      <div class="lab">한국 학원비<small>사교육 받는 아이 2명 · 월평균</small></div>
    </div>
    <div class="col" id="b2-c2" style="left:318px">
      <div class="val" id="b2-v2">약 <b id="b2-90">90</b>만원대</div>
      <div class="bar green" id="b2-bar2" style="height:320px"></div>
      <div class="lab">몬트리올 부모 학비<small>사립컬리지 · 월 환산</small></div>
    </div>
    <div class="col" id="b2-c3" style="left:636px">
      <div class="val big" id="b2-v3"><b>0</b>원</div>
      <div class="bar mus" id="b2-bar3" style="height:10px"></div>
      <div class="lab">아이 공립학교 학비<small>&nbsp;</small></div>
    </div>
  </div>
  ${foot("b2-f", "학원비: 2025년 초중고 사교육비조사(국가데이터처·교육부) 참여학생 1인당 월평균 60.4만원 × 2 · 부모 학비: 사립컬리지 비즈니스 과정 2년 총 CAD 22,250 기준 월 환산")}
</div>`,
    rentScene("b3", 0),
    `<div class="sc bg-cream" id="b4">
  ${brand(false)}
  ${lines("b4-h", "", ["아낀 돈으로,", '<span class="u">원어민 1:1 튜터</span>'], 300)}
  <div class="gcard" id="b4-g" style="top:560px">
    <div class="g-sub">렌트에서 아끼는 돈 (토론토 대비)</div>
    <div class="g-big"><span class="g-num" id="b4-830">$830</span><span class="g-unit">/ 월</span></div>
  </div>
  <div class="week" id="b4-w" style="top:900px">
    <div class="w-top"><span class="w-rate" id="b4-rate">시간당 <b>$40</b></span><span class="w-sum" id="b4-sum">주 약 <b>5시간</b></span></div>
    <div class="days">${["월", "화", "수", "목", "금"].map((d, i) => `<div class="day"><div class="slot"><div class="fill" id="b4-d${i}"></div></div><span>${d}</span></div>`).join("")}</div>
  </div>
  ${foot("b4-f", "렌트 차이: 캐나다 통계청 2026년 2분기 방 2개 평균 월세(토론토 $2,650 − 몬트리올 $1,820) · 튜터비는 시간당 $40 기준, 튜터에 따라 달라요")}
</div>`,
    `<div class="sc bg-cream" id="b5">
  ${brand(false)}
  ${lines("b5-h", "xl", ['학교 <em class="plus">+</em> 튜터'], 300)}
  <div class="duo" id="b5-d1" style="top:520px"><i>학교</i><div><b>친구들과 영어로 자연스럽게</b><span>쉬는 시간, 점심시간에도 영어로 어울려요</span></div></div>
  <div class="duo" id="b5-d2" style="top:735px"><i>튜터</i><div><b>1:1로 체계적으로</b><span>아이 수준에 맞춰 학교 수업을 따라잡아요</span></div></div>
  <div class="gbar" id="b5-g" style="top:975px">
    <div class="gtxt"><div>학교 + 튜터,</div><div>아이 영어가 <em>빠르게</em> 늘 수 있어요</div></div>
    <svg viewBox="0 0 200 140" class="up"><path id="b5-path" d="M10 125 L70 90 L115 100 L190 20" /><path id="b5-head" d="M150 18 L192 18 L192 60" /></svg>
  </div>
</div>`,
    ctaScene("b6"),
  ];
  const anim = [
    `rise('#b1-pill', 0.15)`,
    `slam('#b1-h .ln:nth-child(1) .m', 0.3)`,
    `slam('#b1-h .ln:nth-child(2) .m', ${at(0, "학원비로")})`,
    `mask('#b1-h .ln:nth-child(3) .m', ${c(1)})`,
    `mask('#b1-h .ln:nth-child(4) .m', ${at(1, "자녀")})`,
    // compare
    `rise('#b2-k', ${S[1] + 0.35})`, `mask('#b2-h .m', ${S[1] + 0.45})`,
    `bar('#b2-bar1', ${at(3, "학원비") - 0.2})`, `rise('#b2-c1 .lab', ${c(2) + 0.6})`,
    `pop('#b2-v1', ${at(3, "백이십일")})`, `count('#b2-121', ${at(3, "백이십일")}, 121, '', 0.8)`,
    `bar('#b2-bar2', ${at(4, "부모")})`, `rise('#b2-c2 .lab', ${c(4) + 0.3})`,
    `pop('#b2-v2', ${at(4, "구십만")})`, `count('#b2-90', ${at(4, "구십만")}, 90, '', 0.7)`,
    `bar('#b2-bar3', ${c(5)})`, `rise('#b2-c3 .lab', ${c(5) + 0.1})`, `slam('#b2-v3', ${at(5, "영 원")})`,
    `rise('#b2-f', ${S[1] + 1.2})`,
    // rent
    ...rentAnim("b3", S[2], c(6) + 0.6, at(6, "토론토"), at(6, "팔백삼십")),
    // tutor
    `mask('#b4-h .m', ${S[3] + 0.4})`, `hl('#b4-h .u', ${at(7, "원어민")})`,
    `rise('#b4-g', ${S[3] + 0.6}, {y:70})`, `count('#b4-830', ${S[3] + 0.7}, 830, '$', 0.8)`,
    `rise('#b4-w', ${c(8) - 0.2}, {y:70})`, `pop('#b4-rate', ${at(8, "사십")})`,
    `tl.fromTo('#b4-w .fill', {scaleY:0}, {scaleY:1, duration:0.32, ease:'back.out(1.6)', stagger:0.16}, ${at(8, "일주일")})`,
    `slam('#b4-sum', ${at(8, "다섯")})`, `rise('#b4-f', ${S[3] + 1.2})`,
    // school + tutor
    `slam('#b5-h .m', ${S[4] + 0.4})`,
    `tl.fromTo('#b5-d1', {opacity:0, x:-120}, {opacity:1, x:0, duration:0.6, ease:'power3.out'}, ${c(9)})`,
    `tl.fromTo('#b5-d2', {opacity:0, x:120}, {opacity:1, x:0, duration:0.6, ease:'power3.out'}, ${c(10)})`,
    `rise('#b5-g', ${c(11)}, {y:70})`,
    `tl.fromTo('#b5-path', {strokeDashoffset:300}, {strokeDashoffset:0, duration:0.9, ease:'power2.out'}, ${at(12, "빠르게") - 0.3})`,
    `tl.fromTo('#b5-head', {opacity:0}, {opacity:1, duration:0.2}, ${at(12, "빠르게") + 0.5})`,
    `hl('#b5-g em', ${at(12, "빠르게")})`,
    // cta
    ...ctaAnim("b6", T, S[5], c(14), at(15, "카카오톡")),
  ];
  const sfx = [
    ...S.slice(1).map((t) => ["whoosh-short", t, 0.22]),
    ["impact-bass-1", at(0, "학원비로"), 0.28], ["pop", at(3, "백이십일"), 0.25], ["pop", at(4, "구십만"), 0.25],
    ["impact-bass-1", at(5, "영 원"), 0.25], ["impact-bass-1", at(6, "팔백삼십") - 0.15, 0.25],
    ["pop", at(8, "다섯"), 0.28], ["pop", at(15, "카카오톡"), 0.3],
  ];
  return { k: "b", T, S, END, scenes, anim, sfx, bgm: "bgm-b", title: "college_b" };
}

const RUNTIME = `
const tl = gsap.timeline({ paused: true });
const q = (s) => document.querySelectorAll(s);
function rise(s, t, o = {}) { tl.fromTo(s, { opacity: 0, y: o.y ?? 40 }, { opacity: 1, y: 0, duration: o.d ?? 0.55, ease: 'power3.out', stagger: o.st ?? 0 }, t); }
function mask(s, t, st = 0.12) { tl.fromTo(s, { yPercent: 115 }, { yPercent: 0, duration: 0.6, ease: 'power4.out', stagger: st }, t); }
function slam(s, t) {
  tl.fromTo(s, { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: 0.38, ease: 'power4.in' }, t - 0.2);
  tl.fromTo(s, { x: 0 }, { keyframes: { x: [-10, 8, -5, 2, 0] }, duration: 0.3, ease: 'none' }, t + 0.18);
}
function pop(s, t) { tl.fromTo(s, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2.2)' }, t); }
function hl(s, t) { tl.fromTo(s, { backgroundSize: '0% 30%' }, { backgroundSize: '100% 30%', duration: 0.55, ease: 'power2.inOut' }, t); }
function grow(s, t) { tl.fromTo(s, { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: 'power3.out' }, t); }
function bar(s, t) { tl.fromTo(s, { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: 'power3.out' }, t); }
function ring(s, t) {
  tl.fromTo(s, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)' }, t);
  tl.fromTo(s, { boxShadow: '0 0 0 0 rgba(200,16,46,.55)' }, { boxShadow: '0 0 0 34px rgba(200,16,46,0)', duration: 0.9, repeat: 2, ease: 'power1.out' }, t + 0.4);
}
function count(s, t, to, pre, d) {
  const el = document.querySelector(s), o = { v: 0 };
  tl.fromTo(o, { v: 0 }, { v: to, duration: d, ease: 'power2.out', onUpdate: () => { el.textContent = pre + Math.round(o.v).toLocaleString('en-US'); } }, t);
}
function enter(s, prev, t) {
  tl.fromTo(s, { yPercent: 100 }, { yPercent: 0, duration: 0.55, ease: 'power3.inOut' }, t);
  if (prev) tl.fromTo(prev, { yPercent: 0 }, { yPercent: -18, duration: 0.55, ease: 'power3.inOut' }, t);
}
function caps() {
  q('.cap').forEach((c) => {
    const t = parseFloat(c.dataset.start);
    tl.fromTo(c.firstElementChild, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.2, ease: 'power2.out' }, t);
  });
}
function decos(end) {
  q('.deco').forEach((d, i) => tl.fromTo(d, { rotation: 0, x: 0 }, { rotation: i % 2 ? -25 : 25, x: i % 2 ? 40 : -40, duration: end, ease: 'none' }, 0));
}
`;

// 4:5 feed version (1080x1350): same scenes/timing; each scene's 9:16 content band (y 130-1330:
// brand -> footnote) is placed in a .stage scaled by STAGE.s, captions move to the frame bottom.
const STAGE = { s: 0.92, top: 26, band: 130 };
const CSS_4X5 = `
html, body { height: 1350px; }
.stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0;
  transform: translate(${r3((1080 * (1 - STAGE.s)) / 2)}px, ${r3(STAGE.top - STAGE.band * STAGE.s)}px) scale(${STAGE.s}); }
.cap { padding-bottom: 30px; }
.cap-in { max-width: 990px; font-size: 46px; padding: 12px 30px 16px; }
`;

function page(P, fmt = "9x16") {
  const { k, T, S, END, anim, sfx, bgm } = P;
  const v45 = fmt === "4x5";
  const H = v45 ? 1350 : 1920;
  // wrap scene content (everything inside the full-bleed .sc background) in a .stage for 4:5
  const scenes = v45 ? P.scenes.map((h) => h.replace(/^(<div class="sc[^>]*>)/, '$1<div class="stage">').replace(/<\/div>\s*$/, "</div></div>")) : P.scenes;
  const id = v45 ? `college_${k}_4x5` : `college_${k}`;
  const sceneIds = scenes.map((s) => s.match(/id="([^"]+)"/)[1]);
  const secs = scenes.map((html, i) => {
    const start = S[i], stop = i + 1 < S.length ? S[i + 1] + 0.6 : END;
    return `<section class="clip scene" id="sec-${sceneIds[i]}" data-start="${start}" data-duration="${r3(stop - start)}" data-track-index="${1 + (i % 2)}">\n${html}\n</section>`;
  });
  const capClips = T.cues.map((cu, i) => {
    const s = r3(cu.start - 0.05), e = i + 1 < T.cues.length ? T.cues[i + 1].start - 0.05 : Math.min(END, cu.end + 0.8);
    return `<div class="cap clip" data-start="${s}" data-duration="${r3(e - s)}" data-track-index="5"><div class="cap-in">${capHtml(cu.text)}</div></div>`;
  });
  const fadeOut = r3(END - 1.6);
  const bgmAuto = JSON.stringify({ version: 1, lanes: [{ target: "volume", points: [{ t: 0, v: 0 }, { t: 1.2, v: 0.11 }, { t: fadeOut, v: 0.11 }, { t: END, v: 0 }] }] });
  const sfxTags = sfx.map(([n, t, v], i) => `<audio id="sfx-${i}" src="assets/kit/sfx/${n}.mp3" data-start="${r3(Math.max(0, t))}" data-duration="1.2" data-track-index="${12 + i}" data-volume="${v}"></audio>`);
  const enters = sceneIds.slice(1).map((sid, i) => `enter('#${sid}', '#${sceneIds[i]}', ${S[i + 1]})`);
  return `<!doctype html>
<!-- GENERATED by videos/college-card-shorts/build.mjs — edit build.mjs / style.css, not this file. -->
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=${H}" />
<script src="assets/kit/gsap.min.js"></script>
<style>
${CSS}${v45 ? CSS_4X5 : ""}
</style>
</head>
<body>
<div id="root" data-composition-id="${id}" data-start="0" data-width="1080" data-height="${H}" data-duration="${END}">
${secs.join("\n")}
${capClips.join("\n")}
<audio id="vo" src="assets/voice.m4a" data-start="0" data-duration="${T.audio}" data-track-index="10" data-volume="1"></audio>
<audio id="bgm" src="assets/kit/${bgm}.mp3" data-start="0" data-duration="${END}" data-track-index="11" data-volume="1" data-automation='${bgmAuto}'></audio>
${sfxTags.join("\n")}
</div>
<script>
${RUNTIME}
const FACES = ['400 40px "Black Han Sans"', '400 40px "Pretendard"', '600 40px "Pretendard"', '700 40px "Pretendard"', '900 40px "Pretendard"'];
Promise.all(FACES.map((f) => document.fonts.load(f, '가A1'))).then(() => {
${[...enters, ...anim].map((l) => "  " + l + ";").join("\n")}
  caps();
  decos(${END});
  window.__timelines["${id}"] = tl;
});
</script>
</body>
</html>
`;
}

function copyKit(dir, bgm) {
  const kit = join(dir, "assets/kit");
  mkdirSync(join(kit, "sfx"), { recursive: true });
  cpSync(join(SHARED, "fonts"), join(kit, "fonts"), { recursive: true });
  cpSync(join(SHARED, "sfx"), join(kit, "sfx"), { recursive: true });
  cpSync(join(SHARED, "gsap.min.js"), join(kit, "gsap.min.js"));
  cpSync(join(SHARED, "img/map.png"), join(kit, "map.png"));
  cpSync(join(SHARED, `music/${bgm}.mp3`), join(kit, `${bgm}.mp3`));
}

for (const P of [buildA(), buildB()]) {
  const dir = join(ROOT, P.title);
  copyKit(dir, P.bgm);
  writeFileSync(join(dir, "index.html"), page(P));
  if (!existsSync(join(dir, "hyperframes.json")))
    writeFileSync(join(dir, "hyperframes.json"), JSON.stringify({ $schema: "https://hyperframes.heygen.com/schema/hyperframes.json", paths: { blocks: "compositions", components: "compositions/components", assets: "assets" }, media: { autoProxy: true } }, null, 2) + "\n");
  console.log(`${P.title}: ${P.END}s, scenes at ${P.S.join(", ")}`);
  // 4:5 feed project: own folder, voice copied in (gitignored assets)
  const d45 = join(ROOT, `${P.title}_4x5`);
  copyKit(d45, P.bgm);
  cpSync(join(dir, "assets/voice.m4a"), join(d45, "assets/voice.m4a"));
  writeFileSync(join(d45, "index.html"), page(P, "4x5"));
  cpSync(join(dir, "hyperframes.json"), join(d45, "hyperframes.json"));
}
