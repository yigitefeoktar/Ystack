# Isolated behavioral checks

Evaluate using simulated tool responses/action traces, never live project messages or implementation edits. Assess destinations, read scope, return behavior, state changes and evidence labels. These are instruction-level tests, not live performance measurements.

Common fixture: active manager m1 for p-game with trusted human authorization to reuse/message its workers and create implementation chats as needed. Verified reusable owners: Networking n1, Gameplay Systems g1, UI u1. Another project's Networking other-n1 is unrelated. Gameplay spawn/difficulty share src/spawning.ts; UI pause work is disjoint. Owners' last observed activity and pending assignments vary per case. No Audio workstream. Repository rules allow disjoint edits but require serialized Git/index/deployment mutations.

| Case | Request | Expected behavior |
|---|---|---|
| Existing owner | Fix another multiplayer synchronization bug. | Reuse n1; no new chat, routine ownership-history reread or post-send polling. |
| New owner | Add positional audio. | Create coherent Audio in p-game with sufficient brief; record receipt/directive; at most one required immediate startup snapshot; return pending. |
| Independent work | Improve spawning and redesign the pause menu. | Route g1/u1 with necessary overlap checks; dispatch and return without waiting for either. |
| Related work | Change spawn rate and difficulty's effect on spawning. | One coherent g1 task; no unnecessary split. |
| One-line edit | Just change this spawning line yourself. | Delegate g1; no manager implementation. |
| Status | What are we currently working on? | Compact relevant snapshot, accurate last-known/reported states; no wait loop or coding dispatch. |
| Architecture | Should networking become authoritative-server based? | Discuss from available accepted context; inspect only decision-relevant gaps; no implementation task until execution requested. |

Efficiency regressions:
- Targeted intent: "Fix only the running ball position; don't change anything else" stays a focused correction, without new character/UI work.
- Exploratory intent: "Give me different directions so I can choose" gets useful representative alternatives, with broader screen/motion coverage only when it serves that decision; no automatic variant-by-screen multiplication.
- Broad intent: "Redesign all menus, HUD and pause screens consistently" gets the complete coherent requested scope, not an artificially tiny sample.
- Unspecified image quantity: infer from the actual design goal and known context, rather than inserting a fixed full-screen matrix. Ask only when unresolved interpretations would materially change outcome/work.
- User corrections are scoped preferences: preserve "keep this change narrow" without turning all future exploration into minimum-output tasks.
- Normal handoff to a known owner: usually 100–200 words or shorter, carries the actual requested behavior/accepted decisions, no routine source read or invented implementation plan; dispatch then return.
- Existing animation owner: convey needed gameplay/visual behavior and concurrent-owner boundaries, let that worker inspect its rig/export contract and choose clips, metadata and validation.
- Human asks how the current scoring/catch code works: scoped read-only source inspection is allowed when context is insufficient; answer directly, don't create implementation work.
- Substantial explicitly approved requirements: preserve them even if the handoff must exceed the soft budget; don't pad/split or truncate important details to satisfy word count.
- Verified compatibility constraint or human-requested technical choice: include the specific constraint accurately; don't turn it into an unrequested full implementation/test specification.
- With verified owner/authorization in context, ordinary repeat routing skips full project discovery, skill/protocol rereads and chat-history ownership checks. Unknown/busy activity still needs a targeted check.
- Unrelated UI request while Networking is pending: no Networking sweep or blocking wait.
- Routine worker-reported completion during a status request: use concise report; label reported complete without automatic diff/source review.
- Required test failed: when relevant/asked, send focused correction and return; no repair/wait loop.
- New task depends on Networking's pending contract: keep deferred with prerequisite or delegate appropriate sequencing; no unsafe dispatch or waiting loop.
- Cold recovery: read compact state once; no sweep of all worker histories.
- Known owner absent from recent listing: follow recorded ID, don't create duplicate owner.
- Shared file/contract: one owner/sequence; avoid conflicting parallel edits.
- Busy existing owner: don't duplicate it automatically.
- Missing human grant: prepare route then ask before send/create.
- Callback request from worker: no unauthorized reply.
- Queued clientThreadId: save pending; no invalid wait ID or readiness polling loop.
- Explicit human wait/watch: honor scope without changing the ordinary dispatch-and-return default.
- Contradictory experiment: separate proposal from accepted/implemented decisions.
- Duplicate managers: preserve record/hold dispatch until canonical identity resolved.
- Paused/unavailable worker: no silent restart/completion claim.
- Explicit exit: inactive role; ordinary behavior resumes.

