"""Generate index.html (+ compositions/region.html, subset fonts) for the Montreal overview video.

Run from the project root:  python3 -I tools/build.py
Inputs:  ../../plans/montreal-overview/TRANSCRIPT_clean.json (word timings of mtl_clean.flac)
         assets/audio/narration.m4a (mtl_clean.flac, loudnorm -16 LUFS + light denoise)
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import CSS, JS_HELPERS, leaf  # noqa: E402
import scenes_b  # noqa: E402,F401  (registers scenes 15-27 after 01-14)
from scenes_a import S  # noqa: E402
import region  # noqa: E402

ROOT = os.path.dirname(HERE)
PLAN = os.path.join(ROOT, "..", "..", "plans", "montreal-overview")
OFF = 0.5  # lead-in before the narration starts
END_AUDIO = 304.0  # narration ends 297.6; end card holds to here
TOTAL = round(END_AUDIO + OFF, 2)
A = lambda t: round(t + OFF, 3)  # noqa: E731

tr = json.load(open(os.path.join(PLAN, "TRANSCRIPT_clean.json"), encoding="utf-8"))
SEG = tr["segments"]

# ------------------------------------------------------------------ captions (SCRIPT.txt wording)
CAPS = [
    (0, 0, "안녕하세요, {AA Canada}의 심동섭 실장입니다. 몬트리올에 대한 전반적인 내용을 요약해서 설명해 드릴게요."),
    (1, 1, "몬트리올은 아래와 같은 {장점}이 있습니다. 사설어학원 또는 사립컬리지."),
    (2, 2, "몬트리올에는 부모님의 사설어학원 또는 사립컬리지를 통해 동반자녀가 모두 {공립학교 무상교육}을 받을 수 있어서,"),
    (3, 3, "부모님의 {학비가 저렴}하고, 학업 부담이 너무 높지 않고, 수업 스케줄이 자녀의 {등하교를 케어}하기에 유리한 장점이 있어요."),
    (4, 4, "몬트리올은 캐나다에서 {두 번째로 큰 대도시}입니다."),
    (5, 6, "여기서부터 비롯되는 장점이 많은데요, 자녀 학교의 {교육 수준}이 높고, {생활 편의성}이 높고, {문화 환경}이 아주 우수합니다."),
    (7, 7, "몬트리올은 캐나다 두 번째 대도시이지만, 한국 사람들이 많이 가는 밴쿠버나 토론토에 비해서 아파트 렌트비 등 생활비가 {중소도시 수준}으로 저렴합니다."),
    (8, 10, "자녀를 동반해서 {자녀무상교육} 플랜으로 갈 수 있는 캐나다 도시 중에서 몬트리올은 압도적으로 {가장 저렴}하지만, 자녀 교육이나 보고 듣는 경험의 측면에서는 훌륭하기 때문에 인기가 많이 있어요."),
    (11, 13, "몬트리올은 캐나다에서 두 번째로 큰 대도시입니다. 그래서 캐나다 내에서 {교육 환경}, {문화 환경}, {생활 편의성} 등에 있어서 최고의 조건을 갖추고 있습니다."),
    (14, 14, "{2026년 2분기} 캐나다 통계청 자료입니다."),
    (15, 15, "밴쿠버와 토론토처럼 대도시는 항상 집값이 비쌉니다. 하지만 몬트리올은 캐나다 두 번째 대도시임에도 불구하고 렌트비는 {중소도시 수준}입니다."),
    (16, 16, "우리나라에서 국영수가 중요하듯 캐나다에서도 {랭귀지}와 {수학}이 가장 중요합니다."),
    (17, 17, "위 표에서 보듯이 몬트리올 학생들의 {수학 점수}는 압도적으로 높습니다."),
    (18, 18, "그리고 몬트리올 아이들은 {영어와 불어}를 모국어 수준으로 둘 다 자연스럽게 구사하는 아이들이 정말 많습니다."),
    (19, 19, "그리고 퀘벡주는 {교육에 대한 투자}를 아주 많이 합니다."),
    (20, 21, "스쿨버스는 모두 {전기버스}로 바뀌었고, 모든 초등학교에 {3D 프린터}가 있고, 교실에는 {스마트보드}가 있습니다."),
    (22, 22, "결과적으로 몬트리올의 학업 환경은 {캐나다 최고 수준}입니다."),
    (23, 23, "퀘벡 전 지역에 {영어교육청}과 {불어교육청}이 중첩되어 있고,"),
    (24, 25, "부모가 어학연수로 가는 경우 영어교육청은 {최대 3년}까지 무상교육을 하고, 이후에 자녀는 불어교육청으로 옮겨야 합니다."),
    (26, 26, "불어교육청은 영어교육청과 달리 불어 능력이 부족한 아이들을 데리고 따로 {웰컴클래스}를 운영합니다."),
    (27, 27, "이 웰컴클래스는 레귤러 클래스와 완전히 별도로 구성되어 있으며, 수학과 약간의 예체능 이외에는 {불어 어학 수업} 위주로만 수업을 합니다."),
    (28, 28, "완전 {기초 레벨}부터 가르쳐 주고, 일정한 레벨에 도달하면 {정규 수업반}으로 넘어가게 됩니다."),
    (29, 29, "웰컴클래스에서 아이들은 불어가 부족하기 때문에 {영어로 많이 소통}을 하게 되고, 자연스럽게 영어가 늘게 됩니다."),
    (30, 30, "수업은 불어 어학을 배우게 되기 때문에 아이들이 {스트레스 없이} 불어를 배울 수 있으며, 자연스럽게 {영어 불어를 함께} 하는 아이로 자라게 됩니다."),
    (31, 31, "불어교육청 산하의 학교들은 영어 수업 비중이 학교와 시기에 따라 {40% 수준}까지 있습니다."),
    (32, 33, "{영어중심학교}의 수업 시간표입니다. {노란색}이 영어이고, {빨간색}이 불어입니다."),
    (34, 34, "{주 4회} 불어 어학 수업이 있고, 예체능 과목 중 하나를 학기마다 돌아가면서 불어로 수업합니다."),
    (35, 35, "하지만 불어 시간에도 친구들끼리는 모두 {영어로 소통}을 합니다."),
    (36, 36, "빨간색이 {다운타운}이고, 부모님의 어학원들은 모두 다운타운에 위치하고 있습니다."),
    (37, 38, "A, B, C, D 각각 특징이 있고, 각 가정의 성향에 따라서 선택을 하면 되고, 지역 선정은 바로 하실 필요는 없고, {출국하실 때까지} 고민하실 수 있는 문제입니다."),
    (39, 39, "지역이나 자녀 학교에 대한 자세한 내용은 {비자를 진행하면서} 안내 드리도록 하겠습니다."),
    (40, 41, "캐나다 {핼리팩스}에서 고등학교를 졸업하고, {몬트리올}에서 대학과 직장생활을 한 제 배우자 엘리와, 다른 나라 안 하고"),
    (42, 43, "오로지 캐나다 유학 업무만 {20년 이상} 경력이 있는 저희 부부가 고민 없이 선택한 도시가 몬트리올이고, 아직까지 높은 만족도를 유지하면서 지내고 있습니다."),
    (44, 44, "유학업계에서 압도적으로 많은 숫자를 몬트리올로 보내고 있습니다."),
    (45, 46, "몬트리올에 상주하면서 {한국-몬트리올 직영} 시스템을 갖추고 있는 유학원은 저희밖에 없고, 케이스 경험도 정보도 저희가 가장 많습니다."),
    (47, 47, "{입학 수속}을 하면서 학비 납부를 하고요,"),
    (48, 49, "그리고 {입학허가서}가 나오면 퀘벡 주정부의 유학허가인 {CAQ}를 신청해서 승인을 받습니다."),
    (50, 51, "그 이후에 {학생비자}를 신청해서 승인을 받고, 비자 승인 이후에 본격적으로 {출국 준비}를 하게 됩니다."),
    (52, 53, "전체적인 진행 기간은 프로그램마다 달라질 수 있고, 심사 기간도 늘어났다 줄어들었다 합니다."),
    (54, 55, "몬트리올에서의 {부모님 프로그램 정보}에 대해서는 별도로 안내를 드리도록 하겠습니다."),
]
MAXC = 54  # chars per caption card (2 lines at 42px within 1480px)


def plain(s):
    return s.replace("{", "").replace("}", "")


def split_chunks(text):
    """Balanced split into n chunks of <= MAXC chars, preferring breaks after , or ."""
    import math
    words = text.split(" ")
    n = max(1, math.ceil(len(plain(text)) / MAXC))
    while True:
        out, cur = [], []
        target = len(plain(text)) / n
        for w in words:
            cur.append(w)
            L = len(plain(" ".join(cur)))
            punct = w[-1] in ",." and L >= target * 0.6
            if len(out) < n - 1 and (L >= target or punct and L >= target * 0.75):
                out.append(cur)
                cur = []
        if cur:
            out.append(cur)
        if all(len(plain(" ".join(c))) <= MAXC for c in out):
            break
        n += 1
    res = []
    for c in out:
        s = " ".join(c)
        if s.count("{") > s.count("}"):
            s += "}"
        if s.count("}") > s.count("{"):
            s = "{" + s
        res.append(s)
    return res


def caption_items():
    items = []
    for a, b, text in CAPS:
        words = [w for s in SEG[a:b + 1] for w in s["words"]]
        wl = [len(w[2]) for w in words]
        tot_w = sum(wl)
        chunks = split_chunks(text)
        tot_c = sum(len(plain(c).replace(" ", "")) for c in chunks)
        acc = 0
        starts = []
        for c in chunks:
            f = acc / tot_c
            # word whose cumulative char fraction reaches f
            cum, idx = 0, 0
            for i, n in enumerate(wl):
                if cum / tot_w >= f - 1e-6:
                    idx = i
                    break
                cum += n
                idx = i + 1
            idx = min(idx, len(words) - 1)
            starts.append(words[idx][0] if starts or True else 0)
            acc += len(plain(c).replace(" ", ""))
        starts[0] = SEG[a]["start"]
        end = SEG[b]["end"]
        for i, c in enumerate(chunks):
            s = starts[i]
            e = starts[i + 1] if i + 1 < len(chunks) else end + 0.35
            items.append([s, e, c])
    for i in range(len(items) - 1):
        if items[i][1] > items[i + 1][0] - 0.02:
            items[i][1] = items[i + 1][0] - 0.02
        if items[i + 1][0] - items[i][1] < 0.6:  # bridge short gaps so captions don't blink
            items[i][1] = items[i + 1][0] - 0.02
    return items


def cap_html(c):
    return re.sub(r"\{([^}]*)\}", r"<b>\1</b>", c)


# ------------------------------------------------------------------ transitions
SHADERS = ["domain-warp", "whip-pan", "cross-warp-morph", "sdf-iris", "whip-pan", "cross-warp-morph", "domain-warp",
           "cinematic-zoom", "sdf-iris", "whip-pan", "cross-warp-morph", "ripple-waves", "flash-through-white",
           "domain-warp", "sdf-iris", "cross-warp-morph", "whip-pan", "cross-warp-morph", "ripple-waves",
           "cross-warp-morph", "sdf-iris", "cinematic-zoom", "domain-warp", "cross-warp-morph", "sdf-iris", "cross-warp-morph"]
TD = 0.7


def main():
    assert len(SHADERS) == len(S) - 1, (len(SHADERS), len(S))
    region.build(os.path.join(ROOT, "compositions", "region.html"))
    scenes_html, scene_js, transitions = [], [], []
    for i, sc in enumerate(S):
        t0, t1 = sc["t0"], sc["t1"]
        gx, gy = sc["glow"]
        body = sc["html"]
        if body == "__REGION_HOST__":
            body = (f'<div id="rg-host" data-composition-id="region" data-composition-src="compositions/region.html" '
                    f'data-start="{A(t0)}" data-duration="{round(t1 - t0, 3)}" data-track-index="2" data-width="1920" data-height="1080" '
                    f'style="position:absolute;inset:0"></div>')
        bg = (f'<div class="bgl" id="{sc["id"]}-bg"><svg class="dots" width="2040" height="1200" aria-hidden="true">'
              f'<defs><pattern id="{sc["id"]}-dp" width="46" height="46" patternUnits="userSpaceOnUse"><circle cx="23" cy="23" r="2.6" fill="#EBD5CB"/></pattern></defs>'
              f'<rect width="2040" height="1200" fill="url(#{sc["id"]}-dp)"/></svg>'
              f'<div class="glow" style="left:{gx - 450}px;top:{gy - 450}px"></div>'
              f'<div class="ghost" aria-hidden="true" data-layout-ignore style="left:-40px;top:640px">{sc["ghost"]}</div>'
              f'{leaf(360, "#F2D2C9", 3, cls="bgleaf", style=f"left:{1540 if i % 2 else 1500}px;top:{-90 if i % 2 else 620}px")}</div>')
        scenes_html.append(f'<div id="{sc["id"]}" class="scene">{bg}<div class="stage">{body}</div></div>')
        d = round(t1 - t0 + 1.2, 3)
        sid = sc["id"]
        scene_js.append(
            f'// ---- {sid} ({t0}-{t1})\n'
            f'tl.fromTo("#{sid} .ghost", {{ x: 0 }}, {{ x: -260, duration: {d}, ease: "none" }}, A({t0 - 0.6}));\n'
            f'tl.fromTo("#{sid} .glow", {{ scale: 0.85 }}, {{ scale: 1.15, duration: {d}, ease: "sine.inOut" }}, A({t0 - 0.6}));\n'
            f'tl.fromTo("#{sid} .bgleaf", {{ rotation: -8 }}, {{ rotation: 14, duration: {d}, ease: "sine.inOut" }}, A({t0 - 0.6}));\n'
            f'tl.fromTo("#{sid} .dots", {{ y: 0 }}, {{ y: -46, duration: {d}, ease: "none" }}, A({t0 - 0.6}));\n'
            + "{\n" + sc["js"] + "}\n")
        if i < len(S) - 1:
            transitions.append({"time": round(A(t1) - TD / 2, 3), "shader": SHADERS[i], "duration": TD})

    # chapter pills
    chaps, cur = [], None
    for sc in S:
        if sc["chap"] != (cur[0] if cur else None):
            if cur:
                chaps.append(cur)
            cur = [sc["chap"], sc["t0"], sc["t1"]]
        else:
            cur[2] = sc["t1"]
    chaps.append(cur)
    chap_html, chap_js = [], []
    for k, (name, a, b) in enumerate(chaps):
        if not name:
            continue
        chap_html.append(f'<div id="chap-{k}" class="clip chap" data-start="{A(a)}" data-duration="{round(b - a, 3)}" data-track-index="5"><span id="chapi-{k}"><i></i>{name}</span></div>')
        chap_js.append(f'tl.fromTo("#chapi-{k}", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, A({a + 0.15}));')

    caps = caption_items()
    cap_el = "\n".join(
        f'<div id="cap-{i:03d}" class="clip cap" data-start="{A(s)}" data-duration="{round(e - s, 3)}" data-track-index="20"><span class="t">{cap_html(c)}</span></div>'
        for i, (s, e, c) in enumerate(caps))

    # BGM: level ~22 dB under the narration (narration -16 LUFS); a little louder on the end card
    def dur(p):
        return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

    a_len = dur(os.path.join(ROOT, "assets/music/bgm-a.mp3"))
    LV, LE = BGM_GAIN, BGM_GAIN * 2.2
    ad = round(min(a_len, TOTAL), 2)
    b_start = round(ad - 4, 2)
    bd = round(TOTAL - b_start, 2)
    end_t = A(297.8)
    auto_a = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 1.5, "v": LV}, {"t": round(ad - 4, 2), "v": LV}, {"t": ad, "v": 0}]}]}
    auto_b = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 4, "v": LV}, {"t": round(end_t - b_start, 2), "v": LV},
                                                                          {"t": round(end_t - b_start + 1.2, 2), "v": LE}, {"t": round(bd - 2.5, 2), "v": LE}, {"t": bd, "v": 0}]}]}
    audio = (f'<audio id="vo" src="assets/audio/narration.m4a" data-start="{OFF}" data-duration="298.5" data-track-index="10" data-volume="1"></audio>\n'
             f'<audio id="bgm-a" src="assets/music/bgm-a.mp3" data-start="0" data-duration="{ad}" data-track-index="11" data-volume="1" data-automation=\'{json.dumps(auto_a)}\'></audio>\n'
             f'<audio id="bgm-b" src="assets/music/bgm-b.mp3" data-start="{b_start}" data-duration="{bd}" data-track-index="12" data-volume="1" data-automation=\'{json.dumps(auto_b)}\'></audio>')

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>몬트리올 개요 상담 영상 · AA Canada</title>
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/vendor/shader-transitions.global.js"></script>
<style>
@font-face {{ font-family: "Black Han Sans"; src: url("assets/fonts/BlackHanSans.woff2") format("woff2"); font-weight: 400; font-display: block; }}
@font-face {{ font-family: "Noto Sans KR"; src: url("assets/fonts/NotoSansKR-500.woff2") format("woff2"); font-weight: 500; font-display: block; }}
@font-face {{ font-family: "Noto Sans KR"; src: url("assets/fonts/NotoSansKR-700.woff2") format("woff2"); font-weight: 700; font-display: block; }}
@font-face {{ font-family: "Noto Sans KR"; src: url("assets/fonts/NotoSansKR-900.woff2") format("woff2"); font-weight: 900; font-display: block; }}
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
<div class="basefill"></div>
{chr(10).join(scenes_html)}
<div id="progress" class="clip progress" data-start="0" data-duration="{TOTAL}" data-track-index="4"></div>
{chr(10).join(chap_html)}
<img id="logo" class="clip logo" src="assets/img/logo.png" alt="AA Canada" data-start="{A(7.5)}" data-duration="{round(A(298.0) - A(7.5), 3)}" data-track-index="6">
{cap_el}
{audio}
</div>
<script>
{JS_HELPERS.replace("__OFF__", str(OFF))}
const tl = HyperShader.init({{
  bgColor: "#FFF8F2",
  accentColor: "#C8102E",
  compositionId: "main",
  scenes: {json.dumps([s["id"] for s in S])},
  transitions: {json.dumps(transitions)},
}});
window.__timelines["main"] = tl;
tl.fromTo("#progress", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {TOTAL}, ease: "none" }}, 0);
tl.fromTo("#logo", {{ scale: 0.4, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.7, ease: "back.out(2)" }}, A(7.6));
{chr(10).join(chap_js)}
{chr(10).join(scene_js)}
</script>
</body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"offset": OFF, "total": TOTAL, "scenes": [{k: s[k] for k in ("id", "t0", "t1", "chap")} for s in S],
               "transitions": transitions, "captions": caps}, open(os.path.join(ROOT, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subset_fonts()
    print("scenes", len(S), "captions", len(caps), "total", TOTAL)


BGM_GAIN = 0.08  # bgm-a/b measure ~-16.5 LUFS; x0.08 (-22 dB) puts the bed ~22 dB under the -16 LUFS narration


def subset_fonts():
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    text = ""
    for f in ("index.html", "compositions/region.html"):
        text += open(os.path.join(ROOT, f), encoding="utf-8").read()
    chars = set(re.sub(r"<[^>]+>", " ", text)) | set("0123456789$%,.+-·↔→()!?:~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÉé'")
    uni = ",".join(f"U+{ord(c):04X}" for c in sorted(chars) if ord(c) >= 32)
    src = os.environ.get("FONT_SRC", "/tmp/claude-0")
    out = os.path.join(ROOT, "assets/fonts")

    def sub(font, dst):
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        s = subset.Subsetter(opts)
        s.populate(unicodes=subset.parse_unicodes(uni))
        s.subset(font)
        font.flavor = "woff2"
        font.save(dst)

    sub(TTFont(os.path.join(src, "BlackHanSans.ttf")), os.path.join(out, "BlackHanSans.woff2"))
    for w in (500, 700, 900):
        vf = TTFont(os.path.join(src, "NotoSansKR.ttf"))
        inst = instancer.instantiateVariableFont(vf, {"wght": w})
        sub(inst, os.path.join(out, f"NotoSansKR-{w}.woff2"))


if __name__ == "__main__":
    main()
