# Frame packet: 04-federal-5000

## Project inputs

- Project: /home/user/AI-/videos/french-nclc5-federal-quota
- Design tokens: /home/user/AI-/videos/french-nclc5-federal-quota/frame.md
- RULES_DIR: /root/.claude/skills/hyperframes-animation/rules

## Assigned storyboard block

## Frame 4 — 연방 5,000개 TO

- scene: "2026 연방정부" 아이브로우 아래 큰 숫자 5,000이 카운트업, "불어권 전용 TO" 라벨
- voiceover: "그런데 2026년, 연방정부가 중요한 발표를 했습니다. 불어를 하는 이민자를 위해, 연방 몫으로 5,000개의 정원을 따로 마련한 겁니다."
- duration: 9.567s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/04-federal-5000.html
- type: product_intro
- persuasion: Statistical proof + Concept announcement
- beat: Surprise + orientation
- blueprint: dataviz-countup (Reproduce)
- focal: the giant cobalt number "5,000" counting up
- roles: cream ground + faint cobalt radial bloom behind the number = background · "5,000" = foreground subject · eyebrow "2026 · 연방정부 발표" + label "불어권 전용 TO" = supporting

narrativeRole: 해결책의 주인공인 '연방 불어권 전용 5,000개 TO'를 숫자로 등장시킨다.
keyMessage: 연방이 불어권 전용으로 5,000개 TO를 따로 마련했다.


Scene 1 (0.0–4.2s): on "2026년"(0.5s) an eyebrow pill "2026 · 연방정부" springs in at upper third; on "중요한 발표"(2.5s) a headline "연방정부의 새 발표" per-word reveals beneath it.
Scene 2 (4.2–7.3s): on "불어를 하는 이민자를 위해"(4.3s) a cobalt-tinted card "불어 사용 이민자 전용" slides up into the middle; a soft cobalt glow blooms (`ambient-glow-bloom`).
Scene 3 (7.3–9.57s): on "5,000개의"(7.4s) the hero number counts 0 → 5,000 in cobalt, value-scaled so the type grows as it climbs (`counting-dynamic-scale`), centered at y≈880 near full width; on "따로 마련한"(8.4s) a label "개 · 연방 별도 정원(TO)" settles under it. Hold.

## Selected blueprint: dataviz-countup

# dataviz-countup — Data-Viz / Count-Up

**intent**: Make numbers and charts the hero — a count-up ring/number, a trend chart, a tilted stat/card grid — and traverse the data instruments with a camera that pushes THROUGH them (or scrolls across them) to land on one hero metric, so the data itself carries the argument.

**roles served**

- Problem (from `problem-dataviz-pushthrough`): quantifies the pain with real-looking instruments — a count-up ring → a trend chart → a stat grid — the camera pushing THROUGH each object into the next to dramatize a worsening / large-scale problem ("X% of people struggle with…").
- Product_Intro (from `product-intro-dataviz-scroll-reveal`): a confident "look at the result / the data" open — hard-cut from a hook word into a perspective-tilted grid of data-viz cards, then a hands-off camera scroll lands one glowing hero metric while a kinetic tagline assembles word-by-word.
- Hook (from `hook-counter-burst`): a cold-open hook on ONE dramatic statistic — the frame opens dark and empty, 3–5 thematic icons puncture in clustered at center, then the headline number EXPLODES upward in size as the icons fling outward to their marks (the count-up and the spread are one beat), closed by a slow camera lean-in. Kinetic from frame 1.
- Key_Feature (from dark-stat-scrub-montage): prove the feature with its own analytics — on a black canvas, kinetic headline beats alternate with self-drawing charts and a 3D-tilted dark dashboard that a cursor SCRUBS (tracking line + live tooltips), stitched by hard cuts and one zoom punch. The one variant where a cursor touches the data.
- Social_Proof (from `gauge-beat`): a single count-up instrument — radial gauge arc-draw + rapidly ticking metric + caption — embedded as ONE BEAT inside a kinetic-typography relay; entered and exited by element-level scale/blur push-throughs on a static frame. The instrument guest-stars; the relay itself belongs to kinetic-type-beats.

