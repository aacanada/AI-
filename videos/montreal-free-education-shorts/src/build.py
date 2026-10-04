#!/usr/bin/env python3
"""Generates index.html for the AA Canada Montreal shorts.

Timings come from the narration's pause map (public/narration.m4a) and the
segment-level transcript; edit CAPTIONS / scene times here and re-run.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

DURATION = 133.0

# (start, end, text) — [brackets] mark highlighted words
CAPTIONS = [
    (0.91, 3.40, "캐나다 [자녀무상교육],"),
    (3.40, 6.55, "아직도 부모 학비로 2년에 [4만 불] 쓰실 건가요?"),
    (6.84, 11.30, "2년 전체 학비, [만 3천 불대]로 끝내는 방법이 있습니다."),
    (11.77, 14.95, "자녀를 캐나다 공립학교에 [무상]으로 보내려면"),
    (15.04, 17.05, "부모가 [학생비자]를 받아야 하죠."),
    (17.19, 20.80, "그런데 다른 지역에서 2년 프로그램을 찾으면"),
    (20.95, 24.25, "부모 학비만 보통 [4만 불] 정도 나옵니다."),
    (24.42, 28.30, "아이 교육비 아끼려다 [부모 학비가 더] 드는 상황이에요."),
    (28.64, 32.10, "그래서 저희 [AA Canada]가 준비한 프로그램이 있습니다."),
    (32.26, 35.75, "[몬트리올 사립컬리지] 이커머스 전공입니다."),
    (35.94, 37.85, "비자 기간은 [2년],"),
    (37.96, 41.50, "2년 전체 학비는 [13,750불]이에요."),
    (41.63, 45.60, "등록비, 수속료까지 [전부 포함]된 금액입니다."),
    (45.90, 48.65, "가장 중요한 건 [수업 시간]입니다."),
    (48.77, 50.75, "원래 [야간반]인 과정을"),
    (50.82, 54.62, "[오전 8시 반부터 12시 반]까지 듣도록 바꾼,"),
    (54.70, 57.30, "저희만의 [독점 프로그램]이에요."),
    (57.30, 60.80, "아이 학교 보내고 수업 듣고, [아이 하교 전에] 끝납니다."),
    (60.89, 62.75, "[등하교 걱정]이 없어요."),
    (62.96, 67.55, "그리고 오후에는 [주당 24시간]까지 합법적으로 일할 수 있습니다."),
    (67.68, 70.90, "영어 점수는 [듀오링고 85점]이 필요한데요,"),
    (70.90, 74.60, "입학 신청할 때 바로 내지 않아도 되고"),
    (74.60, 79.30, "[수업 시작 전까지만] 제출하면 되도록 학교와 협의해 두었습니다."),
    (79.75, 83.25, "몬트리올은 캐나다에서 [두 번째로 큰 도시]인데,"),
    (83.37, 85.70, "렌트비는 [중소도시 수준]입니다."),
    (85.70, 87.65, "그리고 아이와 함께 와도"),
    (87.72, 90.50, "[차 없이] 살 수 있는 거의 유일한 도시예요."),
    (90.64, 94.00, "지하철과 버스가 잘 되어 있어서 차값,"),
    (94.11, 97.10, "보험료까지 [아낄 수 있습니다]."),
    (97.74, 100.20, "'몬트리올은 [불어] 쓰는 곳 아니야?'"),
    (100.20, 103.75, "이 걱정 때문에 아예 알아보지 않는 분들 많으시죠."),
    (103.89, 107.50, "[영어만으로도] 충분히 생활할 수 있습니다."),
    (107.81, 110.90, "아이는 [영어 중심 학교]에 보낼 수도 있고,"),
    (110.90, 114.60, "[영어와 불어]를 모두 하는 아이로 키울 수도 있어요."),
    (114.69, 117.10, "선택은 [부모님]이 하시면 됩니다."),
    (117.27, 119.35, "아낀 학비 중 일부를"),
    (119.46, 121.70, "아이 [영어 튜터]에 써 보세요."),
    (121.70, 124.45, "짧은 기간에 영어 실력이 [확 달라집니다]."),
    (124.57, 129.40, "자세한 상담은 프로필 링크에서, [AA Canada]로 신청해 주세요."),
]

# scene id, start, end
SCENES = [
    ("s1", 0.0, 11.4),
    ("s2", 11.4, 28.3),
    ("s3", 28.3, 45.6),
    ("s4", 45.6, 62.7),
    ("s5", 62.7, 67.55),
    ("s6", 67.55, 79.3),
    ("s7", 79.3, 97.1),
    ("s8", 97.1, 117.0),
    ("s9", 117.0, DURATION),
]

SCENE_HTML = {
    "s1": """
      <div class="grp" id="s1-a">
        <div class="pill red" id="s1-tag">캐나다 자녀무상교육</div>
        <div class="kicker" id="s1-k1">2년 부모 학비</div>
        <div class="strike-wrap" id="s1-old">
          <div class="mega white" id="s1-40k">$40,000</div>
          <div class="strike" id="s1-strike" data-layout-allow-occlusion></div>
        </div>
        <div class="kicker" id="s1-k2">AA Canada라면</div>
        <div class="mega yellow" id="s1-new">$40,000</div>
        <div class="sub" id="s1-sub">등록비 · 수속료 <b>모두 포함</b></div>
      </div>""",
    "s2": """
      <div class="grp" id="s2-a">
        <div class="card" id="s2-c1"><span class="num">01</span><div><div class="card-t">자녀 공립학교</div><div class="card-b yellow">무상교육</div></div></div>
        <div class="arrow-down" id="s2-ar"></div>
        <div class="card red-card" id="s2-c2"><span class="num">조건</span><div><div class="card-t">부모가</div><div class="card-b">학생비자</div></div></div>
      </div>
      <div class="grp" id="s2-b">
        <div class="kicker" id="s2-k">타 지역 2년 프로그램</div>
        <div class="bar-row" id="s2-row1">
          <div class="bar-label">부모 학비</div>
          <div class="bar-track"><div class="bar-fill redfill" id="s2-bar"></div></div>
          <div class="bar-val" id="s2-val">약 $40,000</div>
        </div>
        <div class="big2" id="s2-q1">교육비 아끼려다</div>
        <div class="big2 hl-red" id="s2-q2">학비가 더 든다?</div>
      </div>""",
    "s3": """
      <div class="grp" id="s3-a">
        <div class="stamp" id="s3-stamp">AA CANADA 독점</div>
        <div class="kicker" id="s3-k">몬트리올 사립컬리지</div>
        <div class="title-xl" id="s3-t" style="font-size:128px">E-COMMERCE</div>
        <div class="kicker" id="s3-k2">전공</div>
        <div class="tiles">
          <div class="tile" id="s3-t1"><div class="tile-l">비자 기간</div><div class="tile-v">2년</div></div>
          <div class="tile hot" id="s3-t2"><div class="tile-l">2년 전체 학비</div><div class="tile-v">$13,750</div></div>
        </div>
        <div class="checks" id="s3-chk">
          <div class="chk" id="s3-c1">등록비 포함</div>
          <div class="chk" id="s3-c2">수속료 포함</div>
        </div>
      </div>""",
    "s4": """
      <div class="grp" id="s4-a">
        <div class="kicker" id="s4-k">가장 중요한 건</div>
        <div class="title-xl yellow" id="s4-t">수업 시간</div>
        <div class="swap">
          <div class="strike-wrap" id="s4-night"><div class="big2 dim">야간반</div><div class="strike" id="s4-ns" data-layout-allow-occlusion></div></div>
          <div class="arrow-right" id="s4-arr"></div>
          <div class="big2 yellow" id="s4-day">오전반</div>
        </div>
      </div>
      <div class="grp" id="s4-b">
        <div class="clock" id="s4-clock">08:30<span>–</span>12:30</div>
        <div class="sub" id="s4-days">주 4회 · 주당 16시간</div>
        <div class="day" id="s4-dayline">
          <div class="day-track"></div>
          <div class="day-class" id="s4-class">수업</div>
          <div class="day-mk" id="s4-m1" style="left:5.5%"><i></i><span>아이 등교</span></div>
          <div class="day-mk" id="s4-m2" style="left:72%"><i></i><span>아이 하교</span></div>
          <div class="day-tick" style="left:0%">7시</div>
          <div class="day-tick" style="left:45.4%">12시</div>
          <div class="day-tick" style="left:90.9%">17시</div>
        </div>
        <div class="stamp green" id="s4-stamp">등하교 걱정 NO</div>
        <div class="pill red" id="s4-excl">야간반 → 오전반 독점 커스터마이징</div>
      </div>""",
    "s5": """
      <div class="grp" id="s5-a">
        <div class="kicker" id="s5-k">수업 끝난 오후에는</div>
        <div class="giant yellow" id="s5-24">24</div>
        <div class="big2" id="s5-u">시간 / 주</div>
        <div class="pill green-pill" id="s5-p">합법적으로 취업 가능</div>
      </div>""",
    "s6": """
      <div class="grp" id="s6-a">
        <div class="duo" id="s6-duo">Duolingo</div>
        <div class="giant" id="s6-85">85<small>점</small></div>
        <div class="row-x" id="s6-r1"><span class="mark x">✕</span><span>입학 신청할 때 제출</span></div>
        <div class="row-x ok" id="s6-r2"><span class="mark o">✓</span><span>수업 시작 전까지만 제출</span></div>
        <div class="stamp" id="s6-stamp">학교와 협의 완료</div>
      </div>""",
    "s7": """
      <div class="grp" id="s7-a">
        <div class="title-xl" id="s7-t">MONTRÉAL</div>
        <div class="lcard" id="s7-c1"><span class="badge">No.2</span><div>캐나다 <b>두 번째 대도시</b></div></div>
        <div class="lcard" id="s7-c2"><span class="badge">$</span><div>렌트비는 <b>중소도시 수준</b></div></div>
        <div class="lcard hot" id="s7-c3"><span class="badge car">
          <svg viewBox="0 0 64 40" width="64" height="40"><path d="M8 26 L14 12 Q16 8 22 8 L42 8 Q48 8 50 12 L56 26 L58 26 Q60 26 60 28 L60 33 L4 33 L4 28 Q4 26 6 26 Z" fill="#0e0e12"/><circle cx="17" cy="34" r="5" fill="#0e0e12"/><circle cx="47" cy="34" r="5" fill="#0e0e12"/><line x1="2" y1="38" x2="62" y2="2" stroke="#ff2d3d" stroke-width="6" stroke-linecap="round"/></svg>
        </span><div>자녀 동반, <b>차 없이 생활</b></div></div>
        <div class="chips" id="s7-chips"><div class="chip" id="s7-ch1">지하철</div><div class="chip" id="s7-ch2">버스</div></div>
        <div class="save" id="s7-save">차값 · 보험료 <b>SAVE</b></div>
      </div>""",
    "s8": """
      <div class="grp" id="s8-a">
        <div class="big2" id="s8-q">몬트리올 =</div>
        <div class="title-xl" id="s8-fr">불어만?</div>
        <div class="stamp big" id="s8-x">오해!</div>
      </div>
      <div class="grp" id="s8-b">
        <div class="title-xl yellow" id="s8-en">영어만으로</div>
        <div class="big2" id="s8-ok">생활 OK</div>
        <div class="kicker" id="s8-kk">자녀 학교는 선택</div>
        <div class="opt" id="s8-o1"><span class="opt-l">A</span><div>영어 중심 학교</div></div>
        <div class="opt" id="s8-o2"><span class="opt-l">B</span><div>영어 + 불어 이중언어</div></div>
        <div class="pill red" id="s8-p">선택은 부모님이</div>
      </div>""",
    "s9": """
      <div class="grp" id="s9-a">
        <div class="cmp">
          <div class="cmp-col" id="s9-l"><div class="cmp-h">타 지역</div><div class="strike-wrap"><div class="cmp-v dim" id="s9-lv">$40,000</div><div class="strike" id="s9-lv-strike" data-layout-allow-occlusion></div></div></div>
          <div class="cmp-vs">VS</div>
          <div class="cmp-col" id="s9-r"><div class="cmp-h">몬트리올</div><div class="cmp-v yellow">$13,750</div></div>
        </div>
        <div class="arrow-down" id="s9-ar"></div>
        <div class="card" id="s9-tutor"><span class="num">+</span><div><div class="card-t">아낀 비용 일부로</div><div class="card-b yellow">자녀 영어 튜터</div></div></div>
        <div class="big2" id="s9-up">영어 실력 <span class="yellow">급상승</span></div>
      </div>
      <div class="grp" id="s9-b">
        <div class="logo" id="s9-logo">AA CANADA</div>
        <div class="kicker" id="s9-lk">캐나다 자녀무상교육 · 몬트리올 전문</div>
        <div class="cta" id="s9-cta">프로필 링크에서 상담 신청</div>
        <div class="disc" id="s9-disc">※ 비자 승인 여부와 세부 조건은 개인마다 다를 수 있습니다.</div>
      </div>""",
}

# GSAP timeline body (absolute seconds)
TIMELINE = r"""
const E = "power3.out", B = "back.out(1.8)";
const pop = (sel, t, extra) => tl.fromTo(sel, { opacity: 0, y: 50, scale: 0.92 }, Object.assign({ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: E }, extra || {}), t);
const slam = (sel, t, rot) => tl.fromTo(sel, { opacity: 0, scale: 2.4, rotation: rot || -8 }, { opacity: 1, scale: 1, rotation: rot || -8, duration: 0.35, ease: "power4.in" }, t);
const out = (sel, t) => tl.to(sel, { opacity: 0, y: -60, duration: 0.3, ease: "power2.in" }, t);
const draw = (sel, t, d) => tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: d || 0.35, ease: "power2.out" }, t);
const count = (sel, from, to, t, d, prefix) => {
  const o = { v: from }, el = document.querySelector(sel);
  tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out",
    onUpdate: () => { el.textContent = (prefix || "$") + Math.round(o.v).toLocaleString("en-US"); } }, t);
};

