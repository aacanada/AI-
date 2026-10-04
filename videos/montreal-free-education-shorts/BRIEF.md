---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "부모가 사설어학원을 다니면서 몬트리올 자녀무상교육이 가능하다 — AA Canada 독점 프로그램"
destination: shorts
aspect: "9:16"
language: ko
voice: "ElevenLabs cloned voice '네 번째' (9qtE9eIaqHMUAfRp4QTW), speed 1.12"
length: ~84s
---

## Intent
사설어학원을 통한 캐나다 몬트리올 자녀무상교육 쇼츠. 오해 2가지 반박 → 해답 → 장점 → 프로그램 정보 → 학비 → 자녀 언어 → 장기 플랜 → 패스트트랙 → CTA.

## Notes
- Narration: ElevenLabs `with-timestamps` per scene (`gen_tts.py`), captions/reveals anchored to char timings (`build.py`).
- BGM: ElevenLabs Music (instrumental), trimmed + faded to video length.
- Rebuild: `python3 build.py && npx hyperframes render --quality high --output renders/video.mp4`.
