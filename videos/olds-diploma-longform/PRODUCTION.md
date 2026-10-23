# Olds College 전공 시리즈 EP2 - 2년 디플로마 3가지 (production)

Script: `plans/olds-diploma-longform/SCRIPT.txt` section 4 (s08 last sentence changed per owner). Pipeline = EP1
(`videos/olds-agribusiness-longform`) tools: `tools/script.py` rows/keys/foot + `SAY` (TTS-only pronunciation),
`tools/scenes.py` (9 scenes), `tools/templates.py` (cards + major icons), `tools/timing.py`, `tools/build.py`.

```bash
cd videos/olds-diploma-longform
python3 -I tools/tts.py            # ElevenLabs "일곱번째" with timestamps -> plans/olds-diploma-longform/audio/oldsdip_sNN.mp3
python3 -I tools/build.py && npm run check
npx --yes hyperframes@0.8.174 render -o renders/video.mp4 --fps 30
python3 -I tools/shorts.py         # ../olds-diploma-shorts/{techgronomy,horticulture,agmanagement}
(cd ../olds-diploma-shorts/<key> && npx --yes hyperframes@0.8.174 render -o renders/video.mp4 --fps 30)
```
Captions use the TTS character timestamps (exact). Voice QC: `voice_qc.md`. Design review: `DESIGN_NOTES.md`.
