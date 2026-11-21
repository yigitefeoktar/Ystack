---
name: bytebrew-game-analytics
description: Add, audit, verify, or repair observer-only ByteBrew game analytics. Use when explicitly invoked or when the user requests ByteBrew work in natural language, such as "connect this to Bytebrew", "add ByteBrew analytics", "check the ByteBrew dashboard", or "fix missing ByteBrew events", including clear follow-ups to that work. Do not activate merely because a task mentions gameplay events, multiplayer authority, performance, or analytics without a ByteBrew connection established by the request or context.
---

# ByteBrew Game Analytics

In T3 Code with Codex or Claude Code, follow the shared global instructions and `T3_SETUP.md` runtime guide. Use the current session tools instead of assuming Codex desktop APIs or plugins; preserve this skill's activation and authorization boundaries.

Build useful gameplay analytics without letting analytics influence the game. Treat the current gameplay behavior as immutable unless the user separately requests a gameplay change.

Read [references/bytebrew-guide.md](references/bytebrew-guide.md) before integrating the SDK, designing a schema, controlling the ByteBrew dashboard, or diagnosing missing data. Check ByteBrew's official platform documentation before using exact SDK APIs because package names and methods can change.

## Non-negotiable guarantees

- Keep analytics observer-only. Gameplay must never read an analytics result.
- Never await analytics inside input, simulation, physics, rendering, spawning, scoring, or networking paths.
- Emit events only after the authoritative gameplay decision has already succeeded.
- Isolate SDK calls behind one small adapter. Catch SDK failures inside that adapter.
- Allow analytics to be disabled or unconfigured without changing gameplay.
- Do not add per-frame tracking, unbounded queues, or events inside collision-loop iterations.
- Prefer semantic events and coarse state samples over replay-level telemetry.
- Do not change rules, constants, timing, randomness, entity order, network authority, controls, UI, saves, or rendering merely to simplify analytics.
- Complete and verify related edits locally before committing when commits trigger deployment.

If an analytics requirement conflicts with one of these guarantees, preserve the game and reduce analytics detail.

## Workflow

### 1. Inspect before editing

Identify:

- game lifecycle boundaries: start, pause, resume, finish, retry, load, quit and abandonment;
- authoritative locations for actions and outcomes;
- existing analytics adapter, event names, environment configuration and tests;
- single-player versus multiplayer authority;
- high-frequency loops that must remain analytics-free;
- questions the data should answer and the minimum events needed.

Do not scatter direct SDK calls throughout gameplay files.

### 2. Define a stable semantic schema

Use a typed event registry or equivalent central schema. Preserve existing event names and fields when upgrading an established integration.

Prefer these event classes:

- lifecycle: run/session started, paused, resumed and ended;
- actions: shot accepted, ability used, item used or objective engaged;
- outcomes: enemy defeated, objective destroyed, player defeated or run won/lost;
- world events: meaningful authoritative spawns or transformations;
- optional state sample: coarse position and world-state observation on a fixed interval;
- final summary: counters, first-action timings, durations, outcome and completeness.

Attach stable common fields such as schema version, environment tag, app/build version, run ID, elapsed time, map/level, mode, control scheme, event source, actor/target type and relevant coordinates. Avoid personal information and unbounded payloads.

### 3. Integrate through an adapter

Keep the public surface small, for example:

- `initialize(config)`
- `beginRun(context)`
- `track(eventName, fields)`
- `pauseRun()` / `resumeRun()`
- `endRun(outcome)`

The adapter should enrich fields, maintain analytics-only counters, bound or drop low-priority work under pressure, and fail closed. Missing credentials, unavailable SDKs, browser privacy controls and transport errors must be harmless to gameplay.

### 4. Hook only confirmed outcomes

- Track input actions only after validation/acceptance.
- Track kills, destruction and scores only after the authoritative mutation succeeds.
- In host-authoritative multiplayer, let the host decide world outcomes; relay analytics-only observations to the relevant player when needed.
- Deduplicate retries, duplicated packets and repeated callbacks with analytics-owned IDs.
- Do not infer authoritative results on guests.
- Do not count ability-generated projectiles as manual shots unless the schema explicitly defines them that way.

### 5. Protect performance

- Keep hot-path hooks to a small object construction and a non-blocking adapter call.
- Sample state conservatively; five seconds is a safe default until profiling supports more frequency.
- Skip samples while paused, hidden, outside active play or under queue pressure. Never catch up missed samples.
- Drop samples before actions and outcomes. Preserve lifecycle endings whenever possible.
- Avoid serializing entire entity arrays, paths, frames, screenshots or replay streams.
- Profile representative worst-case entity counts and compare analytics enabled versus disabled.

### 6. Verify locally before dashboard work

Test the adapter with a fake transport. Cover disabled, missing and throwing SDKs; idempotent endings; pause-aware duration; counter accuracy; event enrichment; queue pressure; deduplication; and lifecycle transitions.

Run the existing game, multiplayer and save/load tests, type checking, linting and production build. Review the final diff specifically for gameplay conditions, constants, state mutations, random-number consumption, timing and network authority.

### 7. Verify in ByteBrew

Use a controlled run with known counts. If a signed-in dashboard tab is available, use it without exposing app keys.

1. Open the app's **Settings → Events Manager** to confirm event names and subparameters arrive and remain enabled.
2. Open **Custom Workspace → Mechanics** to query counts, filters, aggregates and breakdowns.
3. Set the correct UTC date range.
4. Filter by environment tag, schema version, build and run ID when available.
5. Compare dashboard results with the controlled run and final summary.

Do not claim exact-count verification when only the event schema is visible. Distinguish SDK initialization, event registration, event ingestion and aggregate-report verification.

### 8. Roll out safely

- Keep credentials in runtime configuration; never copy them into documentation or responses.
- Add an explicit pre-release/test tag to every custom event and make it centrally configurable.
- Ship the complete integration in one reviewed commit when automatic deployments are enabled.
- Start with semantic events and conservative sampling. Increase detail only after profiling and real analytical need.
- Report what was verified locally, what was verified in ByteBrew, and what remains pending.

## Completion standard

Consider the integration ready only when:

- analytics can be disabled with identical gameplay results;
- SDK failures do not surface to gameplay;
- authoritative events fire once with correct context;
- controlled-run counts reconcile or any dashboard delay is explicitly reported;
- the test/environment tag is present;
- no measurable frame-time or input regression appears;
- existing unrelated tests and behavior remain unchanged.
