# 영유 vs 몬트리올 long-form — production runbook

```bash
cd videos/yeongyu-montreal-longform
pip install sherpa-onnx fonttools brotli numpy
# ASR models (huggingface is blocked in the sandbox; GitHub releases work):
#   github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2
#   github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-zipformer-korean-2024-06-24.tar.bz2
YV_ASR_DIR=<models dir> YV_REDO_ASR=1 python3 -I tools/audio_prep.py   # clean + ASR (slow: ~5 min/file on 4 CPUs)
python3 -I tools/audio_prep.py           # re-clean only (keeps ASR in assets/voice/_asr.json)
python3 -I tools/asr_check.py > ASR_CHECK.md
python3 -I tools/build.py                # timing.json, compositions/sNN.html, index.html
YV_FONTSRC=<dir with npm-packed @fontsource/black-han-sans + noto-sans-kr> python3 -I tools/fonts.py
python3 -I tools/build.py && python3 -I tools/shorts.py && python3 -I tools/thumbnail.py
npm run check && npm run render
```

- `tools/script.py` rows = what was actually read (captions). `T('phrase')` cues in `tools/scenes_*.py` re-sync to speech.
- `tools/voice_edits.json`: retakes/stumbles cut from the raw recordings (raw time). Inner pauses > 1.0 s → 0.7 s.
- Whisper in sherpa-onnx drops half-syllable byte tokens; audio_prep loads a `<id>` token table and rebuilds the bytes.

## Recording vs script (ASR, confirmed with re-transcription at several offsets)

| scene | what was read | status |
|---|---|---|
| s08 | "9월 30일 기준으로 **만 5세**면 다닐 수 있습니다." (script: 그해 9월 30일 기준으로 만 4세면 유치원에 다닐 수 있습니다.) raw 17.18–21.38 s | **원장님 결정 대기 — 렌더 보류** |
| s01 | "AA Canada입니다" (원장 생략) | 자막을 녹음대로 |
| s11 | "첫 번째," (첫째) | 자막을 녹음대로 |
| s02 | "2020…" 말 바꿈, "월평균 교집 교…평균" 더듬음 | 컷 (voice_edits.json) |
| s03 / s08 / s11 | 같은 문장 두 번 읽음 (재녹음 테이크) | 앞 테이크 컷 |
| all | "관리형" 없음 | OK |