// persistent chrome
tl.fromTo("#progress", { scaleX: 0 }, { scaleX: 1, duration: 132.9, ease: "none" }, 0);
tl.fromTo("#stripe", { x: -200 }, { x: 200, duration: 132.9, ease: "none" }, 0);

// S1 hook
pop("#s1-tag", 0.2);
pop("#s1-k1", 0.9);
pop("#s1-old", 1.1, { ease: B });
draw("#s1-strike", 4.6, 0.3);
tl.to("#s1-40k", { opacity: 0.35, duration: 0.3 }, 4.7);
pop("#s1-k2", 6.9);
pop("#s1-new", 7.1, { ease: B });
count("#s1-new", 40000, 13750, 7.3, 1.6);
tl.fromTo("#s1-new", { scale: 1 }, { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }, 8.9);
pop("#s1-sub", 9.3);
out("#s1-a", 11.05);

// S2 problem
pop("#s2-c1", 11.8);
pop("#s2-ar", 14.0);
pop("#s2-c2", 15.0, { ease: B });
out("#s2-a", 16.85);
pop("#s2-k", 17.2);
pop("#s2-row1", 17.6);
draw("#s2-bar", 21.0, 1.2);
pop("#s2-val", 21.6, { ease: B });
pop("#s2-q1", 24.5);
slam("#s2-q2", 25.6, -3);
out("#s2-b", 27.95);

