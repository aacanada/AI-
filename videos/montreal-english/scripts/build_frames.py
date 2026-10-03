# Frames 03-07 of the Montreal short (frames 01-02 were hand-built; edit their HTML directly).
# Cues come from audio_meta.json word timings via W(frame, word-prefix).
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = ROOT + "/compositions/frames"
HEAD = open(os.path.join(ROOT, "..", "..", ".claude/skills/aa-shorts/scripts/frame_head.html")).read()
META = {v["frame"]: v for v in json.load(open(ROOT + "/audio_meta.json"))["voices"]}

def W(frame, prefix, nth=0, off=0.0):
    """Start time of the nth word in `frame` starting with `prefix`, plus offset."""
    hits = [w for w in META[frame]["words"] if w["text"].startswith(prefix)]
    return round(max(0.0, hits[nth]["start"] + off), 2)

BASE_CSS = """
    #root { position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; font-family:"Pretendard",sans-serif; color:#111; }
    .bg { position:absolute; inset:0; background:#fdfae7; }
    .sh-stage { position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:50% 0; transform:translateY(170px) scale(0.85); }
    .eyebrow { position:absolute; left:80px; top:250px; display:flex; align-items:center; gap:20px; font-size:40px; font-weight:700; color:#1e2bfa; letter-spacing:.04em; }
    .eyebrow i { display:block; width:60px; height:5px; border-radius:3px; background:#1e2bfa; }
    .h1 { position:absolute; left:80px; right:80px; font-size:96px; font-weight:800; line-height:1.15; letter-spacing:-.03em; }
    .h1 em { font-style:normal; color:#1e2bfa; }
    .card { position:absolute; background:rgba(30,43,250,0.04); border:1.5px solid rgba(30,43,250,0.2); border-radius:14px; }
    .pill { position:absolute; padding:20px 40px; border-radius:100px; font-size:44px; font-weight:700; white-space:nowrap; }
    .pill.soft { background:rgba(30,43,250,0.08); color:#1e2bfa; }
    .pill.solid { background:#1e2bfa; color:#fdfae7; }
    .num { font-variant-numeric:tabular-nums; }
"""

def frame(fid, frame_no, css, html, js):
    dur = META[frame_no]["duration_s"]
    n = fid[:2]
    doc = f"""<template>
{HEAD}
{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{fid}" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
    <div id="f{n}-bg" class="bg clip" data-start="0" data-duration="{dur}" data-track-index="0"></div>
    <div class="sh-stage" id="f{n}-stage">
{html}
    </div>
  </div>
  <script>
    (function(){{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);
      const count = (id, to, at, d, fmt) => {{
        const el = $(id), st = {{ v: 0 }};
        tl.to(st, {{ v: to, duration: d, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(Math.round(st.v)); }} }}, at);
      }};
{js}
      window.__timelines["{fid}"] = tl;
    }})();
  </script>
</template>
"""
    open(os.path.join(OUT, fid + ".html"), "w").write(doc)

