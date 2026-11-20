# Personal preferences

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
