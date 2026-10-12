import json, re, subprocess, difflib, sys
P = sys.argv[1]
norm = lambda s: re.sub(r"[^0-9A-Za-z가-힣%:]", "", s).lower()
voices = []
for line in open(f"{P}/.vo_text.txt", encoding="utf8"):
    n, text = line.rstrip("\n").split("|", 1); n = int(n); id_ = f"{n:02d}"
    stt = [w for w in json.load(open(f"{P}/.stt_{id_}.json"))["words"] if w["type"] == "word"]
    # per-char times from STT
    sc, st = [], []
    for w in stt:
        t = norm(w["text"]); L = max(len(t), 1)
        for k, c in enumerate(t):
            sc.append(c); st.append((w["start"] + (w["end"] - w["start"]) * k / L, w["start"] + (w["end"] - w["start"]) * (k + 1) / L))
    words = text.split(); chars = []; owner = []
    for i, w in enumerate(words):
        for c in norm(w): chars.append(c); owner.append(i)
    sm = difflib.SequenceMatcher(None, chars, sc, autojunk=False)
    cmap = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size): cmap[a + k] = st[b + k]
    res = [[None, None] for _ in words]
    for ci, o in enumerate(owner):
        if ci in cmap:
            s, e = cmap[ci]
            if res[o][0] is None: res[o][0] = s
            res[o][1] = e
    # interpolate gaps
    for i in range(len(res)):
        if res[i][0] is None:
            prev = next((res[j][1] for j in range(i - 1, -1, -1) if res[j][1] is not None), 0.0)
            nxt = next((res[j][0] for j in range(i + 1, len(res)) if res[j][0] is not None), prev + 0.4)
            res[i] = [prev + 0.02, max(prev + 0.1, nxt - 0.02)]
    wav = f"assets/voice/{id_}.wav"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{P}/{wav}"]).decode())
    voices.append({"frame": n, "path": wav, "duration_s": round(dur, 3),
                   "words": [{"id": f"w{i}", "text": w, "start": round(res[i][0], 3), "end": round(res[i][1], 3)} for i, w in enumerate(words)]})
    print(id_, round(dur, 2), " ".join(f"{w}@{res[i][0]:.2f}" for i, w in enumerate(words)))
json.dump({"bgm": None, "bgm_pending": False, "voices": voices, "sfx": []}, open(f"{P}/audio_meta.json", "w"), ensure_ascii=False, indent=2)
