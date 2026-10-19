"""Chapter title card and testimonial clip compositions."""
from common import scene_html

CARD_CSS = """
R #{cid}-num{{left:140px;top:250px;font-size:400px;color:#e8b931}}
R #{cid}-ghost{{left:900px;top:-80px;font-size:900px;color:rgba(255,255,255,.07);font-weight:900;line-height:1}}
R #{cid}-bar{{left:150px;top:690px;width:180px;height:12px;border-radius:6px;background:#c8102e}}
R #{cid}-mas{{left:1500px;top:520px;width:320px;height:340px}}
"""


def card(cid, ch, title, sub, mascot, duration, trk=32):
    body = f"""
          <div class="abs" id="{cid}-ghost" data-layout-allow-overflow>{ch:02d}</div>
          <div class="abs l" id="{cid}-k" style="left:160px;top:210px;font-size:34px;color:rgba(255,255,255,.7)">CHAPTER</div>
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
    if mascot:
        body += f'\n          <div class="abs" id="{cid}-mas"><img src="@B/{mascot}.png" alt="" style="width:100%;height:100%;object-fit:contain" /></div>'
        js += f"tl.fromTo('#{cid}-mas',{{opacity:0,y:70,rotation:-6}},{{opacity:1,y:0,rotation:0,duration:0.55,ease:'back.out(1.8)'}},0.7);\n"
    audio = f'        <audio id="{cid}-sfx" src="assets/sfx/impact.mp3" data-start="0.45" data-duration="1.2" data-track-index="{trk}" data-volume="0.22" data-hf-media-start-basis="local"></audio>'
    return scene_html(cid, duration, CARD_CSS.format(cid=cid), body, js, "", audio)


CLIP_CSS = """
R #{cid}-bgp img{{filter:blur(18px) saturate(.6)}}
R #{cid}-fr{{left:160px;top:40px;width:1600px;height:900px;border-radius:30px;overflow:hidden;background:#0b1630;box-shadow:0 30px 70px rgba(0,0,0,.5)}}
R #{cid}-fr video{{width:100%;height:100%;object-fit:cover;display:block}}
R #{cid}-ph{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg,#1f3a6b,#14254a)}}
R #{cid}-tag{{left:210px;top:740px;padding:14px 30px;border-radius:16px;background:rgba(11,22,48,.86);border-left:8px solid #e8b931;font-weight:800;font-size:34px;white-space:nowrap}}
R #{cid}-nc{{left:0;right:0;top:330px;display:flex;flex-direction:column;align-items:center}}
"""


def clip(cid, slot, info, duration, trk=31):
    tag = info["tag"]
    name = tag.split(" · ")[0]
    if slot["has_video"]:
        inner = (f'<video id="{cid}-v" src="assets/clips/{slot["clip"]}.mp4" data-start="{slot["clipAt"]}" '
                 f'data-duration="{slot["clipDur"]}" data-track-index="{trk}" data-has-audio="true" data-volume="1" data-hf-media-start-basis="local" playsinline></video>')
    else:
        inner = (f'<div id="{cid}-ph"><div class="h" style="font-size:200px;color:#e8b931;line-height:.8">&ldquo;</div>'
                 f'<div class="hd" style="font-size:64px;margin-top:10px">{name} 학생 후기</div>'
                 f'<div class="b" style="font-size:30px;margin-top:24px;color:rgba(255,255,255,.7)">후기 영상 자리 ({slot["clip"]}) · SGA 공식 유튜브 Students&#39; Voice</div></div>')
    body = f"""
          <div class="abs" id="{cid}-fr">{inner}</div>
          <div class="abs" id="{cid}-tag">{tag}</div>
          <div class="abs" id="{cid}-nc"><div class="pill" style="position:relative;font-size:30px">학생 후기 · Students&#39; Voice</div>
            <div class="h" style="font-size:96px;margin-top:30px">{name}</div><div class="hd" style="font-size:44px;color:#e8b931;margin-top:14px">{tag.split(" · ", 1)[1]}</div></div>"""
    bg = f'        <div class="full" id="{cid}-bgp" style="opacity:.3"><img src="@P/campus-13-lobby.jpg" alt="" /></div>'
    at = slot["clipAt"]
    js = f"""
inn('#{cid}-nc',0.0,{{y:20,d:0.35}});
outt('#{cid}-nc',{at - 0.25},{{d:0.25,s:0.9}});
tl.fromTo('#{cid}-fr',{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.45,ease:'power3.out'}},{at - 0.2});
inn('#{cid}-tag',{at + 0.3},{{x:-30,y:0}});
"""
    return scene_html(cid, duration, CLIP_CSS.format(cid=cid), body, js, bg)
