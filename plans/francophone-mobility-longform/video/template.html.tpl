<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>프랑코폰 모빌리티 롱폼</title>
    <script src="assets/js/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Pretendard"; src: url("assets/fonts/Pretendard-Medium.woff2") format("woff2"); font-weight: 500; }
      @font-face { font-family: "Pretendard"; src: url("assets/fonts/Pretendard-Bold.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Pretendard"; src: url("assets/fonts/Pretendard-ExtraBold.woff2") format("woff2"); font-weight: 800; }
      @font-face { font-family: "Pretendard"; src: url("assets/fonts/Pretendard-Black.woff2") format("woff2"); font-weight: 900; }
      :root {
        --navy: #0f2742; --ink: #1b2430; --muted: #5d6877; --cream: #f6f2ea; --card: #ffffff;
        --red: #d52b1e; --blue: #1f5fbf; --line: #e2dccf; --gold: #f2b84b;
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--cream); color: var(--ink); font-family: "Pretendard", sans-serif; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--cream); }
      .backdrop { position: absolute; inset: 0; background:
          radial-gradient(1200px 700px at 85% 10%, rgba(31,95,191,0.07), transparent 60%),
          radial-gradient(900px 600px at 5% 95%, rgba(213,43,30,0.06), transparent 60%), var(--cream); }
      .brandmark { position: absolute; right: 64px; top: 48px; font-weight: 800; font-size: 26px; letter-spacing: 0.04em; color: var(--navy); opacity: 0.55; }
      .scene { position: absolute; inset: 0; }
      .scene-inner { position: absolute; inset: 0; }
      .bg-navy { position: absolute; inset: 0; background: radial-gradient(1400px 800px at 70% 20%, #1c3d66, var(--navy)); }
      .face-video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }

      .chapter { position: absolute; left: 96px; top: 70px; font-size: 44px; font-weight: 800; color: var(--navy); display: flex; align-items: center; gap: 22px; }
      .chapter span { font-size: 26px; font-weight: 800; color: #fff; background: var(--red); border-radius: 10px; padding: 6px 14px; }

      /* captions */
      .cap { position: absolute; left: 0; right: 0; bottom: 64px; display: flex; justify-content: center; }
      .cap-text { max-width: 1600px; background: rgba(12, 20, 32, 0.82); color: #fff; font-size: 46px; font-weight: 700; line-height: 1.3;
        padding: 14px 34px; border-radius: 14px; text-align: center; }

      /* S1 */
      .s1-wrap { position: absolute; left: 140px; right: 140px; top: 200px; color: #fff; }
      .s1-kicker { display: inline-block; font-size: 34px; font-weight: 700; color: var(--gold); border: 2px solid rgba(242,184,75,0.6); border-radius: 999px; padding: 10px 26px; }
      .s1-title { margin-top: 42px; display: flex; flex-direction: column; gap: 10px; font-weight: 900; font-size: 104px; line-height: 1.12; }
      .s1-title .l3 { color: var(--gold); }
      .s1-host { margin-top: 56px; display: flex; align-items: center; gap: 22px; font-size: 32px; }
      .s1-host b { display: block; font-weight: 800; }
      .s1-host span { color: rgba(255,255,255,0.7); font-size: 28px; }
      .host-dot { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, var(--red), #ff7a5c); }
      .lower-third { position: absolute; left: 96px; bottom: 200px; background: rgba(15,39,66,0.9); color: #fff; padding: 22px 34px; border-left: 10px solid var(--red); border-radius: 8px; }
      .lt-kicker { font-size: 28px; color: var(--gold); font-weight: 700; }
      .lt-title { font-size: 56px; font-weight: 900; margin-top: 6px; }

      /* S2 */
      .flow { position: absolute; left: 0; right: 0; top: 230px; display: flex; justify-content: center; align-items: center; gap: 30px; }
      .node { width: 330px; height: 250px; background: var(--card); border: 3px solid var(--line); border-radius: 26px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 18px 40px rgba(15,39,66,0.08); }
      .node .ico { font-size: 70px; }
      .node b { font-size: 50px; font-weight: 900; color: var(--navy); }
      .node small { font-size: 28px; color: var(--muted); }
      .node.accent { border-color: var(--red); }
      .node.accent b { color: var(--red); }
      .arrow { width: 110px; height: 8px; background: var(--navy); border-radius: 4px; position: relative; transform-origin: left center; }
      .arrow::after { content: ""; position: absolute; right: -6px; top: -12px; border-left: 22px solid var(--navy); border-top: 16px solid transparent; border-bottom: 16px solid transparent; }
      .def-card { position: absolute; left: 50%; top: 540px; width: 1100px; margin-left: -550px; text-align: center; background: var(--navy); color: #fff; border-radius: 22px; padding: 26px; }
      .def-en { font-size: 36px; color: rgba(255,255,255,0.75); font-weight: 700; }
      .def-ko { font-size: 64px; font-weight: 900; margin-top: 4px; }
      .proof { position: absolute; left: 0; right: 0; top: 770px; display: flex; justify-content: center; align-items: center; gap: 18px; }
      .pill { font-size: 36px; font-weight: 800; padding: 14px 28px; border-radius: 999px; background: var(--card); border: 3px solid var(--line); color: var(--navy); }
      .pill.red { background: var(--red); border-color: var(--red); color: #fff; }
      .pill.blue { background: var(--blue); border-color: var(--blue); color: #fff; }
      .sep { font-size: 40px; color: var(--muted); font-weight: 800; }

      /* S3 */
      .steps { position: absolute; left: 96px; right: 96px; top: 190px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px; }
      .step { background: var(--card); border: 3px solid var(--line); border-radius: 24px; padding: 30px 28px; height: 640px; position: relative; box-shadow: 0 18px 40px rgba(15,39,66,0.08); }
      .step .num { width: 60px; height: 60px; border-radius: 50%; background: var(--navy); color: #fff; font-size: 34px; font-weight: 900; display: flex; align-items: center; justify-content: center; }
      .step h3 { font-size: 48px; font-weight: 900; margin: 20px 0 4px; color: var(--navy); }
      .step p { font-size: 28px; color: var(--muted); margin: 0 0 18px; }
      .big { margin-top: 16px; }
      .big em { display: block; font-style: normal; font-size: 70px; font-weight: 900; color: var(--red); line-height: 1.05; }
      .big small { font-size: 28px; color: var(--muted); font-weight: 700; }
      .tag { position: absolute; left: 24px; right: 24px; bottom: 26px; font-size: 26px; font-weight: 800; text-align: center; padding: 12px; border-radius: 12px; background: #eef2f8; color: var(--navy); }
      .tag.red { background: #fdeceb; color: var(--red); }
      .stamp { position: absolute; right: 150px; top: 60px; font-size: 54px; font-weight: 900; color: var(--red); border: 7px solid var(--red); border-radius: 18px; padding: 8px 30px; transform: rotate(-6deg); background: rgba(255,255,255,0.85); }
      .stamp.blue { color: var(--blue); border-color: var(--blue); }

      /* S4 */
      .plan { position: absolute; left: 140px; right: 140px; top: 290px; height: 200px; display: flex; gap: 14px; }
      .blk { border-radius: 22px; color: #fff; display: flex; flex-direction: column; justify-content: center; padding: 0 34px; position: relative; transform-origin: left center; }
      .blk b { font-size: 50px; font-weight: 900; }
      .blk small { font-size: 28px; opacity: 0.85; font-weight: 700; }
      .blk.lang { flex: 1; background: #6b7f99; }
      .blk.col { flex: 2.2; background: var(--navy); }
      .blk.pgwp { flex: 3; background: var(--red); }
      .badge { position: absolute; right: 24px; top: -30px; background: var(--gold); color: var(--ink); font-size: 30px; font-weight: 900; padding: 8px 20px; border-radius: 999px; }
      .axis { position: absolute; left: 140px; right: 140px; top: 520px; display: flex; justify-content: space-between; font-size: 32px; font-weight: 800; color: var(--muted); border-top: 4px dashed #c9c1b2; padding-top: 16px; }
      .costs { position: absolute; left: 0; right: 0; top: 680px; display: flex; justify-content: center; gap: 26px; }
      .chip { font-size: 40px; font-weight: 800; padding: 16px 34px; border-radius: 999px; background: var(--card); border: 3px solid var(--line); }

      /* S5 */
      .langs { position: absolute; left: 0; right: 0; top: 190px; display: flex; justify-content: center; align-items: center; gap: 24px; flex-wrap: wrap; }
      .lg { font-size: 56px; font-weight: 900; padding: 14px 44px; border-radius: 18px; color: #fff; }
      .lg.en { background: var(--red); } .lg.fr { background: var(--blue); }
      .lg-cap { width: 100%; text-align: center; font-size: 32px; color: var(--muted); font-weight: 800; }
      .prov { position: absolute; left: 160px; right: 160px; top: 420px; display: grid; grid-template-columns: repeat(10, 1fr); gap: 12px; }
      .pv { height: 120px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; color: #fff; }
      .pv.en { background: #a9b3c1; } .pv.fr { background: var(--blue); box-shadow: 0 0 0 6px rgba(31,95,191,0.25); }
      .prov-cap { position: absolute; left: 0; right: 0; top: 560px; text-align: center; font-size: 30px; font-weight: 700; color: var(--muted); display: flex; justify-content: center; align-items: center; gap: 12px; }
      .k { display: inline-block; width: 24px; height: 24px; border-radius: 6px; }
      .k.fr { background: var(--blue); } .k.en { background: #a9b3c1; margin-left: 24px; }
      .targets { position: absolute; left: 50%; width: 1100px; margin-left: -550px; top: 190px; height: 640px; background: var(--card); border-radius: 26px; border: 3px solid var(--line); padding: 34px 60px; }
      .tg-title { font-size: 42px; font-weight: 900; color: var(--navy); text-align: center; }
      .bars { position: absolute; left: 120px; right: 120px; bottom: 40px; top: 140px; display: flex; justify-content: space-around; align-items: flex-end; }
      .bar { width: 200px; height: 100%; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; gap: 8px; }
      .bar .fill { width: 160px; background: var(--blue); border-radius: 14px 14px 0 0; height: 300px; transform-origin: bottom center; }
      .bar b { font-size: 56px; font-weight: 900; color: var(--blue); }
      .bar small { font-size: 32px; color: var(--muted); font-weight: 800; }

      /* S6 */
      .fm-head { position: absolute; left: 96px; top: 170px; }
      .fm-name { font-size: 84px; font-weight: 900; color: var(--blue); }
      .fm-sub { font-size: 36px; color: var(--muted); font-weight: 700; margin-top: 4px; }
      #fmstamp { right: 150px; top: 170px; }
      .checks { position: absolute; left: 96px; top: 380px; width: 900px; margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 22px; }
      .checks li { font-size: 40px; font-weight: 800; background: var(--card); border: 3px solid var(--line); border-radius: 18px; padding: 20px 26px; display: flex; align-items: center; gap: 18px; }
      .checks li small { font-size: 28px; color: var(--muted); font-weight: 700; }
      .checks i { font-style: normal; width: 48px; height: 48px; border-radius: 50%; background: var(--blue); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 30px; flex: none; }
      .vs { position: absolute; right: 96px; top: 400px; width: 780px; display: flex; align-items: center; gap: 18px; }
      .vs-c { flex: 1; border-radius: 22px; padding: 28px; text-align: center; height: 380px; }
      .vs-c h4 { margin: 0 0 14px; font-size: 38px; font-weight: 900; }
      .vs-c p { margin: 6px 0; font-size: 30px; font-weight: 700; }
      .vs-c .money { font-size: 76px; font-weight: 900; margin-top: 24px; }
      .vs-c small { font-size: 24px; font-weight: 700; }
      .vs-c.gray { background: #e7e3da; color: var(--muted); }
      .vs-c.gray .money { text-decoration: line-through; text-decoration-thickness: 6px; }
      .vs-c.blue { background: var(--blue); color: #fff; }
      .vs-mid { font-size: 36px; font-weight: 900; color: var(--muted); }

      /* S7 */
      .ladder { position: absolute; left: 110px; top: 200px; width: 760px; height: 600px; display: flex; align-items: flex-end; gap: 10px; }
      .rung { flex: 1; height: calc(var(--h) * 44px); background: #c9d1dc; border-radius: 10px 10px 4px 4px; display: flex; align-items: flex-start; justify-content: center; padding-top: 8px; font-size: 30px; font-weight: 900; color: #fff; transform-origin: bottom center; }
      .rung.hi { background: var(--blue); }
      .lad-cap { position: absolute; left: 0; right: 0; bottom: -56px; text-align: center; font-size: 30px; color: var(--muted); font-weight: 800; }
      .need { position: absolute; left: 960px; top: 190px; width: 840px; background: var(--card); border: 3px solid var(--line); border-radius: 24px; padding: 26px 36px; }
      .need-t { font-size: 64px; font-weight: 900; color: var(--navy); }
      .need-t em { font-style: normal; color: var(--blue); }
      .need-row { display: flex; gap: 16px; align-items: center; margin-top: 14px; }
      .need-row span { font-size: 34px; font-weight: 800; padding: 10px 24px; border-radius: 12px; }
      .need-row .ok { background: #e6effc; color: var(--blue); }
      .need-row .no { background: #efece6; color: #9a9389; text-decoration: line-through; }
      .need-row small { font-size: 28px; color: var(--muted); font-weight: 700; }
      .tests { position: absolute; left: 960px; top: 520px; display: flex; gap: 18px; }
      .tests span { font-size: 34px; font-weight: 900; color: #fff; background: var(--navy); padding: 12px 26px; border-radius: 12px; }
      .mtl { position: absolute; left: 960px; top: 630px; width: 840px; }
      .pin { font-size: 42px; font-weight: 900; color: var(--red); }
      .year { display: flex; align-items: center; gap: 24px; margin-top: 12px; }
      .yr-bar { flex: 1; height: 26px; background: #e2dccf; border-radius: 13px; overflow: hidden; }
      .yr-fill { height: 100%; width: 100%; background: linear-gradient(90deg, var(--blue), var(--red)); transform-origin: left center; }
      .year b { font-size: 44px; font-weight: 900; color: var(--navy); }
      .gov { margin-top: 14px; font-size: 32px; font-weight: 800; color: var(--blue); }

      /* S8 */
      .fam { position: absolute; left: 0; right: 0; top: 200px; display: flex; justify-content: center; align-items: center; gap: 40px; }
      .fc { width: 620px; height: 440px; background: var(--card); border: 3px solid var(--line); border-radius: 28px; padding: 30px 40px; text-align: center; box-shadow: 0 18px 40px rgba(15,39,66,0.08); }
      .fc.kid { border-color: var(--red); }
      .fico { font-size: 96px; }
      .fc h4 { margin: 8px 0 14px; font-size: 52px; font-weight: 900; color: var(--navy); }
      .fc p { margin: 4px 0; font-size: 36px; font-weight: 700; }
      .fc p b { font-size: 46px; color: var(--red); }
      .fc small { font-size: 26px; color: var(--muted); font-weight: 700; }
      .fplus { font-size: 90px; font-weight: 900; color: var(--muted); }
      .fpath { position: absolute; left: 0; right: 0; top: 720px; display: flex; justify-content: center; align-items: center; gap: 16px; }

      /* S9 / END */
      .s9-wrap { position: absolute; left: 160px; right: 160px; top: 170px; display: flex; flex-direction: column; gap: 26px; }
      .sum { color: #fff; font-size: 52px; font-weight: 900; background: rgba(255,255,255,0.08); border-radius: 20px; padding: 26px 34px; display: flex; align-items: center; gap: 26px; }
      .sum span { font-size: 28px; font-weight: 800; color: var(--navy); background: var(--gold); padding: 6px 16px; border-radius: 10px; flex: none; }
      .sum.alt { background: rgba(31,95,191,0.55); font-size: 46px; }
      .contact { position: absolute; left: 50%; bottom: 200px; transform: translateX(-50%); white-space: nowrap; background: var(--red); color: #fff; font-size: 48px; font-weight: 800; padding: 20px 44px; border-radius: 999px; }
      .contact i { font-style: normal; opacity: 0.6; margin: 0 10px; }
      .endcard { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #fff; gap: 18px; }
      .brand { font-size: 130px; font-weight: 900; letter-spacing: 0.02em; }
      .end-sub { font-size: 40px; font-weight: 700; color: var(--gold); }
      .end-ct { font-size: 48px; font-weight: 800; margin-top: 20px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="/*TOTAL*/">
      <div class="backdrop" id="bd"></div>
      <div class="brandmark">AA Canada</div>
      <!--MEDIA-->
      <!--SLOTS-->
      <!--CAPS-->
    </div>
    <script>
      const T = /*TIMING*/;
      const FACES = /*FACES*/;
      // global time of the first caption in a scene that contains `kw`
      function K(sid, kw, dflt) {
        const s = T[sid];
        for (const c of s.caps) if (c[1].includes(kw)) return s.start + c[0];
        return s.start + (dflt || 0);
      }
      const S = (sid) => T[sid].start;
      const E = (sid) => T[sid].start + T[sid].dur;
      const tl = gsap.timeline({ paused: true });
      const up = (sel, at, extra) => tl.fromTo(sel, { opacity: 0, y: 40 }, Object.assign({ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, extra || {}), at);
      const pop = (sel, at) => tl.fromTo(sel, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, at);
      const count = (sel, to, at, dec) => { const o = { v: 0 }; tl.to(o, { v: to, duration: 1.2, ease: "power2.out", onUpdate: () => { document.querySelector(sel).textContent = dec ? o.v.toFixed(1).replace(/\.0$/, "") : Math.round(o.v); } }, at); };

      // slow ambient drift so the frame never sits fully still
      tl.fromTo("#bd", { scale: 1, xPercent: 0 }, { scale: 1.12, xPercent: -3, duration: /*TOTAL*/, ease: "none" }, 0);
      tl.fromTo(".brandmark", { opacity: 0.45 }, { opacity: 0.7, duration: 4, yoyo: true, repeat: Math.floor(/*TOTAL*/ / 4) - 1, ease: "sine.inOut" }, 0);

      // scene fades
      for (const sid of Object.keys(T)) {
        tl.fromTo("#in-" + sid, { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power1.out" }, S(sid));
        tl.to("#in-" + sid, { opacity: 0, duration: 0.35, ease: "power1.in" }, E(sid) - 0.35);
      }

      // S1
      if (FACES.includes("S1")) {
        up("#s1lt", S("S1") + 0.8);
      } else {
        up("#s1k", S("S1") + 0.4);
        tl.fromTo("#s1t span", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.7, stagger: 0.35, ease: "power3.out" }, S("S1") + 0.7);
        up("#s1h", S("S1") + 2.2);
      }

      // S2
      up("#ch2", S("S2") + 0.2);
      up("#s2a", S("S2") + 0.5);
      tl.fromTo("#s2r1", { scaleX: 0 }, { scaleX: 1, duration: 0.4 }, K("S2", "원칙적으로", 5));
      pop("#s2b", K("S2", "원칙적으로", 5) + 0.3);
      tl.fromTo("#s2r2", { scaleX: 0 }, { scaleX: 1, duration: 0.4 }, K("S2", "원칙적으로", 5) + 0.8);
      up("#s2c", K("S2", "원칙적으로", 5) + 1.1);
      up("#s2def", K("S2", "노동시장", 10));
      tl.fromTo("#s2proof .pill, #s2proof .sep", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.45, stagger: 0.4 }, K("S2", "캐나다 사람", 14));

      // S3
      up("#ch3", S("S3") + 0.2);
      up("#st1", K("S3", "잡뱅크", 4));
      up("#st2", K("S3", "임금도", 14));
      up("#st3", K("S3", "신청비", 19));
      pop("#st3x", K("S3", "돌려받지", 24));
      up("#st4", K("S3", "심사 기간", 27));
      count("#c98", 98, K("S3", "고임금 직종은 평균", 29));
      count("#c82", 82, K("S3", "고임금 직종은 평균", 29) + 0.8);
      pop("#st4x", K("S3", "광고 기간은", 38));
      pop("#s3stamp", K("S3", "이 모든", 42));

      // S4
      up("#ch4", S("S4") + 0.2);
      tl.fromTo("#p1", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.5 }, K("S4", "어학연수", 3));
      tl.fromTo("#p2", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.6 }, K("S4", "어학연수", 3) + 0.8);
      tl.fromTo("#p3", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.6 }, K("S4", "어학연수", 3) + 1.8);
      up("#paxis", K("S4", "어학연수", 3) + 2.4);
      pop("#p3b", K("S4", "필요가 없습니다", 12));
      tl.fromTo(".chip", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, stagger: 0.5 }, K("S4", "다만", 17));

      // S5
      up("#ch5", S("S5") + 0.2);
      tl.fromTo("#s5lang", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6 }, K("S5", "공용어", 4));
      tl.fromTo("#s5prov .pv", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.08 }, K("S5", "퀘벡주를", 8));
      up("#s5pcap", K("S5", "퀘벡주를", 8) + 1.0);
      const tgAt = K("S5", "비율 목표", 22);
      tl.to("#s5lang, #s5prov, #s5pcap", { opacity: 0, duration: 0.4 }, tgAt - 0.5);
      up("#s5tg", tgAt);
      tl.fromTo("#b26", { scaleY: 0 }, { scaleY: 9 / 10.5, duration: 1.0, ease: "power2.out" }, tgAt + 0.5);
      tl.fromTo("#b27", { scaleY: 0 }, { scaleY: 9.5 / 10.5, duration: 1.0, ease: "power2.out" }, tgAt + 1.3);
      tl.fromTo("#b28", { scaleY: 0 }, { scaleY: 1, duration: 1.0, ease: "power2.out" }, tgAt + 2.1);
      count("#t26", 9, tgAt + 0.5, true); count("#t27", 9.5, tgAt + 1.3, true); count("#t28", 10.5, tgAt + 2.1, true);

      // S6
      up("#ch6", S("S6") + 0.2);
      up("#fmh", S("S6") + 0.6);
      pop("#fmstamp", K("S6", "LMIA 없이", 6));
      up("#ck1", K("S6", "조건은", 11));
      up("#ck2", K("S6", "직종 제한", 17));
      up("#ck3", K("S6", "구인광고도", 23));
      up("#fmvs", K("S6", "구인광고도", 23) + 0.6);
      up("#ck4", K("S6", "불어를 쓰지", 32));

      // S7
      up("#ch7", S("S7") + 0.2);
      tl.fromTo("#lad .rung", { scaleY: 0 }, { scaleY: 1, duration: 0.4, stagger: 0.06, ease: "power2.out" }, K("S7", "12단계", 3));
      up("#lad .lad-cap", K("S7", "12단계", 3) + 0.6);
      up("#need", K("S7", "두 영역", 8));
      tl.fromTo("#r5", { scale: 1 }, { scale: 1.12, duration: 0.3, yoyo: true, repeat: 3 }, K("S7", "두 영역", 8) + 0.2);
      up("#tests", K("S7", "TEF", 15));
      up("#mtl", K("S7", "몬트리올", 22));
      tl.fromTo("#yrf", { scaleX: 0 }, { scaleX: 1, duration: 1.4, ease: "power1.inOut" }, K("S7", "몬트리올", 22) + 0.5);
      pop("#gov", K("S7", "퀘벡 정부", 29));

      // S8
      up("#ch8", S("S8") + 0.2);
      up("#fcp", K("S8", "부모님이", 4));
      pop("#fplus", K("S8", "부모님이", 4) + 0.6);
      up("#fck", K("S8", "동반 자녀", 6));
      tl.fromTo("#fpath .pill, #fpath .sep", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.45, stagger: 0.35 }, K("S8", "1년 뒤", 18));

      // S9
      if (!FACES.includes("S9")) {
        up("#s9a", S("S9") + 0.5);
        up("#s9b", K("S9", "몬트리올에서", 6));
        up("#s9c", K("S9", "영주권", 13));
      }
      up("#s9ct", K("S9", "AA Canada", 17));

      // END
      tl.fromTo("#endc > *", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, stagger: 0.25 }, S("END") + 0.3);

      // captions: soft fade-in of each caption's text
      document.querySelectorAll(".cap").forEach((el) => {
        const a = parseFloat(el.dataset.start);
        tl.fromTo(el.querySelector(".cap-text"), { opacity: 0 }, { opacity: 1, duration: 0.15 }, a);
      });

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