**duration**: ~4–12s (Hook ~4s · Product_Intro ~6s · dark-scrub-montage ~7.3–7.75s · Problem ~11–12s · gauge-beat ~2.5s inside a ~10.8s relay)

**shot structure** Data-viz field on `[bg color]` (dark or light, soft corner glows); `[gradient A→B]` brand stroke on charts/rings; clean sans-serif white/dark text; a continuous camera move runs underneath that traverses 2–3 data instruments and resolves on a hero metric. One instrument per beat; the camera carries the cut.

- Scene 1 (0.0–Xs): the first data instrument establishes centered — a `[stat]` reads as the hero. A bold center number COUNTS UP `[start]`→`[end]` while its transform scale grows to the static final type size, with `[stat label]` below; its paired graphic (a circular progress RING sweeping to `[pct]` with a `[gradient]` stroke, or a bar/fill) animates in on the SAME ease so number + graphic land as one beat. Supporting `[avatar/object]` elements pop in with spring overshoot into a scattered glowing orbit; a `[headline]` fades up. A very slow continuous camera zoom-in runs throughout.
- Scene 2 (Xs–Ys): the camera traverses to the next instrument and that instrument animates — a `[gradient]` trend line / area chart DRAWS left→right on grid lines (Problem), or off-center cards SCROLL away as the layout glides (Product_Intro). The arriving `[stat-2]` number counts up / the chart resolves.
- Scene 3 / Scene N (…–end): the camera lands the `[hero metric card]` (big number + label + delta + rising chart) in dead-center; a soft `[accent]` glow blooms behind it; the move reaches its peak then eases to a settled, slightly wider composition with the hero centered and supporting cards flanking it. HOLD on the final frame.

- Variant — Problem (push-THROUGH, count-up → trend → grid): Scene 1 is a centered circular progress ring + count-up center number with scattered glowing `[avatar/object]` orbit. Scene 2 is a fast camera PUSH-IN straight through the center of the ring (ring, number, orbiting elements scale up and fly out of frame) into a rounded `[card]` holding `[stat-2 header]` over a `[gradient]` line chart with grid lines + translucent area fill that draws left→right; camera pushes through then settles. Scene 3: camera PANS to a second `[card]` whose number counts up, holding a grid of the `[avatar/object]` elements — a subset dim/blur while the rest receive `[accent]` circular checkmark badges that SPRING-POP; camera settles to the end. The traversal is z-depth push-through between instruments.
- Variant — Product_Intro (scroll-to-hero + word-by-word tagline): a brief opener — Scene 0 (~0.0–0.85s): a full-frame `[hero-color orb]` with a bold white `[hook phrase]` over it; static shimmer, then HARD CUT. Scene 1 cuts to a slightly perspective-TILTED grid of `[data-viz / product cards]` (charts, heatmaps, stat cards with deltas + source footers) with `[tagline word 1]` centered; the grid begins SCROLLING (e.g. toward upper-left) with its tilt held. Scene 2: the grid keeps scrolling so the `[hero metric card]` glides into dead-center as off-center cards slide away; `[tagline word 1]` translates out and `[word 2]` rises in from a frame edge. Scene 3: hero card settles centered, `[accent]` glow blooms behind it, camera PUSHES IN slightly; `[word 2]` holds near it. Scene 4: `[word 2]` slides out, the final `[tagline word]` drops in from the opposite edge above the still-glowing hero, push-in peaks. Scene 5: overlay type clears, camera eases BACK OUT to a settled wider tilted composition — hero centered with glow, supporting cards flanking. The traversal is a hands-off camera SCROLL across a tilted card plane (no cursor, no clicks) + a one-word-at-a-time kinetic headline + push-in-then-out bookend.
- Variant — Key_Feature (dark-scrub-montage: kinetic beats × instruments, cut-stitched): on black, `[kinetic word]` beats ALTERNATE with data instruments; hard cuts stitch the beats and the camera is locked per beat — the traversal is a montage, not a continuous move. Beat A: a bold `[heading]` holds while a thick `[trend line]` DRAWS itself left→right inside a dark chart band, rising to break above the band's edge; at the peak a `[accent]` dot pops and a pill tooltip springs in, its label building to `[value + delta]`. Beat B: ONE fast zoom PUNCH lands a close-up, slightly 3D-tilted dark `[analytics dashboard]` (metric cards with deltas, translucent oversized numerals floating behind); a white cursor SCRUBS a chart — a vertical tracking line follows it and `[date: value]` tooltips read out live, then a second chart ACTIVATES with a color flip and its own scrubbing tooltip — while the tilted plane drifts gently sideways; quick pull-away/fade to black. Beat C: a `[glowing wave / typed line / impact word]` beat lands the closing stat LOCKUP — `[title]` + big `[stat]` counting up + `[green delta arrow + context line]` — and holds static to the end. Kinetic words between instruments scale up violently past the frame as element-level push-through transitions (no camera).
- Variant — Social_Proof (gauge-beat inside a relay): a static-camera kinetic-type relay hosts ONE instrument beat — thin concentric `[accent]` arcs radiate from center, a thick `[accent]` progress arc draws clockwise over them, a large `[metric]` rapidly ticks up to `[big value]` with a `[caption]` below; the group slowly scales up (element-level drift), then hard-cuts out to the next text beat. Entry/exit for every beat is scale-up-from-blur in / scale-up-and-blur-past-frame out — a fake push-through with no camera anywhere. Use when social proof is one number and the surrounding beats are typography.

