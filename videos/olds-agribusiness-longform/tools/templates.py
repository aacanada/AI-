"""Scene title card and face-video (S01 / S12) backgrounds."""
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


FACE_CSS = """
R #{cid}-fv{{position:absolute;inset:0;overflow:hidden;background:#082a1f}}
R #{cid}-fv video{{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(1.05) contrast(1.03)}}
R #{cid}-ph{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:repeating-linear-gradient(135deg,#124a37 0 40px,#0f3d2e 40px 80px)}}
"""


def face_bg(cid, slot, trk):
    """Full-screen director video (original sound) or a placeholder card of the same length."""
    if slot["real"]:
        inner = (f'<video id="{cid}-v" src="assets/face/{slot["face"]}.mp4" data-start="0" data-duration="{slot["voiceDur"]}" '
                 f'data-track-index="{trk}" data-has-audio="true" data-volume="1" data-hf-media-start-basis="local" playsinline></video>')
    else:
        inner = (f'<div id="{cid}-ph"><div class="h" style="font-size:96px;color:#e8b931">얼굴 영상 자리</div>'
                 f'<div class="hd" style="font-size:40px;margin-top:22px">olds_face_{slot["face"]}.mp4 · 원장님 원음 · {slot["voiceDur"]:.0f}초 가정</div>'
                 f'<div class="b" style="font-size:30px;margin-top:16px;color:rgba(255,255,255,.7)">영상 도착 후 tools/face_prep.py → tools/build.py 로 교체</div></div>')
    return f'        <div id="{cid}-fv">{inner}</div>', FACE_CSS.format(cid=cid)
