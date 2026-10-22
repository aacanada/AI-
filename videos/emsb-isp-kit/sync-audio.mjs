#!/usr/bin/env node
// 원장님 녹음이 plans/emsb-isp-2027/audio/ 에 올라오면 실행합니다.
//   node sync-audio.mjs        -> 녹음 앞뒤 무음을 0.3s만 남기고 트림, 길이를 timing.json에 기록
//   node build.mjs             -> 기록된 길이(녹음 + 장면 사이 0.4s)로 HTML 재생성
// 녹음이 없는 장면은 timing.json의 임시 길이를 그대로 둡니다.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const KIT = dirname(fileURLToPath(import.meta.url));
const REPO = join(KIT, "../..");
const IN = join(REPO, "plans/emsb-isp-2027/audio");
const OUT = join(KIT, "audio-trimmed");
const file = join(KIT, "timing.json");
const timing = JSON.parse(readFileSync(file, "utf8"));
const keep = timing.lead; // seconds of silence kept at each end (brief: 0.3s)

const trim = (src, dst) =>
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", src, "-af",
    `silenceremove=start_periods=1:start_threshold=-40dB:start_silence=${keep},areverse,` +
    `silenceremove=start_periods=1:start_threshold=-40dB:start_silence=${keep},areverse`,
    "-ac", "1", "-c:a", "aac", "-b:a", "160k", dst]);
const duration = (f) =>
  +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString().trim();

mkdirSync(OUT, { recursive: true });
let n = 0;
for (const [group, prefix] of [["longform", "emsb_"], ["shorts", "emsb_sh_"]]) {
  for (const [id, sc] of Object.entries(timing[group])) {
    const src = join(IN, `${prefix}${id}.m4a`);
    if (!existsSync(src)) continue;
    const dst = join(OUT, `${prefix}${id}.m4a`);
    trim(src, dst);
    const d = Math.round(duration(dst) * 1000) / 1000;
    const old = sc.duration;
    Object.assign(sc, { audio: relative(REPO, dst).split("\\").join("/"), audioDuration: d, duration: Math.round((d + timing.gap) * 1000) / 1000 });
    delete sc.cues; // 이전 문장 타이밍은 새 녹음과 맞지 않으므로 지움(필요하면 다시 입력)
    console.log(`${group}/${id}: ${old}s -> ${sc.duration}s (audio ${d}s)`);
    n++;
  }
}
writeFileSync(file, JSON.stringify(timing, null, 2) + "\n");
console.log(n ? `${n} file(s) synced. Next: node build.mjs` : "no recordings found in plans/emsb-isp-2027/audio/");
