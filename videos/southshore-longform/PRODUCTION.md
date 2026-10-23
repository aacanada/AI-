# 사우스쇼어 지도 롱폼 — production runbook

브리프: `plans/southshore-longform/VIDEO_BRIEF.md` · 대본: `plans/southshore-longform/SCRIPT.txt` · 학교 영상: `plans/southshore-longform/assets/school-videos/`
템플릿: 영유 롱폼(메이플 레드, `claude/jolly-tesla-u70qgi` 의 `videos/yeongyu-montreal-longform`)을 복사해 고친 것.

## 현재 상태 (2026-10-23)

- 음성: 원장님 녹음 대신 **ElevenLabs "일곱번째"** (voice vxpRrQegUpenYtez6hz1, eleven_multilingual_v2). `tools/tts.py` 가 장면별
  `plans/southshore-longform/audio/ss_s01~s10.mp3` + with-timestamps 정렬을 만들고, 자막 타이밍은 그 정렬로 맞춤(자막은 대본 원문,
  TTS에는 숫자를 한국어로 풀어 쓴 발음 텍스트 `SAY`). 총 6:13.6. Whisper로 다시 받아 적어 대본과 대조함(빠진 문장 없음).
- 대본 수정(원장님 지시): s04 "인구의 2~3% 수준" → "비중이 아주 낮은 편", "아시아계가 인구의 20% 정도" → "아시아계 주민이 꽤 많습니다".
  화면의 % 표기(아시아계 원 안의 2%·3%·20%)도 삭제, 원 크기만 남김.
- B-roll: 생랑베르 인터내셔널 입구 클립은 RSB 로고 타이틀 카드가 끝난 뒤 구간(2.3~3.9s)으로 바꿈.

### 디자인 다듬기 (frontend-design 기준, 2026-10-23)
- 장면 머리표 "— 3 · 제목"(대시+가운뎃점 템플릿 표기) → 빨간 숫자 칸 + 제목. 장(章) 순서라 번호는 유지.
- 카드: 모든 카드에 같던 큰 반경·흐린 그림자 → 반경 20px, 얇은 와인색 테두리와 짧은 아래 그림자. 빨강 카드는 진한 아래 선, 분홍 카드는 그림자 없음.
- 배경 점무늬 농도 절반, 큰 제목(Black Han Sans) 자간 -0.02em, 출처 줄 23px + 크림색 외곽으로 지도 위 대비 확보.
- 쇼츠: 하단 480px 비움(로고는 맨 위, CTA는 제목 아래로 이동), 커버의 장식용 큰 단풍잎 삭제.
- 썸네일 "한국인이 없다?" → "한국인은 거의 없다?" (원장님 표현 원칙 "한국 사람이 거의 없는"과 맞춤, 단정 표현 제거).

## 파일 지도

| 파일 | 역할 |
|---|---|
| `tools/script.py` | 내레이션 행(자막 단위), 자막 강조어(KEYS), 장면별 출처 줄(FOOT) |
| `tools/geo.py` | 지도 좌표·투영·해안선·REM 노선·도시·학교 좌표, 카메라 뷰 |
| `tools/mapkit.py` | 지도 카메라, 라벨, 핀, B-roll 창(`reel`), 아이콘 |
| `tools/scenes_a/b/c.py` | 장면 S01-S03 / S04-S06 / S07-S10. `T('구절')` = 그 구절을 말하는 시점 |
| `tools/clips.py` | 학교 영상 B-roll 구간 정의와 자르기 |
| `tools/build.py` | timing → compositions + index.html (자막, 출처 줄, BGM 덕킹, 전환) |
| `tools/shorts.py`, `tools/short_covers.py` | 숏폼 5편, 커버 |
| `tools/thumbnail.py`, `tools/upload_text.py` | 썸네일, 업로드 문구 |

## 표현 규칙 점검 (브리프 5장)

- 커미션·"무상/무료 교육" 없음. 학비 화면에 "2027-28 · 캐나다 달러 · 변경될 수 있음" 각주.
- 통학 시간 숫자는 REM 공식 "브로사드→중앙역 18분"만. 학교→역 시간 없음.
- 88.5%·몬테레지 1위 = "브로슈어 기준" 표기. 인구 = "2021 캐나다 인구조사" 표기.
- 썸네일·B-roll에 학생 얼굴 클로즈업 없음. RSB 로고 미사용(영상 속 엔드카드 구간도 제외).
