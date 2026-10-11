#!/usr/bin/env node
// Render AA Canada thumbnails from a JSON spec with Playwright (Chromium).
// usage: node make-thumbnail.mjs <spec.json> <outDir>
// spec: { "badge":"2026 연방 발표", "strike":"점수 경쟁", "title":["불어 *중하 수준*이면","쿼터 경쟁 끝"],
//         "big":"5,000", "bigUnit":"TO", "sub":"주정부 쿼터와 *별도*" }
// writes <outDir>/thumbnail-shorts.png (1080x1920) and <outDir>/thumbnail-youtube.png (1280x720)
import { readFileSync, mkdirSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require(require("node:child_process").execSync("npm root -g").toString().trim() + "/playwright")); }
const [specPath, outDir = "."] = process.argv.slice(2);
if (!specPath) { console.error("usage: make-thumbnail.mjs <spec.json> <outDir>"); process.exit(1); }
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const tpl = pathToFileURL(join(dirname(fileURLToPath(import.meta.url)), "..", "assets", "thumbnail.html")).href;
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch(process.env.PLAYWRIGHT_BROWSERS_PATH ? {} : {});
for (const [name, w, h] of [["thumbnail-shorts", 1080, 1920], ["thumbnail-youtube", 1280, 720]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto(tpl + "#" + encodeURIComponent(JSON.stringify({ ...spec, ...(spec[name] || {}), width: w, height: h })));
  await page.waitForSelector("body[data-ready='1']");
  const out = resolve(outDir, name + ".png");
  await page.screenshot({ path: out });
  console.log("✓", out);
  await page.close();
}
await browser.close();
