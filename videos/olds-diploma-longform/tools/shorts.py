"""Three 9:16 shorts (one per major) cut from the EP2 long-form. Run from the long-form project root after tools/tts.py:
    python3 -I tools/shorts.py            # builds ../olds-diploma-shorts/<key>/ (index.html + assets)
then render each:  (cd ../olds-diploma-shorts/<key> && npx --yes hyperframes@0.8.174 render -o renders/video.mp4 --fps 30)

Audio per short = new TTS hook line + the long-form scene for that major (cut from the major's name, so "첫 번째는"
drops) + one TTS summary line built only from long-form facts + the owner's CTA line. Voice "일곱번째", same as the long-form.
Layout rules (AA Canada shorts): captions in the top band (y 215), key visuals y 560-1300, bottom 480 px empty,
"full video" pill visible all along, end card for the last 2 s.
"""
import base64
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timing  # noqa: E402
import tts  # noqa: E402
from script import MAJORS, SCENES  # noqa: E402
from templates import icon  # noqa: E402

OUTROOT = os.path.join("..", "olds-diploma-shorts")
AUD = tts.AUD
GAP = 0.22
FACT = ("2년 과정이라 졸업하면 워크퍼밋을 최대 3년까지 받을 수 있어요. 학비는 1년에 약 1만 9천 캐나다 달러예요.")
CTA = "올즈컬리지 상담은 AA Canada, 카카오톡 canlog로 물어봐 주세요."
CTA_SAY = "올즈컬리지 상담은 에이에이 캐나다, 카카오톡 캔로그로 물어봐 주세요."
SHORTS = {
    "techgronomy": dict(major="tech", scene="s04", start="정밀농업 테크고노미", hook="드론과 데이터로 농사를 짓는 전공, 캐나다 알버타에 있어요.",
                        photos=["sf-03-drone-flying", "sf-04-sensor"], chips=["드론·센서 데이터", "4개월 유급 인턴십", "AIA 자격 과정 도전"],
                        cues=["드론과 센서로", "4개월은", "졸업하면 알버타"], cover=["드론과 데이터로", "농사 짓는 전공", "캐나다 2년 디플로마"]),
    "horticulture": dict(major="horti", scene="s05", start="원예 테크놀로지스트", hook="식물 좋아하세요? 급여 받으며 실습하는 캐나다 원예 전공이 있어요.",
                         photos=["campus-05-central-gardens", "sf-13-indoor-ag"], chips=["재배·온실·조경·창업", "캠퍼스가 실습장", "필드스쿨 급여 실습"],
                         cues=["식물 재배", "캠퍼스 자체가", "중간에 필드스쿨이"], cover=["식물 좋아하면", "캐나다 원예 전공", "2년 디플로마"]),
    "agmanagement": dict(major="mgmt", scene="s06", start="농업경영 디플로마", hook="경영이나 영업 경력, 캐나다 농업에서 살릴 수 있어요.",
                         photos=["prog-09-ag-sales", "sf-18-agexpert-farm-mgmt"], chips=["경영+농업 전반", "전공 2가지 선택", "편입 협약(학교 자료)"],
                         cues=["회계, 마케팅", "전공은 두 가지", "학교 자료에 따르면"], cover=["경영·영업 경력", "캐나다 농업에서", "살리는 2년 전공"]),
}
MAXC = 13


def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def chunk(text):
    """Caption lines <= MAXC chars, never running across a sentence end."""
    import re
    lines = []
    for sent in re.split(r"(?<=[.?!])\s+", text.replace("AA Canada", "AA\u00a0Canada").replace("1만 9천", "1만\u00a09천").replace("최대 3년", "최대\u00a03년")):
        cur = ""
        for w in sent.split(" "):
            if cur and len(cur) + 1 + len(w) > MAXC:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            lines.append(cur)
    return [x.replace("\u00a0", " ") for x in lines]


