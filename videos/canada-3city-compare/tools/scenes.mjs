// Scene data. Every data-at is an absolute narration time (s) taken from
// assets/audio/narration-asr.json segment starts.

const STARTS = [
  ["s01-opening", 0], ["s02-montreal-too", 41.85], ["s03-edu-pisa", 85.27], ["s04-edu-pcap", 135.03],
  ["s05-edu-grades", 174.39], ["s06-rent", 213.14], ["s07-tuition-kids", 270.42], ["s08-parent-tor-van", 340.18],
  ["s09-parent-mtl", 415.51], ["s10-culture-van", 477.75], ["s11-culture-tor", 551.9], ["s12-culture-mtl", 644.95],
  ["s13-pop-van", 751.58], ["s14-pop-tor", 798.46], ["s15-pop-mtl", 839.0], ["s16-pop-india", 877.46],
  ["s17-pop-korean", 906.68], ["s18-weather", 984.6], ["s19-car", 1030.17], ["s20-language", 1062.52],
  ["s21-wrap", 1130.33], ["s22-contact", 1157.72],
];
const END = 1196.35;

// ---------- helpers ----------
const at = (t, fx = "up") => `data-at="${t}" data-fx="${fx}"`;
const mk = (txt, t) => `<span class="mk" ${at(t, "mark")}><span class="mkb"></span><span class="mkt">${txt}</span></span>`;
const chap = (n, title, sub, t) =>
  `<div class="chap" ${at(t, "left")}><div class="n">${n}</div><h2>${title}</h2>${sub ? `<div class="sub">${sub}</div>` : ""}</div>`;
const CITY = { van: ["밴쿠버", "브리티시컬럼비아 · BC"], tor: ["토론토", "온타리오 · ON"], mtl: ["몬트리올", "퀘벡 · QC"] };
const pill = (c, t, fx = "left") => `<div class="pill ${c}" ${t != null ? at(t, fx) : ""}>${CITY[c][0]}</div>`;
const count = (to, t, { pre = "", suf = "", dec = 0, comma = true, cls = "big" } = {}) =>
  `<span class="${cls}" ${at(t, "count")} data-to="${to}" data-pre="${pre}" data-suf="${suf}" data-dec="${dec}" ${comma ? "data-comma" : ""}>${pre}0${suf}</span>`;

const CRITERIA = [
  ["1", "교육환경"], ["2", "거주비"], ["3", "학비 (조기유학)"], ["4", "부모 학비 (무상교육)"],
  ["5", "문화적 환경"], ["6", "인구 구성"], ["7", "날씨"], ["8", "자동차"], ["+", "자녀 언어향상"],
];
const critGrid = (t0, step) =>
  `<div class="crit">${CRITERIA.map(
    ([n, name], i) => `<div class="ct" ${at((t0 + i * step).toFixed(2), "pop")}><span class="ctn">${n}</span><span class="ctt">${name}</span></div>`,
  ).join("")}</div>`;
const critCss = `
#S .crit{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;}
#S .ct{display:flex;align-items:center;gap:26px;height:150px;padding:0 36px;background:#FBF9F4;border:3px solid var(--rule);border-radius:22px;}
#S .ctn{width:76px;height:76px;flex:none;border-radius:50%;background:var(--ink);color:var(--paper);font-size:40px;font-weight:900;display:flex;align-items:center;justify-content:center;}
#S .ct:last-child .ctn{background:var(--marker);color:var(--ink);}
#S .ctt{font-size:42px;font-weight:800;}`;

const cityCards = (times, extra = {}) =>
  `<div class="crow">${["van", "tor", "mtl"]
    .map((c, i) =>
      times[i] == null
        ? extra.empty
          ? `<div class="card empty" ${at(extra.empty, "fade")}><div class="q">?</div></div>`
          : `<div></div>`
        : `<div class="card cityc ${c}" ${at(times[i], "pop")}><div class="bar"></div><div class="cn cc">${CITY[c][0]}</div><div class="cp">${CITY[c][1]}</div>${(extra[c] || "")}</div>`,
    )
    .join("")}</div>`;
const cityCardCss = `
#S .crow{position:absolute;left:120px;right:120px;top:560px;height:310px;display:grid;grid-template-columns:repeat(3,1fr);gap:40px;}
#S .crow .card{padding:40px 44px 0;}
#S .cn{font-size:70px;font-weight:900;letter-spacing:-.03em;line-height:1.15;}
#S .cp{font-size:30px;font-weight:600;color:var(--ink2);margin-top:8px;}
#S .card.empty{border:4px dashed var(--rule);background:transparent;display:flex;align-items:center;justify-content:center;}
#S .q{font-size:140px;font-weight:900;color:var(--rule);}`;

// list of attractions (culture scenes)
const attractions = (items, cols) =>
  `<div class="att" style="grid-template-rows:repeat(${Math.ceil(items.length / cols)},1fr)">${items
    .map(
      ([t, name, desc], i) =>
        `<div class="ai" ${at(t, "right")}><div class="ain">${i + 1}</div><div><div class="aname">${name}</div><div class="adesc">${desc}</div></div></div>`,
    )
    .join("")}</div>`;
const cultureCss = `
#S .head2{display:flex;align-items:center;gap:36px;margin-top:26px;height:80px;}
#S .head2 .pill{font-size:52px;}
#S .head2 .pill::before{width:30px;height:30px;}
#S .tl{font-size:40px;font-weight:800;}
#S .tl2{font-size:32px;font-weight:600;color:var(--ink2);}
#S .att{position:absolute;left:120px;right:120px;top:380px;bottom:180px;display:grid;grid-template-columns:1fr 1fr;grid-auto-flow:column;column-gap:60px;row-gap:14px;}
#S .ai{display:flex;align-items:center;gap:26px;border-bottom:3px solid var(--rule);}
#S .ain{width:58px;height:58px;flex:none;border-radius:50%;background:var(--c);color:#fff;font-size:30px;font-weight:900;display:flex;align-items:center;justify-content:center;}
#S .aname{font-size:38px;font-weight:800;}
#S .adesc{font-size:27px;font-weight:600;color:var(--ink2);margin-top:4px;}`;

// population ring + bars
const ring = (p, t) => `<div class="ring" ${at(t, "ring")} data-p="${p / 100}">
  <svg viewBox="0 0 400 400" width="400" height="400"><circle cx="200" cy="200" r="160" fill="none" stroke="#E2DCCB" stroke-width="44"/>
  <circle class="ringv" cx="200" cy="200" r="160" fill="none" stroke="currentColor" stroke-width="44" stroke-linecap="butt" transform="rotate(-90 200 200)"/></svg>
  <div class="rc">${count(p, t, { suf: "%", dec: 1, comma: false, cls: "big rv" })}<div class="rl">소수 민족<br/>Visible Minority</div></div></div>`;
const popBars = (rows) =>
  `<div class="pb">${rows
    .map(
      ([t, name, v, note]) =>
        `<div class="pr" ${at(t, "up")}><div class="pn">${name}</div><div class="pt"><div class="pf" ${at(t, "barx")} style="width:${(v / 30) * 100}%"></div></div><div class="pv">${v}%</div>${note ? `<div class="pnote">${note}</div>` : ""}</div>`,
    )
    .join("")}</div>`;
