---
name: Kootenay Postcard (v2 — 버논 영상 디자인 시스템 계승)
canvas: 1920x1080
colors:
  paper: "#FAF6EF"      # 모든 장면 배경 (밝은 종이 톤)
  ink: "#16324F"        # 제목·본문 (딥네이비)
  ink-soft: "#4A5F78"   # 보조 텍스트
  green: "#2E7D5B"      # 주 강조 — 셀커크/쿠트니 숲 그린 (데이터, 스크립트 문구)
  green-deep: "#1F5E44" # 그린 위·옆 텍스트 대비용
  sunset: "#E8572B"     # 포인트 — 스티커, 취소선 (한 장면 한 곳)
  sand: "#F3C969"       # 형광펜 하이라이트
typography:
  display: Pretendard 900, 96–300px, tracking -0.03em
  heading: Pretendard 800, 56–80px
  body: Pretendard 500, 32–44px
  label: Pretendard 700, 22–26px, tracking 0.08em
  script: Yellowtail — 영문 포인트 한 줄 (Resort Town, Queen City of the Kootenays)
spacing: { safe-x: 120px, caption-keepout-bottom: 180px }
---

## 원칙 (사용자 피드백 반영)
- 사진을 배경으로 깔지 않는다. 화면은 밝은 종이 배경 + 모션 그래픽(아이콘, 지도, 일러스트, 막대, 타임라인) 위주.
- 사진은 폴라로이드/타일로 잠깐씩만 (화면 폭 25% 안팎), 내부는 느린 켄번스.
- 자막: 하단 네이비 pill (버논 영상과 동일).
- 챕터 전환: 오른쪽에서 밀고 들어오는 push slide.
- 공통 CSS/헬퍼: tools/common.css, tools/helpers.js → tools/build.py 로 compositions/*.html 생성.
