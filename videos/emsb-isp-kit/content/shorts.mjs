// EMSB 숏폼 12편 (9:16). 롱폼과 같은 컴포넌트(lib/components.mjs)를 재사용합니다.
// 자막은 SHORTS_SCRIPT.txt에서 자동으로 가져오고, cue "c<문장번호>"로 화면을 문장에 맞춥니다.
import * as K from "../lib/components.mjs";
import { SOURCE, FREE_NOTE } from "./longform.mjs";

const SQ = [1920, 1920];
const SCHOOL_SOURCE = "출처: EMSB 2027-28 International Student Program 자료 · 학교 소개 자료 (2026.10 기준)";
const MONEY_SOURCE = "출처: EMSB 2027-28 International Student Program 자료 (2026.10 기준) · CAD";

export const shorts = [
  { id: "face", series: ["몬트리올 학교 탐방", "1/8"], hook: "다운타운 한복판<br>예술 공립고", name: "FACE School", photo: "school_face.jpg",
    facts: [["c2@0.1", "음악·미술·연극·무용"], ["c2@0.6", "재즈밴드·오케스트라·합창"], ["c3", "악기 학교 대여"], ["c4@0.2", "48년째 예술 교육"], ["c4@0.7", "지하철 Peel·McGill역"]] },
  { id: "jfk", series: ["몬트리올 학교 탐방", "2/8"], hook: "미디어·영상<br>좋아하는 아이라면", name: "John F. Kennedy", photo: "school_jfk.jpg", crop: [0, 150, 1920, 1200],
    facts: [["c1", "빌레레 지역"], ["c2@0.1", "미디어아트·기술 선택"], ["c2@0.6", "과학·수학 심화"], ["c3@0.1", "로보틱스·하키·영화 클럽"], ["c4", "지하철 St-Michel역"]] },
  { id: "lmac", series: ["몬트리올 학교 탐방", "3/8"], hook: "공립학교에서<br>IB를?", name: "Laurier Macdonald", photo: "school_lauriermac.jpg",
    facts: [["c1@0.1", "생레오나르"], ["c1@0.6", "IB 중등 과정"], ["c2@0.1", "수학 가속반 → 미적분"], ["c2@0.5", "로보틱스·STEAM 클럽"], ["c2@0.8", "해외 문화 탐방·봉사 여행"]] },
  { id: "lbp", series: ["몬트리올 학교 탐방", "4/8"], hook: "운동 좋아하는<br>아이라면", name: "Lester B. Pearson", photo: "school_lesterbpearson.jpg", crop: [0, 150, 1920, 1200],
    facts: [["c1@0.1", "몬트리올 북쪽"], ["c1@0.6", "스포츠 특화반"], ["c2@0.1", "심화 수학·과학"], ["c2@0.6", "제3외국어 이탈리아어"], ["c3", "수학 경시·로보틱스·체스"]] },
  { id: "lha", series: ["몬트리올 학교 탐방", "5/8"], hook: "과학·기술·예술<br>STEAM 학교", name: "LaurenHill Academy", photo: "school_laurenhill.jpg",
    facts: [["c2@0.1", "생로랑"], ["c2@0.4", "주니어(7~8) 캠퍼스"], ["c2@0.7", "시니어(9~11) 캠퍼스"], ["c3@0.2", "미디어아트·영화·연극·음악"], ["c3@0.7", "코딩·게임 클럽"], ["c4", "지하철 Côte-Vertu역"]] },
  { id: "mma", series: ["몬트리올 학교 탐방", "6/8"], hook: "국제학생이<br>가장 많은 학교", name: "Marymount Academy Intl.", photo: "school_marymount.jpg", crop: [0, 380, 1920, 1200], hookCrop: [640, 380, 980, 1540],
    facts: [["c0@0.6", "국제학생·임시 체류 학생 최다"], ["c2@0.5", "IB 중등 과정"], ["c3", "IB 첫 1~2년 불어 몰입"], ["c4@0.3", "학습 지원 센터"], ["c5", "지하철 Villa-Maria역"]] },
  { id: "rv", series: ["몬트리올 학교 탐방", "7/8"], hook: "수학·과학<br>좋아하는 아이에게", name: "Royal Vale", photo: "school_royalvale.jpg",
    facts: [["c1@0.1", "NDG 지역"], ["c1@0.4", "유치원~11학년"], ["c1@0.75", "수학·과학 중심"], ["c2@0.2", "AP 준비 과정"], ["c2@0.6", "로보틱스·음악·연극·스포츠"], ["c3", "7학년 입학시험 · 정원 제한", "warn"]] },
  { id: "whs", series: ["몬트리올 학교 탐방", "8/8"], hook: "1873년 개교,<br>AP 학교", name: "Westmount High", photo: "school_westmount.jpg",
    facts: [["c0@0.3", "1873년 개교"], ["c2@0.2", "AP: 영문학·심리학"], ["c2@0.6", "AP: 미적분·환경과학"], ["c3@0.2", "농구·하키·컬링"], ["c3@0.7", "재즈밴드·연극"], ["c4", "지하철 Atwater·Vendôme역"]] },
  { id: "fee", series: ["EMSB 2027-28 한눈에", "1/4"], hook: "캐나다 공립학교<br>학비 한눈에<br>(2027-28)", name: "2027-28 국제학생 학비", photo: "school_laurenhill.jpg", money: true },
  { id: "short", series: ["EMSB 2027-28 한눈에", "2/4"], hook: "3개월만 다녀보는<br>캐나다 공립학교", name: "3·4·5개월 단기 스쿨링", photo: "isp_excursions.jpg", size: [1920, 1080], hookCrop: [0, 0, 600, 1060], money: true },
  { id: "apply", series: ["EMSB 2027-28 한눈에", "3/4"], hook: "9월 입학,<br>언제까지 뭘 준비?", name: "신청 일정·서류 체크리스트", photo: "school_lauriermac.jpg", money: true },
  { id: "free", series: ["EMSB 2027-28 한눈에", "4/4"], hook: "초등 학비<br>CAD 12,020 vs 0", name: "같은 학교, 학비가 다르다?", photo: "school_westmount.jpg", money: true, foot: [FREE_NOTE, MONEY_SOURCE] },
];

