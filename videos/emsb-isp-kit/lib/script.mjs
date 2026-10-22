// Parse SCRIPT.txt / SHORTS_SCRIPT.txt so on-screen captions are always the script verbatim.
import { readFileSync } from "node:fs";

// Split on sentence punctuation followed by whitespace ("92.1" stays whole);
// re-join name initials such as "John F. Kennedy", "Lester B. Pearson".
const splitSentences = (para) =>
  para.split(/(?<=[.?!])\s+/).reduce((acc, s) => {
    if (acc.length && /(^|\s)[A-Z]\.$/.test(acc[acc.length - 1])) acc[acc.length - 1] += " " + s;
    else acc.push(s.trim());
    return acc;
  }, []).filter(Boolean);

export function parseScript(file, headerRe) {
  const out = {};
  let cur = null;
  for (const raw of readFileSync(file, "utf8").split(/\r?\n/)) {
    const line = raw.trim();
    const m = line.match(headerRe);
    if (m) { cur = out[m[1]] = []; continue; }
    if (!cur || !line || /^=+$/.test(line) || /^[A-Z]\. /.test(line)) continue;
    if (/^=+/.test(line)) { cur = null; continue; }
    cur.push(...splitSentences(line));
  }
  return out;
}

export const parseLongform = (file) => parseScript(file, /^emsb_(s\d\d)\.m4a/);
export const parseShorts = (file) => parseScript(file, /^--- emsb_sh_(\w+)\.m4a/);