const popCss = `
#S .basis{font-size:32px;font-weight:700;color:var(--ink2);}
#S .ring{position:absolute;left:120px;top:340px;width:400px;height:400px;color:var(--c);}
#S .ring svg{position:absolute;inset:0;}
#S .rc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
#S .rv{font-size:96px;}
#S .rl{font-size:24px;font-weight:700;color:var(--ink2);text-align:center;line-height:1.3;margin-top:6px;}
#S .pb{position:absolute;left:640px;right:120px;top:350px;display:flex;flex-direction:column;gap:30px;}
#S .pr{display:grid;grid-template-columns:230px 1fr 150px;align-items:center;column-gap:24px;}
#S .pn{font-size:38px;font-weight:800;}
#S .pt{height:46px;background:#E8E2D2;border-radius:10px;overflow:hidden;}
#S .pf{height:100%;background:var(--c);border-radius:10px;transform-origin:left center;}
#S .pv{font-size:44px;font-weight:900;text-align:right;font-variant-numeric:tabular-nums;}
#S .pnote{grid-column:2/4;font-size:26px;font-weight:700;color:var(--c);margin-top:6px;}
#S .ptags{position:absolute;left:640px;right:120px;top:700px;display:flex;flex-wrap:wrap;gap:20px 24px;}
#S .ptags .tag{font-size:32px;}`;

// ---------- scenes ----------
const S = {};

S["s01-opening"] = {
  title: "오프닝", noExit: true,
  css: `
#S .kick{font-size:38px;font-weight:700;color:var(--ink2);}
#S h1{font-size:110px;font-weight:900;letter-spacing:-.035em;line-height:1.1;margin-top:14px;}
#S h1 .vs{color:var(--ink2);font-weight:700;font-size:72px;padding:0 14px;}
#S .subt{font-size:52px;font-weight:800;margin-top:22px;}
#S .chips{position:absolute;left:120px;top:470px;display:flex;gap:18px;}
${cityCardCss}`,
  html: `
<div class="kick" ${at(0.3)}>캐나다 자녀동반유학</div>
<h1 ${at(0.7)}><span class="cc van">밴쿠버</span><span class="vs">vs</span><span class="cc tor">토론토</span><span class="vs">vs</span><span class="cc mtl">몬트리올</span></h1>
<div class="subt" ${at(1.3)}>${mk("8가지 기준", 2.0)}으로 비교해 봤어요</div>
<div class="chips"><div class="tag lite" ${at(27.29, "pop")}>자녀 교육환경</div><div class="tag lite" ${at(31.45, "pop")}>문화적 환경</div><div class="tag lite" ${at(34.2, "pop")}>생활 편의성</div><div class="tag" ${at(37.88, "pop")}>→ 결국 대도시</div></div>
${cityCards([18.6, 21.0, null], { empty: 22.0 })}`,
};

S["s02-montreal-too"] = {
  title: "몬트리올도 함께", noEnter: true,
  css: `
#S .h{font-size:84px;font-weight:900;letter-spacing:-.03em;}
#S .h2{font-size:44px;font-weight:700;color:var(--ink2);margin-top:20px;}
#S .mtag{display:flex;flex-direction:column;align-items:flex-start;gap:10px;margin-top:18px;}
#S .strike{position:relative;font-size:28px;font-weight:700;color:var(--ink2);}
#S .strike i{position:absolute;left:-6px;right:-6px;top:50%;height:5px;background:var(--mtl);transform-origin:left center;display:block;}
#S .second{font-size:36px;font-weight:900;}
#S .crit{position:absolute;left:120px;right:120px;top:300px;}
#S .h3{position:absolute;left:120px;top:150px;font-size:72px;font-weight:900;}
${critCss}
${cityCardCss}`,
  html: `
<div data-out="70.2"><div class="h" ${at(42.3)}>여기에 <span class="cc mtl">몬트리올</span>도 함께</div>
<div class="h2" ${at(59.32)}>자녀 교육 · 문화 환경 · 생활 편의성 → 대도시의 특징 그대로</div></div>
<div data-out="70.2">${cityCards([null, null, 43.6], {
    van: "",
    mtl: `<div class="mtag"><span class="strike" ${at(47.83, "fade")}>한국에선 '중소도시' 취급?<i ${at(54.6, "barx")}></i></span><span class="second" ${at(54.87, "up")}>${mk("캐나다 2번째 대도시", 55.3)}</span></div>`,
  }).replace('<div class="crow"><div></div><div></div>', `<div class="crow"><div class="card cityc van"><div class="bar"></div><div class="cn cc">밴쿠버</div><div class="cp">${CITY.van[1]}</div></div><div class="card cityc tor"><div class="bar"></div><div class="cn cc">토론토</div><div class="cp">${CITY.tor[1]}</div></div>`)}</div>
<div class="h3" ${at(75.77)}>부모님들이 가장 많이 보시는 기준</div>
${critGrid(76.4, 0.45)}`,
};

// PISA box plot (values read from the user's chart: p10, p25, mean-lo, mean-hi, p75, p90)
const PISA = [
  ["매니토바", 362, 412, 467, 477, 531, 583], ["서스캐처원", 359, 407, 462, 473, 527, 581],
  ["뉴펀들랜드", 350, 398, 448, 466, 517, 573], ["PEI", 364, 413, 459, 487, 543, 591],
  ["뉴브런즈윅", 356, 404, 464, 474, 530, 585], ["OECD 평균", 356, 409, 472, 473, 536, 590, "oecd"],
  ["노바스코샤", 356, 403, 462, 478, 533, 590], ["온타리오", 377, 431, 489, 502, 557, 617, "tor"],
  ["BC", 378, 431, 489, 506, 561, 617, "van"], ["퀘벡", 391, 451, 506, 521, 584, 631, "mtl"],
  ["캐나다", 375, 431, 495, 501, 563, 619], ["앨버타", 377, 433, 494, 515, 572, 634],
];
const px = (v) => (((v - 340) / 300) * 100).toFixed(2) + "%";
S["s03-edu-pisa"] = {
  title: "교육 PISA", ghost: "PISA",
  css: `
#S .lc{position:absolute;left:120px;top:290px;width:560px;display:flex;flex-direction:column;gap:30px;}
#S .lt{font-size:40px;font-weight:800;line-height:1.35;}
#S .ls{font-size:30px;font-weight:600;color:var(--ink2);line-height:1.4;}
#S .tags{display:flex;gap:16px;}
#S .chart{position:absolute;left:740px;right:120px;top:270px;}
#S .row{display:grid;grid-template-columns:190px 1fr;align-items:center;height:44px;}
#S .rn{font-size:25px;font-weight:700;color:var(--ink2);}
#S .row.hl .rn{color:var(--c);font-weight:900;}
#S .row.oecd .rn{color:var(--ink);font-weight:900;}
#S .trk{position:relative;height:100%;}
#S .wh{position:absolute;top:50%;height:3px;background:#9C9480;transform-origin:left center;}
#S .bx{position:absolute;top:9px;bottom:9px;background:#BDB39C;border-radius:5px;transform-origin:left center;}
#S .row.hl .bx{background:var(--c);} #S .row.oecd .bx{background:var(--ink);}
#S .mn{position:absolute;top:5px;bottom:5px;width:6px;background:var(--marker);border-radius:3px;}
#S .ax{display:grid;grid-template-columns:190px 1fr;margin-top:10px;}
#S .axt{position:relative;height:40px;border-top:3px solid var(--ink2);}
#S .axt span{position:absolute;top:8px;font-size:22px;font-weight:700;color:var(--ink2);transform:translateX(-50%);}
#S .gl{position:absolute;top:0;bottom:50px;left:190px;right:0;}
#S .gl i{position:absolute;top:0;bottom:0;width:2px;background:rgba(28,36,49,.12);}
#S .dir{position:absolute;right:120px;top:205px;font-size:30px;font-weight:800;}
#S .callout{position:absolute;left:120px;top:760px;font-size:40px;font-weight:900;color:var(--mtl);}`,
  html: `
${chap("1", "교육환경", "학업성취도 비교", 85.6)}
<div class="lc">
  <div class="lt" ${at(87.58)}>캐나다는 주마다<br/>교육제도가 다릅니다</div>
  <div class="ls" ${at(94.26)}>그나마 객관적으로 비교할 수 있는 지표 2가지 — 주별 비교</div>
  <div class="tags"><span class="tag" ${at(96.5, "pop")}>PISA</span><span class="tag lite" ${at(97.2, "pop")}>PCAP</span></div>
  <div class="ls" ${at(110.62)}><b style="color:var(--ink)">PISA</b> — OECD가 주관하는<br/>국제 학생 평가 프로그램</div>
</div>
<div class="dir" ${at(117.14, "right")}>오른쪽으로 갈수록 ${mk("수학 점수 ↑", 117.8)}</div>
<div class="chart">
  <div class="gl">${[350, 400, 450, 500, 550, 600].map((v) => `<i style="left:${px(v)}"></i>`).join("")}</div>
  ${PISA.map(([n, p10, p25, m1, m2, p75, p90, c], i) => {
    const hl = c && c !== "oecd";
    const cls = `row ${c === "oecd" ? "oecd" : ""} ${hl ? "hl " + c : ""}`;
    const t = (110.8 + i * 0.12).toFixed(2);
    const inner = `<div class="trk"><div class="wh" ${at(t, "barx")} style="left:${px(p10)};width:calc(${px(p90)} - ${px(p10)})"></div><div class="bx" ${at(t, "barx")} style="left:${px(p25)};width:calc(${px(p75)} - ${px(p25)})"></div><div class="mn" style="left:${px((m1 + m2) / 2)}"></div></div>`;
    return `<div class="${cls}" ${at(t, "fade")}><div class="rn">${n}</div>${c ? inner : `<div class="trk" ${at(121.78, "dim")}>${inner.slice(17, -6)}</div>`}</div>`;
  }).join("")}
  <div class="ax"><div></div><div class="axt">${[350, 400, 450, 500, 550, 600].map((v) => `<span style="left:${px(v)}">${v}</span>`).join("")}</div></div>
</div>
<div class="callout" ${at(131.06, "pop")}>${mk("퀘벡이 가장 오른쪽", 131.6)}</div>
<div class="src">자료: OECD PISA 주별 수학 점수 분포 (10~90 백분위, 노란 선 = 평균)</div>`,
};

