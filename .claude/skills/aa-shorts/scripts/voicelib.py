"""Shared helpers for AA Canada shorts: SCRIPT.md parsing, pronunciation rules,
ElevenLabs TTS / speech-to-text / history, and audio_meta.json writing.

audio_meta.json is the frame-keyed shape the faceless-explainer scripts consume:
  {"bgm": null, "bgm_pending": false, "sfx": [],
   "voices": [{"frame": 1, "path": "assets/voice/01.wav", "duration_s": 3.8,
               "words": [{"id": "w0", "text": "...", "start": 0.0, "end": 0.4}]}]}
Caption words always carry the SCRIPT spelling; pronunciation fixes only touch
what is sent to / heard from the voice.
"""
import difflib, json, os, re, subprocess, tempfile, time
import requests

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.65, "similarity_boost": 0.8, "style": 0.1, "use_speaker_boost": True, "speed": 1.0}

# Spoken-only rewrites, applied per script word. Add a row whenever the voice misreads something.
SAY = [
    (r"불어권", "불어꿘"),
    (r"(\d+)%", r"\1퍼센트"),
    (r"^AA캐나다", "에이에이 캐나다"),
    (r"^AA", "에이에이"),
    (r"^5,750달러", "오천칠백오십 달러"),
    (r"^40달러", "사십 달러"),
    # The cloned voice tends to insert "어…" at these commas.
    (r"^점심시간이든,$", "점심시간이든"),
    (r"^달러,$", "달러."),
    (r"^발표까지,$", "발표까지"),
]
# Fillers the cloned voice improvises; a take whose transcript contains one is retaken.
FILLER = re.compile(r"(^|\s)(어|음|뭐|아우|이제|근데)[\s,.…]")

# Trailing silence per frame: a breath after the hook/answer, a long hold on the last (CTA) frame.
PAD_FIRST, PAD_DEFAULT, PAD_LAST = 0.45, 0.35, 2.0


def key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        raise SystemExit("ELEVENLABS_API_KEY is not set")
    return k


def voice_id():
    v = os.environ.get("ELEVENLABS_VOICE_ID")
    if not v:
        raise SystemExit("ELEVENLABS_VOICE_ID is not set")
    return v


def parse_script(path):
    """SCRIPT.md → [{"frame": N, "text": spoken line}] from `## … (Frame N)` + indented text."""
    out, cur = [], None
    for line in open(path, encoding="utf8").read().splitlines():
        h = re.match(r"^#{2,3}\s+.*?\(frame\s+(\d+)\)", line, re.I)
        if h:
            if cur and cur["text"]:
                out.append(cur)
            cur = {"frame": int(h.group(1)), "text": ""}
            continue
        if not cur or re.match(r"^\s*\*\*", line):
            continue
        m = re.match(r"^(?: {4,}|\t)(.+)$", line)
        if m:
            cur["text"] += (" " if cur["text"] else "") + m.group(1).strip()
    if cur and cur["text"]:
        out.append(cur)
    for l in out:
        l["text"] = l["text"].strip().strip('"')
    return out


def spoken(word):
    for pat, rep in SAY:
        word = re.sub(pat, rep, word)
    return word


def spoken_line(text):
    return " ".join(spoken(w) for w in text.split())


def norm(s):
    return re.sub(r"[^\w]", "", s)


def ffprobe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def to_wav(src, dst, pad=0.0, start=None, end=None, speed=1.0):
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    if end is not None:
        cmd += ["-to", f"{end:.3f}"]
    af = (f"atempo={speed}," if speed != 1.0 else "") + f"apad=pad_dur={pad}"
    cmd += ["-i", src, "-af", af, "-ar", "44100", "-ac", "1", dst]
    subprocess.run(cmd, check=True)


def pad_for(frame, frames):
    if frame == max(frames):
        return PAD_LAST
    return PAD_FIRST if frame in (1, 2) else PAD_DEFAULT


# ── ElevenLabs ────────────────────────────────────────────────────────────────
def _post(url, **kw):
    for attempt in range(4):
        r = requests.post(url, headers={"xi-api-key": key()}, timeout=180, **kw)
        if r.status_code < 500 and r.status_code != 429:
            break
        time.sleep(2 ** (attempt + 1))
    if not r.ok:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    return r


def tts_with_timestamps(text, prev_text=None, next_text=None):
    body = {"text": text, "model_id": MODEL, "voice_settings": SETTINGS}
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    r = _post(f"{API}/text-to-speech/{voice_id()}/with-timestamps?output_format=mp3_44100_128", json=body)
    return r.json()


def stt(path):
    """Speech-to-text with word timestamps → (text, [{"text","start","end"}])."""
    with open(path, "rb") as f:
        r = _post(f"{API}/speech-to-text", data={"model_id": "scribe_v1", "language_code": "ko"},
                  files={"file": (os.path.basename(path), f)})
    d = r.json()
    words = [{"text": w["text"], "start": w["start"], "end": w["end"]}
             for w in d.get("words", []) if w.get("type") == "word"]
    return d.get("text", ""), words


