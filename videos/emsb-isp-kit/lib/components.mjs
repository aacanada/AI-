// Reusable visual components (HTML strings). Every timing argument is a cue spec resolved by ctx.T():
//   number  -> seconds from scene start      "c3"     -> start of sentence 3
//   "c3+0.5" / "c3-0.4" -> offset from cue   "c3@0.5" -> halfway through sentence 3
//   "end-4" -> 4 s before scene end
// Animations are declared with data-a/data-t and played by runtime/emsb-runtime.js.

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const px = (v) => (typeof v === "number" ? `${Math.round(v * 100) / 100}px` : v);
const boxStyle = ([x, y, w, h], extra = "") =>
  `left:${px(x)};top:${px(y)};${w != null ? `width:${px(w)};` : ""}${h != null ? `height:${px(h)};` : ""}${extra}`;

// Inline markup for our own copy (trusted, may contain inline HTML): *text* -> red emphasis.
export const md = (s) => String(s).replace(/\*(.+?)\*/g, "<em>$1</em>");

export const fmtNum = (v, dec = 0) => (dec ? (+v).toFixed(dec) : Math.round(v).toLocaleString("en-US"));

export function anim(ctx, kind, at, o = {}) {
  if (at == null || ctx.static) return "";
  let s = ` data-a="${kind}" data-t="${ctx.T(at).toFixed(3)}"`;
  if (o.d != null) s += ` data-d="${(+o.d).toFixed(3)}"`;
  if (o.out != null) s += ` data-out="${ctx.T(o.out).toFixed(3)}"`;
  if (o.kb) s += ` data-kb="${o.kb}"`;
  if (o.to != null) s += ` data-to="${o.to}"`;
  if (o.dec) s += ` data-dec="${o.dec}"`;
  return s;
}

/** Wrap children in an absolutely positioned group that enters at `at` and (optionally) leaves at `out`. */
export const group = (ctx, { at = 0, out, a = "fade", box = [0, 0, "100%", "100%"] }, inner) =>
  `<div class="abs"${anim(ctx, a, at, { out })} style="${boxStyle(box)}">${inner}</div>`;

export const chapter = (ctx, label, text) =>
  `<div class="chapter"${anim(ctx, "drop", 0.1)}><b>${esc(label)}</b>${esc(text)}</div>`;

export const srctag = (ctx, text = "EMSB 2027-28 공식 자료 기준") => `<div class="srctag"${anim(ctx, "fade", 0.3)}>${esc(text)}</div>`;

export const title = (ctx, text, { box, size = 72, at = 0.2, a = "rise", out, align = "left", cls = "" }) =>
  `<div class="title ${cls}"${anim(ctx, a, at, { out })} style="${boxStyle(box, `font-size:${size}px;text-align:${align};`)}">${md(text)}</div>`;

export const text = (ctx, html, { box, size = 32, at = 0.3, a = "rise", out, cls = "kicker", style = "" }) =>
  `<div class="${cls}"${anim(ctx, a, at, { out })} style="${boxStyle(box, `font-size:${size}px;${style}`)}">${html}</div>`;

/** Big counting number. value: number, dec: decimals, pre/suf: unit text. */
export const bignum = (ctx, { box, value, dec = 0, pre = "", suf = "", label = "", size = 200, at, out, countAt, labelSize = 40 }) =>
  `<div class="bignum"${anim(ctx, "pop", at, { out })} style="${boxStyle(box)}">
    <div class="row" style="font-size:${size}px">${pre ? `<span class="unit">${esc(pre)}</span>` : ""}<span${anim(ctx, "count", countAt ?? at, { to: value, dec, d: 1.4 })}>${fmtNum(value, dec)}</span>${suf ? `<span class="unit">${esc(suf)}</span>` : ""}</div>
    ${label ? `<div class="lab" style="font-size:${labelSize}px">${md(label)}</div>` : ""}
  </div>`;

/** Chips row. items: [text | {t, at, cls}] ; staggered from `at` by `step` unless item has its own `at`. */
export const chips = (ctx, items, { box, at, step = 0.35, out, cls = "", justify = "flex-start" }) =>
  `<div class="chips" style="${boxStyle(box, `justify-content:${justify};`)}"${out != null ? anim(ctx, "fade", 0, { out }) : ""}>${items
    .map((it, i) => {
      const o = typeof it === "string" ? { t: it } : it;
      const t0 = o.at ?? (typeof at === "number" ? at + i * step : `${at}+${(i * step).toFixed(2)}`);
      return `<div class="chip ${o.cls ?? cls}"${anim(ctx, "pop", t0)}>${md(o.t)}</div>`;
    })
    .join("")}</div>`;

