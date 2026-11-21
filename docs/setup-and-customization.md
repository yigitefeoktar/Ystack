# Setup and customization

## Choose the skills you need

Ystack's workflows are modular. Installing all seven does not make every workflow run on every task. Six support normal description-based selection; Master Project Manager has `allow_implicit_invocation: false` and needs deliberate invocation.

The descriptions guide selection; they are not deterministic event hooks. Match depends on your Codex version, available context, and installed tools. Use the exact `$skill-name` when you want a particular workflow. A chat about editing a skill is not an instruction to carry out its external workflow.

## Tool and account requirements

| Skill | Needed for its actual work |
| --- | --- |
| Confirm Task Understanding | Conversation context; filesystem/project access when relevant |
| Game Audio Review | The game's source, its playback implementation, a browser with audio, and the project's normal development tools; the supplied UI assets use React/TypeScript |
| ByteBrew Game Analytics | Your own ByteBrew application/configuration; official SDK docs; authenticated dashboard access for ingestion/count verification |
| Game Deployment | Your own GitHub repository and Vercel project, authenticated CLI/connectors as available, and the project's build tools |
| CrazyGames Basic Launch | Your own CrazyGames developer account and a supported authenticated browser/upload session |
| Manage Games Hub | Your own hub repository, a saved Codex desktop project, project/chat creation tools, and the hub's deployment access |
| Master Project Manager | current host project/chat tools (T3 or legacy Codex desktop) and a verified saved project; additional workers use their own normal project permissions |

This repository installs instructions and helper files. It does not install connectors, provision accounts, copy credentials, start a backend, or grant access to another user's repositories. If the required tools are unavailable, the skill should report the limitation rather than simulate a successful action.

## Personal project bindings

### Games Hub

`skills/manage-games-hub/SKILL.md` records the author's public hub (`yigitefeoktar/game-hub`) and its live URL. Treat these as origin context. Before using the skill for your own website:

1. Replace the repository, remote, branch, and live URL with your own verified values.
2. Create/select your own saved Codex project and adjust its expected label if it is not `game hub`.
3. Inspect your catalogue schema. The supplied workflow expects `src/App.tsx`, `ALL_GAMES`, and optional `FEATURED_GAMES`; adapt that section if your site differs.
4. Preserve the distinction between a request to publish a listing and a read-only catalogue question. Do not direct another user's task into the author's project.

### Deployment

The author uses GitHub `main` and Vercel for frontends and free services by default. The skill also records historical restrictions on Google Cloud billing and triggers. Those statements describe this setup; verify your own environment and customize the policy deliberately rather than treating those historic dates as current account facts.

Backend operations are opt-in. An absent backend declaration does not authorize installing a server or copying another game's endpoint. The Windows PC reference describes a separately implemented updater/watchdog design; neither that implementation nor a tunnel service ships with Ystack. Public machine-specific addresses, assigned ports, and key-expiry dates have been removed from the reference.

Record actual deployment IDs, production URLs, commands, checks, and limitations in each game's own `AGENTS.md`. The global file holds personal response and UI preferences; the reusable skill holds workflow guidance.

### ByteBrew and CrazyGames

Use your own accounts and game identities. Put SDK configuration in the appropriate runtime/environment system; do not commit credentials. ByteBrew's reference contains symbolic `WEB_APP_ID` and `WEB_SDK_KEY` examples, not working credentials.

The CrazyGames skill deliberately rechecks official requirements before use. A prepared draft is not a submitted or approved game. The skill retains its review steps and separate requirements for final submission and developer-completed legal fields.

## Expected interactions

### Understanding checks

- An explicit invocation produces a compact checklist: understanding, actions, consequential assumptions/questions, and completion criteria.
- Questions are numbered, even when there is only one.
- A small clear correction is folded in and work proceeds; it does not require another literal "continue".
- A substantial plan revision gets an updated checklist and renewed confirmation, subject to explicit instructions to proceed.
- A routine "Do you understand?" with a clear task gets a short normal answer.

### Sound work

A review without a requested sound change leaves active gameplay audio unchanged. It may add/update a preview page and start its server so you can listen one cue at a time. For a clear review-only invocation, use:

```text
Use $game-audio-review to review existing sounds and open the preview.
Do not change gameplay audio.
```

Requests to create, replace, tune, or repair effects use the same preview workflow. Existing preview pages and pending comparisons should be reused. Options stay outside gameplay until chosen; a requested fix or selected replacement can then be implemented. A small sound change does not automatically require a full audio audit.

### Manager mode

Under T3 Code, follow the root T3_SETUP.md guide and the T3 section of the manager tool protocol; the legacy desktop section does not apply. Master Project Manager is a persistent, explicit role for one project. It routes implementation to workers, maintains compact coordination notes, and normally returns after dispatch rather than waiting for completion. Do not add that role to global or project `AGENTS.md`: ordinary workers must remain ordinary workers.

Its tool protocol is a snapshot of the author's desktop environment. Live tool contracts take precedence. In particular, use current supported status/wait tools for following a specific task to completion; do not create an automation to track a specific task's milestone or completion. Scheduling is for genuinely future reminders, recurring reports, and standing alerts when requested.

## Global preferences

Adopt the parts of root `AGENTS.md` you want. It intentionally prefers:

- A warm, natural, professional tone that stays candid about problems.
- Plain-language recommendations and ownership of routine technical decisions, with questions focused on outcomes and meaningful tradeoffs.
- Simple game screens with minimal text.
- Generated artwork rather than elaborate SVG artwork for game backgrounds/icons.
- No game title/icon on game-over screens and no native game scrollbars.
- Normally three rendered visual proposals, with another count whenever requested.
- Images of actual implemented results, or GIF/video when motion matters.
- Code-driven preview rendering with minimal computer use.
- Only handled development-server, app-preview, or live-app URLs quietly on the final line of user-facing answers; no URLs in reasoning summaries or progress commentary. Other useful links remain in the answer body and must never be withheld because of the footer rule.

These defaults do not imply that SVGs cannot be used to render previews, that every request needs multiple proposals, or that Codex should invent a URL when no server exists. The skills do not replace the host's higher-priority instructions or tool restrictions.

The global file also records the author's standing request to synchronize instruction and published-skill changes to this repository in the same task. That maintenance rule applies to the author's own setup. If you adopt the global file, replace its repository with your own fork or remove that section; the distributed file does not give you permission to write to the author's repository. Keep private configuration and machine details out of any public sync.

## Updates, backups, and removal

To update, pull the repository, review the diff, and rerun the installer with the same destination/selection plus `--force`. Existing skill folders are moved to `<skills-directory-parent>/.ystack-backups/<timestamp>/skills/`. If global instructions are explicitly replaced, their backup goes to `<codex-home>/.ystack-backups/<timestamp>/AGENTS.md`. Paths are printed during installation.

To restore, close/restart the affected Codex session as needed and copy the desired backed-up file/folder back to its original destination. Check for subsequent local edits first. For removal, remove only the skill folders you installed from Ystack, preserving any local customizations. Global instructions require separate manual restoration; the installer never silently merges them.

To scope skills to one repository, install with `--skills-dir /path/to/project/.agents/skills`. For a legacy user directory, use `--skills-dir ~/.codex/skills`. Avoid duplicate copies with the same skill name across discovery locations. The default installation does not touch `config.toml` or alter an existing disabled-skill setting.
