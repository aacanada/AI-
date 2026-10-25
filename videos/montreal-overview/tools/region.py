"""Region scene (03:24-03:45) as a standalone sub-composition: compositions/region.html.

Uses the director's map (plans/montreal-overview/assets/owner/region-map-abcd.png), shown as supplied.
Motion: zoom into the red downtown circle -> pull back -> A/B/C/D badges pop on the blue circles ->
legend lines appear one by one, each blinking its areas -> "pick before departure" / "details during visa" cards.
The legend text is cut from the original and laid back at the same pixels (tools/owner_img.py), so the
finished frame is the original picture. Times inside this file are LOCAL (0 = 03:23.8 of the narration).
"""
import json
import os

from common import icon as I, RED, INK, HI, SUB  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(open(os.path.join(ROOT, "assets/img/owner/rects.json")))["region"]
T0 = 203.8  # narration time where this scene starts
W, H = 1240, 696  # map window (image 868x487)
FIT = (1.4286, 434, 243.5)
DT = (612, 248)  # red downtown circle centre (image px)
BADGE = {"A": (505, 312), "B": (280, 333), "C": (585, 105), "D": (760, 305)}  # blue circle centres (image px)
LEG = [("l1", "AC"), ("l2", "BCD"), ("l3", "AB"), ("l4", "ACD")]
LEG_T = [211.2, 212.9, 214.6, 216.3]


def L(t):
    return round(t - T0, 3)


