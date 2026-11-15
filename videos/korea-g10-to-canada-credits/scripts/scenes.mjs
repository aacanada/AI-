// 장면 데이터 — 모든 장면의 문구·블록 상태·시간이 이 파일 하나에서 나온다.
// 출처 메모는 STORYBOARD.md / SPEC.md 참고. 숫자를 바꾸면 여기만 바꾼다.

export const BC_CELLS = [
  // 1행: 10학년 필수
  { id: "la10", t: "LA 10", kind: "req" },
  { id: "ma10", t: "수학 10", kind: "req" },
  { id: "sc10", t: "과학 10", kind: "req" },
  { id: "ss10", t: "사회 10", kind: "req" },
  { id: "pe10", t: "체육 10", kind: "req" },
  // 2행
  { id: "cle", t: "CLE", kind: "req" },
  { id: "art", t: "예술·ADST", kind: "req" },
  { id: "la11", t: "LA 11", kind: "req" },
  { id: "ma11", t: "수학 11/12", kind: "req" },
  { id: "sc11", t: "과학 11/12", kind: "req" },
  // 3행
  { id: "ss11", t: "사회 11/12", kind: "req" },
  { id: "la12", t: "LA 12", kind: "req", g12: true },
  { id: "clc", t: "CLC", kind: "req", g12: true },
  { id: "e1", t: "선택", kind: "elec" },
  { id: "e2", t: "선택", kind: "elec" },
  // 4행
  { id: "e3", t: "선택", kind: "elec" },
  { id: "e4", t: "선택", kind: "elec" },
  { id: "e5", t: "선택", kind: "elec" },
  { id: "e6", t: "선택", kind: "elec" },
  { id: "e7", t: "선택", kind: "elec" },
];

export const ON_CELLS = [
  { id: "en9", t: "영어 9", kind: "req" },
  { id: "en10", t: "영어 10", kind: "req" },
  { id: "en11", t: "영어 11", kind: "req" },
  { id: "en12", t: "영어 12", kind: "req" },
  { id: "ma9", t: "수학 9", kind: "req" },
  { id: "ma10", t: "수학 10", kind: "req" },
  { id: "ma11", t: "수학 11/12", kind: "req" },
  { id: "sc9", t: "과학 9", kind: "req" },
  { id: "sc10", t: "과학 10", kind: "req" },
  { id: "geo", t: "지리 9", kind: "req" },
  { id: "his", t: "역사 10", kind: "req" },
  { id: "art", t: "예술", kind: "req" },
  { id: "pe", t: "체육", kind: "req" },
  { id: "fsl", t: "불어", kind: "req" },
  { id: "tech", t: "기술", kind: "req" },
  { id: "cc", t: "진로·시민", kind: "req" },
  { id: "stem", t: "STEM", kind: "req" },
  ...Array.from({ length: 13 }, (_, i) => ({ id: `o${i + 1}`, t: "선택", kind: "elec" })),
];

const BC_G10 = ["ma10", "sc10", "ss10", "pe10"];
const BC_LOCK = ["la11", "la12", "sc11", "ma11", "ss11", "cle", "clc"];
const ON_LOCAL = ["en11", "en12", "ma11", "o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10", "o11"];

// 블록 상태 계산기
const base = (cells) => Object.fromEntries(cells.map((c) => [c.id, c.kind]));
const all = (cells, st) => Object.fromEntries(cells.map((c) => [c.id, st]));

const bcEq = () => ({ ...all(BC_CELLS, "open"), ...Object.fromEntries(BC_G10.map((i) => [i, "eq"])) });
const bcLock = () => ({ ...bcEq(), ...Object.fromEntries(BC_LOCK.map((i) => [i, "lock"])) });
const bcDone = () => {
  const s = bcEq();
  for (const i of ["la10", "cle", "la11", "ma11", "sc11", "art", "e1", "e2"]) s[i] = "y11";
  for (const i of ["ss11", "la12", "clc", "e3", "e4", "e5", "e6", "e7"]) s[i] = "y12";
  return s;
};
const onPlar = () => {
  const s = all(ON_CELLS, "eq");
  for (const i of ON_LOCAL) s[i] = "local";
  return s;
};
const onDone = () => {
  const s = all(ON_CELLS, "eq");
  ON_LOCAL.forEach((i, n) => (s[i] = n % 2 === 0 ? "y11" : "y12"));
  return s;
};

