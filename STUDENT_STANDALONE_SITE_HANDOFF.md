# Coral Keepers — standalone student site (handoff for another repo / AI)

Use this document when you want a **separate deployable website** that shows **only the student experience** (same UI as `Student/` in this monorepo), **without** any control to open the teacher app. The student and teacher apps intentionally live in one repo today; this explains how to split or mirror the student half cleanly.

---

## 1. Duplicating the **entire** Coral Keepers Teacher folder (common workflow)

If you are **copying the whole project** into a new folder or new repo (same layout: `Student/`, `Teacher/`, `assets/`, `vercel.json`, docs, etc.):

| Topic | What to do |
|--------|------------|
| **Asset paths** | **No edits needed.** `Student/*.html` uses `../assets/...`; that still resolves because `assets/` stays at the **repo root**, sibling to `Student/`. |
| **Student → teacher UI** | **Still required:** remove the **“Student View” switch** from every `Student/*.html` file (see §4.1). That is the only navigation from the student shell into `Teacher/`. |
| **Default URL / hosting** | **Change `vercel.json`:** this repo redirects `/` → `Teacher/index.html`. For a student-only site, point `/` to **`Student/index.html`** instead (or your host’s equivalent). Until you do that, opening the site root still lands on **teacher**. |
| **`Teacher/` directory** | **Optional.** Student pages do not need it at runtime once the switch is gone. You can **delete the whole `Teacher/` folder** for a smaller deploy and to avoid shipping teacher UI at all—or **keep** it if you want an easy diff/merge with the original monorepo. If you delete it, grep `Student/` for `Teacher` and expect **no** matches after switch removal. |

So: **full-folder copy does *not* remove the need to edit student HTML and hosting config**; it only means you do **not** have to manually cherry-pick `assets/` or worry about broken `../assets/` paths.

---

## 2. What exists in the source project

| Path | Role |
|------|------|
| `Student/*.html` | All student-facing pages (home, learn, readings, videos, quizzes, submissions, calendar, messages, profile, announcements, plus content pages for lessons/quizzes). |
| `Teacher/*.html` | Teacher-only UI. **Do not ship** in a student-only site. |
| `assets/` (repo root) | Shared images, SVGs, icons, fonts are loaded via **relative URLs** from HTML. |
| `vercel.json` (repo root) | Sends `/` → `Teacher/index.html` for the **combined** demo. A student-only deployment must **not** use that redirect as the default entry. |

Student pages reference shared media as **`../assets/...`** (because `Student/` is one level below repo root). Any new layout must preserve that relationship **or** rewrite those paths.

---

## 3. Alternative: minimal copy (subset only)

Skip this section if you already duplicated the **entire** folder (§1). Use this when you want the **smallest** new project instead of a full clone.

### 3.0 Files to copy for a minimal functional student site

Copy **at minimum**:

- Entire **`assets/`** directory (repo root), unchanged — unless you intentionally trim unused files later.
- All **`Student/*.html`** files (currently 20 HTML files in `Student/`).

Optional / same as source:

- Nothing from `Teacher/` is required for the student UI to render.
- Do **not** copy `.cursor/`, debug logs, or internal docs unless you want them in the new repo.

**Inventory of `Student/*.html` (verify in source before copying):**

- `index.html` — dashboard / home  
- `learn.html` — assignments hub  
- `readings.html`, `videos.html`, `quizzes.html`, `submissions.html` — section hubs  
- `announcements.html`, `calendar.html`, `messages.html`, `profile.html`  
- Content / task pages (examples): `is-coral-animal.html`, `coral-bleaching.html`, `reading-coral-101.html`, `reading-coral-anatomy.html`, `reading-identify-coral.html`, `quiz-coral-101.html`, `quiz-coral-bleaching.html`, `quiz-identify-coral.html`, `submission-coral-essay.html`, `submission-class-participation.html`  

If the source tree gains new `Student/*.html` pages, copy those too so in-app links do not 404.

---

