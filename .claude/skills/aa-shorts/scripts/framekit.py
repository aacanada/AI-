"""Frame authoring kit for AA Canada shorts (1080×1920, top captions).

Each video writes its own `scripts/build_frames.py`:

    import sys; sys.path.insert(0, "<repo>/.claude/skills/aa-shorts/scripts")
    from framekit import Kit
    k = Kit("videos/<slug>")
    k.frame("03-classroom", 3, css, html, js)   # js may use cues like {k.W(3, "100%")}

- Content lives inside a `.sh-stage` wrapper (translateY 170px, scale .85) so it sits
  below the top caption band (y 170–360) and above the Shorts bottom UI. Author in
  1080×1920 stage coordinates with content between y≈250 and y≈1580.
- `W(frame, prefix, nth=0, off=0)` = start time of the nth word starting with `prefix`
  in that frame's narration (audio_meta.json) — cue every reveal to the voice with it.
- JS helpers inside each frame: `tl`, `$(id)`, `count(id, to, at, dur, fmt)`.
- Prefix ids/classes with `fNN-` (frame number). Base classes available: .eyebrow,
  .h1 (em = cobalt), .card, .pill.soft, .pill.solid, .num.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(HERE, "frame_head.html")).read()

BASE_CSS = """
    #root { position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; font-family:"Pretendard",sans-serif; color:#111; }
    .bg { position:absolute; inset:0; background:#fdfae7; }
    .sh-stage { position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:50% 0; transform:translateY(170px) scale(0.85); }
    .eyebrow { position:absolute; left:80px; top:250px; display:flex; align-items:center; gap:20px; font-size:40px; font-weight:700; color:#1e2bfa; letter-spacing:.04em; }
    .eyebrow i { display:block; width:60px; height:5px; border-radius:3px; background:#1e2bfa; }
    .h1 { position:absolute; left:80px; right:80px; font-size:96px; font-weight:800; line-height:1.15; letter-spacing:-.03em; }
    .h1 em { font-style:normal; color:#1e2bfa; }
    .card { position:absolute; background:rgba(30,43,250,0.04); border:1.5px solid rgba(30,43,250,0.2); border-radius:14px; }
    .pill { position:absolute; padding:20px 40px; border-radius:100px; font-size:44px; font-weight:700; white-space:nowrap; }
    .pill.soft { background:rgba(30,43,250,0.08); color:#1e2bfa; }
    .pill.solid { background:#1e2bfa; color:#fdfae7; }
    .num { font-variant-numeric:tabular-nums; }
"""


class Kit:
    def __init__(self, project):
        self.project = os.path.abspath(project)
        meta = json.load(open(os.path.join(self.project, "audio_meta.json")))
        self.voices = {v["frame"]: v for v in meta["voices"]}

    def W(self, frame, prefix, nth=0, off=0.0):
        hits = [w for w in self.voices[frame]["words"] if w["text"].startswith(prefix)]
        if len(hits) <= nth:
            raise KeyError(f"frame {frame}: no word #{nth} starting with {prefix!r}")
        return round(max(0.0, hits[nth]["start"] + off), 2)

    def duration(self, frame):
        return self.voices[frame]["duration_s"]

    def frame(self, fid, frame_no, css, html, js):
        dur = self.duration(frame_no)
        n = fid[:2]
        doc = f"""<template>
{HEAD}
{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{fid}" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
    <div id="f{n}-bg" class="bg clip" data-start="0" data-duration="{dur}" data-track-index="0"></div>
    <div class="sh-stage" id="f{n}-stage">
{html}
    </div>
  </div>
  <script>
    (function(){{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);
      const count = (id, to, at, d, fmt) => {{
        const el = $(id), st = {{ v: 0 }};
        tl.to(st, {{ v: to, duration: d, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(Math.round(st.v)); }} }}, at);
      }};
{js}
      window.__timelines["{fid}"] = tl;
    }})();
  </script>
</template>
"""
        out = os.path.join(self.project, "compositions/frames", fid + ".html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(doc)
        print(f"✓ {fid} ({dur}s)")
