---
name: Okanagan Postcard
canvas: 1920x1080
colors:
  paper: "#FAF6EF"        # 배경. 따뜻한 오프화이트(브로슈어 종이 톤)
  paper-deep: "#F1EADF"   # 패널·카드 바닥
  ink: "#16324F"          # 본문·제목. 딥네이비(순검정 금지)
  ink-soft: "#4A5F78"     # 보조 텍스트
  lake: "#1F8A99"         # 주 강조. 오카나간 호수 틸 (포컬, 데이터 '캐나다 95%')
  lake-deep: "#146A77"    # 틸 위 텍스트 대비용
  sunset: "#E8572B"       # 포인트. SD22 브로슈어 오렌지 (스티커, 한 장면에 한 곳만)
  vine: "#7FB236"         # 보조. 포도밭 그린 (체크, 성장)
  sand: "#F3C969"         # 형광펜 하이라이트(텍스트 밑줄 전용)
typography:
  display:
    family: Pretendard
    weight: 900
    size: 96-132px
    tracking: -0.03em
  heading:
    family: Pretendard
    weight: 800
    size: 56-80px
  body:
    family: Pretendard
    weight: 500
    size: 32-42px
  label:
    family: Pretendard
    weight: 700
    size: 22-26px
    tracking: 0.08em
  script:
    family: Yellowtail
    weight: 400
    size: 72-140px
    use: 영문 포인트 문구 1줄 (Take Flight!, Vernon, Selling Point)
spacing:
  safe-x: 120px
  safe-top: 96px
  caption-keepout-bottom: 180px
components:
  polaroid: "흰 테두리 18px(하단 64px), 그림자 0 18px 40px rgba(22,50,79,.22), 회전 -8°~+8°, 손글씨 캡션"
  sticker: "SELLING POINT 0N — sunset 배경 pill, 흰 글자 label, 회전 -4°, 테이프 질감 없음"
  chip: "paper 배경 + ink 2px 테두리 pill, label 타입"
  panel: "ink 92% 반투명 패널, 반경 28px, paper 텍스트"
  pin: "sunset 물방울 핀 + lake 펄스 링"
---

## Overview

오카나간 호수의 여름 엽서 같은 화면. 밝은 종이 배경 위에 실제 버논 사진이 폴라로이드로 놓이고,
숫자와 지도는 깔끔한 인포그래픽으로 얹힌다. 학원 광고가 아니라 "여행 다큐 + 상담 노트" 톤.

## The Frame

- 배경은 모든 장면에서 `paper`. 풀스크린 사진 장면만 예외(사진 위 하단 그라데이션은 ink 0→55%).
- 배경 질감: 아주 옅은 종이 그레인 + 화면 가장자리의 큰 유령 텍스트(장면 키워드, ink 6~8%) 또는 호수 물결 라인.
- 사진은 ASSETS.md 등급을 지킨다: A등급만 풀스크린, B는 화면 폭 40% 이하, C는 25% 이하.

## Composition Rules

- 좌측 정렬 기본. 제목은 좌상단 safe 영역에 고정, 시각물은 우측/하단.
- 하단 180px은 자막 영역. 핵심 정보 금지.
- 한 장면에 sunset은 한 곳(스티커 또는 포컬 1개). 데이터 강조는 lake.
- 반복 장치(spine): ① 버논 핀 — 지도 장면마다 같은 핀이 기준점 ② 폴라로이드 스택 — 사진은 늘 기울어진 카드로 떨어져 쌓임 ③ SELLING POINT 스티커 6장 — 마지막 장면에서 한데 모임.

## Motion

- 진입 0.4~0.7s, ease는 power3.out / back.out(1.6) / expo.out 섞어 쓰기.
- 폴라로이드는 위에서 떨어지며 회전 정착(back.out), 사진 내부는 항상 느린 켄번스(1.00→1.06).
- 장면 전환 방향은 왼쪽으로 통일(내용이 오른쪽에서 들어와 왼쪽으로 나감).

## Do's and Don'ts

- Do: 실제 사진, 실제 숫자, 짧은 한국어 문장.
- Don't: 그라데이션 텍스트, 네온, 빨간 경고 자막, 가짜 UI, 인종 표현, 기술 과목(목공·재봉·자동차 정비), 졸업률 수치, 커미션 정보.
- Don't: 저해상도 사진을 풀스크린으로 키우기.
