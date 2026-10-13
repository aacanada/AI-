# frame.md — Selkirk × RCIP 디자인 스펙

**Concept:** "쿠트니에서 온 엽서" — 휴양지에서 보낸 엽서처럼, 사진은 흰 테두리 카드로 놓이고 손글씨 대신 세리프 제목과 우표·소인 같은 라벨이 붙는다. 데이터 챕터는 같은 숲색 위에 큰 숫자.

## Palette (one background family, one accent)
- `--forest` #12291F — 기본 배경 (숲, 깊은 초록)
- `--forest-2` #1A3A2D — 패널/카드 그늘
- `--cream` #F4EFE3 — 본문 글자, 엽서 테두리
- `--cream-dim` #CFC8B6 — 보조 글자
- `--gold` #E2B04A — 유일한 강조색 (일출, 숫자, 하이라이트)
- `--lake` #7FB3AE — 지도/라인 보조 (저채도 호수색, 강조 아님)

## Type
- Headline: Noto Serif KR 900 / 700 — 제목, 도시 이름, 큰 숫자
- Body/labels: IBM Plex Sans KR 400/600/700 — 설명, 라벨, 자막
- Sizes: 헤드라인 88–150px, 본문 36–44px, 라벨 22–26px(자간 0.12em), 자막 40px
- 숫자: Noto Serif KR 900, tabular

## Layout
- 1920×1080, 좌우 여백 120px, 하단 160px는 자막 영역(장면 콘텐츠 금지)
- 사진 카드: cream 14px 테두리, 2° 내외 기울기, 그림자 0 30px 60px rgba(0,0,0,.45)
- 라벨(우표형): gold 2px 테두리 사각, 대문자 영문 + 한글
- 배경 장치: 아주 큰 흐린 산 실루엣(SVG), 고스트 텍스트(지명, 12% cream), gold 방사형 글로우

## Motion
- 에너지: Calm–Medium. 사진은 느린 켄번스(scale 1.0→1.08, 6–10s), 카드 입장은 back.out 소폭 + 회전 정착
- 제목: waterfall-entry (아래에서 whip, 바이너리 opacity)
- 숫자: counting-dynamic-scale
- 챕터 전환: blur crossfade 0.7s (주), push slide(데이터 챕터 진입, 보조)

## Don'ts
- 시안/네온, 그라디언트 텍스트, 순백/순흑, 저해상도 사진 풀스크린 확대