**motion vocabulary** count-up number with transform-scale growth on the value; circular progress-ring sweep; growth bar / progress fill; gradient trend-line + area-fill left→right draw; spring-overshoot pop-in of scattered glowing avatar/object elements; perspective-tilted card grid; directional grid scroll (cards glide in/out of center); hero-card centering; soft accent glow bloom behind the hero; slow continuous zoom-in; fast camera push-IN / push-THROUGH the center of an instrument; lateral/vertical camera pan between cards; gentle push-in that peaks then eases back out to a wider settle; selective dim/blur of a subset + spring-pop checkmark badges; full-frame hook orb → hard cut; kinetic tagline assembled word-by-word (each word drops/rises from a frame edge, prior word slides out). Dark-scrub-montage additions: self-drawing chart line that breaks above its band; peak dot + pill tooltip spring-pop; cursor chart scrub with vertical tracking line + live date/value tooltip readouts; chart activation color flip; 3D-tilted dark dashboard plane with slow lateral drift; translucent oversized numerals floating behind cards; fast zoom punch-in; pull-away/fade-to-black beat exit; hard-cut beat stitching; kinetic word push-through (element scales up past the frame); typed line with blinking cursor; impact slam word + particle-dissolve punctuation; glowing wave draw; green delta arrow pop; stat lockup hold. Gauge-beat additions: concentric static arcs + thick clockwise progress-arc draw; rapid count-up tick; scale-up-from-blur entrance / scale-up-and-blur-past-frame exit (element-level fake push-through).

**rule mapping** (motion verb → `rules/<id>.md`)

