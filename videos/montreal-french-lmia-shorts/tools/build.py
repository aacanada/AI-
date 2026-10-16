"""Build index.html (1080x1920 Shorts) from timing.json.
Captions sit in the TOP band (Shorts UI covers the bottom). Re-run after tts.py."""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "timing.json").read_text())
TOTAL = T["total"]

HL = ["몬트리올", "가장 싸게", "가장 저렴하게", "무기", "중하 레벨", "LMIA 면제", "고용주 부담 제로",
      "훨씬 유리", "계속!", "영주권자 학비", "유리한", "엄청납니다", "1~2년", "기간 제한 없음",
      "AA Canada", "불어", "바로 전환"]
HL_RE = re.compile("|".join(re.escape(h) for h in sorted(HL, key=len, reverse=True)))

def cap_html(text):
    out, pos = [], 0
    for m in HL_RE.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        out.append(f'<span class="hl">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)

def r(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")

# ---------- scene bodies (visual zone, below the caption band) ----------
SCENES = {
"s1-hook": """
  <div class="pill" id="s1-pill">캐나다 자녀무상교육 · 장기플랜</div>
  <div class="s1-q" id="s1-q">
    <div class="s1-qline">가장 싸게,</div>
    <div class="s1-qline">가장 오래?</div>
  </div>
  <div class="s1-answer" id="s1-answer">
    <div class="s1-pin"><svg viewBox="0 0 24 24" width="120" height="120"><path fill="#E63946" d="M12 2C7.6 2 4 5.6 4 10c0 5.6 8 12 8 12s8-6.4 8-12c0-4.4-3.6-8-8-8zm0 11a3 3 0 110-6 3 3 0 010 6z"/></svg></div>
    <div class="s1-city">몬트리올</div>
    <div class="s1-bar" id="s1-bar"></div>
    <div class="s1-sub">MONTRÉAL · QUÉBEC</div>
  </div>
""",
"s2-montreal": """
  <div class="s2-chart" id="s2-chart">
    <div class="chart-title">자녀 동반 체류비 · 상대 비교</div>
    <div class="bar-row"><div class="bar-label">밴쿠버</div><div class="bar-track"><div class="bar" id="s2-b1"></div></div></div>
    <div class="bar-row"><div class="bar-label">토론토</div><div class="bar-track"><div class="bar" id="s2-b2"></div></div></div>
    <div class="bar-row"><div class="bar-label hlc">몬트리올</div><div class="bar-track"><div class="bar bar-win" id="s2-b3"></div><div class="bar-tag" id="s2-tag">최저</div></div></div>
  </div>
  <div class="s2-weapon" id="s2-weapon">
    <div class="fr-badge">FR</div>
    <div class="weapon-text">불어 = <span class="y">무기</span></div>
    <div class="weapon-sub">불어권이라 피할 곳이 아니라, 활용할 곳</div>
  </div>
""",
"s3-route": """
  <div class="route">
    <div class="node" id="s3-n1"><div class="num">1</div><div><div class="nt">몬트리올에서 불어 공부</div><div class="ns">퀘벡 정부 불어수업 활용</div></div></div>
    <div class="link" id="s3-l1"></div>
    <div class="node" id="s3-n2"><div class="num">2</div><div><div class="nt">중하 레벨 불어회화</div><div class="ns">NCLC 5 수준</div></div></div>
    <div class="link" id="s3-l2"></div>
    <div class="node" id="s3-n3"><div class="num">3</div><div><div class="nt">영어권 지역으로 이동</div><div class="ns">밴쿠버 · 토론토 · 런던</div></div></div>
    <div class="link" id="s3-l3"></div>
    <div class="node node-win" id="s3-n4"><div class="num">✓</div><div><div class="nt">LMIA 면제 취업비자</div><div class="ns">Francophone Mobility</div></div></div>
  </div>
""",
"s4-lmia": """
  <div class="lmia-card" id="s4-card">
    <div class="lmia-title">LMIA</div>
    <div class="lmia-sub">노동시장영향평가 · <b>고용주</b>가 신청</div>
    <div class="burden" id="s4-i1"><span>서류 · 구인광고 증빙</span><i class="strike" id="s4-x1"></i></div>
    <div class="burden" id="s4-i2"><span>신청비 CAD $1,000</span><i class="strike" id="s4-x2"></i></div>
    <div class="burden" id="s4-i3"><span>수개월 심사 대기</span><i class="strike" id="s4-x3"></i></div>
  </div>
  <div class="stamp" id="s4-stamp">면제</div>
  <div class="s4-up" id="s4-up">고용주 부담 0 → 취업 경쟁력 ↑</div>
""",
"s5-benefits": """
  <div class="s5-head" id="s5-head">취업비자 보유 기간 동안</div>
  <div class="check" id="s5-c1"><div class="cb">✓</div><div><div class="ct">자녀 무상교육 계속</div><div class="cs">공립 초·중·고</div></div></div>
  <div class="check" id="s5-c2"><div class="cb">✓</div><div><div class="ct">대학은 영주권자 학비</div><div class="cs">영주권 없이도 적용 가능</div></div></div>
  <div class="check" id="s5-c3"><div class="cb">✓</div><div><div class="ct">영주권 진행에도 유리</div><div class="cs">캐나다 경력 + 불어</div></div></div>
""",
"s6-money": """
  <div class="vs-wrap">
    <div class="col col-bad" id="s6-left">
      <div class="col-h">학생으로 체류</div>
      <div class="arrow down">↓</div>
      <div class="col-big"><div>매년</div><div>학비 지출</div></div>
    </div>
    <div class="vs" id="s6-vs">VS</div>
    <div class="col col-good" id="s6-right">
      <div class="col-h">취업으로 체류</div>
      <div class="arrow up">↑</div>
      <div class="col-big"><div>매달</div><div>급여 수입</div></div>
    </div>
  </div>
  <div class="s6-sum" id="s6-sum">금액 차이 = <span class="y">엄청남</span></div>
""",
"s7-pgwp": """
  <div class="tl-axis">시간 →</div>
  <div class="track" id="s7-tb">
    <div class="track-h y">불어 루트 · LMIA 면제</div>
    <div class="seg-row">
      <div class="seg seg-blue" id="s7-b1">어학 1~2년</div>
      <div class="seg seg-gold" id="s7-b2"><span>취업비자</span><span id="s7-b2t">&nbsp;· 일하는 한 계속 ∞</span></div>
    </div>
  </div>
  <div class="track" id="s7-ta">
    <div class="track-h">일반 유학 → PGWP</div>
    <div class="seg-row">
      <div class="seg seg-gray" id="s7-a1">유학 1~3년</div>
      <div class="seg seg-gray2" id="s7-a2">PGWP 최대 3년</div>
      <div class="endcap" id="s7-end">끝</div>
    </div>
  </div>
  <div class="s7-note" id="s7-note">취업은 더 빠르게 · 기간 제한 없이</div>
""",
"s8-cta": """
  <div class="cta-logo" id="s8-logo">AA CANADA</div>
  <div class="cta-sub" id="s8-sub">캐나다 자녀무상교육 · 유학 후 이민 · 영주권</div>
  <div class="cta-cities" id="s8-cities">몬트리올 · 밴쿠버 · 토론토 · 런던</div>
  <div class="cta-btn" id="s8-btn">몬트리올 불어 루트 상담 신청</div>
""",
}

scene_divs, cap_divs = [], []
for i, s in enumerate(T["scenes"]):
    scene_divs.append(
        f'<section id="{s["id"]}" class="clip scene" data-start="{r(s["start"])}" data-duration="{r(s["duration"])}" data-track-index="1">'
        f'<div class="stage" id="{s["id"]}-in">{SCENES[s["id"]]}</div></section>')
    for j, c in enumerate(s["captions"]):
        cap_divs.append(
            f'<div id="cap-{i}-{j}" class="clip cap" data-start="{r(c["start"])}" data-duration="{r(c["end"] - c["start"])}" data-track-index="2">'
            f'<div class="cap-box" id="cap-{i}-{j}-box"><span class="cap-text">{cap_html(c["text"])}</span></div></div>')

page = (ROOT / "tools" / "template.html").read_text()
page = (page.replace("__TOTAL__", r(TOTAL))
            .replace("__SCENES__", "\n      ".join(scene_divs))
            .replace("__CAPTIONS__", "\n      ".join(cap_divs))
            .replace("__TIMING__", json.dumps(T, ensure_ascii=False)))
(ROOT / "index.html").write_text(page)
print("index.html written; total", TOTAL)
