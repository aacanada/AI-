---
workflow: general-video
flow: automation
storyboard: no
message: "불어교육(FI/EF) 학생이 영어 성적도 더 높다 — 몬트리올 웰컴클래스를 거쳐 온타리오 FI/EF로 가는 루트"
destination: youtube
aspect: 1920x1080
language: ko
audience: 캐나다 자녀 동반 유학·이민을 알아보는 한국 학부모
length: 3m18s
---

## Intent

AA Canada 네이버 카페 글(https://cafe.naver.com/aamontreal/39102)을 데이터 설명 영상으로 옮긴다.
설계서 전체는 `../VIDEO_BRIEF.md` — 씬 구성, 대본, 차트 JSON, 모션 가이드는 그 문서를 그대로 따른다.
1차 범위: S01~S03만 만들어 톤(색, 자막, 음성) 확인 후 S04~S12 진행.

## Assets

- assets/capture_1.jpg ~ capture_5.jpg — 원문 캡쳐. "증거 카드"로만 사용(브리프 1장).
- assets/voice/*.mp3, assets/narration.wav — ElevenLabs TTS (환경의 ELEVENLABS_VOICE_ID, eleven_multilingual_v2).
- assets/fonts/ — Pretendard(한글), Inter(숫자). jsDelivr가 네트워크 정책상 막혀 있어 npm 패키지에서 로컬로 복사.
- assets/vendor/gsap.min.js — 같은 이유로 로컬 번들.

## Customizations

- 한국어 TTS 내레이션 + 문장 단위 번인 자막 (자막 타이밍은 timing.json에서 생성).
- 차트 숫자는 VIDEO_BRIEF.md 2장의 JSON만 사용, 결정적 카운트업.
- FI #0055A4 / EF #E4572E / TDSB #9AA0A6 색 고정.

## Notes

- 자료 연도(TDSB 2011-12, 통계청 2000) 화면에 표기.
- OINP 수치(146명, 35/57점)는 S11 제작 전에 최신 정책 확인 필요.
