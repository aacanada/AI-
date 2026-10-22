# 사우스쇼어 지도 롱폼 — production runbook

브리프: `plans/southshore-longform/VIDEO_BRIEF.md` · 대본: `plans/southshore-longform/SCRIPT.txt` · 학교 영상: `plans/southshore-longform/assets/school-videos/`
템플릿: 영유 롱폼(메이플 레드, `claude/jolly-tesla-u70qgi` 의 `videos/yeongyu-montreal-longform`)을 복사해 고친 것.

## 현재 상태 (2026-10-22)

- 녹음 전: **무음 + 가짜 타이밍**(글자당 0.21초)으로 10장면 전체 빌드, `npm run check` 통과(오류 0).
- 지도: OSM 서버·위성 데이터는 샌드박스에서 막혀 있어 브리프의 대안대로 **실제 좌표 기반 스키매틱 지도**(`tools/geo.py`)를 직접 그림. 캐나다 전도는 svg-maps/canada (CC BY 4.0).
- B-roll: `tools/clips.py` 가 학교 영상 4개에서 28개 구간을 잘라 `assets/clips/` (16:9, 무음). 구간은 `plans/riverside-video/01_TIMESTAMP_SHEET.md` 기준, 학생 얼굴 클로즈업 제외.
- 숏폼 5편: `../southshore-shorts/short-a ~ e` (index.html, cover.jpg, upload-text.txt). 음성은 녹음이 오면 자동으로 붙음.
- 썸네일: `thumbnail/thumbnail.jpg` (기본안 "다운타운 18분인데 한국인이 없다?"), `thumbnail/thumbnail-b.jpg` (대안).

## 녹음이 오면 (Aside가 `plans/southshore-longform/audio/ss_s01.m4a ~ ss_s10.m4a` 업로드)

```bash
cd videos/southshore-longform
pip install sherpa-onnx fonttools brotli numpy
# ASR 모델 (huggingface 막힘, GitHub releases 사용):
#   github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-zipformer-korean-2024-06-24.tar.bz2
#   github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2
YV_ASR_DIR=<models dir> YV_REDO_ASR=1 python3 -I tools/audio_prep.py   # 트림(앞뒤 0.3s)·노이즈·-16 LUFS + ASR
python3 -I tools/asr_check.py > ASR_CHECK.md                           # 대본과 다르게 읽은 줄 + 숫자 누락 표시
# ↑ 결과를 세션에 보고하고, 다르게 읽은 줄은 tools/script.py 행을 실제 말에 맞춤(숫자·사실은 바꾸지 않음).
#   더듬은 곳/재녹음 테이크는 tools/voice_edits.json 에 raw 시간으로 적어 잘라냄.
python3 -I tools/build.py                 # timing.json(실제 길이), compositions/, index.html 재생성
YV_FONTSRC=<npm pack @fontsource/black-han-sans @fontsource/noto-sans-kr 풀어 둔 폴더> python3 tools/fonts.py
python3 -I tools/build.py && python3 -I tools/shorts.py && python3 -I tools/thumbnail.py && python3 -I tools/short_covers.py
python3 -I tools/upload_text.py           # 챕터 시간이 실제 녹음 기준으로 바뀜
npm run check && npx hyperframes render -q delivery -o renders/video.mp4
cd ../southshore-shorts/short-a && npx hyperframes render -o ../renders/short-a.mp4   # b~e 동일
```

- 장면 사이 여백 0.4s, 첫 장면 0.5s, 마지막 엔드카드 4s 유지(`tools/timing.py`).
- 100MB 넘으면 기존처럼 `video.mp4.part-00/01` + `video.mp4.sha256` 으로 나눔.

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
