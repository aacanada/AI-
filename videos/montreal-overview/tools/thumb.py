"""Thumbnail 1280x720: python3 -I tools/thumb.py  (writes thumbnail/thumbnail.html + .png via Playwright)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import skyline, leaf, RED, INK, HI, SUB
ROOT = os.path.dirname(HERE)
F = "../assets/fonts"
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Black Han Sans"; src: url("{F}/BlackHanSans.woff2"); }}
@font-face {{ font-family: "Noto Sans KR"; src: url("{F}/NotoSansKR-900.woff2"); font-weight: 900; }}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1280px;height:720px;overflow:hidden;background:#FFF8F2;position:relative;font-family:"Noto Sans KR"}}
.sky{{position:absolute;left:-160px;top:330px;transform:scale(0.84);transform-origin:0 0}}
.t1{{position:absolute;left:56px;top:40px;font-family:"Black Han Sans";font-size:178px;line-height:1;color:{RED};letter-spacing:-2px}}
.t2{{position:absolute;left:62px;top:228px;font-family:"Black Han Sans";font-size:116px;line-height:1;color:{INK}}}
.mk{{position:relative;display:inline-block;isolation:isolate}} .mk:before{{content:"";position:absolute;left:-2%;width:104%;bottom:16%;height:40%;background:{HI};z-index:-1;border-radius:6px}}
.badge{{position:absolute;right:46px;top:58px;width:250px;height:250px;border-radius:50%;background:{RED};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(8deg);border:8px solid #fff;box-shadow:0 0 0 6px {RED}}}
.badge b{{font-family:"Black Han Sans";font-size:96px;line-height:.95}} .badge span{{font-weight:900;font-size:34px}}
.chips{{position:absolute;left:62px;top:372px;display:flex;gap:12px}} .chips span{{font-weight:900;font-size:30px;padding:8px 22px;border-radius:999px;background:#fff;border:4px solid {INK};color:{INK}}}
.chips span.r{{background:{RED};border-color:{RED};color:#fff}}
.logo{{position:absolute;right:28px;bottom:24px;width:120px;height:120px}}
.lf{{position:absolute;left:880px;top:300px;opacity:.9}}
</style></head><body>
<div class="sky">{skyline()}</div>
<div class="lf">{leaf(150, "#F2D2C9", 4)}</div>
<div class="t1">몬트리올,</div>
<div class="t2"><span class="mk">이것만</span> 보세요</div>
<div class="badge"><b>5분</b><span>핵심 정리</span></div>
<div class="chips"><span class="r">자녀무상교육</span><span>렌트비</span><span>교육청</span><span>진행 절차</span></div>
<img class="logo" src="../assets/img/logo.png">
</body></html>"""
p = os.path.join(ROOT, "thumbnail", "thumbnail.html")
open(p, "w", encoding="utf-8").write(html)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const pg=await b.newPage({{viewport:{{width:1280,height:720}}}});
await pg.goto('file://{p}');await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);await pg.screenshot({{path:'{os.path.join(ROOT,"thumbnail","thumbnail.png")}'}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True, cwd="/tmp")
print("ok")
