// Shared EMSB runtime: turns data-a / data-t attributes (written by build.mjs, absolute seconds)
// into ONE paused GSAP timeline. Waits for Black Han Sans + Noto Sans KR before registering.
(function () {
  var root = document.querySelector("[data-composition-id]");
  var id = root.getAttribute("data-composition-id");
  var fmt = function (v, dec) {
    return dec ? v.toFixed(dec) : Math.round(v).toLocaleString("en-US");
  };
  var KB = {
    in: [{ scale: 1.0 }, { scale: 1.1 }],
    out: [{ scale: 1.12 }, { scale: 1.0 }],
    left: [{ scale: 1.1, xPercent: 1.5 }, { scale: 1.1, xPercent: -1.5 }],
    right: [{ scale: 1.1, xPercent: -1.5 }, { scale: 1.1, xPercent: 1.5 }],
    up: [{ scale: 1.1, yPercent: 1.5 }, { scale: 1.1, yPercent: -1.5 }],
  };

  function build() {
    var tl = gsap.timeline({ paused: true });
    document.querySelectorAll("[data-a]").forEach(function (el) {
      var t = parseFloat(el.dataset.t || "0");
      var d = el.dataset.d ? parseFloat(el.dataset.d) : null;
      switch (el.dataset.a) {
        case "rise": tl.fromTo(el, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: d || 0.6, ease: "power3.out" }, t); break;
        case "drop": tl.fromTo(el, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: d || 0.6, ease: "power3.out" }, t); break;
        case "pop": tl.fromTo(el, { opacity: 0, scale: 0.82 }, { opacity: 1, scale: 1, duration: d || 0.55, ease: "back.out(1.7)" }, t); break;
        case "fade": tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: d || 0.5, ease: "none" }, t); break;
        case "left": tl.fromTo(el, { opacity: 0, x: -70 }, { opacity: 1, x: 0, duration: d || 0.6, ease: "power3.out" }, t); break;
        case "right": tl.fromTo(el, { opacity: 0, x: 70 }, { opacity: 1, x: 0, duration: d || 0.6, ease: "power3.out" }, t); break;
        case "wipe": tl.fromTo(el, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: d || 0.8, ease: "power2.inOut" }, t); break;
        case "cap": tl.fromTo(el, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.22, ease: "power2.out" }, t); break;
        case "drift": tl.fromTo(el, { scale: 1, x: 0 }, { scale: 1.015, x: -8, duration: d, ease: "none" }, t); break;
        case "float": tl.fromTo(el, { x: 0, y: 0 }, { x: 60, y: -40, duration: d, ease: "sine.inOut" }, t); break;
        case "kb": {
          var k = KB[el.dataset.kb || "in"];
          tl.fromTo(el, k[0], Object.assign({ duration: d, ease: "none" }, k[1]), t);
          break;
        }
        case "count": {
          var to = parseFloat(el.dataset.to), dec = parseInt(el.dataset.dec || "0", 10), o = { v: 0 };
          el.textContent = fmt(0, dec);
          tl.to(o, { v: to, duration: d || 1.3, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v, dec); } }, t);
          break;
        }
        case "pulse": tl.fromTo(el, { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(2)" }, t); break;
      }
      if (el.dataset.out) tl.to(el, { opacity: 0, duration: 0.4, ease: "power1.in" }, parseFloat(el.dataset.out));
    });
    window.__timelines[id] = tl;
  }

  var faces = ['400 40px "Black Han Sans"', '400 40px "Noto Sans KR"', '700 40px "Noto Sans KR"', '900 40px "Noto Sans KR"'];
  Promise.all(faces.map(function (f) { return document.fonts.load(f, "가A1"); })).then(function () {
    var ok = faces.every(function (f) { return document.fonts.check(f, "가A1"); });
    if (!ok) console.error("[emsb] fonts failed to load: " + faces.join(", "));
    root.setAttribute("data-fonts-ready", ok ? "1" : "0");
    build();
  });
})();