# ---------- Frame 3 — 수업 중 친구들과 100% 영어 ----------
frame("03-classroom", 3, """
    .f3-title { top:320px; }
    .f3-panel { top:500px; width:440px; height:400px; }
    .f3-kr { left:80px; } .f3-ca { left:560px; border-color:#1e2bfa; border-width:3px; background:rgba(30,43,250,0.06); }
    .f3-ptag { position:absolute; left:24px; top:20px; font-size:36px; font-weight:800; }
    .f3-ca .f3-ptag { color:#1e2bfa; }
    .f3-e { position:absolute; font-size:72px; line-height:1; }
    .f3-svg { position:absolute; left:0; top:0; width:440px; height:400px; }
    .f3-svg line { stroke-width:5; stroke-linecap:round; }
    .f3-cap { position:absolute; left:0; right:0; bottom:18px; text-align:center; font-size:32px; font-weight:700; color:#6b6b6b; }
    .f3-b { position:absolute; padding:10px 18px; background:#fff; border:2px solid rgba(30,43,250,0.3); border-radius:20px; font-size:28px; font-weight:800; color:#1e2bfa; white-space:nowrap; }
    .f3-chips { position:absolute; left:80px; right:80px; top:940px; display:flex; gap:20px; }
    .f3-chips .pill { position:relative; padding:18px 34px; font-size:42px; }
    .f3-card { left:80px; right:80px; top:1070px; height:330px; padding:34px 56px; }
    .f3-lab { font-size:46px; font-weight:700; color:#6b6b6b; }
    .f3-stat { display:flex; align-items:baseline; gap:24px; margin-top:30px; }
    .f3-n { font-size:190px; font-weight:900; color:#1e2bfa; line-height:1; letter-spacing:-.04em; }
    .f3-en { font-size:58px; font-weight:800; }
    .f3-key { left:80px; right:80px; top:1440px; text-align:center; font-size:52px; padding:24px 40px; }
""", """
      <div class="eyebrow" id="f3-eye"><i></i>근거 ① 수업 시간</div>
      <div class="h1 f3-title" id="f3-title">캐나다 수업 = <em>대화</em></div>
      <div class="card f3-panel f3-kr" id="f3-kr">
        <div class="f3-ptag">🇰🇷 한국 교실</div>
        <svg class="f3-svg" viewBox="0 0 440 400">
          <line x1="220" y1="170" x2="90" y2="255" stroke="#c9c9d6"/>
          <line x1="220" y1="170" x2="220" y2="255" stroke="#c9c9d6"/>
          <line x1="220" y1="170" x2="350" y2="255" stroke="#c9c9d6"/>
        </svg>
        <div class="f3-e" style="left:184px; top:88px">🧑‍🏫</div>
        <div class="f3-e" style="left:54px; top:260px; font-size:60px">🧒</div>
        <div class="f3-e" style="left:190px; top:260px; font-size:60px">👧</div>
        <div class="f3-e" style="left:320px; top:260px; font-size:60px">👦</div>
        <div class="f3-cap">선생님 설명 듣기</div>
      </div>
      <div class="card f3-panel f3-ca" id="f3-ca">
        <div class="f3-ptag">🇨🇦 캐나다 교실</div>
        <svg class="f3-svg" viewBox="0 0 440 400" id="f3-net">
          <line x1="110" y1="150" x2="330" y2="150" stroke="#1e2bfa"/>
          <line x1="110" y1="150" x2="110" y2="290" stroke="#1e2bfa"/>
          <line x1="330" y1="150" x2="330" y2="290" stroke="#1e2bfa"/>
          <line x1="110" y1="290" x2="330" y2="290" stroke="#1e2bfa"/>
          <line x1="110" y1="150" x2="330" y2="290" stroke="#1e2bfa"/>
          <line x1="330" y1="150" x2="110" y2="290" stroke="#1e2bfa"/>
        </svg>
        <div class="f3-e" style="left:74px; top:114px">🧒</div>
        <div class="f3-e" style="left:294px; top:114px">👧</div>
        <div class="f3-e" style="left:74px; top:254px">👦</div>
        <div class="f3-e" style="left:294px; top:254px">🧑</div>
        <div class="f3-b" id="f3-b1" style="left:110px; top:62px">What do you think?</div>
        <div class="f3-b" id="f3-b2" style="left:150px; top:200px">I agree!</div>
        <div class="f3-b" id="f3-b3" style="left:120px; top:335px">Let's try this!</div>
      </div>
      <div class="f3-chips">
        <div class="pill soft" id="f3-c1">👥 짝 활동</div>
        <div class="pill soft" id="f3-c2">💬 모둠 토론</div>
        <div class="pill soft" id="f3-c3">🎤 발표</div>
      </div>
      <div class="card f3-card" id="f3-card">
        <div class="f3-lab">수업 중 친구들과의 소통</div>
        <div class="f3-stat"><span class="f3-n num" id="f3-n">0%</span><span class="f3-en" id="f3-en">English</span></div>
      </div>
      <div class="pill solid f3-key" id="f3-key">🔑 이게 영어가 느는 핵심</div>
""", f"""
      tl.fromTo("#f3-eye", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, 0.0);
      tl.fromTo("#f3-title", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 0.15);
      tl.fromTo("#f3-kr", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {W(3,"한국처럼",0,-0.1)});
      tl.fromTo("#f3-ca", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {W(3,"아니에요")});
      tl.to("#f3-kr", {{opacity:0.45, duration:0.4}}, {W(3,"아니에요",0,0.3)});
      tl.fromTo("#f3-c1", {{opacity:0, y:30, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.35, ease:"back.out(1.8)"}}, {W(3,"짝")});
      tl.fromTo("#f3-c2", {{opacity:0, y:30, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.35, ease:"back.out(1.8)"}}, {W(3,"모둠")});
      tl.fromTo("#f3-c3", {{opacity:0, y:30, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.35, ease:"back.out(1.8)"}}, {W(3,"발표")});
      const pop = (id, at) => tl.fromTo(id, {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)", transformOrigin:"50% 100%"}}, at);
      pop("#f3-b1", {W(3,"수업",1)}); pop("#f3-b2", {W(3,"친구들과")}); pop("#f3-b3", {W(3,"이야기해야")});
      tl.fromTo("#f3-card", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {W(3,"학교에서는")});
      count("f3-n", 100, {W(3,"100%",0,-0.2)}, 0.9, (n) => n + "%");
      tl.fromTo("#f3-n", {{scale:0.6}}, {{scale:1, duration:0.9, ease:"power2.out", transformOrigin:"0% 80%"}}, {W(3,"100%",0,-0.2)});
      tl.fromTo("#f3-en", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:0.4, ease:"power2.out"}}, {W(3,"영어예요")});
      tl.fromTo("#f3-key", {{opacity:0, y:40, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.8)"}}, {W(3,"바로")});
      tl.to("#f3-key", {{scale:1.05, duration:0.25, ease:"power2.out"}}, {W(3,"핵심입니다")});
      tl.to("#f3-key", {{scale:1, duration:0.35, ease:"power2.inOut"}}, {W(3,"핵심입니다",0,0.25)});
""")

