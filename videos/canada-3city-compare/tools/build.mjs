// Generates index.html + compositions/*.html from the scene data below.
// Times in data-at are ABSOLUTE narration seconds (from assets/audio/narration-asr.json);
// each scene's script rebases them to scene-local time.
import { writeFileSync, mkdirSync } from "node:fs";
import { scenes } from "./scenes.mjs";

const TOTAL = 1196.35;
const FONT_WEIGHTS = [
  ["Regular", 400],
  ["Medium", 500],
  ["SemiBold", 600],
  ["Bold", 700],
  ["ExtraBold", 800],
  ["Black", 900],
];
const fontFace = (base) =>
  FONT_WEIGHTS.map(
    ([n, w]) =>
      `@font-face{font-family:"Pretendard";src:url("${base}assets/fonts/Pretendard-${n}.woff2") format("woff2");font-weight:${w};font-style:normal;}`,
  ).join("\n");

const TOKENS = `
  --paper:#F5F2EA; --paper2:#ECE7DA; --ink:#1C2431; --ink2:#4E5767; --rule:#C9C1AE;
  --van:#5B3FA0; --tor:#13845A; --mtl:#D2343F; --marker:#F7D046;`;

// Shared scene CSS (lives inside every <template>).
const sceneCss = (id) => `
#${id}{position:absolute;inset:0;${TOKENS}font-family:"Pretendard",sans-serif;color:var(--ink);overflow:hidden;}
#${id} *{box-sizing:border-box;margin:0;padding:0;}
#${id} .stage{position:absolute;inset:0;padding:150px 120px 170px;}
#${id} .ghost{position:absolute;right:-40px;bottom:120px;font-size:300px;font-weight:900;color:var(--ink);opacity:.06;white-space:nowrap;letter-spacing:-.04em;line-height:1;}
#${id} .chap{display:flex;align-items:center;gap:26px;height:96px;}
#${id} .chap .n{width:84px;height:84px;border-radius:50%;background:var(--ink);color:var(--paper);font-size:44px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none;}
#${id} .chap h2{font-size:66px;font-weight:900;letter-spacing:-.02em;}
#${id} .chap .sub{font-size:34px;font-weight:600;color:var(--ink2);padding-left:24px;border-left:4px solid var(--rule);}
#${id} .van{--c:var(--van);} #${id} .tor{--c:var(--tor);} #${id} .mtl{--c:var(--mtl);}
#${id} .cc{color:var(--c);}
#${id} .pill{display:inline-flex;align-items:center;gap:14px;font-size:34px;font-weight:800;color:var(--c);}
#${id} .pill::before{content:"";width:22px;height:22px;border-radius:50%;background:var(--c);}
#${id} .mk{position:relative;display:inline-block;isolation:isolate;}
#${id} .mk .mkb{position:absolute;left:-8px;right:-8px;bottom:4%;height:46%;background:var(--marker);display:block;transform-origin:left center;transform:scaleX(0);border-radius:4px;}
#${id} .mk .mkt{position:relative;}
#${id} .card{position:relative;background:#FBF9F4;border:3px solid var(--rule);border-radius:22px;overflow:hidden;}
#${id} .card.cityc{border-color:var(--c);}
#${id} .card .bar{position:absolute;left:0;top:0;right:0;height:14px;background:var(--c);}
#${id} .note{font-size:34px;font-weight:600;color:var(--ink2);}
#${id} .big{font-weight:900;letter-spacing:-.03em;font-variant-numeric:tabular-nums;}
#${id} .tag{display:inline-flex;align-items:center;padding:12px 26px;border-radius:999px;background:var(--ink);color:var(--paper);font-size:32px;font-weight:700;}
#${id} .tag.lite{background:var(--paper2);color:var(--ink);border:3px solid var(--rule);}
#${id} .arrow{font-weight:900;color:var(--ink2);}
#${id} .doc{position:absolute;background:#fff;border:3px solid var(--rule);border-radius:18px;overflow:hidden;box-shadow:0 26px 60px rgba(28,36,49,.22);}
#${id} .doc .cam{position:absolute;left:0;top:0;width:100%;height:100%;transform-origin:0 0;}
#${id} .doc img{display:block;width:100%;height:100%;}
#${id} .hb{position:absolute;border:5px solid var(--c);border-radius:8px;box-shadow:0 0 0 4px rgba(255,255,255,.7);}
#${id} .hb b{position:absolute;right:-5px;bottom:100%;margin-bottom:6px;white-space:nowrap;background:var(--c);color:#fff;font-size:22px;font-weight:800;padding:4px 12px;border-radius:8px;}
#${id} .hb.in b{bottom:auto;top:50%;right:8px;margin:0;transform:translateY(-50%);font-size:20px;padding:2px 10px;}
#${id} .hb.ink{--c:var(--ink);} #${id} .hb.mark{--c:#E0B417;}
#${id} .capt{position:absolute;left:14px;top:14px;z-index:2;background:var(--ink);color:var(--paper);font-size:20px;font-weight:800;padding:6px 14px;border-radius:8px;}
#${id} .src{position:absolute;right:120px;bottom:178px;font-size:22px;font-weight:600;color:var(--ink2);}
`;