/** Card: {box, t (title), s (sub), big (number), count:{value,dec,pre,suf}, cls, at, a} */
export const card = (ctx, c) => {
  const big = c.count
    ? `<div class="cbig">${c.count.pre ? `<span style="font-size:.5em;color:var(--sub)">${esc(c.count.pre)} </span>` : ""}<span${anim(ctx, "count", c.countAt ?? c.at, { to: c.count.value, dec: c.count.dec, d: 1.3 })}>${fmtNum(c.count.value, c.count.dec)}</span>${c.count.suf ? `<span style="font-size:.5em">${esc(c.count.suf)}</span>` : ""}</div>`
    : c.big ? `<div class="cbig">${md(c.big)}</div>` : "";
  return `<div class="card ${c.cls ?? ""}"${anim(ctx, c.a ?? "rise", c.at, { out: c.out })} style="${boxStyle(c.box, c.style ?? "")}">
    ${c.pre ?? ""}${big}${c.t ? `<div class="ct"${c.tsize ? ` style="font-size:${c.tsize}px"` : ""}>${md(c.t)}</div>` : ""}${c.s ? `<div class="cs"${c.ssize ? ` style="font-size:${c.ssize}px"` : ""}>${md(c.s)}</div>` : ""}
  </div>`;
};

/**
 * Photo with crop + Ken Burns. src: asset file name; size: source [W,H]; crop: [sx,sy,sw,sh] (source px)
 * box: frame [x,y,w,h]. pins: [{x,y,label,at}] in source px (move with the Ken Burns).
 */
export function photo(ctx, { src, size, crop, box, kb = "in", at = 0, a = "fade", out, label, sub, bleed = false, radius, pins = [], kbFrom, kbDur, overlay = false }) {
  const [W, H] = size;
  const [sx, sy, sw, sh] = crop ?? [0, 0, W, H];
  const [, , fw, fh] = box;
  const s = Math.max(fw / sw, fh / sh);
  const cx = (sx + sw / 2) * s, cy = (sy + sh / 2) * s;
  const left = fw / 2 - cx, top = fh / 2 - cy;
  const kbStart = kbFrom ?? 0;
  const dur = kbDur ?? Math.max(1, ctx.D - kbStart);
  const pinHtml = pins
    .map((p) => `<div class="pin${p.side === "left" ? " pl" : ""}" style="left:${px(p.x * s)};top:${px(p.y * s)}"${anim(ctx, "pulse", p.at)}><i></i>${p.label ? `<span>${esc(p.label)}</span>` : ""}</div>`)
    .join("");
  return `<div class="photo${bleed ? " bleed" : ""}"${overlay ? " data-layout-allow-overlap" : ""}${anim(ctx, a, at, { out })} style="${boxStyle(box, radius != null ? `border-radius:${radius}px;` : "")}">
    <div class="inner"${kb ? anim(ctx, "kb", kbStart, { d: dur, kb }) : ""} style="left:${px(left)};top:${px(top)};width:${px(W * s)};height:${px(H * s)};transform-origin:${px(cx)} ${px(cy)};">
      <img src="${ctx.asset(src)}" alt="" />${pinHtml}
    </div>
    ${label ? `<div class="plabel">${esc(label)}${sub ? `<small>${md(sub)}</small>` : ""}</div>` : ""}
  </div>`;
}

/** Fee table. cols: header labels; rows: [{label, cells:[{value, at}] , at}] */
export const feeTable = (ctx, { box, cols, rows, at, rowH = 120, headH = 70, grid = "1.1fr 1fr 1fr", out }) =>
  `<div class="ftable"${anim(ctx, "rise", at, { out })} style="${boxStyle(box)}">
    <div class="tr th" style="grid-template-columns:${grid};height:${headH}px">${cols.map((c, i) => `<div class="td" style="text-align:${i ? "right" : "left"}">${esc(c)}</div>`).join("")}</div>
    ${rows
      .map(
        (r) => `<div class="tr"${anim(ctx, "left", r.at)} style="grid-template-columns:${grid};height:${rowH}px">
        <div class="td rowlab" style="font-size:1.25em">${md(r.label)}${r.sub ? `<div style="font-family:var(--body);font-weight:700;font-size:.62em;color:var(--muted)">${esc(r.sub)}</div>` : ""}</div>
        ${r.cells
          .map((c) => `<div class="td money"${anim(ctx, "pop", c.at)}><small>CAD</small><span${anim(ctx, "count", c.at, { to: c.value, d: 1.1 })}>${fmtNum(c.value)}</span></div>`)
          .join("")}
      </div>`
      )
      .join("")}
  </div>`;

