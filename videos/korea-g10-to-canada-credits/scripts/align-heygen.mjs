// node scripts/align-heygen.mjs → assets/voice/<id>-heygen.align.json (ElevenLabs forced alignment)
import { readFileSync, writeFileSync } from "node:fs";
const TEXT = {
  intro: "안녕하세요, 에이에이캐나다입니다. 고1 마치고 캐나다로 가면 졸업까지 어떻게 될까요? BC와 온타리오를 비교해 드릴게요.",
  outro: "우리 아이 성적표로는 어느 주가 더 유리할지, 에이에이캐나다에서 일대일로 확인해 보세요. 감사합니다.",
};
for (const [id, text] of Object.entries(TEXT)) {
  const fd = new FormData();
  fd.append("file", new Blob([readFileSync(`assets/voice/${id}-heygen.mp3`)], { type: "audio/mpeg" }), `${id}.mp3`);
  fd.append("text", text);
  const res = await fetch("https://api.elevenlabs.io/v1/forced-alignment", { method: "POST", headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY }, body: fd });
  if (!res.ok) { console.error(id, res.status, await res.text()); process.exit(1); }
  const j = await res.json();
  const chars = j.characters.map((c) => c.text);
  writeFileSync(`assets/voice/${id}-heygen.align.json`, JSON.stringify({ characters: chars, character_start_times_seconds: j.characters.map((c) => c.start), character_end_times_seconds: j.characters.map((c) => c.end) }));
  console.log(id, chars.join(""), j.characters[0].start, j.characters.at(-1).end);
}
