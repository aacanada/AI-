# NSISP vs NISEP 롱폼 (production)

입력: `plans/nsisp-nisep-longform/` (VIDEO_BRIEF.md, SCRIPT.md, audio/S1~S9.mp3, heygen/S1_face.mp4·S9_face.mp4).
구조와 파이프라인은 `videos/olds-diploma-longform`(브랜치 claude/youthful-archimedes-h2obtb)을 따름.

```bash
cd videos/nsisp-nisep-longform
cp ../../plans/nsisp-nisep-longform/heygen/*.mp4 assets/face/   # gitignore 대상
python3 -I tools/asr.py            # ElevenLabs Scribe 단어 타임스탬프 -> assets/voice/asr/SN.json (자막·큐 타이밍)
python3 -I tools/build.py && npm run check
npx --yes hyperframes@0.8.174 render -o renders/video_hf.mp4 --fps 30
python3 -I tools/mix.py            # 내레이션 -16 LUFS + BGM + SFX -> renders/video.mp4, renders/loudness.json
```

- 타임라인: S1 얼굴(0초) → 장면 사이 0.5초 여백, 그림 전환 0.4초 크로스페이드 → S9 얼굴 → 3초 엔드카드. 총 316.1초(5:16).
- S1/S9 소리는 HeyGen 클립 오디오를 그대로 씀 (S1/S9 mp3는 재생하지 않음, 자막 타이밍 계산에만 사용).
- 자막: `tools/script.py` (대본 기준). 화면 규칙상 최상급 표현을 빼서 내레이션과 몇 단어 다름:
  S1 "가장 먼저 찾는 곳" → "먼저 찾는 곳", S3 "가장 많이 물어보시는" → "많이 물어보시는",
  S6 "제일 걱정되는 건" → "걱정되는 건", S9 "아이 소식이 제일 궁금하시죠" → "아이 소식이 궁금하시죠".
- 화면 규칙: 출처 표기 없음, 최상급 없음, NSISP 비용 숫자 없음, 커미션 없음, 대학 로고 없음(텍스트 카드).
- 지도: `tools/canada_map.json` (영유 vs 몬트리올 롱폼에서 재사용).
