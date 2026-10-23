// EMSB 롱폼 11장면 (16:9). 자막은 SCRIPT.txt에서 자동으로 가져오고, 여기서는 화면만 정의합니다.
// 타이밍은 cue("c<문장번호>")로 걸어 두었기 때문에 녹음 길이가 바뀌어도 화면이 문장을 따라갑니다.
import * as K from "../lib/components.mjs";

export const SOURCE = "출처: EMSB 2027-28 International Student Program 자료 (2026.10 기준) · 금액은 모두 캐나다 달러(CAD)";
export const FREE_NOTE = "※ 학비 면제: 퀘벡 교육부 면제 규정, 부모 학교·체류 조건에 따라 다름 · 상담 필요";
export const GRAD_NOTE = "※ 졸업률: 퀘벡 영어 공립 교육청 중 졸업률 1위 92.1% (2024-25학년도, EMSB 2026.09 발표)";

const SCHOOL = [1920, 1920];
const SCHOOL_CROP = [0, 300, 1920, 1100];
const MAP = { src: "gb_hs_network_map.jpg", size: [1920, 960], crop: [480, 130, 640, 620] };

const bg = (c) =>
  K.blob(c, { box: [1460, -260, 760, 760] }) + K.blob(c, { box: [-240, 760, 520, 520], color: "#ffe9e3" });

const schoolCard = (c, { box, src, name, sub, at, crop = SCHOOL_CROP }) =>
  K.photo(c, { src, size: SCHOOL, crop, box, at, a: "pop", label: name, sub, kb: "in", kbFrom: 0 });

