# 버논 고등학교 탐방 쇼츠 (6편)

브리프: `plans/vernon-schools-shorts/VIDEO_BRIEF.md`. 공통 템플릿은 `shared/`, 편마다 `short-N-*/script.json` 만 다릅니다.

| 파일 | 역할 |
|---|---|
| `short-N-*/script.json` | 대본 chunks + 장면별 비주얼(items) + 썸네일 + 게시 정보. 편마다 이것만 수정 |
| `shared/build.py` | script.json + timing.json → `index.html` (HyperFrames, 셰이더 전환·키네틱 타이포·오도미터·지도·3D 카드) |
| `shared/engine.js`, `shared/style.css`, `shared/template.html` | 공통 모션 엔진/스타일 |
| `shared/narration_full.py` | 원장님 통파일 `short-N_full.m4a` → 장면별 분할(무음 + 대본 글자수 DP 정렬), 장면 사이 무음 0.35초로, 장면 안 쉼 최대 0.5초, loudnorm I=-16 + afftdn → `narration.wav` + `timing.json` |
| `shared/narration.py` | 장면별 파일 `short-N_sK.m4a` 로 올 때 |
| `shared/asr_ko.py` | 한국어 ASR(sherpa-onnx zipformer-korean)로 녹음 문구 확인 — 대본과 다르게 읽은 곳은 자막을 녹음에 맞춤 |
| `shared/estimate_timing.py` | 녹음 전 임시 타이밍(글자 수 × 0.13초) |
| `shared/thumbnail.py`, `shared/meta.py` | 썸네일 PNG/JPG, 게시 대기함 meta.txt |

## 녹음이 오면 (편마다)

```bash
git checkout origin/main -- plans/vernon-schools-shorts/audio
python3 shared/narration_full.py short-N-x ../../plans/vernon-schools-shorts/audio   # [--tempo 1.05] (최대 1.1)
python3 shared/asr_ko.py ../../plans/vernon-schools-shorts/audio/short-N_full.m4a <model-dir>   # 문구 확인
python3 shared/build.py short-N-x && (cd short-N-x && npx hyperframes lint && npx hyperframes snapshot --at ...)
(cd short-N-x && npx hyperframes render --quality high --output renders/video.mp4)
python3 shared/thumbnail.py short-N-x && python3 shared/meta.py short-N-x
```

BGM: 버논 롱폼과 같은 `shared/bgm/bgm-a.mp3`, `bgm-b.mp3` (나레이션 구간 자동 덕킹). SFX: HyperFrames 번들(`shared/sfx/CREDITS.md`).