const hookLines = (c, sh, at = 0, out) =>
  sh.hook.split("<br>").map((l, i, arr) =>
    `<div class="hook"${K.anim(c, "pop", at + i * 0.15, { out })} style="top:${700 - arr.length * 70 + i * 140}px;font-size:${l.length > 9 ? 104 : 124}px">${K.md(l)}</div>`).join("");

const hookPhoto = (c, sh, o = {}) => {
  const size = sh.size ?? SQ;
  const crop = sh.hookCrop ?? [470, 380, 980, 1540]; // below the photo's own name label
  return K.photo(c, { src: sh.photo, size, crop, box: [0, 0, 1080, 1920], bleed: true, kb: "in", ...o }) + `<div class="hookbg"${o.out != null ? K.anim(c, "fade", 0, { out: o.out }) : ""}></div>`;
};

const factChips = (c, facts) =>
  K.chips(c, facts.map(([at, t, cls]) => ({ at, t, cls: cls ?? "" })), { box: [60, 1036, 960], justify: "center" });

// ---- topic bodies (photo zone 430..1300) ----
const BODY = {
  fee: (c) => `
    ${K.feeTable(c, { box: [60, 560, 960, 420], at: "c1", grid: "0.7fr 1.15fr 1.15fr", rowH: 175, headH: 70,
      cols: ["구분", "1년(10개월)", "반년(5개월)"],
      rows: [
        { label: "초등", at: "c2", cells: [{ value: 12020, at: "c2@0.1" }, { value: 6260, at: "c4@0.15" }] },
        { label: "중고등", at: "c2@0.45", cells: [{ value: 15170, at: "c2@0.55" }, { value: 7835, at: "c4@0.6" }] },
      ] })}
    ${K.chips(c, [{ t: "보험 포함", cls: "solid", at: "c3" }], { box: [60, 1000, 960], justify: "center" })}
    ${K.chips(c, [{ t: "신청비 CAD 250", at: "c5@0.05" }, { t: "교통 월 CAD 65", at: "c5@0.35" }, { t: "교복 CAD 250~300", at: "c5@0.7" }, { t: "⚠ CAD 1,000 환불 불가", cls: "warn", at: "c6" }], { box: [60, 1092, 960], justify: "center" })}`,
  short: (c) => `
    ${K.photo(c, { src: "isp_excursions.jpg", size: [1920, 1080], crop: [0, 0, 1920, 1080], box: [60, 560, 960, 330], kb: "in", at: 2.2, out: "c5" })}
    ${K.photo(c, { src: "gb_cover.jpg", size: SQ, crop: [60, 510, 1720, 740], box: [60, 560, 960, 330], kb: "in", kbFrom: "c5", at: "c5", a: "fade" })}
    ${[["3", 4901, "c2@0.3"], ["4", 6368, "c2@0.75"], ["5", 7835, "c3"]].map(([m, v, cat], i) => K.card(c, {
      box: [60 + i * 330, 910, 300, 220], at: `c1@${(0.2 + i * 0.25).toFixed(2)}`, a: "pop", cls: i === 0 ? "hl" : "", style: "padding:18px 20px;align-items:center;text-align:center",
      pre: `<div class="ct" style="font-size:52px"><em>${m}</em>개월</div><div class="cs" style="font-size:26px;margin:4px 0">중고등 CAD</div>`,
      count: { value: v }, countAt: cat })).join("")}
    ${K.chips(c, [{ t: "3·4·5개월 모두 9월 학기 시작", at: "c3@0.1" }], { box: [60, 1150, 960], justify: "center" })}`,
  apply: (c) => `
    ${K.seg(c, { box: [60, 560, 960, 84], text: "*12/1 ~ 5/31* 온라인 신청", at: "c1", size: 50, style: "font-family:var(--display)" })}
    ${K.checklist(c, [
      { t: "여권", at: "c2@0.08" },
      { t: "상세 기본증명서 + 공증 번역본", at: "c2@0.2" },
      { t: "최근 3년치 성적표", at: "c2@0.38" },
      { t: "현재 학교 추천서", at: "c2@0.55" },
      { t: "예방접종 기록", at: "c2@0.68" },
      { t: "학생 계약서 (서명)", at: "c2@0.82" },
      { t: "듀오링고 점수 *5/31까지*", at: "c3", hl: true, icon: "!" },
    ], { box: [60, 660, 960], size: 30 })}
    ${K.seg(c, { box: [60, 1200, 960, 90], text: "CAQ+학생비자 *6~20주* → 봄까지 신청!", at: "c4", a: "pop", bg: "var(--ink)", size: 40, style: "font-family:var(--display)" })}`,
  free: (c) => `
    ${K.card(c, { box: [60, 560, 960, 220], pre: '<div class="cs" style="margin:0 0 6px">부모 <b>동반만</b> 할 때</div>', count: { value: 12020, pre: "CAD", suf: " / 년" }, t: "자녀 = 국제학생 학비", at: "c1", a: "left" })}
    ${K.card(c, { box: [60, 796, 960, 220], cls: "red", pre: '<div class="cs" style="margin:0 0 6px">부모가 퀘벡에서 <b>학생비자</b>로 공부할 때</div>', big: "학비 면제", t: "동반 자녀 공립학교", at: "c2", a: "right" })}
    ${K.chips(c, [{ t: "다만 몇 가지 조건 있음 · 상담 필요", cls: "warn", at: "c3" }], { box: [60, 1030, 960], justify: "center" })}
    ${K.feeTable(c, { box: [60, 1110, 960, 240], at: "c4", grid: "0.8fr 1.2fr 1fr", rowH: 86, headH: 62,
      cols: ["자녀", "동반만(1년)", "학생비자"],
      rows: [
        { label: "1명", at: "c4@0.1", cells: [{ value: 12020, at: "c4@0.15" }, { value: 0, at: "c4@0.3" }] },
        { label: "2명", at: "c4@0.5", cells: [{ value: 24040, at: "c4@0.55" }, { value: 0, at: "c4@0.7" }] },
      ] })}`,
};

