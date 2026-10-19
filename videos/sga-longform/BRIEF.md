---
workflow: general-video
flow: automation
storyboard: no
message: "공립은 스스로 관리하는 시스템이라 처음 온 유학생이 놓치기 쉽다 — 2주마다 성적표가 오는 토론토 노스욕 관리형 사립고 SGA"
destination: youtube
aspect: 1920x1080
language: ko
audience: 토론토 조기유학을 검토하는 한국 학부모 (중3~고2 자녀)
length: 9-10m (provisional 7m17s at 0.13 s/char until the recording lands)
angle: explainer
---

## Intent

Source of truth: `../../plans/sga-longform/VIDEO_BRIEF.md` (script, scene design, facts, bans). Faceless
motion graphics + SGA photos + student testimonial clips, narrated by the director's own recording
(`sga_ch01~09.m4a`, no TTS). Routed to general-video because the piece is ~10 minutes.

## Assets

- assets/photos, assets/brochure: resized/cropped from plans/sga-longform/assets by tools/prep_assets.py
- assets/music/bgm-a.mp3, bgm-b.mp3: same calm royalty-free beds as the Vernon long-form (chained, ducked)
- assets/sfx: whoosh / pop / impact / stamp from the HyperFrames bundled Pixabay library (CREDITS.md)
- assets/clips/T1~T4.mp4: pending (YouTube blocked in the cloud sandbox) - placeholder cards render until then
- assets/voice/sNN.wav: pending recording

## Customizations

- Chapter title cards CH2-CH9 (number slam + mask reveal; leak / flash / zoom-blur transitions rotate)
- Scene-to-scene wipe / slide (0.45 s), odometer counters with slam + 3-frame shake, line-draw diagrams,
  chip pops, stamps, Ken Burns, light sweep on chapter-first photos, dust particles (S01) and gold burst (S32)
- Mascot Oly 4x (CH4 card, S21, S24, S32)
- Brand line + chapter pill + footnotes + captions live in index.html so scenes stay reusable for shorts
