#!/usr/bin/env python3
"""tools/src/<short>.html + <short>/timing.json → <short>/index.html (1080x1920 standalone)
- <section id=".." class="beat" data-beat="a-b"> : 구간 a 시작 0.2초 전 ~ 구간 b 시작 0.2초 전 (b=end → 엔드카드 전까지, cta → 영상 끝)
- 스크립트에서 S[i](구간 시작), P[i](말 시작), D(전체 길이), V(음성 끝) 사용
"""
import re, json, pathlib, shutil
here = pathlib.Path(__file__).resolve().parent; proj = here.parent
css = (here / "common.css").read_text(); helpers = (here / "helpers.js").read_text()
CTA = 3.6
for src in sorted((here / "src").glob("*.html")):
    sid = src.stem; T = json.load(open(proj / sid / "timing.json"))
    S = T["S"]; P = [s["speak"] for s in T["segs"]]; V = T["voice_dur"]; D = round(V + CTA, 2)
    t = src.read_text()
    style = re.search(r"<style>(.*?)</style>", t, re.S); extra = style.group(1) if style else ""
    body = re.sub(r"<style>.*?</style>", "", t, flags=re.S)
    js = re.search(r"<script>(.*?)</script>", body, re.S).group(1)
    markup = re.sub(r"<script>.*?</script>", "", body, flags=re.S).strip().replace("<!--CTA-->", (here / "cta.html").read_text())
    js += """
inn('#cta-k',V+0.15,{y:16}); whip('#cta-t',V+0.3,90); grow('#cta-r',V+0.8,0.5);
inn('#cta-p',V+1.0,{x:-30,y:0}); inn('#cta-kk',V+1.3,{x:-30,y:0}); pop('#cta-c',V+1.8);
"""
    for m in re.finditer(r'<img src="assets/img/([^"]+)"', markup):
        shutil.copy(proj.parent / "selkirk-rcip-longform/assets/img" / m.group(1), proj / sid / "assets/img" / m.group(1))
    fades = []
    def beat(mm):
        sidd = mm.group(1)
        if mm.group(2) == "cta":
            return f'id="{sidd}" class="beat clip" data-start="{round(V - 0.05, 2)}" data-duration="{round(D - V + 0.05, 2)}"'
        a, b = mm.group(2).split("-")
        s0 = 0.0 if int(a) == 0 else round(S[int(a)] - 0.2, 2)
        e = round(V + 0.1, 2) if b == "end" else (D if b == "cta" else round(S[int(b)] - 0.2, 2))
        if b not in ("cta",): fades.append((sidd, e))
        return f'id="{sidd}" class="beat clip" data-start="{s0}" data-duration="{round(e - s0, 2)}"'
    markup = re.sub(r'id="([^"]+)" class="beat" data-beat="([^"]+)"', beat, markup)
    markup = re.sub(r'(<section [^>]*class="beat clip"[^>]*>)(.*?)(</section>)', lambda mm: f'{mm.group(1)}<div class="in">{mm.group(2)}</div>{mm.group(3)}', markup, flags=re.S)
    fade_js = "\n".join(f"tl.fromTo(q('#{x} .in'),{{opacity:1}},{{opacity:0,duration:0.22,ease:'power1.in',immediateRender:false}},{round(e - 0.24, 2)});" for x, e in fades)
    caps = [c for s in T["segs"] for c in s["captions"]]
    cap_html = "\n".join(
        f'<div class="cue clip" id="cap-{i}" data-start="{c["t"]}" data-duration="{round(max(0.4, (caps[i+1]["t"] if i + 1 < len(caps) and caps[i+1]["t"] - c["end"] < 0.5 else c["end"] + 0.2) - c["t"] - 0.03), 2)}"><span>{c["text"]}</span></div>'
        for i, c in enumerate(caps))
    rid = "sroot"
    html = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{sid}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #FAF6EF; }}
{css.replace('ROOT', rid)}
#{rid} .in{{position:absolute;inset:0}}
#{rid} .cue{{position:absolute;left:0;right:0;top:1390px;height:auto;display:flex;justify-content:center;z-index:40}}
#{rid} .cue span{{background:#16324F;color:#FAF6EF;font-weight:800;font-size:54px;line-height:1.3;padding:14px 34px;border-radius:18px;max-width:960px;text-align:center}}
{extra.replace('ROOT', rid)}
    </style>
  </head>
  <body>
    <!-- tools/build.py 로 생성 -->
    <div id="{rid}" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{D}">
{markup}
{cap_html}
      <audio id="voice" src="assets/voice/voice.mp3" data-start="0" data-duration="{V}" data-track-index="8" data-volume="1"></audio>
    </div>
    <script>
      (function () {{
{helpers.replace('ROOT', rid)}
const D = {D}, V = {V};
const S = {json.dumps(S)}, P = {json.dumps(P)};
{js}
{fade_js}
window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    (proj / sid / "index.html").write_text(html)
    for f in ["hyperframes.json", "package.json"]:
        src_f = proj.parent / "selkirk-rcip-longform" / f
        (proj / sid / f).write_text(src_f.read_text().replace("selkirk-rcip-longform", sid))
    print("built", sid, D)
