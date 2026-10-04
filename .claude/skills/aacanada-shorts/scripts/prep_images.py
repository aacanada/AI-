#!/usr/bin/env python3
"""Bring the user's attached screenshots into the project.

  python3 prep_images.py <image-or-dir> [...] [--crop "img-01:0,0,100,70"] [--redact "img-02:12,40,30,6" ...]

- Copies each image (png/jpg/jpeg/webp/heic→jpg if ffmpeg can read it) to public/images/img-NN.jpg
  in the given order (directories: sorted by filename). Default source: /mnt/user-data/uploads.
- Downscales very large captures (max 1600px wide, max 4000px tall) — keeps text sharp at 1080 canvas.
- --crop keeps only a region (PERCENT of the original: id:x,y,w,h) — trim blank margins, status bars.
- --redact pixelates a region given in PERCENT of the image: id:x,y,w,h (repeatable). Use it for
  names, passport/visa numbers, emails, phone numbers, addresses, faces of private people.
- Writes images.json: [{id, src, source, w, h, ratio, kind}] — kind is wide | square | tall | xtall.
  build.py injects it into the template as IMAGES.
"""
import json, os, subprocess, sys

EXT = (".png", ".jpg", ".jpeg", ".webp", ".heic", ".heif", ".bmp", ".gif")
args, redact, crop = [], {}, {}
it = iter(sys.argv[1:])
for a in it:
    if a in ("--redact", "--crop"):
        iid, box = next(it).split(":", 1)
        vals = [float(v) for v in box.split(",")]
        if a == "--crop":
            crop[iid] = vals
        else:
            redact.setdefault(iid, []).append(vals)
    else:
        args.append(a)
if not args:
    args = ["/mnt/user-data/uploads"]

files = []
for a in args:
    if os.path.isdir(a):
        files += [os.path.join(a, f) for f in sorted(os.listdir(a)) if f.lower().endswith(EXT)]
    elif os.path.isfile(a):
        files.append(a)
    else:
        print(f"! not found: {a}", file=sys.stderr)
if not files:
    sys.exit("no images found — ask the user to attach/upload the screenshots (see SKILL.md § 첨부 이미지)")


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "csv=p=0:s=x", path]).decode().strip()
    w, h = out.split("\n")[0].split("x")
    return int(w), int(h)


os.makedirs("public/images", exist_ok=True)
manifest = []
for n, src in enumerate(files, 1):
    iid = f"img-{n:02d}"
    out = f"public/images/{iid}.jpg"
    w0, h0 = probe(src)
    pre = ""
    if iid in crop:  # redact boxes are in % of the CROPPED image
        cx, cy, cw, ch = crop[iid]
        pre = f"crop={int(w0 * cw / 100)}:{int(h0 * ch / 100)}:{int(w0 * cx / 100)}:{int(h0 * cy / 100)},"
        w0, h0 = int(w0 * cw / 100), int(h0 * ch / 100)
    scale = min(1.0, 1600 / w0, 4000 / h0)
    w, h = int(w0 * scale) // 2 * 2, int(h0 * scale) // 2 * 2
    chain = [f"[0:v]{pre}scale={w}:{h}:flags=lanczos,format=rgb24[b0]"]
    last = "b0"
    for k, (x, y, bw, bh) in enumerate(redact.get(iid, [])):
        px, py = int(w * x / 100), int(h * y / 100)
        pw, ph = max(int(w * bw / 100), 8), max(int(h * bh / 100), 8)
        cell = max(min(pw, ph) // 2, 10)
        chain.append(f"[{last}]split[m{k}][c{k}]")
        chain.append(f"[c{k}]crop={pw}:{ph}:{px}:{py},scale={max(pw // cell, 1)}:{max(ph // cell, 1)},"
                     f"scale={pw}:{ph}:flags=neighbor[p{k}]")
        chain.append(f"[m{k}][p{k}]overlay={px}:{py}[b{k + 1}]")
        last = f"b{k + 1}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", ";".join(chain),
                    "-map", f"[{last}]", "-frames:v", "1", "-q:v", "2", out], check=True)
    r = h / w
    kind = "wide" if r < 0.85 else "square" if r < 1.3 else "tall" if r < 2.4 else "xtall"
    manifest.append({"id": iid, "src": out, "source": os.path.abspath(src), "w": w, "h": h,
                     "ratio": round(r, 3), "kind": kind, "crop": crop.get(iid), "redacted": redact.get(iid, [])})
    print(f"{iid}  {kind:<6} {w}x{h}  ← {src}" + (f"  (redacted {len(redact[iid])})" if iid in redact else ""))
json.dump(manifest, open("images.json", "w"), ensure_ascii=False, indent=1)
print("→ images.json  (Read each public/images/img-NN.jpg to see it before designing scenes)")
