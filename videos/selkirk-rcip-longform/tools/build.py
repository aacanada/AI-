#!/usr/bin/env python3
"""tools/src/<id>.html → compositions/<id>.html  (timing.json 기반)

src 규칙
- 첫 줄 <!--ROOT:<id>-->  (길이 D와 문장 시각 R은 timing.json에서 주입)
- 장면 구간: <section class="beat" data-beat="a-b"> → 문장 a 시작 0.3초 전부터 문장 b 시작 0.3초 전까지 (b=end면 챕터 끝)
- 스크립트에서 D, R[i] 사용 가능. 각 beat는 끝나기 직전 0.3초 페이드아웃이 자동으로 붙는다(마지막 beat 제외).
"""
import re, json, pathlib
here = pathlib.Path(__file__).resolve().parent
proj = here.parent
css = (here / "common.css").read_text()
helpers = (here / "helpers.js").read_text()
timing = {c["id"]: c for c in json.load(open(proj / "timing.json"))["chapters"]}
PRE = 0.3
for src in sorted((here / "src").glob("*.html")):
    t = src.read_text()
    m = re.search(r"<!--ROOT:(\S+)(?: DUR:[\d.]+)?-->", t)
    rid = m.group(1)
    ch = timing[rid]; D = ch["duration"]; R = ch["R"]
    style = re.search(r"<style>(.*?)</style>", t, re.S)
    extra_css = style.group(1) if style else ""
    body = re.sub(r"<style>.*?</style>", "", t[m.end():], flags=re.S)
    js = re.search(r"<script>(.*?)</script>", body, re.S).group(1)
    markup = re.sub(r"<script>.*?</script>", "", body, flags=re.S).strip()
    fades = []
    def beat(mm):
        a, b = mm.group(2).split("-")
        s = 0.0 if int(a) == 0 else round(R[int(a)] - PRE, 2)
        e = D if b == "end" else round(R[int(b)] - PRE, 2)
        sid = mm.group(1)
        if b != "end": fades.append((sid, e))
        return f'id="{sid}" class="beat clip" data-start="{s}" data-duration="{round(e - s, 2)}"'
    markup = re.sub(r'id="([^"]+)" class="beat" data-beat="([^"]+)"', beat, markup)
    fade_js = "\n".join(f"tl.fromTo(q('#{sid} .in'),{{opacity:1}},{{opacity:0,duration:0.28,ease:'power1.in',immediateRender:false}},{round(e - 0.3, 2)});" for sid, e in fades)
    # 각 beat 내용은 .in 래퍼로 감싼다
    markup = re.sub(r'(<section [^>]*class="beat clip"[^>]*>)(.*?)(</section>)', lambda mm: f'{mm.group(1)}<div class="in">{mm.group(2)}</div>{mm.group(3)}', markup, flags=re.S)
    out = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{css.replace('ROOT', rid)}
#{rid} .in{{position:absolute;inset:0}}
{extra_css.replace('ROOT', rid)}
      </style>
      <div id="{rid}" data-composition-id="{rid}" data-width="1920" data-height="1080" data-duration="{D}">
{markup}
      </div>
      <script>
        (function () {{
{helpers.replace('ROOT', rid)}
const D = {D};
const R = {json.dumps(R)};
{js}
{fade_js}
window.__timelines["{rid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
    (proj / "compositions" / f"{rid}.html").write_text(out)
    print("built", rid, D)
