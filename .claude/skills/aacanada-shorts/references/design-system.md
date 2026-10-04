# 디자인 시스템 — 교육용 · 프리미엄

## 무드
대학 강의 노트처럼 정리된 구조 + 프라이빗 뱅킹 브로슈어 같은 색감. 쨍한 원색과 이모지, 과한 흔들림(쉐이크), 네온 글로우는 쓰지 않는다. 모션은 부드럽고 짧게(0.4–0.6s, power3.out / 약한 back.out).

## 토큰 (`:root`)
| 토큰 | 값 | 용도 |
| --- | --- | --- |
| `--bg` | `#070a12` | 바탕 |
| `--navy` / `--navy-2` | `#0e1528` / `#18223f` | 노드, 배지 |
| `--gold` / `--gold-2` | `#c9a96e` / `#e6cf9f` | 키커, 테두리, 강조 단어 (`.gold`) |
| `--gold-deep` | `#9c7b45` | 아이보리 위 골드 라인 |
| `--gold-grad` | 135° 샴페인 그라디언트 | 판정 슬랩, 최종 칩, CTA 버튼, 진행바 |
| `--ivory` | `#f4efe6` | 본문 글자, 강조 카드 바탕 |
| `--ink` | `#0d1322` | 아이보리/골드 위 글자 |
| `--slate` | `#9aa3b8` | 보조 설명 |
| `--wine` | `#c95a55` | ✕ 스탬프, 취소선 (부정 표시에만) |
| `--hair` | 골드 34% | 카드 헤어라인 |

## 타이포
- 한글: Pretendard 800(제목·카드), 900(대형 숫자 아닌 강조), 700(보조).
- 숫자·금액·영문 워드마크: `.serif` (Playfair Display). 금액은 항상 serif.
- `.title` 72px, `.title-xl` 104px, 카드 핵심어 52–58px, 보조 28–36px. 자막 54px.
- `word-break: keep-all` 이 기본. `<br>` 대신 `<span class="line">`.

## 레이아웃 (1080×1920)
- 0–250px: 크롬(진행바, 브랜드, 토픽, 레슨 카운터) — 자동.
- 270–1280px: `.stage` (flex column, gap 34px). 내용은 여기만.
- 1350–1520px: 자막.
- 1540px 아래: 쇼츠 UI가 덮는 영역 → 비운다.
- 좌우 여백 70px. 카드 폭 920–960px.

## 컴포넌트 카탈로그 (템플릿에 실물 있음)
| 컴포넌트 | 클래스 | 쓰임 |
| --- | --- | --- |
| 키커 | `.kicker` | 장면 레이블 "POINT · 학비", "오늘의 질문", "LONG-TERM PLAN" |
| 유리 카드 | `.glass` | 모든 카드의 기본 바탕 |
| 오해 카드 + 스탬프 | `.myth` `.myth-tag` `.myth-text` `.stamp` | 훅에서 오해 제시 → ✕ |
| 판정 슬랩 | `.verdict` | "아닙니다!" "정답은 O" |
| 방정식 | `.eq` `.card(.ivory/.glass)` `.op` | A + B, A → B |
| 배지 | `.badge` `.badge-top` `.badge-main` | 독점/유일/핵심 메시지 |
| 체크 행 | `.rows` `.row` `.check` `.row-main` `.row-sub` | 장점 2–4개 |
| 정보 타일 2×2 | `.tiles` `.tile` `.tile-k/v/s` | 조건·일정 요약 |
| 영수증 | `.receipt` `.r-line` `.r-div` `.r-total-*` + `countUp()` | 학비·비용 합계 |
| 버블 | `.bubbles` `.bubble(.split)` | 2가지 선택지 |
| 로드맵 | `.road` `.road-fill` `.step(.goal)` `.node` `.step-box` | 단계별 경로 |
| 체인 | `.pill-label` `.chain` `.chip(.final)` `.arrow` `.skip` `.note` | 지름길·프로세스 |
| CTA | `.ornament` `.logo` `.logo-sub` `.cta-btn` | 마지막 장면 |
| 스크린샷 카드 | `.shot` > `.shot-inner[data-layout-allow-overflow]` > `img[data-img="img-01"]` + `.hl-box` | 첨부 이미지(가로형) |
| 휴대폰 프레임 | `.shot.phone` (내부 동일) | 세로 캡처, 카톡·앱 화면 |
| 고정 창 | `.shot.window` (높이 860) | 긴 페이지·서류의 일부만 |
| 이미지 라벨/설명 | `.shot-tag` (예: "실제 상담 캡처"), `.shot-cap` | 출처·기준 표기 |

## 타임라인 헬퍼 (템플릿 스크립트에 정의됨)
- `c(id, 앵커)` → 그 말이 시작되는 절대 시각. 없는 앵커면 에러로 알려 준다.
- `S[id]`, `sEnd(id)` → 장면 시작/끝.
- `from(sel, at, fromVars?, toVars?)` 기본: 아래에서 페이드업.
- `slideIn(sel, at, dx)`, `pulse(sel, at, scale)`, `countUp(sel, 숫자, at)`, `enterKicker(stageSel, id)`, `exit(stageSel, id)`.
- 이미지: `shotIn(sel, at)`, `spot(hlSel, at)`, `focusShot(sel, {x,y,w,h}, at)` (영역이 폭 60% 이하일 때 확대 효과가 큼), `unfocusShot(sel, at)`, `scrollShot(sel, at, dur, from%, to%)`. 이미지 크기는 `images.json`에서 주입되므로 로딩과 무관하게 정확하다.
- 장면마다: `enterKicker` → 제목 `from(... S[id]+0.1)` → 요소들을 각 앵커에 → `exit`.

## HyperFrames 주의 (실수하면 렌더가 깨짐)
- `.clip` 요소 자체에 opacity/visibility 트윈 금지 → 안쪽 `.stage`를 움직인다.
- CSS `transform` 초기값 + GSAP 같은 속성 트윈 금지 → `fromTo` 사용.
- `Math.random`, `Date.now` 금지. `repeat`는 유한 횟수만.
- 모든 `<audio>`에 `id`. 외부 CDN 금지(로컬 `public/`).
- 장면 `id` 속성은 문서 전체에서 유일하게(`s-cost`, `cost-stage`, `cost-title`처럼 접두어).
