#!/usr/bin/env node
// Generates the HyperFrames projects for the EMSB package from ONE timing file (timing.json).
//   node build.mjs              -> longform + all shorts
//   node build.mjs longform     -> videos/emsb-isp-longform/
//   node build.mjs shorts [ids] -> videos/emsb-isp-shorts/<id>/
// Captions come verbatim from plans/emsb-isp-2027/SCRIPT.txt / SHORTS_SCRIPT.txt.
import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync, rmSync } from "node:fs";
import { dirname, resolve, relative, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseLongform, parseShorts } from "./lib/script.mjs";
import * as K from "./lib/components.mjs";

const KIT = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(KIT, "../..");
const PLAN = join(REPO, "plans/emsb-isp-2027");
const ASSETS = join(PLAN, "assets");
const AA_LOGO = join(REPO, "plans/yeongyu-montreal-longform/assets/aa-canada-logo-transparent.png");
const HF_VERSION = "0.8.185";
const timing = JSON.parse(readFileSync(join(KIT, "timing.json"), "utf8"));
const r3 = (v) => Math.round(v * 1000) / 1000;
const rel = (from, to) => relative(from, to).split("\\").join("/");

// ---------- caption text ----------
const UNIT = "(?:퍼센트|개월|학년도|학년|년치|년|주|세|명|곳|월|일|점|번|시간|달러|원|%)";
const NUM_RE = new RegExp(`\\d[\\d,.]*(?:-\\d+)*(?:[만천백]\\s?\\d*)*(?:\\s?[일이삼사오육칠팔구십백]+(?=\\s?달러))?\\s?${UNIT}?`, "g");
const highlight = (s) => K.esc(s).replace(NUM_RE, (m) => `<span class="n">${m}</span>`);

/** Split a sentence into caption chunks of <= max chars, preferring comma boundaries. */
function chunk(sentence, max) {
  if (sentence.length <= max) return [sentence];
  const parts = sentence.split(/(?<=,)\s+/);
  const out = [];
  let cur = "";
  for (const p of parts) {
    if (!cur) cur = p;
    else if ((cur + " " + p).length <= max) cur += " " + p;
    else { out.push(cur); cur = p; }
  }
  if (cur) out.push(cur);
  // still too long -> split on spaces
  return out.flatMap((c) => {
    if (c.length <= max) return [c];
    const words = c.split(" "), res = [];
    let line = "";
    const n = Math.ceil(c.length / max), target = c.length / n;
    for (const w of words) {
      if (line && (line + " " + w).length > target + 4) { res.push(line); line = w; }
      else line = line ? line + " " + w : w;
    }
    if (line) res.push(line);
    return res;
  });
}

/** Sentence start/end times inside a scene (seconds from scene start). */
function sentenceTimes(sentences, sc, D) {
  const start = timing.lead, end = D - timing.gap - timing.tail;
  if (Array.isArray(sc.cues) && sc.cues.length === sentences.length) {
    const s = sc.cues.map(Number);
    return { starts: s, ends: s.map((v, i) => (i + 1 < s.length ? s[i + 1] : end)), end };
  }
  const w = sentences.map((x) => x.length + 6);
  const total = w.reduce((a, b) => a + b, 0);
  const starts = [], ends = [];
  let t = start;
  for (const wi of w) { starts.push(t); t += ((end - start) * wi) / total; ends.push(t); }
  return { starts, ends, end };
}

function makeCtx({ t0, D, times, projDir, isStatic = false }) {
  const T = (spec) => {
    if (typeof spec === "number") return t0 + spec;
    const m = String(spec).match(/^(c(\d+)(?:@([\d.]+))?|end)((?:[+-][\d.]+)*)$/);
    if (!m) throw new Error(`bad cue spec "${spec}"`);
    let v;
    if (m[1] === "end") v = D;
    else {
      const i = +m[2];
      if (i >= times.starts.length) throw new Error(`cue c${i} out of range (${times.starts.length} sentences)`);
      v = times.starts[i] + (m[3] ? (times.ends[i] - times.starts[i]) * +m[3] : 0);
    }
    for (const o of m[4].match(/[+-][\d.]+/g) ?? []) v += +o;
    return t0 + Math.max(0, Math.min(D - 0.05, v));
  };
  return { T, D, t0, static: isStatic, asset: (f) => stage(projDir, join(ASSETS, f), `assets/${f}`) };
}

function captions(sentences, times, t0, D, max) {
  const caps = [];
  sentences.forEach((s, i) => {
    const parts = chunk(s, max);
    const len = parts.reduce((a, p) => a + p.length, 0);
    let t = times.starts[i];
    const span = times.ends[i] - times.starts[i];
    parts.forEach((p) => { caps.push({ start: t, html: highlight(p) }); t += (span * p.length) / len; });
  });
  return caps.map((c, i) => ({ ...c, start: r3(t0 + c.start), end: r3(t0 + (i + 1 < caps.length ? caps[i + 1].start : D)) }));
}