const PCAP = [["BC", 490, "van"], ["AB", 507], ["SK", 481], ["MB", 475], ["ON", 512, "tor"], ["QC", 537, "mtl"], ["NB", 493], ["NS", 498], ["PE", 497], ["NL", 480], ["캐나다", 510, "can"]];
const py = (v) => ((v - 400) / 200) * 520;
S["s04-edu-pcap"] = {
  title: "교육 PCAP", ghost: "PCAP",
  css: `
#S .lc{position:absolute;left:120px;top:290px;width:520px;display:flex;flex-direction:column;gap:28px;}
#S .lt{font-size:40px;font-weight:800;line-height:1.35;}
#S .ls{font-size:30px;font-weight:600;color:var(--ink2);line-height:1.4;}
#S .ch{position:absolute;left:720px;right:120px;top:300px;height:520px;display:flex;align-items:flex-end;gap:22px;border-bottom:3px solid var(--ink2);}
#S .b{position:relative;flex:1;height:100%;}
#S .bf{position:absolute;left:0;right:0;bottom:0;background:#D8D0BC;border-radius:8px 8px 0 0;transform-origin:bottom center;}
#S .b.van .bf,#S .b.tor .bf,#S .b.mtl .bf{background:var(--c);} #S .b.can .bf{background:var(--ink);}
#S .bv{position:absolute;left:-10px;right:-10px;text-align:center;font-size:28px;font-weight:900;font-variant-numeric:tabular-nums;}
#S .bn{position:absolute;left:-14px;right:-14px;bottom:-48px;text-align:center;font-size:26px;font-weight:800;color:var(--ink2);}
#S .avg{position:absolute;left:720px;right:120px;height:0;border-top:4px dashed var(--ink);}
#S .avg span{position:absolute;left:0;top:-48px;font-size:26px;font-weight:800;background:var(--paper);padding:0 8px;}
#S .callout{position:absolute;left:120px;top:690px;font-size:46px;font-weight:900;}`,
  html: `
${chap("1", "교육환경", "PCAP", 135.3)}
<div class="lc">
  <div class="lt" ${at(135.6)}>PCAP — 캐나다 전국<br/>학업성취도 평가</div>
  <div class="ls" ${at(138.17)}>캐나다 교육부 장관 협의회(CMEC)가 만든 평가</div>
  <div class="ls" ${at(146.42)}>주별 수학 점수</div>
</div>
<div class="ch">${PCAP.map(([n, v, c], i) => {
    const t = (146.6 + i * 0.1).toFixed(2), h = py(v), bt = c && c !== "can" ? { BC: 148.34, ON: 150.6, QC: 152.92 }[n] : t;
    return `<div class="b ${c || ""}"><div class="bf" ${at(t, "bary")} style="height:${h}px"></div><div class="bv" style="bottom:${h + 8}px" ${at(bt, "pop")}>${c ? mk(v, bt) : v}</div><div class="bn">${n}</div></div>`;
  }).join("")}</div>
<div class="avg" style="top:${300 + 520 - py(510)}px" ${at(156.31, "fade")}><span>캐나다 평균 510</span></div>
<div class="callout" ${at(160.12, "up")}><span class="cc mtl" style="--c:var(--mtl)">퀘벡</span>, 꽤 높은 편</div>
<div class="src" ${at(163.9, "fade")}>※ 학업성취도가 절대적인 기준은 아닙니다 · 자료: CMEC PCAP</div>`,
};

S["s05-edu-grades"] = {
  title: "학년별 경향",
  css: `
#S .lead{font-size:36px;font-weight:700;color:var(--ink2);margin-top:24px;}
#S .cols{position:absolute;left:120px;right:120px;top:330px;height:540px;display:grid;grid-template-columns:repeat(3,1fr);gap:40px;}
#S .card{padding:60px 40px 0;display:flex;flex-direction:column;gap:26px;}
#S .card .pill{font-size:52px;}
#S .k{font-size:44px;font-weight:900;line-height:1.3;}
#S .s{font-size:32px;font-weight:700;color:var(--ink2);line-height:1.4;}
#S .row{display:flex;align-items:center;gap:16px;font-size:34px;font-weight:800;}
#S .row b{display:inline-block;padding:6px 16px;border-radius:10px;background:var(--ink);color:var(--paper);font-size:28px;}`,
  html: `
${chap("1", "교육환경", "학년별로 많이 가는 도시", 174.6)}
<div class="lead" ${at(174.9)}>유학업계에서 실제로 보면</div>
<div class="cols">
  <div class="card cityc van" ${at(177.2, "pop")}><div class="bar"></div>${pill("van")}<div class="k">${mk("초등학생", 178.3)}<br/>비율이 높은 편</div></div>
  <div class="card cityc tor" ${at(180.66, "pop")}><div class="bar"></div>${pill("tor")}<div class="k">${mk("중학생 이상", 182.2)}<br/>학년이 높을수록</div></div>
  <div class="card cityc mtl" ${at(186.55, "pop")}><div class="bar"></div>${pill("mtl")}<div class="s">숫자는 적지만</div>
    <div class="k" ${at(193.43)}>영어+불어 둘 다 →<br/>${mk("저학년이 유리", 195.5)}</div>
    <div class="row" ${at(200.89)}><b>단기</b>영어에 집중</div>
    <div class="row" ${at(204.86)}><b>장기</b>영어 + 불어</div></div>
</div>`,
};

