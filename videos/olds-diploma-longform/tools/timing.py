"""Build timing.json (slot layout + per-character speech times). Run from project root:
    python3 -I tools/timing.py

Per scene (all narration, no face video):
  - assets/voice/<sid>.wav present (made by tools/audio_prep.py) -> real duration;
    assets/voice/<sid>.words.json ([{"text","start","end"}]) -> character times by alignment.
  - otherwise provisional: non-space characters x 0.13 s, characters spread linearly.
  - once any recording is in, a scene whose recording is missing is LEFT OUT (listed in timing.json "missing").
"""
import difflib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import CHAPTERS, SCENES  # noqa: E402

CPS = 0.13      # provisional seconds per non-space character
LEAD = 0.35     # scene visible before its narration starts (= gap between scenes, brief: 0.35 s)
TR = 0.45       # transition inside a chapter (unused: one narration slot per scene)
CARD = 1.8      # scene title card (brief: 1.5~2 s)
CTR = 0.6       # transition into a title card
FIRST_LEAD = 0.6
END_HOLD = 3.0  # CTA hold after the last line


def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def char_times(text, dur, words=None):
    """Return a start time for every character of text (spaces get the next char's time)."""
    idx = [k for k, c in enumerate(text) if not c.isspace()]
    times = [None] * len(text)
    if words:
        sc, st = [], []
        for w in words:
            cs = [c for c in w["text"] if not c.isspace()]
            for j, c in enumerate(cs):
                sc.append(c)
                st.append(w["start"] + (w["end"] - w["start"]) * j / max(1, len(cs)))
        sm = difflib.SequenceMatcher(None, [text[k] for k in idx], sc, autojunk=False)
        for a, b, size in sm.get_matching_blocks():
            for x in range(size):
                times[idx[a + x]] = st[b + x]
        # interpolate gaps
        known = [(k, times[k]) for k in idx if times[k] is not None]
        if not known:
            words = None
        else:
            for k in idx:
                if times[k] is None:
                    prev = [kt for kt in known if kt[0] < k]
                    nxt = [kt for kt in known if kt[0] > k]
                    if prev and nxt:
                        (k0, t0), (k1, t1) = prev[-1], nxt[0]
                        times[k] = t0 + (t1 - t0) * (k - k0) / (k1 - k0)
                    else:
                        times[k] = (prev[-1][1] if prev else nxt[0][1])
    if not words:
        n = len(idx)
        for j, k in enumerate(idx):
            times[k] = dur * j / n
    nxt = dur
    for k in range(len(text) - 1, -1, -1):
        if times[k] is None:
            times[k] = nxt
        else:
            times[k] = round(times[k], 3)
            nxt = times[k]
    return times


def build():
    out, t = [], 0.0
    chap_of = {c[0]: c for c in CHAPTERS}
    any_real = any(os.path.exists(os.path.join("assets", "voice", sc["id"] + ".wav")) for sc in SCENES)
    scenes = [sc for sc in SCENES if not any_real or os.path.exists(os.path.join("assets", "voice", sc["id"] + ".wav"))]
    missing = [sc["id"] for sc in SCENES if sc not in scenes]
    for i, sc in enumerate(scenes):
        ch = sc["ch"]
        if chap_of[ch][4]:
            out.append(dict(id=f"c{ch:02d}", kind="card", ch=ch, start=round(t, 3), content=CARD,
                            trans_in=chap_of[ch][4], ov=CTR))
            t += CARD
        text = " ".join(sc["rows"])
        wav = os.path.join("assets", "voice", sc["id"] + ".wav")
        wj = os.path.join("assets", "voice", sc["id"] + ".words.json")
        has = os.path.exists(wav)
        nchar = sum(1 for c in text if not c.isspace())
        vd = round(probe(wav), 3) if has else round(nchar * CPS, 3)
        words = json.load(open(wj, encoding="utf-8")) if has and os.path.exists(wj) else None
        lead = FIRST_LEAD if i == 0 else LEAD
        times = [round(lead + x, 3) for x in char_times(text, vd, words)]
        rows, pos = [], 0
        for r in sc["rows"]:
            rows.append(dict(t=times[pos], text=r))
            pos += len(r) + 1
        for k, r in enumerate(rows):
            r["end"] = rows[k + 1]["t"] - 0.1 if k + 1 < len(rows) else round(lead + vd, 3)
        hold = END_HOLD if i == len(scenes) - 1 else 0
        out.append(dict(id=sc["id"], kind="vo", ch=ch, start=round(t, 3), content=round(lead + vd + hold, 3),
                        voiceAt=lead, voiceDur=vd, real=has, aligned=bool(words), text=text, chars=times, rows=rows,
                        trans_in=None if i == 0 else "fade", ov=TR))
        t += lead + vd + hold
    # each slot extends over the next slot's incoming transition
    for k, s in enumerate(out):
        ov = out[k + 1]["ov"] if k + 1 < len(out) else 0
        s["duration"] = round(s["content"] + ov, 3)
    build.missing = missing
    return out, round(t, 3)


if __name__ == "__main__":
    slots, total = build()
    json.dump(dict(total=total, slots=slots), open("timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    real = sum(1 for s in slots if s["kind"] == "vo" and s["real"])
    print(f"slots {len(slots)} total {total:.1f}s ({int(total // 60)}:{total % 60:04.1f}) real-voice scenes {real}/{len(SCENES)} missing {build.missing}")
    for s in slots:
        if s["kind"] != "vo":
            print(f"  S{s['ch']:02d} @ {int(s['start'] // 60)}:{s['start'] % 60:04.1f}")
