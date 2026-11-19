#!/usr/bin/env python3
"""Build the HyperFrames project from narration timings.

- reads audio/vo/sNN.json (ElevenLabs alignment) + SCRIPT_v2.md caption wording
- resolves anchors in src/scenes/sNN.html (<!--ANCHORS {...}--> / <!--SFX [...]-->)
- writes compositions/sNN.html, index.html, build/timeline.json (scene/sfx/vo placements)
"""
import json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "..", "..", "plans", "french-why-longform")
FPS = 30
PRE = {"s01": 1.2}
PRE_DEFAULT = 0.6
POST = {"s14": 3.4}
POST_DEFAULT = 0.9
SCENES = [f"s{i:02d}" for i in range(1, 15)]
FOOTNOTE = "이민·비자 요건은 바뀔 수 있으며 최종 판단은 캐나다 이민부가 합니다 (2026.11 기준)"


def q(t):  # quantize to frame grid
    return round(round(t * FPS) / FPS, 4)


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())


def script_lines():
    s = open(os.path.join(PLAN, "SCRIPT_v2.md"), encoding="utf-8").read()
    secs = re.split(r"^## S(\d+)\..*$", s, flags=re.M)
    out = {}
    for i in range(1, len(secs), 2):
        body = secs[i + 1].split("\n---")[0]
        out["s%02d" % int(secs[i])] = [l.strip() for l in body.strip().splitlines()
                                       if l.strip() and not l.strip().startswith("-") and not l.startswith("예상")]
    return out


class Align:
    def __init__(self, sid):
        d = json.load(open(os.path.join(ROOT, "audio", "vo", f"{sid}.json"), encoding="utf-8"))
        a = d["alignment"]
        self.chars = a["characters"]
        self.st = a["character_start_times_seconds"]
        self.en = a["character_end_times_seconds"]
        self.text = "".join(self.chars)
        self.lines = d["lines"]
        # char offsets for each narration line
        self.offs = []
        pos = 0
        for ln in self.lines:
            i = self.text.index(ln, pos)
            self.offs.append((i, i + len(ln)))
            pos = i + len(ln)

    def t_start(self, i):
        while i < len(self.chars) and self.chars[i].isspace():
            i += 1
        return self.st[min(i, len(self.st) - 1)]

    def t_end(self, j):  # j exclusive
        j -= 1
        while j > 0 and self.chars[j] in " \n\"'.,?!":
            j -= 1
        return self.en[j]

    def find(self, word, occ=1, after=0):
        pos = after
        for _ in range(occ):
            i = self.text.index(word, pos)
            pos = i + 1
        return i


HANGUL = re.compile(r"[가-힣]+")


GOOD_END = ("는지", "인지", "하고", "에서", "면", "데", "고", "서", "며", "에", "도", "요", "는", "은")


def split_chunks(line, maxlen=27):
    """split a caption line into display chunks at punctuation, then at natural spaces"""
    parts = re.findall(r"(?:[^,.?!]|[,.](?=\d))+[,.?!]*\"?", line)
    parts = [p.strip() for p in parts if p.strip()]
    chunks = []
    for p in parts:
        if chunks and len(chunks[-1]) + 1 + len(p) <= maxlen and not chunks[-1].endswith((".", "?", "!", ".\"", "?\"")):
            chunks[-1] = chunks[-1] + " " + p
        else:
            chunks.append(p)
    out = []
    for c in chunks:
        while len(c) > maxlen + 3:
            words = c.split(" ")
            best, target = None, len(c) / 2
            for k in range(1, len(words)):
                acc = len(" ".join(words[:k]))
                if acc < 6 or len(c) - acc < 6:
                    continue
                score = abs(acc - target) - (5 if words[k - 1].rstrip(",").endswith(GOOD_END) else 0)
                if best is None or score < best[1]:
                    best = (k, score)
            if best is None:
                break
            out.append(" ".join(words[:best[0]]))
            c = " ".join(words[best[0]:])
        out.append(c)
    merged = []
    for c in out:  # fold very short lead-ins ("첫째,") into the following chunk
        if merged and len(merged[-1]) < 9 and len(merged[-1]) + 1 + len(c) <= 33:
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return merged


def caption_chunks(al, sid, slines):
    res = []
    for li, (sl, (a, b)) in enumerate(zip(slines, al.offs)):
        narr = al.text[a:b]
        chunks = split_chunks(sl)
        ls, le = al.t_start(a), al.t_end(b)
        bounds = [ls]
        npos = 0
        for ci, ch in enumerate(chunks[:-1]):
            toks = HANGUL.findall(ch)
            t = None
            if toks:
                tok = toks[-1]
                k = narr.find(tok, npos)
                if k >= 0:
                    npos = k + len(tok)
                    t = al.en[a + npos - 1]
            if t is None:  # proportional fallback
                frac = sum(len(c) for c in chunks[:ci + 1]) / sum(len(c) for c in chunks)
                t = ls + (le - ls) * frac
            bounds.append(max(t, bounds[-1] + 0.4))
        bounds.append(le)
        segs = [[ch, bounds[ci], bounds[ci + 1]] for ci, ch in enumerate(chunks)]
        k = 0
        while k < len(segs) - 1:  # merge flashes (<1.4s) with a neighbour when the result still fits one row
            a, b = segs[k], segs[k + 1]
            if (a[2] - a[1] < 1.4 or b[2] - b[1] < 1.4) and len(a[0]) + 1 + len(b[0]) <= 33:
                segs[k] = [a[0] + " " + b[0], a[1], b[2]]
                del segs[k + 1]
            else:
                k += 1
        for ch, a, b in segs:
            res.append({"text": ch, "start": a, "end": b, "line": li})
    return res