function sceneHtml(s) {
  const id = s.id;
  return `<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /><title>${s.title}</title></head>
  <body>
    <template>
      <style>
${fontFace("")}
${sceneCss(id)}
${(s.css || "").replaceAll("#S", "#" + id)}
      </style>
      <div id="${id}" data-composition-id="${id}" data-width="1920" data-height="1080">
        ${s.ghost ? `<div class="ghost">${s.ghost}</div>` : ""}
        <div class="stage">
${s.html}
        </div>
      </div>
      <script>
        (function () {
          var S = ${s.start}, D = ${s.duration}, root = document.getElementById("${id}");
          var tl = gsap.timeline({ paused: true });
          var stage = root.querySelector(".stage"), ghost = root.querySelector(".ghost");
          ${s.noEnter ? "" : `tl.fromTo(stage, { x: 90, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, 0);`}
          ${s.noExit ? "" : `tl.fromTo(stage, { x: 0, opacity: 1 }, { x: -90, opacity: 0, duration: 0.45, ease: "power2.in", immediateRender: false }, D - 0.45);`}
          if (ghost) tl.fromTo(ghost, { x: 0 }, { x: -220, duration: D, ease: "none" }, 0);
          var FX = {
            up: [{ y: 36, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: "power3.out" }],
            left: [{ x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.55, ease: "expo.out" }],
            right: [{ x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.55, ease: "expo.out" }],
            pop: [{ scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.7)" }],
            fade: [{ opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power1.out" }],
            barx: [{ scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "power3.out" }],
            bary: [{ scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: "power3.out" }]
          };
          function fmt(v, el) {
            var dec = +(el.getAttribute("data-dec") || 0), s = v.toFixed(dec);
            if (el.hasAttribute("data-comma")) s = Number(s).toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
            return (el.getAttribute("data-pre") || "") + s + (el.getAttribute("data-suf") || "");
          }
          root.querySelectorAll("[data-at]").forEach(function (el) {
            var t = Math.max(0, +el.getAttribute("data-at") - S);
            (el.getAttribute("data-fx") || "up").split(" ").forEach(function (fx) {
              if (FX[fx]) tl.fromTo(el, FX[fx][0], FX[fx][1], t);
              else if (fx === "mark") { var b = el.querySelector(".mkb"); if (b) tl.fromTo(b, { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.15); }
              else if (fx === "count") {
                var o = { v: +(el.getAttribute("data-from") || 0) }, to = +el.getAttribute("data-to");
                el.textContent = fmt(o.v, el);
                tl.fromTo(o, { v: o.v }, { v: to, duration: 1.1, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v, el); } }, t);
              } else if (fx === "ring") {
                var c = el.querySelector(".ringv"), C = 2 * Math.PI * +c.getAttribute("r"), p = +el.getAttribute("data-p");
                c.style.strokeDasharray = C; tl.fromTo(c, { strokeDashoffset: C }, { strokeDashoffset: C * (1 - p), duration: 1.2, ease: "power3.out" }, t);
              } else if (fx === "dim") tl.fromTo(el, { opacity: 1 }, { opacity: 0.22, duration: 0.5, ease: "power1.out", immediateRender: false }, t);
            });
          });
          root.querySelectorAll("[data-out]").forEach(function (el) {
            var t = +el.getAttribute("data-out") - S;
            tl.fromTo(el, { opacity: 1, y: 0 }, { opacity: 0, y: -24, duration: 0.4, ease: "power2.in", immediateRender: false }, t);
          });
          ${s.js || ""}
          window.__timelines["${id}"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
`;
}

// ---- index.html: shared background, chapter spine, narration, scene hosts ----
const CHAPTERS = [
  ["1", "교육환경", 85.27],
  ["2", "거주비", 213.14],
  ["3", "학비", 270.42],
  ["4", "부모 학비", 340.18],
  ["5", "문화", 477.75],
  ["6", "인구", 751.58],
  ["7", "날씨", 984.6],
  ["8", "자동차", 1030.17],
  ["+", "언어", 1062.52],
];
const SPINE_START = 85.27, SPINE_END = 1130.33;

function indexHtml() {
  const hosts = scenes
    .map(
      (s, i) => `      <div id="slot-${s.id}" data-composition-id="${s.id}" data-composition-src="compositions/${s.id}.html"
        data-start="${s.start}" data-duration="${s.duration}" data-track-index="2" data-width="1920" data-height="1080"></div>`,
    )
    .join("\n");
  const pills = CHAPTERS.map(
    ([n, name], i) => `<div class="sp" id="sp${i}"><span class="spn">${n}</span><span class="spt">${name}</span></div>`,
  ).join("");
  return `<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>밴쿠버 vs 토론토 vs 몬트리올 — 8가지 기준 비교</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
${fontFace("")}
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #F5F2EA; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Pretendard", sans-serif; ${TOKENS} }
      #bg { position: absolute; inset: 0; background: var(--paper); }
      #grid { position: absolute; inset: -60px; background-image: linear-gradient(rgba(28,36,49,.07) 2px, transparent 2px), linear-gradient(90deg, rgba(28,36,49,.07) 2px, transparent 2px); background-size: 60px 60px; }
      #glow { position: absolute; width: 1400px; height: 1400px; left: 900px; top: -500px; border-radius: 50%; background: radial-gradient(circle, rgba(247,208,70,.28), rgba(247,208,70,0) 65%); }
      #spine { position: absolute; left: 120px; right: 120px; top: 38px; height: 64px; display: flex; gap: 12px; }
      #spine .sp { flex: 1; display: flex; align-items: center; justify-content: center; gap: 10px; border-radius: 14px; border: 3px solid var(--rule); background: #FBF9F4; color: var(--ink2); font-size: 24px; font-weight: 700; }
      #spine .spn { font-weight: 900; }
      #brand { position: absolute; right: 120px; bottom: 60px; font-size: 24px; font-weight: 800; color: var(--ink2); letter-spacing: .04em; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${TOTAL}" data-width="1920" data-height="1080">
      <div id="bg-layer" class="clip" data-start="0" data-duration="${TOTAL}" data-track-index="0">
        <div id="bg"></div><div id="grid"></div><div id="glow"></div>
        <div id="brand">AA CANADA</div>
      </div>
      <div id="spine-layer" class="clip" data-start="${SPINE_START}" data-duration="${(SPINE_END - SPINE_START).toFixed(2)}" data-track-index="3">
        <div id="spine">${pills}</div>
      </div>
${hosts}
      <audio id="narration" src="assets/audio/narration.m4a" data-start="0" data-duration="${TOTAL}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      var tl = gsap.timeline({ paused: true });
      tl.fromTo("#grid", { x: 0, y: 0 }, { x: -60, y: -60, duration: ${TOTAL}, ease: "none" }, 0);
      tl.fromTo("#glow", { scale: 1 }, { scale: 1.12, duration: 8, ease: "sine.inOut", yoyo: true, repeat: ${Math.floor(TOTAL / 8) - 1} }, 0);
      tl.fromTo("#spine", { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, ${SPINE_START});
      tl.fromTo("#spine", { opacity: 1 }, { opacity: 0, duration: 0.45, ease: "power2.in", immediateRender: false }, ${SPINE_END - 0.45});
      var CH = ${JSON.stringify(CHAPTERS.map((c) => c[2]))};
      CH.forEach(function (t, i) {
        var el = document.getElementById("sp" + i), end = CH[i + 1] || ${SPINE_END};
        tl.fromTo(el, { backgroundColor: "#FBF9F4", color: "#4E5767", borderColor: "#C9C1AE" },
          { backgroundColor: "#1C2431", color: "#F5F2EA", borderColor: "#1C2431", duration: 0.35, ease: "power2.out", immediateRender: false }, t);
        if (end < ${SPINE_END})
          tl.fromTo(el, { backgroundColor: "#1C2431", color: "#F5F2EA", borderColor: "#1C2431" },
            { backgroundColor: "#F7D046", color: "#1C2431", borderColor: "#F7D046", duration: 0.35, ease: "power2.out", immediateRender: false }, end);
      });
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
}

mkdirSync(new URL("../compositions/", import.meta.url), { recursive: true });
for (const s of scenes) writeFileSync(new URL(`../compositions/${s.id}.html`, import.meta.url), sceneHtml(s));
writeFileSync(new URL("../index.html", import.meta.url), indexHtml());
console.log(`built ${scenes.length} scenes, total ${TOTAL}s`);
