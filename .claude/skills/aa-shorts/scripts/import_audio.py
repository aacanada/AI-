#!/usr/bin/env python3
"""Import narration the user generated on the ElevenLabs website (mode B).

Sources (pick one):
  (default)        ElevenLabs history — the most recent items whose text matches SCRIPT.md.
                   Works whether the user generated one take per line or the whole script at once.
  --ids a,b,c      specific history item ids (in script order, or one id for the whole script)
  --file x.mp3     a local recording of the whole script (e.g. downloaded from Google Drive)

Timing comes from ElevenLabs speech-to-text on the actual audio, mapped back onto the
SCRIPT.md wording, so captions show the script spelling even if the voice ad-libbed.
A whole-script recording is cut into per-line clips at the silences between lines.

  python3 import_audio.py --project videos/<slug> [--ids …|--file …] [--speed 1.1] [--dry-run]
"""
import argparse, os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import voicelib as V

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--ids", default="")
ap.add_argument("--file", default="")
ap.add_argument("--speed", type=float, default=1.0, help="tempo change, pitch kept (e.g. 1.1 = 10%% faster)")
ap.add_argument("--dry-run", action="store_true", help="only report which history items would be used")
a = ap.parse_args()

proj = os.path.abspath(a.project)
lines = V.parse_script(os.path.join(proj, "SCRIPT.md"))
frames = [l["frame"] for l in lines]
full_text = " ".join(l["text"] for l in lines)
tmpdir = tempfile.mkdtemp(prefix="aa-import-")
os.makedirs(os.path.join(proj, "assets/voice"), exist_ok=True)


def sim_line(item_text, line_text):
    return max(V.similarity(item_text, line_text), V.similarity(item_text, V.spoken_line(line_text)))


def pick_from_history():
    """→ ("full", item) or ("lines", {frame: item}).

    A whole-script take wins: that is what the user makes on the website (per-line takes are
    usually our own API retakes). Newest whole-script take first; per-line only when there is none.
    """
    hist = V.history()  # newest first
    full = [h for h in hist if sim_line(h["text"], full_text) >= 0.8]
    if full:
        for other in full[1:3]:
            print(f"  (older whole-script take: {other['history_item_id']} · {other.get('model_id')})")
        return "full", full[0]
    per = {}
    for l in lines:
        for h in hist:
            if sim_line(h["text"], l["text"]) >= 0.85:
                per[l["frame"]] = h
                break
    if len(per) == len(lines):
        return "lines", per
    missing = [l["frame"] for l in lines if l["frame"] not in per]
    raise SystemExit(f"✗ no whole-script take and no history match for line(s) {missing} — "
                     "generate them on the ElevenLabs site, or pass --ids / --file")


def import_line(frame, src, text):
    wav = os.path.join(proj, f"assets/voice/{frame:02d}.wav")
    V.to_wav(src, wav, pad=V.pad_for(frame, frames), speed=a.speed)
    heard_text, heard = V.stt(wav)
    words = V.align_words(text, heard)
    print(f"✓ line {frame}: {V.ffprobe_duration(wav):.2f}s | heard: {heard_text}")
    return {"frame": frame, "path": f"assets/voice/{frame:02d}.wav",
            "duration_s": round(V.ffprobe_duration(wav), 3), "words": words}


def import_full(src):
    """Cut one whole-script recording into per-line clips at the gaps between lines."""
    if a.speed != 1.0:
        fast = os.path.join(tmpdir, "full_speed.wav")
        V.to_wav(src, fast, speed=a.speed)
        src = fast
    heard_text, heard = V.stt(src)
    words = V.align_words(full_text, heard)
    total = V.ffprobe_duration(src)
    # index of each line's first/last word in the flat word list
    bounds, k = [], 0
    for l in lines:
        n = len(l["text"].split())
        bounds.append((k, k + n - 1))
        k += n
    cuts = [0.0]
    for (_, last), (first, _) in zip(bounds, bounds[1:]):
        gap_a, gap_b = words[last]["end"], words[first]["start"]
        cuts.append(round((gap_a + gap_b) / 2 if gap_b > gap_a else gap_b - 0.02, 3))
    cuts.append(total)
    voices = []
    for i, l in enumerate(lines):
        f = l["frame"]
        s, e = cuts[i], cuts[i + 1]
        wav = os.path.join(proj, f"assets/voice/{f:02d}.wav")
        V.to_wav(src, wav, pad=V.pad_for(f, frames), start=s, end=e)
        lw = []
        for j, w in enumerate(words[bounds[i][0]:bounds[i][1] + 1]):
            lw.append({"id": f"w{j}", "text": w["text"], "start": round(max(0.0, w["start"] - s), 3),
                       "end": round(max(0.0, w["end"] - s), 3)})
        d = V.ffprobe_duration(wav)
        voices.append({"frame": f, "path": f"assets/voice/{f:02d}.wav", "duration_s": round(d, 3), "words": lw})
        print(f"✓ line {f}: {s:.2f}–{e:.2f}s of the recording → {d:.2f}s")
    print(f"  heard: {heard_text}")
    return voices


if a.file:
    voices = import_full(os.path.abspath(a.file))
else:
    if a.ids:
        ids = [x for x in a.ids.split(",") if x]
        hist = {h["history_item_id"]: h for h in V.history()}
        if len(ids) == 1:
            mode, pick = "full", hist.get(ids[0], {"history_item_id": ids[0], "text": "?"})
        elif len(ids) == len(lines):
            mode, pick = "lines", {l["frame"]: hist.get(i, {"history_item_id": i, "text": "?"}) for l, i in zip(lines, ids)}
        else:
            raise SystemExit(f"✗ --ids: give 1 id (whole script) or {len(lines)} ids (one per line)")
    else:
        mode, pick = pick_from_history()
    if mode == "lines":
        for l in lines:
            h = pick[l["frame"]]
            print(f"  line {l['frame']} ← {h['history_item_id']} ({h.get('voice_name','?')}) {h['text'][:40]}")
    else:
        print(f"  whole script ← {pick['history_item_id']} ({pick.get('model_id','?')}) {pick['text'][:40]}…")
    if a.dry_run:
        sys.exit(0)
    if mode == "lines":
        voices = []
        for l in lines:
            mp3 = os.path.join(tmpdir, f"{l['frame']:02d}.mp3")
            V.history_audio(pick[l["frame"]]["history_item_id"], mp3)
            voices.append(import_line(l["frame"], mp3, l["text"]))
    else:
        mp3 = os.path.join(tmpdir, "full.mp3")
        V.history_audio(pick["history_item_id"], mp3)
        voices = import_full(mp3)

V.write_meta(proj, voices)
