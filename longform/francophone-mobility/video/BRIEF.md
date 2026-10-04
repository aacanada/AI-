---
workflow: general-video
flow: automation
storyboard: no
message: "캐나다 취업의 벽 LMIA를 불어(NCLC 5)로 건너뛸 수 있고, 몬트리올은 영어와 불어를 함께 준비할 수 있는 가장 현실적인 도시다."
destination: youtube
aspect: "16:9"
language: ko
audience: "캐나다 취업·이민을 고민하는 한국인 (AA Canada 잠재 고객)"
length: "~6:50 (내레이션 실측)"
---

## Intent
SCRIPT.md(../SCRIPT.md)의 19개 라인을 장면 하나씩 서브 컴포지션으로 만들고 합친 페이스리스 설명 롱폼.
사용자 요청: "하이퍼프레임즈로 모션그래픽 활용하려면 영상을 짧게 나눠서 만들고 합쳐야 한다고 했지? 진행해줘"

## Assets
- 내레이션: ElevenLabs "네 번째" 클론 보이스, 라인별 mp3 (assets/voice/01–19.mp3) — 실측 길이가 장면 길이를 결정
- 폰트: Black Han Sans(제목), IBM Plex Sans KR(본문), Space Mono(라틴 라벨) — 로컬 woff2
- GSAP: 로컬 assets/vendor/gsap.min.js (CDN 차단 환경)

## Customizations
- BGM, 자막: 이번 버전에는 없음 (요청 시 추가)

## Notes
- 장면 화면 메모는 SCRIPT.md의 **화면:** 항목을 따른다.
