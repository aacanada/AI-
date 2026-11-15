// node scripts/tts.mjs [id...] → assets/voice/<id>.mp3 + <id>.align.json (ElevenLabs with-timestamps)
import { writeFileSync, existsSync } from "node:fs";
import { SCENES } from "./scenes.mjs";
const VOICE = "S2nra0Bd5UeFVzGK3oaH";
const only = process.argv.slice(2);
for (const s of SCENES) {
  if (s.layout === "avatar") continue;
  if (only.length && !only.includes(s.id)) continue;
  if (!only.length && existsSync(`assets/voice/${s.id}.mp3`)) continue;
  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`, {
    method: "POST",
    headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ text: s.vo, model_id: "eleven_v4", voice_settings: { stability: 0.8, similarity_boost: 0.75 } }),
  });
  if (!res.ok) { console.error(s.id, res.status, await res.text()); process.exit(1); }
  const j = await res.json();
  writeFileSync(`assets/voice/${s.id}.mp3`, Buffer.from(j.audio_base64, "base64"));
  writeFileSync(`assets/voice/${s.id}.align.json`, JSON.stringify(j.normalized_alignment ?? j.alignment));
  console.log(s.id, "ok");
}
