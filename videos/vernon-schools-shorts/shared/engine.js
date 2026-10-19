// Shared motion engine for the Vernon school shorts. Reads SPEC (script.json), TIMING (timing.json) and
// TRANS (scene-boundary shader transitions) and builds ONE paused timeline via HyperShader.
const S = TIMING.scenes;
const TOTAL = TIMING.total;
const tl = HyperShader.init({
  bgColor: "#0b1730",
  accentColor: SPEC.accent,
  scenes: S.map((s) => s.id),
  transitions: TRANS,
});

// deterministic PRNG (seeded)
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const q = (sel, root) => Array.from((root || document).querySelectorAll(sel));
const capStart = (i, j) => S[i].captions[Math.min(j, S[i].captions.length - 1)].start;
const atTime = (i, a, dt) => (a === -1 ? S[i].start : capStart(i, a || 0)) + (dt || 0);
const sceneEnd = (i) => S[i].start + S[i].duration;

function shake(i, t, amp) {
  const cam = document.getElementById(S[i].id + "-cam");
  const a = amp || 14;
  tl.fromTo(cam, { x: 0, y: 0 }, { keyframes: [
    { x: a, y: -a * 0.6, duration: 0.033 }, { x: -a * 0.8, y: a * 0.5, duration: 0.033 },
    { x: a * 0.5, y: a * 0.4, duration: 0.033 }, { x: -a * 0.3, y: -a * 0.2, duration: 0.033 }, { x: 0, y: 0, duration: 0.04 },
  ], immediateRender: false }, t);
}

function burst(el, t, seed, spread) {
  const r = rng(seed);
  q(".pt", el).forEach((p) => {
    const ang = r() * Math.PI * 2, dist = (spread || 520) * (0.35 + r() * 0.75), s = 0.5 + r() * 1.3;
    tl.fromTo(p, { x: 0, y: 0, opacity: 1, scale: s },
      { x: Math.cos(ang) * dist, y: Math.sin(ang) * dist * 0.8 + 120 * r(), opacity: 0, scale: s * 0.4,
        duration: 0.9 + r() * 0.7, ease: "power3.out", immediateRender: false }, t);
  });
}

function odoRoll(root, t, dur) {
  q(".od-col", root).forEach((c, k, all) => {
    const d = +c.dataset.d;
    tl.fromTo(c.querySelector(".od-strip"), { yPercent: 0 },
      { yPercent: -(10 + d) * 5, duration: (dur || 1.3) + (all.length - k) * 0.06, ease: "power3.out" }, t);
  });
}

function drawPaths(paths, t, dur, stagger) {
  paths.forEach((p) => { p.setAttribute("pathLength", "1"); p.style.strokeDasharray = "1"; });
  tl.fromTo(paths, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur || 1, stagger: stagger || 0.12, ease: "power2.inOut" }, t);
}

const popIn = (els, t, stagger, extra) =>
  tl.fromTo(els, { opacity: 0, scale: 0.4, y: 40 },
    Object.assign({ opacity: 1, scale: 1, y: 0, duration: 0.5, stagger: stagger || 0, ease: "back.out(2.2)" }, extra || {}), t);