- count-up number whose transform scale grows with the value → `counting-dynamic-scale` (primary text rule)
- circular progress-ring sweep (the ring fill) → `stat-bars-and-fills` (ring form) — its draw mechanics delegate to → `svg-path-draw`
- growth bars / progress fill paired beside a number → `stat-bars-and-fills` (primary data rule)
- gradient trend-line / area-chart left→right draw → `svg-path-draw` (a path/line draws itself)
- spring-overshoot pop-in of the avatar/object elements → `spring-pop-entrance` (elastic overshoot); the scattered-ring layout of glowing avatars/objects → `avatar-cloud-network`; if they keep drifting/orbiting → `orbit-3d-entry`
- spring-pop `[accent]` checkmark badges → `spring-pop-entrance`
- perspective-tilted card grid (tilt held static while content moves) → `3d-page-scroll`
- directional scroll across the tilted card plane (cards glide in/out of center) → `3d-page-scroll` (scroll) + `viewport-change` (lateral/vertical pan form)
- hero metric card centering (scroll/pan lands the target dead-center) → `coordinate-target-zoom` (target lands at viewport center) / `viewport-change`
- hard-cut from the hook orb into the grid → `scale-swap-transition`
- kinetic tagline assembled word-by-word → `kinetic-beat-slam` (one onset grid, distinct per-word entrances)
- slow continuous zoom-in + push-THROUGH the instruments + lateral/vertical pan between cards + push-in-then-out bookend → `multi-phase-camera` (see camera modifier)
- soft accent glow BLOOM behind the hero card → `ambient-glow-bloom` (un-triggered soft glow/bloom behind the static hero element — distinct from `press-release-spring`'s press-triggered glow and `asr-keyword-glow`'s word-timed envelope)
- selective dim/blur of a SUBSET of grid items (focus-falloff on the non-highlighted cards) → `depth-of-field-blur` (selective per-element blur/dim to spotlight the highlighted cards — the same focus-falloff rule used in `constellation-hub`)
- cursor chart scrub (cursor-tied vertical tracking line + live data readout in a tooltip) → `chart-scrub-readout` (the tracking line, tooltip pop, and seek-safe live value readout driven by cursor x)
- chart activation color flip (second chart lights up under the scrub) → `gsap-effects` (color/opacity chord at the scrub handoff — basic tween, no dedicated rule needed)
- 3D-tilted dashboard plane + slow lateral drift → `3d-page-scroll` (the tilt framing) + `sine-wave-loop` (the drift; keep amplitude tiny so the scrub stays legible)
- fast zoom punch-in to the dashboard → `multi-phase-camera` (one short aggressive push phase) aimed via `coordinate-target-zoom`; add `motion-blur-streak` at peak velocity
- kinetic word push-through / scale-up-and-blur-past-frame exit / scale-up-from-blur entrance → `kinetic-beat-slam` (the beat grammar) + `motion-blur-streak` (blur peaks at max speed, resolves at the settle — its entrance form runs the blur-in, its exit form the blow-past)
- typed line with blinking cursor → `discrete-text-sequence` + `context-sensitive-cursor` (square-wave blink)
- impact slam word → `kinetic-beat-slam`; its particle-dissolve punctuation → `particle-burst` (glyph→particles dissolve, deterministic)
- glowing wave draw → `svg-path-draw` (the draw) + `ambient-glow-bloom` (the glow envelope)
- green delta arrow pop / peak dot + pill tooltip → `spring-pop-entrance`
- concentric static arcs + clockwise progress-arc draw (gauge beat) → `stat-bars-and-fills` (ring form) → draw mechanics `svg-path-draw` (both already mapped above — the gauge is the existing ring with static concentric chrome behind it)

**camera modifier**: The camera is the through-line that traverses the data instruments — one camera wrapper sequenced by `multi-phase-camera`, with each stop targeted via `coordinate-target-zoom` onto the focal instrument/card.

- Problem — push-THROUGH: a slow continuous zoom-in (drift overlay) plus a fast PUSH-IN straight through the center of one instrument into the next (`multi-phase-camera`, Steady-push pattern), then a lateral/vertical PAN to the final card. Z-depth push-through is the signature (distinguishes it from a flat pan-tour).
- Product_Intro — scroll-to-hero + bookend push: a hands-off directional SCROLL across the tilted card plane (`3d-page-scroll` scroll / `viewport-change` pan) that lands the hero card center, then a gentle push-in that PEAKS and eases BACK OUT to a wider settle (`multi-phase-camera`, Bookend-pull pattern). No cursor, no clicks — the camera does the navigating.
- Key_Feature — montage-cut: the camera is NOT the through-line — hard cuts stitch the instrument beats, the frame is locked inside each beat, and exactly ONE fast zoom punch (`multi-phase-camera` single push phase + `coordinate-target-zoom`) lands the dashboard close-up; exits are pull-away/fade-to-black. Between instruments, ELEMENTS fake the push: kinetic words scale up past the frame (`kinetic-beat-slam` + `motion-blur-streak`). Gauge-beat form drops even the punch — fully static, all push-through element-level. Reach for this mode when the dialect is a dark rapid montage; the Problem/Product_Intro modes remain the default for a single continuous argument.

