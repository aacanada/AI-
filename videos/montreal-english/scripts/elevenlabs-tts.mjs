#!/usr/bin/env node
// elevenlabs-tts.mjs — narrate SCRIPT.md with the saved ElevenLabs voice.
//
// Uses the /with-timestamps endpoint so word timings come from the exact script
// text (Whisper re-transcription mangles Korean). Writes assets/voice/NN.wav per
// line plus audio_meta.json in the frame-keyed shape captions.mjs /
// assemble-index.mjs consume.
//
//   ELEVENLABS_API_KEY=… ELEVENLABS_VOICE_ID=… node scripts/elevenlabs-tts.mjs [--only 03,05]

import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { join, resolve } from "node:path";

const ROOT = resolve(new URL("..", import.meta.url).pathname);
const KEY = process.env.ELEVENLABS_API_KEY;
const VOICE = process.env.ELEVENLABS_VOICE_ID;
if (!KEY || !VOICE) throw new Error("ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID must be set");

const MODEL = "eleven_multilingual_v2";
const SETTINGS = { stability: 0.65, similarity_boost: 0.8, style: 0.1, use_speaker_boost: true, speed: 1.0 };

const onlyIdx = process.argv.indexOf("--only");
const only = onlyIdx > 0 ? new Set(process.argv[onlyIdx + 1].split(",")) : null;

// Same parse as the workflow's audio adapter: `## … (Frame N)` + indented spoken text.
function parseScript(md) {
  const out = [];
  let cur = null;
  const flush = () => cur && cur.text.trim() && out.push(cur);
  for (const line of md.split(/\r?\n/)) {
    const h = line.match(/^#{2,3}\s+.*?\(frame\s+(\d+)\)/i);
    if (h) {
      flush();
      cur = { frame: Number(h[1]), text: "" };
      continue;
    }
    if (!cur || /^\s*\*\*/.test(line)) continue;
    const m = line.match(/^(?: {4,}|\t)(.+)$/);
    if (m) cur.text += (cur.text ? " " : "") + m[1].trim();
  }
  flush();
  return out.map((l) => ({ ...l, text: l.text.replace(/^"|"$/g, "") }));
}

// Character alignment → whitespace-delimited words.
function toWords(al) {
  const words = [];
  let cur = null;
  al.characters.forEach((ch, i) => {
    if (/\s/.test(ch)) {
      if (cur) words.push(cur);
      cur = null;
      return;
    }
    const s = al.character_start_times_seconds[i];
    const e = al.character_end_times_seconds[i];
    if (!cur) cur = { text: ch, start: s, end: e };
    else {
      cur.text += ch;
      cur.end = e;
    }
  });
  if (cur) words.push(cur);
  return words.map((w, i) => ({ id: `w${i}`, text: w.text, start: +w.start.toFixed(3), end: +w.end.toFixed(3) }));
}

const pad2 = (n) => String(n).padStart(2, "0");
const lines = parseScript(readFileSync(join(ROOT, "SCRIPT.md"), "utf8"));
const metaPath = join(ROOT, "audio_meta.json");
const prev = existsSync(metaPath) ? JSON.parse(readFileSync(metaPath, "utf8")) : { voices: [] };
const voices = new Map(prev.voices.map((v) => [v.frame, v]));
mkdirSync(join(ROOT, "assets/voice"), { recursive: true });

for (const [i, line] of lines.entries()) {
  const id = pad2(line.frame);
  if (only && !only.has(id)) continue;
  const body = {
    text: line.text,
    model_id: MODEL,
    voice_settings: SETTINGS,
    previous_text: lines[i - 1]?.text,
    next_text: lines[i + 1]?.text,
  };
  const res = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`,
    { method: "POST", headers: { "xi-api-key": KEY, "Content-Type": "application/json" }, body: JSON.stringify(body) },
  );
  if (!res.ok) throw new Error(`line ${id}: ElevenLabs ${res.status} ${await res.text()}`);
  const data = await res.json();
  const mp3 = join(ROOT, `assets/voice/${id}.mp3`);
  const wav = join(ROOT, `assets/voice/${id}.wav`);
  writeFileSync(mp3, Buffer.from(data.audio_base64, "base64"));
  const ff = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-i", mp3, "-ar", "44100", "-ac", "1", wav]);
  if (ff.status !== 0) throw new Error(`line ${id}: ffmpeg failed`);
  rmSync(mp3);
  const dur = Number(
    spawnSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).stdout.toString(),
  );
  const words = toWords(data.alignment);
  voices.set(line.frame, { frame: line.frame, path: `assets/voice/${id}.wav`, duration_s: +dur.toFixed(3), words });
  console.log(`✓ voice ${id}: ${dur.toFixed(2)}s, ${words.length} words`);
}

const meta = { bgm: null, bgm_pending: false, voices: [...voices.values()].sort((a, b) => a.frame - b.frame), sfx: prev.sfx ?? [] };
writeFileSync(metaPath, JSON.stringify(meta, null, 2));
const total = meta.voices.reduce((a, v) => a + v.duration_s, 0);
console.log(`✓ audio_meta.json — ${meta.voices.length} lines, ${total.toFixed(1)}s narration`);