# ---------- Frame 4 — 수업도 80% 영어 ----------
frame("04-timetable", 4, """
    .f4-title { top:320px; }
    .f4-wrap { position:absolute; left:110px; top:500px; width:860px; height:997px; border-radius:14px; overflow:hidden; border:1.5px solid rgba(30,43,250,0.2); background:#fff; }
    .f4-img { position:absolute; left:0; top:0; width:860px; height:997px; transform-origin:50% 100%; }
    .f4-call { position:absolute; left:470px; top:1310px; padding:20px 36px; border-radius:100px; background:#dc2626; color:#fff; font-size:46px; font-weight:800; white-space:nowrap; }
    .f4-res { left:80px; right:80px; top:540px; height:580px; padding:56px; background:#fdfae7; }
    .f4-lab { font-size:52px; font-weight:700; color:#6b6b6b; }
    .f4-n { margin-top:40px; font-size:240px; font-weight:900; color:#1e2bfa; line-height:1.05; letter-spacing:-.04em; }
    .f4-track { position:relative; height:44px; border-radius:6px; background:rgba(30,43,250,0.08); margin-top:26px; overflow:hidden; }
    .f4-fill { position:absolute; left:0; top:0; bottom:0; width:80%; background:#1e2bfa; border-radius:6px; transform-origin:0 50%; }
    .f4-fr { position:absolute; right:0; top:0; bottom:0; width:20%; display:flex; align-items:center; justify-content:center; font-size:28px; font-weight:700; color:#dc2626; }
    .f4-keys { display:flex; justify-content:space-between; margin-top:16px; font-size:36px; font-weight:700; }
""", """
      <div class="eyebrow" id="f4-eye"><i></i>근거 ② 시간표</div>
      <div class="h1 f4-title" id="f4-title">수업도 <em>영어</em> 중심</div>
      <div class="f4-wrap" id="f4-wrap" data-layout-allow-overflow><img class="f4-img" id="f4-img" src="assets/timetable.webp" alt=""></div>
      <div class="f4-call" id="f4-call">불어는 하루 1시간</div>
      <div class="card f4-res" id="f4-res">
        <div class="f4-lab">전체 수업 중 영어</div>
        <div class="f4-n num" id="f4-n">0%</div>
        <div class="f4-track"><div class="f4-fill" id="f4-fill"></div><div class="f4-fr" id="f4-fr">불어</div></div>
        <div class="f4-keys"><span style="color:#1e2bfa">English</span><span style="color:#dc2626">Français</span></div>
      </div>
""", f"""
      tl.fromTo("#f4-eye", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, 0.0);
      tl.fromTo("#f4-title", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 0.1);
      tl.fromTo("#f4-wrap", {{opacity:0, y:120}}, {{opacity:1, y:0, duration:0.55, ease:"power3.out"}}, 0.2);
      tl.fromTo("#f4-img", {{scale:1}}, {{scale:1.3, duration:2.2, ease:"power1.inOut"}}, 0.6);
      tl.fromTo("#f4-call", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {W(4,"불어는")});
      tl.fromTo("#f4-res", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {W(4,"전체",0,-0.1)});
      tl.to(["#f4-wrap","#f4-call"], {{opacity:0, duration:0.4}}, {W(4,"전체",0,-0.1)});
      count("f4-n", 80, {W(4,"80%",0,-0.2)}, 0.8, (n) => n + "%");
      tl.fromTo("#f4-fill", {{scaleX:0}}, {{scaleX:1, duration:0.8, ease:"power2.out"}}, {W(4,"80%",0,-0.2)});
      tl.fromTo("#f4-fr", {{opacity:0}}, {{opacity:1, duration:0.3}}, {W(4,"영어로")});
""")