def tts_line(vid, name, text, say_text):
    mp3 = os.path.join(AUD, f"oldsdip_short_{name}.mp3")
    aj = os.path.join("assets", "voice", f"short_{name}.align.json")
    if not (os.path.exists(mp3) and os.path.exists(aj)):
        r = tts.tts(vid, say_text)
        open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
        json.dump(r["alignment"], open(aj, "w", encoding="utf-8"), ensure_ascii=False)
    tts.finish(f"short_{name}", mp3, json.load(open(aj, encoding="utf-8")))
    wav = os.path.join("assets", "voice", f"short_{name}.wav")
    words = json.load(open(os.path.join("assets", "voice", f"short_{name}.words.json"), encoding="utf-8"))
    d = probe(wav)
    return wav, 0.0, d, text, timing.char_times(text, d, words)


def scene_part(sid, start_phrase):
    sc = next(s for s in SCENES if s["id"] == sid)
    text = " ".join(sc["rows"])
    wav = os.path.join("assets", "voice", f"{sid}.wav")
    words = json.load(open(os.path.join("assets", "voice", f"{sid}.words.json"), encoding="utf-8"))
    d = probe(wav)
    ct = timing.char_times(text, d, words)
    k = text.index(start_phrase)
    a = max(0.0, ct[k] - 0.06)
    sub = text[k:]
    return wav, a, d, sub, [round(t - a, 3) for t in ct[k:]]