def build(path):
    legend = "".join(f'<img class="rg-leg" id="rg-{k}" src="assets/img/owner/region-{k}.png" style="left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px" alt="">'
                     for k, (x0, y0, x1, y1) in REG.items())
    legbox = "".join(f'<div class="hl rg-lb" id="rg-b{k}" style="left:{x0 - 3}px;top:{y0}px;width:{x1 - x0 + 6}px;height:{y1 - y0}px;border-width:2px;border-radius:4px"></div>'
                     for k, (x0, y0, x1, y1) in REG.items())
    badges = "".join(f'<div class="bdg" id="rg-{n}" style="left:{x}px;top:{y}px">{n}</div>' for n, (x, y) in BADGE.items())
    js = []
    for (k, areas), t in zip(LEG, LEG_T):
        js.append(f't.fromTo("#rg-{k}", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {L(t)});')
        js.append(f't.fromTo("#rg-b{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {L(t)});')
        js.append(f't.to("#rg-b{k}", {{ opacity: 0, duration: 0.3 }}, {L(t + 1.55)});')
        others = [n for n in "ABCD" if n not in areas]
        if others:
            js.append(f't.to("{", ".join("#rg-" + n for n in others)}", {{ opacity: 0.35, duration: 0.2 }}, {L(t + 0.1)});')
            js.append(f't.to("{", ".join("#rg-" + n for n in others)}", {{ opacity: 1, duration: 0.25 }}, {L(t + 1.55)});')
        js.append(f't.fromTo("{", ".join("#rg-" + n for n in areas)}", {{ scale: 1 }}, {{ scale: 1.45, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 3 }}, {L(t + 0.15)});')
    s, cx, cy = FIT

    def v(s, cx, cy):
        return f"x: {W / 2 - cx * s:.1f}, y: {H / 2 - cy * s:.1f}, scale: {s}"

    html = f"""<template id="region-template">
<div data-composition-id="region" data-width="1920" data-height="1080" style="position:absolute;inset:0">
<div class="win" id="rg-win" style="left:90px;top:110px;width:{W}px;height:{H}px">
 <div class="pic" id="rg-pic" style="width:868px;height:487px">
  <img src="assets/img/owner/region-base.png" style="left:0;top:0;width:868px;height:487px" alt="몬트리올 지역 지도 (A~D)">
  {legend}{legbox}
  <div class="hl" id="rg-dt" style="left:{DT[0] - 46}px;top:{DT[1] - 58}px;width:92px;height:116px;border-radius:50%;border-width:3px"></div>
  <div class="abs" id="rg-dl" style="left:{DT[0] + 44}px;top:{DT[1] - 4}px"><span class="chip" style="font-size:14px;padding:3px 10px">다운타운</span></div>
  <div class="abs" id="rg-sl" style="left:{DT[0] + 40}px;top:{DT[1] - 52}px"><span class="chip d" style="font-size:12px;padding:3px 9px">부모님 어학원</span></div>
  {badges}
 </div></div>
<div class="abs" id="rg-p1" style="left:1380px;top:150px;width:480px">
 <div class="kick">몬트리올 지역</div>
 <div class="h3" style="margin-top:8px"><span class="red">빨간 원</span> = 다운타운</div>
 <div class="body" style="margin-top:16px;font-size:32px">부모님 어학원은 모두 다운타운에</div></div>
<div class="abs" id="rg-p2" style="left:1380px;top:430px;width:480px">
 <div class="h3" style="font-size:54px">A·B·C·D</div><div class="body" style="font-size:36px">지역마다 특징이 달라요</div>
 <div class="small" style="font-size:30px;margin-top:6px">각 가정의 성향에 맞게 선택</div></div>
<div class="abs" id="rg-cal" style="left:1370px;top:300px;width:500px">
 <div class="card row" style="position:relative;padding:26px 28px;gap:20px;border-color:{RED}">{I('calendar', 96, RED, 4)}<div><div class="bhs" style="font-size:44px">지역 선택은</div><div class="bhs red" style="font-size:40px">출국 전까지 천천히</div></div></div></div>
<div class="abs" id="rg-visa" style="left:1370px;top:560px;width:500px">
 <div class="card row" style="position:relative;padding:26px 28px;gap:20px">{I('doc', 90, INK, 4)}<div><div class="body" style="font-size:30px;color:{SUB}">지역 · 자녀 학교 상세</div><div class="bhs" style="font-size:44px">비자 진행하며 안내</div></div></div></div>
<script>
(function () {{
  const t = gsap.timeline({{ paused: true }});
  t.fromTo("#rg-pic", {{ {v(*FIT)} }}, {{ {v(*FIT)}, duration: 0.01 }}, 0);
  t.set(".rg-leg, .rg-lb, .bdg, #rg-dt, #rg-dl, #rg-sl", {{ opacity: 0 }}, 0);
  t.fromTo("#rg-win", {{ scale: 0.86, opacity: 0, rotation: -2 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.6, ease: "back.out(1.5)" }}, 0.05);
  t.to("#rg-pic", {{ {v(3.3, *DT)}, duration: 1.3, ease: "power3.inOut" }}, {L(204.2)});
  t.fromTo("#rg-dt", {{ opacity: 0, scale: 1.6, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {L(204.9)});
  t.fromTo("#rg-dt", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {L(205.5)});
  t.fromTo("#rg-dl", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "back.out(2)" }}, {L(205.0)});
  t.fromTo("#rg-sl", {{ opacity: 0, y: -14 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }}, {L(206.2)});
  t.fromTo("#rg-p1", {{ x: 300, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.6, ease: "power4.out" }}, {L(204.4)});
  t.to("#rg-pic", {{ {v(*FIT)}, duration: 0.9, ease: "power3.inOut" }}, {L(208.5)});
  t.to("#rg-dl, #rg-sl", {{ opacity: 0, duration: 0.3 }}, {L(208.5)});
  ["#rg-A", "#rg-B", "#rg-C", "#rg-D"].forEach((b, i) => t.fromTo(b, {{ opacity: 0, scale: 2.6, rotation: -30 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.4)" }}, {L(209.4)} + i * 0.22));
  t.fromTo("#rg-p2", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {L(209.6)});
  {chr(10).join("  " + j for j in js).strip()}
  t.to("#rg-p1, #rg-p2", {{ x: 400, opacity: 0, duration: 0.45, ease: "power2.in" }}, {L(214.1)});
  t.fromTo("#rg-cal", {{ x: 600, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.7, ease: "power4.out" }}, {L(214.4)});
  t.fromTo("#rg-cal .card", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.25, yoyo: true, repeat: 1 }}, {L(217.6)});
  t.to("#rg-pic", {{ {v(1.47, 434, 250)}, duration: 3.0, ease: "sine.inOut" }}, {L(217.9)});
  t.fromTo("#rg-visa", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, ease: "back.out(1.6)" }}, {L(220.2)});
  t.fromTo(".bdg", {{ scale: 1 }}, {{ scale: 1.18, duration: 0.25, yoyo: true, repeat: 1, stagger: 0.12 }}, {L(222.6)});
  window.__timelines["region"] = t;
}})();
</script>
</div>
</template>
"""
    open(path, "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    build(os.path.join(ROOT, "compositions/region.html"))