# ---------- Frame 5 — 학비 차이 ($20,000 vs $12,000) ----------
frame("05-tuition", 5, """
    .f5-title { top:320px; font-size:84px; }
    .f5-base { position:absolute; left:80px; right:80px; top:1400px; height:4px; background:#111; opacity:.15; }
    .f5-bar { position:absolute; bottom:520px; width:320px; border-radius:14px 14px 0 0; transform-origin:50% 100%; }
    .f5-on { left:130px; height:800px; background:#c9c9d6; }
    .f5-mt { left:630px; height:480px; background:#1e2bfa; }
    .f5-val { position:absolute; width:420px; text-align:center; font-size:76px; font-weight:900; letter-spacing:-.03em; }
    .f5-v1 { left:80px; top:500px; color:#6b6b6b; } .f5-v2 { left:580px; top:820px; color:#1e2bfa; }
    .f5-lab { position:absolute; top:1420px; width:420px; text-align:center; font-size:40px; font-weight:700; line-height:1.3; }
    .f5-l1 { left:80px; color:#6b6b6b; } .f5-l2 { left:580px; color:#1e2bfa; }
    .f5-brk { position:absolute; left:470px; top:600px; width:60px; height:320px; border:5px solid #1e2bfa; border-left:none; border-radius:0 18px 18px 0; transform-origin:0 0; }
    .f5-save { position:absolute; left:575px; top:590px; width:410px; padding:22px 30px; border-radius:20px; background:#1e2bfa; color:#fdfae7; text-align:center; }
    .f5-save small { display:block; font-size:36px; font-weight:700; opacity:.85; }
    .f5-save b { display:block; font-size:96px; font-weight:900; letter-spacing:-.03em; line-height:1.1; }
""", """
      <div class="eyebrow" id="f5-eye"><i></i>근거 ③ 부모님 학비 (1년)</div>
      <div class="h1 f5-title" id="f5-title">학비 차이가 <em>이만큼</em></div>
      <div class="f5-base"></div>
      <div class="f5-bar f5-on" id="f5-b1"></div>
      <div class="f5-bar f5-mt" id="f5-b2"></div>
      <div class="f5-val f5-v1 num" id="f5-v1">약 $0</div>
      <div class="f5-val f5-v2 num" id="f5-v2">$0</div>
      <div class="f5-lab f5-l1" id="f5-l1">온타리오<br>대학부설</div>
      <div class="f5-lab f5-l2" id="f5-l2">몬트리올<br>사립컬리지</div>
      <div class="f5-brk" id="f5-brk"></div>
      <div class="f5-save" id="f5-save"><small>1년 차액</small><b class="num">$8,000</b></div>
""", f"""
      tl.fromTo("#f5-eye", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, 0.0);
      tl.fromTo("#f5-title", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 0.2);
      tl.fromTo("#f5-l1", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4}}, {W(5,"온타리오")});
      tl.fromTo("#f5-b1", {{scaleY:0}}, {{scaleY:1, duration:1.3, ease:"power2.out"}}, {W(5,"온타리오",0,0.1)});
      tl.fromTo("#f5-v1", {{opacity:0}}, {{opacity:1, duration:0.3}}, {W(5,"약")});
      count("f5-v1", 20000, {W(5,"약")}, 0.9, (n) => "약 $" + n.toLocaleString("en-US"));
      tl.fromTo("#f5-l2", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4}}, {W(5,"몬트리올")});
      tl.fromTo("#f5-b2", {{scaleY:0}}, {{scaleY:1, duration:0.9, ease:"power2.out"}}, {W(5,"몬트리올",0,0.1)});
      tl.fromTo("#f5-v2", {{opacity:0}}, {{opacity:1, duration:0.3}}, {W(5,"만",0,-0.15)});
      count("f5-v2", 12000, {W(5,"만",0,-0.15)}, 0.8, (n) => "$" + n.toLocaleString("en-US"));
      tl.fromTo("#f5-brk", {{opacity:0, scaleY:0}}, {{opacity:1, scaleY:1, duration:0.5, ease:"power2.out"}}, {W(5,"1년에",1,-0.2)});
      tl.fromTo("#f5-save", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.8)"}}, {W(5,"8천",0,-0.1)});
      tl.to("#f5-save", {{scale:1.06, duration:0.3, ease:"power2.out"}}, {max(W(5,"차이가"), round(W(5,"8천",0,-0.1)+0.47,2))});
      tl.to("#f5-save", {{scale:1, duration:0.4, ease:"power2.inOut"}}, {max(W(5,"차이가"), round(W(5,"8천",0,-0.1)+0.47,2))+0.32:.2f});
""")

