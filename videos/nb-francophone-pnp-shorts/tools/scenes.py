# Scene bodies for the visual zone (y 560–1440), keyed by scene id in script.json.
SCENES = {
"s1-hook": """
  <div class="pill" id="s1-pill">캐나다 영주권 · 불어 루트</div>
  <div class="s1-q" id="s1-q">
    <div class="s1-level"><span class="s1-fr">FR</span><span>불어 중하 레벨</span></div>
    <div class="s1-arrow" id="s1-arrow">↓</div>
    <div class="s1-pr">영주권<span class="y">?</span></div>
  </div>
  <div class="s1-answer" id="s1-answer">
    <div class="s1-pin"><svg viewBox="0 0 24 24" width="120" height="120"><path fill="#E63946" d="M12 2C7.6 2 4 5.6 4 10c0 5.6 8 12 8 12s8-6.4 8-12c0-4.4-3.6-8-8-8zm0 11a3 3 0 110-6 3 3 0 010 6z"/></svg></div>
    <div class="s1-city">뉴브런즈윅</div>
    <div class="s1-bar" id="s1-bar"></div>
    <div class="s1-sub">NEW BRUNSWICK · NB PNP</div>
  </div>
""",
"s2-route": """
  <div class="map" id="s2-map">
    <svg class="map-svg" viewBox="0 0 960 520" width="960" height="520">
      <path id="s2-path" d="M 170 380 C 330 120, 640 100, 790 300" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900"/>
      <circle id="s2-dot1" cx="170" cy="380" r="34" fill="#2f6bff" stroke="#fff" stroke-width="8"/>
      <circle id="s2-dot2" cx="790" cy="300" r="34" fill="#e63946" stroke="#fff" stroke-width="8"/>
    </svg>
    <div class="city-lbl" id="s2-l1" style="left:40px;top:430px">몬트리올<small>QUÉBEC</small></div>
    <div class="city-lbl" id="s2-l2" style="left:620px;top:368px">뉴브런즈윅<small>NEW BRUNSWICK</small></div>
    <div class="plane" id="s2-plane">C16</div>
  </div>
  <div class="steps">
    <div class="step" id="s2-st1"><b>1</b>불어 5레벨<small>퀘벡 정부 불어수업</small></div>
    <div class="step" id="s2-st2"><b>2</b>LMIA 면제<small>Francophone Mobility</small></div>
    <div class="step step-win" id="s2-st3"><b>3</b>NB 취업<small>C16 워크퍼밋</small></div>
  </div>
""",
"s3-stream": """
  <div class="tree">
    <div class="t-root" id="s3-root">NB PNP<small>뉴브런즈윅 주정부이민</small></div>
    <div class="t-line" id="s3-line1"></div>
    <div class="t-mid" id="s3-mid"><div>New Brunswick</div><div>Strategic Initiative</div></div>
    <div class="t-line" id="s3-line2"></div>
    <div class="t-leaf" id="s3-leaf"><span class="tag">불어권 전용</span>불어권 근로자 경로<small>Francophone Workers in New Brunswick</small></div>
  </div>
""",
"s4-req": """
  <div class="req-h" id="s4-h">기본 요건 체크</div>
  <div class="req" id="s4-r1"><div class="cb">✓</div><div><div class="ct">NB 정규직 풀타임</div><div class="cs">12개월 이상 운영한 NB 고용주</div></div></div>
  <div class="req" id="s4-r2"><div class="cb">✓</div><div><div class="ct">NB 거주 6개월</div><div class="cs">C16으로 일하며 거주</div></div></div>
  <div class="req" id="s4-r3"><div class="cb">✓</div><div><div class="ct">불어 NCLC 5</div><div class="cs">말하기·듣기·읽기·쓰기</div></div></div>
  <div class="req" id="s4-r4"><div class="cb">✓</div><div><div class="ct">고졸 이상 + 경력 1년</div><div class="cs">최근 5년 · 선발 점수 65점 이상</div></div></div>
""",
"s5-nclc": """
  <div class="adv" id="s5-adv">장점 ①</div>
  <div class="gauge" id="s5-gauge">
    <div class="g-title">불어 요구 수준 (NCLC)</div>
    <div class="g-track">
      <div class="g-fill" id="s5-fill"></div>
      <div class="g-tick" style="left:0%">1</div><div class="g-tick" style="left:22.2%">3</div>
      <div class="g-tick" style="left:44.4%">5</div><div class="g-tick" style="left:66.6%">7</div>
      <div class="g-tick" style="left:88.8%">9</div>
    </div>
    <div class="g-mark g-ee" id="s5-ee" style="left:66.6%"><div class="g-flag"><div>익스프레스 엔트리</div><div>불어 선발</div></div><div class="g-num">7</div></div>
    <div class="g-mark g-nb" id="s5-nb" style="left:44.4%"><div class="g-num">5</div><div class="g-flag"><div>NB 불어권</div><div>근로자 경로</div></div></div>
  </div>
  <div class="s5-ok" id="s5-ok">NCLC 5로 <span class="y">OK!</span></div>
""",
"s6-flow": """
  <div class="adv" id="s6-adv">장점 ②</div>
  <div class="flow-card" id="s6-card">
    <div class="fc-h">C16 워크퍼밋으로 NB 근무</div>
    <div class="fc-track"><div class="fc-fill" id="s6-fill"></div>
      <div class="fc-pt" id="s6-p1" style="left:50%"><div class="fc-dot">✓</div><div class="fc-lbl"><div>6개월</div><b>거주 요건</b></div></div>
      <div class="fc-pt" id="s6-p2" style="left:100%"><div class="fc-dot">✓</div><div class="fc-lbl"><div>1년</div><b>경력 요건</b></div></div>
    </div>
    <div class="fc-axis"><span>시작</span></div>
  </div>
  <div class="s6-sum" id="s6-sum">일하는 동안 <span class="y">저절로 충족</span></div>
""",
"s7-priority": """
  <div class="adv" id="s7-adv">장점 ③</div>
  <div class="prio-label" id="s7-label">2026년 7월 · NB 주정부 초청</div>
  <div class="prio-num"><span id="s7-num">0</span><small>명</small></div>
  <div class="prio-sub" id="s7-sub">불어권 대상 Strategic Initiative</div>
  <div class="prio-badge" id="s7-badge">그날 최대 규모</div>
""",
"s8-tip": """
  <div class="tip-h" id="s8-h">⚠ 꼭 챙길 포인트</div>
  <div class="skills">
    <div class="sk-row"><div class="sk-name">C16 워크퍼밋</div>
      <div class="sk on" id="s8-a1">말하기</div><div class="sk on" id="s8-a2">듣기</div><div class="sk off" id="s8-a3">읽기</div><div class="sk off" id="s8-a4">쓰기</div></div>
    <div class="sk-row"><div class="sk-name y">NB 주정부</div>
      <div class="sk on" id="s8-b1">말하기</div><div class="sk on" id="s8-b2">듣기</div><div class="sk on hot" id="s8-b3">읽기</div><div class="sk on hot" id="s8-b4">쓰기</div></div>
  </div>
  <div class="tip-sum" id="s8-sum">4영역 모두 <span class="y">NCLC 5</span></div>
""",
"s9-cta": """
  <div class="cta-logo" id="s9-logo">AA CANADA</div>
  <div class="cta-sub" id="s9-sub">캐나다 자녀무상교육 · 유학 후 이민 · 영주권</div>
  <div class="cta-cities" id="s9-cities">몬트리올 · 밴쿠버 · 토론토 · 런던</div>
  <div class="cta-btn" id="s9-btn">불어 영주권 루트 상담 신청</div>
""",
}
