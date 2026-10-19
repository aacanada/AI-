# SGA long-form - production runbook

Everything that can be made without the narration is built. Do NOT render until the recording is in.

## Layout

- `tools/script.py` - narration rows (verbatim from VIDEO_BRIEF), keywords (gold in captions), footnotes, chapters, clips
- `tools/scenes_a.py / scenes_b.py / scenes_c.py` - 29 narration scenes; `tools/templates.py` - chapter cards + testimonial clips
- `tools/timing.py` - slot layout; `tools/build.py` - writes `timing.json`, `compositions/*.html`, `index.html`
- Scene animation cues use `T('phrase')` = when that phrase is spoken, so every beat re-syncs to the real recording.
- Captions (<= 22 chars/line, 1 line), brand line, chapter pill, footnotes, BGM ducking, whooshes: generated in `index.html`.

## When the recording arrives (`plans/sga-longform/audio/sga_ch01~09.m4a`)

```bash
cd videos/sga-longform
python3 -I tools/audio_prep.py        # denoise, trim, loudnorm -16, split by pauses -> assets/voice/sNN.wav
cat assets/voice/_split.json           # check each scene cut (fallback_cut=true means verify by ear)
python3 -I tools/build.py              # re-times all scenes, captions, ducking
npm run check
```
- If a line was read differently from the script, edit the row in `tools/script.py` to match the recording
  (never numbers/facts) and rebuild. A `T('phrase')` cue that no longer exists makes build.py stop with its name.
- Whisper (`hyperframes transcribe`, ko) is tried for word timing; in the cloud sandbox huggingface.co is
  blocked, so rows are snapped to detected pauses instead.

## When the testimonial clips arrive (`plans/sga-longform/assets/clips/T1~T4.mp4`)

```bash
python3 -I tools/clip_prep.py          # cut brief ranges +-1 s, trim to speech, 1080p30, loudnorm
python3 -I tools/build.py
```
Check the subtitles against the audio; for exact timing write `assets/clips/Tn.subs.json`. Skip any part
where a previous school's name is audible.

## Render and publish

```bash
npm run render   # -> renders/ ; copy to renders/video.mp4
```
Then fill the chapter timestamps in `upload-text.txt` from `timing.json` (first slot start of each chapter),
fill `meta.txt` files line, and stage `publish/2026-11-10-sga-longform/` on the `publish` branch
(split >90 MB per publish/README.md, `READY` last).
