// Scenes that show the user's own source captures (assets/captures/*.png) as
// documents on screen, with highlight boxes and camera zooms timed to narration.
// Box / zoom coordinates are in the capture's own pixel space.

const IMG = {
  pisa: ["assets/captures/pisa.png", 874, 574],
  pcap: ["assets/captures/pcap.png", 846, 500],
  rent: ["assets/captures/rent.png", 878, 635],
  chart: ["assets/captures/temp-chart.png", 1100, 645],
  table: ["assets/captures/temp-table.png", 1030, 397],
};

// doc(): an on-screen capture card.
//   pos: CSS for left/right/top; w: card width in px (height follows the image aspect)
//   boxes: [t, x, y, w, h, cls, label]  (cls: van|tor|mtl|ink|mark)
//   zooms: [t, scale, cx, cy, dur]      (cx/cy = point to centre, image px)
export function CAPTURE_SCENES({ at }) {
  let n = 0;
  function doc(key, { pos, w, appear, out, boxes = [], zooms = [], fx = "right" }) {
    const [src, iw, ih] = IMG[key];
    const h = Math.round((w * ih) / iw), id = `cap${++n}`;
    const pct = (v, d) => ((v / d) * 100).toFixed(3) + "%";
    const bx = boxes
      .map(([t, x, y, bw, bh, cls, label]) =>
        `<div class="hb ${cls}" ${at(t, "pop")} style="left:${pct(x, iw)};top:${pct(y, ih)};width:${pct(bw, iw)};height:${pct(bh, ih)}">${label ? `<b>${label}</b>` : ""}</div>`)
      .join("");
    const html = `<div class="doc ${id}" ${at(appear, fx)} ${out ? `data-out="${out}"` : ""} style="${pos};width:${w}px;height:${h}px"><div class="cam"><img src="${src}" alt="" />${bx}</div><div class="capt">실제 자료 캡처</div></div>`;
    const js = zooms.length
      ? `(function(){var cam=root.querySelector(".${id} .cam"),W=${w},H=${h},IW=${iw},IH=${ih};
          function st(s,cx,cy){var px=cx*W/IW,py=cy*H/IH,x=W/2-px*s,y=H/2-py*s;x=Math.min(0,Math.max(W-W*s,x));y=Math.min(0,Math.max(H-H*s,y));return{scale:s,x:x,y:y};}
          var prev={scale:1,x:0,y:0};
          ${JSON.stringify(zooms)}.forEach(function(z){var nx=st(z[1],z[2],z[3]);tl.fromTo(cam,prev,Object.assign({duration:z[4]||1.2,ease:"power2.inOut",immediateRender:false},nx),Math.max(0,z[0]-S));prev=nx;});})();`
      : "";
    return { html, js };
  }

  const leftCol = `
#S .lc{position:absolute;left:120px;top:290px;width:540px;display:flex;flex-direction:column;gap:28px;}
#S .lt{font-size:40px;font-weight:800;line-height:1.35;}
#S .ls{font-size:30px;font-weight:600;color:var(--ink2);line-height:1.4;}
#S .tags{display:flex;gap:16px;}
#S .callout{font-size:44px;font-weight:900;line-height:1.3;}`;
  const chapter = (n, title, sub, t) =>
    `<div class="chap" ${at(t, "left")}><div class="n">${n}</div><h2>${title}</h2>${sub ? `<div class="sub">${sub}</div>` : ""}</div>`;
  const mk = (txt, t) => `<span class="mk" ${at(t, "mark")}><span class="mkb"></span><span class="mkt">${txt}</span></span>`;
  const S = {};

  // ① PISA
  const pisa = doc("pisa", {
    pos: "right:120px;top:250px", w: 980, appear: 110.62,
    boxes: [
      [117.14, 255, 420, 515, 44, "ink", "오른쪽으로 갈수록 점수 ↑"],
      [121.78, 130, 219, 645, 28, "ink in", "OECD 평균"],
      [124.12, 130, 272, 645, 28, "tor in", "온타리오"],
      [125.2, 130, 299, 645, 28, "van in", "BC"],
      [126.3, 130, 326, 645, 28, "mtl in", "퀘벡"],
    ],
    zooms: [[124.0, 1.3, 450, 290, 1.4], [131.06, 1.5, 430, 320, 1.4]],
  });
  S["s03-edu-pisa"] = {
    title: "교육 PISA", css: leftCol, js: pisa.js,
    html: `
${chapter("1", "교육환경", "학업성취도 비교", 85.6)}
<div class="lc">
  <div class="lt" ${at(87.58)}>캐나다는 주마다<br/>교육제도가 다릅니다</div>
  <div class="ls" ${at(94.26)}>그나마 객관적으로 비교할 수 있는 지표 2가지 — 주별 비교</div>
  <div class="tags"><span class="tag" ${at(96.5, "pop")}>PISA</span><span class="tag lite" ${at(97.2, "pop")}>PCAP</span></div>
  <div class="ls" ${at(110.62)}><b style="color:var(--ink)">PISA</b> — OECD가 주관하는<br/>국제 학생 평가 프로그램</div>
  <div class="callout" ${at(131.06)}><span style="color:var(--mtl)">퀘벡</span>이 ${mk("가장 오른쪽", 131.8)}</div>
</div>
${pisa.html}`,
  };

  // ① PCAP
  const pcap = doc("pcap", {
    pos: "right:120px;top:262px", w: 1040, appear: 135.6,
    boxes: [
      [148.34, 90, 248, 56, 225, "van", "BC 490"],
      [150.6, 360, 200, 56, 273, "tor", "ON 512"],
      [152.92, 428, 150, 56, 323, "mtl", "QC 537"],
      [156.31, 80, 204, 745, 18, "ink", "캐나다 평균 510"],
    ],
    zooms: [[152.92, 1.45, 455, 300, 1.2], [156.0, 1.0, 423, 250, 1.2]],
  });
  S["s04-edu-pcap"] = {
    title: "교육 PCAP", css: leftCol, js: pcap.js,
    html: `
${chapter("1", "교육환경", "PCAP", 135.3)}
<div class="lc">
  <div class="lt" ${at(135.6)}>PCAP — 캐나다 전국<br/>학업성취도 평가</div>
  <div class="ls" ${at(138.17)}>캐나다 교육부 장관 협의회(CMEC)가 만든 평가</div>
  <div class="ls" ${at(146.42)}>주별 수학 점수</div>
  <div class="callout" ${at(160.12)}><span style="color:var(--mtl)">퀘벡</span>, ${mk("꽤 높은 편", 160.8)}</div>
  <div class="ls" ${at(163.9)}>※ 학업성취도가 절대적인 기준은 아닙니다</div>
</div>
${pcap.html}`,
  };

  // ② Rent
  const rent = doc("rent", {
    pos: "right:120px;top:250px", w: 880, appear: 228.95,
    boxes: [
      [229.6, 4, 84, 870, 34, "van in", "밴쿠버 1위 $2,500"],
      [234.8, 4, 155, 870, 35, "tor in", "토론토 3위 $2,220"],
      [240.0, 4, 481, 870, 35, "mtl in", "몬트리올 12위 $1,710"],
      [249.43, 4, 192, 870, 34, "ink in", "핼리팩스"],
      [250.0, 4, 264, 870, 35, "ink in", "오타와"],
      [250.6, 4, 409, 870, 35, "ink in", "킹스턴"],
      [251.2, 4, 445, 870, 35, "ink in", "키치너"],
      [260.22, 488, 52, 88, 570, "mark", "전년 대비"],
    ],
    zooms: [
      [229.3, 1.55, 300, 100, 1.2], [234.55, 1.55, 300, 172, 1.0], [238.9, 1.55, 300, 498, 1.4],
      [249.2, 1.0, 439, 317, 1.2], [260.22, 1.3, 530, 330, 1.2],
    ],
  });
  S["s06-rent"] = {
    title: "거주비", css: leftCol, js: rent.js,
    html: `
${chapter("2", "거주비", "1베드룸 월 렌트비 (CAD)", 213.4)}
<div class="lc">
  <div class="lt" ${at(215.58)}>도시 선택의 핵심 = ${mk("예산", 217)}<br/>그래서 렌트비가 중요해요</div>
  <div class="ls" ${at(223.58)}>대도시니까 렌트비가 비싼 건 어느 정도 감안해야 합니다</div>
  <div class="callout" ${at(255.38)}>몬트리올은 대도시인데<br/>${mk("렌트비는 중소도시 수준", 256.5)}</div>
  <div class="ls" ${at(260.22)}>다행히 전년 대비 전체적으로 안정되는 추세</div>
</div>
${rent.html}`,
  };

  // ⑦ Weather — chart capture, then the table capture
  const chart = doc("chart", {
    pos: "left:120px;top:250px", w: 1100, appear: 995.0, out: 1022.8,
    boxes: [
      [995.48, 128, 265, 92, 262, "ink", "1월"],
      [1011.96, 528, 92, 100, 132, "ink", "7월"],
    ],
    zooms: [[995.6, 1.6, 175, 400, 1.3], [1011.6, 1.6, 578, 160, 1.6]],
  });
  const table = doc("table", {
    pos: "left:120px;top:262px", w: 1500, appear: 1023.4,
    boxes: [
      [1024.0, 150, 52, 722, 40, "van in", "밴쿠버 최고"],
      [1024.6, 150, 251, 722, 40, "van in", "밴쿠버 최저"],
    ],
  });
  const row = (c, name, v, t) =>
    `<div class="wr" ${at(t, "right")}><span class="cc ${c}" style="--c:var(--${c})">${name}</span><b>${v}</b></div>`;
  S["s18-weather"] = {
    title: "날씨", js: chart.js + table.js,
    css: `
#S .verdict{position:absolute;right:120px;top:166px;font-size:40px;font-weight:900;}
#S .side{position:absolute;left:1270px;right:120px;top:270px;display:flex;flex-direction:column;gap:14px;}
#S .sh{font-size:36px;font-weight:900;margin-top:18px;}
#S .wr{display:flex;justify-content:space-between;align-items:baseline;padding:12px 0;border-bottom:3px solid var(--rule);font-size:32px;font-weight:800;}
#S .wr b{font-size:38px;font-weight:900;font-variant-numeric:tabular-nums;}
#S .foot{position:absolute;left:120px;top:858px;font-size:40px;font-weight:900;}`,
    html: `
${chapter("7", "날씨", "일평균 최고·최저 기온", 984.9)}
<div class="verdict" ${at(991.35, "right")}>솔직히 비교 불가 — ${mk("밴쿠버 압도적", 993.8)}</div>
${chart.html}
<div class="side" data-out="1022.8">
  <div class="sh" ${at(995.48)}>1월 최고 / 최저</div>
  ${row("van", "밴쿠버", "6° / 2°", 996.95)}${row("tor", "토론토", "-1° / -8°", 1002.1)}${row("mtl", "몬트리올", "-5° / -12°", 1006.3)}
  <div class="sh" ${at(1011.96)}>7월 최고</div>
  ${row("van", "밴쿠버", "22°", 1012.5)}${row("tor", "토론토", "25°", 1018.36)}${row("mtl", "몬트리올", "26°", 1019.6)}
</div>
${table.html}
<div class="foot" ${at(1024.2)}><span style="color:var(--van)">밴쿠버</span>는 여름·겨울 기온차가 작고 ${mk("전체적으로 온화", 1025.4)}</div>`,
  };

  return S;
}
