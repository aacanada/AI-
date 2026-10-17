// Shared motion kit for AA Canada HyperFrames videos (seek-safe: everything lives on the one paused timeline).
// Usage (after HyperShader.init):  const K = Kit(tl, { W: 1080, H: 1920, total: TOTAL });
function Kit(tl, o) {
  const W = o.W, H = o.H, TOTAL = o.total;
  const K = {};
  K.pop = (sel, t, extra) => tl.fromTo(sel, { opacity: 0, y: 40, scale: 0.9 },
    Object.assign({ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, extra || {}), t);
  K.out = (sel, t, extra) => tl.to(sel, Object.assign({ opacity: 0, y: -30, scale: 0.94, duration: 0.3, ease: "power2.in" }, extra || {}), t);
  K.kin = (sel, t, stg) => tl.fromTo(sel, { opacity: 0, rotationX: 90, y: 60, filter: "blur(12px)" },
    { opacity: 1, rotationX: 0, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out", stagger: stg || 0.03 }, t);
  K.sweep = (sel, t, d) => tl.fromTo(sel, { x: -600, rotation: 25 }, { x: W + 600, rotation: 25, duration: d || 1.0, ease: "power2.inOut" }, t);
  K.ring = (sel, t) => tl.fromTo(sel, { opacity: 1, scale: 0 }, { opacity: 0, scale: 3, duration: 0.75, ease: "power2.out" }, t);
  K.draw = (sel, t, d, extra) => tl.fromTo(sel, { strokeDashoffset: 1 }, Object.assign({ strokeDashoffset: 0, duration: d || 0.5, ease: "power2.inOut" }, extra || {}), t);
  K.fnIn = (sel, t) => tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: 0.4 }, t);
  K.shake = (sel, t, a) => {
    a = a || 8;
    [[a, -a * 0.7], [-a * 0.85, a * 0.6], [a * 0.6, a * 0.8], [-a * 0.4, -a * 0.4], [0, 0]]
      .forEach((p, k) => tl.to(sel, { x: p[0], y: p[1], duration: 1 / 30, ease: "none" }, t + k / 30));
  };
  K.slam = (sel, t, from) => tl.fromTo(sel, { opacity: 0, scale: from || 2.4, rotationX: -40 },
    { opacity: 1, scale: 1, rotationX: 0, duration: 0.3, ease: "power4.in" }, t);              // lands at t + 0.3
  K.stamp = (sel, t, rot) => tl.fromTo(sel, { opacity: 0, scale: 3, rotation: (rot || -12) - 18 },
    { opacity: 1, scale: 1, rotation: rot || -12, duration: 0.28, ease: "power4.in" }, t);      // lands at t + 0.28
  K.flip = (sel, t, extra) => tl.fromTo(sel, { rotationY: -90, opacity: 0, x: -120 },
    Object.assign({ rotationY: 0, opacity: 1, x: 0, duration: 0.7, ease: "back.out(1.3)" }, extra || {}), t);
  // odometer column: element .strip of 20 digits (0-9,0-9) with cell height h
  K.roll = (sel, from, to, t, d, h) => tl.fromTo(sel, { y: -from * h }, { y: -to * h, duration: d, ease: "power3.out" }, t);
  // count-up on a text node
  K.count = (sel, a, b, t, d, fmt) => {
    const el = document.querySelector(sel), st = { v: a };
    fmt = fmt || ((v) => Math.round(v).toLocaleString("en-US"));
    tl.fromTo(st, { v: a }, { v: b, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = fmt(st.v); } }, t);
  };
  K.pulse = (sel, t, until, period) => {
    period = period || 1.0;
    const n = Math.max(1, Math.floor((until - t) / period));
    tl.to(sel, { scale: 1.06, duration: period / 2, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut" }, t);
  };

  // ---------- deterministic particles (seeded PRNG, drawn from timeline time) ----------
  const FX = document.getElementById("fx"), g = FX.getContext("2d");
  function rng(a) { return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  K.rng = rng;
  const GOLD = ["#ffc83d", "#ffe08a", "#ffb000", "#ffffff"];
  const SYS = [];
  K.burst = (t0, x, y, p) => {
    p = p || {}; const r = rng(p.seed || 7), cols = p.colors || GOLD, ps = [];
    for (let k = 0; k < Math.min(120, p.n || 90); k++) {
      const a = p.cone ? -Math.PI / 2 + (r() - 0.5) * p.cone : r() * Math.PI * 2, sp = (p.sp || 1100) * (0.3 + r() * 0.8);
      ps.push({ vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, s: (p.size || 9) * (0.5 + r()), c: cols[k % cols.length], l: (p.life || 1.2) * (0.55 + r() * 0.45), sq: r() < 0.5, rot: r() * 6 });
    }
    SYS.push({ t0, x, y, ps, grav: p.grav == null ? 1500 : p.grav, drag: p.drag || 2.4, kind: "burst" });
  };
  K.rain = (t0, t1, n, seed) => {
    const r = rng(seed), ps = [];
    for (let k = 0; k < Math.min(120, n); k++) ps.push({ x: r() * W, y0: H * 0.22 + r() * H * 0.2, d: r() * Math.max(0.2, t1 - t0 - 0.8), v: 140 + r() * 160, s: 4 + r() * 7, w: r() * 6, c: GOLD[k % 4] });
    SYS.push({ t0, t1, ps, kind: "rain" });
  };
  function drawFx(t) {
    g.clearRect(0, 0, W, H);
    for (const s of SYS) {
      if (s.kind === "burst") {
        const dt = t - s.t0; if (dt < 0 || dt > 2) continue;
        const k = (1 - Math.exp(-s.drag * dt)) / s.drag;
        for (const p of s.ps) {
          if (dt > p.l) continue;
          const x = s.x + p.vx * k, y = s.y + p.vy * k + 0.5 * s.grav * dt * dt * 0.6, a = 1 - dt / p.l, sz = p.s * (0.4 + 0.6 * a);
          g.globalAlpha = a; g.fillStyle = p.c;
          if (p.sq) { g.save(); g.translate(x, y); g.rotate(p.rot + dt * 6); g.fillRect(-sz / 2, -sz / 4, sz, sz / 2); g.restore(); }
          else { g.beginPath(); g.arc(x, y, sz / 2, 0, 6.2832); g.fill(); }
        }
      } else {
        const dt = t - s.t0; if (dt < 0 || t > s.t1) continue;
        for (const p of s.ps) {
          const lt = dt - p.d; if (lt < 0) continue;
          const a = Math.min(1, lt * 2.5) * Math.max(0, Math.min(1, (s.t1 - t) * 3));
          g.globalAlpha = a * 0.85; g.fillStyle = p.c; g.beginPath();
          g.arc(p.x + Math.sin(lt * 2 + p.w) * 18, p.y0 + p.v * lt, p.s / 2, 0, 6.2832); g.fill();
        }
      }
    }
    g.globalAlpha = 1;
  }
  K.finish = () => {
    const FXP = { t: 0 };
    tl.fromTo(FXP, { t: 0 }, { t: TOTAL, duration: TOTAL, ease: "none", onUpdate: () => drawFx(FXP.t) }, 0);
  };
  // global drift layers
  K.drift = () => {
    tl.fromTo(".mesh", { x: -60, y: 0 }, { x: 60, y: -160, duration: TOTAL, ease: "none" }, 0);
    tl.fromTo(".gridl", { y: 0 }, { y: -360, duration: TOTAL, ease: "none" }, 0);
    document.querySelectorAll(".bk").forEach((el) => tl.fromTo(el, { y: 0 }, { y: -520 * parseFloat(el.dataset.sp), duration: TOTAL, ease: "none" }, 0));
    document.querySelectorAll(".spd").forEach((el) => tl.fromTo(el, { x: 0 }, { x: -parseFloat(el.dataset.sp) * TOTAL * 60, duration: TOTAL, ease: "none" }, 0));
  };
  return K;
}