export function render(c, sh) {
  const size = sh.size ?? SQ;
  const body = BODY[sh.id]
    ? BODY[sh.id](c)
    : K.photo(c, { src: sh.photo, size, crop: sh.crop ?? [0, 300, 1920, 1200], box: [60, 560, 960, 460], kb: "in", at: 2.2 }) + factChips(c, sh.facts);
  const foot = (sh.foot ?? [sh.money ? MONEY_SOURCE : SCHOOL_SOURCE]).map((f) => `<div>${K.md(f)}</div>`).join("");
  return `
  <div class="stage"${K.anim(c, "drift", 0, { d: c.D })}>
    ${K.blob(c, { box: [720, 1380, 640, 640] })}${K.blob(c, { box: [-280, 1560, 620, 620], color: "#ffe9e3" })}
    ${K.text(c, sh.hook.replace(/<br>/g, " "), { box: [60, 412, 960], size: 34, at: 2.3, style: "color:var(--red);font-weight:900" })}
    ${K.title(c, sh.name, { box: [60, 456, 960], size: sh.name.length > 18 ? 54 : 64, at: 2.4 })}
    ${body}
  </div>
  ${hookPhoto(c, sh, { out: 2.4 })}
  ${hookLines(c, sh, 0.15, 2.4)}
  ${K.chapter(c, ...sh.series)}
  <div class="foot"${K.anim(c, "fade", 2.4)}>${foot}</div>
  ${K.cta(c, { box: [90, 600, 900, 680], at: "end-3", l1: sh.id.length > 0 && sh.money ? "자세한 상담은" : "EMSB 학교 상담은", l2: "AA Canada", l3: "카카오톡 canlog", l4: "☎ 02-567-4345" })}`;
}

/** 1080x1920 cover frame: hook text + photo (static). */
export const cover = (c, sh) => `
  ${hookPhoto(c, sh)}
  ${hookLines(c, sh)}
  ${K.chapter(c, ...sh.series)}
  <div class="abs" style="left:60px;right:60px;top:1240px;text-align:center"><span class="chip solid" style="font-size:44px;display:inline-block">${K.md(sh.name)}</span></div>
`;