# ---------- Frame 6 — 원어민 튜터 ($40 × 4 × 50 = $8,000) ----------
frame("06-tutor", 6, """
    .f6-title { top:320px; font-size:84px; }
    .f6-eqs { position:absolute; left:80px; right:80px; top:480px; }
    .f6-row { display:flex; justify-content:space-between; align-items:baseline; padding:18px 8px; border-bottom:2px solid rgba(30,43,250,0.15); font-size:60px; font-weight:800; }
    .f6-row span:first-child { color:#6b6b6b; font-size:44px; font-weight:700; }
    .f6-tot { margin-top:16px; border-bottom:none; }
    .f6-tot b { font-size:110px; font-weight:900; color:#1e2bfa; letter-spacing:-.03em; }
    .f6-ok { left:80px; top:1050px; }
    .f6-chart { position:absolute; left:80px; right:80px; top:1170px; height:400px; }
    .f6-svg { position:absolute; left:40px; top:30px; width:840px; height:340px; }
    .f6-svg path { fill:none; stroke-width:9; stroke-linecap:round; }
    .f6-lg { position:absolute; font-size:34px; font-weight:700; }
""", """
      <div class="eyebrow" id="f6-eye"><i></i>근거 ④ 원어민 튜터</div>
      <div class="h1 f6-title" id="f6-title">차액으로 <em>원어민 튜터</em></div>
      <div class="f6-eqs">
        <div class="f6-row" id="f6-r1"><span>원어민 튜터</span><span class="num">$40 / 시간</span></div>
        <div class="f6-row" id="f6-r2"><span>일주일</span><span>× 4회</span></div>
        <div class="f6-row" id="f6-r3"><span>1년 내내</span><span>× 50주</span></div>
        <div class="f6-row f6-tot" id="f6-r4"><span>=</span><b class="num">$8,000</b></div>
      </div>
      <div class="pill solid f6-ok" id="f6-ok">학비 차액만으로 OK ✓</div>
      <div class="card f6-chart" id="f6-chart">
        <svg class="f6-svg" viewBox="0 0 840 340">
          <path id="f6-slow" d="M10 320 C 300 315, 420 300, 560 220 S 760 60, 830 40" stroke="#c9c9d6"/>
          <path id="f6-fast" d="M10 320 C 120 300, 200 200, 330 130 S 650 40, 830 20" stroke="#1e2bfa"/>
        </svg>
        <div class="f6-lg" id="f6-lg1" style="left:600px; top:300px; color:#9a9a9a">혼자 적응</div>
        <div class="f6-lg" id="f6-lg2" style="left:40px; top:20px; color:#1e2bfa">튜터와 함께 → 적응기 단축</div>
      </div>
""", f"""
      tl.fromTo("#f6-eye", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, 0.0);
      tl.fromTo("#f6-title", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 0.15);
      tl.fromTo("#f6-r1", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {W(6,"시간당")});
      tl.fromTo("#f6-r2", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {W(6,"일주일에")});
      tl.fromTo("#f6-r3", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {W(6,"1년")});
      tl.fromTo("#f6-r4", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.8)", transformOrigin:"100% 50%"}}, {W(6,"붙여줄")});
      tl.fromTo("#f6-ok", {{opacity:0, y:30, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.8)"}}, {W(6,"있어요")});
      tl.fromTo("#f6-chart", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {W(6,"처음의",0,-0.1)});
      const slow = $("f6-slow"), fast = $("f6-fast"); slow.style.strokeDasharray = 1100; fast.style.strokeDasharray = 1100;
      tl.fromTo(slow, {{strokeDashoffset:1100}}, {{strokeDashoffset:0, duration:1.2, ease:"power1.inOut"}}, {W(6,"답답한")});
      tl.fromTo("#f6-lg1", {{opacity:0}}, {{opacity:1, duration:0.3}}, {W(6,"적응기를")});
      tl.fromTo(fast, {{strokeDashoffset:1100}}, {{strokeDashoffset:0, duration:0.9, ease:"power2.out"}}, {W(6,"훨씬")});
      tl.fromTo("#f6-lg2", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.3}}, {W(6,"빨리")});
""")

