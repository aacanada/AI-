"""Build timing.json: one slot per recording, per-character speech times. Run from project root:
    python3 -I tools/timing.py
assets/voice/<sid>.wav (tools/audio_prep.py) gives the real duration; <sid>.words.json (whisper phrases with
start/end) gives character times by aligning the phrase text to the script row text.
"""
import difflib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SCENES  # noqa: E402

CPS = 0.15        # provisional seconds per character when no recording
GAP = 0.4         # brief: ~0.4 s between scenes (wav already keeps 0.3 s head/tail)
FIRST_LEAD = 0.5
END_HOLD = 4.0    # end card hold after the last line
TR = 0.5          # scene-to-scene transition overlap


def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def norm(c):
    return c.lower()


def char_times(text, dur, words=None):
    idx = [k for k, c in enumerate(text) if not c.isspace()]
    times = [None] * len(text)
    if words:
        sc, st = [], []
        for w in words:
            cs = [c for c in w["text"] if not c.isspace()]
            for j, c in enumerate(cs):
                sc.append(norm(c))
                st.append(w["start"] + (w["end"] - w["start"]) * j / max(1, len(cs)))
        sm = difflib.SequenceMatcher(None, [norm(text[k]) for k in idx], sc, autojunk=False)
        for a, b, size in sm.get_matching_blocks():
            for x in range(size):
                times[idx[a + x]] = st[b + x]
        known = [(k, times[k]) for k in idx if times[k] is not None]
        # drop non-monotonic matches
        mono, last = [], -1
        for k, t in known:
            if t >= last:
                mono.append((k, t))
                last = t
            else:
                times[k] = None
        known = mono
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
                        times[k] = prev[-1][1] if prev else nxt[0][1]
    if not words:
        n = len(idx)
        for j, k in enumerate(idx):
            times[k] = 0.3 + (dur - 0.6) * j / n
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
    for i, sc in enumerate(SCENES):
        text = " ".join(sc["rows"])
        wav = os.path.join("assets", "voice", sc["id"] + ".wav")
        wj = os.path.join("assets", "voice", sc["id"] + ".words.json")
        has = os.path.exists(wav)
        vd = round(probe(wav), 3) if has else round(len(text.replace(" ", "")) * CPS, 3)
        words = json.load(open(wj, encoding="utf-8")) if has and os.path.exists(wj) else None
        lead = FIRST_LEAD if i == 0 else GAP
        times = [round(lead + x, 3) for x in char_times(text, vd, words)]
        rows, pos = [], 0
        for r in sc["rows"]:
            rows.append(dict(t=times[pos], text=r))
            pos += len(r) + 1
        for k, r in enumerate(rows):
            r["end"] = rows[k + 1]["t"] - 0.05 if k + 1 < len(rows) else round(lead + vd - 0.2, 3)
        hold = END_HOLD if i == len(SCENES) - 1 else 0
        out.append(dict(id=sc["id"], ch=sc["ch"], start=round(t, 3), content=round(lead + vd + hold, 3),
                        voiceAt=lead, voiceDur=vd, real=has, aligned=bool(words), text=text, chars=times, rows=rows))
        t += lead + vd + hold
    for k, s in enumerate(out):
        s["duration"] = round(s["content"] + (TR if k + 1 < len(out) else 0), 3)
    return out, round(t, 3)


if __name__ == "__main__":
    slots, total = build()
    json.dump(dict(total=total, slots=slots), open("timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"slots {len(slots)} total {total:.1f}s ({int(total // 60)}:{total % 60:04.1f})")
    for s in slots:
        print(f"  {s['id']} @ {int(s['start'] // 60)}:{s['start'] % 60:04.1f}  real={s['real']} aligned={s['aligned']}")
