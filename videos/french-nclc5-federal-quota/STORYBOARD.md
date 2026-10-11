---
format: 1080x1920
duration: 110s
message: "불어 NCLC 5(중하 수준)만 있으면, 주정부 쿼터 점수 경쟁과 분리된 연방 5,000개 TO를 쓸 수 있다"
arc: concept-explainer
audience: 캐나다 주정부 이민(영주권)을 고민하는 한국인
mode: autonomous
music: none
---

## Video direction

- **canvas & palette (frame.md):** 1080×1920 portrait. Ground = cream `bg` #fdfae7 on every frame (full-bleed background clip). Headlines near-black `text` #111111; the ONE accent is cobalt `primary` #1e2bfa — every number, the federal "5,000", checkmarks, the short "French" line, the CTA pill. `negative` #dc2626 only for the X / "quota exhausted" marks and the rising cutline; `positive` #059669 only for the single check in Frame 5. Cards = tinted cobalt 4% fill + 20% 1.5px border + 14px radius, NO shadows. Atmosphere (diagonal cobalt-tint band, 3×3 dot grid, concentric rings) only on Frame 1 and Frame 10.
- **type:** Pretendard only (local @font-face from frame.md — paste that <style> block; never link web fonts). Korean hero words 900/800 weight, very large (portrait: few words per line, 2–6 Korean words per line max). Latin digits for all numbers. Eyebrow chips = small cobalt pill tags.
- **portrait layout:** stack vertically; hero anchored around y≈806; all primary content inside the top ~83% (y < 1590) — bottom band reserved for Korean captions. Persistent 3px cobalt progress strip at the very bottom edge growing with frame index (frame N of 10).
- **motion grammar:** smooth long-tail settles (`power3`), no bounce/overshoot. Every element reveals ON its spoken word (times below are seconds from the frame's start, taken from the real voice timings). No front-loading; nothing floats; holds are still (subtle jitter at most). No repeat/yoyo, no randomness. Entrances via fromTo.
- **rhythm / held frames:** Frames 1, 4, 8 are high-energy (kinetic slams, count-up). Frame 6 and Frame 9 are calm breathers (one restrained move then a still hold). Frame 10 builds to the lockup.
- **negative list:** no purple/blue AI gradients, no bokeh, no stock-photo look, no flags/maple-leaf clip-art overload (one simple maple-leaf glyph allowed in Frame 10 only), no browser chrome/cursors, no English-only headlines (Korean first; English/French only as small labels like "NCLC 5", "Express Entry"). Never claim specific provinces. No slideshow (front-load-then-freeze) and no screensaver (everything drifting).

## Frame 1 — 후킹

- scene: 크림 바탕에 굵은 한글 타이포가 비트마다 바뀌며 "점수 경쟁" → "빠져나오는 방법"으로 착지
- voiceover: "캐나다 주정부 이민, 요즘 점수 경쟁 너무 치열하죠? 그런데 불어 하나로, 이 경쟁에서 아예 빠져나오는 방법이 있습니다."
- duration: 7.755s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Pain validation + Counterintuitive claim
- beat: Recognition + intrigue
- blueprint: kinetic-type-beats (Adapt)
- focal: the hero word line "점수 경쟁" that gets struck through and replaced
- roles: cream ground + diagonal cobalt-tint band + 3×3 dot grid = background · hero Korean type = foreground subject · small eyebrow pill "캐나다 주정부 이민" = supporting

narrativeRole: 시청자가 이미 느끼는 '점수 경쟁 피로'를 건드리고, 불어라는 의외의 탈출구로 호기심을 연다.
keyMessage: 불어 하나로 주정부 점수 경쟁에서 빠져나올 수 있다.


Adapt: keep the in-place token swap signature; the swap is "점수 경쟁" → "빠져나오는 법".
Scene 1 (0.0–1.4s): eyebrow pill "캐나다 주정부 이민" springs in upper third (smooth settle). Centered, layered depth.
Scene 2 (1.4–3.3s): on "점수 경쟁"(1.5s) the hero line "점수 경쟁" slams in huge near-black at y≈700 (kinetic beat-slam → `kinetic-beat-slam`); on "치열하죠?"(2.6s) a small row of 5 stacked score chips (72 · 75 · 78 · 81 · 84) jitters/shoves beneath it to say "crowded".
Scene 3 (3.3–5.6s): on "불어 하나로"(4.0s) a thick cobalt strike line sweeps left→right across "점수 경쟁", the score chips dim to 30%; a cobalt pill "불어 하나로" enters under it.
Scene 4 (5.6–7.75s): on "빠져나오는"(6.0s) hard in-place token swap (`discrete-text-sequence`): the struck line is replaced by "경쟁에서 빠져나오는 법" with "빠져나오는" in cobalt; holds still to the end.

## Frame 2 — 쿼터는 한정, 지원자는 넘친다

- scene: 작은 쿼터 상자 하나 옆으로 지원자 점(dot)들이 끝없이 쌓여 넘친다
- voiceover: "주정부 이민은 주마다, 1년에 노미니를 줄 수 있는 숫자, 즉 쿼터가 정해져 있습니다. 그런데 지원자는, 쿼터보다 훨씬 많습니다."
- duration: 9.242s
- transition_in: push-slide UP
- status: outline
- src: compositions/frames/02-quota.html
- type: pain_point
- persuasion: Concretization (abstract quota → a box that overflows)
- beat: Concern
- blueprint: overwhelm-surround (Adapt)
- focal: a small cobalt-outlined box labeled "쿼터" that overflows with applicant dots
- roles: cream ground = background · quota box = foreground subject · applicant dots (near-black, small circles) = supporting · eyebrow + title = supporting

narrativeRole: '쿼터'라는 추상 개념을 넘치는 상자로 구체화해 경쟁이 생기는 이유를 보여준다.
keyMessage: 쿼터는 정해져 있고, 지원자는 훨씬 많다.


Adapt: keep the accumulation-until-overwhelm signature, but the crowd is applicant dots flooding past a fixed-size quota box (no avatar morph).
Scene 1 (0.0–2.5s): eyebrow pill "주정부 이민" + title "주마다 정해진 숫자" per-word reveal (`dynamic-content-sequencing`) in upper third.
Scene 2 (2.5–6.4s): on "1년에 노미니를"(2.6s) a tinted card "1년 노미니 수" draws in center (y≈800) as an outlined box (`svg-path-draw`); on "쿼터가"(5.2s) its label flips to big "쿼터" in cobalt with a small lock icon — the box is fixed-size.
Scene 3 (6.4–9.24s): on "지원자는"(6.8s) applicant dots pour in from top and both sides in an index-staggered cascade (`center-outward-expansion`), filling the box then spilling around and below it; on "훨씬 많습니다"(8.1s) a counter chip "지원자 ≫ 쿼터" pops beside the box; the crowd settles and holds (no drifting).

## Frame 3 — 점수 순 줄 세우기

- scene: 지원자 카드들이 점수 순으로 정렬되고, 커트라인 선이 위로 계속 올라가며 아래 카드들이 흐려진다
- voiceover: "그래서 요즘, 거의 모든 주정부가 점수를 매기고, 높은 점수부터 뽑는 방식으로 바뀌고 있습니다. 커트라인은 계속 올라가고, 몇 점 차이로 기회를 놓치는 분들이 정말 많습니다."
- duration: 11.703s
- transition_in: push-slide UP
- status: outline
- src: compositions/frames/03-score-race.html
- type: pain_point
- persuasion: Causal chain (부족한 쿼터 → 점수제 → 커트라인 상승)
- beat: Tension
- blueprint: dataviz-countup (Adapt)
- focal: a vertical ranked list of applicant score bars with a red CUT-OFF line climbing upward
- roles: cream ground = background · ranked score bars (cobalt-tinted cards with score numbers) = foreground subject · red cut-off line + label "커트라인" = supporting · title = supporting

narrativeRole: 쿼터 부족이 점수 경쟁과 커트라인 상승으로 이어지는 인과를 보여준다.
keyMessage: 모든 주정부가 점수 경쟁으로 바뀌고, 커트라인은 계속 오른다.


Adapt: keep the count-up signature on the cut-off number; the "chart" is a sorted ranking.
Scene 1 (0.0–2.6s): title "거의 모든 주정부가" per-word reveal in the upper third; on "주정부가"(2.0s) the next line "점수 경쟁으로" lands in cobalt.
Scene 2 (2.6–6.8s): on "점수를 매기고"(2.6s) 7 applicant cards (score 92, 88, 85, 81, 77, 73, 69) cascade in as a vertical ranked stack (`stat-bars-and-fills`, bar length ∝ score), index-staggered; on "높은 점수부터"(3.6s) they re-sort top-to-bottom by score with a smooth FLIP-like slide.
Scene 3 (6.8–9.0s): on "커트라인은"(6.9s) a red dashed horizontal line labeled "커트라인" appears at the bottom of the stack with a number counter; on "계속 올라가고"(7.4s) it climbs upward card by card while its counter counts up 68 → 84 (`counting-dynamic-scale`); cards below the line grey out to 25%.
Scene 4 (9.0–11.7s): on "몇 점 차이로"(8.5s) a small callout "-2점" flags the first greyed card just under the line (`css-marker-patterns` circle); holds still.

## Frame 4 — 연방 5,000개 TO

- scene: "2026 연방정부" 아이브로우 아래 큰 숫자 5,000이 카운트업, "불어권 전용 TO" 라벨
- voiceover: "그런데 2026년, 연방정부가 중요한 발표를 했습니다. 불어를 하는 이민자를 위해, 연방 몫으로 5,000개의 정원을 따로 마련한 겁니다."
- duration: 9.567s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/04-federal-5000.html
- type: product_intro
- persuasion: Statistical proof + Concept announcement
- beat: Surprise + orientation
- blueprint: dataviz-countup (Reproduce)
- focal: the giant cobalt number "5,000" counting up
- roles: cream ground + faint cobalt radial bloom behind the number = background · "5,000" = foreground subject · eyebrow "2026 · 연방정부 발표" + label "불어권 전용 TO" = supporting

narrativeRole: 해결책의 주인공인 '연방 불어권 전용 5,000개 TO'를 숫자로 등장시킨다.
keyMessage: 연방이 불어권 전용으로 5,000개 TO를 따로 마련했다.


Scene 1 (0.0–4.2s): on "2026년"(0.5s) an eyebrow pill "2026 · 연방정부" springs in at upper third; on "중요한 발표"(2.5s) a headline "연방정부의 새 발표" per-word reveals beneath it.
Scene 2 (4.2–7.3s): on "불어를 하는 이민자를 위해"(4.3s) a cobalt-tinted card "불어 사용 이민자 전용" slides up into the middle; a soft cobalt glow blooms (`ambient-glow-bloom`).
Scene 3 (7.3–9.57s): on "5,000개의"(7.4s) the hero number counts 0 → 5,000 in cobalt, value-scaled so the type grows as it climbs (`counting-dynamic-scale`), centered at y≈880 near full width; on "따로 마련한"(8.4s) a label "개 · 연방 별도 정원(TO)" settles under it. Hold.

## Frame 5 — 주정부 쿼터가 아니라 연방 쿼터

- scene: 두 개의 카드 — 왼쪽 "주정부 쿼터" 위에 X, 오른쪽 "연방 5,000 TO" 위에 체크, 노미니 아이콘이 오른쪽으로 들어간다
- voiceover: "핵심은 이겁니다. 주정부가 불어 점수 보유자에게 노미니를 주면, 그 숫자가 주정부 자기 쿼터에서 빠지지 않습니다. 연방이 따로 배정한 5,000개를 쓰는 거죠."
- duration: 11.331s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/05-separate-quota.html
- type: feature_showcase
- persuasion: Comparison of two options
- beat: "Aha"
- blueprint: comparison-split (Adapt)
- focal: two stacked cards — top "주정부 쿼터" (with red ✕ "소진 안 됨" outcome) and bottom "연방 5,000 TO" (with green ✓) — and a nominee token that drops into the bottom card
- roles: cream ground = background · two comparison cards = foreground subject · nominee token (cobalt circle with person glyph + "불어 NCLC 5") = supporting · title = supporting

narrativeRole: 불어권 노미니가 주 쿼터를 소진하지 않는다는 메커니즘을 대비로 보여준다.
keyMessage: 불어권 노미니는 주 쿼터가 아니라 연방 5,000개에서 나간다.


Adapt: portrait → stacked cards instead of side-by-side; keep the mirrored-tilt entrance and the badge spring-pop signature.
Scene 1 (0.0–1.3s): title "핵심은 이것" slams in upper third (`kinetic-beat-slam`).
Scene 2 (1.3–4.9s): on "주정부가"(1.3s) the nominee token appears above center; on "노미니를 주면"(3.1s) two cards enter from opposite sides with opposing tilts and settle stacked (`split-tilt-cards`): top "주정부 자기 쿼터" (neutral), bottom "연방 불어권 5,000 TO" (cobalt).
Scene 3 (4.9–8.3s): on "주정부 자기 쿼터에서"(5.9s) a small tally inside the top card stays at "-0" while a red ✕ badge pops on its edge with the words "차감 안 됨" (badge spring-pop, smooth); on "빠지지 않습니다"(7.3s) the top card dims slightly.
Scene 4 (8.3–11.33s): on "연방이 따로 배정한 5,000개를"(8.4s) the nominee token travels down into the bottom card, the card's counter ticks 5,000 → 4,999, and a green ✓ badge pops; holds still.

## Frame 6 — 두 개의 줄

- scene: 같은 무대에서 긴 줄(일반 점수 경쟁)과 짧은 줄(불어권 전용 창구)이 나란히, 사람 아이콘 하나가 짧은 줄로 옮겨간다
- voiceover: "쉽게 말하면, 모두가 서 있는 긴 줄이 아니라, 불어권 전용 창구에 따로 서는 겁니다."
- duration: 5.016s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/06-two-lines.html
- type: benefit_highlight
- persuasion: Analogy / metaphor (전용 창구)
- beat: Comprehension + relief
- blueprint: comparison-split (Adapt)
- focal: two queues — a long queue of grey person dots labeled "일반 점수 경쟁" and a short cobalt lane labeled "불어권 전용 창구"
- roles: cream ground = background · two queues = foreground subject · one highlighted cobalt person = supporting

narrativeRole: 메커니즘을 '전용 창구' 비유로 바꿔 직관적으로 이해시킨다.
keyMessage: 불어 점수가 있으면 일반 경쟁 줄과 분리된다.


Adapt: same stacked stage as Frame 5 (continuity), the comparison is two queues; calm breather — one move then hold.
Scene 1 (0.0–2.9s): on "모두가 서 있는 긴 줄"(0.9s) a long winding queue of ~24 grey person dots assembles index-staggered across the upper half under the label "일반 점수 경쟁" (`center-outward-expansion`).
Scene 2 (2.9–5.02s): on "불어권 전용 창구에"(3.0s) a short cobalt lane with a window icon labeled "불어권 전용 창구 · 연방 5,000" draws in below (`svg-path-draw`); one person dot lifts out of the long queue and glides to the front of the short lane, turning cobalt. Hold still.

## Frame 7 — 필요한 불어는 NCLC 5

- scene: "NCLC 5 = 중하 수준" 큰 타이포, 아래 듣기·말하기·읽기·쓰기 4개 칩이 하나씩 켜지며 5가 찍힌다
- voiceover: "그럼 불어를 얼마나 잘해야 할까요? 원어민 수준이어야 할 것 같지만, 아닙니다. 기준은 NCLC 5, 중하 수준입니다. 듣기, 말하기, 읽기, 쓰기, 네 영역 모두 5레벨이면 됩니다."
- duration: 11.61s
- transition_in: crossfade
- status: outline
- src: compositions/frames/07-nclc5.html
- type: feature_showcase
- persuasion: Question→answer pairing + Progressive disclosure
- beat: Surprise + confidence
- blueprint: grid-card-assemble (Adapt)
- focal: the badge "NCLC 5" with sub-label "중하 수준", then a 2×2 grid of skill cards each stamped "5"
- roles: cream ground = background · "NCLC 5" hero + 2×2 skill grid = foreground subject · question line and crossed-out "원어민 수준?" = supporting

narrativeRole: '불어는 어렵다'는 통념을 깨고 실제 요구 수준(NCLC 5, 4영역)을 보여준다.
keyMessage: 원어민이 아니라 중하 수준(NCLC 5)이면 된다.


Adapt: grid assembles in a 2×2 (portrait), one card per spoken skill.
Scene 1 (0.0–2.4s): question line "불어, 얼마나 잘해야 할까?" per-word reveal at upper third.
Scene 2 (2.4–5.2s): on "원어민 수준이어야"(2.5s) a card "원어민 수준?" appears center; on "아닙니다"(4.5s) a red strike crosses it out (`css-marker-patterns`) and it shrinks/dims away (scale-swap).
Scene 3 (5.2–7.7s): on "NCLC 5"(5.8s) the hero badge "NCLC 5" spring-settles big in cobalt at y≈760; on "중하 수준입니다"(6.8s) the pill "중하 수준" settles under it.
Scene 4 (7.7–11.61s): 2×2 grid below the badge assembles one card per word — "듣기"(7.8s) "말하기"(8.3s) "읽기"(8.8s) "쓰기"(9.3s) — each card carries a small cobalt "5"; on "네 영역 모두"(9.7s) a thin cobalt bracket wraps all four; hold.

## Frame 8 — 엄청난 장점

- scene: 막대 두 개 — Express Entry 불어 카테고리 NCLC 7(높은 막대) vs 연방 TO NCLC 5(낮은 막대), 이어 "중하 수준 불어 → 별도 TO" 결론 카드
- voiceover: "연방 익스프레스 엔트리 불어 카테고리가 7레벨을 요구하는 것과 비교하면, 문턱이 훨씬 낮습니다. 중하 수준의 불어 하나로, 치열한 쿼터 경쟁에서 분리된다는 것. 이건 정말, 엄청난 장점입니다."
- duration: 12.121s
- transition_in: crossfade
- status: outline
- src: compositions/frames/08-big-advantage.html
- type: benefit_highlight
- persuasion: Contrast (NCLC 7 vs NCLC 5) + Distillation
- beat: Conviction + delight
- blueprint: dataviz-countup (Adapt)
- focal: two vertical bars — "Express Entry 불어 카테고리 · NCLC 7" (tall, grey) vs "연방 불어권 TO · NCLC 5" (shorter, cobalt) — then the conclusion card "엄청난 장점"
- roles: cream ground = background · two bars = foreground subject (Scenes 1–2) · conclusion type = foreground subject (Scenes 3–4) · threshold labels = supporting

narrativeRole: 다른 경로와 비교해 문턱이 낮음을 보여주고 '엄청난 장점'이라는 결론을 못박는다.
keyMessage: 중하 수준 불어로 쿼터 경쟁에서 분리되는 것은 엄청난 장점이다.


Adapt: bars-and-fills comparison (`stat-bars-and-fills`) then a velocity-matched cut to a type payoff.
Scene 1 (0.0–3.6s): on "익스프레스 엔트리"(0.5s) the left bar grows up to a "7" mark, labeled "Express Entry 불어 카테고리" + "NCLC 7".
Scene 2 (3.6–6.0s): on "비교하면"(3.6s) the right cobalt bar grows only to the "5" mark labeled "연방 불어권 TO" + "NCLC 5"; on "문턱이 훨씬 낮습니다"(4.7s) a downward arrow + "문턱 ↓" chip pops between them.
Scene 3 (6.0–10.3s): zoom-through seam (`cut-catalog.md`) into a type stack, revealed per phrase: "중하 수준 불어 하나로"(6.1s) → "쿼터 경쟁과"(8.4s) → "분리"(9.3s, cobalt, large).
Scene 4 (10.3–12.12s): on "엄청난 장점"(11.0s) the payoff "엄청난 장점" slams in at hero scale (`kinetic-beat-slam`), cobalt underline marker sweep; hold.

## Frame 9 — 주의할 점

- scene: 조용한 카드 하나 — "※ 주정부 스트림 기본 자격은 필요", 아래 "같은 자격이면 불어가 있는 사람이 유리"
- voiceover: "물론 각 주정부 프로그램의 기본 자격, 예를 들어 직업이나 경력 조건은 갖춰야 합니다. 하지만 같은 자격이라면, 불어가 있는 사람이 훨씬 유리한 위치에 서게 됩니다."
- duration: 9.985s
- transition_in: crossfade
- status: outline
- src: compositions/frames/09-caveat.html
- type: social_proof
- persuasion: Counterexample (한계 명시) → reassurance
- beat: Unease → resolve
- blueprint: titlecard-reveal (Reproduce)
- focal: one calm tinted card "※ 기본 자격은 필요" with two small chips "직업" "경력", then the line "같은 자격이면 → 불어가 유리"
- roles: cream ground = background · caveat card = foreground subject · chips and the conclusion line = supporting

narrativeRole: 과장 없이 조건을 짚어 신뢰를 주고, 그래도 불어가 유리하다는 점으로 돌려놓는다.
keyMessage: 기본 자격은 필요하지만, 같은 조건이면 불어가 결정적 우위다.


Scene 1 (0.0–5.2s): on "기본 자격"(1.6s) the caveat card slide-up crossfades into center (y≈700): small eyebrow "주의" + text "주정부 프로그램 기본 자격은 필요"; on "직업이나"(3.2s) chip "직업", on "경력"(3.7s) chip "경력" pop in under it.
Scene 2 (5.2–9.98s): on "하지만 같은 자격이라면"(5.2s) a second line "같은 자격이라면" fades up below; on "불어가 있는 사람이"(6.8s) "불어 가능자 ▲ 유리" settles in cobalt with a small up-arrow; hold still (breather).

## Frame 10 — 몬트리올에서 시작

- scene: "몬트리올 어학연수 → 불어 NCLC 5 → 영주권" 3단 경로가 차례로 연결되고, AA Canada 워드마크와 상담 안내로 마무리
- voiceover: "그럼 불어 5레벨은 어디서 준비할까요? 불어와 영어를 함께 쓰는 도시, 몬트리올입니다. 몬트리올 어학연수로 불어 5레벨을 만들고, 그 점수로 영주권 경쟁의 판을 바꾸세요. 자세한 로드맵은, AA Canada에 문의 주세요."
- duration: 15.047s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/10-cta.html
- type: cta
- persuasion: Signposting (3-step path) + Callback (판을 바꾸다 ↔ 경쟁에서 빠져나오다)
- beat: Inspiration + resolve
- blueprint: logo-assemble-lockup (Adapt)
- focal: a 3-step vertical path "몬트리올 어학연수 → 불어 NCLC 5 → 영주권" resolving into the "AA Canada" wordmark lockup with a cobalt CTA pill
- roles: cream ground + concentric cobalt rings + dot grid atmosphere = background · 3-step path then wordmark = foreground subject · small "Montréal" label with one simple maple-leaf glyph = supporting

narrativeRole: 행동 경로(몬트리올 어학연수 → NCLC 5 → 영주권)를 제시하고 AA Canada로 연결한다.
keyMessage: 몬트리올 어학연수로 NCLC 5를 만들어 영주권 경쟁의 판을 바꿔라.


Adapt: the lockup is assembled from the path (path nodes collapse into the wordmark); final frame owns a real exit-free hold.
Scene 1 (0.0–4.8s): question "불어 5레벨, 어디서?" per-word reveal upper third; on "불어와 영어를 함께 쓰는 도시"(2.9s) two small pills "Français" + "English" slide in side by side.
Scene 2 (4.8–6.1s): on "몬트리올입니다"(4.8s) hero word "몬트리올" slams in cobalt with tiny "Montréal" label + maple-leaf glyph.
Scene 3 (6.1–11.8s): vertical path assembles step by step: node 1 "몬트리올 어학연수"(6.6s), connector draws (`svg-path-draw`), node 2 "불어 NCLC 5"(7.6s), connector, node 3 "영주권"(10.0s); on "판을 바꾸세요"(10.9s) node 3 fills solid cobalt with cream text.
Scene 4 (11.8–15.05s): on "AA Canada에"(13.1s) the three nodes collapse upward and the wordmark "AA Canada" assembles at y≈760 (`scale-swap-transition`), with sub-line "캐나다 유학·이민 전문"; on "문의 주세요"(14.1s) a cobalt CTA pill "상담 문의" settles beneath; hold to the end.
