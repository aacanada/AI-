# 몬트리올 자녀무상교육: 영어·불어·스페인어 롱폼 — 대표님 미리보기 v2 (2026-10-31)

- 파일: `renders/video.mp4` (1920x1080, 30fps, H.264 + AAC 256k), 길이 **4:06.93**, 23MB(분할 불필요), SHA-256은 `video.mp4.sha256`
- 썸네일: `renders/thumbnail.jpg` (1280x720)
- 음성: ElevenLabs "여덟번째"(voice_id cbVXtFGe9VfUKWtbYIty, API에서 이름으로 조회) + **eleven_multilingual_v2**, Stability 0.5 / Similarity 0.75. 장면별 `audio/mlang_s01.mp3`~`mlang_s09.mp3`
- 상태: 미리보기 전용. publish 브랜치·READY·유튜브/쓰레드 업로드·쇼츠 없음.
- 길이 참고: 브리프 예상은 약 7분이었으나, 대본 TTS 음성 합계가 약 3분 50초라 영상은 약 4분입니다(브리프의 "TTS 길이에 맞춤"을 따름).

## v2 수정 사항 (대표님 요청 2026-10-31)
- "AA Canada" 발음: TTS 입력만 "에이에이 캐나다"로 바꿔 s01·s09를 다시 생성했습니다. 인식 결과는 "에이에이 캐나다", "AA 캐나다"로 정상입니다. 자막은 "AA Canada" 그대로입니다.
- "클라스 다쾨이"를 **"클라스 아께이"**(불어 발음)로 바꿨습니다. 대본(NARRATION.txt), 자막, s04 음성에 모두 반영했고, 인식 결과는 "Classe accueil"입니다.
- "열 달에서 스무 달"을 **"10개월에서 20개월"**로 바꿨습니다. 대본과 자막은 숫자로 적고, TTS 입력은 "십 개월에서 이십 개월"로 넣었습니다. 인식 결과는 "10개월에서 20개월"로 정상입니다.
- canlog: TTS 입력만 **"씨에이앤엘오지"**로 바꿔 한 글자씩 읽게 했습니다. 3회 생성했고, 가장 또박또박한 take를 썼습니다(영어 인식 "CANLOG", 한국어 인식 "CANology"). 자막은 "canlog" 그대로입니다.
- 썸네일: "초등학생이 / 3~4개 국어, / 정말 가능할까?"를 크게 넣은 후크형으로 바꿨습니다. "몬트리올 자녀무상교육"은 아래에 작게 넣었습니다.
- s04 비교 화면의 "vs" 위치를 바로잡았습니다.

