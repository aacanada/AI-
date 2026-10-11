#!/usr/bin/env node
// ElevenLabs Music → assets/music/bgm.mp3, registered in audio_meta.json as host BGM.
// usage: node el-music.mjs <PROJECT_DIR> <length_seconds> ["prompt"] [--volume 0.14]
// Run AFTER el-tts.mjs (so audio_meta.json exists) and set `music: none` in STORYBOARD.md.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
const [P, secs, promptArg] = process.argv.slice(2);
const vi = process.argv.indexOf("--volume"); const volume = vi > 0 ? Number(process.argv[vi + 1]) : 0.14;
const prompt = promptArg && !promptArg.startsWith("--") ? promptArg :
  "Calm, confident corporate news-explainer underscore. Soft piano, light plucks, gentle warm pulse, subtle uplifting build toward the end. Instrumental only, no vocals, steady 100 BPM, unobtrusive under voiceover.";
const r = await fetch("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", { method: "POST",
  headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({ prompt, music_length_ms: Math.round(Number(secs) * 1000), force_instrumental: true }) });
if (!r.ok) { console.error("music failed", r.status, (await r.text()).slice(0, 300)); process.exit(1); }
mkdirSync(join(P, "assets/music"), { recursive: true });
const out = join(P, "assets/music/bgm.mp3");
writeFileSync(out, Buffer.from(await r.arrayBuffer()));
const dur = +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).toString().trim();
const metaPath = join(P, "audio_meta.json");
const m = existsSync(metaPath) ? JSON.parse(readFileSync(metaPath, "utf8")) : { voices: [], sfx: [] };
m.bgm = { path: "assets/music/bgm.mp3", volume, query: "ElevenLabs Music", duration_s: +dur.toFixed(3), source: "host" };
writeFileSync(metaPath, JSON.stringify(m, null, 2));
console.log(`✓ bgm ${dur.toFixed(1)}s → ${out}`);
