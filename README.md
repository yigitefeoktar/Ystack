# Ystack

An opinionated Codex setup for building, reviewing, and publishing browser games.

Ystack collects Yigit Efe Oktar's personal `AGENTS.md` and seven active skills: clear task confirmation, playable sound previews, observer-only analytics, deployment, publishing, and coordination across project chats.

The name is a nod to [Garry Tan's gstack](https://github.com/garrytan/gstack). Ystack is an independent collection, not a fork, port, or affiliated project. It does not include gstack code.

## What's included

| Skill | What it does | When to use it |
| --- | --- | --- |
| [Confirm Task Understanding](skills/confirm-task-understanding/SKILL.md) | A compact understanding checklist, numbered questions, and proportionate confirmation cycles | Explicit invocation, or consequential ambiguity after checking context |
| [Game Audio Review](skills/game-audio-review/SKILL.md) | Sound creation, tuning, diagnosis, and comparisons in a playable preview page | Sound-effect work you need to hear or compare |
| [ByteBrew Game Analytics](skills/bytebrew-game-analytics/SKILL.md) | Add or verify analytics without influencing gameplay | "Connect this to ByteBrew" and related integration or debugging requests |
| [Game Deployment](skills/game-deployment/SKILL.md) | GitHub `main` to Vercel; an optional, explicitly configured Windows backend | Deployment setup, repair, migration, or authorized releases |
| [CrazyGames Basic Launch](skills/crazygames-basic-launch/SKILL.md) | Verify the build, prepare media, and work through a portal draft | "Put the game on Crazy Games"; final submission has separate requirements |
| [Manage Games Hub](skills/manage-games-hub/SKILL.md) | Gather catalogue details and route a listing update to the correct project | "Put it on my website," when the website is the configured Games Hub |
| [Master Project Manager](skills/master-project-manager/SKILL.md) | Coordinate implementation chats without becoming an implementation worker | Explicit activation only; requires Codex desktop project/chat tools |

The three disabled personal skills (`ideate-web-games`, `prototype-web-games`, and `ship-web-games`) are intentionally not distributed here. System and third-party plugin skills are not bundled.

## Install

Requirements: Codex, Git, and Python 3.10 or newer. The installer uses only Python's standard library.

```sh
git clone https://github.com/yigitefeoktar/Ystack.git
cd Ystack
python scripts/install.py --dry-run
python scripts/install.py
```

On Windows, use `py -3` instead of `python` if that is your Python command.

The default destination is `~/.agents/skills`, the current documented user skill directory. Each skill is installed as its own folder. The command does **not** change your global instructions, enable integrations, create projects, or grant publishing permissions.

For an existing Codex installation that uses `~/.codex/skills`, select that directory explicitly:

```sh
python scripts/install.py --skills-dir ~/.codex/skills
```

Install selected skills with repeatable `--skill` options:

```sh
python scripts/install.py --skill confirm-task-understanding --skill game-audio-review
```

Existing destinations are never overwritten by default. To update installed copies, review the changes first, then run the same command with `--force`. Replaced copies are backed up outside the skill discovery folder, and the installer prints their paths. Do not install the same named skills in both user directories: duplicate names can appear in selectors.

Codex normally discovers skill changes automatically. If a skill does not appear, restart Codex and check for a disabling `[[skills.config]]` entry in your Codex configuration. Ystack does not edit that configuration. See the official [skill guide](https://learn.chatgpt.com/docs/build-skills.md).

### Personal AGENTS.md

[AGENTS.md](AGENTS.md) is the author's actual global preference file. It covers simple game UI, generated artwork, no native game scrollbars, code-rendered comparisons for small visual changes, generated concepts for major designs, and quiet URL links at the bottom of responses.

Read it before adopting it. The recommended approach is to merge the preferences you want into your existing `$CODEX_HOME/AGENTS.md` (usually `~/.codex/AGENTS.md`). They are preferences, not a universal requirement for every developer.

If you want the complete file instead, the installer can copy it explicitly:

```sh
python scripts/install.py --agents
```

An existing global file causes a preflight error unless you also pass `--force`; that creates a backup before replacement. `--codex-home PATH` selects a different destination, otherwise `CODEX_HOME` or `~/.codex` is used. Global `AGENTS.override.md`, if present, can take precedence. See the official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md).

## Try it

```text
Use $confirm-task-understanding to check this plan before implementing it: ...
```

```text
Use $game-audio-review to review this game's existing sounds and open the
preview page. Leave the gameplay sounds unchanged.
```

```text
Connect this game to ByteBrew. Keep analytics observer-only.
```

```text
Put this game on Crazy Games. Prepare the Basic Launch draft for my review.
```

```text
Use $master-project-manager to make this chat the manager of this project.
Reuse and message its implementation chats, and create new implementation
chats as needed.
```

The final example is a deliberate project-scoped delegation grant. Installing Ystack or discussing the manager skill does not activate the manager or provide that grant.

## Adapt it to your environment

These skills come from a real personal setup. **Games Hub still names the author's public repository and site. Configure your own hub before using it for publication.** The deployment skill also contains historical project references, Windows-specific backend conventions, and a preference for free services. These are not evidence that your accounts or machine have the same setup.

Read [setup and customization](docs/setup-and-customization.md) for project bindings, integration requirements, activation behavior, update/restore instructions, and limitations. The public PC reference omits personal machine endpoints and assigned ports; no credentials or runtime manager notes are included. The other skill files are snapshots of the installed collection; Master Project Manager is included without a workflow redesign.

## Repository layout

```text
Ystack/
  AGENTS.md                       Personal defaults; optional to install
  skills/<skill-name>/SKILL.md     Seven independent skill entrypoints
    agents/openai.yaml            UI metadata and invocation policy, if present
    references/                   Focused workflow references, if needed
    scripts/                      Skill-specific helpers, if needed
    assets/                       Sound preview component and styles, if needed
  docs/setup-and-customization.md Environment setup and usage details
  scripts/install.py              Local installer with dry run and backups
  scripts/validate.py             Package/frontmatter/reference validation
  tests/test_install.py           Isolated installer behavior tests
```

## Development

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The installer itself needs no third-party dependencies. Validation uses PyYAML. These checks validate packaging and installation, not a live deployment, ByteBrew ingestion, audio playback, or CrazyGames acceptance.

When changing a skill, keep its activation description accurate and update its supporting files and examples together. Test consequential behavior in an isolated workspace; do not use someone else's live project just to test routing. Contributions should preserve the distinction between user intent, tool access, and permission for external actions.

## License

MIT. See [LICENSE](LICENSE).

## T3 Code, Codex, and Claude Code

See [T3_SETUP.md](T3_SETUP.md) for the verified shared-source arrangement and current host-specific workflow. [CLAUDE.md](CLAUDE.md) is the Claude adapter: its relative import assumes the default sibling `.claude` and `.codex` homes. Preserve existing Claude instructions and adjust that import for a custom Codex home. Install the seven skill directories in Claude's personal skills directory, or link them to the same canonical sources used by Codex; do not replace existing linked folders blindly. Do not copy the author's synced third-party skills.

`--agents` installs AGENTS.md and its two companion guides, [T3_SETUP.md](T3_SETUP.md) and [YSTACK_MAINTENANCE.md](YSTACK_MAINTENANCE.md). Existing files are backed up with `--force`. It does not overwrite your Claude adapter or install Claude junctions. For Claude-only use, adapt the import to the location of your shared instructions and keep the companion guides alongside them. Invocation syntax and available tools depend on the provider/host; explicit-only manager behavior must also be respected when a host does not enforce Codex YAML metadata.

The host guide covers T3 project/thread tools, provider-aware delegation, workspace isolation, inline HTML visuals, shared-browser use, PR linking/watching, and secret handling. It does not grant permission to create chats or activate manager mode merely by installation.
