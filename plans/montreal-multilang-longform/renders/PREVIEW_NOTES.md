# 몬트리올 자녀무상교육: 영어·불어·스페인어 롱폼 — 대표님 미리보기 (2026-10-31)

- 파일: `renders/video.mp4` (1920x1080, 30fps, H.264 + AAC 256k), 길이 **4:03.67**, 23MB(분할 불필요), SHA-256은 `video.mp4.sha256`
- 썸네일: `renders/thumbnail.jpg` (1280x720)
- 음성: ElevenLabs "여덟번째"(voice_id cbVXtFGe9VfUKWtbYIty, API에서 이름으로 조회) + **eleven_multilingual_v2**, Stability 0.5 / Similarity 0.75. 장면별 `audio/mlang_s01.mp3`~`mlang_s09.mp3`
- 상태: 미리보기 전용. publish 브랜치·READY·유튜브/쓰레드 업로드·쇼츠 없음.
- 길이 참고: 브리프 예상은 약 7분이었으나, 대본 TTS 음성 합계가 약 3분 47초라 영상은 약 4분입니다(브리프의 "TTS 길이에 맞춤"을 따름).

## 장면 시작 시각 (유튜브 챕터용)
0:00 오프닝: 영어·불어·스페인어까지?
0:17 숫자: 몬트리올 5명 중 1명은 3개 언어
0:47 학비: 퀘벡 교육법 3.1조
1:17 웰컴 클래스(classe d'accueil)
1:59 영어: 초1부터 정규 수업
2:23 스페인어: PEI 운영 공립학교 4곳
2:49 4개 국어는 '목표'
3:11 주의할 점: 선발제·중간 입학
3:31 정리 · 상담 안내

## 음량 (EBU R128, `renders/loudness.json`)
| 항목 | 통합 음량 | 트루피크 |
|---|---|---|
| 최종 믹스 (video.mp4) | **-16.0 LUFS** | -2.2 dBTP |
| 내레이션 단독 (정규화 직후) | **-16.0 LUFS** | -2.3 dBTP |
| 내레이션 단독 (최종 믹스에 들어간 그대로) | **-16.3 LUFS** | -2.6 dBTP |
| BGM 단독 | -34.3 LUFS (내레이션보다 약 18 LU 낮음) | -20.4 dBTP |
| 효과음 단독 | -20.9 LUFS (짧은 효과음 위주) | -9.3 dBTP |
| 참고: TTS 원본 내레이션 | -34.8 LUFS | -6.9 dBTP |

- 순서: 내레이션 트랙을 먼저 -16 LUFS로 정규화(가벼운 컴프레서 + 트루피크 리미터. TTS 원본은 피크가 음량보다 약 28dB 높아서 단순 증폭만 하면 클리핑이 남) → BGM -34 LUFS → 효과음 → 전체를 -16 LUFS로 맞추고 리미터 적용.
- 밴쿠버 롱폼 때(내레이션 -24 LUFS)와 달리 내레이션이 믹스의 주 음량입니다.
- BGM: 밴쿠버 롱폼 BGM(`claude/beautiful-ptolemy-4l997y` 브랜치 `plans/vancouver-esl-free-edu/video/bgm_vanesl.mp3`)을 그대로 재사용.

## 발음 점검 (ElevenLabs Scribe 음성인식으로 대조)
| 항목 | 결과 |
|---|---|
| 69.8퍼센트 (s02), 56.4퍼센트 (s05), 2021년 (s02), 28명 (s04) | 첫 생성부터 정상 |
| 17명 (s04) | 1번째 생성 "18명", 2·3번째 숫자 불분명 → **4번째 take 정상**("최대 17명") 사용 |
| 5, 6학년 (s05) | 1번째 생성 "6학년"만 인식 → **2번째 take 정상** 사용 |
| AA Canada (s01, s09) | 정상 ("AA Canada" / "AA 캐나다"로 인식) |
| 클라스 다쾨이 (s04) | 정상 ("Classe d'accueil"로 인식) |
| 피이아이 (s06, s08) | 정상 ("PEI"로 인식) |
| 잔 망스 · 콜레주 생루이 · 데 수르스 (s06) | 정상 |
| 장 그루 (s06) | 1번째 생성 "잔그루" → **2번째 take**에서 "장그루" 사용. 이 take에서 "라신의"가 "라 시네"로 인식됨(같은 소리의 띄어쓰기 차이로 보이나 귀로 확인 부탁) |
| **canlog (s09)** | 대본 원문 그대로 8회 생성 → 모두 "찬롱/찰롱/찬농/찰록". 대표님 승인(2026-10-31)으로 **TTS 입력에만** "캔로그"로 적어 재생성(5회). 사용한 take는 문장 속·단독 구간 모두 "캣로그"로 인식("로그"는 분명, 첫 글자 ㄴ/ㅅ은 인식기 한계일 수 있음). **대표님 귀로 최종 확인 필요.** 화면 자막은 "canlog" 원문 그대로 |

- 대본 문구는 바꾸지 않았습니다(위 canlog의 TTS 입력 표기만 예외, 자막은 원문). 모든 생성본은 `audio/takes/`(저장소 제외), 인식 결과는 `video/asr/`.

## 화면 구성 메모
- 하단 자막은 대본 그대로이며, 학교 이름과 용어는 표기를 함께 적었습니다(잔 망스(Jeanne-Mance) 등).
- s03 교육법 3.1조는 텍스트 카드로 제작했습니다. s04는 CSSDM 표 캡처에서 17과 28을 강조하고 숫자를 크게 보여 줍니다. 기간은 "정해진 기간 없음 · 보통 10~20개월"로 표시했습니다.
- s03~s08 하단에 상시 각주를 넣고, 각 장면 출처 자막에 확인일 2026.10.31을 적었습니다.
- 수정 후보(미반영): s04 비교 화면에서 "vs" 글자가 17명 카드 아래 끝에 살짝 닿습니다.

## 기술 메모
- HyperFrames CLI는 0.8.209로 고정했습니다. 0.8.223으로 올려 검사해 보니 이 환경(GPU 없음)에서는 셰이더 전환 구간의 장면 내용이 비어 보였습니다. 그래서 밴쿠버 때 정상 렌더된 0.8.209와 셰이더 라이브러리로 되돌렸습니다. 이 상태에서 `hyperframes check`는 통과합니다(레이아웃 0건, 대비 34/34).

## 재생성 방법
- 음성: `python3 video/tools/tts.py [s0N]` / 인식: `python3 video/tools/asr.py [s0N]` / take 추가: `video/tools/retake.sh s0N [횟수]`
- 시간표: `python3 video/tools/timing.py` → `video/timing.json`
- 화면: `python3 video/tools/build.py` → `hf/index.html`, 렌더: `cd hf && npx hyperframes@0.8.209 render --fps 30 --page-side-compositing -o ../renders/video_silent.mp4`
- 오디오: `python3 video/tools/mix.py` → `renders/mix.m4a`, `renders/loudness.json`
- 합치기: `ffmpeg -i renders/video_silent.mp4 -i renders/mix.m4a -map 0:v -map 1:a -c copy -movflags +faststart renders/video.mp4`
- 썸네일: `video/thumb/thumb.html`을 1280x720으로 캡처
