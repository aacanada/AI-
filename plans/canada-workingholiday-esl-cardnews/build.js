const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = process.argv[2];
const FONT = path.join(__dirname, 'node_modules/pretendard/dist/web/static/woff2');
const NOTE = '2026년 11월 기준 · 공식 발표에 따라 변경될 수 있습니다';

const themes = {
  A: { bg: '#FBF5EC', ink: '#1C1A1A', sub: '#6B625A', accent: '#D5261D', onAccent: '#FFFFFF', card: '#FFFFFF', line: '#EADFD0', coverBg: '#D5261D', coverInk: '#FFFFFF', coverSub: '#FFD9D4', coverMark: '#FFE14D' },
  B: { bg: '#0F1830', ink: '#FFFFFF', sub: '#A9B4CF', accent: '#FFD23F', onAccent: '#0F1830', card: '#1A2648', line: '#2A3860', coverBg: '#0F1830', coverInk: '#FFFFFF', coverSub: '#A9B4CF', coverMark: '#FFD23F' },
  C: { bg: '#F2F6EF', ink: '#10382B', sub: '#5C7268', accent: '#0E6B4F', onAccent: '#FFFFFF', card: '#FFFFFF', line: '#D9E5DC', coverBg: '#0E6B4F', coverInk: '#FFFFFF', coverSub: '#CDE7DB', coverMark: '#FFD86B' },
};

const cta = (title) => ({
  type: 'cta', title,
  points: ['내 조건에 맞춘 어학 플랜 상세 안내', '등록 시 최고 혜택 제공', '상담은 무료, 부담 없이 문의하세요'],
  button: '무료 상담 신청하기',
});

const sets = {
  A: [
    { type: 'cover', kw: '2027 캐나다<br>워킹홀리데이', hook: '인비 기다리는 동안<br>지금 해둘 3가지', sub: '준비한 사람이 먼저 출발합니다' },
    { type: 'list', kicker: '2027 시즌 현황', title: '지금까지 확인된 것', items: [
      ['신청 연령', '만 18세 ~ 35세'],
      ['풀(Pool) 오픈일', '미발표 · 추후 공지'],
      ['2027 한국 쿼터', '미발표 · 추후 공지'],
    ], note: NOTE },
    { type: 'list', kicker: '준비 하나', title: '워홀 비자로도<br>어학연수가 됩니다', items: [
      ['최대 6개월', '학생비자 없이 어학연수 가능'],
      ['일과 병행', '공부하면서 일할 수 있는 비자'],
      ['먼저 영어부터', '초반 어학연수가 구직의 출발점'],
    ] },
    { type: 'list', kicker: '준비 둘', title: '어학 플랜은<br>출국 전에 정하세요', items: [
      ['내 영어 레벨', '레벨에 따라 필요한 기간이 다릅니다'],
      ['도시와 어학원', '목표 직종에 맞는 곳을 고릅니다'],
      ['시작 시기', '인기 시작일과 숙소는 일찍 마감'],
    ] },
    { type: 'list', kicker: '준비 셋', title: '초기 정착을<br>미리 그려두세요', items: [
      ['숙소', '첫 달 머물 곳을 먼저 확보'],
      ['초기 자금', '첫 석 달 예산을 항목별로 계산'],
      ['영문 이력서', '도착하자마자 지원할 수 있게'],
    ] },
    cta('2027 워홀 어학 플랜,<br>디테일하게 알려드립니다'),
  ],
  B: [
    { type: 'cover', kw: '캐나다<br>워킹홀리데이', hook: '한인잡만 하다<br>오는 이유', sub: '차이는 첫 석 달에 만들어집니다' },
    { type: 'list', kicker: '현실', title: '현지 일자리는<br>영어에서 갈립니다', items: [
      ['영문 이력서', '캐나다 방식은 형식부터 다릅니다'],
      ['인터뷰', '짧은 대화로 채용이 결정됩니다'],
      ['현장 소통', '손님, 동료와 바로 영어로 일합니다'],
    ] },
    { type: 'list', kicker: '해법', title: '첫 8~12주,<br>어학연수로 시작하세요', items: [
      ['영어 적응', '실전 영어에 익숙해지는 시간'],
      ['구직 준비', '공부하면서 일자리를 알아봅니다'],
      ['현지 인맥', '다국적 친구와 정보가 생깁니다'],
    ], note: '워홀 비자로 최대 6개월까지 어학연수가 가능합니다' },
    { type: 'list', kicker: '준비 내용', title: '어학원에서<br>이런 걸 준비합니다', items: [
      ['이력서 작성', '캐나다식 레쥬메와 커버레터'],
      ['모의 인터뷰', '자주 나오는 질문으로 연습'],
      ['실무 영어', '카페, 레스토랑, 오피스 표현'],
    ], note: '세부 내용은 어학원과 과정에 따라 다릅니다' },
    { type: 'list', kicker: '맞춤 플랜', title: '목표에 따라<br>플랜이 달라집니다', items: [
      ['영어 초급', '일반 영어 집중 과정부터'],
      ['카페 · 레스토랑', '서비스 실무 영어 과정'],
      ['사무직', '비즈니스 영어 과정'],
    ] },
    cta('내 영어 수준에 맞는<br>어학 플랜을 알려드립니다'),
  ],
  C: [
    { type: 'cover', kw: '캐나다<br>워킹홀리데이', hook: '첫 3개월,<br>얼마나 들까?', sub: '출국 전에 꼭 계산해 볼 항목들' },
    { type: 'list', kicker: '비용 항목', title: '초기 비용은<br>네 가지로 나뉩니다', items: [
      ['어학연수', '학비, 등록비, 교재비'],
      ['숙소', '홈스테이, 기숙사, 룸렌트'],
      ['생활비', '식비, 교통비, 통신비'],
      ['출국 준비', '항공권, 보험, 비자 비용'],
    ] },
    { type: 'list', kicker: '견적의 차이', title: '같은 12주인데<br>금액이 다른 이유', items: [
      ['도시', '도시마다 학비와 렌트가 다릅니다'],
      ['수업 시간', '주당 수업 수에 따라 달라집니다'],
      ['숙소 형태', '홈스테이와 룸렌트의 차이'],
      ['등록 시기', '시기별 혜택이 적용됩니다'],
    ] },
    { type: 'list', kicker: '도시 선택', title: '어느 도시에서<br>시작할까요?', items: [
      ['밴쿠버', '온화한 날씨, 서비스직 일자리'],
      ['토론토', '캐나다 최대 도시, 다양한 직종'],
      ['몬트리올', '영어 어학원 선택 가능, 낮은 렌트 부담'],
    ] },
    { type: 'list', kicker: '1:1 맞춤 견적', title: '세 가지만<br>알려주세요', items: [
      ['희망 도시', '아직 못 정했어도 괜찮습니다'],
      ['연수 기간', '8주, 12주, 그 이상'],
      ['출국 시기', '시기에 맞는 혜택을 찾아드립니다'],
    ] },
    cta('내 조건으로<br>어학연수 견적 받아보기'),
  ],
};

