#!/usr/bin/env python3
"""Pick colour palettes so consecutive Shorts never look alike.

  python3 pick_palette.py suggest [--n 3]     -> JSON list of the N least-recently-used palette ids
  python3 pick_palette.py use <id> <project>  -> record the choice (history lives in videos/.palette-history.json)
  python3 pick_palette.py apply <id> <project>-> write the palette into <project>/frame.md colors
  python3 pick_palette.py theme-json <id>     -> {bg,p,t,m,l,al,am,bd,cb} for build_frames.py THEME
"""
import json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
HIST = os.path.join(REPO, "videos", ".palette-history.json")
PAL = {k: v for k, v in json.load(open(os.path.join(HERE, "palettes.json"), encoding="utf-8")).items() if not k.startswith("_")}

def history():
    return json.load(open(HIST, encoding="utf-8")) if os.path.exists(HIST) else []

def suggest(n):
    h = [e["palette"] for e in history()]
    last_used = {p: i for i, p in enumerate(h)}          # later index = more recent
    recent = set(h[-2:])                                 # never offer the last two
    order = sorted(PAL, key=lambda p: last_used.get(p, -1))
    picks = [p for p in order if p not in recent][:n]
    return [{"id": p, "label": PAL[p]["label"]} for p in picks]

def theme_json(pid):
    c = PAL[pid]
    return {"bg": c["bg"], "p": c["primary"], "t": c["text"], "m": c["text-muted"], "l": c["text-light"],
            "al": c["accent-light"], "am": c["accent-medium"], "bd": c["border"], "cb": c["card-bg"]}

def apply(pid, project):
    f = os.path.join(project, "frame.md"); s = open(f, encoding="utf-8").read()
    for k in ["bg", "primary", "text", "text-muted", "text-light", "accent-light", "accent-medium", "border", "card-bg"]:
        s = re.sub(rf'(?m)^(  {re.escape(k)}: )".*?"', rf'\g<1>"{PAL[pid][k]}"', s, count=1)
    open(f, "w", encoding="utf-8").write(s)

def use(pid, project):
    h = history(); h.append({"palette": pid, "project": os.path.basename(os.path.abspath(project)),
                             "date": datetime.date.today().isoformat()})
    os.makedirs(os.path.dirname(HIST), exist_ok=True)
    json.dump(h, open(HIST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "suggest"
    if cmd == "suggest":
        n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3
        print(json.dumps(suggest(n), ensure_ascii=False))
    elif cmd == "theme-json":
        print(json.dumps(theme_json(sys.argv[2])))
    elif cmd == "apply":
        apply(sys.argv[2], sys.argv[3])
    elif cmd == "use":
        use(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