const RENT = [
  ["1", "밴쿠버, BC", "$2,500", "-7.4%", "van"], ["2", "버나비, BC", "$2,380", "-4.8%"], ["3", "토론토, ON", "$2,220", "-11.9%", "tor"],
  ["4", "핼리팩스, NS", "$2,100", "+1.0%", "mid"], ["5", "빅토리아, BC", "$2,020", "-6.5%"], ["6", "오타와, ON", "$1,980", "-1.0%", "mid"],
  ["7", "켈로나, BC", "$1,890", "-4.1%"], ["8", "오샤와, ON", "$1,790", "-6.8%"], ["9", "배리, ON", "$1,760", "-8.8%"],
  ["10", "킹스턴, ON", "$1,750", "+0.6%", "mid"], ["10", "키치너, ON", "$1,750", "-9.3%", "mid"], ["12", "몬트리올, QC", "$1,710", "-2.3%", "mtl"],
  ["13", "해밀턴, ON", "$1,700", "0.0%"], ["14", "캘거리, AB", "$1,670", "-9.2%"], ["15", "런던, ON", "$1,650", "-2.4%"],
];
S["s06-rent"] = {
  title: "거주비", ghost: "RENT",
  css: `
#S .lc{position:absolute;left:120px;top:290px;width:560px;display:flex;flex-direction:column;gap:30px;}
#S .lt{font-size:40px;font-weight:800;line-height:1.35;}
#S .ls{font-size:30px;font-weight:600;color:var(--ink2);line-height:1.4;}
#S .tb{position:absolute;left:760px;right:120px;top:262px;}
#S .tr{position:relative;display:grid;grid-template-columns:80px 1fr 200px 170px;align-items:center;height:38px;font-size:25px;font-weight:600;padding:0 18px;}
#S .tr.th{height:44px;font-size:22px;font-weight:800;color:var(--ink2);border-bottom:3px solid var(--ink2);}
#S .tr span{position:relative;z-index:1;font-variant-numeric:tabular-nums;}
#S .tr span.r{text-align:right;}
#S .hl{position:absolute;inset:2px 0;border-radius:8px;background:var(--c);opacity:.2;transform-origin:left center;}
#S .tr.van,#S .tr.tor,#S .tr.mtl{font-weight:900;font-size:27px;}
#S .tr.van span,#S .tr.tor span,#S .tr.mtl span{color:var(--c);}
#S .mid .hl{background:#B9B09A;}
#S .yy{position:absolute;right:0;top:0;width:190px;height:${44 + 15 * 38}px;border:4px solid var(--marker);border-radius:12px;}
#S .big2{font-size:42px;font-weight:900;line-height:1.3;}`,
  html: `
${chap("2", "거주비", "1베드룸 월 렌트비 (CAD)", 213.4)}
<div class="lc">
  <div class="lt" ${at(215.58)}>도시 선택의 핵심 = ${mk("예산", 217)}<br/>그래서 렌트비가 중요해요</div>
  <div class="ls" ${at(223.58)}>대도시니까 렌트비가 비싼 건 어느 정도 감안해야 합니다</div>
  <div class="big2" ${at(255.38)}>몬트리올은 대도시인데<br/>${mk("렌트비는 중소도시 수준", 256.5)}</div>
  <div class="ls" ${at(260.22)}>다행히 전년 대비 전체적으로 안정되는 추세</div>
</div>
<div class="tb">
  <div class="tr th" ${at(228.95, "fade")}><span>순위</span><span>도시</span><span class="r">1베드룸</span><span class="r">전년 대비</span></div>
  ${RENT.map(([r, n, p, y, c], i) => {
    const t = (229.1 + i * 0.08).toFixed(2), ht = { van: 230.2, tor: 235.0, mtl: 240.0, mid: 249.43 }[c];
    return `<div class="tr ${c || ""}" ${at(t, "fade")}>${c ? `<div class="hl" ${at(ht, "barx")}></div>` : ""}<span>${r}</span><span>${n}</span><span class="r">${p}</span><span class="r">${y}</span></div>`;
  }).join("")}
  <div class="yy" ${at(260.8, "pop")}></div>
</div>
<div class="src">자료: 캐나다 도시별 1베드룸 평균 렌트 순위 (월별 리포트)</div>`,
};

S["s07-tuition-kids"] = {
  title: "학비 조기유학",
  css: `
#S .paths{position:absolute;left:120px;right:120px;top:300px;display:grid;grid-template-columns:1fr 1fr;gap:50px;}
#S .pc{padding:54px 50px;min-height:420px;}
#S .pk{font-size:58px;font-weight:900;}
#S .pd{font-size:34px;font-weight:700;color:var(--ink2);margin-top:16px;line-height:1.4;}
#S .who{margin-top:44px;display:inline-flex;}
#S .cols{position:absolute;left:120px;right:120px;top:330px;height:540px;display:grid;grid-template-columns:repeat(3,1fr);gap:40px;}
#S .cols .card{padding:56px 40px 0;display:flex;flex-direction:column;gap:12px;}
#S .lab{font-size:28px;font-weight:800;color:var(--ink2);margin-top:14px;}
#S .v1{font-size:76px;}
#S .v2{font-size:46px;font-weight:900;}
#S .ft{font-size:27px;font-weight:700;color:var(--ink2);}
#S .unit{position:absolute;right:120px;top:270px;font-size:26px;font-weight:700;color:var(--ink2);}`,
  html: `
${chap("3", "학비", "조기유학 케이스", 270.7)}
<div class="paths" data-out="295.8">
  <div class="card pc" ${at(270.9, "pop")}><div class="pk">조기유학</div><div class="pd">자녀 학비를 직접 납부</div><div class="tag who" ${at(283.45, "pop")}>자녀 1명 · 단기 플랜</div></div>
  <div class="card pc" ${at(275.54, "pop")}><div class="pk">무상교육</div><div class="pd">부모 비자로 공립학교 학비 면제</div><div class="tag who" ${at(289.94, "pop")}>자녀 2명 이상 · 장기 플랜</div></div>
</div>
<div class="unit" ${at(296.6, "fade")}>1년 기준 · CAD</div>
<div class="cols">
  <div class="card cityc van" ${at(296.8, "pop")}><div class="bar"></div>${pill("van")}<div class="lab">공립 (보험료 포함)</div><div>${count(18000, 302.14, { pre: "약 $", cls: "big v1" })}</div><div class="lab">사립</div><div class="v2" ${at(305.0)}>$20,000~35,000</div><div class="ft" ${at(309.62)}>명문 사립은 더 높음</div></div>
  <div class="card cityc tor" ${at(297.2, "pop")}><div class="bar"></div>${pill("tor")}<div class="lab">공립 (보험료 포함)</div><div>${count(18000, 312.25, { pre: "약 $", cls: "big v1" })}</div><div class="lab">사립</div><div class="v2" ${at(316.5)}>$20,000~35,000</div></div>
  <div class="card cityc mtl" ${at(297.6, "pop")}><div class="bar"></div>${pill("mtl")}<div class="lab">공립 (보험료 포함)</div><div>${count(14000, 321.05, { pre: "약 $", cls: "big v1" })}</div><div class="lab">사립</div><div class="v2" ${at(327.54)}>$20,000~35,000</div><div class="ft" style="font-size:32px;color:var(--ink)" ${at(332.02)}>${mk("반값 수준 불어 사립", 333.5)}</div></div>
</div>`,
};