export const scenes = [
  {
    id: "s01",
    render: (c) => `
      ${K.photo(c, { src: "gb_cover.jpg", size: [1920, 1920], crop: [60, 510, 1720, 740], box: [0, 0, 1920, 1080], bleed: true, kb: "left" })}
      <div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(255,248,242,.97) 0%,rgba(255,248,242,.94) 46%,rgba(255,248,242,.45) 72%,rgba(255,248,242,.12) 100%)"></div>
      <div class="redbar"></div>
      ${K.srctag(c)}
      ${K.text(c, "몬트리올 영어 공립학교 EMSB 기준", { box: [96, 200, 980], size: 40, at: 0.2, out: "c3" })}
      ${K.title(c, "중학생 아이, 캐나다 공립학교 *1년* 학비는?", { box: [96, 270, 1000], size: 100, at: 0.4, out: "c1" })}
      ${K.bignum(c, { box: [96, 300, 960], value: 15170, pre: "CAD", size: 210, label: "중고등 1년 · *보험 포함* · 2027-28", at: "c1", out: "c3" })}
      ${K.text(c, "몬트리올 영어 공립학교", { box: [96, 190, 1000], size: 54, at: "c3", cls: "kicker", style: "color:var(--ink);font-weight:900" })}
      ${K.title(c, "EMSB 완전정리", { box: [96, 262, 1100], size: 150, at: "c3+0.2" })}
      ${K.title(c, "*2027-28*", { box: [96, 440, 1000], size: 120, at: "c3+0.4" })}
      ${K.chips(c, [{ t: "학비", at: "c3@0.2" }, { t: "입학 조건 · 신청", at: "c3@0.4" }, { t: "고등학교 8곳", at: "c3@0.75", cls: "solid" }], { box: [96, 620, 1100] })}
      ${K.text(c, "몬트리올 전문 유학원 <span class='num'>AA Canada</span>", { box: [96, 740, 1000], size: 44, at: "c4", style: "color:var(--ink);font-weight:900" })}
    `,
  },
  {
    id: "s02",
    chapter: ["1장", "EMSB는 어떤 곳"],
    foot: [GRAD_NOTE, SOURCE],
    render: (c) => `
      ${bg(c)}
      ${K.title(c, "EMSB", { box: [64, 128, 400], size: 72, at: 0.3 })}
      ${K.text(c, "English Montreal School Board", { box: [300, 150, 680], size: 34, at: 0.5, style: "color:var(--ink);font-weight:900" })}
      ${K.text(c, "몬트리올 영어 교육청", { box: [300, 198, 680], size: 30, at: 0.7 })}
      ${K.img(c, { src: "emsb_isp_logo.png", box: [64, 262, 300, 112], at: 1.0 })}
      ${K.photo(c, { src: "isp_montreal_skyline.jpg", size: [1920, 1080], crop: [430, 120, 1080, 540], box: [64, 420, 880, 440], kb: "in", at: 0.8, out: "c3" })}
      ${K.photo(c, { src: "isp_territory_map.jpg", size: [1920, 1080], box: [64, 420, 880, 440], kb: "in", kbFrom: "c3", at: "c3", a: "pop", label: "EMSB 관할 지역", sub: "몬트리올 섬 중심부 ~ 동쪽 · 지하철·버스 통학" })}
      ${K.card(c, { box: [1000, 150, 856, 200], t: "퀘벡 최대 영어 공립 교육청", at: "c1", a: "right" })}
      ${K.card(c, { box: [1000, 380, 856, 200], pre: '<div class="cs" style="margin:0 0 6px">학생 수</div>', count: { value: 35000, pre: "약", suf: "명" }, at: "c1@0.55", a: "right" })}
      ${K.card(c, { box: [1000, 610, 856, 250], cls: "hl", pre: '<div class="cbig" style="font-size:96px">92.1%</div>', t: "퀘벡 영어 공립 교육청 중 졸업률 1위 92.1%", tsize: 34, s: "2024-25학년도", at: "c2", a: "right" })}
    `,
  },
  {
    id: "s03",
    chapter: ["2장", "누가 갈 수 있나"],
    render: (c) => {
      const x0 = 64, w = 1792, gap = 8, n = 11, sw = (w - gap * (n - 1)) / n;
      const segs = Array.from({ length: n }, (_, i) =>
        K.seg(c, { box: [x0 + i * (sw + gap), 150, sw, 78], text: `${i + 1}`, size: 40, at: `c0@${(0.05 + i * 0.06).toFixed(2)}`, a: "pop", bg: i < 6 ? "var(--sub)" : "var(--red)" })
      ).join("");
      const sx = (i) => x0 + i * (sw + gap);
      return `
      ${bg(c)}
      ${segs}
      ${K.tick(c, { box: [sx(0), 236, sx(6) - gap - sx(0)], text: "초등 1~6학년", at: "c0@0.6", color: "var(--sub)" })}
      ${K.tick(c, { box: [sx(6), 236, x0 + w - sx(6)], text: "중고등 7~11학년", at: "c0@0.75", color: "var(--red)" })}
      ${K.tick(c, { box: [sx(0) - 20, 276, sw + 40], text: "만 *6*세", at: "c1@0.35", a: "pop" })}
      ${K.tick(c, { box: [sx(6) - 20, 276, sw + 40], text: "만 *12*세", at: "c1@0.6", a: "pop" })}
      ${K.tick(c, { box: [sx(10) - 20, 276, sw + 40], text: "만 *16*세", at: "c1@0.85", a: "pop" })}
      ${K.tick(c, { box: [sx(2), 286, sx(5) - sx(2)], text: "나이: 그해 *9월 30일* 기준", at: "c1@0.1", color: "var(--muted)", size: 26 })}
      <div class="card" ${K.anim(c, "rise", "c2")} style="left:64px;top:350px;width:870px;height:500px;justify-content:flex-start">
        <div class="ct">중고등학생 <em>(7~11학년)</em></div>
        <div class="cs" style="color:var(--red)">혼자 와서 홈스테이로 다닐 수 있어요</div>
      </div>
      ${K.checklist(c, [{ t: "단독 유학 + 홈스테이 가능", at: "c2@0.4" }, { t: "성적 양호", at: "c3@0.2" }, { t: "학습장애 진단 없음", at: "c3@0.6" }], { box: [100, 520, 800] })}
      <div class="card hl" ${K.anim(c, "rise", "c4")} style="left:986px;top:350px;width:870px;height:500px;justify-content:flex-start">
        <div class="ct">초등학생 <em>(1~6학년)</em></div>
        <div class="cs" style="color:var(--sub)">아래 <em>3가지 중 하나</em>가 필요해요</div>
      </div>
      ${K.checklist(c, [
        { icon: "①", t: "형·누나가 EMSB 고교 국제학생", at: "c6@0.05" },
        { icon: "②", t: "부모가 EMSB 직업·성인교육 등록", at: "c6@0.35" },
        { icon: "③", t: "부모 동반 거주 (아이 돌봄)", at: "c6@0.7" },
      ], { box: [1022, 520, 800] })}
      ${K.seg(c, { box: [986, 800, 870, 70], text: "초등 = 가족과 *함께* 오는 구조", at: "c7", a: "pop", bg: "var(--ink)", size: 34 })}
    `;
    },
  },
  {
    id: "s04",
    chapter: ["3장", "2027-28 학비"],
    render: (c) => `
      ${bg(c)}
      ${K.title(c, "2027-28 국제학생 학비 <span style='font-size:.6em;color:var(--sub)'>CAD · 보험 포함</span>", { box: [64, 140, 1300], size: 64, at: 0.2 })}
      ${K.feeTable(c, {
        box: [64, 240, 1140, 380],
        at: "c1",
        cols: ["구분", "1년 (10개월)", "반년 (5개월)"],
        rowH: 155,
        rows: [
          { label: "초등", sub: "1~6학년", at: "c2", cells: [{ value: 12020, at: "c2@0.15" }, { value: 6260, at: "c2@0.65" }] },
          { label: "중고등", sub: "7~11학년", at: "c3", cells: [{ value: 15170, at: "c3@0.15" }, { value: 7835, at: "c3@0.65" }] },
        ],
      })}
      ${K.text(c, "추가 비용", { box: [1260, 244, 600], size: 34, at: "c4", style: "color:var(--ink);font-weight:900" })}
      ${K.card(c, { box: [1260, 300, 596, 100], t: "신청비 <em>CAD 250</em>", at: "c4@0.05", a: "right", style: "padding:16px 28px" })}
      ${K.card(c, { box: [1260, 420, 596, 100], t: "교통카드 <em>월 CAD 65</em>", at: "c4@0.35", a: "right", style: "padding:16px 28px" })}
      ${K.card(c, { box: [1260, 540, 596, 100], t: "교복 <em>CAD 250~300</em>", at: "c4@0.7", a: "right", style: "padding:16px 28px" })}
      ${K.seg(c, { box: [64, 670, 1792, 110], text: "⚠ 학비 중 *CAD 1,000*은 환불 불가 → 일정 확정 후 신청", at: "c5", a: "pop", bg: "#fff", color: "var(--ink)", size: 44, style: "border:4px dashed var(--red);font-family:var(--body);font-weight:900" })}
      ${K.photo(c, { src: "isp_fee_table_crop.jpg", size: [1330, 820], box: [1100, 150, 720, 444], kb: "in", kbFrom: "end-4.5", kbDur: 4.4, at: "end-4.5", a: "pop", overlay: true, label: "원본 자료", sub: "EMSB 2027-28 International Student Program Fees" })}
    `,
  },
  {
    id: "s05",
    chapter: ["4장", "단기 스쿨링"],
    render: (c) => {
      const cards = [
        { m: "3", v: 4901, e: "3,956", at: "c1@0.1", cat: "c2@0.25" },
        { m: "4", v: 6368, e: "5,108", at: "c1@0.4", cat: "c2@0.7" },
        { m: "5", v: 7835, e: "6,260", at: "c1@0.7", cat: "c2+0.6" },
      ];
      const months = ["9월", "10월", "11월", "12월", "1월", "2월", "3월", "4월", "5월", "6월"];
      const cx = 64, cw = 1792 / 10;
      return `
      ${bg(c)}
      ${K.title(c, "1년이 부담스럽다면? <em>3개월부터</em>", { box: [64, 136, 1400], size: 64, at: 0.2 })}
      ${cards.map((k, i) => K.card(c, {
        box: [64 + i * 607, 236, 578, 290], at: k.at, a: "pop", cls: i === 0 ? "hl" : "",
        pre: `<div class="ct" style="font-size:56px"><em>${k.m}</em>개월</div><div class="cs" style="margin:6px 0 4px">중고등 (보험 포함)</div>`,
        count: { value: k.v, pre: "CAD" }, countAt: k.cat,
        s: `초등 CAD ${k.e}`, ssize: 24,
      })).join("")}
      ${months.map((m, i) => K.tick(c, { box: [cx + i * cw, 556, cw], text: m, at: "c3-0.3", size: 28, color: "var(--muted)" })).join("")}
      ${K.seg(c, { box: [cx, 600, cw * 3 - 8, 54], text: "3개월", at: "c3@0.1" })}
      ${K.seg(c, { box: [cx, 662, cw * 4 - 8, 54], text: "4개월", at: "c3@0.5" })}
      ${K.seg(c, { box: [cx, 724, cw * 5 - 8, 54], text: "5개월 (9월~1월)", at: "c4@0.1", bg: "var(--sub)" })}
      ${K.seg(c, { box: [cx + cw * 5, 724, cw * 5 - 8, 54], text: "5개월 (2/1~6/23)", at: "c4@0.45", bg: "var(--sub)" })}
      ${K.chips(c, [{ t: "2월 학기는 자리 제한", cls: "warn", at: "c4@0.75" }], { box: [cx + cw * 5, 790, 900] })}
      ${K.chips(c, [{ t: "교실에 직접 앉아 보는 한 학기", cls: "solid", at: "c5" }], { box: [64, 790, 880] })}
    `;
    },
  },
  {
    id: "s06",
    chapter: ["5장", "신청 일정·서류"],
    render: (c) => `
      ${bg(c)}
      ${K.seg(c, { box: [64, 150, 1792, 70], text: "신청 기간 *12월 1일* ~ *5월 31일*", at: "c0+0.2", size: 40, style: "font-family:var(--display)" })}
      ${K.chips(c, [{ t: "True North 온라인 포털로만 접수", at: "c1+0.2", cls: "soft" }], { box: [64, 236, 1792], justify: "center" })}
      ${K.group(c, { at: "c2", out: "c4" }, `
        ${K.text(c, "준비 서류", { box: [64, 330, 600], size: 36, at: "c2", style: "color:var(--ink);font-weight:900" })}
        ${K.checklist(c, [
          { t: "여권", at: "c2@0.08" },
          { t: "상세 기본증명서 + 공증 번역본", at: "c2@0.2" },
          { t: "최근 3년치 성적표", at: "c2@0.38" },
          { t: "현재 학교 추천서", at: "c2@0.55" },
          { t: "예방접종 기록", at: "c2@0.68" },
          { t: "학생 계약서 (부모·학생 서명)", at: "c2@0.82" },
          { t: "영어: 듀오링고 점수 · *5/31까지*", at: "c3", hl: true, icon: "!" },
        ], { box: [64, 390, 1792], cols: 2 })}
      `)}
      ${K.flow(c, [
        { t: "지원서 접수", s: "약 2주", at: "c4" },
        { t: "입학허가서", s: "약 2주 · 신청비 CAD 250", at: "c4@0.3" },
        { t: "CAQ + 학생비자", s: "6~20주", at: "c4@0.6" },
        { t: "도착 후 Eligibility 발급", s: "약 2주 · 1~3년 유효", at: "c5" },
        { t: "등교!", s: "", at: "c5@0.75" },
      ], { box: [64, 330, 1792, 250] })}
      ${K.photo(c, { src: "isp_coe.jpg", size: [1920, 1080], crop: [0, 0, 1920, 1080], box: [1256, 610, 600, 300], kb: "in", kbFrom: "c5", at: "c5@0.3", a: "pop", out: "c6" })}
      ${K.seg(c, { box: [64, 640, 1100, 100], text: "9월 입학 → *늦어도 봄*에는 신청 완료!", at: "c6", a: "pop", size: 46, bg: "var(--ink)", style: "font-family:var(--display)" })}
    `,
  },
  {
    id: "s07",
    chapter: ["6장", "고등학교 8곳 · 동부"],
    render: (c) => `
      ${bg(c)}
      ${K.photo(c, { ...MAP, box: [64, 140, 760, 730], kb: "in", at: 0.2, pins: [
        { x: 898, y: 599, label: "FACE", at: "c2" },
        { x: 806, y: 401, label: "JFK", at: "c3" },
        { x: 864, y: 352, label: "Laurier Mac", at: "c4" },
        { x: 774, y: 213, label: "LB Pearson", at: "c5" },
      ] })}
      ${K.title(c, "국제학생 받는 고등학교 *8곳*", { box: [870, 140, 990], size: 60, at: "c0", out: "c2" })}
      ${K.chips(c, [{ t: "먼저 동부 4곳", cls: "solid", at: "c1" }], { box: [870, 240, 900], out: "c2" })}
      ${schoolCard(c, { box: [870, 140, 482, 350], src: "school_face.jpg", name: "FACE", sub: "다운타운 · 예술(음악·미술·연극·무용)", at: "c2" })}
      ${schoolCard(c, { box: [1374, 140, 482, 350], src: "school_jfk.jpg", name: "John F. Kennedy", sub: "미디어아트 · 하키 · 로보틱스", at: "c3", crop: [0, 200, 1920, 1100] })}
      ${schoolCard(c, { box: [870, 512, 482, 350], src: "school_lauriermac.jpg", name: "Laurier Macdonald", sub: "생레오나르 · IB 중등 · 미적분 가속반", at: "c4" })}
      ${schoolCard(c, { box: [1374, 512, 482, 350], src: "school_lesterbpearson.jpg", name: "Lester B. Pearson", sub: "몬트리올 북쪽 · 스포츠 특화 · 이탈리아어", at: "c5", crop: [0, 200, 1920, 1100] })}
    `,
  },
  {
    id: "s08",
    chapter: ["7장", "고등학교 8곳 · 서부"],
    render: (c) => `
      ${bg(c)}
      ${K.photo(c, { ...MAP, box: [64, 140, 760, 730], kb: "in", at: 0.2, pins: [
        { x: 571, y: 625, label: "LaurenHill", at: "c1" },
        { x: 797, y: 712, label: "Marymount", at: "c2" },
        { x: 746, y: 729, label: "Royal Vale", side: "left", at: "c3" },
        { x: 864, y: 670, label: "Westmount", at: "c4" },
      ] })}
      ${K.title(c, "서부 *4곳*", { box: [870, 140, 990], size: 64, at: "c0", out: "c1" })}
      ${schoolCard(c, { box: [870, 140, 482, 350], src: "school_laurenhill.jpg", name: "LaurenHill Academy", sub: "생로랑 · STEAM · 예술 과정", at: "c1" })}
      ${schoolCard(c, { box: [1374, 140, 482, 350], src: "school_marymount.jpg", name: "Marymount Academy Intl.", sub: "국제학생 최다 · IB 과정", at: "c2", crop: [0, 380, 1920, 1100] })}
      ${schoolCard(c, { box: [870, 512, 482, 350], src: "school_royalvale.jpg", name: "Royal Vale", sub: "수학·과학 중심 · 7학년 입학시험", at: "c3" })}
      ${schoolCard(c, { box: [1374, 512, 482, 350], src: "school_westmount.jpg", name: "Westmount High", sub: "1873년 개교 · AP 과정", at: "c4" })}
      <div class="abs" ${K.anim(c, "fade", "c5")} style="inset:0;background:rgba(255,248,242,.82)"></div>
      ${K.flow(c, [
        { t: "희망 학교 *3곳* 제출", s: "지원서에 순위대로", at: "c5+0.1" },
        { t: "EMSB가 최종 배정", s: "자리 상황에 따라", at: "c5@0.55" },
      ], { box: [260, 380, 1400, 260] })}
    `,
  },
  {
    id: "s09",
    chapter: ["8장", "학교생활과 지원"],
    render: (c) => `
      ${bg(c)}
      ${K.group(c, { at: 0, out: "c4" }, `
        ${K.card(c, { box: [64, 150, 560, 230], big: "영어", t: "모든 수업은 영어로", at: "c0+0.1", a: "pop" })}
        ${K.card(c, { box: [650, 150, 560, 230], big: "불어", t: "전 학년 *제2언어* 필수", at: "c0@0.55", a: "pop", cls: "hl" })}
        ${K.text(c, "영어 + 불어 = 두 언어에 자연스럽게 익숙해지는 도시", { box: [64, 404, 1150], size: 32, at: "c1" })}
        ${K.card(c, { box: [64, 480, 1146, 300], cls: "red", pre: '<div class="ct" style="font-size:46px">과목당</div>', count: { value: 60, suf: "점 이상 = 학점 인정" }, countAt: "c2", at: "c2", a: "pop", s: "1년만 다녀도 똑같이 적용 → 성적 관리 필수", ssize: 30 })}
        ${K.photo(c, { src: "school_westmount.jpg", size: SCHOOL, crop: [0, 600, 1920, 1320], box: [1250, 150, 606, 630], kb: "up", at: 0.4 })}
      `)}
      ${K.group(c, { at: "c4", out: "c6" }, `
        ${K.title(c, "대신 지원도 있어요", { box: [64, 150, 1792], size: 70, at: "c4", align: "center" })}
        ${K.card(c, { box: [160, 330, 760, 360], big: "매주", t: "영어·불어 *온라인 방과후 튜터링*", at: "c5", a: "pop" })}
        ${K.card(c, { box: [1000, 330, 760, 360], big: "24시간", t: "*모국어* 상담 서비스", at: "c5@0.55", a: "pop", cls: "hl" })}
      `)}
      ${K.group(c, { at: "c6", out: "c8" }, `
        ${K.photo(c, { src: "isp_excursions.jpg", size: [1920, 1080], crop: [0, 0, 1880, 1060], box: [64, 140, 1220, 690], kb: "in", kbFrom: "c6", at: "c6" })}
        ${K.card(c, { box: [1320, 140, 536, 240], count: { value: 4, pre: "연", suf: "회 이상" }, t: "현장학습", at: "c6+0.2", a: "pop" })}
        ${K.chips(c, [{ t: "퀘벡시티", at: "c7@0.05" }, { t: "스키", at: "c7@0.2" }, { t: "슈가쉑 (메이플 농장)", at: "c7@0.45" }, { t: "수도 오타와", at: "c7@0.8", cls: "solid" }], { box: [1320, 420, 536] })}
      `)}
      ${K.group(c, { at: "c8" }, `
        ${K.photo(c, { src: "pamphlet_p2.jpg", size: [1920, 1484], crop: [1320, 170, 600, 420], box: [64, 270, 600, 420], kb: "out", kbFrom: "c8", at: "c8" })}
        ${K.quote(c, { box: [710, 170, 1146, 620], text: "처음엔 영어와 불어를 동시에 배워야 해서 힘들었어요. 하지만 선생님과 친구들 덕분에 이겨낼 수 있었어요. 완전히 새로운 세상에 눈을 뜨게 해줬어요.", by: "- Ji Yeon, 한국 (EMSB 국제학생 팸플릿)", at: "c8+0.3" })}
      `)}
    `,
  },
  {
    id: "s10",
    chapter: ["9장", "홈스테이 & 초등 부모님"],
    foot: [FREE_NOTE, SOURCE],
    render: (c) => `
      ${bg(c)}
      ${K.group(c, { at: 0, out: "c2" }, `
        ${K.title(c, "홈스테이는 어떻게?", { box: [64, 150, 1792], size: 72, at: 0.2, align: "center" })}
        ${K.card(c, { box: [160, 320, 760, 380], big: "✕", t: "EMSB가 *직접 운영하지 않음*", at: "c0+0.2", a: "pop" })}
        ${K.card(c, { box: [1000, 320, 760, 380], big: "추천 업체", t: "+ 후견인 필수", s: "캐나다 시민권자 또는 영주권자", at: "c1", a: "pop", cls: "hl" })}
      `)}
      ${K.title(c, "초등 자녀 부모님이라면 꼭!", { box: [64, 140, 1792], size: 62, at: "c2", align: "center" })}
      ${K.card(c, { box: [64, 236, 870, 320], pre: '<div class="cs" style="margin:0 0 6px;font-size:30px">부모 <b>동반만</b> 할 때</div>', count: { value: 12020, pre: "CAD", suf: " / 년" }, t: "자녀 = 국제학생 학비", at: "c3", a: "left" })}
      ${K.card(c, { box: [986, 236, 870, 320], cls: "red", pre: '<div class="cs" style="margin:0 0 6px;font-size:30px">부모가 퀘벡에서 <b>학생비자</b>로 공부할 때</div>', big: "학비 면제", t: "동반 자녀 공립학교", at: "c4", a: "right" })}
      ${K.chips(c, [{ t: "다만 몇 가지 조건 있음 · 상담 필요", cls: "warn", at: "c5" }], { box: [986, 574, 870], justify: "center" })}
      ${K.feeTable(c, {
        box: [64, 650, 1792, 204], at: "c6", grid: "1fr 1fr 1fr", rowH: 72, headH: 60,
        cols: ["자녀 수", "부모 동반만 (1년)", "부모 학생비자 (1년)"],
        rows: [
          { label: "아이 1명", at: "c6@0.1", cells: [{ value: 12020, at: "c6@0.15" }, { value: 0, at: "c6@0.3" }] },
          { label: "아이 2명", at: "c6@0.5", cells: [{ value: 24040, at: "c6@0.55" }, { value: 0, at: "c6@0.7" }] },
        ],
      })}
    `,
  },
  {
    id: "s11",
    chapter: ["정리", "한눈에 보기"],
    render: (c) => `
      ${bg(c)}
      ${K.group(c, { at: 0, out: "c4" }, `
        ${K.title(c, "정리하겠습니다", { box: [64, 150, 1792], size: 76, at: 0.2 })}
        ${K.checklist(c, [
          { icon: "1", t: "중고등학생은 혼자서도 OK · 1년 학비 *CAD 15,170* (보험 포함)", at: "c1" },
          { icon: "2", t: "*3개월*부터 짧게 경험 가능", at: "c2" },
          { icon: "3", t: "신청 *12/1 ~ 5/31* · 학교 배정은 자리 상황에 따라 → 일찍 준비", at: "c3" },
        ], { box: [64, 290, 1792], size: 46 })}
      `)}
      ${K.cta(c, { box: [360, 170, 1200, 560], at: "c4", l1: "우리 아이 학교·일정·학비 절약법까지", l2: "AA Canada 무료 상담", l3: "카카오톡 canlog", l4: "☎ 02-567-4345 · aacanada.co.kr" })}
      ${K.img(c, { src: "emsb_isp_logo.png", box: [810, 760, 300, 112], at: "c4+0.6" })}
    `,
  },
];

// YouTube 썸네일 1280x720 (정지 화면, 같은 컴포넌트 사용)
export const thumbnail = (c) => `
  ${K.photo(c, { src: "gb_cover.jpg", size: [1920, 1920], crop: [700, 560, 1100, 700], box: [520, 0, 760, 720], bleed: true, kb: null })}
  <div class="abs" style="inset:0;background:linear-gradient(90deg,#FFF8F2 0%,#FFF8F2 44%,rgba(255,248,242,.75) 58%,rgba(255,248,242,0) 80%)"></div>
  <div class="redbar" style="width:18px"></div>
  ${K.title(c, "캐나다 공립학교", { box: [56, 56, 800], size: 92 })}
  ${K.title(c, "1년 학비", { box: [56, 162, 800], size: 92 })}
  ${K.title(c, "*15,170*<span style='font-size:.5em'>달러</span>", { box: [50, 270, 900], size: 190 })}
  ${K.chips(c, [{ t: "CAD · 보험 포함", cls: "solid" }], { box: [62, 500, 600] })}
  ${K.text(c, "몬트리올 EMSB 2027-28 완전정리 · 학교 8곳", { box: [60, 600, 900], size: 38, style: "color:var(--ink);font-weight:900" })}
`;
