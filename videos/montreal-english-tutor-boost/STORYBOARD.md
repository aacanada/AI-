---
format: 1080x1920
duration: 58s
message: "몬트리올 영어학교는 친구들과 100% 영어로 소통해 영어권과 같고, 아낀 생활비 일부로 원어민 튜터를 붙이면 영어가 확실하게 빨리 는다"
arc: concept-explainer
audience: 캐나다 자녀무상교육을 알아보는 학부모
mode: autonomous
music: none
---

## Video direction

- **canvas & palette (frame.md):** 1080×1920 portrait. Ground = cream `bg` #fdfae7 on every frame (full-bleed background clip). Headlines near-black `text` #111111; the ONE accent is cobalt `primary` #1e2bfa — key words, numbers, check marks, the CTA pill. `negative` #dc2626 only for strike/X marks (the "불어권이라 안 된다" myth, the crossed-out car costs); `positive` #059669 only for the single check in Frame 2. Cards = tinted cobalt 4% fill + 20% 1.5px border + 14px radius, NO shadows. Atmosphere (diagonal cobalt-tint band, 3×3 dot grid, concentric rings) only on Frame 1 and Frame 9.
- **type:** Pretendard only (local @font-face from frame.md — paste that <style> block; never link web fonts). Korean hero words 900/800 weight, very large (2–6 Korean words per line max). Latin digits for numbers. Eyebrow chips = small cobalt pill tags.
- **portrait layout:** stack vertically; hero around y≈800; all primary content inside y 220–1580 — the bottom band (y > 1590) is reserved for Korean captions. Persistent 3px cobalt progress strip at the very bottom edge growing with frame index (frame N of 9).
- **money is minor:** amounts appear only as small tags/labels ("연 $8,000+ 절약", "아낀 학비로 주 4회 가능", two small bar labels in Frame 4). No equations, no big count-ups of money. The tutor's VALUE (Frame 7) is the hero of the back half.
- **motion grammar:** smooth long-tail settles (`power3`), no bounce/overshoot. Every element reveals ON its spoken word (times below are seconds from the frame's start, from the real voice timings). No front-loading; holds are still. No repeat/yoyo, no randomness. Entrances via fromTo. Each frame ends with ~0.8s of narration-free hold — keep the final state still.
- **rhythm:** Frames 1, 2, 6 are high-energy. Frame 4 is a quick data hit. Frame 7 is the richest build (4 benefit cards). Frame 9 resolves to the lockup.
- **negative list:** no purple/blue AI gradients, no bokeh, no stock-photo look, no flag/maple-leaf overload (one small maple-leaf glyph allowed in Frame 9 only), no English-only headlines (Korean first; English only as small labels or kids' speech bubbles in Frame 2). No slideshow (front-load-then-freeze) and no screensaver (everything drifting). Do not write "수업이 100% 영어" anywhere — it is "친구들과 100% 영어로 소통".

## Frame 1 — 후킹

- scene: 4개 도시 칩(밴쿠버·토론토·런던·몬트리올)이 떠오르고, 큰 질문 "영어가 가장 빨리 느는 도시는?"이 착지
- voiceover: "캐나다 자녀무상교육, 영어가 가장 빨리 느는 도시는 어디일까요?"
- duration: 4.768s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Curiosity gap (question)
- beat: Intrigue
- blueprint: kinetic-type-beats (Adapt)
- focal: the hero question line "영어가 가장 빨리 느는 도시는?"
- roles: cream ground + diagonal cobalt-tint band + 3×3 dot grid = background · hero question = foreground subject · eyebrow pill "캐나다 자녀무상교육" + 4 city chips = supporting

narrativeRole: 학부모가 이미 궁금해하는 질문(어느 도시가 영어에 제일 좋을까)을 던진다.
keyMessage: 영어가 가장 빨리 느는 도시는 어디일까?

Scene 1 (0.0–1.6s): on "캐나다"(0.24s) eyebrow pill "캐나다 자녀무상교육" settles in upper third (y≈330); on "자녀무상교육"(0.62s) four small city chips "밴쿠버 · 토론토 · 런던 · 몬트리올" rise in a 2×2 grid around y≈520, index-staggered.
Scene 2 (1.6–3.2s): on "영어가"(1.64s) hero line "영어가" slams in huge near-black at y≈800 (`kinetic-beat-slam`); on "빨리"(2.32s) second line "가장 빨리 느는" slams with "빨리" in cobalt.
Scene 3 (3.2–4.77s): on "도시는"(2.78s) third line "도시는?" lands; on "어디일까요?"(3.16s) a big cobalt "?" mark pops at the right edge and the 4 city chips dim to 40% except "몬트리올", which gains a cobalt outline (foreshadowing). Hold still.

## Frame 2 — 불어권 오해 → 친구들과 100% 영어

- scene: "몬트리올 = 불어권?" 말풍선이 빨간 취소선으로 지워지고, "영어교육청 영어학교" 도장 → 아이들 영어 말풍선 → "친구들과 100% 영어 소통" → "= 영어권 도시와 똑같아요"
- voiceover: "몬트리올은 불어권이라 안 된다고요? 영어교육청 소속 영어학교에 가면, 친구들과 100% 영어로 소통합니다. 영어권 도시에 가는 것과 똑같아요."
- duration: 11.564s
- transition_in: push-slide UP
- status: outline
- src: compositions/frames/02-english-school.html
- type: product_intro
- persuasion: Myth → fact reversal
- beat: Relief
- blueprint: kinetic-type-beats (Adapt)
- focal: the hero claim "친구들과 100% 영어로 소통" with "100%" in big cobalt
- roles: cream ground = background · myth bubble then hero claim = foreground subject · stamp card "영어교육청 영어학교" + 3 kids' speech bubbles ("Hi!", "Wanna play?", "Me too!") + equation chip "= 영어권 도시" = supporting

narrativeRole: "불어권이라 안 된다"는 오해를 깨고, 영어학교에서는 친구들과 100% 영어로 소통한다는 사실을 세운다.
keyMessage: 영어학교에 가면 친구들과 100% 영어로 소통한다 — 영어권 도시와 같다.

Scene 1 (0.0–2.8s): on "몬트리올은"(0.22s) a speech-bubble card "몬트리올은 불어권이라…" pops in upper-middle (y≈520); on "안 된다고요?"(1.40s) a thick red strike line sweeps left→right across it and the bubble dims to 35% (`css-marker-patterns`).
Scene 2 (2.8–5.3s): on "영어교육청"(2.90s) a tinted stamp card "영어교육청 소속 영어학교" with a small school glyph slams down at y≈760 (scale 1.15→1, power3); on "영어학교에"(4.02s) a small cobalt check badge appears on the card corner (`positive` green check).
Scene 3 (5.3–8.4s): on "친구들과"(5.36s) three kids' speech bubbles ("Hi!", "Wanna play?", "Me too!") pop around the card, index-staggered; on "100%"(6.02s) the hero line "친구들과 100% 영어로 소통" lands at y≈1120 with "100%" huge cobalt (`counting-dynamic-scale` 0→100, value-scaled, ~0.6s).
Scene 4 (8.4–11.56s): on "영어권"(8.52s) an equation chip "= 영어권 도시와 똑같아요" slides up under the hero line; on "똑같아요"(10.08s) the "=" turns cobalt. Hold still.

## Frame 3 — 대도시인데 렌트는 중소도시

- scene: 위 카드 "도시 규모 · 캐나다 2위 대도시"(긴 막대) / 아래 카드 "렌트비 · 중소도시 수준"(짧은 막대) 대비
- voiceover: "캐나다 두 번째 대도시인데, 렌트비는 중소도시 수준입니다."
- duration: 4.815s
- transition_in: crossfade
- status: outline
- src: compositions/frames/03-rent.html
- type: social_proof
- persuasion: Contrast (big city vs small-city rent)
- beat: Surprise
- blueprint: comparison-split (Adapt)
- focal: two stacked comparison cards with qualitative bars (no numbers)
- roles: cream ground = background · two cards with bars = foreground subject · eyebrow "몬트리올" + skyline silhouette strip = supporting

narrativeRole: 몬트리올이 대도시이면서도 렌트가 저렴하다는 첫 번째 비용 근거.
keyMessage: 캐나다 2위 대도시, 렌트는 중소도시 수준.

Scene 1 (0.0–1.8s): eyebrow pill "몬트리올" + a simple cobalt-tint skyline silhouette strip draws in at top (y≈300) (`svg-path-draw`); on "두 번째"(0.64s) top card "도시 규모" appears with a big cobalt badge "캐나다 2위"; on "대도시인데"(1.10s) its bar grows to near full width (`stat-bars-and-fills`).
Scene 2 (1.8–4.82s): on "렌트비는"(1.82s) bottom card "렌트비" slides in at y≈1050; on "중소도시"(2.60s) its bar grows only to ~40% and a label "중소도시 수준" settles at the bar end in cobalt; on "수준입니다"(3.14s) a small down-arrow tag "↓ 저렴" pops beside it. Hold.

## Frame 4 — 부모 학비 최저

- scene: 두 개의 가로 막대 — "온타리오 대학부설 약 $20,000" vs "몬트리올 사립컬리지 $12,000", 몬트리올 막대에 "가장 저렴" 배지
- voiceover: "부모님이 다니는 컬리지 학비도, 가장 저렴합니다."
- duration: 3.912s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/04-tuition.html
- type: social_proof
- persuasion: Data point
- beat: Confirmation
- blueprint: dataviz-countup (Adapt)
- focal: the short cobalt bar "몬트리올 사립컬리지" with the badge "가장 저렴"
- roles: cream ground = background · two horizontal bars (grey vs cobalt) = foreground subject · eyebrow "부모님 학비 (1년)" = supporting

narrativeRole: 부모 학비가 가장 저렴하다는 두 번째 비용 근거 — 숫자는 막대 라벨로만 작게.
keyMessage: 부모 컬리지 학비도 몬트리올이 가장 저렴.

Scene 1 (0.0–1.4s): on "부모님이"(0.32s) eyebrow pill "부모님 학비 · 1년" at y≈420; on "컬리지"(1.14s) a grey bar "온타리오 대학부설" grows to full width at y≈700 with small label "약 $20,000" (`stat-bars-and-fills`).
Scene 2 (1.4–3.91s): on "학비도"(1.44s) a cobalt bar "몬트리올 사립컬리지" grows to 60% at y≈900 with small label "$12,000"; on "가장"(1.92s)/"저렴합니다"(2.28s) a cobalt badge "가장 저렴" stamps at its end. Hold.

## Frame 5 — 차 없이 생활

- scene: 자동차 아이콘에 빨간 X → "보험료"·"주차비" 카드가 떨어져 나감 → 지하철·버스 노선이 그려지며 "차 없이 OK"
- voiceover: "자녀와 함께 가도, 차 없이 생활할 수 있는 거의 유일한 도시. 보험료도, 주차비도 아낍니다."
- duration: 7.213s
- transition_in: crossfade
- status: outline
- src: compositions/frames/05-no-car.html
- type: feature_showcase
- persuasion: Concretization (car costs disappear)
- beat: Relief
- blueprint: comparison-split (Adapt)
- focal: a simple line-icon car that gets a red X, with cost cards falling away
- roles: cream ground = background · car icon + X = foreground subject · cost cards "보험료", "주차비" + metro/bus line diagram + hero line "차 없이 생활" = supporting

narrativeRole: 자녀 동반 가정도 차 없이 살 수 있다 — 보험료·주차비 절약이라는 세 번째 비용 근거.
keyMessage: 차 없이 생활 가능한 거의 유일한 도시 → 보험료·주차비 절약.

Scene 1 (0.0–1.5s): on "자녀와"(0.50s) eyebrow "자녀 동반 가족" + a small family glyph (parent + child) at y≈330; on "함께"(0.88s) a line-icon car draws in at center y≈700 (`svg-path-draw`).
Scene 2 (1.5–4.6s): on "차"(1.58s)/"없이"(1.78s) a red X slams over the car; on "생활할"(2.08s) a metro/bus line diagram (3 cobalt lines with station dots) draws across behind it; on "유일한"(3.22s) hero line "차 없이 생활" lands at y≈1050 with a small cobalt tag "거의 유일한 도시" (3.64s).
Scene 3 (4.6–7.21s): on "보험료도"(4.70s) a card "보험료" pops off the car and falls away with a red strike; on "주차비도"(5.26s) a second card "주차비" does the same; on "아낍니다"(5.68s) a cobalt pill "절약" settles under the hero line. Hold.

## Frame 6 — 압도적으로 저렴

- scene: 렌트·학비·자동차 아이콘 세 개가 저금통 하나로 모이고, "캐나다 어느 도시보다 압도적으로 저렴" + 작은 꼬리표 "연 $8,000+ 절약"
- voiceover: "모두 합치면, 캐나다 어느 도시보다 압도적으로 저렴합니다."
- duration: 4.565s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/06-cheapest.html
- type: benefit_highlight
- persuasion: Sum-up
- beat: Conviction
- blueprint: kinetic-type-beats (Adapt)
- focal: the hero word "압도적으로" in big cobalt over a simple piggy-bank glyph
- roles: cream ground = background · hero line = foreground subject · three small icon chips (렌트 · 학비 · 자동차) + piggy-bank glyph + small tag "연 $8,000+ 절약" = supporting

narrativeRole: 세 가지 절약을 하나로 묶어 "압도적으로 저렴"이라는 결론을 낸다 — 금액은 작은 꼬리표 하나만.
keyMessage: 모두 합치면 캐나다 어느 도시보다 압도적으로 저렴하다.

Scene 1 (0.0–1.5s): on "모두"(0.22s) three icon chips "렌트", "학비", "자동차" appear in a row at y≈450; on "합치면"(0.50s) they slide together and drop into a simple cobalt-outline piggy-bank glyph at y≈640 (`center-outward-expansion` reversed — converge).
Scene 2 (1.5–4.57s): on "캐나다"(1.50s) line "캐나다 어느 도시보다" reveals at y≈880; on "압도적으로"(2.48s) hero word "압도적으로" slams in huge cobalt (`kinetic-beat-slam`); on "저렴합니다"(3.00s) the line "저렴" lands under it and a SMALL tag "연 $8,000+ 절약" settles beside the piggy bank (small, muted — not a hero). Hold.

## Frame 7 — 원어민 튜터의 힘

- scene: 저금통에서 화살표가 "원어민 튜터" 카드로 이어지고(작은 글씨 "아낀 학비로 주 4회 가능"), 튜터 효용 카드 4장 — 1:1 맞춤 · 학교 수업 따라잡기 · 말문 트기 · 자신감 — 이 차례로 켜진다
- voiceover: "아낀 돈의 일부로 원어민 튜터를 붙이면, 아이 수준에 맞춘 1:1 수업으로 학교 적응도, 영어도 훨씬 빨라집니다."
- duration: 8.091s
- transition_in: push-slide UP
- status: outline
- src: compositions/frames/07-tutor.html
- type: feature_showcase
- persuasion: Benefit stack
- beat: Hope
- blueprint: grid-card-assemble (Adapt)
- focal: a 2×2 grid of benefit cards under a "원어민 튜터" header card
- roles: cream ground = background · 2×2 benefit cards = foreground subject · header card "원어민 튜터" with small piggy-bank → arrow + small note "아낀 학비로 주 4회 가능" = supporting

narrativeRole: 아낀 돈의 일부를 원어민 튜터에 쓰면 어떤 효과가 있는지 — 이 영상의 핵심 가치.
keyMessage: 1:1 맞춤 원어민 튜터로 학교 적응도, 영어도 훨씬 빨라진다.

Scene 1 (0.0–2.6s): on "아낀"(0.08s) a small piggy-bank glyph at upper-left (y≈300) with an arrow drawing right (`svg-path-draw`); on "원어민"(1.00s)/"튜터를"(1.38s) header card "원어민 튜터" lands at y≈360 with a small person+book glyph; on "붙이면"(1.90s) a small muted note "아낀 학비로 주 4회 가능" settles under the header.
Scene 2 (2.6–8.09s): 2×2 cards (y≈620–1380) light up one by one, each with a cobalt icon + bold title + one short line (`stat-bars-and-fills` not needed — plain card reveal, scale 0.96→1 + opacity): card 1 "1:1 맞춤" / "아이 수준에 딱 맞게" on "1:1"(3.60s); card 2 "학교 수업 따라잡기" / "숙제·읽기·쓰기" on "학교"(4.66s); card 3 "말문 트기" / "틀려도 괜찮은 대화 연습" on "영어도"(5.42s); card 4 "자신감" / "먼저 말하는 아이" on "빨라집니다"(6.34s), and all 4 cards get a thin cobalt top accent line at 6.6s. Hold.

## Frame 8 — 학교 + 튜터 = 확실한 향상

- scene: 두 갈래 — 🏫 학교 "친구들과 매일 영어" + 👩‍🏫 튜터 "체계적으로" — 가 합쳐지며 성장 곡선이 위로 꺾이고, "적응기" 구간이 짧아진다
- voiceover: "학교에서는 친구들과 영어로 어울리며 자연스럽게, 튜터와는 체계적으로 빠르게. 그래서 확실하게 늘어납니다."
- duration: 8.425s
- transition_in: crossfade
- status: outline
- src: compositions/frames/08-growth.html
- type: benefit_highlight
- persuasion: Synthesis (two engines → one curve)
- beat: Confidence
- blueprint: dataviz-countup (Adapt)
- focal: an English-growth curve that bends sharply upward when the two lanes merge
- roles: cream ground = background · growth curve chart = foreground subject · two lane cards "학교 · 자연스럽게" and "튜터 · 체계적으로" + label "영어 실력" + small "적응기" bracket that shrinks = supporting

narrativeRole: 학교(자연스러운 소통)와 튜터(체계적 학습)가 합쳐져 영어가 확실하게 는다는 결론.
keyMessage: 학교에서 자연스럽게 + 튜터로 체계적으로 = 확실한 향상.

Scene 1 (0.0–3.4s): on "학교에서는"(0.28s) lane card "학교" (school glyph) slides in at upper-left y≈340; on "친구들과"(1.00s) its sub-line "친구들과 매일 영어" appears; on "자연스럽게"(2.46s) a gentle grey dashed curve starts drawing in the chart area (y≈700–1300) (`svg-path-draw`).
Scene 2 (3.4–6.0s): on "튜터와는"(3.52s) lane card "튜터" (person+book glyph) slides in at upper-right; on "체계적으로"(4.46s) its sub-line "체계적으로" appears; on "빠르게"(5.06s) two arrows from both cards meet at the curve.
Scene 3 (6.0–8.43s): on "그래서"(6.06s) a solid cobalt curve redraws over the grey one, bending upward much sooner; a small "적응기" bracket under the start shrinks; on "확실하게"(6.50s) label "영어 실력 ↑" pops at the curve's end; on "늘어납니다"(6.92s) a cobalt pill "확실하게" settles. Hold.

## Frame 9 — CTA

- scene: "몬트리올 자녀무상교육" 라인 → AA Canada 워드마크 + "상담 문의" 필 + 연락처
- voiceover: "몬트리올 자녀무상교육, AA캐나다와 상담하세요."
- duration: 4.906s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/09-cta.html
- type: cta
- persuasion: Direct ask
- beat: Resolve
- blueprint: logo-assemble-lockup (Adapt)
- focal: the "AA Canada" wordmark lockup with the cobalt CTA pill "상담 문의"
- roles: cream ground + concentric cobalt rings + dot grid = background · wordmark = foreground subject · line "몬트리올 자녀무상교육" with tiny "Montréal" label + one small maple-leaf glyph, contact line "카카오톡 canlog · 02-567-4345" = supporting

narrativeRole: 행동을 요청하고 AA Canada로 연결한다.
keyMessage: 몬트리올 자녀무상교육은 AA Canada와 상담하세요.

Scene 1 (0.0–1.6s): on "몬트리올"(0.32s) a line "몬트리올" lands at y≈520 with tiny "Montréal" label + maple-leaf glyph; on "자녀무상교육"(0.74s) "자녀무상교육" lands under it.
Scene 2 (1.6–4.91s): on "AA캐나다와"(1.66s) the wordmark "AA Canada" assembles at y≈820 (`scale-swap-transition`) with sub-line "캐나다 유학·이민 전문"; on "상담하세요"(2.66s) a cobalt CTA pill "상담 문의" settles beneath (y≈1030) and a muted contact line "카카오톡 canlog · 02-567-4345" fades in at y≈1140. Hold to the end.