// S3 program
slam("#s3-stamp", 28.7, -6);
pop("#s3-k", 32.3);
tl.fromTo("#s3-t", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: B }, 32.6);
pop("#s3-k2", 33.2);
pop("#s3-t1", 36.0, { ease: B });
pop("#s3-t2", 38.0, { ease: B });
tl.fromTo("#s3-t2", { scale: 1 }, { scale: 1.06, duration: 0.18, yoyo: true, repeat: 1 }, 39.6);
pop("#s3-c1", 41.7);
pop("#s3-c2", 42.6);
out("#s3-a", 45.25);

// S4 schedule
pop("#s4-k", 45.9);
tl.fromTo("#s4-t", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: B }, 46.6);
pop("#s4-night", 48.8);
draw("#s4-ns", 49.7, 0.3);
pop("#s4-arr", 50.0);
pop("#s4-day", 50.2, { ease: B });
out("#s4-a", 51.2);
tl.fromTo("#s4-clock", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.5, ease: B }, 51.4);
pop("#s4-days", 52.2);
pop("#s4-dayline", 52.8);
tl.fromTo("#s4-class", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, 53.3);
pop("#s4-excl", 54.8, { ease: B });
pop("#s4-m1", 57.4);
pop("#s4-m2", 59.2);
slam("#s4-stamp", 60.9, -6);
out("#s4-b", 62.35);

