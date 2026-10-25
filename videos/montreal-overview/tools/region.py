"""Region scene (03:24-03:45) as a standalone sub-composition: compositions/region.html.

Kept separate on purpose: the director's own A~D map is not available yet.
This version shows ONLY real geography (Natural Earth outline of the Island of Montreal, with a
downtown marker at Ville-Marie's real coordinates) and generic A/B/C/D cards that are NOT placed
on the map. To swap in the director's map later, see README.md -> "지역 장면 교체".
Times inside this file are LOCAL (0 = 03:23.8 of the narration).
"""
import json
import os

from common import icon as I, RED, INK, HI, SUB, CSS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = json.load(open(os.path.join(ROOT, "assets/geo/geo.json")))
T0 = 203.8  # narration time where this scene starts
DX, DY = 60, 160  # map placement
dx, dy = GEO["downtown"]


def build(path):
    cards = "".join(
        f'<div class="card ctr rg-card" id="rg-c{L}" style="left:{1180 + (i % 2) * 330}px;top:{250 + (i // 2) * 250}px;width:290px;height:210px;flex-direction:column">'
        f'<div class="bhs red" style="font-size:110px;line-height:1">{L}</div><div class="body" style="font-size:30px;color:{SUB}">지역</div></div>'
        for i, L in enumerate("ABCD"))
    html = f"""<template id="region-template">
<div data-composition-id="region" data-width="1920" data-height="1080" style="position:absolute;inset:0">
<style>
  [data-composition-id="region"] .rg-abs {{ position: absolute; }}
</style>
<div class="rg-abs" id="rg-k" style="left:110px;top:120px"><div class="kick">몬트리올 섬</div><div class="h3" style="margin-top:6px">부모님 어학원은 <span class="red">다운타운</span>에</div></div>
<div class="rg-abs" id="rg-map" style="left:{DX}px;top:{DY}px;width:1000px;height:760px;transform-origin:{dx}px {dy}px">
 <svg width="1000" height="760" viewBox="0 0 1000 760" style="overflow:visible">
  <path id="rg-laval" d="{GEO['laval']}" fill="#F6E1DA" stroke="#E2BDB4" stroke-width="3"/>
  <path id="rg-island" d="{GEO['island']}" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <circle id="rg-dt" cx="{dx}" cy="{dy}" r="70" fill="{RED}" fill-opacity="0.85"/>
  <circle id="rg-dr" cx="{dx}" cy="{dy}" r="70" fill="none" stroke="{RED}" stroke-width="5"/>
 </svg>
 <div class="rg-abs" id="rg-dl" style="left:{dx + 90}px;top:{dy - 40}px"><span class="chip">다운타운 (Ville-Marie)</span></div>
 {''.join(f'<div class="rg-abs rg-pin" style="left:{dx - 60 + k * 40}px;top:{dy - 110 - (k % 2) * 24}px">{I("school", 54, INK, 5)}</div>' for k in range(3))}
</div>
<div class="rg-abs" id="rg-cards" style="left:0;top:0">{cards}</div>
<div class="rg-abs" id="rg-cap" style="left:1180px;top:770px;width:620px"><div class="bhs" style="font-size:50px">지역마다 <span class="red">특징</span>이 달라요</div><div class="body" style="font-size:32px;color:{SUB}">각 가정의 성향에 맞게 선택</div></div>
<div class="rg-abs" id="rg-cal" style="left:1150px;top:260px;width:700px">
 <div class="card row" style="position:relative;padding:30px 36px;gap:24px;border-color:{RED}">{I('calendar', 110, RED, 4)}<div><div class="bhs" style="font-size:52px">지역 선택은</div><div class="bhs red" style="font-size:60px">출국 전까지 천천히</div></div></div></div>
<div class="rg-abs" id="rg-visa" style="left:1150px;top:560px;width:700px">
 <div class="card row" style="position:relative;padding:30px 36px;gap:24px">{I('doc', 100, INK, 4)}<div><div class="body" style="font-size:32px;color:{SUB}">지역 · 자녀 학교 상세</div><div class="bhs" style="font-size:52px">비자 진행하며 안내</div></div></div></div>
<div class="rg-abs small" style="left:110px;top:240px;font-size:28px">지도: Natural Earth 해안선 개략도</div>
<script>
(function () {{
  const t = gsap.timeline({{ paused: true }});
  const q = (s) => Array.from(document.querySelectorAll(s));
  const isl = document.getElementById("rg-island"); const L = Math.ceil(isl.getTotalLength() * 1.03);
  isl.style.strokeDasharray = L + " " + L;
  t.fromTo("#rg-k", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, 0.1);
  t.fromTo(isl, {{ strokeDashoffset: L }}, {{ strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut" }}, 0.1);
  t.fromTo(isl, {{ fillOpacity: 0 }}, {{ fillOpacity: 1, duration: 0.6 }}, 1.2);
  t.fromTo("#rg-laval", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, 0.6);
  t.fromTo("#rg-dt", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.5, ease: "back.out(2.5)" }}, {1.0});
  t.fromTo("#rg-dr", {{ attr: {{ r: 70 }}, opacity: 1 }}, {{ attr: {{ r: 150 }}, opacity: 0, duration: 1.4, ease: "power2.out", repeat: 3, repeatDelay: 0.3 }}, 1.3);
  t.fromTo("#rg-dl", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "back.out(2)" }}, 1.4);
  t.fromTo(".rg-pin", {{ y: -120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "bounce.out", stagger: 0.2 }}, {206.2 - T0});
  t.to("#rg-map", {{ scale: 1.12, x: 40, y: 50, duration: 2.2, ease: "sine.inOut" }}, {206.5 - T0});
  t.to("#rg-map", {{ scale: 0.92, x: -20, y: 30, duration: 0.9, ease: "power3.inOut" }}, {209.2 - T0});
  q(".rg-card").forEach((c, i) => t.fromTo(c, {{ scale: 2.4, opacity: 0, rotation: (i - 1.5) * 10 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.45, ease: "expo.out" }}, {209.4 - T0} + i * 0.22));
  t.fromTo("#rg-cap", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, {211.6 - T0});
  t.to("#rg-cards, #rg-cap", {{ x: 900, opacity: 0, duration: 0.5, ease: "power2.in" }}, {214.1 - T0});
  t.fromTo("#rg-cal", {{ x: 700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.7, ease: "power4.out" }}, {214.4 - T0});
  t.fromTo("#rg-cal .card", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.25, yoyo: true, repeat: 1 }}, {217.6 - T0});
  t.fromTo("#rg-visa", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, ease: "back.out(1.6)" }}, {220.2 - T0});
  t.to("#rg-map", {{ scale: 1.05, duration: 3.5, ease: "sine.inOut" }}, {220.6 - T0});
  window.__timelines["region"] = t;
}})();
</script>
</div>
</template>
"""
    open(path, "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    build(os.path.join(ROOT, "compositions/region.html"))