## Selected motion rule: ambient-glow-bloom

---
name: ambient-glow-bloom
description: Un-triggered soft radial glow that blooms in behind a hero element and holds with a bounded idle breathe, or a single-pass traveling sweep across a surface. No click, no word-sync — it just blooms. Finite, deterministic, seek-safe.
metadata:
  tags: glow, bloom, ambient, radial, sweep, hero, presence, finite, un-triggered
---

# Ambient Glow Bloom

A soft radial glow that **blooms in behind a hero element** (card, logo, metric) and holds, giving it presence. Unlike `press-release-spring`'s click-triggered burst or `asr-keyword-glow`'s word-timed envelope, this glow is **un-triggered** — it blooms on the hero's settle and stays lit. Two forms: a **hero bloom** that swells behind a settling element then breathes, and a **traveling sweep** that translates a soft highlight across a surface exactly once.

## How It Works

A radial-gradient layer sits **behind** the hero (glow `z-index: 1`, hero `z-index: 2` — a glow in front occludes it), starting at `opacity: 0`. Over the bloom-in window it ramps `opacity: 0 → peak` with a gentle `scale` swell, timed so `BLOOM_START + BLOOM_DUR` lands on the hero's settle — glow and hero resolve as ONE beat ("powering on"), never glow-then-card. After bloom-in:

1. **Hero bloom** — a **bounded idle breathe** during the hold: a finite `ease: "none"` tween advances a `phase` proxy and `onUpdate` nudges opacity + scale a hair around peak (never a `yoyo` loop). `sin(0) = 0` → the breathe starts exactly at the bloom's resting state.
2. **Traveling sweep** — a narrow highlight band at one edge translates **once** across to the other (`x` off-surface to off-surface), clipped to the surface (`overflow: hidden`). One pass, no return — a repeating sweep reads as a loading shimmer, not a reveal accent (the shimmer-sweep variation below is the sanctioned exception).

Peak opacity stays restrained (**≤ 0.45 hard ceiling**) so the glow gives presence without washing the frame; the glow color is **darker + more saturated** than the element it backs (a same-hue, same-lightness glow disappears into the surface).

## Recipe

```html
<!-- inside a standard scene clip -->
<div class="bloom-stage">
  <div class="bloom-glow" id="bloom-glow"></div>
  <!-- z-index: 1; inset: GLOW_INSET (negative); background: {glowGradient} -->
  <div class="hero-card" id="hero-card">{HeroLabel}</div>
  <!-- z-index: 2 -->
</div>
<!-- sweep form: <div class="sweep" id="sweep"> inside the overflow:hidden surface -->
```

```js
// ── Form A: HERO BLOOM ── bloom in soft, landing on the hero's settle.
tl.fromTo(
  "#bloom-glow",
  { opacity: 0, scale: GLOW_START_SCALE },
  { opacity: GLOW_PEAK_OPACITY, scale: 1, duration: BLOOM_DUR, ease: "power2.out" },
  BLOOM_START,
);
// Bounded breathe during the hold — finite phase tween, NOT a yoyo loop.
const glow = document.getElementById("bloom-glow");
const phase = { p: 0 };
tl.to(
  phase,
  {
    p: Math.PI * 2 * BREATHE_CYCLES,
    duration: BREATHE_DUR,
    ease: "none",
    onUpdate: () => {
      const s = Math.sin(phase.p);
      glow.style.opacity = String(GLOW_PEAK_OPACITY + s * OPACITY_AMP);
      glow.style.transform = `scale(${1 + s * SCALE_AMP})`;
    },
  },
  BLOOM_START + BLOOM_DUR,
);

// ── Form B: TRAVELING SWEEP ── one finite pass, constant glide.
tl.fromTo(
  "#sweep",
  { x: SWEEP_START_X, opacity: 0 },
  { x: SWEEP_END_X, opacity: SWEEP_PEAK_OPACITY, duration: SWEEP_DUR, ease: "none" },
  SWEEP_START,
);
tl.to("#sweep", { opacity: 0, duration: SWEEP_FADE_DUR, ease: "power1.in" }, SWEEP_FADE_START);
```