// S5 work
pop("#s5-k", 63.0);
tl.fromTo("#s5-24", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.5, ease: B }, 64.3);
count("#s5-24", 0, 24, 64.3, 0.9, " ");
pop("#s5-u", 64.9);
pop("#s5-p", 65.8, { ease: B });
out("#s5-a", 67.2);

// S6 duolingo
pop("#s6-duo", 67.8);
tl.fromTo("#s6-85", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.5, ease: B }, 68.9);
pop("#s6-r1", 71.0);
tl.to("#s6-r1", { opacity: 0.45, duration: 0.3 }, 74.4);
pop("#s6-r2", 74.7, { ease: B });
slam("#s6-stamp", 76.9, -5);
out("#s6-a", 78.95);

// S7 montreal
tl.fromTo("#s7-t", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.7, ease: E }, 79.5);
pop("#s7-c1", 80.6);
pop("#s7-c2", 83.4);
pop("#s7-c3", 87.7, { ease: B });
pop("#s7-ch1", 90.7);
pop("#s7-ch2", 91.3);
slam("#s7-save", 94.2, -4);
out("#s7-a", 96.75);

// S8 french myth
pop("#s8-q", 97.8);
tl.fromTo("#s8-fr", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: B }, 98.6);
slam("#s8-x", 100.4, -10);
out("#s8-a", 103.5);
tl.fromTo("#s8-en", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: B }, 103.95);
pop("#s8-ok", 104.9);
pop("#s8-kk", 107.6);
pop("#s8-o1", 108.0, { ease: B });
pop("#s8-o2", 111.0, { ease: B });
slam("#s8-p", 114.8, -3);
out("#s8-b", 116.65);

