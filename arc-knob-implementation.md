# Arc and Knob Implementation

This file captures the working gauge arc and moving knob used in the tablet screen so you can reuse the same behavior elsewhere in the project.

## What it does

- Draws a curved SVG arc
- Positions a moving knob on the arc based on a `0-100` value
- Keeps the knob rotated to match the tangent of the curve
- Lets you resize the arc by changing the SVG viewBox, the arc radii, and the knob dimensions together

## SVG Markup

```html
<div class="meter-wrapper">
  <svg id="meterSvg" class="gauge-svg" viewBox="0 0 260 160" aria-label="Coral vitality arc gauge">
    <defs>
      <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#ff5c69;" />
        <stop offset="35%" style="stop-color:#ffb020;" />
        <stop offset="65%" style="stop-color:#c7dd19;" />
        <stop offset="100%" style="stop-color:#34c96b;" />
      </linearGradient>
    </defs>
    <path class="gauge-base" d="M 8 134 A 114 134 0 0 1 252 134" />
    <g id="knobGroup">
      <rect class="knob-pill" x="-10" y="-20" width="20" height="40" rx="10" />
    </g>
  </svg>
</div>
```

## CSS

```css
.gauge-panel {
  height: 332px;
  position: relative;
}

.meter-wrapper {
  max-width: 500px;
  position: relative;
  transform: translateY(18px);
  width: 100%;
  z-index: 2;
}

.gauge-svg {
  cursor: default;
  height: auto;
  overflow: visible;
  width: 100%;
}

.gauge-base {
  fill: none;
  stroke: url(#gaugeGradient);
  stroke-linecap: round;
  stroke-width: 16;
}

.knob-pill {
  cursor: default;
  fill: #fff;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.2));
  transition: transform 0.1s ease-out;
}
```

## JavaScript

```js
const RADIUS_X = 114;
const RADIUS_Y = 134;
const CX = 130;
const CY = 134;
const INDICATOR_OFFSET = 2.5;
const KNOB_SHIFT_X = 5;

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function updateMeter(value) {
  const clamped = clamp(value, 0, 100);
  const percentage = clamped / 100;
  const angleRad = Math.PI - (percentage * Math.PI);
  const x = CX + RADIUS_X * Math.cos(angleRad);
  const y = CY - RADIUS_Y * Math.sin(angleRad);
  const dx = -RADIUS_X * Math.sin(angleRad);
  const dy = -RADIUS_Y * Math.cos(angleRad);
  const rotation = (Math.atan2(dy, dx) * 180) / Math.PI;
  const normalX = (x - CX) / (RADIUS_X * RADIUS_X);
  const normalY = (y - CY) / (RADIUS_Y * RADIUS_Y);
  const normalLength = Math.hypot(normalX, normalY) || 1;
  const offsetX = (normalX / normalLength) * INDICATOR_OFFSET;
  const offsetY = (normalY / normalLength) * INDICATOR_OFFSET;

  knobGroup.setAttribute(
    "transform",
    "translate(" + (x + offsetX + KNOB_SHIFT_X) + ", " + (y + offsetY) + ") rotate(" + rotation + ")"
  );
}
```

## How to reuse it elsewhere

1. Copy the SVG block into the new screen.
2. Add the CSS rules for the gauge container, wrapper, SVG, arc, and knob.
3. Copy the JavaScript constants and `updateMeter` function.
4. Make sure the new screen has an element with `id="knobGroup"`.
5. Call `updateMeter(yourValue)` whenever the score changes.
6. Keep the SVG geometry and the JS geometry in sync:
   - `viewBox`
   - arc path `d`
   - `RADIUS_X`
   - `RADIUS_Y`
   - `CX`
   - `CY`
   - knob width and height
   - `KNOB_SHIFT_X`

## Notes

- If the knob feels too far left or right, adjust `KNOB_SHIFT_X` by 1 to 2 pixels.
- If the arc needs to sit higher or lower, adjust the wrapper with `transform: translateY(...)` or change the SVG path and center values together.
- If you make the arc wider or taller, update the SVG `viewBox`, the arc path, and the JS radii at the same time so the knob stays aligned.