## Variations

- **Bloom-and-hold** — for scenes <3s or a hero with its own idle, skip the breathe: the single `fromTo` is the whole recipe.
- **Pulse-on-arrival** — bloom slightly PAST peak (`GLOW_OVERSHOOT_OPACITY`, `scale: 1.06`), then a second adjacent tween eases down to a steady hold — one breath punctuating the landing, no ongoing loop.
- **Multi-hero relay** — stagger per-glow `BLOOM_START` by ~0.15–0.3s across a row; shrink `OPACITY_AMP` / `SCALE_AMP` per the `/√N` rule below.
- **Diagonal raked sweep** — angle `{sweepGradient}` (~105°) across a wordmark: the classic one-pass logo sheen. Narrower `SWEEP_WIDTH`, higher `SWEEP_PEAK_OPACITY`.

### Shimmer sweep (text-clipped status-phrase working-state)

The sweep re-aimed **inside type**: a soft highlight gradient clipped into a status phrase ("Thinking…", "Analyzing dataset…") via `background-clip: text` travels left→right through the letterforms — the grey-on-grey shimmer that says _still working_. Unlike every other form here it legitimately **repeats while the status is live**: the repetition is diegetic working-state, not idle wobble (same defense as a blinking caret — the motion performs status). Two things keep it honest: it is **bounded** (one finite tween whose pass count is computed from the status window, never `repeat: -1`), and it is **killed at resolve** — the moment the status completes, the shimmer stops dead; a shimmer surviving into the answer beat turns a working indicator into decoration.

```js
// Status shimmer — N passes as ONE bounded tween. Killed at resolve.
const status = document.getElementById("status-phrase");
// CSS on #status-phrase: background: {shimmerGradient}; background-size: 300% 100%;
// -webkit-background-clip: text; background-clip: text; color: transparent;
const shimmer = { p: 0 };
const PASSES = Math.round(STATUS_DUR / PASS_PERIOD); // whole passes, computed up front
tl.to(
  shimmer,
  {
    p: PASSES,
    duration: STATUS_DUR,
    ease: "none",
    onUpdate: () => {
      const t = shimmer.p % 1; // 0→1 within each pass; percent axis inverted → left→right travel
      status.style.backgroundPosition = `${(1 - t) * 100}% 50%`;
    },
  },
  STATUS_START,
);
tl.set(status, { backgroundPosition: "100% 50%" }, STATUS_START + STATUS_DUR); // resolve: dead.
```

Keep it a whisper: `{shimmerGradient}` is the status text's own grey with one slightly-lighter band (highlight stop a step above the base, nothing near white); `background-size` ~300% keeps the band narrow in the glyphs; `PASS_PERIOD` 1.2–1.8s — slower reads as a sheen accent, faster as a spinner. Whole-number `PASSES` lands the band at its start position exactly at the kill frame, so the `tl.set` is visually a no-op. This is the working-state cousin of `gradient-text-sweep`: reach **here** when the sweep _means_ "in progress," **there** when the gradient is the typographic treatment itself.

## Values

