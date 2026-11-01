"""ElevenLabs narration (voice "여덟번째" = cbVXtFGe9VfUKWtbYIty, eleven_multilingual_v2; 2026-11-01 re-voice, was "일곱번째") with character timestamps. Run from project root:
    python3 -I tools/tts.py            # scenes whose mp3 is missing
    python3 -I tools/tts.py s04 --force
then:  python3 -I tools/build.py

Output: ../../plans/olds-diploma-longform/audio/oldsdip_sNN.mp3 (committed), assets/voice/sNN.align.json (raw alignment),
        assets/voice/sNN.wav (loudnorm -16, 48 kHz) and sNN.words.json (one entry per spoken character, for timing.py).
Needs ELEVENLABS_API_KEY. The voice is looked up by exact name ("여덟번째"); stops if not found (no fallback).
voice_settings follow the Montreal longform (stability 0.5 / similarity_boost 0.75, default speed); stability/style
are nudged per scene in SCENE_SET for natural phrasing. Every request is appended to audio/tts_log.json.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SAY, SCENES  # noqa: E402

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
VOICE_NAME = "여덟번째"
AUD = os.path.join("..", "..", "plans", "olds-diploma-longform", "audio")
OUT = os.path.join("assets", "voice")
BASE = dict(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
# per scene: (stability, style). Opening/closing a little warmer; number-heavy scenes steadier.
SCENE_SET = {"s01": (0.45, 0.12), "s02": (0.5, 0.06), "s03": (0.5, 0.06), "s04": (0.48, 0.08), "s05": (0.48, 0.08),
             "s06": (0.5, 0.06), "s07": (0.55, 0.03), "s08": (0.55, 0.03), "s09": (0.45, 0.12)}


def settings(sid):
    st, sy = SCENE_SET.get(sid, (BASE["stability"], 0.0))
    return dict(BASE, stability=st, style=sy)


def req(path, body=None):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                               headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=180) as f:
        return json.load(f)


def voice_id():
    hit = [v for v in req("/voices")["voices"] if v["name"] == VOICE_NAME]
    if len(hit) != 1:
        raise SystemExit(f'voice "{VOICE_NAME}" not found uniquely')
    return hit[0]["voice_id"], hit[0]["name"]


def say(text):
    for a, b in SAY:
        text = text.replace(a, b)
    return text


def tts(vid, sid, text, prev=None, nxt=None, seed=8):
    body = dict(text=text, model_id=MODEL, voice_settings=settings(sid), seed=seed)
    if prev:
        body["previous_text"] = prev
    if nxt:
        body["next_text"] = nxt
    return req(f"/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128", body)


def norm_chain(src, target=-16.0):
    """Per-scene loudness: gain + gentle compressor + true-peak limiter, iterated until the scene alone reads ~target LUFS.
    (TTS peaks sit far above its loudness, so plain gain would clip.)"""
    import re
    def meas(af):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", af + ",ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return float(re.search(r"I:\s+(-?[\d.]+) LUFS", r[r.rindex("Summary:"):]).group(1))
    g = target - meas("anull")
    for _ in range(10):
        af = (f"volume={g - 6:.2f}dB,acompressor=threshold=-24dB:ratio=3:attack=5:release=120:knee=4,"
              f"volume=6dB,alimiter=limit=0.70:attack=1:release=80:level=false")
        got = meas(af)
        if abs(got - target) < 0.1:
            break
        g += target - got
    return af, got


PAUSE = {".": 0.50, "?": 0.55, "!": 0.50}  # target silence after a sentence end (TTS gives ~0.15-0.25 s)
SR = 48000


def breathe(x, ch, st, en, spoken, t0):
    """Lengthen the silence after each sentence end (except the last) to PAUSE. Cut point = quietest 10 ms frame
    in the gap; inserted audio is digital silence. Returns new samples and per-char time shifts."""
    import numpy as np
    hop = SR // 100
    nfr = len(x) // hop
    rms = np.sqrt(np.mean(x[:nfr * hop].reshape(nfr, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    cuts = []  # (sample, insert_seconds, char index after which the shift applies)
    for j, k in enumerate(spoken[:-1]):
        if ch[k] not in PAUSE:
            continue
        nk = spoken[j + 1]
        a, b = en[k] - t0 - 0.06, st[nk] - t0 + 0.06
        fa, fb = max(0, int(a * 100)), min(nfr - 1, int(b * 100) + 1)
        if fb <= fa:
            continue
        f = fa + int(np.argmin(db[fa:fb + 1]))
        lo = f
        while lo > 0 and db[lo - 1] < -45:
            lo -= 1
        hi = f
        while hi < nfr - 1 and db[hi + 1] < -45:
            hi += 1
        have = (hi - lo + 1) / 100
        add = round(max(0.0, PAUSE[ch[k]] - have), 3)
        if add > 0:
            cuts.append((f * hop + hop // 2, add, nk))
    parts, last, shift = [], 0, {}
    total = 0.0
    for smp, add, nk in cuts:
        parts += [x[last:smp], np.zeros(int(add * SR), dtype=x.dtype)]
        last = smp
        total += add
        shift[nk] = total
    parts.append(x[last:])
    return np.concatenate(parts), cuts


def finish(sid, mp3, align):
    """mp3 + alignment -> trimmed, sentence pauses lengthened, loudness-normalised (-16 LUFS) 48 kHz wav
    + per-character words.json (times follow the inserted pauses)."""
    import numpy as np
    ch, st, en = align["characters"], align["character_start_times_seconds"], align["character_end_times_seconds"]
    spoken = [k for k, c in enumerate(ch) if not c.isspace()]
    t0 = max(0.0, st[spoken[0]] - 0.08)
    t1 = en[spoken[-1]] + 0.25
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", mp3, "-ar", str(SR), "-ac", "1",
                          "-f", "f32le", "-"], check=True, capture_output=True).stdout
    x = np.frombuffer(pcm, dtype=np.float32)
    y, cuts = breathe(x, ch, st, en, spoken, t0)
    raw = os.path.join(OUT, f"{sid}.raw.wav")
    wav = os.path.join(OUT, f"{sid}.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", raw],
                   input=y.astype(np.float32).tobytes(), check=True)
    af, got = norm_chain(raw)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", af, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", wav], check=True)
    os.remove(raw)
    print(f"  {sid}: +{sum(c[1] for c in cuts):.2f}s pauses at {len(cuts)} sentence ends, normalised {got:.1f} LUFS")
    words, add, ci = [], 0.0, 0
    for k in spoken:
        while ci < len(cuts) and cuts[ci][2] == k:
            add += cuts[ci][1]
            ci += 1
        words.append(dict(text=ch[k], start=round(st[k] - t0 + add, 3), end=round(en[k] - t0 + add, 3)))
    json.dump(words, open(os.path.join(OUT, f"{sid}.words.json"), "w", encoding="utf-8"), ensure_ascii=False)


def main(args):
    force = "--force" in args
    only = [a for a in args if not a.startswith("--")]
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    vid, vname = voice_id()
    print(f"voice: {vname} ({vid})")
    texts = [say(" ".join(s["rows"])) for s in SCENES]
    used = 0
    for i, s in enumerate(SCENES):
        if only and s["id"] not in only:
            continue
        mp3 = os.path.join(AUD, s["audio"] + ".mp3")
        aj = os.path.join(OUT, f"{s['id']}.align.json")
        if os.path.exists(mp3) and os.path.exists(aj) and not force:
            finish(s["id"], mp3, json.load(open(aj, encoding="utf-8")))
            continue
        seed = int(os.environ.get("TTS_SEED", "8"))
        r = tts(vid, s["id"], texts[i], texts[i - 1][-300:] if i else None, texts[i + 1][:300] if i + 1 < len(texts) else None, seed)
        data = base64.b64decode(r["audio_base64"])
        open(mp3, "wb").write(data)
        tk = os.path.join(AUD, "takes")
        os.makedirs(tk, exist_ok=True)
        n = len([f for f in os.listdir(tk) if f.startswith(s["audio"] + "_t") and f.endswith(".mp3")]) + 1
        open(os.path.join(tk, f'{s["audio"]}_t{n}.mp3'), "wb").write(data)
        json.dump(r["alignment"], open(os.path.join(tk, f'{s["audio"]}_t{n}.align.json'), "w", encoding="utf-8"), ensure_ascii=False)
        lp = os.path.join(AUD, "tts_log.json")
        log = json.load(open(lp, encoding="utf-8")) if os.path.exists(lp) else {}
        log.setdefault(s["id"], []).append(dict(take=n, voice_id=vid, voice_name=vname, model_id=MODEL, seed=seed,
                                                 voice_settings=settings(s["id"]), chars=len(texts[i]), tts_text=texts[i]))
        json.dump(log, open(lp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(r["alignment"], open(aj, "w", encoding="utf-8"), ensure_ascii=False)
        used += len(texts[i])
        finish(s["id"], mp3, r["alignment"])
        print(f"{s['id']}: {len(texts[i])} chars")
    print(f"characters sent: {used}")


if __name__ == "__main__":
    main(sys.argv[1:])