def resolve(al, spec, pre):
    """anchor spec: 'L3' line start, 'L3e' line end, 'word' / 'word#2', optional '+0.3' / '-0.2'"""
    off = 0.0
    m = re.match(r"^(.*?)([+-]\d+(?:\.\d+)?)$", spec)
    if m and m.group(1):
        spec, off = m.group(1), float(m.group(2))
    if re.fullmatch(r"L\d+e?", spec):
        n = int(spec[1:].rstrip("e"))
        a, b = al.offs[n]
        t = al.t_end(b) if spec.endswith("e") else al.t_start(a)
    elif spec == "END":
        t = al.t_end(len(al.chars))
    else:
        occ = 1
        if "#" in spec:
            spec, o = spec.split("#")
            occ = int(o)
        i = al.find(spec, occ)
        t = al.t_start(i)
    return q(pre + t + off)


def build():
    slines = script_lines()
    t0 = 0.0
    timeline = {"fps": FPS, "scenes": [], "sfx": [], "captions": []}
    helpers = open(os.path.join(ROOT, "src", "helpers.js"), encoding="utf-8").read()
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    for sid in SCENES:
        al = Align(sid)
        vo_len = dur(os.path.join(ROOT, "audio", "vo", f"{sid}.mp3"))
        pre = PRE.get(sid, PRE_DEFAULT)
        D = q(pre + vo_len + POST.get(sid, POST_DEFAULT))
        sp = os.path.join(ROOT, "src", "scenes", f"{sid}.html")
        if not os.path.exists(sp):
            sp = os.path.join(ROOT, "src", "placeholder.html")
        src = open(sp, encoding="utf-8").read()
        m = re.search(r"<!--ANCHORS\s*(\{.*?\})\s*-->", src, flags=re.S)
        anchors = json.loads(m.group(1)) if m else {}
        cues = {k: resolve(al, v, pre) if isinstance(v, str) else q(v) for k, v in anchors.items()}
        cues["L"] = [[q(pre + al.t_start(a)), q(pre + al.t_end(b))] for a, b in al.offs]
        cues["D"] = D
        ms = re.search(r"<!--SFX\s*(\[.*?\])\s*-->", src, flags=re.S)
        sfx = json.loads(ms.group(1)) if ms else []
        for name, at in sfx:
            t = cues[at] if isinstance(at, str) and at in cues else (resolve(al, at, pre) if isinstance(at, str) else at)
            timeline["sfx"].append({"name": name, "t": q(t0 + t), "scene": sid})
        if sid != "s01":  # seam wipe sound, aligned with the index wipe start (seam - 0.3s)
            timeline["sfx"].append({"name": "transition_ding", "t": q(t0 - 0.3), "scene": sid})
        body = re.sub(r"<!--(ANCHORS|SFX).*?-->", "", src, flags=re.S)
        body = body.replace("__CUES__", json.dumps(cues)).replace("__HELPERS__", helpers).replace("__ID__", sid)
        html = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
{body}
    </template>
  </body>
</html>
"""
        open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w", encoding="utf-8").write(html)
        for c in caption_chunks(al, sid, slines[sid]):
            timeline["captions"].append({"text": c["text"], "start": q(t0 + pre + c["start"]), "end": q(t0 + pre + c["end"]), "scene": sid})
        timeline["scenes"].append({"id": sid, "start": q(t0), "duration": D, "vo_start": q(t0 + pre), "vo_len": vo_len})
        t0 = q(t0 + D)
    timeline["total"] = q(t0)
    # caption display windows: hold until next chunk (max gap 0.6s)
    caps = timeline["captions"]
    for i, c in enumerate(caps):
        nxt = caps[i + 1]["start"] if i + 1 < len(caps) else c["end"] + 0.5
        c["show"] = c["start"] - 0.05
        c["hide"] = min(nxt - 0.17, c["end"] + 0.6) if nxt - c["end"] < 1.2 else c["end"] + 0.45
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    json.dump(timeline, open(os.path.join(ROOT, "build", "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_index(timeline)
    print("total", timeline["total"], "scenes", len(timeline["scenes"]), "sfx", len(timeline["sfx"]), "captions", len(caps))


def write_index(tl):
    tpl = open(os.path.join(ROOT, "src", "index.tpl.html"), encoding="utf-8").read()
    hosts = []
    for i, s in enumerate(tl["scenes"]):
        hosts.append(f'      <div id="{s["id"]}" class="clip scene-host" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
                     f'data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1" data-width="1920" data-height="1080"></div>')
    caps = []
    for i, c in enumerate(tl["captions"]):
        txt = c["text"].replace("&", "&amp;").replace("<", "&lt;")
        caps.append(f'        <div class="cap" id="cap-{i}"><span>{txt}</span></div>')
    s02 = next(s for s in tl["scenes"] if s["id"] == "s02")
    s13 = next(s for s in tl["scenes"] if s["id"] == "s13")
    fn_start, fn_dur = s02["start"], q(s13["start"] + s13["duration"] - s02["start"])
    seams = [s["start"] for s in tl["scenes"][1:]]
    capdata = [[round(c["show"], 3), round(c["hide"], 3)] for c in tl["captions"]]
    out = (tpl.replace("__TOTAL__", str(tl["total"]))
           .replace("__HOSTS__", "\n".join(hosts))
           .replace("__CAPTIONS__", "\n".join(caps))
           .replace("__CAPDATA__", json.dumps(capdata))
           .replace("__SEAMS__", json.dumps(seams))
           .replace("__FN_START__", str(fn_start)).replace("__FN_DUR__", str(fn_dur))
           .replace("__FOOTNOTE__", FOOTNOTE))
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    build()