## 장면 시작 시각 (유튜브 챕터용)
0:00 오프닝: 영어·불어·스페인어까지?
0:17 숫자: 몬트리올 5명 중 1명은 3개 언어
0:46 학비: 퀘벡 교육법 3.1조
1:16 웰컴 클래스(classe d'accueil)
2:00 영어: 초1부터 정규 수업
2:24 스페인어: PEI 운영 공립학교 4곳
2:50 4개 국어는 '목표'
3:12 주의할 점: 선발제·중간 입학
3:32 정리 · 상담 안내

## 음량 (EBU R128, `renders/loudness.json`)
| 항목 | 통합 음량 | 트루피크 |
|---|---|---|
| 최종 믹스 (video.mp4) | **-16.1 LUFS** | -2.0 dBTP |
| 내레이션 단독 (정규화 직후) | **-16.0 LUFS** | -2.1 dBTP |
| 내레이션 단독 (최종 믹스에 들어간 그대로) | **-16.3 LUFS** | -2.4 dBTP |
| BGM 단독 | -34.3 LUFS (내레이션보다 약 18 LU 낮음) | -20.4 dBTP |
| 효과음 단독 | -20.9 LUFS (짧은 효과음 위주) | -9.3 dBTP |
| 참고: TTS 원본 내레이션 | -35.5 LUFS | -6.9 dBTP |

- 순서: 내레이션 트랙을 먼저 -16 LUFS로 정규화(가벼운 컴프레서 + 트루피크 리미터. TTS 원본은 피크가 음량보다 약 28dB 높아서 단순 증폭만 하면 클리핑이 남) → BGM -34 LUFS → 효과음 → 전체를 -16 LUFS로 맞추고 리미터 적용.
- 밴쿠버 롱폼 때(내레이션 -24 LUFS)와 달리 내레이션이 믹스의 주 음량입니다.
- BGM: 밴쿠버 롱폼 BGM(`claude/beautiful-ptolemy-4l997y` 브랜치 `plans/vancouver-esl-free-edu/video/bgm_vanesl.mp3`)을 그대로 재사용.

## 발음 점검 (ElevenLabs Scribe 음성인식으로 대조)
| 항목 | 결과 |
|---|---|
| 69.8퍼센트 (s02), 56.4퍼센트 (s05), 2021년 (s02), 28명 (s04) | 첫 생성부터 정상 |
| 17명 (s04) | v2에서 3회 생성, 그중 1회만 "최대 17명"으로 정상(나머지는 16명·18명) → 정상 take 사용 |
| 5, 6학년 (s05) | 1번째 생성 "6학년"만 인식 → **2번째 take 정상** 사용 |
| AA Canada (s01, s09) | 정상 ("AA Canada" / "AA 캐나다"로 인식) |
| 클라스 아께이 (s04, v2) | 정상 ("Classe accueil"로 인식) |
| 피이아이 (s06, s08) | 정상 ("PEI"로 인식) |
| 잔 망스 · 콜레주 생루이 · 데 수르스 (s06) | 정상 |
| 장 그루 (s06) | 1번째 생성 "잔그루" → **2번째 take**에서 "장그루" 사용. 이 take에서 "라신의"가 "라 시네"로 인식됨(같은 소리의 띄어쓰기 차이로 보이나 귀로 확인 부탁) |
| **canlog (s09)** | v1: 원문 그대로 8회 생성했는데 모두 "찬롱/찰롱"으로 인식됨 → TTS 입력 "캔로그"로 바꿨더니 "캣로그"로 인식됨. **v2: 대표님 요청으로 TTS 입력 "씨에이앤엘오지"** → 인식 결과 "CANLOG"(영어)·"CANology"(한국어). 한 글자씩 읽는지 대표님 귀로 확인 부탁드립니다. 자막은 "canlog" 원문 그대로 |

- 대본 문구는 대표님이 요청하신 2곳(클라스 아께이, 10개월에서 20개월)만 바꿨습니다. canlog·AA Canada는 TTS 입력만 바꾸고 자막은 원문 그대로입니다. 모든 생성본은 `audio/takes/`(저장소 제외), 인식 결과는 `video/asr/`.

## 화면 구성 메모
- 하단 자막은 대본 그대로이며, 학교 이름과 용어는 표기를 함께 적었습니다(잔 망스(Jeanne-Mance) 등).
- s03 교육법 3.1조는 텍스트 카드로 제작했습니다. s04는 CSSDM 표 캡처에서 17과 28을 강조하고 숫자를 크게 보여 줍니다. 기간은 "정해진 기간 없음 · 보통 10~20개월"로 표시했습니다.
- s03~s08 하단에 상시 각주를 넣고, 각 장면 출처 자막에 확인일 2026.10.31을 적었습니다.

## 기술 메모
- HyperFrames CLI는 0.8.209로 고정했습니다. 0.8.223으로 올려 검사해 보니 이 환경(GPU 없음)에서는 셰이더 전환 구간의 장면 내용이 비어 보였습니다. 그래서 밴쿠버 때 정상 렌더된 0.8.209와 셰이더 라이브러리로 되돌렸습니다. 이 상태에서 `hyperframes check`는 통과합니다(레이아웃 0건, 대비 34/34).

## 재생성 방법
- 음성: `python3 video/tools/tts.py [s0N]` / 인식: `python3 video/tools/asr.py [s0N]` / take 추가: `video/tools/retake.sh s0N [횟수]`
- 시간표: `python3 video/tools/timing.py` → `video/timing.json`
- 화면: `python3 video/tools/build.py` → `hf/index.html`, 렌더: `cd hf && npx hyperframes@0.8.209 render --fps 30 --page-side-compositing -o ../renders/video_silent.mp4`
- 오디오: `python3 video/tools/mix.py` → `renders/mix.m4a`, `renders/loudness.json`
- 합치기: `ffmpeg -i renders/video_silent.mp4 -i renders/mix.m4a -map 0:v -map 1:a -c copy -movflags +faststart renders/video.mp4`
- 썸네일: `video/thumb/thumb.html`을 1280x720으로 캡처