const css = (t) => `
@font-face{font-family:P;font-weight:500;src:url('file://${FONT}/Pretendard-Medium.woff2')}
@font-face{font-family:P;font-weight:700;src:url('file://${FONT}/Pretendard-Bold.woff2')}
@font-face{font-family:P;font-weight:900;src:url('file://${FONT}/Pretendard-Black.woff2')}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;font-family:P;font-weight:500;background:${t.bg};color:${t.ink};overflow:hidden;word-break:keep-all;letter-spacing:-0.02em}
.wrap{position:relative;width:1080px;height:1350px;padding:96px 84px 150px;display:flex;flex-direction:column}
.foot{position:absolute;left:84px;right:84px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:700;color:${t.sub}}
.dots{display:flex;gap:10px}.dots i{width:12px;height:12px;border-radius:50%;background:${t.line}}.dots i.on{width:36px;border-radius:6px;background:${t.accent}}
.kicker{display:inline-block;align-self:flex-start;font-size:32px;font-weight:700;color:${t.onAccent};background:${t.accent};padding:12px 26px;border-radius:999px}
h2{font-size:84px;font-weight:900;line-height:1.2;margin-top:36px;letter-spacing:-0.035em}
.items{margin-top:auto;display:flex;flex-direction:column;gap:22px}
.item{background:${t.card};border:2px solid ${t.line};border-radius:28px;padding:42px 44px}
.item b{display:block;font-size:52px;font-weight:900;color:${t.accent === '#FFD23F' ? t.accent : t.ink}}
.item span{display:block;font-size:38px;color:${t.sub};margin-top:8px}
.items.n4 .item{padding:26px 40px}.items.n4 .item b{font-size:42px}.items.n4 .item span{font-size:33px}
.note{margin-top:26px;font-size:27px;color:${t.sub}}
.cover{background:${t.coverBg};color:${t.coverInk}}
.cover .tag{align-self:flex-start;font-size:34px;font-weight:700;border:3px solid ${t.coverInk};padding:14px 30px;border-radius:999px}
.cover .kw{font-size:152px;font-weight:900;line-height:1.1;letter-spacing:-0.05em;color:${t.coverMark};margin-top:40px}.cover .bar{width:120px;height:12px;border-radius:6px;background:${t.coverInk};margin-top:56px}.cover h1{font-size:92px;font-weight:900;line-height:1.2;letter-spacing:-0.04em;margin-top:auto}
.cover h1 m{color:${t.coverMark}}
.cover .sub{font-size:44px;font-weight:700;color:${t.coverSub};margin-top:40px;margin-bottom:60px}
.cover .foot{color:${t.coverSub}}
.cover .ring{position:absolute;right:-180px;top:-180px;width:620px;height:620px;border-radius:50%;border:90px solid rgba(255,255,255,.08)}
.cta h2{margin-top:0;font-size:88px}
.pts{margin-top:64px;display:flex;flex-direction:column;gap:30px}
.pt{display:flex;align-items:center;gap:26px;font-size:44px;font-weight:700}
.pt i{flex:none;width:56px;height:56px;border-radius:50%;background:${t.accent};position:relative}
.pt i:after{content:'';position:absolute;left:19px;top:12px;width:14px;height:26px;border:solid ${t.onAccent};border-width:0 6px 6px 0;transform:rotate(45deg)}
.btn{margin-top:auto;background:${t.accent};color:${t.onAccent};font-size:56px;font-weight:900;text-align:center;padding:44px;border-radius:32px}
.hint{text-align:center;font-size:32px;color:${t.sub};margin-top:26px}
`;