| token                   | range / default                                        | notes                                                                      |
| ----------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------- |
| GLOW_PEAK_OPACITY       | 0.15 (subtle) → 0.30 (default) → **0.45 hard ceiling** | higher washes the frame; a glow you consciously notice is too strong       |
| GLOW_INSET              | −200 to −450px (1920×1080)                             | negative so the halo extends past the hero; too small reads as a tight rim |
| GLOW_START_SCALE        | 0.80–1.0                                               | ≤1.0 — grow into place, never shrink                                       |
| BLOOM_DUR / BLOOM_START | 0.6–1.4s                                               | `BLOOM_START + BLOOM_DUR` ≈ the hero's settle frame                        |
| OPACITY_AMP / SCALE_AMP | 0.02–0.05 / 0.01–0.03 default                          | `PEAK + OPACITY_AMP ≤ 0.45`; push only when the glow is the sole motion    |
| BREATHE_CYCLES          | period 2.5–4s per breath                               | glow breathes slower than element breathing                                |
| SWEEP_WIDTH             | 15–35% of surface (grid) / 8–15% (wordmark)            |                                                                            |
| SWEEP_DUR               | 0.8–1.6s                                               | one deliberate pass — slow enough to read as light                         |
| SWEEP_PEAK_OPACITY      | 0.10 → 0.25 (default) → 0.40                           | same ≤ ~0.45 wash limit; tight sweeps tolerate the high end                |
| SWEEP_START_X / END_X   | fully off-surface both ends                            | no visible spawn/despawn mid-surface; fade reaches 0 as the band clears    |
| PASS_PERIOD (shimmer)   | 1.2–1.8s                                               | with whole-number PASSES                                                   |

## Critical Constraints

- **Glow peak opacity ≤ 0.45** — including breathe amplitude; default to the LOW end (0.15–0.30).
- **Glow behind, hero in front**; glow color darker + more saturated than the hero surface.
- **Land glow and hero as one beat** — before or after reads as two separate events.
- **Breathe is bounded, sweep is one pass** — the only sanctioned repetition is the shimmer sweep, bounded and killed at resolve.
- **Concurrent halos compound** — per-glow amps ≤ default `/√N`, stagger breathe periods (2.6s / 2.9s / 3.3s) so they don't pulse in lockstep.
- **Don't combine a `boxShadow` glow on the hero with this halo layer** — they compete and read muddy; the glow lives on the dedicated layer.

## See also

`sine-wave-loop` (hero breathes on scale/y while the glow breathes on opacity, out of phase) · `press-release-spring` (the click-triggered sibling — never both behind one element) · `counting-dynamic-scale` / `stat-bars-and-fills` (bloom behind a landing stat) · `center-outward-expansion` (sweep across the assembled grid) · `gradient-text-sweep` (the design-beat gradient counterpart).

## Selected motion rule: counting-dynamic-scale

---
name: counting-dynamic-scale
description: Counter animation where the value counts up while transform scale grows to its final size, creating escalating visual weight without per-frame text reflow.
metadata:
  tags: counter, counting, scale, transform, number, dynamic, emphasis
---

# Counting with Dynamic Scale

A number counts from A → B while its transform scale grows to the final size — escalating visual weight ("this is impressive") without tweening `font-size` or forcing text layout on every frame. The final font size is static CSS; only the transform changes.

## How It Works

Two synchronized tweens at the SAME timeline position with the SAME ease: (1) a proxy value rendered as text via `onUpdate` (`Math.round(...).toLocaleString()`), (2) the counter's transform `scale: START_SCALE → 1`, where `START_SCALE = START_SIZE / END_SIZE`. A suffix (`%`, `×`, `+`) slides in AFTER the count lands — the number gets its own beat — and a label fades in early.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="counter-wrap">
  <span class="counter" id="counter">0</span><span class="counter-suffix">{suffix}</span>
</div>
<div class="counter-label">{label}</div>
```

```css
.counter-wrap {
  display: flex;
  align-items: baseline;
  justify-content: center;
  width: {counterContainerWidth}; /* fixed width — no layout shift as digit count changes */
}
.counter {
  font-variant-numeric: tabular-nums; /* MANDATORY — digits keep equal width */
  display: inline-block;
  font-size: {endSize}; /* final size is static; GSAP animates scale, not font-size */
  transform-origin: center center;
}
.counter-suffix {
  opacity: 0;
  transform: translateY(20px);
}
```

```js
const counter = document.getElementById("counter");
const state = { value: 0 };
const START_SCALE = START_SIZE / END_SIZE;