def build_short(key, cfg, vid):
    m = MAJORS[cfg["major"]]
    out = os.path.join(OUTROOT, key)
    for d in ("assets/photos", "assets/fonts", "assets/vendor", "assets/audio"):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    parts = [tts_line(vid, f"{key}_hook", cfg["hook"], tts.say(cfg["hook"])),
             scene_part(cfg["scene"], cfg["start"]),
             tts_line(vid, "fact", FACT, tts.say(FACT)),
             tts_line(vid, "cta", CTA, CTA_SAY)]
    # narration: concat with short gaps
    tmp = os.path.join(out, "assets", "audio")
    seg_files, t, segs = [], 0.0, []
    for i, (wav, a, d, text, ct) in enumerate(parts):
        f = os.path.join(tmp, f"seg{i}.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-to", f"{d:.3f}", "-i", wav, "-ar", "48000", "-ac", "1", f], check=True)
        dd = probe(f)
        segs.append(dict(t0=round(t, 3), dur=dd, text=text, ct=[round(t + x, 3) for x in ct]))
        seg_files.append(f)
        t += dd + GAP
    lst = os.path.join(tmp, "list.txt")
    gap = os.path.join(tmp, "gap.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(GAP), gap], check=True)
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\nfile '{os.path.abspath(gap)}'\n" for f in seg_files))
    nar = os.path.join(tmp, "narration.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", nar], check=True)
    for f in seg_files + [gap, lst]:
        os.remove(f)
    voice_end = t - GAP
    END = 2.2
    total = round(voice_end + 0.6 + END, 3)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join("assets", "music", "bgm-a.mp3"), "-t", str(total + 1),
                    "-af", f"afade=t=in:d=1,afade=t=out:st={total - 2:.2f}:d=2", "-b:a", "128k", os.path.join(tmp, "bgm.mp3")], check=True)
    for p in cfg["photos"]:
        shutil.copy(os.path.join("assets", "photos", p + ".jpg"), os.path.join(out, "assets", "photos"))
    for f in ("Pretendard-Bold.woff2", "Pretendard-ExtraBold.woff2", "Pretendard-Black.woff2"):
        shutil.copy(os.path.join("assets", "fonts", f), os.path.join(out, "assets", "fonts"))
    shutil.copy(os.path.join("assets", "vendor", "gsap.min.js"), os.path.join(out, "assets", "vendor"))
    for f in ("package.json", "hyperframes.json", ".gitignore"):
        shutil.copy(f, os.path.join(out, f))

    # captions
    caps = []
    for sg in segs:
        pos = 0
        for ln in chunk(sg["text"]):
            k = sg["text"].find(ln, pos)
            pos = k + len(ln)
            caps.append([sg["ct"][k], sg["ct"][min(pos, len(sg["ct"]) - 1)] + 0.25, ln])
    for i in range(len(caps) - 1):
        caps[i][1] = min(caps[i][1], caps[i + 1][0] - 0.02)
    keys = cfg["chips"] + ["최대 3년", "1만 9천", "AA Canada", "canlog", m["short"]]

    def hl(s):
        for kk in ("최대 3년", "1만 9천", "AA Canada", "canlog", m["short"], "드론", "데이터", "급여", "원예", "경영", "영업"):
            if kk in s:
                return s.replace(kk, f"<b>{kk}</b>", 1)
        return s
    cap_html = "\n".join(f'      <div id="cap-{i:02d}" class="clip cap" data-start="{a:.3f}" data-duration="{max(0.2, b - a):.3f}" data-track-index="20"><span>{hl(s)}</span></div>'
                         for i, (a, b, s) in enumerate(caps))

    def T(seg, phrase):
        sg = segs[seg]
        return sg["ct"][sg["text"].index(phrase)]
    s1 = segs[1]
    cue_t = [T(1, c) for c in cfg["cues"]]
    fact_t, cta_t = segs[2]["t0"], segs[3]["t0"]
    chips = "".join(f'<div class="kc" id="k{i}" style="border-color:{m["color"]}">{c}</div>' for i, c in enumerate(cfg["chips"]))
    photos = "".join(f'<div class="ph" id="p{i}"><img src="assets/photos/{p}.jpg" alt=""/></div>' for i, p in enumerate(cfg["photos"]))
    fd = round(cta_t - fact_t, 3)
    html = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face{{font-family:Pretendard;font-weight:700;src:url(assets/fonts/Pretendard-Bold.woff2) format("woff2")}}
      @font-face{{font-family:Pretendard;font-weight:800;src:url(assets/fonts/Pretendard-ExtraBold.woff2) format("woff2")}}
      @font-face{{font-family:Pretendard;font-weight:900;src:url(assets/fonts/Pretendard-Black.woff2) format("woff2")}}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0e2a22; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; color:#fff; font-family:Pretendard,sans-serif;
        background:#0e2a22; background-image:repeating-linear-gradient(118deg,{m["color"]}1f 0 3px,transparent 3px 52px); }}
      .abs {{ position:absolute; }}
      .brand {{ z-index:80; left:60px; top:132px; font-weight:800; font-size:30px; letter-spacing:.06em; color:rgba(255,255,255,.85); }}
      .cap {{ position:absolute; left:0; right:0; top:215px; height:150px; z-index:50; display:flex; justify-content:center; align-items:center; }}
      .cap span {{ display:inline-block; background:rgba(4,20,15,.82); padding:16px 34px; border-radius:18px; font-weight:900; font-size:74px; line-height:1.15; white-space:nowrap; }}
      .cap b {{ color:#ffd23f; font-weight:900; }}
      #plate {{ left:60px; top:450px; width:960px; display:flex; align-items:center; gap:28px; font-weight:900; font-size:70px; line-height:1.05; color:{m["color"]}; }}
      #plate small {{ display:block; font-size:44px; color:#f3ecdc; margin-top:12px; }}
      .ph {{ position:absolute; width:900px; height:410px; left:90px; overflow:hidden; border-radius:8px 34px 8px 34px; border:6px solid #f3ecdc; box-shadow:0 24px 50px rgba(0,0,0,.4); }}
      .ph img {{ width:100%; height:100%; object-fit:cover; display:block; }}
      #p0 {{ top:740px; }} #p1 {{ top:740px; }}
      .kc {{ position:relative; display:inline-block; margin:0 16px 18px 0; padding:16px 30px; border-radius:99px; border:3px solid; background:rgba(4,20,15,.75); font-weight:900; font-size:38px; white-space:nowrap; }}
      #chips {{ left:90px; top:1175px; width:920px; }}
      .fc {{ position:absolute; left:90px; width:900px; padding:40px 48px; border-radius:8px 34px 8px 34px; background:#f3ecdc; color:#0e2a22; }}
      .fc .l {{ font-weight:800; font-size:40px; }}
      .fc .v {{ font-weight:900; font-size:96px; color:{m["ink"]}; line-height:1.1; }}
      #src {{ left:90px; top:1300px; width:900px; font-weight:700; font-size:28px; color:rgba(255,255,255,.7); }}
      #cta {{ position:absolute; inset:0; background:#0b231c; }}
      #cta .aa {{ position:absolute; left:0; right:0; top:620px; text-align:center; font-weight:900; font-size:130px; letter-spacing:.02em; }}
      #cta .sub {{ position:absolute; left:0; right:0; top:800px; text-align:center; font-weight:800; font-size:48px; color:#f3ecdc; }}
      #cta .btn {{ position:absolute; left:140px; top:930px; width:800px; height:130px; border-radius:70px; background:#c8102e; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:56px; }}
      #pill {{ left:120px; top:1352px; width:840px; height:84px; border-radius:50px; background:#c8102e; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:38px; z-index:60; }}
      #endc {{ position:absolute; inset:0; background:#0b231c; z-index:70; }}
      #endc div {{ position:absolute; left:0; right:0; top:820px; text-align:center; font-weight:900; font-size:72px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-duration="{total}">
      <div class="abs brand">AA CANADA</div>
      <div class="abs" id="plate">{icon(m["icon"], m["color"], 150)}<div>{m["name"]}<small>2년 디플로마 · 알버타 Olds College</small></div></div>
      {photos}
      <div class="abs" id="chips">{chips}</div>
      <div class="fc" id="f0" style="top:640px"><div class="l">2년 과정 졸업 후 워크퍼밋</div><div class="v">최대 3년</div></div>
      <div class="fc" id="f1" style="top:960px"><div class="l">1년 학비 + 필수비용 (유학생)</div><div class="v">약 CAD 19,000</div></div>
      <div class="abs" id="src">IRCC PGWP 기준 · Olds College 2026-27 학비표(2026-08-10판), 책값 별도</div>
      <div id="cta"><div class="aa">AA CANADA</div><div class="sub">올즈컬리지 상담</div><div class="btn">카카오톡 canlog</div></div>
      <div class="abs" id="pill">▶ 전체 영상 4분 정리 · 관련 동영상에서</div>
      <div id="endc"><div>전체 영상은 관련 동영상에서 ▶</div></div>
      <audio id="narration" src="assets/audio/narration.wav" data-start="0.3" data-duration="{probe(nar):.3f}" data-track-index="10" data-volume="1"></audio>
      <audio id="bgm" src="assets/audio/bgm.mp3" data-start="0" data-duration="{total}" data-track-index="11" data-volume="0.07"></audio>
{cap_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const O = 0.3;
      tl.set(['#p0','#p1','#chips .kc','#f0','#f1','#src','#cta','#endc'], {{ opacity: 0 }}, 0);
      tl.fromTo('#plate', {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:'power3.out' }}, 0.15);
      tl.fromTo('#plate svg', {{ rotation:-25, scale:0.5 }}, {{ rotation:0, scale:1, duration:0.6, ease:'back.out(1.8)' }}, 0.2);
      tl.fromTo('#p0', {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:'power3.out' }}, O + {s1["t0"]});
      tl.fromTo('#p0 img', {{ scale:1 }}, {{ scale:1.12, duration:{cue_t[1] - s1["t0"]:.2f}, ease:'none' }}, O + {s1["t0"]});
      tl.to('#p0', {{ opacity:0, duration:0.3 }}, O + {cue_t[1] - 0.3:.2f});
      tl.fromTo('#p1', {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:'power3.out' }}, O + {cue_t[1]:.2f});
      tl.fromTo('#p1 img', {{ scale:1 }}, {{ scale:1.12, duration:{fact_t - cue_t[1]:.2f}, ease:'none' }}, O + {cue_t[1]:.2f});
{chr(10).join(f"      tl.fromTo('#k{i}', {{ opacity:0, scale:0.4 }}, {{ opacity:1, scale:1, duration:0.4, ease:'back.out(2.2)' }}, O + {c:.2f});" for i, c in enumerate(cue_t))}
      tl.to(['#p1','#chips','#plate'], {{ opacity:0, duration:0.3 }}, O + {fact_t - 0.3:.2f});
      tl.fromTo('#f0', {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:0.5, ease:'power3.out' }}, O + {fact_t:.2f});
      tl.fromTo('#f1', {{ opacity:0, x:60 }}, {{ opacity:1, x:0, duration:0.5, ease:'power3.out' }}, O + {T(2, "학비는"):.2f});
      tl.fromTo('#src', {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, O + {T(2, "학비는") + 0.4:.2f});
      tl.to(['#f0','#f1','#src'], {{ opacity:0, duration:0.2 }}, O + {cta_t - 0.2:.2f});
      tl.fromTo('#cta', {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, O + {cta_t - 0.2:.2f});
      tl.fromTo('#cta .btn', {{ scale:1.5, opacity:0 }}, {{ scale:1, opacity:1, duration:0.4, ease:'power4.in' }}, O + {T(3, "카카오톡"):.2f});
      tl.fromTo('#pill', {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4 }}, 0.6);
{chr(10).join(f"      tl.to('#pill', {{ scale:1.05, duration:0.3, yoyo:true, repeat:1 }}, {x:.1f});" for x in [k * 6.0 for k in range(1, int((total - END) // 6))])}
      tl.to('#pill', {{ opacity:0, duration:0.2 }}, {total - END:.2f});
      tl.to('#cta', {{ opacity:0, duration:0.2 }}, {total - END:.2f});
      tl.fromTo('#endc', {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {total - END:.2f});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
"""
    # captions are timed against the narration, which starts at 0.3 s
    import re
    html = re.sub(r'(<div id="cap-\d+" class="clip cap" data-start=")([\d.]+)"', lambda mm: f'{mm.group(1)}{float(mm.group(2)) + 0.3:.3f}"', html)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    # cover (1080x1920): title + brand only
    cover = f"""<!doctype html><html lang="ko"><head><meta charset="UTF-8"/><title>{key} cover</title><style>
@font-face{{font-family:Pretendard;font-weight:800;src:url(../assets/fonts/Pretendard-ExtraBold.woff2) format("woff2")}}
@font-face{{font-family:Pretendard;font-weight:900;src:url(../assets/fonts/Pretendard-Black.woff2) format("woff2")}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#0e2a22;font-family:Pretendard,sans-serif;color:#fff}}
.ph{{position:absolute;left:0;top:0;width:1080px;height:1920px}}.ph img{{width:100%;height:100%;object-fit:cover;filter:brightness(.45)}}
.fur{{position:absolute;inset:0;background:repeating-linear-gradient(118deg,{m["color"]}26 0 3px,transparent 3px 52px)}}
.b{{position:absolute;left:70px;top:150px;font-weight:800;font-size:34px;letter-spacing:.06em}}
.ic{{position:absolute;left:70px;top:330px}}
.t{{position:absolute;left:66px;top:560px;font-weight:900;font-size:124px;line-height:1.14;letter-spacing:-.04em}}
.t span{{display:block}}.t span:last-child{{color:{m["color"]}}}
.s{{position:absolute;left:70px;top:1060px;font-weight:800;font-size:48px;color:#f3ecdc}}
</style></head><body><div class="ph"><img src="../assets/photos/{cfg["photos"][0]}.jpg" alt=""/></div><div class="fur"></div>
<div class="b">AA CANADA</div><div class="ic">{icon(m["icon"], m["color"], 180)}</div>
<div class="t">{''.join(f'<span>{x}</span>' for x in cfg["cover"])}</div><div class="s">알버타 Olds College · 워크퍼밋 최대 3년</div></body></html>"""
    os.makedirs(os.path.join(out, "thumbnail"), exist_ok=True)
    open(os.path.join(out, "thumbnail", "cover.html"), "w", encoding="utf-8").write(cover)
    print(f"{key}: {total:.1f}s, voice {voice_end:.1f}s, captions {len(caps)}")
    return total


if __name__ == "__main__":
    vid, name = tts.voice_id()
    for k, c in SHORTS.items():
        if len(sys.argv) > 1 and k not in sys.argv[1:]:
            continue
        build_short(k, c, vid)