## 4. What to remove or change (teacher bridge)

### 4.1 Remove the “Student View” switch (required)

In every copied student HTML file, the top nav includes an **`<a class="nav-link switch" ... href="../Teacher/index.html">`** block that switches to the teacher app. For a standalone student site:

- **Delete the entire `<a>...</a>` element** whose opening tag matches: `class="nav-link switch"` (and `href` pointing at `Teacher`).

Typical shape (indentation may vary):

```html
<a class="nav-link switch" href="../Teacher/index.html">
  <span>Student View</span>
  <span class="switch-icon" aria-hidden="true">
    <img src="../assets/teacher-switch-blue.svg" alt="" width="16" height="16" />
  </span>
</a>
```

**Verification:** after edits, the student tree must contain **no** matches for:

- `../Teacher/`
- `Teacher/index.html`
- `class="nav-link switch"` (or `nav-link switch` in markup)

### 4.2 Optional cleanup (CSS)

Rules targeting `.nav-link.switch` / `.switch-icon` in `<style>` blocks become unused once the link is removed. Removing them is optional; it reduces file size slightly.

### 4.3 `Student/index.html` script (optional)

The file may declare:

```js
const isTeacherView = window.location.pathname.includes('/Teacher/');
```

If this variable is **unused** after your edits, delete the line to avoid linter noise. If any logic branches on `isTeacherView`, keep the variable but set it to **`false`** for a student-only build (or remove the branch if dead).

---

## 5. Paths and “functional” checklist

### 5.1 Asset paths

- As copied from this repo, each page under `Student/` uses **`../assets/...`**.
- If the new site’s HTML lives in a folder **sibling** to `assets/` at project root (mirroring this repo), **keep** `../assets/` as-is.
- If you flatten so HTML is **next to** `assets/` (no `Student/` folder), change every `../assets/` → `assets/` (or `/assets/` if you use absolute paths from site root).

### 5.2 Internal links

Student pages link to each other with **same-directory** names (`index.html`, `learn.html`, etc.). Keep that pattern unless you change routing.

### 5.3 External embeds

Some pages embed third-party iframes (e.g. Cory assistant). Those are not “teacher”; they are fine to keep unless product policy says otherwise.

### 5.4 Hosting entry URL

- This repo’s `vercel.json` redirects `/` to **Teacher** for the combined demo.
- A **student-only** deployment should set the default document to **`Student/index.html`** (or your equivalent path) and **omit** the teacher default redirect.

---

## 6. What *not* to do

- Do **not** leave any link or button that navigates to `Teacher/` — that violates “student-only.”
- Do **not** assume `StudentPortal/` exists in this repo; that was an experiment and should remain **deleted**. Always copy from **`Student/`**.

---

## 7. Suggested workflow for the receiving AI

**If the human duplicated the entire Coral Keepers Teacher folder:**

1. Open `Student/*.html` and remove every `nav-link switch` → `../Teacher/index.html` block (§4.1).  
2. Edit **`vercel.json`**: change the `/` redirect target from **`Teacher/index.html`** to **`Student/index.html`** (§1 table).  
3. Optionally delete the entire **`Teacher/`** folder; then grep `Student/` for `Teacher` → zero hits.  
4. Optionally clean `isTeacherView` / unused switch CSS (§4.2–4.3).  
5. Smoke-test from site root: Home → Learn → reading / video / quiz / submissions / calendar / messages / profile.

**If instead they want a minimal new tree (no full copy):**

1. Copy `assets/` + all `Student/*.html`; preserve sibling layout **or** rewrite `../assets/` (§3, §5.1).  
2. Same switch removal and hosting defaults as above.

---

## 8. One-line summary

**Full-folder copy:** paths stay valid; you **still** remove the student **teacher switch**, **retarget `vercel.json`** (or host default) to **`Student/index.html`**, and optionally delete **`Teacher/`**. **Minimal copy:** `assets/` + `Student/*.html` + same switch + hosting rules.