S["s08-parent-tor-van"] = {
  title: "부모 학비 토론토 밴쿠버",
  css: `
#S .lead{font-size:34px;font-weight:700;color:var(--ink2);margin-top:20px;}
#S .two{position:absolute;left:120px;right:120px;top:330px;height:560px;display:grid;grid-template-columns:1fr 1fr;gap:50px;}
#S .two .card{padding:50px 44px 0;}
#S .card .pill{font-size:50px;}
#S .st{display:grid;grid-template-columns:120px 1fr auto;align-items:center;gap:20px;margin-top:26px;padding-bottom:20px;border-bottom:3px solid var(--rule);}
#S .yr{font-size:28px;font-weight:900;color:var(--paper);background:var(--c);border-radius:10px;text-align:center;padding:6px 0;}
#S .what{font-size:34px;font-weight:800;}
#S .amt{font-size:42px;font-weight:900;font-variant-numeric:tabular-nums;}
#S .warn{margin-top:28px;font-size:30px;font-weight:800;line-height:1.45;}
#S .warn small{display:block;font-size:27px;font-weight:600;color:var(--ink2);}`,
  html: `
${chap("4", "부모 학비", "자녀 무상교육 케이스", 340.5)}
<div class="lead" ${at(345.5)}>여기서 세 도시가 꽤 많이 차이가 나요</div>
<div class="two">
  <div class="card cityc tor" ${at(347.5, "pop")}><div class="bar"></div>${pill("tor")}
    <div class="st" ${at(351.32)}><div class="yr">1년차</div><div class="what">대학부설 어학과정</div><div class="amt">약 $18,500</div></div>
    <div class="st" ${at(355.48)}><div class="yr">2년차</div><div class="what">대학 1년</div><div class="amt">$17,000~21,000</div></div>
    <div class="warn" ${at(362.39)}>⚠ ${mk("회화 위주 수업이 아니에요", 365.2)}<small ${at(369.56)}>학업 부담이 꽤 클 수 있어요 — 아이도 챙기셔야 하니까요</small></div></div>
  <div class="card cityc van" ${at(379.54, "pop")}><div class="bar"></div>${pill("van")}
    <div class="st" ${at(381.75)}><div class="yr">1년차</div><div class="what">사설어학원</div><div class="amt">약 $13,500</div></div>
    <div class="st" ${at(385.43)}><div class="yr">2년차</div><div class="what">대학 1년</div><div class="amt">$20,000~25,000</div></div>
    <div class="warn" ${at(390.9)}>${mk("사설어학원 무상교육 — 세 도시 중 유일", 392)}<small ${at(398.17)}>학업 부담↓ · 학비↓</small><small ${at(403.58)}>2년차: 조건부입학 충족 → 부모 대학 진학, 또는 조기유학 전환</small></div></div>
</div>`,
};

S["s09-parent-mtl"] = {
  title: "부모 학비 몬트리올",
  css: `
#S .mc{position:absolute;left:120px;top:280px;width:800px;height:600px;padding:40px 46px 0;}
#S .mc .pill{font-size:50px;}
#S .what{font-size:34px;font-weight:800;margin-top:18px;}
#S .amt{font-size:72px;margin-top:4px;white-space:nowrap;}
#S .amt small{font-size:30px;font-weight:700;color:var(--ink2);margin-left:10px;}
#S .fl{margin-top:16px;display:flex;flex-direction:column;gap:10px;}
#S .fi{font-size:29px;font-weight:700;display:flex;gap:14px;}
#S .fi::before{content:"✓";color:var(--mtl);font-weight:900;}
#S .route{position:absolute;left:980px;right:120px;top:290px;display:flex;flex-direction:column;gap:12px;}
#S .rh{font-size:38px;font-weight:900;margin-bottom:6px;}
#S .rs{display:flex;align-items:center;gap:18px;font-size:32px;font-weight:800;padding:14px 24px;background:#FBF9F4;border:3px solid var(--rule);border-radius:16px;}
#S .rs b{width:46px;height:46px;flex:none;border-radius:50%;background:var(--mtl);color:#fff;font-size:24px;display:flex;align-items:center;justify-content:center;}
#S .rs.last{border-color:var(--mtl);}
#S .ra{font-size:26px;color:var(--ink2);padding-left:36px;line-height:1;}
#S .rfoot{margin-top:14px;font-size:36px;font-weight:900;}
#S .cmp{position:absolute;left:120px;right:120px;top:330px;display:flex;flex-direction:column;gap:46px;}
#S .ch{font-size:44px;font-weight:900;}
#S .cr{display:grid;grid-template-columns:200px 1fr 330px;align-items:center;gap:28px;}
#S .cr .pill{font-size:42px;}
#S .ct{position:relative;height:64px;}
#S .cf{position:absolute;left:0;top:0;bottom:0;background:var(--c);border-radius:10px;transform-origin:left center;}
#S .cf2{position:absolute;top:0;bottom:0;background:var(--c);opacity:.45;border-radius:0 10px 10px 0;transform-origin:left center;}
#S .cv{font-size:44px;font-weight:900;text-align:right;font-variant-numeric:tabular-nums;}`,
  html: `
${chap("4", "부모 학비", "몬트리올", 415.8)}
<div class="card cityc mtl mc" data-out="471.6" ${at(416.2, "pop")}><div class="bar"></div>${pill("mtl")}
  <div class="what" ${at(417.43)}>사립컬리지 · 사설어학원</div>
  <div class="amt big" ${at(419.0)}>${mk("$11,000~12,500", 420.4)}<small>/ 1년</small></div>
  <div class="fl">
    <div class="fi" ${at(426.07)}>사립컬리지 비즈니스 과정으로 무상교육</div>
    <div class="fi" ${at(430.62)}>입학 조건이 상대적으로 수월</div>
    <div class="fi" ${at(433.4)}>수업 스케줄이 자유로워 아이 케어에 유리</div>
    <div class="fi" ${at(438.1)}>주당 24시간까지 파트타임 가능</div>
    <div class="fi" ${at(441.6)}>학업 부담은 캐나다에서 가장 적은 편</div>
  </div></div>
<div class="route" data-out="471.6">
  <div class="rh" ${at(446.81, "right")}>사설어학원을 다니는 경우</div>
  <div class="rs" ${at(447.6, "right")}><b>1</b>영어 · 불어 공부</div>
  <div class="ra" ${at(452.18, "fade")}>▼ 장기 플랜이라면</div>
  <div class="rs" ${at(452.6, "right")}><b>2</b>불어 공부 → 중하급 회화 수준</div>
  <div class="ra" ${at(458.4, "fade")}>▼</div>
  <div class="rs" ${at(458.87, "right")}><b>3</b>영어권 지역으로 이동</div>
  <div class="ra" ${at(461.0, "fade")}>▼</div>
  <div class="rs last" ${at(461.3, "right")}><b>4</b>취업비자 전환 (프랑코폰 모빌리티)</div>
  <div class="rfoot" ${at(467.13)}>${mk("압도적으로 저렴한 플랜", 468)}</div>
</div>
<div class="cmp">
  <div class="ch" ${at(472.02)}>나란히 보면 — 부모 1년차 학비</div>
  <div class="cr tor" ${at(472.4)}>${pill("tor")}<div class="ct"><div class="cf" ${at(472.5, "barx")} style="width:${(18500 / 20000) * 100}%"></div></div><div class="cv">약 $18,500</div></div>
  <div class="cr van" ${at(472.8)}>${pill("van")}<div class="ct"><div class="cf" ${at(472.9, "barx")} style="width:${(13500 / 20000) * 100}%"></div></div><div class="cv">약 $13,500</div></div>
  <div class="cr mtl" ${at(473.2)}>${pill("mtl")}<div class="ct"><div class="cf" ${at(473.3, "barx")} style="width:${(11000 / 20000) * 100}%"></div><div class="cf2" ${at(474.0, "barx")} style="left:${(11000 / 20000) * 100}%;width:${(1500 / 20000) * 100}%"></div></div><div class="cv">${mk("$11,000~12,500", 474.4)}</div></div>
</div>`,
};

