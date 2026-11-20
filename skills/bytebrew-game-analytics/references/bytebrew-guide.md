# ByteBrew Game Analytics Guide

## Contents

1. [Official sources](#official-sources)
2. [How the SDK works](#how-the-sdk-works)
3. [Observer-only architecture](#observer-only-architecture)
4. [Reusable event design](#reusable-event-design)
5. [Run lifecycle and summaries](#run-lifecycle-and-summaries)
6. [Performance and reliability](#performance-and-reliability)
7. [Multiplayer authority](#multiplayer-authority)
8. [Dashboard runbook](#dashboard-runbook)
9. [Verification matrix](#verification-matrix)
10. [Troubleshooting](#troubleshooting)
11. [Privacy, credentials and releases](#privacy-credentials-and-releases)

## Official sources

Consult the official platform-specific documentation before implementation:

- JavaScript SDK: https://docs.bytebrew.io/sdk/javascript
- App settings and Events Manager: https://docs.bytebrew.io/dashboard/gamesettings
- Mechanics: https://docs.bytebrew.io/customworkspace/custommechanics
- Documentation home and other SDKs: https://docs.bytebrew.io/startup/home

Prefer official ByteBrew documentation and official packages over blogs or remembered method signatures.

## How the SDK works

ByteBrew is initialized once with the app/game ID, SDK key and app version. The JavaScript package documented at the time this guide was written is `bytebrew-web-sdk`:

```ts
import { ByteBrew } from "bytebrew-web-sdk";

ByteBrew.initializeByteBrew(WEB_APP_ID, WEB_SDK_KEY, APP_VERSION);
ByteBrew.newCustomEvent("run_started", {
  environment: "test",
  schema_version: "1",
});
```

Confirm the exact package and API in the current official SDK guide. Other engines and platforms use their own ByteBrew SDKs.

Custom-event names and parameter names should use simple underscore-separated identifiers. ByteBrew warns that spaces, periods and colons are not processed correctly. Prefer flat scalar values; avoid nested objects, arrays, binary data and unbounded strings unless the active SDK explicitly supports them.

Initialize early enough to capture the first run, but do not block the game on initialization. If initialization throws, log only in development and continue without analytics.

## Observer-only architecture

Place ByteBrew behind one adapter owned by the analytics layer:

```ts
type Priority = "critical" | "normal" | "sample";

interface AnalyticsTransport {
  send(name: string, fields: Record<string, string | number | boolean>): void;
}

function track(name: EventName, fields: EventFields): void {
  try {
    if (!enabled || !transport) return;
    const payload = enrichAndValidate(name, fields);
    enqueueOrSend(name, payload, EVENT_REGISTRY[name].priority);
    updateAnalyticsSummary(name, payload);
  } catch (error) {
    recordAnalyticsFailure(error);
  }
}
```

Important boundaries:

- Gameplay calls the adapter; the adapter never controls gameplay.
- Gameplay never waits for SDK initialization, delivery or responses.
- Analytics counters live inside the adapter and are derived from accepted events.
- Analytics code must not mutate gameplay entities or collections.
- Analytics must not consume the game's random-number generator.
- Do not expose ByteBrew objects throughout the codebase.
- An empty or invalid configuration should produce a no-op adapter.

Avoid changing a gameplay function's return value or control flow solely to support analytics. If context is missing, capture it after the decision from already-available state or omit the optional field.

## Reusable event design

Use semantic events that remain meaningful across game versions. Suggested generic categories:

| Category | Examples | Priority |
|---|---|---|
| Lifecycle | `run_started`, `run_paused`, `run_resumed`, `run_ended` | Critical |
| Player actions | `shot_fired`, `ability_used`, `item_used` | Normal |
| Outcomes | `enemy_defeated`, `objective_destroyed`, `player_defeated` | Normal |
| World events | `enemy_spawned`, `phase_changed`, `objective_engaged` | Normal |
| State observation | `player_state_sample` | Sample |
| Summary | fields attached to `run_ended` or a separate summary event | Critical |

Recommended shared fields:

- `schema_version`
- `environment` or `test_tag`
- `app_version` and build identifier
- `timeline_session_id` and `run_id`
- `event_sequence`
- `event_time_ms`
- `run_elapsed_ms` and active elapsed time
- `event_category` and `event_source`
- level/map, mode and difficulty
- device type, orientation and control scheme when relevant
- actor ID/type and position
- target ID/type and position
- outcome and cause code

Use stable IDs within a run for bullets, entities and objectives when correlation matters. Do not use player names, email addresses or other personal identifiers as correlation keys.

Define event metadata centrally:

```ts
const EVENT_REGISTRY = {
  shot_fired: { category: "action", priority: "normal", counter: "shots" },
  enemy_defeated: { category: "outcome", priority: "normal", counter: "kills" },
  player_state_sample: { category: "state", priority: "sample" },
  run_ended: { category: "lifecycle", priority: "critical" },
} as const;
```

This prevents spelling drift and lets future games extend the schema without rewriting the transport.

## Run lifecycle and summaries

Distinguish an app session from a gameplay run. A retry, load or new multiplayer round should usually create a new run ID even if it occurs within one app session.

Track:

- total duration;
- paused duration;
- active duration;
- start origin such as fresh start, retry, quick load, save-file load or multiplayer round;
- previous run ID when runs are linked;
- outcome, cause and completeness.

End an active run once. Starting a new run should close any unfinished prior run as abandoned when the product semantics support that. Browser backgrounding should normally pause observation rather than declare a run ended. An abrupt process or page close may leave a run without an ending event; treat the missing ending as incomplete data rather than fabricating an outcome.

Useful summary counters include actions, kills, meaningful spawns, objectives engaged/destroyed, abilities used, first-action timings, sample count, sampled travel distance, final score/state and dropped analytics counts.

Counters must be updated from events accepted by the analytics adapter. They must not feed back into gameplay state.

## Performance and reliability

Use this priority order when pressure occurs:

1. preserve lifecycle and final summary events;
2. preserve confirmed player actions and outcomes;
3. discard state samples first.

For periodic observation:

- default to one sample every five seconds;
- run outside the animation/physics loop;
- skip while paused or the document is hidden;
- never replay missed samples;
- gather only inexpensive scalar counts and positions;
- avoid nearest-object searches if they are expensive or already unavailable;
- cap queued samples and report skipped/dropped counts in the summary.

Do not retry forever. Bound memory and retry attempts. If the SDK provides its own batching, avoid adding a competing high-volume queue without evidence it is necessary.

Performance validation should include representative maximum entity counts. Compare frame time, input latency, simulation state and network behavior with analytics enabled and disabled. Optional observer callbacks should complete comfortably below one frame budget; target sub-millisecond work for ordinary hooks and samples when practical.

## Multiplayer authority

Analytics must respect the game's existing authority model:

- The authority that confirms an outcome is the source of truth for kills, damage, objective destruction, score and projectile removal.
- A guest may record its accepted local action after host confirmation, or receive an analytics-only relay from the host.
- Relayed analytics messages must be validated for room, round, owner, event allowlist and scalar bounds.
- Reject stale, duplicate, malformed and wrong-round messages.
- Never let the analytics relay modify match state or trigger gameplay events.
- Keep guest predictions out of outcome analytics.

If the product needs per-player timelines, route a confirmed world event to the relevant owner without duplicating it for every guest. Deduplicate by event ID or authoritative sequence.

## Dashboard runbook

### Obtain configuration

Open the ByteBrew app, then **Settings → Game Settings**. Copy the platform's app/game ID and SDK key into the application's runtime secret or environment-variable system. Do not paste credentials into source files, issues, logs, screenshots or chat responses.

For browser games, client credentials cannot be perfectly hidden. Environment variables prevent accidental repository exposure but are not a security boundary once bundled into client code.

### Check real-time event registration

Open **Settings → Events Manager**:

1. Search for the expected event.
2. Confirm the event is enabled.
3. Expand it and verify the expected subparameters.
4. Confirm the test/environment field appears.

Events Manager is the fastest check that ByteBrew received an event name and learned its schema. It does not by itself prove exact event counts or a completed run summary.

### Check counts and values

Open **Custom Workspace → Mechanics**:

1. Select the correct date range. ByteBrew reporting uses UTC.
2. Add the event under **Events**.
3. Add subparameter filters such as environment, schema version, build, run ID or known test values.
4. Use Count unless another aggregate is required.
5. Add a breakdown such as date, build, device or an event subparameter when useful.
6. Choose a chart type and press **Apply**.
7. Read the graph and data table.

Mechanics supports count, unique and average aggregates plus average, median, sum, minimum and maximum aggregation of event subparameters. Formulas can compare multiple configured events.

### Controlled verification run

Before playing, write down expected actions, for example:

- start one run;
- perform a known number of manual actions;
- use each ability once;
- create one known outcome;
- pause/resume once;
- end the run normally.

Then verify:

- all event names and fields in Events Manager;
- exact counts and filtered values in Mechanics;
- one start and one normal ending;
- summary counters equal event counts;
- generated/projectile side effects do not inflate manual-action counts;
- the environment/test tag is present on every event.

If Mechanics does not yet show the run, do not claim count verification. Recheck UTC range, filters, event status, build/schema values, blockers and SDK initialization. Report event registration separately from aggregate verification.

## Verification matrix

### Unit and integration tests

- correct enrichment and environment tag;
- missing configuration produces a no-op;
- unavailable or throwing transport does not escape;
- events after run end are ignored;
- end is idempotent;
- a new run closes or rejects an unfinished run according to policy;
- paused time is excluded from active duration;
- counters and first-action timings are correct;
- samples pause, skip and drop correctly;
- critical events survive queue pressure;
- duplicated multiplayer relays are ignored.

### Regression tests

- existing single-player tests;
- multiplayer authority and reconnect tests;
- projectile/collision tests;
- save/load and retry tests;
- type checking, linting and production build.

### Equivalence test

Run a deterministic scenario twice with identical inputs and seed:

1. analytics enabled with a fake or recording transport;
2. analytics completely disabled.

Compare gameplay-visible state: positions, velocities, health, score, entities, outcome, random sequence and network messages. Any difference is a failed analytics integration.

### Manual validation

- normal completion;
- defeat;
- explicit quit/abandonment;
- retry;
- save/load when supported;
- pause and background/restore;
- offline or blocked ByteBrew transport;
- representative mobile and desktop devices;
- multiplayer host and guest when supported.

## Troubleshooting

### Event is absent from Events Manager

Check initialization, platform keys, app version, consent/tracking state, runtime configuration, browser blockers, network policy, import/package errors and event-name characters. Confirm the call happens after successful initialization without awaiting it in gameplay.

### Event exists but expected fields are absent

Confirm the event path actually executed, values are flat supported scalars, parameter names use safe characters, and the field is not disabled in Events Manager. Different paths may be emitting different schemas under the same name.

### Counts are too high

Look for duplicate callbacks, input plus outcome tracking of the same action, React lifecycle duplication, retries, host-and-guest double reporting, generated projectiles counted as manual shots and multiple endings. Add stable analytics event IDs and adapter-side deduplication.

### Counts are too low

Look for hooks before validation, early returns, dropped normal-priority events, incorrect ownership filters, run closure before delivery, wrong UTC range, wrong build/schema/environment filter and disabled event parameters.

### Summary differs from event counts

Ensure adapter counters update exactly when an event is accepted. Do not maintain separate gameplay-derived summary counters. Confirm the summary is sent after the final action/outcome and only once.

### The game stutters

Disable sampling first, then measure. Search for per-frame calls, entity-array serialization, synchronous storage, expensive distance calculations, console spam, unbounded retries and analytics inside inner collision loops. Preserve gameplay and reduce telemetry.

## Privacy, credentials and releases

- Collect gameplay information, not personal information.
- Avoid names, emails, chat text, IP addresses, device advertising identifiers or precise real-world location unless separately justified and consented.
- Use random run/session IDs rather than identity-derived IDs.
- Respect the SDK's consent and stop-tracking mechanisms where required.
- Keep keys in managed runtime configuration and redact them from outputs.
- Apply a centrally configured environment tag such as `test`, `staging` or `production` to every event.
- Never silently mix test and production data.
- Change the release tag only as an explicit release step after verification.
