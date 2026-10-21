# Olds College Agribusiness long-form - production runbook

Brief: `plans/olds-agribusiness-longform/VIDEO_BRIEF.md` (main). Pipeline reused from the SGA long-form
(`claude/busy-fermat-uhhvcr`, `videos/sga-longform/`); BGM `bgm-a/bgm-b` = Vernon / SGA long-form (same files).

Final format (owner decision 2026-10): **no face video.** All 13 scenes are the director's voice
(`plans/olds-agribusiness-longform/audio/olds_ch01~12.m4a` + `olds_ch08b.m4a`) over photos / motion graphics.
Recording is final: rows in `tools/script.py` are the recorded sentences (ch08b jobs+wage is new, ch09 PGWP and
ch11 RRS were rewritten before recording). Change screen text to match the recording, never the other way round.

## Layout

- `tools/script.py` - 13 scenes (display S01~S13; ids s01..s08, s08b, s09..s12), audio file per scene, caption keywords, footnotes, scene cards
- `tools/scenes_a.py` S02~S04 / `scenes_b.py` S05~S08 / `scenes_c.py` AOS / `scenes_d.py` S01, jobs+wage, PGWP, RRS, closing+CTA
- `tools/templates.py` scene title cards; `tools/common.py` palette, GSAP helpers, shared graphics (Alberta map, check, arrow, particles)
- `tools/timing.py` slot layout (a scene whose recording is missing is left out and listed in `timing.json` "missing")
- `tools/build.py` writes `timing.json`, `compositions/*.html`, `index.html` (captions <= 22 chars, ducking, whooshes, footnotes)

## Rebuild from the recordings

```bash
git fetch origin main && git checkout origin/main -- plans/olds-agribusiness-longform/audio
cd videos/olds-agribusiness-longform
OLDS_NO_WHISPER=1 python3 -I tools/audio_prep.py   # denoise, trim, loudnorm -16, pauses > 0.7 s -> 0.45 s, atempo <= 1.1
python3 -I tools/build.py
npm run check
```
- `OLDS_NO_WHISPER=1`: huggingface.co is blocked in the cloud sandbox, so caption rows are snapped to pauses.
- A `T('phrase')` cue that no longer exists makes build.py stop with its name -> adjust that cue in `scenes_*.py`.

## Render

```bash
npx --yes hyperframes@0.8.174 render -o renders/video.mp4 --fps 30
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
