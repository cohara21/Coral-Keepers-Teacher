# Cory assets by health score

Reference for which Cory image is shown at which **AI health score** (0–100%). Logic lives in JavaScript on the home/dashboard pages unless noted as static.

**Source of truth (score → mood):**

- `Student/index.html` — `coryMoodImageForScore()` (arc gauge) and `calculateAIHealthScore()` (simulation card)
- `Teacher/index.html` — `coryMoodImageForScore()` (arc gauge only; no simulation Cory swap)

Both mood functions use the **same thresholds** and the same file naming pattern: `../assets/Cory {n}.svg`.

---

## 1. AI Health Score arc (`.health-cory`)

Updates when the live tank health metric changes (demo tick, stress mode, etc.). Initial HTML loads `corymain.svg` until the first `render()` runs.

| Health score | Asset file | Cory # |
|--------------|------------|--------|
| **90–100** | `assets/Cory 1.svg` | 1 (best) |
| **75–89** | `assets/Cory 2.svg` | 2 |
| **60–74** | `assets/Cory 3.svg` | 3 |
| **40–59** | `assets/Cory 4.svg` | 4 |
| **20–39** | `assets/Cory 5.svg` | 5 |
| **0–19** | `assets/Cory 6.svg` | 6 (worst) |

**Boundary rule:** comparisons use `>=` (e.g. `90` → Cory 1, `89` → Cory 2, `20` → Cory 5, `19` → Cory 6). Score is `Math.round()`’d before lookup.

**Where it appears:**

| Page | Element | Function |
|------|---------|----------|
| `Student/index.html` | `<img class="health-cory">` | `coryMoodImageForScore(health)` via `updateArcCoryMascot()` |
| `Teacher/index.html` | `<img class="health-cory">` | same |

---

## 2. Tank simulation card (Student home only)

When the user moves simulation sliders, `calculateAIHealthScore()` computes a **total score** (sum of temp / pH / salinity / redox sub-scores, max 100) and swaps the simulation preview image. **Same numeric bands** as the arc, but different files (`CorySimulation*.webp`).

| Total simulation score | Asset file | Cory # |
|------------------------|------------|--------|
| **90–100** | `assets/CorySimulation1.webp` | 1 |
| **75–89** | `assets/CorySimulation2.webp` | 2 |
| **60–74** | `assets/CorySimulation3.webp` | 3 |
| **40–59** | `assets/CorySimulation4.webp` | 4 |
| **20–39** | `assets/CorySimulation5.webp` | 5 |
| **0–19** | `assets/CorySimulation6.webp` | 6 |

**Where it appears:**

| Page | Element IDs | Notes |
|------|-------------|--------|
| `Student/index.html` | `#cory-avatar`, `#cory-avatar-modal` | Inline sim card + enlarged sim modal |

`Teacher/index.html` does **not** include this simulation Cory swap.

> **Repo note:** As of this doc, `Cory 1.svg`–`Cory 6.svg` exist under `assets/`. `CorySimulation1.webp`–`CorySimulation6.webp` are **referenced in code** but may need to be added to `assets/` if previews are broken.

---

## 3. Static Cory assets (not tied to score)

These do **not** change with health percentage.

| File | Used on | Role |
|------|---------|------|
| `assets/corymain.svg` | `Student/index.html`, `Teacher/index.html` | Default `src` on `.health-cory` before JS updates |
| `assets/coryforcard.svg` | `Student/index.html`, `Teacher/index.html` | Icon on each **Core Vitals** flip card (`.vital-cory-icon`) |
| `assets/cory-hover-icon.svg` | — | Listed in asset inventories; **not referenced** in HTML/JS in this repo |
| `assets/corychaticon.svg` | — | Listed in asset inventories; **not referenced** in HTML/JS in this repo |

---

## 4. Cory chat (iframe, not a local mood asset)

Many pages embed the external assistant:

```html
<iframe id="cory-iframe" src="https://cory-ai-brain.vercel.app/" …>
```

That UI is **not** one of `Cory 1.svg`–`Cory 6.svg`. On `Student/index.html` / `Teacher/index.html`, tank metrics are sent to the iframe via `postMessage` (`UPDATE_TANK_DATA`); mood artwork inside the iframe is controlled by that app, not by the tables above.

---

## 5. Quick lookup (same bands everywhere score-based)

```
Score:  90+    75–89   60–74   40–59   20–39   0–19
Cory #:   1      2       3       4       5       6
Arc:     Cory N.svg
Sim:     CorySimulationN.webp   (Student/index.html only)
```

---

## 6. Default health on load (for testing)

| Page | Initial `metrics.health` | First arc Cory after render |
|------|--------------------------|-----------------------------|
| `Student/index.html` | `85` | `Cory 2.svg` |
| `Teacher/index.html` | `85` | `Cory 2.svg` |

Simulation sliders default to a total score around **94** (`CorySimulation1.webp`) when all four sliders are present at their default values.