function html(key, card, idx, total) {
  const t = themes[key];
  const dots = `<div class="dots">${Array.from({ length: total }, (_, i) => `<i class="${i === idx ? 'on' : ''}"></i>`).join('')}</div>`;
  let body;
  if (card.type === 'cover') {
    body = `<div class="wrap cover"><div class="ring"></div><div class="kw">${card.kw}</div><div class="bar"></div>
      <h1>${card.hook}</h1><div class="sub">${card.sub}</div>
      <div class="foot"><span>옆으로 넘겨보세요 →</span>${dots}</div></div>`;
  } else if (card.type === 'list') {
    body = `<div class="wrap"><div class="kicker">${card.kicker}</div><h2>${card.title}</h2>
      <div class="items n${card.items.length}">${card.items.map(([b, s]) => `<div class="item"><b>${b}</b><span>${s}</span></div>`).join('')}</div>
      ${card.note ? `<div class="note">${card.note}</div>` : ''}
      <div class="foot"><span>캐나다 워홀 어학연수</span>${dots}</div></div>`;
  } else {
    body = `<div class="wrap cta"><h2>${card.title}</h2>
      <div class="pts">${card.points.map((p) => `<div class="pt"><i></i>${p}</div>`).join('')}</div>
      <div class="btn">${card.button}</div><div class="hint">아래 버튼을 눌러 간단히 신청하세요</div>
      <div class="foot"><span>캐나다 워홀 어학연수</span>${dots}</div></div>`;
  }
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>${css(t)}</style></head><body>${body}</body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const [key, cards] of Object.entries(sets)) {
    const dir = path.join(OUT, `set-${key}`);
    fs.mkdirSync(dir, { recursive: true });
    for (let i = 0; i < cards.length; i++) {
      fs.writeFileSync(path.join(__dirname,'card.html'), html(key, cards[i], i, cards.length)); await page.goto('file://'+path.join(__dirname,'card.html'));
      await page.evaluate(() => document.fonts.ready);
      const over = await page.evaluate(() => {
        const w = document.querySelector('.wrap'); const f = document.querySelector('.foot').getBoundingClientRect();
        return [...w.children].filter((c) => !c.classList.contains('foot') && !c.classList.contains('ring')).some((c) => c.getBoundingClientRect().bottom > f.top - 10 || c.scrollWidth > 920);
      });
      if (over) console.log('OVERFLOW', key, i + 1);
      await page.screenshot({ path: path.join(dir, `${key}-${i + 1}.png`) });
    }
  }
  // contact sheet
  const imgs = Object.keys(sets).map((k) => `<div style="display:flex;gap:8px;margin-bottom:8px">${sets[k].map((_, i) => `<img src="file://${OUT}/set-${k}/${k}-${i + 1}.png" width="360">`).join('')}</div>`).join('');
  await page.setViewportSize({ width: 2210, height: 1380 });
  fs.writeFileSync(path.join(__dirname,'sheet.html'), `<body style="margin:8px;background:#888">${imgs}</body>`); await page.goto('file://'+path.join(__dirname,'sheet.html'));
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: path.join(__dirname, 'sheet.png'), fullPage: true });
  await browser.close();
})();
