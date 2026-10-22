#!/usr/bin/env node
// Replace only the changed scenes of an already-rendered (voiceless) longform mp4.
//   node build.mjs segment s01 s06               # render-only projects in emsb-isp-longform/.segments/<id>
//   (cd ../emsb-isp-longform/.segments/s01 && npx hyperframes render --quality looks --output seg.mp4)
//   node splice.mjs emsb-isp-longform_voiceless.mp4 s01 s06
// Scene boundaries come from emsb-isp-longform/chapters.json; scene durations must not have changed.
// Video-only: once narration exists, render the whole longform instead (audio spans every scene).
import { readFileSync, existsSync, renameSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const KIT = dirname(fileURLToPath(import.meta.url));
const DIR = join(KIT, "../emsb-isp-longform");
const [name, ...ids] = process.argv.slice(2);
if (!name || !ids.length) throw new Error("usage: node splice.mjs <video.mp4> <scene id>...");
const src = join(DIR, name);
const { total, chapters } = JSON.parse(readFileSync(join(DIR, "chapters.json"), "utf8"));
const probe = (f, q) => execFileSync("ffprobe", ["-v", "error", ...q, "-of", "csv=p=0", f]).toString().trim();
if (probe(src, ["-select_streams", "a", "-show_entries", "stream=index"])) throw new Error("source has audio; re-render the full longform instead");
if (Math.abs(+probe(src, ["-show_entries", "format=duration"]) - total) > 0.05) throw new Error("source duration != chapters.json total (scene lengths changed?)");

const inputs = [], parts = [];
const nIn = () => inputs.filter((x) => x === "-i").length;
let keepFrom = null;
const flushKeep = (to) => {
  if (keepFrom == null) return;
  // each kept range is its own seeked input, so nothing is buffered while concat reads earlier parts
  inputs.push("-ss", String(keepFrom), "-t", String(to - keepFrom), "-i", src);
  parts.push(`[${nIn() - 1}:v]setpts=PTS-STARTPTS[p${parts.length}]`);
  keepFrom = null;
};
chapters.forEach((c, i) => {
  const end = i + 1 < chapters.length ? chapters[i + 1].start : total;
  if (!ids.includes(c.id)) { if (keepFrom == null) keepFrom = c.start; return; }
  flushKeep(c.start);
  const seg = join(DIR, ".segments", c.id, "seg.mp4");
  if (!existsSync(seg)) throw new Error(`missing ${seg}`);
  if (Math.abs(+probe(seg, ["-show_entries", "format=duration"]) - (end - c.start)) > 0.05) throw new Error(`${c.id}: segment length mismatch`);
  inputs.push("-i", seg);
  parts.push(`[${nIn() - 1}:v]setpts=PTS-STARTPTS[p${parts.length}]`);
});
flushKeep(total);
const graph = parts.join(";") + ";" + parts.map((_, i) => `[p${i}]`).join("") + `concat=n=${parts.length}:v=1:a=0[out]`;
const tmp = src.replace(/\.mp4$/, ".splice-tmp.mp4");
execFileSync("ffmpeg", ["-v", "error", "-y", ...inputs, "-filter_complex", graph, "-map", "[out]", "-r", "30",
  "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp], { stdio: "inherit" });
renameSync(tmp, src);
console.log(`spliced ${ids.join(", ")} into ${name} (${probe(src, ["-show_entries", "format=duration"])}s)`);
