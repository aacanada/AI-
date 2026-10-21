"""Scene title card."""
from common import scene_html

CARD_CSS = """
R #{cid}-num{{left:140px;top:250px;font-size:400px;color:#e8b931}}
R #{cid}-ghost{{left:900px;top:-80px;font-size:900px;color:rgba(255,255,255,.07);font-weight:900;line-height:1}}
R #{cid}-bar{{left:150px;top:690px;width:180px;height:12px;border-radius:6px;background:#00b373}}
"""


def card(cid, ch, title, sub, duration, trk=32):
    body = f"""
          <div class="abs" id="{cid}-ghost" data-layout-allow-overflow>{ch:02d}</div>
          <div class="abs l" id="{cid}-k" style="left:160px;top:210px;font-size:34px;color:rgba(255,255,255,.7)">SCENE</div>
          <div class="abs num" id="{cid}-num">{ch:02d}</div>
          <div class="abs h" id="{cid}-t" style="left:720px;top:380px;font-size:120px;white-space:nowrap">{title}</div>
          <div class="abs hd" id="{cid}-s" style="left:726px;top:540px;font-size:52px;color:#e8b931;white-space:nowrap">{sub}</div>
          <div class="abs" id="{cid}-bar"></div>"""
    js = f"""
inn('#{cid}-k',0.05,{{y:14,d:0.4}});
slam('#{cid}-num',0.1,{{d:0.38}});
mask('#{cid}-t',0.45,0.6,'l');inn('#{cid}-s',0.8,{{y:16,d:0.5}});grow('#{cid}-bar',0.6,0.6);
tl.fromTo('#{cid}-ghost',{{x:80}},{{x:-60,duration:D,ease:'none'}},0);
"""
    audio = f'        <audio id="{cid}-sfx" src="assets/sfx/impact.mp3" data-start="0.45" data-duration="1.2" data-track-index="{trk}" data-volume="0.22" data-hf-media-start-basis="local"></audio>'
    return scene_html(cid, duration, CARD_CSS.format(cid=cid), body, js, "", audio)
