#!/usr/bin/env node
// ElevenLabs narration (voice "일곱번째") for the EMSB longform + shorts, in place of the owner's recording.
//   node tts.mjs                  -> every scene/short that has no mp3 yet
//   node tts.mjs s01 sh_fee       -> only these (forces regeneration)
//   node tts.mjs --dry            -> print TTS texts + character count, no API calls
// Writes plans/emsb-isp-2027/audio/emsb_<id>.mp3 (raw TTS), tts/emsb_<id>.json (alignment),
// audio-trimmed/emsb_<id>.m4a (0.3 s silence each side) and timing.json (duration, audio, cues).
// Captions stay the script's original text; only the spoken text is respelled (numbers, English names).
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { parseLongform, parseShorts } from "./lib/script.mjs";

const KIT = dirname(fileURLToPath(import.meta.url));
const REPO = join(KIT, "../..");
const PLAN = join(REPO, "plans/emsb-isp-2027");
const VOICE_NAME = "일곱번째";
const MODEL = "eleven_multilingual_v2";
const timingFile = join(KIT, "timing.json");
const timing = JSON.parse(readFileSync(timingFile, "utf8"));

// Spoken respellings, applied in order (specific before generic).
const SAY = [
  ["2027-28학년도", "이천이십칠, 이십팔 학년도"], ["2024-25학년도", "이천이십사, 이십오 학년도"],
  ["92.1퍼센트", "구십이 점 일 퍼센트"], ["02-567-4345", "공이, 오육칠, 사삼사오"],
  ["1만 5천 백칠십 달러", "만 오천백칠십 달러"], ["1만 2천 이십 달러", "만 이천이십 달러"], ["1만 2천 달러", "만 이천 달러"],
  ["6천 이백육십 달러", "육천이백육십 달러"], ["7천 팔백삼십오 달러", "칠천팔백삼십오 달러"],
  ["4천 9백1달러", "사천구백일 달러"], ["6천 3백68달러", "육천삼백육십팔 달러"],
  ["3만 5천 명", "삼만 오천 명"], ["1천 달러", "천 달러"], ["250에서 300달러", "이백오십에서 삼백 달러"],
  ["250달러", "이백오십 달러"], ["65달러", "육십오 달러"], ["1873년", "천팔백칠십삼 년"],
  ["12월 1일", "십이월 일일"], ["5월 31일", "오월 삼십일일"], ["9월 30일", "구월 삼십일"], ["2월 1일", "이월 일일"], ["6월 23일", "유월 이십삼일"],
  ["6주에서 20주", "육 주에서 이십 주"], ["24시간", "이십사 시간"], ["60점", "육십 점"], ["48년째", "사십팔 년째"], ["3년치", "삼 년치"],
  ["1, 2년", "일이 년"], ["7, 8학년", "칠, 팔 학년"],
  ["1학년은 만 6세, 7학년은 만 12세, 11학년은 만 16세", "일 학년은 만 여섯 살, 칠 학년은 만 열두 살, 십일 학년은 만 열여섯 살"],
  ["11학년", "십일 학년"], ["9학년", "구 학년"], ["7학년", "칠 학년"], ["5학년", "오 학년"], ["1학년", "일 학년"],
  ["10개월", "십 개월"], ["5개월", "오 개월"], ["4개월", "사 개월"], ["3개월", "삼 개월"],
  ["2주", "이 주"], ["1년", "일 년"], ["1위", "일 위"], ["1월", "일월"], ["2월", "이월"], ["9월", "구월"],
  ["8곳", "여덟 곳"], ["4곳", "네 곳"], ["3곳", "세 곳"], ["4번", "네 번"], ["0원", "영 원"],
  ["제2언어", "제 이 언어"], ["제3외국어", "제 삼 외국어"],
  ["English Montreal School Board", "잉글리시 몬트리올 스쿨 보드"], ["John F. Kennedy", "존 에프 케네디"],
  ["Laurier Macdonald", "로리에 맥도널드"], ["Lester B. Pearson", "레스터 비 피어슨"], ["LaurenHill Academy", "로렌힐 아카데미"],
  ["Marymount Academy International", "메리마운트 아카데미 인터내셔널"], ["Royal Vale", "로열 베일"], ["Westmount High", "웨스트마운트 하이"],
  ["Peel역", "필역"], ["McGill역", "맥길역"], ["St-Michel역", "생미셸역"], ["Côte-Vertu역", "코트베르튀역"],
  ["Villa-Maria역", "빌라마리아역"], ["Atwater역", "앳워터역"], ["Vendôme역", "방돔역"],
  ["True North", "트루 노스"], ["Eligibility", "엘리저빌리티"], ["AA Canada", "에이에이 캐나다"], ["canlog", "캔로그"],
  ["EMSB", "이엠에스비"], ["CAQ", "씨에이큐"], ["STEAM", "스팀"], ["NDG", "엔디지"], ["FACE", "페이스"], ["IB", "아이비"], ["AP", "에이피"],
];
const say = (s) => SAY.reduce((t, [a, b]) => t.split(a).join(b), s);