S["s10-culture-van"] = {
  title: "문화 밴쿠버", ghost: "VANCOUVER", css: cultureCss,
  html: `
${chap("5", "문화적 환경", "세 도시의 분위기", 478.0)}
<div class="head2 van">${pill("van", 483.32)}<div class="tl" ${at(485.11)}>아름다운 자연 + 문화·레저</div><div class="tl2" ${at(492.47)}>야외 활동을 좋아한다면 ${mk("장점 극대화", 493.5)}</div></div>
<div class="van">${attractions([
    [497.08, "사이언스 월드", "직접 만지고 느끼며 배우는 체험형 과학관"],
    [504.31, "그랜빌 아일랜드", "공예품·먹거리 시장, 아이들을 위한 키즈 마켓"],
    [514.26, "스탠리 파크", "자전거·산책·피크닉, 거대한 공원"],
    [519.77, "밴쿠버 아쿠아리움", "스탠리 파크 안, 다양한 해양 생물"],
    [525.98, "카필라노 서스펜션 브리지", "스릴 넘치는 현수교와 자연 탐험"],
    [533.14, "플라이오버 캐나다", "캐나다의 자연을 몰입형 시뮬레이션으로"],
    [539.7, "밴쿠버 박물관", "밴쿠버의 역사와 문화"],
    [544.54, "밴쿠버 벚꽃 축제", "봄마다 벚꽃 구경과 문화 행사"],
  ], 2)}</div>`,
};
S["s11-culture-tor"] = {
  title: "문화 토론토", ghost: "TORONTO", css: cultureCss,
  html: `
${chap("5", "문화적 환경", "세 도시의 분위기", 552.2)}
<div class="head2 tor">${pill("tor", 552.6)}<div class="tl" ${at(554.3)}>다문화 + 대형 박물관·공연</div><div class="tl2" ${at(564.38)}>${mk("일 년 내내", 565.2)} 축제와 행사</div></div>
<div class="tor">${attractions([
    [568.34, "로열 온타리오 박물관", "캐나다 최대 박물관, 공룡 화석부터 세계 유물까지"],
    [576.86, "온타리오 과학 센터", "직접 만지고 체험하는 전시"],
    [582.9, "리플리스 아쿠아리움", "CN 타워 옆, 상어 터널 대형 수족관"],
    [589.4, "CN 타워", "유리 바닥 전망대에서 도시 전경"],
    [597.72, "하이 파크", "동물원·놀이터·호수, 봄 벚꽃 축제"],
    [603.83, "토론토 아일랜드 공원", "페리로 가는 섬, 해변과 놀이공원"],
    [611.19, "카사 로마", "중세로 여행 온 듯한 성과 정원"],
    [618.23, "디스틸러리 지구", "빅토리아 시대 건물 속 공방과 상점"],
    [628.54, "메이플 리프스 · 랩터스", "아이스하키·농구 경기 관람"],
    [636.0, "다문화 축제", "연중 여러 나라의 음식과 공연"],
  ], 2)}</div>`,
};
S["s12-culture-mtl"] = {
  title: "문화 몬트리올", ghost: "MONTRÉAL", css: cultureCss,
  html: `
${chap("5", "문화적 환경", "세 도시의 분위기", 645.2)}
<div class="head2 mtl">${pill("mtl", 645.6)}<div class="tl" ${at(647.42)}>유럽의 예술적·역사적 분위기</div><div class="tl2" ${at(659.26)}>${mk("확연히 다른 분위기", 660.3)}</div></div>
<div class="mtl">${attractions([
    [664.25, "국제 재즈 페스티벌", "세계 최대 재즈 축제, 야외 무료 공연"],
    [676.09, "국제 불꽃축제", "여름밤을 수놓는 세계적인 불꽃"],
    [681.98, "F1 캐나다 그랑프리", "스피드와 박진감 넘치는 레이싱"],
    [691.32, "몬트리올 미술관", "로댕 '생각하는 사람' 등 세계적 작품"],
    [700.95, "몬트리올 과학 센터", "구항구의 체험형 과학관, 아이맥스"],
    [710.17, "바이오돔", "5가지 생태계를 재현한 실내 동물원"],
    [717.14, "식물원 & 곤충관", "아름다운 정원과 곤충 관찰"],
    [724.89, "몽루아얄 공원", "여름엔 피크닉, 겨울엔 스케이트·썰매"],
    [733.08, "올드 몬트리올", "자갈길 역사 지구, 유럽 분위기"],
    [742.52, "라롱드", "다양한 놀이기구의 대형 놀이공원"],
  ], 2)}</div>`,
};

const popScene = (c, n, startT, basis, extraHead, ringT, p, bars, tags) => ({
  title: "인구 " + CITY[c][0], ghost: "2021", css: popCss,
  html: `
${chap("6", "인구 구성", "2021 인구조사", startT + 0.3)}
<div class="${c}">
<div class="head2" style="display:flex;align-items:center;gap:30px;margin-top:22px">${pill(c, startT + 0.6)}<div class="basis" ${at(basis[0])}>${basis[1]}</div>${extraHead || ""}</div>
${ring(p, ringT)}
${popBars(bars)}
<div class="ptags">${tags.join("")}</div>
</div>`,
});
S["s13-pop-van"] = popScene("van", 0, 751.58, [759.22, "메트로 밴쿠버 기준"], `<div class="basis" style="color:var(--ink)" ${at(762.71)}>아시아계 비율 최상위 도시</div>`, 767.67, 54.5,
  [[773.05, "중국계", 25.9], [776.2, "남아시아계", 6.9], [780.22, "필리핀계", 5.9]],
  [`<div class="tag" ${at(783.29, "pop")}>이민자 42%</div>`, `<div class="tag lite" ${at(786.65, "pop")}>그중 절반 이상 아시아 출신</div>`, `<div class="tag lite" ${at(789.94, "pop")}>리치몬드·버나비 소수 민족 60~80%</div>`]);
S["s14-pop-tor"] = popScene("tor", 0, 798.46, [798.9, "토론토 시 기준"], `<div class="basis" style="color:var(--ink)" ${at(801.82)}>세계에서 가장 다문화적인 도시 중 하나</div>`, 810.81, 57.0,
  [[815.29, "남아시아계", 14.0], [817.8, "중국계", 10.7], [820.89, "흑인계", 9.6]],
  [`<div class="tag lite" ${at(823.6, "pop")}>유럽계 백인 43.5%</div>`, `<div class="tag" ${at(827.77, "pop")}>이민자 46% (밴쿠버보다 높음)</div>`, `<div class="tag lite" ${at(832.25, "pop")}>리틀 이탈리아 · 리틀 인디아 · 코리아타운</div>`]);
S["s15-pop-mtl"] = popScene("mtl", 0, 839.0, [841.14, "몬트리올 시 기준"], `<div class="basis" style="color:var(--ink)" ${at(847.06)}>백인 비율 상대적으로 높음 · 프랑스어권 문화</div>`, 853.05, 38.8,
  [[856.06, "흑인계", 11.5, "캐나다 주요 도시 중 흑인 비율 최고"], [861.6, "아랍계", 8.2], [864.41, "남아시아계", 4.6]],
  [`<div class="tag" ${at(867.93, "pop")}>프랑스계가 가장 큰 비율</div>`, `<div class="tag lite" ${at(870.5, "pop")}>이탈리아계 · 아일랜드계 등 유럽계 비중도 높음</div>`]);

S["s16-pop-india"] = {
  title: "인도인 증가",
  css: `
#S .h{font-size:76px;font-weight:900;margin-top:40px;}
#S .cols{position:absolute;left:120px;right:120px;top:400px;height:470px;display:grid;grid-template-columns:repeat(3,1fr);gap:40px;}
#S .card{padding:56px 44px 0;display:flex;flex-direction:column;gap:22px;}
#S .card .pill{font-size:52px;}
#S .up{font-size:110px;font-weight:900;color:var(--c);line-height:1;}
#S .t{font-size:34px;font-weight:800;line-height:1.4;}
#S .s{font-size:29px;font-weight:700;color:var(--ink2);line-height:1.4;}`,
  html: `
${chap("6", "인구 구성", "최근 이슈", 877.7)}
<div class="h" ${at(878.2)}>${mk("인도계 이민자 증가", 880.5)}</div>
<div class="cols">
  <div class="card cityc tor" ${at(883.58, "pop")}><div class="bar"></div>${pill("tor")}<div class="up">▲</div><div class="t">증가가 가장 두드러짐</div></div>
  <div class="card cityc van" ${at(885.6, "pop")}><div class="bar"></div>${pill("van")}<div class="up">▲</div><div class="t">증가가 가장 두드러짐</div></div>
  <div class="card cityc mtl" ${at(898.14, "pop")}><div class="bar"></div>${pill("mtl")}<div class="up" style="font-size:80px">—</div><div class="t">유입 규모 상대적으로 작음</div><div class="s" ${at(899.74)}>퀘벡주의 프랑스어 정책 영향</div></div>
</div>
<div class="src" ${at(889.02, "fade")} style="left:120px;right:auto;font-size:28px;color:var(--ink)">토론토·밴쿠버: 기존 대규모 커뮤니티 + 활발한 경제 활동</div>`,
};

