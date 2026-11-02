"""Thumbnail, upload-text.txt and meta.txt for one short: python3 -I tools/package.py <N> <publish-date YYYY-MM-DD>
(run from videos/sga-shorts after the render; writes into sN/)."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shorts import SHORTS  # noqa: E402

N, DATE = int(sys.argv[1]), sys.argv[2]
SP, D = SHORTS[N], f"s{N}"
LONG = "https://youtu.be/UDw6TbnewKU"
CHROME = "/opt/pw-browsers/chromium"

th = SP["thumb"]
lines = "".join(f'<div class="ln" style="color:{c}">{t}</div>' for t, c in th["lines"])
stamp = ('<svg class="x" viewBox="0 0 300 300"><circle cx="150" cy="150" r="130" fill="none" stroke="#c8102e" stroke-width="18"/>'
         '<path d="M85 85 L215 215 M215 85 L85 215" stroke="#c8102e" stroke-width="26" stroke-linecap="round"/></svg>') if th.get("stamp") else ""
html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8" /><title>SGA Short {N}</title>
<style>
@font-face{{font-family:Pretendard;font-weight:800;src:url(../assets/fonts/Pretendard-ExtraBold.woff2) format("woff2")}}
@font-face{{font-family:Pretendard;font-weight:900;src:url(../assets/fonts/Pretendard-Black.woff2) format("woff2")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#14254a;font-family:Pretendard,sans-serif}}
.ph{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.ph img{{width:100%;height:100%;object-fit:cover;filter:brightness(.42) saturate(.7)}}
.gr{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:linear-gradient(180deg,rgba(20,37,74,.2) 0%,rgba(20,37,74,.75) 45%,rgba(20,37,74,.95) 100%)}}
.brand{{position:absolute;left:0;width:1080px;top:200px;text-align:center;color:rgba(255,255,255,.92);font-weight:800;font-size:34px;letter-spacing:.06em}}
.box{{position:absolute;left:70px;width:940px;top:560px}}
.ln{{font-weight:900;font-size:172px;line-height:1.12;letter-spacing:-.04em;text-shadow:0 8px 30px rgba(0,0,0,.5)}}
.x{{position:absolute;right:60px;top:200px;width:300px;height:300px;transform:rotate(-12deg)}}
.pill{{position:absolute;left:70px;top:1260px;background:#e8b931;color:#14254a;font-weight:900;font-size:50px;padding:18px 40px;border-radius:99px}}
.sga{{position:absolute;left:74px;top:1400px;color:rgba(255,255,255,.85);font-weight:800;font-size:40px}}
</style></head><body>
<div class="ph"><img src="../assets/photos/{th['photo']}.jpg" alt="" /></div><div class="gr"></div>
<div class="brand">AA CANADA · 토론토 조기유학</div>
<div class="box">{lines}{stamp}</div>
<div class="pill">{th['pill']}</div>
<div class="sga">노스욕 St. George Academy</div>
</body></html>"""
open(f"{D}/thumbnail.html", "w", encoding="utf-8").write(html)
png = os.path.abspath(f"{D}/.thumb.png")
subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                "--window-size=1080,2100", "--virtual-time-budget=4000", f"--screenshot={png}", "file://" + os.path.abspath(f"{D}/thumbnail.html")],
               check=True, capture_output=True)
from PIL import Image  # noqa: E402
Image.open(png).convert("RGB").crop((0, 0, 1080, 1920)).save(f"{D}/thumbnail.jpg", quality=90)
os.remove(png)

u = SP["upload"]
tm = json.load(open(f"{D}/timing.json"))
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/video.mp4"]))
text = f"""[유튜브 제목]
{u['title']}

[유튜브 설명]
{u['first']}
{u['body']}

▶ 전체 영상(롱폼): {LONG}
▶ 우리 아이 필요 학점 무료 계산 · 상담: 카카오톡 canlog · 02-567-4345
무료 상담신청 https://forms.gle/QcH198mQWJEF1LSc8

{u['note']}
※ 나레이션은 AI 합성 음성입니다.

{u['tags']}

[인스타 캡션]
{u['first']}
{u['body']}

전체 영상은 유튜브 AA Canada 채널에서 볼 수 있습니다.
무료 학점 계산 · 상담: 카카오톡 canlog

{u['tags'].replace(' #shorts', '')}
"""
open(f"{D}/upload-text.txt", "w", encoding="utf-8").write(text)
meta = f"""type: short
title: {u['title']}
channels: youtube, instagram-reels, threads, naver-clip
visibility: public
publish_order: {N}
publish_after: {DATE}
linked_to: {LONG}
files: video.mp4 ({int(dur // 60)}:{dur % 60:04.1f}, 1080x1920 30fps), thumbnail.jpg (1080x1920), upload-text.txt
source: aacanada/AI- branch claude/busy-fermat-uhhvcr, videos/sga-shorts/ (tools/shorts.py #{N})
notes: 나레이션 ElevenLabs "일곱번째" 합성 음성 -> 업로드 때 변경·합성 콘텐츠 표시를 켤 것. 학생 얼굴 노출 없음. 게시일은 하루 1편 이하로 조정 가능.
"""
open(f"{D}/meta.txt", "w", encoding="utf-8").write(meta)
print(f"{D}: thumbnail, upload-text, meta ({dur:.1f}s)")