// Copy a source file into <projDir>/_kit/<dest> (HyperFrames only serves files inside the project).
function stage(projDir, src, dest) {
  const out = join(projDir, "_kit", dest);
  mkdirSync(dirname(out), { recursive: true });
  copyFileSync(src, out);
  return `_kit/${dest}`;
}
function stageRuntime(projDir) {
  rmSync(join(projDir, "_kit"), { recursive: true, force: true });
  for (const f of ["BlackHanSans", "NotoSansKR-400", "NotoSansKR-700", "NotoSansKR-900"]) stage(projDir, join(KIT, "fonts", `${f}.woff2`), `fonts/${f}.woff2`);
  stage(projDir, join(KIT, "runtime/gsap.min.js"), "gsap.min.js");
  stage(projDir, AA_LOGO, "assets/aa-canada-logo.png");
}

// ---------- page ----------
function css(projDir) {
  return readFileSync(join(KIT, "runtime/emsb.css"), "utf8").replace(/url\("\.\.\/fonts\//g, 'url("_kit/fonts/');
}

function page({ projDir, id, W, H, fmt, total, body, isStatic = false }) {
  const runtime = "_kit";
  return `<!doctype html>
<!-- GENERATED by videos/emsb-isp-kit/build.mjs — edit the kit (content/*.mjs, timing.json), not this file. -->
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=${W}, height=${H}" />
<script src="${runtime}/gsap.min.js"></script>
<style>
html, body { width: ${W}px; height: ${H}px; }
${css(projDir)}
</style>
</head>
<body>
<div id="root" class="${fmt}" data-composition-id="${id}" data-start="0" data-width="${W}" data-height="${H}" data-fps="${timing.fps}" data-duration="${r3(total)}">
${body}
<img class="aalogo" src="_kit/assets/aa-canada-logo.png" alt="AA Canada" />
</div>
${isStatic ? `<script>window.__timelines["${id}"] = gsap.timeline({ paused: true });</script>` : `<script>
${readFileSync(join(KIT, "runtime/emsb-runtime.js"), "utf8")}</script>`}
</body>
</html>
`;
}

function writeProject(projDir, name, html) {
  mkdirSync(projDir, { recursive: true });
  writeFileSync(join(projDir, "index.html"), html);
  const hj = join(projDir, "hyperframes.json");
  if (!existsSync(hj))
    writeFileSync(hj, JSON.stringify({ $schema: "https://hyperframes.heygen.com/schema/hyperframes.json", paths: { blocks: "compositions", components: "compositions/components", assets: "assets" }, media: { autoProxy: true } }, null, 2) + "\n");
  const pj = join(projDir, "package.json");
  if (!existsSync(pj))
    writeFileSync(pj, JSON.stringify({ name, private: true, type: "module", scripts: {
      check: `npx --yes hyperframes@${HF_VERSION} check`,
      render: `npx --yes hyperframes@${HF_VERSION} render --quality looks --output out.mp4`,
    } }, null, 2) + "\n");
}

const audioTag = (projDir, id, sc, t0) =>
  sc.audio ? `<audio id="vo-${id}" src="${stage(projDir, join(REPO, sc.audio), `audio/${id}.m4a`)}" data-start="${r3(t0)}" data-duration="${r3(sc.audioDuration)}" data-track-index="8"></audio>` : "";

const capHtml = (caps, cls = "") =>
  caps.map((c, i) => `<div class="cap clip ${cls}" data-start="${c.start}" data-duration="${r3(c.end - c.start)}" data-track-index="5"><div class="cap-in" data-a="cap" data-t="${c.start}">${c.html}</div></div>`).join("\n");

// Upload text drafts are copied next to each video (NOT into a publish queue, no READY file).
// Longform: chapter timestamps are filled from the actual scene starts.
const mmss = (t) => `${String(Math.floor(t / 60)).padStart(2, "0")}:${String(Math.floor(t % 60)).padStart(2, "0")}`;
function writeUploadText(projDir, name, chapters) {
  const src = join(PLAN, "uploads", name);
  if (!existsSync(src)) return;
  let lines = readFileSync(src, "utf8").split("\n");
  if (chapters) {
    const i = lines.findIndex((l) => l.startsWith("(챕터 타임스탬프"));
    if (i > 0) {
      lines.splice(i, 1);
      chapters.slice(1).forEach((c, k) => { if (lines[i + k]?.trim()) lines[i + k] = `${mmss(c.start)} ${lines[i + k].trim()}`; });
    }
  }
  writeFileSync(join(projDir, "upload-text.txt"), lines.join("\n"));
}

// ---------- longform ----------
async function buildLongform() {
  const { scenes, SOURCE, thumbnail } = await import("./content/longform.mjs");
  const projDir = join(REPO, "videos/emsb-isp-longform");
  const script = parseLongform(join(PLAN, "SCRIPT.txt"));
  stageRuntime(projDir);
  let t0 = 0;
  const parts = [], chapters = [];
  for (const s of scenes) {
    const sc = timing.longform[s.id];
    const D = +sc.duration, sentences = script[s.id];
    const times = sentenceTimes(sentences, sc, D);
    const ctx = makeCtx({ t0, D, times, projDir });
    const foot = (s.foot ?? [SOURCE]).map((f) => `<div>${K.md(f)}</div>`).join("");
    parts.push(`<section id="${s.id}" class="scene clip" data-start="${r3(t0)}" data-duration="${r3(D)}" data-track-index="1">
<div class="stage"${K.anim(ctx, "drift", 0, { d: D })}>${s.render(ctx)}</div>
${s.chapter ? K.chapter(ctx, ...s.chapter) : ""}
<div class="foot"${s.foot ? ' style="bottom:14px"' : ""}>${foot}</div>
${audioTag(projDir, s.id, sc, t0)}
</section>
${capHtml(captions(sentences, times, t0, D, 50), s.foot ? "capup" : "")}`);
    chapters.push({ id: s.id, start: r3(t0), title: s.chapter ? s.chapter.join(" ") : "오프닝" });
    t0 += D;
  }
  const html = page({ projDir, id: "emsb-longform", W: 1920, H: 1080, fmt: "f169", total: t0, body: parts.join("\n") });
  writeProject(projDir, "emsb-isp-longform", html);
  writeFileSync(join(projDir, "chapters.json"), JSON.stringify({ total: r3(t0), chapters }, null, 2) + "\n");
  writeUploadText(projDir, "emsb_longform_upload-text.txt", chapters);
  if (thumbnail) {
    const td = join(projDir, "thumbnail-src");
    stageRuntime(td);
    const ctx = makeCtx({ t0: 0, D: 1, times: { starts: [0], ends: [1] }, projDir: td, isStatic: true });
    writeProject(td, "emsb-longform-thumb", page({ projDir: td, id: "emsb-longform-thumb", W: 1280, H: 720, fmt: "f169 thumb", total: 1, body: thumbnail(ctx), isStatic: true }));
  }
  console.log(`longform: ${scenes.length} scenes, ${r3(t0)}s -> ${rel(REPO, projDir)}`);
}

// ---------- shorts ----------
async function buildShorts(only) {
  const { shorts, render, cover } = await import("./content/shorts.mjs");
  const script = parseShorts(join(PLAN, "SHORTS_SCRIPT.txt"));
  for (const sh of shorts) {
    if (only.length && !only.includes(sh.id)) continue;
    const projDir = join(REPO, "videos/emsb-isp-shorts", sh.id);
    const sc = timing.shorts[sh.id];
    const D = +sc.duration, sentences = script[sh.id];
    const times = sentenceTimes(sentences, sc, D);
    stageRuntime(projDir);
    const ctx = makeCtx({ t0: 0, D, times, projDir });
    const body = `<section id="sh-${sh.id}" class="scene clip" data-start="0" data-duration="${r3(D)}" data-track-index="1">
${render(ctx, sh)}
${audioTag(projDir, sh.id, sc, 0)}
</section>
${capHtml(captions(sentences, times, 0, D, 30))}`;
    writeUploadText(projDir, `emsb_sh_${sh.id}_upload-text.txt`);
    writeProject(projDir, `emsb-sh-${sh.id}`, page({ projDir, id: `emsb-sh-${sh.id}`, W: 1080, H: 1920, fmt: "f916", total: D, body }));
    const td = join(projDir, "cover-src");
    stageRuntime(td);
    const cctx = makeCtx({ t0: 0, D: 1, times: { starts: [0], ends: [1] }, projDir: td, isStatic: true });
    writeProject(td, `emsb-sh-${sh.id}-cover`, page({ projDir: td, id: `emsb-sh-${sh.id}-cover`, W: 1080, H: 1920, fmt: "f916", total: 1, body: cover(cctx, sh), isStatic: true }));
    console.log(`short ${sh.id}: ${D}s, ${sentences.length} sentences -> ${rel(REPO, projDir)}`);
  }
}

const [what = "all", ...rest] = process.argv.slice(2);
if (what === "all" || what === "longform") await buildLongform();
if (what === "all" || what === "shorts") await buildShorts(rest);