S["s17-pop-korean"] = {
  title: "한인 인구",
  css: `
#S .rows{position:absolute;left:120px;right:120px;top:290px;display:flex;flex-direction:column;gap:26px;}
#S .kr{display:grid;grid-template-columns:270px 560px 1fr;align-items:center;gap:36px;height:178px;padding:0 36px;background:#FBF9F4;border:3px solid var(--rule);border-radius:22px;}
#S .kr .pill{font-size:46px;}
#S .tot{font-size:26px;font-weight:700;color:var(--ink2);margin-top:8px;}
#S .cnt{font-size:72px;}
#S .cnt small{font-size:30px;font-weight:700;color:var(--ink2);margin-left:6px;}
#S .bt{height:22px;background:#E8E2D2;border-radius:8px;overflow:hidden;margin-top:12px;}
#S .bf{height:100%;background:var(--c);border-radius:8px;transform-origin:left center;}
#S .nt{display:flex;flex-direction:column;gap:8px;}
#S .n1{font-size:31px;font-weight:800;}
#S .n2{font-size:27px;font-weight:700;color:var(--ink2);}`,
  html: `
${chap("6", "인구 구성", "한인 인구", 906.9)}
<div class="rows">
  <div class="kr tor" ${at(910.5, "right")}><div>${pill("tor")}<div class="tot">전체 인구 620만</div></div>
    <div><div>${count(84000, 911.96, { cls: "big cnt" })}<small>명</small></div><div class="bt"><div class="bf" ${at(912.2, "barx")} style="width:${(84000 / 90000) * 100}%"></div></div></div>
    <div class="nt"><div class="n1" ${at(917.43)}>${mk("생활 편의성 최고", 918.4)}</div><div class="n2" ${at(921.78)}>한인타운 · 마트 · 식당 · 병원 · 학원</div><div class="n2" ${at(930.3)}>노스요크 · 리치몬드힐 · 마캄</div></div></div>
  <div class="kr van" ${at(937.78, "right")}><div>${pill("van")}<div class="tot">전체 인구 264만</div></div>
    <div><div>${count(63000, 939.42, { cls: "big cnt" })}<small>명</small></div><div class="bt"><div class="bf" ${at(939.6, "barx")} style="width:${(63000 / 90000) * 100}%"></div></div></div>
    <div class="nt"><div class="n1" ${at(944.57)}>토론토 다음으로 편리</div><div class="n2" ${at(948.41)}>코퀴틀람 · 버나비 · 포트코퀴틀람</div><div class="n2" ${at(958.26)}>따뜻하고 습도 낮은 날씨도 인기 요인</div></div></div>
  <div class="kr mtl" ${at(966.52, "right")}><div>${pill("mtl")}<div class="tot">전체 인구 430만</div></div>
    <div><div>${count(11000, 968.0, { cls: "big cnt" })}<small>명</small></div><div class="bt"><div class="bf" ${at(968.2, "barx")} style="width:${(11000 / 90000) * 100}%"></div></div></div>
    <div class="nt"><div class="n1" ${at(973.21)}>불어 환경 → 한인 커뮤니티 작음</div><div class="n2" ${at(977.98)}>한인 편의시설이 확실히 적어요</div></div></div>
</div>`,
};

// weather: axis -15..30 over 520px
const ty = (v) => ((v + 15) / 45) * 440;
const wbar = (c, lo, hi, t) =>
  `<div class="wb ${c}"><div class="wf" ${at(t, "bary")} style="bottom:${ty(lo)}px;height:${ty(hi) - ty(lo)}px"></div><div class="wv" style="bottom:${ty(hi) + 8}px" ${at(t + 0.4, "fade")}>${hi}°</div><div class="wv lo" style="bottom:${ty(lo) - 46}px" ${at(t + 0.4, "fade")}>${lo}°</div><div class="wn cc">${CITY[c][0]}</div></div>`;
S["s18-weather"] = {
  title: "날씨", ghost: "°C",
  css: `
#S .verdict{position:absolute;right:120px;top:166px;font-size:40px;font-weight:900;}
#S .pan{position:absolute;top:300px;width:760px;height:440px;}
#S .pan.p1{left:120px;} #S .pan.p2{right:120px;}
#S .ph{position:absolute;left:0;top:-14px;font-size:40px;font-weight:900;}
#S .zero{position:absolute;left:0;right:0;height:0;border-top:3px dashed var(--ink2);}
#S .zero span{position:absolute;right:0;top:-36px;font-size:24px;font-weight:800;color:var(--ink2);}
#S .bars{position:absolute;left:120px;right:40px;top:0;bottom:0;display:flex;gap:60px;}
#S .wb{position:relative;flex:1;height:100%;}
#S .wf{position:absolute;left:24px;right:24px;background:var(--c);border-radius:14px;transform-origin:bottom center;}
#S .wv{position:absolute;left:0;right:0;text-align:center;font-size:36px;font-weight:900;font-variant-numeric:tabular-nums;}
#S .wv.lo{color:var(--ink2);font-size:30px;}
#S .wn{position:absolute;left:-10px;right:-10px;bottom:-56px;text-align:center;font-size:30px;font-weight:900;}
#S .foot{position:absolute;left:120px;top:848px;font-size:34px;font-weight:800;}`,
  html: `
${chap("7", "날씨", "일평균 최고·최저 기온", 984.9)}
<div class="verdict" ${at(991.35, "right")}>솔직히 비교 불가 — ${mk("밴쿠버 압도적", 993.8)}</div>
<div class="pan p1" ${at(995.48, "fade")}><div class="ph">1월</div><div class="zero" style="bottom:${ty(0)}px"><span>0°C</span></div>
  <div class="bars">${wbar("van", 2, 6, 996.95)}${wbar("tor", -8, -1, 1002.1)}${wbar("mtl", -12, -5, 1006.3)}</div></div>
<div class="pan p2" ${at(1011.96, "fade")}><div class="ph">7월</div><div class="zero" style="bottom:${ty(0)}px"><span>0°C</span></div>
  <div class="bars">${wbar("van", 14, 22, 1012.5)}${wbar("tor", 17, 25, 1018.36)}${wbar("mtl", 17, 26, 1019.6)}</div></div>
<div class="foot" ${at(1023.16)}><span class="cc van" style="--c:var(--van)">밴쿠버</span>는 여름·겨울 기온차가 작고 ${mk("전체적으로 온화", 1025)}</div>`,
};