// Count value — onUpdate changes text only
tl.to(
  state,
  {
    value: TARGET_VALUE,
    duration: COUNT_DUR,
    ease: COUNT_EASE,
    onUpdate: () => {
      counter.textContent = Math.round(state.value).toLocaleString();
    },
  },
  0,
);

// Visual growth — compositor transform sharing the count's timing + ease
tl.fromTo(counter, { scale: START_SCALE }, { scale: 1, duration: COUNT_DUR, ease: COUNT_EASE }, 0);

// Suffix slides in AFTER the count completes
tl.to(
  ".counter-suffix",
  { opacity: 1, y: 0, duration: SUFFIX_DUR, ease: `back.out(${SUFFIX_BOUNCE_FACTOR})` },
  COUNT_DUR,
);

// Label fades in early
tl.from(".counter-label", { opacity: 0, y: 12, duration: LABEL_DUR, ease: "power2.out" }, LABEL_AT);
```

## Variations

- **Direct `innerText` tween (no proxy)** — GSAP can tween `innerText` directly for a number-only counter; keep the proxy form when you need locale formatting or suffix logic. The scale tween stays separate either way:

```js
tl.to(
  counter,
  { innerText: TARGET_VALUE, duration: COUNT_DUR, ease: COUNT_EASE, snap: { innerText: 1 } },
  0,
);
```

- **3D depth entry** — add a `tl.from(".counter", { z: -300, ... }, 0)` push-in; requires `perspective` on `.counter-wrap` and `transform-style: preserve-3d` on the counter.
- **Multi-stat coordinated reveal** — 3 stats counting in parallel share the SAME ease, duration, and start position so they finish together (a chord, not an arpeggio). Each stat usually also needs a paired graphic (bar / ring / stars) — don't stop at the number; see [stat-bars-and-fills.md](stat-bars-and-fills.md).

## Values

| token                 | range                                       | notes                                                                         |
| --------------------- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| TARGET_VALUE          | 2–3 digits ideal                            | 4+ digits needs a wider container; must fit at END_SIZE without clipping      |
| START_SIZE / END_SIZE | START ≈ 40–60% of END                       | design inputs used once for START_SCALE; never tween either                   |
| COUNT_DUR             | 1.2–2.5s                                    | below ~0.8s reads as a flash — the eye must read the digits scrolling past    |
| COUNT_EASE            | `power2.out` / `power3.out` ⭐ / `expo.out` | shared by value + scale; more `.out` = more dramatic deceleration at the peak |
| SUFFIX_DUR            | 0.3–0.6s                                    | fires at `COUNT_DUR`, never during the count                                  |
| SUFFIX_BOUNCE_FACTOR  | 1.4–2.0                                     | overshoot is fine on the suffix (it's punctuation, not data)                  |
| LABEL_AT / LABEL_DUR  | AT < COUNT_DUR/2; 0.4–0.7s                  | label arrives before the count peaks                                          |

## Critical Constraints

- **`tabular-nums` mandatory** + fixed-width container as belt-and-suspenders — without them digit-count transitions (9 → 10 → 100) jitter as glyph widths change.
- **Never set `fontSize` in `onUpdate`** — final type size is static CSS; only the transform changes per frame. Keep `onUpdate` O(1): set text only, no style writes or DOM creation.
- **`Math.round`, not `Math.floor`** — halfway through the final integer should already display the final value.
- **Avoid `back.out` / `elastic.out` on the counter itself** — overshoot makes the number look unstable (it's data, not decoration). Grow in place, don't bounce.
- **Label is BIG TEXT, not a page-style caption** — a tiny paragraph under a hero-size number reads as visual noise in video. Display-size, uppercase, tracked: the label is part of the headline.

## See also

`stat-bars-and-fills` (the paired graphic — give it the same ease/duration so number and fill land as one beat) · `svg-path-draw` (icons drawing in around the number) · `center-outward-expansion` (icons bursting outward at the count peak).
