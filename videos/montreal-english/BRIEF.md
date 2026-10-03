---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "몬트리올에서도 아이 영어 충분히 늘어요 — 친구들과 100% 영어, 수업 80% 영어, 아낀 학비로 매일 원어민 튜터"
destination: shorts
aspect: 1080x1920
language: ko
audience: "캐나다 자녀무상교육을 알아보며 '불어권이라 영어가 안 늘 것'이라는 이유로 몬트리올을 제외하는 한국 학부모"
length: 60s
angle: listicle
vo_mode: verbatim
voice: elevenlabs:9qtE9eIaqHMUAfRp4QTW
---

## Intent

AA Canada 원장님 본인 목소리(ElevenLabs 저장 음성)로 읽는 세로 숏폼(유튜브 쇼츠 / 인스타 릴스).
요청 원문: "videos/montreal-english 대본으로 내 일레븐랩스 목소리 입혀서 숏폼 만들어줘".
톤: 차분하고 신뢰감 있는 상담 선생님. 숫자는 또박또박 힘 있게.

## Assets

- SCRIPT.md — 확정 대본 (verbatim 사용, 프레임 8개)
- assets/timetable.webp — 실제 영어 중심 학교 시간표 (영어 노란 형광, 불어 빨간 동그라미). Frame 4 근거 이미지.
- assets/fonts/ — Pretendard (OFL) 한글 폰트, 렌더 환경에 한글 폰트가 없어서 로컬 파일로 포함.

## Customizations

- 내레이션: ElevenLabs `eleven_multilingual_v2`, 저장 음성 `$ELEVENLABS_VOICE_ID`, `/with-timestamps`로 정확한 한글 단어 타이밍 (scripts/elevenlabs-tts.mjs).
- 숫자 카운트업: 100%, 80%, $5,750 / $20,000 막대 비교, $40 × 5 × 50 = $10,000 계산식.
- 한글 카라오케 자막(하단).

## Notes

- 발음 교정은 scripts/elevenlabs-tts.mjs의 SAY 표에서 음성에만 적용, 자막은 대본 표기 유지:
  불어권→불어꿘, N%→N퍼센트, AA캐나다→에이에이 캐나다, 5,750달러→오천칠백오십 달러.
  이 음성은 일부 쉼표에서 "어…"를 넣는 경향이 있어 해당 쉼표는 음성용 텍스트에서만 제거.
- 유튜브 쇼츠 자막은 항상 상단 배치 (자막 밴드 y 170–360px, 본문은 그 아래 안전영역).
- BGM 없음: HeyGen 미로그인 상태라 음원 라이브러리 검색 불가. 업로드 시 플랫폼 음원 추가 권장.
- CTA 연락처: 카카오톡 canlog · 02-567-4345.
