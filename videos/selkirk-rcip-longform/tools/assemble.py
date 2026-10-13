#!/usr/bin/env python3
"""timing.json → index.html(챕터 + 내레이션 + 자막 + 챕터 전환) 와 compositions/captions.html"""
import json, pathlib
proj = pathlib.Path(__file__).resolve().parent.parent
T = json.load(open(proj / "timing.json"))
total = T["total"]
chs = [c for c in T["chapters"] if (proj / "compositions" / f'{c["id"]}.html').exists()]

# ---- captions
cues = [cap for c in T["chapters"] for cap in c["captions"]]
items = "\n".join(
    f'  <div class="cue clip" id="cap-{i}" data-start="{c["t"]}" data-duration="{round(max(0.4, (cues[i+1]["t"] if i+1 < len(cues) and cues[i+1]["t"] - c["end"] < 0.6 else c["end"] + 0.25) - c["t"] - 0.04), 2)}"><span>{c["text"]}</span></div>'
    for i, c in enumerate(cues))
(proj / "compositions" / "captions.html").write_text(f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
@font-face{{font-family:Pretendard;font-weight:700;src:url(assets/fonts/Pretendard-Bold.woff2) format("woff2")}}
#captions{{position:absolute;inset:0;pointer-events:none}}
#captions .cue{{position:absolute;left:0;right:0;top:auto;bottom:56px;height:auto;display:flex;justify-content:center}}
#captions .cue span{{background:#16324F;color:#FAF6EF;font-family:Pretendard,sans-serif;font-weight:700;font-size:40px;line-height:1.3;padding:12px 30px;border-radius:14px;word-break:keep-all;max-width:1500px;text-align:center}}
      </style>
      <div id="captions" data-composition-id="captions" data-width="1920" data-height="1080" data-duration="{total}">
{items}
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          window.__timelines["captions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
""", encoding="utf-8")

# ---- index
hosts, trans = [], []
for i, c in enumerate(chs):
    hosts.append(f'''      <div id="{c["id"]}" class="clip" data-composition-id="{c["id"]}" data-composition-src="compositions/{c["id"]}.html"
        data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="{1 + i % 2}" data-width="1920" data-height="1080"></div>''')
    if i > 0:
        T1 = c["start"]
        trans.append(f'tl.fromTo("#{chs[i-1]["id"]}", {{ xPercent: 0 }}, {{ xPercent: -100, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {T1});')
        trans.append(f'tl.fromTo("#{c["id"]}", {{ xPercent: 100 }}, {{ xPercent: 0, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {T1});')
end = max(c["start"] + c["duration"] for c in chs)
dur = total if len(chs) == len(T["chapters"]) else round(end, 2)
(proj / "index.html").write_text(f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>셀커크 컬리지 × RCIP</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #FAF6EF; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #FAF6EF; }}
    </style>
  </head>
  <body>
    <!-- tools/assemble.py 로 생성 (timing.json 기준). 직접 고치지 말고 스크립트를 다시 실행하세요. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
      <audio id="narration" src="{T["voice"]}" data-start="0" data-duration="{min(T["voice_dur"], dur)}" data-track-index="8" data-volume="1"></audio>
      <div id="captions-host" data-track-kind="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{dur}" data-track-index="9" data-width="1920" data-height="1080"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // 챕터 전환: push slide (오른쪽에서 들어와 왼쪽으로)
      {(chr(10) + "      ").join(trans)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""", encoding="utf-8")
print("chapters", [c["id"] for c in chs], "dur", dur, "cues", len(cues))
