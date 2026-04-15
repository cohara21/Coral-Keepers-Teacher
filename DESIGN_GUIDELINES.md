# Coral Keepers Design Guidelines

## 1. Goal
Keep Coral Keepers visually consistent across Teacher and Student experiences.

Use this file as the design protocol for all future UI edits.

## 2. Core Visual Language
- Tone: clean, classroom-friendly, ocean-inspired.
- Geometry: soft rectangles, rounded corners, subtle shadows.
- Density: moderate whitespace, readable hierarchy, no cramped sections.
- Contrast: prioritize readability over decorative effects.

## 3. Typography
- Primary font family: Inter.
- Headings: medium or semibold weight, clear vertical rhythm.
- Labels and metadata: small uppercase treatment where already used.
- Body text: maintain readable line-height and avoid tiny text.

## 4. Color System
- Primary accent blue: #0075de.
- Neutral text: #2f3333.
- Muted text: #5b605f.
- Background base: #faf9f8.
- White surface cards: #ffffff.

Guideline:
- Keep existing color tokens and values unless a change is intentionally global.
- Do not introduce random one-off hex colors when an existing token/value is available.

## 5. Layout Rules
- Preserve top navigation height and behavior.
- Keep page content within established max widths per page.
- Match vertical spacing patterns already used on sibling pages.
- For mirrored screens, maintain equal structural spacing in Teacher and Student where intended.

## 6. Card and Surface Style
- Card corners: small-radius style consistent with existing pages.
- Borders: light borders with low-contrast neutral color.
- Shadows: subtle elevation only, avoid heavy blur or deep drop shadows.
- Avoid mixing radically different card styles within the same screen.

## 7. Buttons and Interactive Controls
- Primary actions use blue background with white text.
- Secondary actions stay neutral and low emphasis.
- Hover and focus states should be visible but not flashy.
- Keep button height and padding consistent within each page.

## 8. Cory Chat UI Protocol
Cory is a reusable UI pattern and should remain consistent everywhere it appears.

Required behavior:
- Trigger in bottom-right corner.
- Popup opens/closes via trigger, close button, outside click, and Escape key.
- Empty initial body (no pre-filled conversation line).
- User bubble: blue, right aligned.
- Cory bubble: light gray, left aligned.
- Input supports Enter and Send button.

Current visual positioning standard:
- Close button top offset: 20px.
- Pointer right offset: 30px.

## 9. Teacher and Student Consistency Protocol
When a change applies to both views:
- Update matching Teacher and Student pages in the same pass.
- Keep interactions and component behavior equivalent.
- Preserve route correctness for each view's navigation.

When a change is view-specific:
- Keep it isolated to the relevant folder.
- Do not leak Teacher-only UI into Student pages or vice versa.

## 10. Responsive and Accessibility Guardrails
- Ensure layouts remain usable on narrow widths.
- Avoid text clipping and horizontal overflow.
- Maintain keyboard access for interactive controls.
- Preserve visible focus states.
- Keep semantic labels and aria attributes already in use.

## 11. Change Acceptance Checklist
Before finalizing UI edits:
- Check visual consistency against nearby pages.
- Verify nav links still target correct view pages.
- Verify spacing and alignment in both desktop and narrow widths.
- Verify Cory behavior on every touched page.
- Run error check on edited files.

## 12. Do Not Do
- Do not redesign one page into a different visual system.
- Do not remove shared interaction patterns without replacing them consistently.
- Do not change asset paths unless all references are updated.
- Do not commit system files like .DS_Store.
