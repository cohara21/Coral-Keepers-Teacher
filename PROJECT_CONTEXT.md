# Coral Keepers Project Context

## 1. Project Purpose
Coral Keepers is a two-view web experience for classroom coral education:
- Teacher view for course management, messaging, assignments, and reading posts.
- Student view for learning activities, profile, messaging, and calendar.

The project is currently a static multi-page HTML/CSS/JavaScript site with shared assets.

## 2. Top-Level Structure
- /Teacher: Teacher-facing pages.
- /Student: Student-facing pages.
- /assets: Shared images/icons/media.
- /vercel.json: Deployment config.
- /.github/copilot-instructions.md: Editing guardrails for this repo.

## 3. Information Architecture
Teacher pages:
- index.html
- course.html
- course-details.html
- post-reading.html
- learn.html
- calendar.html
- announcements.html
- messages.html

Student pages:
- index.html
- learn.html
- calendar.html
- announcements.html
- messages.html
- profile.html
- is-coral-animal.html

## 4. Critical IA Rules
- Keep Student and Teacher versions aligned when a change applies to both.
- Keep version-specific changes only in the matching folder.
- Preserve all existing relative links and asset paths.
- Teacher switches and nav must stay inside Teacher routes.
- Student switches and nav must stay inside Student routes.

## 5. Cory Chat System Contract
Cory chat appears as a floating button and popup on many pages.

Expected behavior baseline:
- Opens from bottom-right trigger button.
- Closes via X button, outside click, and Escape key.
- Empty initial chat body (no pre-seeded prompt text).
- User messages on right in blue bubbles.
- Cory messages on left in light gray bubbles.
- Message text wraps inside bubble bounds.
- Enter key and send button both submit.

Expected key selectors and elements:
- Trigger button: .floating-ai or .cory-trigger depending on page.
- Popup: #coryPopup
- Close button: .cory-close
- Chat body: .cory-body
- Input: .cory-input
- Send button: .cory-send

Positioning decisions currently used:
- Close button top offset: 20px
- Pointer right offset: 30px

## 6. Known Sensitive Areas
- Teacher/messages.html has two interactive systems in one script:
- Message composer logic (new message buttons, class/student targeting, send state)
- Cory chat logic

If editing Teacher/messages.html:
- Do not remove compose handlers for .new-message-trigger.
- Keep compose panel open/close logic intact.
- Keep Cory logic separate and complete.

## 7. Visual Consistency Notes
- Student/index.html is the source-of-truth style reference for Cory popup behavior and bubble layout.
- Teacher/post-reading.html hero banner should match standard teacher banner scale (currently reduced to align with other pages).

## 8. Change Management Checklist
Before finishing a cross-page update:
- Confirm mirrored Student/Teacher pages were both updated where applicable.
- Verify Cory open, close, send, and Enter behavior on touched pages.
- Verify no broken nav links between Teacher and Student sections.
- Run a syntax/error check on edited files.

## 9. Git Workflow Notes
- Avoid committing .DS_Store.
- Commit only intended files for each task.
- Push main after confirming changes locally.