S["s19-car"] = {
  title: "자동차",
  css: `
#S .two{position:absolute;left:120px;right:120px;top:290px;height:380px;display:grid;grid-template-columns:1fr 1fr;gap:50px;}
#S .two .card{padding:56px 46px 0;}
#S .pills{display:flex;gap:30px;}
#S .pills .pill{font-size:48px;}
#S .k{font-size:50px;font-weight:900;margin-top:30px;line-height:1.3;}
#S .s{font-size:31px;font-weight:700;color:var(--ink2);margin-top:18px;}
#S .strip{position:absolute;left:120px;right:120px;top:710px;display:flex;align-items:center;gap:22px;}
#S .strip .tag{font-size:32px;}
#S .eq{font-size:44px;font-weight:900;color:var(--ink2);}`,
  html: `
${chap("8", "자동차", "구입이 필요할까?", 1030.4)}
<div class="two">
  <div class="card" style="border-color:var(--ink)" ${at(1033.62, "pop")}><div class="pills">${pill("van")}${pill("tor")}</div><div class="k">보통 ${mk("자동차 구입 필요", 1035)}</div></div>
  <div class="card cityc mtl" ${at(1037.8, "pop")}><div class="bar"></div>${pill("mtl")}<div class="k">1~2년 단기라면<br/>안 사는 경우가 더 많아요</div><div class="s" ${at(1043.61)}>꼭 필요할 땐 공유자동차 서비스</div></div>
</div>
<div class="strip"><div class="tag lite" ${at(1048.41, "pop")}>한국보다 비싼 보험료</div><div class="tag lite" ${at(1051.8, "pop")}>주차비</div><div class="eq" ${at(1053.11, "fade")}>=</div><div class="tag" ${at(1053.4, "pop")}>매달 나가는 기본 지출</div><div style="font-size:36px;font-weight:900;margin-left:16px" ${at(1056.82)}>${mk("예산에 꼭 포함", 1058)}</div></div>`,
};

S["s20-language"] = {
  title: "자녀 언어향상",
  css: `
#S .qa{position:absolute;left:120px;right:120px;top:290px;display:flex;flex-direction:column;gap:34px;}
#S .l1{font-size:40px;font-weight:700;color:var(--ink2);}
#S .q{font-size:62px;font-weight:900;}
#S .q span{color:var(--mtl);}
#S .a{font-size:62px;font-weight:900;}
#S .son{display:inline-flex;align-items:center;gap:16px;font-size:36px;font-weight:800;padding:18px 30px;background:#FBF9F4;border:3px solid var(--mtl);border-radius:18px;}
#S .fr{position:absolute;left:120px;right:120px;display:flex;align-items:center;gap:22px;}
#S .fr.r1{top:330px;} #S .fr.r2{top:600px;}
#S .rl{width:190px;flex:none;font-size:32px;font-weight:900;color:var(--paper);background:var(--ink);border-radius:14px;padding:16px 0;text-align:center;}
#S .box{font-size:36px;font-weight:800;padding:26px 30px;background:#FBF9F4;border:3px solid var(--rule);border-radius:18px;}
#S .ar{font-size:44px;font-weight:900;color:var(--ink2);}`,
  html: `
${chap("+", "자녀 언어향상", "몬트리올에서도 영어가 늘까?", 1062.8)}
<div class="qa" data-out="1091.6">
  <div class="l1" ${at(1069.18)}>어느 도시든 시간이 지나면 아이들 영어는 충분히 늘어요</div>
  <div class="q" ${at(1074.55)}>"<span>불어 환경</span>이라 영어가 안 늘면 어쩌지?"</div>
  <div class="a" ${at(1082.9)}>→ 몬트리올에서도 ${mk("영어는 충분히 늡니다", 1084)}</div>
  <div ${at(1087.19, "pop")}><span class="son">몬트리올에 사는 제 아들도 제1언어가 영어예요</span></div>
</div>
<div class="fr r1"><div class="rl" ${at(1092.18, "left")}>예산</div><div class="box" ${at(1093.0, "right")}>몬트리올은 저렴</div><div class="ar" ${at(1095.5, "fade")}>→</div><div class="box" ${at(1096.0, "right")}>아낀 비용으로 ${mk("튜터", 1097)}</div><div class="ar" ${at(1102.8, "fade")}>→</div><div class="box" ${at(1103.22, "right")}>학교 적응 · 영어 향상</div></div>
<div class="fr r2"><div class="rl" ${at(1109.75, "left")}>장기 플랜</div><div class="box" ${at(1112.63, "right")}>${mk("영어 + 불어", 1113.6)} 자연스럽게</div><div class="ar" ${at(1118.6, "fade")}>→</div><div class="box" ${at(1119.06, "right")}>3년 이상 후 귀국 → 서울프랑스학교 등 외국인학교</div></div>`,
};

S["s21-wrap"] = {
  title: "마무리",
  css: `
#S .h{font-size:64px;font-weight:900;}
#S .crit{position:absolute;left:120px;right:120px;top:290px;}
${critCss}
#S .ct{height:140px;}
#S .msg{position:absolute;left:120px;right:120px;top:330px;}
#S .m1{font-size:46px;font-weight:700;color:var(--ink2);}
#S .m2{font-size:96px;font-weight:900;letter-spacing:-.03em;line-height:1.2;margin-top:34px;}`,
  html: `
<div class="h" ${at(1130.6)} data-out="1140.5">8가지 기준으로 비교해 봤습니다</div>
<div data-out="1140.5">${critGrid(1131.2, 0.3)}</div>
<div class="msg">
  <div class="m1" ${at(1140.89)}>가정마다 중요한 기준은 다 다를 거예요</div>
  <div class="m2" ${at(1144.54)}>우리 가족의<br/>${mk("우선순위", 1148.41)}부터 정해보세요</div>
</div>`,
};

S["s22-contact"] = {
  title: "상담 안내", noExit: true,
  css: `
#S .brand{font-size:110px;font-weight:900;letter-spacing:-.02em;}
#S .brand span{color:var(--mtl);}
#S .bs{font-size:38px;font-weight:700;color:var(--ink2);margin-top:8px;}
#S .svc{display:flex;gap:18px;margin-top:40px;align-items:center;}
#S .svc .free{font-size:40px;font-weight:900;margin-left:12px;}
#S .ct{position:absolute;left:120px;right:120px;top:600px;display:grid;grid-template-columns:repeat(3,1fr);gap:36px;}
#S .cb{padding:36px 38px;background:#FBF9F4;border:3px solid var(--ink);border-radius:22px;}
#S .cl{font-size:28px;font-weight:800;color:var(--ink2);}
#S .cv{font-size:50px;font-weight:900;margin-top:8px;font-variant-numeric:tabular-nums;}
#S .cs{font-size:24px;font-weight:700;color:var(--ink2);margin-top:6px;}
#S .bye{position:absolute;right:120px;top:170px;text-align:right;font-size:36px;font-weight:800;color:var(--ink2);line-height:1.5;}`,
  html: `
<div class="brand" ${at(1158.0)}>AA <span>CANADA</span></div>
<div class="bs" ${at(1158.6)}>어느 도시든 자세한 진행 절차와 상담은 편하게 문의 주세요</div>
<div class="svc"><div class="tag lite" ${at(1164.86, "pop")}>입학 수속</div><div class="tag lite" ${at(1165.6, "pop")}>비자 대행</div><div class="tag lite" ${at(1166.3, "pop")}>출국 준비 가이드</div><div class="free" ${at(1167.2)}>${mk("전부 무료 진행", 1167.8)}</div></div>
<div class="ct">
  <div class="cb" ${at(1170.65, "pop")}><div class="cl">전화</div><div class="cv">02-567-4345</div></div>
  <div class="cb" ${at(1174.26, "pop")}><div class="cl">휴대폰</div><div class="cv">010-4857-4345</div><div class="cs">평일 야간 · 주말 상담 가능</div></div>
  <div class="cb" ${at(1179.45, "pop")}><div class="cl">카카오톡</div><div class="cv">canlog</div></div>
</div>
<div class="bye" ${at(1184.44, "right")}>구독 · 좋아요 부탁드려요<br/><span style="color:var(--ink);font-weight:900" ${at(1191.13, "fade")}>감사합니다</span></div>`,
};

export const scenes = STARTS.map(([id, start], i) => {
  const end = i + 1 < STARTS.length ? STARTS[i + 1][1] : END;
  return { id, start, duration: +(end - start).toFixed(2), ...S[id] };
});