const A = {
  bg(el, it, i, t) {
    const s0 = Math.max(0, S[i].start - 0.6), d = sceneEnd(i) - s0 + 0.6;
    const dir = it.kb === "out" ? -1 : 1, pan = it.pan == null ? 30 : it.pan;
    tl.fromTo(el.querySelector(".bg-back"), { scale: dir > 0 ? 1.0 : 1.12, x: -pan },
      { scale: dir > 0 ? 1.12 : 1.0, x: pan, duration: d, ease: "none" }, s0);
    const f = el.querySelector(".bg-front");
    if (f) tl.fromTo(f, { scale: dir > 0 ? 1.04 : 1.18, y: 0, x: -pan * 2 },
      { scale: dir > 0 ? 1.2 : 1.04, y: -50, x: pan * 2, duration: d, ease: "none" }, s0);
  },
  card(el, it, i, t) {
    const card = el.querySelector(".card");
    if (it.enter === "up") tl.fromTo(card, { y: 1100, rotation: 6, opacity: 1 }, { y: 0, rotation: it.rot || 0, duration: 0.7, ease: "power4.out" }, t);
    else tl.fromTo(card, { rotationY: -90, opacity: 0, scale: 0.9 }, { rotationY: 0, opacity: 1, scale: 1, rotation: it.rot || 0, duration: 0.85, ease: "back.out(1.3)" }, t);
    tl.fromTo(el.querySelector(".card-img"), { scale: 1.0, x: -20 }, { scale: 1.12, x: 20, duration: Math.max(1, sceneEnd(i) - t), ease: "none" }, t);
    tl.fromTo(el.querySelector(".sweep"), { x: 0 }, { x: 1700, duration: 1.0, ease: "power2.inOut" }, t + 0.7);
    const lab = el.querySelector(".card-label");
    if (lab) popIn(lab, t + 0.55);
  },
  slam(el, it, i, t) {
    tl.fromTo(el.querySelector(".slam-t"), { scale: 2.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.32, ease: "power4.in" }, t);
    tl.fromTo(el.querySelector(".shock"), { scale: 0.2, opacity: 0.95 }, { scale: 3.2, opacity: 0, duration: 0.7, ease: "power2.out", immediateRender: false }, t + 0.32);
    shake(i, t + 0.32, it.shake || 16);
    const sub = el.querySelector(".slam-sub");
    if (sub) tl.fromTo(sub, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, atTime(i, it.subAt == null ? it.at : it.subAt, (it.subDt || 0.5)));
  },
  odo(el, it, i, t) {
    const lab = el.querySelector(".odo-label");
    if (lab) tl.fromTo(lab, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35 }, t);
    tl.fromTo(el.querySelector(".odo-wrap"), { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power4.in" }, t);
    odoRoll(el, t + 0.1, it.dur || 1.4);
    if (it.shake !== false) shake(i, t + 0.35, 10);
    const ul = el.querySelector(".odo-ul");
    if (ul) tl.fromTo(ul, { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, t + (it.dur || 1.4) + 0.2);
  },
  title(el, it, i, t) {
    tl.fromTo(el, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }, t);
    tl.fromTo(q(".ch", el), { rotationX: 90, y: 60, opacity: 0, filter: "blur(12px)" },
      { rotationX: 0, y: 0, opacity: 1, filter: "blur(0px)", duration: 0.55, stagger: 0.03, ease: "power3.out" }, t + 0.2);
    tl.fromTo(el.querySelector(".t-ko span"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, t + 0.6);
  },
  stats(el, it, i, t) {
    tl.fromTo(el, { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, t);
    q(".stat", el).forEach((st, k) => {
      const tt = it.ats ? atTime(i, it.ats[k], it.dts ? it.dts[k] : 0.05) : t + 0.2 + k * 0.5;
      tl.fromTo(st, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35 }, tt);
      odoRoll(st, tt + 0.05, 1.1);
    });
  },
  map(el, it, i, t) {
    tl.fromTo(el, { opacity: 0, scale: 0.85, rotation: 4 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }, t);
    drawPaths(q(".mp-draw", el), t + 0.2, 1.1, 0.1);
    tl.fromTo(q(".mp-lake", el), { fill: "rgba(31,181,201,0)" }, { fill: "rgba(31,181,201,0.4)", duration: 0.6 }, t + 1.0);
    q(".mp-pin", el).forEach((p, k) => {
      tl.fromTo(p, { y: -260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: "bounce.out" }, t + 1.1 + k * 0.15);
      tl.fromTo(p.querySelector(".mp-pulse"), { scale: 1, opacity: 0.9, transformOrigin: "50% 50%" },
        { scale: 3.2, opacity: 0, duration: 0.9, repeat: 3, ease: "power1.out" }, t + 1.7 + k * 0.15);
    });
    const lab = q(".mp-label, .mp-note", el);
    if (lab.length) tl.fromTo(lab, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.15 }, t + 1.5);
  },
  chips(el, it, i, t) {
    const chips = q(".chip", el);
    if (it.ats) chips.forEach((c, k) => popIn(c, atTime(i, it.ats[k], 0.05)));
    else popIn(chips, t, it.stagger || 0.08);
  },
  note(el, it, i, t) {
    tl.fromTo(el, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, t);
  },
  quote(el, it, i, t) {
    tl.fromTo(el, { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, t);
    tl.fromTo(el.querySelector(".q-mark"), { scale: 2.4, rotation: -30, opacity: 0 }, { scale: 1, rotation: 0, opacity: 0.9, duration: 0.5, ease: "back.out(2)" }, t + 0.2);
    tl.fromTo(el.querySelector(".q-text"), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7, ease: "power2.inOut" }, t + 0.3);
    tl.fromTo(el.querySelector(".q-by"), { opacity: 0 }, { opacity: 1, duration: 0.4 }, t + 0.9);
  },
  thumbs(el, it, i, t) {
    tl.fromTo(q(".thumb", el), { x: 700, rotation: 10, opacity: 0 }, { x: 0, rotation: 0, opacity: 1, duration: 0.7, stagger: 0.18, ease: "power4.out" }, t);
  },
  icons(el, it, i, t) {
    const tiles = q(".itile", el);
    tiles.forEach((tile, k) => {
      const tt = it.ats ? atTime(i, it.ats[k], 0.05) : t + k * 0.14;
      tl.fromTo(tile, { opacity: 0, y: 90, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.8)" }, tt);
      tl.fromTo(tile.querySelector(".ic-c"), { rotation: -180, scale: 0 }, { rotation: 0, scale: 1, duration: 0.6, ease: "back.out(1.6)" }, tt + 0.1);
    });
  },
  split(el, it, i, t) {
    q(".sp-card", el).forEach((c, k) => {
      const tt = it.ats ? atTime(i, it.ats[k], 0.05) : t + k * 0.4;
      tl.fromTo(c, { rotationY: -90, opacity: 0 }, { rotationY: 0, opacity: 1, duration: 0.8, ease: "back.out(1.3)" }, tt);
      tl.fromTo(c.querySelector(".sp-ic"), { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2)" }, tt + 0.5);
    });
  },
  checks(el, it, i, t) {
    q(".ck", el).forEach((row, k) => {
      const tt = it.ats ? atTime(i, it.ats[k], 0.05) : t + k * 0.5;
      tl.fromTo(row, { opacity: 0, x: -100 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, tt);
      tl.fromTo(row.querySelector(".ck-path"), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, tt + 0.3);
    });
  },
  stamp(el, it, i, t) {
    tl.fromTo(el.querySelector(".stamp"), { scale: 3, rotation: -30, opacity: 0 }, { scale: 1, rotation: it.rot == null ? -12 : it.rot, opacity: 1, duration: 0.3, ease: "power4.in" }, t);
    shake(i, t + 0.3, 8);
  },
  people(el, it, i, t) {
    tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, t);
    popIn(q(".pp", el), t + 0.15, 0.05);
    const tf = atTime(i, it.fillAt == null ? it.at : it.fillAt, it.fillDt || 0.2);
    tl.fromTo(q(".pp-f svg", el), { fill: "#3a4a6a" }, { fill: "#1fb5c9", duration: 0.3, stagger: 0.09 }, tf);
    tl.fromTo(q(".pp-o svg", el), { fill: "#3a4a6a" }, { fill: "#ffd23f", duration: 0.3 }, tf + 0.9);
    tl.fromTo(el.querySelector(".pp-l"), { opacity: 0 }, { opacity: 1, duration: 0.4 }, tf + 1.0);
  },
  fork(el, it, i, t) {
    popIn(el.querySelector(".fk-root"), t);
    drawPaths(q(".fk", el), t + 0.3, 0.9, 0.15);
    popIn(q(".fk-node", el), t + 1.0, 0.25);
  },
  fan(el, it, i, t) {
    const cards = q(".fan-c", el), n = cards.length, mid = (n - 1) / 2;
    cards.forEach((c, k) => {
      const o = k - mid;
      tl.fromTo(c, { y: 900, rotation: 0, x: 0, opacity: 0 },
        { y: Math.abs(o) * 30, rotation: o * 11, x: o * 120, opacity: 1, duration: 0.8, ease: "back.out(1.2)" }, t + k * 0.09);
    });
  },
  pick(el, it, i, t) {
    const card = el.querySelector(".pk-card");
    tl.fromTo(card, { rotationY: -100, opacity: 0, scale: 0.85 }, { rotationY: 0, opacity: 1, scale: 1, duration: 0.85, ease: "back.out(1.2)" }, t);
    tl.fromTo(el.querySelector(".pk-img"), { scale: 1.0 }, { scale: 1.12, duration: Math.max(1, sceneEnd(i) - t), ease: "none" }, t);
    popIn(el.querySelector(".pk-type"), t + 0.5);
    popIn(el.querySelector(".pk-ic"), t + 0.6);
    tl.fromTo(q(".pk-name, .pk-en", el), { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.45, stagger: 0.1, ease: "power3.out" },
      atTime(i, it.nameAt == null ? 1 : it.nameAt, 0.05));
    tl.fromTo(el.querySelector(".pk-v"), { scale: 2.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "power4.in" },
      atTime(i, it.nameAt == null ? 1 : it.nameAt, 0.35));
    shake(i, atTime(i, it.nameAt == null ? 1 : it.nameAt, 0.65), 10);
  },
  notes(el, it, i, t) {
    drawPaths(q(".nl", el), t, 1.0, 0.08);
    tl.fromTo(q(".nn", el), { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.12, ease: "bounce.out" }, t + 0.4);
  },
  balance(el, it, i, t) {
    popIn(el, t);
    tl.fromTo(el.querySelector(".bl-beam"), { rotation: -9 }, { rotation: 9, duration: 0.55, repeat: 7, yoyo: true, ease: "sine.inOut" }, t + 0.3);
  },
  cta(el, it, i, t) {
    popIn(el.querySelector(".cta-chip"), t);
    tl.fromTo(q(".cta-logo .ch", el), { rotationX: 90, y: 80, opacity: 0, filter: "blur(12px)" },
      { rotationX: 0, y: 0, opacity: 1, filter: "blur(0px)", duration: 0.6, stagger: 0.04, ease: "power3.out" }, t + 0.15);
    tl.fromTo(q(".cta-sub, .cta-cities", el), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, stagger: 0.15 }, t + 0.6);
    const btn = el.querySelector(".cta-btn");
    popIn(btn, t + 0.95);
    const left = TOTAL - (t + 1.5);
    const reps = Math.max(1, Math.floor(left / 0.5) - 1);
    tl.fromTo(btn, { scale: 1 }, { scale: 1.07, duration: 0.5, repeat: reps, yoyo: true, ease: "sine.inOut", immediateRender: false }, t + 1.5);
  },
  particles(el, it, i, t) {
    burst(el, t, 77 + i * 13, it.spread);
  },
};

// background drift (absolute time so it reads as one continuous bed under every scene)
tl.fromTo(".b1", { x: 0, y: 0 }, { x: 260, y: 180, duration: TOTAL, ease: "sine.inOut" }, 0);
tl.fromTo(".b2", { x: 0, y: 0 }, { x: -320, y: -260, duration: TOTAL, ease: "sine.inOut" }, 0);
tl.fromTo(".grid", { y: 0 }, { y: 90, duration: TOTAL, ease: "none" }, 0);

// scene items
SPEC.scenes.forEach((sc, i) => {
  sc.items.forEach((it, k) => {
    const el = document.getElementById(sc.id + "-i" + k);
    if (el && A[it.t]) A[it.t](el, it, i, atTime(i, it.at, it.dt));
  });
  const foot = document.getElementById(sc.id).querySelector(".foot");
  if (foot) tl.fromTo(foot, { opacity: 0 }, { opacity: 1, duration: 0.5 }, S[i].start + 0.4);
});

// captions pop at their own start
S.forEach((s, i) => s.captions.forEach((c, j) => {
  tl.fromTo(document.getElementById("cap-" + i + "-" + j + "-box"), { opacity: 0, scale: 0.9, y: 16 }, { opacity: 1, scale: 1, y: 0, duration: 0.22, ease: "back.out(2)" }, c.start);
}));

// final scene: gentle fade to navy in the last 0.5s (the only exit allowed)
tl.fromTo(document.getElementById(S[S.length - 1].id + "-cam"), { opacity: 1 }, { opacity: 0, duration: 0.45, immediateRender: false }, TOTAL - 0.5);
window.__timelines["main"] = tl;
tl.seek(0);