export const BC = {
  key: "bc",
  name: "BC주",
  diploma: "Dogwood Diploma",
  city: "밴쿠버",
  cells: BC_CELLS,
  cols: 5,
  unit: 4,
};
export const ON = {
  key: "on",
  name: "온타리오주",
  diploma: "OSSD",
  city: "토론토",
  cells: ON_CELLS,
  cols: 6,
  unit: 1,
};

// focus: "both" | "bc" | "on"
export const SCENES = [
  {
    id: "intro",
    title: "인트로 — 대표님 인사",
    act: "오프닝",
    dur: 9,
    layout: "avatar",
    side: "left",
    kicker: "AA Canada 학점 가이드",
    lines: ["한국 고1 마치고", "캐나다 졸업장까지"],
    sub: "BC주 vs 온타리오주",
    vo: "(HeyGen 영상 음성 — HEYGEN_SCRIPT.md 인트로)",
    reads: "둥근 창의 대표님 얼굴(0-9s); 제목 '한국 고1 마치고 캐나다 졸업장까지'(0.6-4s); 'BC주 vs 온타리오주'(4-9s)",
    sound: "BGM 낮게 시작, 대표님 음성 위주",
  },
  {
    id: "s01",
    title: "같은 성적표, 두 갈래",
    act: "1막 졸업 요건",
    dur: 8,
    layout: "transcript",
    headline: "고1을 마친 민준이",
    vo: "[calm] 한국에서 고1을 마친 민준이. 같은 성적표를 들고 BC로 갈 때와 온타리오로 갈 때, 졸업까지의 길은 꽤 다릅니다.",
    reads: "성적표와 '고1 수료' 도장(0.3-3s); 'BC주 · 온타리오주 Grade 11' 두 갈래(3-8s)",
    sound: "도장 '쾅', 종이 찢어지듯 둘로 갈라지는 '슥'",
  },
  {
    id: "s02",
    title: "학점 단위부터 다르다",
    act: "1막 졸업 요건",
    dur: 11,
    focus: "both",
    headline: "졸업 학점, 단위부터 다릅니다",
    state: { bc: all(BC_CELLS, "open"), on: all(ON_CELLS, "open") },
    big: { bc: "80학점", on: "30학점" },
    notes: {
      bc: [{ k: "과목당 4학점", s: "4학점 블록 20칸" }],
      on: [{ k: "과목당 1학점", s: "1학점 블록 30칸" }],
    },
    vo: "[calm] BC는 80학점, 온타리오는 30학점이 필요합니다. 숫자 차이가 커 보이지만, BC는 한 과목이 4학점, 온타리오는 1학점이라 단위가 다를 뿐이에요.",
    reads: "'80학점' 블록 틀(0.5-4s); '30학점' 블록 틀(4-7s); '과목당 4학점 / 1학점'(7-11s)",
    sound: "빈 칸이 그려질 때 가벼운 '틱' 연속",
  },
  {
    id: "s03",
    title: "BC 도그우드 디플로마",
    act: "1막 졸업 요건",
    dur: 13,
    focus: "bc",
    headline: "BC 졸업장: 필수 52 + 선택 28",
    state: { bc: base(BC_CELLS), on: all(ON_CELLS, "open") },
    notes: {
      bc: [
        { k: "필수 52 + 선택 28 = 80학점", s: "학점은 Grade 10~12 과정에서만" },
        { k: "12학년 과목 16학점 이상", s: "Language Arts 12 · CLC 포함" },
        { k: "원주민 관련 과목 4학점", s: "최근 신설된 필수 요건", tone: "red" },
      ],
    },
    vo: "[calm] BC 졸업장, 도그우드 디플로마는 10학년부터 12학년까지 필수 52학점과 선택 28학점을 채워야 합니다. 이 중 16학점 이상은 12학년 과목이어야 하고, 원주민 관련 과목 4학점도 필수예요.",
    reads: "필수 13칸이 초록으로(0.5-4s); '12학년 16학점 이상'(4-8s); '원주민 관련 4학점'(8-13s)",
    sound: "블록 착지마다 '톡'",
  },
  {
    id: "s04",
    title: "BC 졸업 평가 3개",
    act: "1막 졸업 요건",
    dur: 11,
    focus: "bc",
    headline: "BC 졸업 평가 3개",
    state: { bc: base(BC_CELLS), on: all(ON_CELLS, "open") },
    dimGrid: "bc",
    exams: [
      { k: "Numeracy 10", s: "11학년 편입생도 응시", st: "must" },
      { k: "Literacy 10", s: "11·12학년 편입생은 면제 신청 가능", st: "waive" },
      { k: "Literacy 12", s: "12학년에 응시", st: "must" },
    ],
    vo: "[calm] 여기에 졸업 평가가 세 개 있습니다. 11학년이나 12학년으로 편입하면 리터러시 10은 면제를 신청할 수 있지만, 뉴머러시 10과 리터러시 12는 반드시 치러야 해요.",
    reads: "평가 3개 이름(0.5-4s); 'Literacy 10 면제 신청 가능'(4-8s); 나머지 둘 '필수'(8-11s)",
    sound: "평가 카드가 놓일 때 '탁' 3번",
  },
  {
    id: "s05",
    title: "온타리오 OSSD",
    act: "1막 졸업 요건",
    dur: 12,
    focus: "on",
    headline: "온타리오 졸업장: 30학점",
    state: { bc: all(BC_CELLS, "open"), on: base(ON_CELLS) },
    notes: {
      on: [
        { k: "필수 17 + 선택 13", s: "2024년 이후 9학년 입학생 기준" },
        { k: "2023년 이전 입학생", s: "필수 18 + 선택 12" },
        { k: "영어는 학년마다 1과목", s: "영어 4 · 수학 3 · 과학 2 …" },
      ],
    },
    vo: "[calm] 온타리오 졸업장, OSSD는 30학점입니다. 2024년 이후 9학년 입학생 기준으로 필수 17학점, 선택 13학점이고, 영어는 학년마다 한 과목씩 모두 네 과목을 들어야 해요.",
    reads: "필수 17칸이 파랑으로(0.5-4s); '필수 17 + 선택 13'(4-8s); '영어는 학년마다 1과목'(8-12s)",
    sound: "블록 착지마다 '톡'",
  },
  {
    id: "s06",
    title: "학점 말고도 필요한 것",
    act: "1막 졸업 요건",
    dur: 9,
    focus: "on",
    headline: "온타리오: 학점 말고도 필요한 것",
    state: { bc: all(BC_CELLS, "open"), on: base(ON_CELLS) },
    dimGrid: "on",
    exams: [
      { k: "OSSLT 문해력 시험", s: "불합격 시 OLC4O 과목으로 대체", st: "must" },
      { k: "봉사활동 40시간", s: "졸업 전까지 누적", st: "must" },
      { k: "온라인 학점 2개", s: "학부모가 면제 신청 가능", st: "waive" },
    ],
    vo: "[calm] 그리고 학점과 별도로 문해력 시험 OSSLT, 봉사활동 40시간, 온라인 학점 두 개가 있습니다.",
    reads: "'OSSLT'(0.5-3s); '봉사 40시간'(3-6s); '온라인 학점 2개'(6-9s)",
    sound: "항목마다 '탁'",
  },
  {
    id: "s07",
    title: "BC: 한국 고1 학점 인정",
    act: "2막 한국 학점 인정",
    dur: 12,
    focus: "bc",
    headline: "BC: 한국 고1 학점 인정",
    state: { bc: bcEq(), on: all(ON_CELLS, "open") },
    notes: {
      bc: [
        { k: "Equivalency 인정", s: "학습성과가 약 80% 일치하는 과목" },
        { k: "번역 공증 성적표 제출", s: "한국 성적표 → 영문 번역 공증본" },
        { k: "인정 범위는 학교 심사", s: "칸 표시는 예시", tone: "red" },
      ],
    },
    vo: "[calm] 이제 민준이의 고1 성적표를 볼까요. BC에서는 BC 밖에서 들은 과목 중 학습 내용이 약 80% 일치하는 과목만 이퀴벌런시로 인정됩니다. 성적표는 번역 공증본으로 내야 해요.",
    reads: "성적표 블록이 10학년 칸으로 떨어짐(0.5-4s); '약 80% 일치'(4-8s); '번역 공증'(8-12s)",
    sound: "인정 블록 착지 '톡', 도장 '쾅'",
  },
  {
    id: "s08",
    title: "유학생 졸업학점 정책",
    act: "2막 한국 학점 인정",
    dur: 12,
    focus: "bc",
    headline: "BC 유학생 정책: 이 7과목은 현지 수강",
    state: { bc: bcLock(), on: all(ON_CELLS, "open") },
    notes: {
      bc: [
        { k: "입국 전 2년간 영어·불어로 교육받지 않은 학생", s: "International Student Graduation Credit Policy" },
        { k: "BC 교사에게 직접 수강", s: "인정·Challenge로 대체 불가", tone: "red" },
        { k: "LA 12 자리", s: "English Studies 12 또는 EFP 12 · CLC는 학교 감독" },
      ],
    },
    vo: "[calm] 하지만 유학생에게는 제한이 있습니다. 입국 전 2년 동안 영어나 불어로 공부하지 않았다면, 이 일곱 과목은 인정이나 챌린지 없이 BC 교사에게 직접 들어야 해요.",
    reads: "자물쇠 7개가 잠김(0.5-4s); '입국 전 2년'(4-8s); '직접 수강, 대체 불가'(8-12s)",
    sound: "자물쇠 '철컥' 7번, 빠르게",
  },
  {
    id: "s09",
    title: "온타리오: PLAR 학점 인정",
    act: "2막 한국 학점 인정",
    dur: 13,
    focus: "on",
    headline: "온타리오: 교장이 정하는 PLAR 인정",
    state: { bc: bcLock(), on: onPlar() },
    notes: {
      on: [
        { k: "교장이 이전 학습을 평가", s: "인정 학점과 남은 필수과목을 결정" },
        { k: "2년 이수 → 온타리오에서 최소 14학점", s: "그중 영어 2 · 수학 1 · 과학 0" },
        { k: "고1 수료를 몇 년 이수로 볼지", s: "학교별 확인 필요", tone: "red" },
      ],
    },
    vo: "[calm] 온타리오는 교장이 이전 학습을 평가해 인정 학점과 남은 필수과목을 정합니다. 정부 전학생 기준표에서 2년을 이수한 학생은 온타리오에서 최소 14학점을 따면 되고, 여기에 영어 두 과목, 수학 한 과목이 들어갑니다.",
    reads: "인정 블록이 넓게 채워짐(0.5-4s); '최소 14학점'(4-9s); '영어 2 · 수학 1'(9-13s)",
    sound: "블록이 한꺼번에 '촤르륵' 채워짐",
  },
  {
    id: "s10",
    title: "2년 이수 편입생 기준",
    act: "2막 한국 학점 인정",
    dur: 9,
    focus: "on",
    headline: "2년 이수 편입생 기준",
    state: { bc: bcLock(), on: onPlar() },
    dimGrid: "on",
    exams: [
      { k: "문해력 요건(OSSLT)", s: "편입생도 그대로 적용", st: "must" },
      { k: "금융문해 요건", s: "2년 이수 편입생", st: "free" },
      { k: "봉사 40시간", s: "시간 조정은 교장 재량", st: "waive" },
      { k: "온라인 학점", s: "인정 여부는 교장 판단", st: "waive" },
    ],
    vo: "[calm] 문해력 요건은 그대로 필요하지만, 금융문해 요건은 면제입니다. 봉사시간과 온라인 학점은 교장이 판단해요.",
    reads: "'OSSLT 필수'(0.5-3s); '금융문해 면제'(3-5.5s); '교장 재량/판단'(5.5-9s)",
    sound: "체크 '틱'",
  },
  {
    id: "s11",
    title: "BC: 2년 동안 현지에서",
    act: "3막 캐나다 학점 취득",
    dur: 13,
    focus: "bc",
    headline: "BC: 11·12학년, 보통 2년",
    state: { bc: bcDone(), on: onPlar() },
    notes: {
      bc: [
        { k: "핵심 과목은 11·12학년에 현지 이수", s: "자물쇠 과목 → 11학년 · 12학년 블록" },
        { k: "Numeracy 10 · Literacy 12 응시", s: "Literacy 10은 면제 신청 가능" },
        { k: "12학년 바로 입학은 어렵다", s: "BC 정부가 직접 명시", tone: "red" },
      ],
    },
    vo: "[calm] BC의 민준이는 11학년과 12학년 2년 동안 핵심 과목을 현지에서 채우고, 졸업 평가도 치러야 합니다. 12학년으로 바로 들어가면 졸업 요건을 맞추기 어렵다고 BC 정부도 안내하고 있어요.",
    reads: "11학년 블록 채움(0.5-5s); 12학년 블록 채움(5-9s); '12학년 바로 입학은 어렵다'(9-13s)",
    sound: "블록 '톡톡' 리듬, 마지막 칸 채울 때 '띵'",
  },
  {
    id: "s12",
    title: "온타리오: 남은 14학점",
    act: "3막 캐나다 학점 취득",
    dur: 10,
    focus: "on",
    headline: "온타리오: 최소 14학점을 2년에",
    state: { bc: bcDone(), on: onDone() },
    notes: {
      on: [
        { k: "11학년 · 12학년에 나눠 이수", s: "영어 11 · 영어 12 · 수학 11/12 포함" },
        { k: "관리 포인트", s: "OSSLT 시험 · 봉사활동 시간", tone: "red" },
      ],
    },
    vo: "[calm] 온타리오의 민준이는 남은 14학점 이상을 2년에 나눠 채웁니다. 이때 관리 포인트는 OSSLT 시험과 봉사활동 시간이에요.",
    reads: "14칸이 11·12학년으로 채워짐(0.5-5s); '관리 포인트: OSSLT · 봉사'(5-10s)",
    sound: "블록 '톡톡', 마지막에 '띵'",
  },
  {
    id: "s13",
    title: "한눈에 비교",
    act: "정리",
    dur: 11,
    focus: "both",
    headline: "한눈에 비교",
    state: { bc: bcDone(), on: onDone() },
    small: true,
    notes: {
      bc: [
        { k: "인정 범위가 좁다" },
        { k: "11·12학년 핵심 과목은 현지 수강" },
        { k: "졸업 평가 + 보통 2년" },
      ],
      on: [
        { k: "교장 재량, 인정 폭이 넓다" },
        { k: "최소 14학점을 2년 안에" },
        { k: "OSSLT · 봉사시간 관리가 핵심" },
      ],
    },
    vo: "[calm] 정리하면, BC는 인정 범위가 좁아 핵심 과목을 현지에서 들어야 하고, 온타리오는 인정 폭이 넓어 남은 학점을 채우는 구조입니다.",
    reads: "BC 세 줄(0.5-5s); 온타리오 세 줄(5-11s)",
    sound: "BGM 한 단계 올라감",
  },
  {
    id: "s14",
    title: "주의 문구",
    act: "정리",
    dur: 6,
    layout: "caution",
    vo: "[calm] 단, 최종 인정 학점은 학교와 교육청의 평가에 따라 달라집니다.",
    reads: "주의 문구(0.5-6s)",
    sound: "BGM 잠시 낮춤",
  },
  {
    id: "outro",
    title: "아웃트로 — 상담 안내",
    act: "클로징",
    dur: 9,
    layout: "avatar",
    side: "right",
    kicker: "1:1 학점 상담",
    lines: ["우리 아이 성적표로는", "어느 주가 유리할까?"],
    sub: "AA Canada",
    vo: "(HeyGen 영상 음성 — HEYGEN_SCRIPT.md 아웃트로)",
    reads: "대표님 얼굴(0-9s); 질문 두 줄(0.6-5s); 'AA Canada' 마크(5-9s)",
    sound: "BGM 마무리",
  },
];

let t = 0;
for (const s of SCENES) {
  s.start = t;
  t += s.dur;
}
export const TOTAL = t;
