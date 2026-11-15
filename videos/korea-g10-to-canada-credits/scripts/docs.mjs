// node scripts/docs.mjs → STORYBOARD.md, SCRIPT.md, boards/storyboard.html (scenes.mjs 기준)
import { writeFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { SCENES, TOTAL } from "./scenes.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const fmt = (n) => (Number.isInteger(n) ? `${n}` : n.toFixed(1));
const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, "0")}`;
const stills = readdirSync(join(ROOT, "boards/stills")).filter((f) => f.startsWith("frame-")).sort();

// STORYBOARD.md
let md = `---
format: 1920x1080
duration: ${TOTAL}s
message: "한국 고1 수료 후 캐나다 11학년 편입: BC는 인정 범위가 좁아 핵심 과목을 현지에서 2년, 온타리오는 교장 재량 인정 후 최소 14학점"
arc: 인트로(대표님) → 졸업 요건 → 한국 학점 인정 → 캐나다 학점 취득 → 비교 → 주의 → 아웃트로(대표님)
audience: 캐나다 조기유학·자녀 편입을 검토하는 한국 학부모
mode: collaborative
---

`;
SCENES.forEach((s, i) => {
  md += `## Frame ${i + 1} — ${s.title} (${fmt(s.start)}-${fmt(s.start + s.dur)}s)

- act: ${s.act}
- status: built
- src: compositions/${s.id}.html
- duration: ${s.dur}s
- poster: ${fmt(s.dur / 2)}
- transition_in: ${i === 0 ? "cut" : "push"}
- voiceover: ${s.vo}
- reads: ${s.reads}
- sound: ${s.sound}

`;
});
writeFileSync(join(ROOT, "STORYBOARD.md"), md);

// SCRIPT.md (ElevenLabs 본편 내레이션)
let sc = `# 내레이션 대본 (본편) — ElevenLabs

- 음성: "아홉번째 자연톤 (10-18 촬영 음성)" · voice_id \`S2nra0Bd5UeFVzGK3oaH\`
- 모델: Eleven v4 (\`eleven_v4\`)
- 설정: stability 0.8 · similarity_boost 0.75
- 규칙: 각 문단 앞 [calm] 태그 · "AA Canada"는 "에이에이캐나다"로 표기
- 인트로·아웃트로 음성은 HeyGen 영상에 포함 (HEYGEN_SCRIPT.md)
- 문단 하나 = 장면 하나. 실제 음성 길이가 나오면 장면 길이를 그에 맞춥니다.

`;
for (const s of SCENES) {
  if (s.layout === "avatar") continue;
  sc += `## ${s.id} — ${s.title} (${mmss(s.start)}~${mmss(s.start + s.dur)})\n\n${s.vo}\n\n`;
}
writeFileSync(join(ROOT, "SCRIPT.md"), sc);

// boards/storyboard.html
const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;");
let lastAct = "";
const frames = SCENES.map((s, i) => {
  const act = s.act !== lastAct ? `<section class="act">${esc(s.act)}</section>` : "";
  lastAct = s.act;
  const img = stills.find((f) => f.startsWith(`frame-${String(i).padStart(2, "0")}-`));
  return `${act}
<div class="frame">
  <img src="stills/${img}" alt="" />
  <div class="title">${String(i + 1).padStart(2, "0")}: ${esc(s.title)}</div>
  <div class="time">${fmt(s.start)} to ${fmt(s.start + s.dur)}s</div>
  <p class="words"><b>내레이션</b> ${esc(s.vo)}</p>
  <p class="words"><b>화면</b> ${esc(s.reads)}</p>
  <p class="words"><b>소리</b> ${esc(s.sound)}</p>
</div>`;
}).join("\n");

const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>BC vs 온타리오 학점 스토리보드</title>
<style>
  body { margin: 0; background: #F2F4F7; color: #16202B; font-family: Inter, "Pretendard", system-ui, sans-serif; }
  header { padding: 40px 48px 8px; }
  h1 { margin: 0; font-size: 28px; }
  header p { margin: 8px 0 0; color: #4A5562; font-size: 15px; line-height: 1.6; }
  main { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 24px; padding: 24px 48px 64px; }
  .act { grid-column: 1 / -1; font-size: 20px; font-weight: 800; margin-top: 16px; }
  .frame { background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 16px rgba(16,32,48,.08); padding-bottom: 14px; }
  .frame img { width: 100%; display: block; aspect-ratio: 16/9; }
  .title { font-weight: 800; font-size: 17px; padding: 12px 16px 0; }
  .time { color: #6B7682; font-size: 13px; padding: 2px 16px 4px; }
  .words { font-size: 14px; line-height: 1.55; margin: 6px 16px 0; color: #2B3440; }
  .words b { color: #1F5FAD; margin-right: 6px; }
</style>
</head>
<body>
<header>
  <h1>한국 고1 → 캐나다 졸업장: BC vs 온타리오 (스토리보드)</h1>
  <p>16:9 · 약 ${mmss(TOTAL)} · 정지 화면은 각 장면의 완성 상태(애니메이션 전). 인트로·아웃트로의 둥근 창은 HeyGen 대표님 영상 자리입니다.<br/>
  블록 색: 초록/파랑 진한 칸 = 필수 · 연한 칸 = 선택 · 빗금 = 한국 학점 인정 · 빨간 자물쇠 = BC 현지 수강 필수 · 테두리만 = 온타리오 현지 이수 · G11/G12 = 이수 학년</p>
</header>
<main>
${frames}
</main>
</body>
</html>
`;
writeFileSync(join(ROOT, "boards/storyboard.html"), html);
console.log("ok", stills.length, "stills");
