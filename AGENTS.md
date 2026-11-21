# Personal preferences

## Shared Codex and Claude Code setup in T3 Code

- The personal Codex and Claude Code setups share these instructions and the same seven personal skill sources. Claude's global `CLAUDE.md` imports this file; its personal skill folders may be links to the Codex sources. Edit the canonical source once rather than replacing linked folders or maintaining divergent provider copies. Preserve provider-specific and unrelated instructions.
- In T3 Code, read the sibling `T3_SETUP.md` when setup context is missing or a host-specific workflow is needed. Use current session tool contracts, not remembered Codex desktop API names. Provider/model availability and permissions must be verified, not inferred from this file.
- Ordinary work needs no orchestration. Use delegation only when requested or required by an applicable workflow. Separate top-level chats from child agents; preserve the user's selected provider/model and use T3-managed workspace isolation. Never substitute another provider silently.
- Use T3's supported HTML presentation tools for requested in-chat visuals, code rendering for exported assets, and its shared browser only for requested browser work. Follow current host instructions for thread receipts, waiting, PR links, secrets, and scheduling. Do not assume Codex desktop panels, connectors, or completion callbacks exist in T3.

## Ystack repository synchronization

- For Yigit Efe Oktar's own Codex setup, keep the public repository `https://github.com/yigitefeoktar/Ystack` synchronized whenever this universal `AGENTS.md` or a personal skill distributed there is changed. Update the corresponding public files and any affected usage instructions in the same task, run relevant repository validation, and commit and push the task-related update to `main`. This is standing authorization for those updates; preserve unrelated work and reconcile newer remote changes safely.
- Preserve the public copy's redactions and portability notes. Never copy credentials, private machine endpoints, runtime state, or unrelated system/plugin/disabled skills into the repository. If synchronization cannot be completed, report the specific blocker. This maintainer-specific rule is not authorization for other users to publish to the author's repository; people adopting Ystack should configure their own repository or remove this section.

## Project URLs in responses

- In project chats, end every response with clickable links to the relevant current dev server, preview, or live URLs being worked on, whenever available. Include them in discussions, questions, and status updates as well as implementation reports, even when no changes were made in the latest turn. Use actual known URLs; do not invent them. If no URL is available, omit links silently without mentioning their absence.
- Keep these links unobtrusive at the very bottom of the message, on one final line with short neutral labels such as `Dev`, `Preview`, or `Live`, separated by a middle dot when there are multiple links. Do not add a heading, bold emphasis, callout, or repeated promotional wording around them. Repeat a URL in the body only when it is needed to explain the task.

## Game UI design

- Keep game UIs simple and uncluttered. Use minimal, purposeful text; avoid unnecessary headings, explanations, labels, and decorative copy.
- Prefer generated images for game UI artwork, especially backgrounds and illustrated icons, over complex hand-built SVG backgrounds or icons. Use image-generation tools for these assets when available.
- Never add the game's name or game icon to game-over screens.
- Remove default browser/Windows scrollbars throughout all game UIs, including menus. Prefer layouts that do not need scrolling. If scrolling is necessary, preserve usable scrolling while hiding the native scrollbar; build a custom scrollbar only when absolutely necessary.

## Visual proposals and completed changes

- When proposing visual changes, normally show three meaningfully different options as rendered images, numbered sequentially with short explanations so I can choose. Three is a default, not a fixed requirement: give more or fewer when I ask. Respect an already chosen design; do not reopen settled choices or invent alternatives for nonvisual work.
- After implementing visual changes, show images of the actual implemented result whenever possible. Include the visual in the response rather than only describing the change or giving a file path.
- For animation, timing, transitions, or other changes that benefit from motion, show a short video or animated GIF instead of relying only on still images. Present alternatives side by side when that makes comparison easier.
- Produce previews mainly through code-driven rendering: the game's own renderer/canvas, HTML/CSS, or rendered SVGs. Reuse actual assets and rendering code where practical so the preview represents the proposed or implemented result faithfully.
- Avoid computer use for obtaining these images and videos. Prefer direct rendering, headless browser scripts, frame export, and video encoding. Use computer use only when necessary and keep it minimal.
- Clearly distinguish proposal/mockup renders from renders of implemented changes. A mockup is not evidence that the running game looks or behaves that way.
- Generated images are preferred for artwork used inside the game UI; code/SVG rendering remains appropriate for producing previews and comparisons.
