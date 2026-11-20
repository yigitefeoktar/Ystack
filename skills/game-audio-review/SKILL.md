---
name: game-audio-review
description: Make game sound-effect work reviewable in a playable sound preview page. Use when explicitly invoked or for requests to add, create, wire up, replace, tune, balance, fix, test, hear, show, or compare game sound effects whenever the user needs to audition or review the result, including clear follow-ups and numbered selections. Covers new effects and targeted changes as well as full audio reviews, harsh or repetitive sounds, missing playback, and volume issues; it is not limited to audits or requests that explicitly mention a preview page.
---

# Game Audio Review

Make the active game's sound-effect work easy for Yigit to hear and review, whether adding effects, changing them, fixing playback, comparing alternatives, or auditing audio. Use a simple preview page: a light background, a narrow column of labeled rows, a Play button per sound, one sound at a time, and replacement comparisons at the top.

## Scope and discovery

- Work in the user's active game project. Inspect its instructions, Git status, audio entry points, assets, event callers, and existing preview page. Preserve unrelated work.
- For requested sound-effect work that needs an audible review, prepare or update the preview page and start its local preview when needed, even if the user did not explicitly request a preview page. Reuse this project's running server after verifying its identity; otherwise start a loopback server on an available port and open the page in Codex. Honor explicit read-only or no-server instructions. Do not start another game's project or assume port 3000 belongs to this one.
- Match the work to the request. For a targeted addition, replacement, tuning, or playback fix, use the relevant sections below and verify the affected cues and mix. Keep the preview catalogue current without turning every small sound change into a full-game audio audit; perform the broader audit when requested or needed to diagnose the issue.
- Follow the project's checks, commit, and deployment rules for any requested code or preview UI changes. An audit alone does not authorize changing the game's audio. Do requested fixes and selected replacements without asking for approval again.
- Inventory every audio cue actually used in the game: UI feedback, orders, combat, abilities, outcomes, ambient loops, music, and voices where present. Map each to its trigger and playback function. Distinguish unused assets and trailer-only sounds from active game sounds.

First check whether the active game already has a sound preview page. Search its files and routes for audio preview components, sound catalogs, and playback buttons; names such as `SoundPreview`, `sounds=1`, `audio-preview`, or `soundboard` are useful clues. Verify the page belongs to this game and discover its actual URL from the routing code. Reuse and extend that page when it exists, preserving its layout and existing comparisons. Do not create a duplicate page or assume a particular route, repository path, or game name.

Only when no sound preview page exists, adapt [assets/SoundPreview.tsx](assets/SoundPreview.tsx) and [assets/SoundPreview.css](assets/SoundPreview.css). These assets provide the desired layout without requiring Tailwind; wire their entries to the active game's actual audio code.

## Audit sound quality and the mix

Evaluate each cue in context rather than declaring every difference a defect:

- **Character:** Does its tone fit its event? Are success, rejection, and danger distinguishable? Flag harsh buzzing, excessive static, piercing frequencies, abrupt starts/stops, overly long tails, or a cue that resembles damaged hardware.
- **Repetition:** Consider how often it fires, AI versus player events, rapid interactions, and overlap. A pleasant isolated sound can be tiring when triggered repeatedly.
- **Perceived volume:** Compare complete effects after their production mixer, including all layers, duration, pitch, filtering, and envelopes. Equal oscillator gain values or equal peaks do not establish equal perceived loudness.
- **Mix behavior:** Inspect music masking, missing/muted cues, clipping/headroom, summing during busy play, and source cleanup. Check whether compressors or limiters alter single cues unintentionally.

Measure representative output where feasible. For synthetic Web Audio, render the actual scheduler with `OfflineAudioContext`; for recorded assets, decode or analyze the actual files with their production gain applied. Use [references/measurement.md](references/measurement.md) and [scripts/analyze-audio-buffer.js](scripts/analyze-audio-buffer.js). Keep scratch renders and reports outside tracked game files unless requested. Prefer an isolated measurement page or fresh module/context; restore temporary global overrides.

Use a useful hierarchy: quiet controls, consistent routine gameplay cues, softer frequently repeated pulses, and slightly louder major events. About 3 dB more for major events is a starting point, not a universal requirement. Compare within each role before flattening intentional differences. Discover and preserve the user's approved sound choices from the current game's code and conversation unless asked to change them.

Give a concise finding per sound or group: **good**, **needs tuning**, or **replacement suggested**, with the reason and evidence. Separate measured issues, code-based inferences, and subjective preference. Do not claim to have listened if only code or measurements were inspected. When audio listening is unavailable, make the preview usable and let the user judge timbre; still complete objective checks.

## Open all sounds in the preview

- Reuse the current preview page and its URL. Update its inventory when sounds are added or removed; do not hardcode a stale sound count.
- Play the game's real implementations with the same gain/mixer as gameplay. Prepare/resume audio from a real user click. Exclude incidental hover/click cues and background music from isolated effect previews.
- Each row needs a stable ID, a readable name, a brief description of its trigger, and a Play button. Show starting/playing/last-played status. Prevent accidental overlapping previews. For loops or music, provide a bounded excerpt and stop it afterward.
- Keep the simple layout and comparison sections. Maintain mouse-wheel and touch scrolling despite global game styles that disable them, keyboard-accessible controls, and access to the last row.
- Verify in a browser: the inventory is complete, a trusted click unlocks audio, actual output is non-silent, the audio context runs, there are no playback errors, and scrolling reaches the bottom. A status timer finishing is not proof that audio played. Open the verified URL in the user's Codex panel and provide its link.

## When the user asks for options

- Add distinct alternatives **inside this same preview page**, next to the current sound at the top. A few options normally means 3–5; four is a useful default. Name them `Option 1`, `Option 2`, etc., with short descriptions.
- Keep the current cue available for comparison. Preserve other sounds and existing pending option sets. Identify which sound each comparison belongs to, and keep option numbers stable until the choice is settled.
- Match candidate loudness to the current cue's role so a louder sample does not win unfairly. Use clean attacks/releases and the production mixing path where feasible. Candidate generators/assets stay outside active gameplay until chosen.
- Run and open the page so the user can audition the options. Explain the differences briefly, then let the user choose. Do not replace the active game cue just because options were requested.

## When the user chooses or asks for a fix

- Map a number to the latest options for the named sound. If there are multiple genuinely ambiguous comparisons, clarify the mapping; otherwise implement the selection directly.
- Share the chosen implementation between gameplay and preview, including the same mix calibration. Update the active label and remove stale choice instructions while retaining comparisons when useful.
- For balancing, adjust each complete effect using measurements and its role. Preserve tone and timing unless those were also in scope. Check quiet UI cues, routine cues, important events, repetition, and a representative busy mix. Use peak protection when demonstrated overlap problems warrant it, and remeasure single effects afterward.
- Run the project's relevant checks and verify the real playback path. Follow its release workflow and confirm deployment when required. Keep unrelated assets, credentials, videos, and scratch audio out of the commit.

Finish with the main findings or implemented result, the working preview link, meaningful verification, and any release details required by the project. The user should be able to listen immediately, request options on that page, and choose a numbered replacement in a follow-up.
