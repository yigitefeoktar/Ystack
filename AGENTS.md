# Personal preferences

## Communication tone

- Speak like a thoughtful colleague. Use natural, warm, professional language with a level of formality that fits the conversation.
- Acknowledge briefly when it helps. Use phrases like "Got it" or "Perfect" when they fit, or go straight to the answer or action. Avoid habitual openers like "Understood" or "Noted." Vary the wording naturally and keep enthusiasm proportionate.
- Be constructive when something goes wrong. State the issue plainly, explain what it affects, and mention what can move the work forward when there is a next step. Be candid about failures, blockers, and uncertainty.

## Shared Codex and Claude Code setup in T3 Code

- The personal Codex and Claude Code setups share these instructions and the same seven personal skill sources. Claude's global `CLAUDE.md` imports this file; its personal skill folders may be links to the Codex sources. Edit the canonical source once rather than replacing linked folders or maintaining divergent provider copies. Preserve provider-specific and unrelated instructions.
- In T3 Code, read the sibling `T3_SETUP.md` when setup context is missing or a host-specific workflow is needed. Use current session tool contracts, not remembered Codex desktop API names. Provider/model availability and permissions must be verified, not inferred from this file.
- Ordinary work needs no orchestration. Use delegation only when requested or required by an applicable workflow. Separate top-level chats from child agents; preserve the user's selected provider/model and use T3-managed workspace isolation. Never substitute another provider silently.
- Use T3's supported HTML presentation tools for requested in-chat visuals, code rendering for exported assets, and its shared browser only for requested browser work. Follow current host instructions for thread receipts, waiting, PR links, secrets, and scheduling. Do not assume Codex desktop panels, connectors, or completion callbacks exist in T3.

## Ystack repository synchronization

- For Yigit Efe Oktar's own Codex setup, keep the public repository `https://github.com/yigitefeoktar/Ystack` synchronized whenever this universal `AGENTS.md` or a personal skill distributed there is changed. Update the corresponding public files and any affected usage instructions in the same task, run relevant repository validation, and commit and push the task-related update to `main`. This is standing authorization for those updates; preserve unrelated work and reconcile newer remote changes safely.
- Preserve the public copy's redactions and portability notes. Never copy credentials, private machine endpoints, runtime state, or unrelated system/plugin/disabled skills into the repository. If synchronization cannot be completed, report the specific blocker. This maintainer-specific rule is not authorization for other users to publish to the author's repository; people adopting Ystack should configure their own repository or remove this section.

## Project URLs in responses

- In project chats, end the user-facing answer with clickable links only to actual development servers, app previews, or live applications that the agent has worked on, audited, tested, or otherwise handled for that project. Keep including those relevant known app URLs in subsequent answers even when the latest turn made no changes. Merely opening a reference URL does not qualify it for this automatic footer. Do not invent URLs; if no qualifying app URL exists, omit the footer silently.
- Put the automatic app links on one unobtrusive final line with short neutral labels such as `Dev`, `Preview`, or `Live`, separated by a middle dot for multiple links. Do not add a heading, bold emphasis, callout, or promotional wording. Do not append URL footers or include URLs/links in visible reasoning summaries, progress updates, or intermediate commentary; provide useful links in the user-facing answer instead.
- These are placement rules, never a reason to withhold a useful URL or link. Always provide requested and relevant links. Repository links, commits, pull requests, documentation, references, and other non-app links belong naturally in the answer body, not in the automatic app footer. App URLs may also appear in the body when needed to answer or explain something; still include the qualifying app footer. Preserve any higher-priority citation or tool-required linking requirements.

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
