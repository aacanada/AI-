---
workflow: general-video
flow: automation
storyboard: no
message: "영유 비용이면 몬트리올에서 아이가 영어로 '생활'한다 — 아이 학비 0원, 아이가 많을수록 유리"
destination: youtube
aspect: 1920x1080
language: ko
audience: 영어유치원에 아이를 보내거나 고민 중인 한국 부모 (특히 자녀 2명 이상)
length: ~8m (director's 11 recordings after trims/retake cuts)
angle: explainer
---

## Intent

Source of truth: `../../plans/yeongyu-montreal-longform/VIDEO_BRIEF.md` + `SCRIPT.txt`. Faceless, all-graphics, narrated by
the director's own recordings (yv_s01~s11). Compare only 영어유치원 vs 캐나다(몬트리올) 자녀무상교육 — 관리형 조기유학
never appears. Kindergarten age is "그해 9월 30일 기준 만 4세" (never 만 5세). No 불어 in title/thumbnail.

## Assets

- Brand template "메이플 레드" (cream #FFF8F2, red #C8102E, text #2B2B2B, highlight #FFD6CF, sub #7A1B26; no blue)
- Fonts: Black Han Sans + Noto Sans KR (npm @fontsource, subset by tools/fonts.py)
- Logo + blog cards: plans/yeongyu-montreal-longform/assets → assets/img
- Canada map: @svg-maps/canada (CC BY 4.0) → tools/canada_map.json, credited in the S07 footnote
- BGM bgm-a/b + SFX: same beds/library as the SGA long-form (Pixabay license, assets/sfx/CREDITS.md)
- No photos (Pexels/Unsplash unreachable from the sandbox) — every scene is drawn (SVG/HTML)

## Customizations

- Captions: full narration, white box, numbers/keys in red; source footnotes per brief
- Shorts A-F 9:16 reuse the same scene files (window-scrubbed) → ../yeongyu-montreal-shorts/