def history(page_size=100):
    r = requests.get(f"{API}/history", params={"page_size": page_size}, headers={"xi-api-key": key()}, timeout=60)
    r.raise_for_status()
    out = []
    for h in r.json()["history"]:
        if not h.get("text") and h.get("source") == "TTS":
            # eleven_v4 takes made on the website leave `text` empty; recover it from the alignment
            d = requests.get(f"{API}/history/{h['history_item_id']}", headers={"xi-api-key": key()}, timeout=60).json()
            al = (d.get("alignments") or {}).get("alignment") or {}
            h["text"] = re.sub(r"\s+", " ", "".join(al.get("characters", []))).strip()
        if h.get("text"):
            out.append(h)
    return out


def history_audio(item_id, dst):
    r = requests.get(f"{API}/history/{item_id}/audio", headers={"xi-api-key": key()}, timeout=120)
    r.raise_for_status()
    open(dst, "wb").write(r.content)


# ── timing alignment ──────────────────────────────────────────────────────────
def chars_from_alignment(al):
    """ElevenLabs character alignment → whitespace-split tokens with start/end."""
    toks, cur = [], None
    for ch, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                toks.append(cur)
            cur = None
        elif cur is None:
            cur = {"text": ch, "start": s, "end": e}
        else:
            cur["text"] += ch
            cur["end"] = e
    if cur:
        toks.append(cur)
    return toks


def fold_tokens(script_text, toks):
    """Map spoken tokens (one script word may be several spoken tokens) back to script words."""
    words, k = [], 0
    for j, w in enumerate(script_text.split()):
        n = len(spoken(w).split())
        span = toks[k:k + n]
        k += n
        if span:
            words.append({"id": f"w{j}", "text": w, "start": round(span[0]["start"], 3), "end": round(span[-1]["end"], 3)})
    return words


def align_words(script_text, heard):
    """Time each script word from STT words of the same audio (STT spelling may differ,
    e.g. "백 퍼센트" vs "100%"). Char-level match on the spoken form; unmatched words are
    interpolated between neighbours."""
    script_words = script_text.split()
    h_chars, h_time = [], []
    for w in heard:
        cs = norm(w["text"]) or "_"
        dur = max(w["end"] - w["start"], 0.01)
        for i, c in enumerate(cs):
            h_chars.append(c)
            h_time.append((w["start"] + dur * i / len(cs), w["start"] + dur * (i + 1) / len(cs)))

    def match(form):
        """Char-align one spelling of the script against the transcript → per-word (start, end, hits)."""
        chars, owner = [], []
        for j, w in enumerate(script_words):
            for c in norm(form(w)):
                chars.append(c)
                owner.append(j)
        sm = difflib.SequenceMatcher(a=chars, b=h_chars, autojunk=False)
        got = {}
        for a, b, size in sm.get_matching_blocks():
            for i in range(size):
                j = owner[a + i]
                s, e = h_time[b + i]
                g = got.setdefault(j, [s, e, 0])
                g[1] = e
                g[2] += 1
        return got

    # STT may write a word as spoken ("사십 달러") or as written ("$40", "100%", "AA") — try both
    # spellings and keep, per word, whichever matched more characters.
    t_start, t_end = {}, {}
    for got in (match(spoken), match(lambda w: w)):
        for j, (s, e, hits) in got.items():
            if hits > t_start.get(j, (0, 0))[1]:
                t_start[j] = (s, hits)
                t_end[j] = e
    t_start = {j: v[0] for j, v in t_start.items()}
    n = len(script_words)
    total_end = heard[-1]["end"] if heard else 0.0
    starts = [t_start.get(j) for j in range(n)]
    known = [j for j in range(n) if starts[j] is not None]
    for j in range(n):
        if starts[j] is None:
            lo = max([k for k in known if k < j], default=None)
            hi = min([k for k in known if k > j], default=None)
            s0 = starts[lo] if lo is not None else 0.0
            s1 = starts[hi] if hi is not None else total_end
            i0 = lo if lo is not None else -1
            i1 = hi if hi is not None else n
            starts[j] = s0 + (s1 - s0) * (j - i0) / (i1 - i0)
    words = []
    for j, w in enumerate(script_words):
        end = t_end.get(j, starts[j + 1] if j + 1 < n else total_end)
        words.append({"id": f"w{j}", "text": w, "start": round(starts[j], 3), "end": round(max(end, starts[j]), 3)})
    return words


def write_meta(project, voices):
    meta = {"bgm": None, "bgm_pending": False, "voices": sorted(voices, key=lambda v: v["frame"]), "sfx": []}
    json.dump(meta, open(os.path.join(project, "audio_meta.json"), "w"), ensure_ascii=False, indent=2)
    total = sum(v["duration_s"] for v in meta["voices"])
    print(f"✓ audio_meta.json — {len(voices)} lines, {total:.1f}s")


def similarity(a, b):
    return difflib.SequenceMatcher(a=norm(a), b=norm(b), autojunk=False).ratio()
