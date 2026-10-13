#!/usr/bin/env python3
"""tools/src/<id>.html → compositions/<id>.html
src 파일은 <!--ROOT:id DUR:sec--> 한 줄, 그 아래 마크업, 그리고 <script> 본문만 담는다.
공통 CSS(tools/common.css)와 헬퍼(tools/helpers.js)를 끼워 넣어 완전한 sub-composition을 만든다."""
import re, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
proj = here.parent
css = (here / "common.css").read_text()
helpers = (here / "helpers.js").read_text()
for src in sorted((proj / "tools" / "src").glob("*.html")):
    t = src.read_text()
    m = re.search(r"<!--ROOT:(\S+) DUR:([\d.]+)-->", t)
    rid, dur = m.group(1), m.group(2)
    style = re.search(r"<style>(.*?)</style>", t, re.S)
    extra_css = style.group(1) if style else ""
    body = re.sub(r"<style>.*?</style>", "", t[m.end():], flags=re.S)
    js = re.search(r"<script>(.*?)</script>", body, re.S).group(1)
    markup = re.sub(r"<script>.*?</script>", "", body, flags=re.S).strip()
    out = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{css.replace('ROOT', rid)}
{extra_css.replace('ROOT', rid)}
      </style>
      <div id="{rid}" data-composition-id="{rid}" data-width="1920" data-height="1080" data-duration="{dur}">
{markup}
      </div>
      <script>
        (function () {{
{helpers.replace('ROOT', rid)}
const D = {dur};
{js}
window.__timelines["{rid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
    (proj / "compositions" / f"{rid}.html").write_text(out)
    print("built", rid)
