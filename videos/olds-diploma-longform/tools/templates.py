"""Scene title card + major icons (shared with the shorts and thumbnail)."""
from common import scene_html

ICONS = {
    "drone": '<svg viewBox="0 0 120 120" width="{s}" height="{s}"><g fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round">'
             '<path d="M36 36 L84 84 M84 36 L36 84"/><circle cx="30" cy="30" r="16"/><circle cx="90" cy="30" r="16"/><circle cx="30" cy="90" r="16"/><circle cx="90" cy="90" r="16"/></g>'
             '<rect x="46" y="46" width="28" height="28" rx="6" fill="{c}"/></svg>',
    "leaf": '<svg viewBox="0 0 120 120" width="{s}" height="{s}"><path d="M24 98 C20 50 50 18 102 16 C104 66 74 100 24 98 Z" fill="{c}"/>'
            '<path d="M24 98 C46 72 66 52 88 32" fill="none" stroke="#0e2a22" stroke-width="6" stroke-linecap="round"/></svg>',
    "chart": '<svg viewBox="0 0 120 120" width="{s}" height="{s}"><g fill="{c}"><rect x="16" y="64" width="22" height="40" rx="4"/>'
             '<rect x="49" y="44" width="22" height="60" rx="4"/><rect x="82" y="20" width="22" height="84" rx="4"/></g></svg>',
}


def icon(name, color, size=96):
    return ICONS[name].format(c=color, s=size)


CARD_CSS = """
R #{cid}-num{{left:150px;top:300px;font-size:300px;color:{color}}}
R #{cid}-bar{{left:160px;top:660px;width:220px;height:14px;border-radius:7px;background:{color}}}
R #{cid}-ic{{left:1560px;top:190px;width:200px;height:200px}}
"""


def card(cid, ch, title, sub, duration, trk=32, color="#e8b931", icon_name=None):
    body = f"""
          <div class="abs num" id="{cid}-num">{ch:02d}</div>
          <div class="abs h" id="{cid}-t" style="left:720px;top:380px;font-size:112px;white-space:nowrap">{title}</div>
          <div class="abs hd" id="{cid}-s" style="left:726px;top:530px;font-size:48px;color:{color};white-space:nowrap">{sub}</div>
          <div class="abs" id="{cid}-bar"></div>"""
    js = f"""
slam('#{cid}-num',0.1,{{d:0.38}});
mask('#{cid}-t',0.45,0.6,'l');inn('#{cid}-s',0.8,{{y:16,d:0.5}});grow('#{cid}-bar',0.6,0.6);
"""
    if icon_name:
        body += f'\n          <div class="abs" id="{cid}-ic">{icon(icon_name, color, 200)}</div>'
        js += f"tl.fromTo('#{cid}-ic',{{opacity:0,rotation:-20,scale:0.5}},{{opacity:1,rotation:0,scale:1,duration:0.6,ease:'back.out(1.8)'}},0.5);\n"
    audio = f'        <audio id="{cid}-sfx" src="assets/sfx/impact.mp3" data-start="0.45" data-duration="1.2" data-track-index="{trk}" data-volume="0.22" data-hf-media-start-basis="local"></audio>'
    return scene_html(cid, duration, CARD_CSS.format(cid=cid, color=color), body, js, "", audio)