// S9 close
pop("#s9-l", 117.3);
pop("#s9-r", 117.8, { ease: B });
draw("#s9-lv-strike", 118.4, 0.3);
pop("#s9-ar", 119.4);
pop("#s9-tutor", 119.7, { ease: B });
pop("#s9-up", 121.8, { ease: B });
out("#s9-a", 124.2);
tl.fromTo("#s9-logo", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.6, ease: B }, 124.5);
pop("#s9-lk", 125.1);
pop("#s9-cta", 126.0, { ease: B });
tl.fromTo("#s9-cta", { scale: 1 }, { scale: 1.06, duration: 0.45, yoyo: true, repeat: 7, ease: "sine.inOut" }, 127.0);
pop("#s9-disc", 127.4);
"""


def caption_html(i, start, end, text):
    parts = re.split(r"(\[[^\]]+\])", text)
    inner = "".join(
        f'<span class="hl">{html.escape(p[1:-1])}</span>' if p.startswith("[") else html.escape(p)
        for p in parts
    )
    dur = round(end - start, 2)
    return (
        f'<div id="cap-{i:02d}" class="clip cap" data-start="{start}" data-duration="{dur}" '
        f'data-track-index="2"><div class="cap-box" id="capbox-{i:02d}">{inner}</div></div>'
    )


def build():
    scenes = "\n".join(
        f'    <section id="{sid}" class="clip scene" data-start="{s}" data-duration="{round(e - s, 2)}" '
        f'data-track-index="1">{SCENE_HTML[sid]}\n    </section>'
        for sid, s, e in SCENES
    )
    caps = "\n".join(f"    {caption_html(i, *c)}" for i, c in enumerate(CAPTIONS))
    cap_tweens = "\n".join(
        f'tl.fromTo("#capbox-{i:02d}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }}, {s});'
        for i, (s, e, t) in enumerate(CAPTIONS)
    )
    page = TEMPLATE.replace("{{SCENES}}", scenes).replace("{{CAPTIONS}}", caps)
    page = page.replace("{{TIMELINE}}", TIMELINE + "\n// captions\n" + cap_tweens)
    page = page.replace("{{DURATION}}", str(DURATION))
    with open(os.path.join(HERE, "..", "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


TEMPLATE = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()

if __name__ == "__main__":
    build()