/** Horizontal (or vertical) step flow. items: [{t, s, at}] */
export const flow = (ctx, items, { box, vertical = false, out }) =>
  `<div class="flow" style="${boxStyle(box, vertical ? "flex-direction:column;" : "")}"${out != null ? anim(ctx, "fade", 0, { out }) : ""}>${items
    .map(
      (it, i) =>
        `${i ? `<div class="arrow"${anim(ctx, "fade", it.at)} style="${vertical ? "justify-content:center;padding:4px 0;" : ""}">${vertical ? "↓" : "→"}</div>` : ""}<div class="step${i === items.length - 1 ? " last" : ""}"${anim(ctx, "pop", it.at)} style="${vertical ? "flex-direction:row;gap:20px;text-align:left;justify-content:flex-start;padding:16px 24px;" : ""}"><div class="sn"${vertical ? ' style="margin:0;flex:0 0 auto"' : ""}>${i + 1}</div><div><div class="st">${md(it.t)}</div>${it.s ? `<div class="ss">${md(it.s)}</div>` : ""}</div></div>`
    )
    .join("")}</div>`;

/** Checklist. items: [{t, at, hl}] */
export const checklist = (ctx, items, { box, cols = 1, out, size }) =>
  `<div class="checks" style="${boxStyle(box, `grid-template-columns:repeat(${cols},1fr);${size ? `font-size:${size}px;` : ""}`)}"${out != null ? anim(ctx, "fade", 0, { out }) : ""}>${items
    .map((it) => `<div class="check${it.hl ? " hl" : ""}"${anim(ctx, "left", it.at)}><i>${it.icon ?? "✓"}</i><span>${md(it.t)}</span></div>`)
    .join("")}</div>`;

export const quote = (ctx, { box, text, by, at, out, size }) =>
  `<div class="quote"${anim(ctx, "rise", at, { out })} style="${boxStyle(box)}"><div class="qm">“</div><div class="qt"${size ? ` style="font-size:${size}px"` : ""}>${md(text)}</div><div class="qb">${esc(by)}</div></div>`;

export const img = (ctx, { src, box, at, a = "fade", out, cls = "abs", style = "" }) =>
  `<img class="${cls}" src="${ctx.asset(src)}" alt=""${anim(ctx, a, at, { out })} style="${boxStyle(box, `object-fit:contain;${style}`)}" />`;

export const footnote = (ctx, text) => `<div class="foot">${md(text)}</div>`;

/** Rounded bar element (timeline segments, calendar bars). */
export const seg = (ctx, { box, text = "", at, bg = "var(--red)", color = "#fff", size = 30, a = "wipe", out, style = "" }) =>
  `<div class="seg"${anim(ctx, a, at, { out })} style="${boxStyle(box, `background:${bg};color:${color};font-size:${size}px;${style}`)}">${md(text)}</div>`;

export const tick = (ctx, { box, text, at, a = "fade", color = "var(--ink)", size, align = "center" }) =>
  `<div class="tick"${anim(ctx, a, at)} style="${boxStyle(box, `color:${color};text-align:${align};${size ? `font-size:${size}px;` : ""}`)}">${md(text)}</div>`;

/** AA Canada CTA / end card. */
export const cta = (ctx, { box, at, l1 = "AA Canada 무료 상담", l2 = "카카오톡 canlog", l3, l4, a = "pop" }) =>
  `<div class="cta" data-layout-allow-overlap${anim(ctx, a, at)} style="${boxStyle(box)}">
    <div class="c1">${esc(l1)}</div><div class="c2">${md(l2)}</div>${l3 ? `<div class="c3">${md(l3)}</div>` : ""}${l4 ? `<div class="c4">${md(l4)}</div>` : ""}
  </div>`;

export const blob = (ctx, { box, at = 0, color }) =>
  `<div class="blob"${anim(ctx, "float", at, { d: Math.max(1, ctx.D - 0.1) })} style="${boxStyle(box, color ? `background:${color};` : "")}"></div>`;

export { esc, boxStyle };