const jobs = [];
const L = parseLongform(join(PLAN, "SCRIPT.txt"));
for (const id of Object.keys(timing.longform)) jobs.push({ key: id, group: "longform", id, file: `emsb_${id}`, sentences: L[id] });
const S = parseShorts(join(PLAN, "SHORTS_SCRIPT.txt"));
for (const id of Object.keys(timing.shorts)) jobs.push({ key: `sh_${id}`, group: "shorts", id, file: `emsb_sh_${id}`, sentences: S[id] });

const args = process.argv.slice(2);
const dry = args.includes("--dry");
const only = args.filter((a) => !a.startsWith("--"));
const API = "https://api.elevenlabs.io/v1";
const headers = { "xi-api-key": process.env.ELEVENLABS_API_KEY ?? "", "content-type": "application/json" };

async function voiceId() {
  const r = await fetch(`${API}/voices`, { headers });
  if (!r.ok) throw new Error(`voices: HTTP ${r.status} ${await r.text()}`);
  const norm = (s) => s.replace(/\s+/g, "").replace(/^7/, "일곱");
  const voices = (await r.json()).voices;
  const v = voices.find((x) => norm(x.name) === norm(VOICE_NAME)) ?? voices[6];
  console.log(`voice: ${v.name} (${v.voice_id})`);
  return v.voice_id;
}

const probeDur = (f) => +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString().trim();

const todo = jobs.filter((j) => (only.length ? only.includes(j.key) : !existsSync(join(PLAN, "audio", `${j.file}.mp3`))));
const texts = todo.map((j) => {
  const parts = j.sentences.map(say);
  const leftovers = parts.join(" ").match(/[0-9A-Za-z]+/g);
  if (leftovers) console.warn(`${j.key}: not respelled -> ${[...new Set(leftovers)].join(", ")}`);
  return { ...j, parts, text: parts.join(" ") };
});
const chars = texts.reduce((a, t) => a + t.text.length, 0);
console.log(`${texts.length} job(s), ${chars} characters`);
if (dry) { for (const t of texts) console.log(`\n[${t.key}] ${t.text}`); process.exit(0); }

const vid = await voiceId();
mkdirSync(join(PLAN, "audio"), { recursive: true });
mkdirSync(join(KIT, "tts"), { recursive: true });
mkdirSync(join(KIT, "audio-trimmed"), { recursive: true });
for (const t of texts) {
  const r = await fetch(`${API}/text-to-speech/${vid}/with-timestamps?output_format=mp3_44100_128`, {
    method: "POST", headers, body: JSON.stringify({ text: t.text, model_id: MODEL }),
  });
  if (!r.ok) {
    console.error(`${t.key}: HTTP ${r.status} ${await r.text()}`);
    console.error("stopping (no fallback TTS). Re-run later for the remaining files.");
    break;
  }
  const res = await r.json();
  const mp3 = join(PLAN, "audio", `${t.file}.mp3`);
  writeFileSync(mp3, Buffer.from(res.audio_base64, "base64"));
  const al = res.alignment;
  writeFileSync(join(KIT, "tts", `${t.file}.json`), JSON.stringify({ voice: vid, model: MODEL, text: t.text, alignment: al }) + "\n");

  // sentence start offsets inside the TTS text -> times from the character alignment
  const starts = [];
  let off = 0;
  for (const p of t.parts) { starts.push(off); off += p.length + 1; }
  const ok = al && al.characters.length === t.text.length;
  const at = (i) => al.character_start_times_seconds[Math.min(i, al.characters.length - 1)];
  const nonSpace = al.characters.map((c, i) => (/\s/.test(c) ? null : i)).filter((i) => i != null);
  const sp0 = al.character_start_times_seconds[nonSpace[0]], sp1 = al.character_end_times_seconds[nonSpace[nonSpace.length - 1]];
  const keep = timing.lead, offset = sp0 - keep; // trimmed audio starts `keep` s before speech
  const m4a = join(KIT, "audio-trimmed", `${t.file}.m4a`);
  const pad = Math.max(0, -offset);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", mp3, "-af",
    `atrim=start=${Math.max(0, offset).toFixed(3)}:end=${(sp1 + timing.tail).toFixed(3)},asetpts=PTS-STARTPTS,adelay=${Math.round(pad * 1000)}:all=1,apad=pad_dur=${Math.max(0, timing.tail - 0.0).toFixed(2)}`,
    "-t", (sp1 - sp0 + keep + timing.tail).toFixed(3), "-ac", "1", "-c:a", "aac", "-b:a", "160k", m4a]);
  const d = Math.round(probeDur(m4a) * 1000) / 1000;
  const sc = timing[t.group][t.id];
  Object.assign(sc, {
    audio: relative(REPO, m4a).split("\\").join("/"), audioDuration: d, duration: Math.round((d + timing.gap) * 1000) / 1000,
    cues: ok ? starts.map((s) => Math.round((at(s) - offset) * 1000) / 1000) : undefined,
  });
  if (!ok) delete sc.cues;
  writeFileSync(timingFile, JSON.stringify(timing, null, 2) + "\n");
  console.log(`${t.key}: ${d}s audio, ${t.text.length} chars${ok ? "" : " (alignment length mismatch -> proportional captions)"}`);
}
