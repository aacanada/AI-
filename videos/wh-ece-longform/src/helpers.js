      const H = (function () {
        const fmtNum = (v, o) => {
          o = o || {};
          const d = o.dec || 0;
          let s = d ? v.toFixed(d) : Math.round(v).toString();
          if (o.comma) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
          return (o.pre || "") + s + (o.suf || "");
        };
        // schematic Canada map (concept diagram): province tiles in a 1600x430 box. returns city coords
        const CANADA = {
          tiles: [["BC", 0, 250, 40], ["AB", 258, 150, 30], ["SK", 416, 140, 30], ["MB", 564, 150, 30], ["ON", 722, 330, 70], ["QC", 1060, 320, 0], ["대서양", 1388, 212, 170]],
          city: { 밴쿠버: [70, 360], 캘거리: [335, 310], 토론토: [960, 385], 몬트리올: [1250, 345] },
          build(el, opts) {
            opts = opts || {};
            let h = '<svg viewBox="0 0 1600 430" width="1600" height="430" style="position:absolute;left:0;top:0;overflow:visible">';
            this.tiles.forEach(([n, x, w, t], i) => {
                const bc = n === "BC" && opts.bc;
                h += '<g class="tile tile-' + i + '"><rect x="' + x + '" y="' + t + '" width="' + w + '" height="' + (410 - t) + '" rx="22" fill="' + (bc ? "#c8102e" : "#efe3cf") + '" stroke="#fffdf8" stroke-width="4"/>' +
                  '<text x="' + (x + w / 2) + '" y="' + (t + 60) + '" text-anchor="middle" font-family="Pretendard" font-size="40" font-weight="900" fill="' + (bc ? "#fff" : "#a8977f") + '">' + n + "</text></g>";
            });
            h += "</svg>";
            el.insertAdjacentHTML("beforeend", h);
          },
        };
        return {
          canada: CANADA,
          // count-up number (seek-safe proxy, text written in onUpdate)
          count(tl, el, from, to, t, d, o) {
            const st = { v: from };
            el.textContent = fmtNum(from, o);
            tl.fromTo(st, { v: from }, { v: to, duration: d || 1.2, ease: "power2.out", onUpdate: () => (el.textContent = fmtNum(st.v, o)) }, t);
            tl.fromTo(el, { scale: 0.7 }, { scale: 1, duration: d || 1.2, ease: "power2.out" }, t);
          },
          pop(tl, els, t, o) {
            o = o || {};
            tl.fromTo(els, { opacity: 0, scale: o.from || 0.6 }, { opacity: 1, scale: 1, duration: o.d || 0.5, ease: o.ease || "back.out(1.8)", stagger: o.stagger || 0 }, t);
          },
          rise(tl, els, t, o) {
            o = o || {};
            tl.fromTo(els, { opacity: 0, y: o.y || 40 }, { opacity: 1, y: 0, duration: o.d || 0.55, ease: o.ease || "power3.out", stagger: o.stagger || 0 }, t);
          },
          slideX(tl, els, t, o) {
            o = o || {};
            tl.fromTo(els, { opacity: 0, x: o.x || -80 }, { opacity: 1, x: 0, duration: o.d || 0.6, ease: o.ease || "power3.out", stagger: o.stagger || 0 }, t);
          },
          out(tl, els, t, o) {
            o = o || {};
            tl.fromTo(els, { opacity: 1, y: 0 }, { opacity: 0, y: o.y == null ? -30 : o.y, duration: o.d || 0.4, ease: "power2.in", immediateRender: false, stagger: o.stagger || 0 }, t);
          },
          fadeOut(tl, els, t, d) {
            tl.fromTo(els, { opacity: 1 }, { opacity: 0, duration: d || 0.4, ease: "power1.in", immediateRender: false }, t);
          },
          // marker sweep behind text: element .hl > .hl-bg
          mark(tl, el, t, d) {
            tl.fromTo(el, { scaleX: 0 }, { scaleX: 1, duration: d || 0.5, ease: "power2.inOut" }, t);
          },
          growX(tl, el, t, d, to) {
            tl.fromTo(el, { scaleX: 0 }, { scaleX: to == null ? 1 : to, duration: d || 1, ease: "power3.out" }, t);
          },
          growY(tl, el, t, d) {
            tl.fromTo(el, { scaleY: 0 }, { scaleY: 1, duration: d || 1, ease: "power3.out" }, t);
          },
          stamp(tl, el, t) {
            tl.fromTo(el, { opacity: 0, scale: 2.2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.42, ease: "back.out(2.2)" }, t);
          },
          // slow ambient breathing, finite repeats within scene duration
          breathe(tl, els, D, o) {
            o = o || {};
            const per = o.per || 3;
            const n = Math.max(1, Math.floor(D / per) - 1);
            tl.fromTo(els, { y: 0, rotation: 0 }, { y: o.y || -14, rotation: o.r || 0, duration: per / 2, ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, 0.1);
          },
          // camera move on a capture: el is the inner image wrapper
          cam(tl, el, t, d, s, x, y) {
            tl.to(el, { scale: s, x: x, y: y, duration: d, ease: "power2.inOut" }, t);
          },
          // capture camera: move/zoom a .shot so a highlight band [x0,y0,x1,y1] (native px) is centred
          camTo(tl, shot, band, natH, s, t, d) {
            const k = 716 / 538, W = 716, HS = 520;
            if (!s) s = Math.max(1.12, Math.min(1.6, (0.94 * 538) / (band[2] - band[0])));
            const cx = ((band[0] + band[2]) / 2) * k, cy = ((band[1] + band[3]) / 2) * k;
            let x = W / 2 - cx * s, y = HS / 2 - cy * s;
            x = Math.min(0, Math.max(W - W * s, x));
            y = Math.min(0, Math.max(Math.min(0, HS - natH * k * s), y));
            const prev = shot.__cam || { scale: 1, x: 0, y: 0 };
            tl.fromTo(shot, { scale: prev.scale, x: prev.x, y: prev.y }, { scale: s, x: x, y: y, duration: d || 1.6, ease: "power2.inOut", immediateRender: !shot.__cam }, t);
            shot.__cam = { scale: s, x: x, y: y };
          },
          // red ring drawn around a highlight band inside a .shot
          ring(tl, shot, band, t) {
            const k = 716 / 538;
            const r = document.createElement("div");
            r.className = "ring";
            r.style.left = band[0] * k - 10 + "px";
            r.style.top = band[1] * k - 8 + "px";
            r.style.width = (band[2] - band[0]) * k + 20 + "px";
            r.style.height = (band[3] - band[1]) * k + 16 + "px";
            shot.appendChild(r);
            tl.fromTo(r, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, t);
            return r;
          },
          draw(tl, path, t, d, len) {
            try { len = Math.ceil(path.getTotalLength()) + 4 || len; } catch (e) {}
            tl.fromTo(path, { opacity: 0 }, { opacity: 1, duration: 0.05 }, t);
            tl.fromTo(path, { strokeDasharray: len + " " + len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: d || 1, ease: "power2.inOut" }, t);
          },
          sceneIn(tl, root) {
            const k = root.querySelector(".kicker");
            if (k) {
              tl.fromTo(k.querySelector(".k-num"), { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 0.05);
              tl.fromTo(k.querySelector(".k-title"), { opacity: 0, x: -20, clipPath: "inset(0 100% 0 0)" }, { opacity: 1, x: 0, clipPath: "inset(0 0% 0 0)", duration: 0.7, ease: "power3.out" }, 0.18);
            }
          },
          sceneOut(tl, root, D) {
            const st = root.querySelector(".stage");
            if (st) tl.fromTo(st, { opacity: 1 }, { opacity: 0, duration: 0.35, ease: "power1.in", immediateRender: false }, D - 0.4);
          },
        };
      })();
