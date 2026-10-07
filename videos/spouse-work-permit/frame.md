# frame.md — AA Canada · 배우자 워크퍼밋 설명 영상

Concept: **"이민 서류철(immigration file)"** — 따뜻한 종이색 바탕 위에 잉크 네이비 타이포,
캐나다 레드를 단 하나의 강조색으로. 가능/불가 판정은 서류 도장(stamp)처럼 찍힌다.

## Palette
- --paper: #F4EFE6 (background, warm paper)
- --paper-2: #EAE2D4 (panels)
- --ink: #18233A (foreground, navy ink)
- --ink-soft: #4A5468 (secondary text)
- --red: #C8281E (accent — Canada red; 핵심 강조, '불가' 도장)
- --green: #1F7A4D (판정 '가능' 전용 기능색)
- --amber: #B7791F (판정 '조건부/주의' 전용 기능색)

## Type
- Pretendard (local @font-face, assets/fonts) — 한글 전 영역. 헤드라인 800–900, 본문 400–500.
- JetBrains Mono (bundled) — 데이터/라벨 레지스터: 날짜, 'TEER 0·1', '16개월', 섹션 번호.
- 헤드라인 80–140px, 본문 36–48px, 라벨 22–26px. 자막 44px.

## Layout
- 상단 좌측: 섹션 라벨(모노, 'PART 03 · 취업비자'), 상단 우측: AA CANADA 워드마크.
- 하단 200px는 자막 안전영역 — 장면 콘텐츠는 y ≤ 860px.
- 배경: 미세한 종이 그레인 + 대형 고스트 텍스트(8–12%) + 붉은 메이플/헤어라인 룰.

## Motion
- 진입: power3.out / back.out(1.6) / expo.out 혼용, 도장은 scale 1.6→1 + 회전 -8° 슬램.
- 전환: 기본 push-slide(좌), 파트 전환은 staggered blocks(네이비/레드), 클로징은 blur crossfade.
