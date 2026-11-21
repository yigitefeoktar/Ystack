# Shared T3 Code setup

## Verified local arrangement

Both Codex and Claude Code are used through T3 Code. Claude's global CLAUDE.md imports the Codex global AGENTS.md. The seven personal Claude skill directories are Windows junctions to the corresponding canonical Codex skill directories. Preserve those links; editing a canonical skill updates both providers. Synced/system/plugin skills are separate and must not be copied into this collection. This records the verified arrangement, not a guarantee about another user's machine.

## Runtime decisions

- Ordinary coding needs no T3 orchestration. Use live session contracts as authority; tools can load late. Try a named tool before declaring it absent. Do not probe private app databases or credentials to replace a missing tool.
- Use native same-provider agents for bounded synchronous work when the requested model/settings fit; use delegate_task for cross-provider models, explicit settings, background work, or separate checkouts. Call orchestrator_capabilities once before the first delegation. Do not launch agents merely to inspect this setup. Honor the user's requested provider; report unavailable choices rather than switching.
- Delegates receive only their task. Supply essential context, constraints, acceptance, and ownership. Use isolation: worktree for a separate checkout; never create a child's checkout in a shell or its prompt. Follow a running delegate's returned next action without polling. Cancel obsolete tasks through task_cancel.
- Top-level chats are user-owned: create them only on an explicit request or an applicable explicit standing grant. Use t3_thread_launch for one chat or project-bound workspace; create_threads is not delegation. Read a given thread before discussing its state, retain returned links/IDs, and mention threads with their exact returned link. Discovery uses t3_project_list and t3_thread_search; an imported desktop ID is not automatically a T3 ID.
- For new top-level worktrees use workspaceStrategy, honor a requested base, and otherwise use the default remote branch for independent work. Local unpublished dependencies use their local base. Read or wait once after launch as required; a receipt is not completion. Manager dispatch normally returns pending; honor explicit waiting through current wait contracts. Never use reminders or scheduled jobs to monitor a specific run.
- For an image/mockup/chart requested in chat, use html_preview then html_render with self-contained HTML; no server is needed for that presentation. Keep the outer background transparent and follow live sizing/theme rules. For an image intended for external use, supply a PNG artifact. Existing audio/game preview servers remain useful for actual audition and browser interaction; do not start one merely to show a static visual.
- Browser work uses preview_status first, then preview_open if needed. Use preview tools only when browser work is requested, not to inspect every code edit. Public information otherwise uses web fetch/search. Follow current fallback rules; never silently switch browsers. Keep a tab open only when requested or in use by the user. Browser/upload/SDK tools available in one provider session may not be available in another.
- Request a user-only secret with request_secret; never ask for tokens/passwords in chat. Existing authenticated CLIs/connectors can be used without requesting credentials again.
- After creating or pushing a PR, immediately link it with link_pull_request/link_pull_requests. Use watch_pull_request for requested PR monitoring or work blocked on PR checks/reviews, following the live handback/unwatch contract. Do not substitute shell polling.
- Do not invent capabilities, successful deployment, browser/audio verification, or model identities. Preserve skill-specific activation, scope, and external-action boundaries.

For changes to this shared setup, see [YSTACK_MAINTENANCE.md](YSTACK_MAINTENANCE.md).
