#!/usr/bin/env node
// ElevenLabs narration with word timings for a HyperFrames faceless-explainer project.
// Reads SCRIPT.md ("## Line N — label (Frame N)" + 4-space-indented spoken text), writes
// assets/voice/NN.wav per frame and a frame-keyed audio_meta.json that captions.mjs /
// assemble-index.mjs / audio.mjs sync-durations already understand. Keeps any host BGM entry.
//
// usage: node el-tts.mjs <PROJECT_DIR> [--voice-name "네 번째"] [--speed 1.05]
// env:   ELEVENLABS_API_KEY (required), ELEVENLABS_VOICE_ID (optional; --voice-name wins)
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
const argv = process.argv.slice(2);
const P = argv[0];
const flag = (n, d) => { const i = argv.indexOf(`--${n}`); return i > 0 ? argv[i + 1] : d; };
const key = process.env.ELEVENLABS_API_KEY;
if (!P || !key) { console.error("usage: el-tts.mjs <PROJECT_DIR> [--voice-name 이름] (needs ELEVENLABS_API_KEY)"); process.exit(1); }
const H = { "xi-api-key": key, "Content-Type": "application/json" };

let VOICE = process.env.ELEVENLABS_VOICE_ID;
const voiceName = flag("voice-name", VOICE ? null : "네 번째");
if (voiceName) {
  const list = await (await fetch("https://api.elevenlabs.io/v1/voices", { headers: H })).json();
  const v = list.voices.find((x) => x.name.trim() === voiceName);
  if (!v) { console.error(`voice "${voiceName}" not found. available: ${list.voices.map((x) => x.name).join(", ")}`); process.exit(1); }
  VOICE = v.voice_id;
}
const speed = Number(flag("speed", "1.05"));

const lines = []; let cur = null;
for (const l of readFileSync(join(P, "SCRIPT.md"), "utf8").split("\n")) {
  const h = l.match(/^#{2,3}\s+.*\(Frame (\d+)\)/i); if (h) { cur = { frame: +h[1], text: "" }; lines.push(cur); continue; }
  const m = l.match(/^(?: {4,}|\t)(.+)$/); if (cur && m) cur.text += (cur.text ? " " : "") + m[1].trim();
}
mkdirSync(join(P, "assets/voice"), { recursive: true });
const voices = [];
for (let i = 0; i < lines.length; i++) {
  const { frame, text } = lines[i]; if (!text) continue;
  const body = { text, model_id: "eleven_multilingual_v2", language_code: "ko",
    voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.15, use_speaker_boost: true, speed },
    previous_text: lines[i - 1]?.text, next_text: lines[i + 1]?.text };
  let r;
  for (let a = 0; a < 3; a++) {
    r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`, { method: "POST", headers: H, body: JSON.stringify(body) });
    if (r.ok) break; console.error("retry", frame, r.status, (await r.text()).slice(0, 200)); await new Promise((s) => setTimeout(s, 2000 * (a + 1)));
  }
  if (!r.ok) throw new Error("TTS failed frame " + frame);
  const j = await r.json();
  const id = String(frame).padStart(2, "0");
  const mp3 = join(P, `assets/voice/${id}.mp3`), wav = join(P, `assets/voice/${id}.wav`);
  writeFileSync(mp3, Buffer.from(j.audio_base64, "base64"));
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", mp3, "-ar", "44100", "-ac", "1", wav]);
  const dur = +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).toString().trim();
  const al = j.alignment; const words = []; let w = null;
  al.characters.forEach((c, k) => {
    if (/\s/.test(c)) { if (w) { words.push(w); w = null; } return; }
    if (!w) w = { text: "", start: al.character_start_times_seconds[k], end: 0 };
    w.text += c; w.end = al.character_end_times_seconds[k];
  });
  if (w) words.push(w);
  voices.push({ frame, path: `assets/voice/${id}.wav`, duration_s: +dur.toFixed(3),
    words: words.map((x, n) => ({ id: `w${n}`, text: x.text, start: +x.start.toFixed(3), end: +x.end.toFixed(3) })) });
  console.log(`frame ${id}: ${dur.toFixed(2)}s, ${words.length} words`);
}
const metaPath = join(P, "audio_meta.json");
const prev = existsSync(metaPath) ? JSON.parse(readFileSync(metaPath, "utf8")) : {};
writeFileSync(metaPath, JSON.stringify({ bgm: prev.bgm ?? null, bgm_pending: false, voices, sfx: prev.sfx ?? [] }, null, 2));
console.log(`voice ${VOICE} · total ${voices.reduce((s, v) => s + v.duration_s, 0).toFixed(2)}s → ${metaPath}`);