# ---------- Frame 7 — CTA ----------
frame("07-cta", 7, """
    .f7-rings { position:absolute; left:540px; top:900px; width:0; height:0; }
    .f7-rings i { position:absolute; border:2px solid rgba(30,43,250,0.12); border-radius:50%; }
    .f7-chips { position:absolute; left:80px; top:300px; display:flex; gap:24px; }
    .f7-chips .pill { position:relative; }
    .f7-h { top:440px; font-size:110px; font-weight:900; }
    .f7-brand { position:absolute; left:80px; right:80px; top:820px; height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#1e2bfa; border-radius:20px; color:#fdfae7; }
    .f7-brand b { font-size:140px; font-weight:900; letter-spacing:-.02em; line-height:1; }
    .f7-brand small { font-size:40px; font-weight:700; opacity:.85; margin-top:14px; }
    .f7-c { left:80px; right:80px; text-align:center; font-size:54px; font-weight:800; background:#fff; color:#111; border:2px solid rgba(30,43,250,0.2); }
    .f7-c1 { top:1170px; } .f7-c2 { top:1300px; }
    .f7-fine { position:absolute; left:80px; right:80px; top:1440px; text-align:center; font-size:32px; font-weight:500; color:#6b6b6b; }
""", """
      <div class="f7-rings" id="f7-rings" data-layout-allow-overflow>
        <i style="left:-300px; top:-300px; width:600px; height:600px"></i>
        <i style="left:-440px; top:-440px; width:880px; height:880px"></i>
      </div>
      <div class="f7-chips">
        <div class="pill soft" id="f7-c-en">영어 ✓</div>
        <div class="pill soft" id="f7-c-bud">예산 ✓</div>
      </div>
      <div class="h1 f7-h" id="f7-h"><em>몬트리올</em>도<br>꼭 알아보세요</div>
      <div class="f7-brand" id="f7-brand"><b>AA Canada</b><small>캐나다 자녀무상교육 · 유학 · 이민</small></div>
      <div class="pill f7-c f7-c1" id="f7-c1">💬 카카오톡 <span style="color:#1e2bfa">canlog</span></div>
      <div class="pill f7-c f7-c2" id="f7-c2">📞 <span class="num">02-567-4345</span></div>
      <div class="f7-fine" id="f7-fine">* 학비 프로모션·학생비자 접수는 선착순으로 제한될 수 있어요</div>
""", f"""
      tl.fromTo("#f7-c-en", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, 0.0);
      tl.fromTo("#f7-c-bud", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {W(7,"예산도")});
      tl.fromTo("#f7-h", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.55, ease:"power3.out"}}, {W(7,"몬트리올도",0,-0.05)});
      tl.fromTo("#f7-rings", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:2.0, ease:"power2.out"}}, {W(7,"AA",0,-0.3)});
      tl.fromTo("#f7-brand", {{opacity:0, y:60, scale:0.95}}, {{opacity:1, y:0, scale:1, duration:0.55, ease:"power3.out"}}, {W(7,"AA",0,-0.15)});
      tl.fromTo("#f7-c1", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {W(7,"함께하겠습니다",0,0.2)});
      tl.fromTo("#f7-c2", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {W(7,"함께하겠습니다",0,0.5)});
      tl.fromTo("#f7-fine", {{opacity:0}}, {{opacity:1, duration:0.5}}, {W(7,"함께하겠습니다",0,1.0)});
""")
print("v3 frames written")
