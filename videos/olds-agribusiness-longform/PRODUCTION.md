# Olds College Agribusiness long-form - production runbook

Brief: `plans/olds-agribusiness-longform/VIDEO_BRIEF.md` (main). Pipeline reused from the SGA long-form
(`claude/busy-fermat-uhhvcr`, `videos/sga-longform/`); BGM `bgm-a/bgm-b` = Vernon / SGA long-form (same files).

Everything that can be made without the voice and face videos is built. **Do NOT render until both arrive**,
then render once.

## Layout

- `tools/script.py` - 12 scenes: S01/S12 face rows, S02~S11 narration rows (verbatim from the brief), caption keywords (gold), footnotes, scene cards
- `tools/scenes_a.py` S01~S04 / `scenes_b.py` S05~S08 / `scenes_c.py` S09~S12; `tools/templates.py` - scene title cards + face video / placeholder
- `tools/common.py` - palette, GSAP helpers, shared graphics (Alberta map, check, arrow, particles) for later shorts
- `tools/timing.py` - slot layout; `tools/build.py` - writes `timing.json`, `compositions/*.html`, `index.html`
- Cues use `T('phrase')` = when that phrase is spoken, so every beat re-syncs to the real recording.
- Captions (<= 22 chars/line), brand line, scene pill, footnotes, BGM ducking, whooshes: generated in `index.html`.
- Provisional timing now: narration chars x 0.13 s, S01/S12 25 s each -> 5:45. The real read will be longer (brief: ~9-10 min).

## When the files arrive (main branch)

- `plans/olds-agribusiness-longform/audio/olds_ch02~ch11.m4a` **or** `olds_voice_full.m4a` (1 s pause between scenes)
- `plans/olds-agribusiness-longform/face/olds_face_open.mp4`, `olds_face_close.mp4` (1080p or 720p)

```bash
git fetch origin main && git checkout origin/main -- plans/olds-agribusiness-longform/audio plans/olds-agribusiness-longform/face
cd videos/olds-agribusiness-longform
python3 -I tools/audio_prep.py       # denoise, trim, loudnorm -16, (split full file by pauses) -> assets/voice/sNN.wav
cat assets/voice/_split.json          # check each cut (fallback_cut=true -> verify by ear / scene durations)
python3 -I tools/face_prep.py        # trim, 720p->1080p30, loudnorm -16 -> assets/face/open.mp4, close.mp4 (+ words.json)
python3 -I tools/build.py            # re-times all scenes, captions, ducking, CTA
npm run check
```
- Face captions follow what was actually said: if the director paraphrased, edit the S01/S12 rows in `tools/script.py`
  (meaning the same, never numbers/facts) and rebuild. Same for narration rows.
- A `T('phrase')` cue that no longer exists makes build.py stop with its name -> adjust that cue in `scenes_*.py`.
- Whisper (`hyperframes transcribe`, ko) is tried for word timing; if huggingface.co is blocked, rows are snapped to pauses.
- Slow read -> pitch-preserving atempo up to 1.1x; pauses > 0.7 s inside a scene shortened to 0.45 s; 0.35 s between scenes.
- One contact sheet per scene group (S01~04 / S05~08 / S09~12) with `npx hyperframes@0.8.174 snapshot . --at ... --no-end`.

## Render

```bash
npm run render    # -> renders/ ; copy to renders/video.mp4
```
Then fill the chapter timestamps in `upload-text.txt` from `timing.json` (S01 = 00:00, each scene card start),
and the files line in `meta.txt`.

## Publish (only after Aside gives the publish date)

Stage `publish/<date>-olds-agribusiness-longform/` on the `publish` branch per publish/README.md
(type: longform, channels: youtube, split > 100 MB, `READY` last). Not before.

## Facts guard (brief section 1)

2년 = "2년 과정(최소 16개월)" · DFS 유급/무급 둘 다 가능 ("유급 자리를 잡는 게 핵심", S01 각주 포함) ·
AOS "경력이 될 수 있다" + EOI 선발 · RRS 면제 "가능성 · 확인 필요" · 학비 2026-27 기준 각주 ·
배우자·가족 동반, 연봉, 거리·인구 숫자, "무조건/100%", 마감 임박 표현 없음.
