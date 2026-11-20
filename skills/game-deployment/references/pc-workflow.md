# PC release workflow

Historical implementation reference: `yigitefeoktar/Ricochet-Arena`, directories `deployment/pc` and `deployment/skills/game-deployment`. This public copy documents the workflow; it does not include or install the updater, watcher, tunnel, or a running backend. Inspect the implementation and adapt it to the user's own repository before using it. Do not depend on uncommitted developer files. Install this skill from Ystack's `skills/game-deployment` folder. Keep any retired skill folders outside the active skills directory.

## Optional backend declaration

A frontend-only or deferred game uses `"backend": null` in `deployment.json`. Do not create a runtime installation for it. A later backend needs its own inspected code, enabled manifest, port/task names, HTTPS routing and smoke tests. Ricochet's current updater intentionally accepts only its implemented contract, not arbitrary commands or targets.

The historical example's `deployment.json` declares `main`, Vercel `build:frontend` output `dist/frontend`, and PC `build:backend` entry `dist/backend/server.cjs`. Private machine addresses and assigned ports are omitted from this public copy. Resolve a separate `BACKEND_PUBLIC_URL`, `BACKEND_PORT`, and `CANDIDATE_PORT` from the user's verified configuration; both ports must be loopback-only. Never reuse another game's endpoint or port allocation.

## Installation and updates

On the Windows PC, an installed bootstrap copy of `deployment/pc/update.cjs` polls its explicitly configured GitHub repository's main branch every minute. Its local JSON contains repository URL, bounded release/cache root, npm CLI path, candidate port, pointer/pause files, and activation/pruning script paths. Keep local machine paths and credentials out of GitHub; the implementation and runbook are versioned there.

The updater fetches the exact main SHA into an isolated cache and inspects the manifest **before npm install or any backend operation**. It archives that commit into its own release folder, runs `npm ci`, lint and the backend build, then starts a candidate on a different localhost port. Health and a two-client Socket.IO smoke test must pass before activation. The current release continues running during preparation. Activation stops only the recorded owned backend, changes the release pointer, restarts and health-checks it. Failure restores the old pointer and restarts the previous release. Retain active, previous successful and latest attempted release; prune only validated 40-character commit directories under the configured release root.

An independent Windows watcher restarts the active backend after a crash and starts at user sign-in. The updater also starts at sign-in. This installation does not run the game backend before Windows sign-in or after logout. Do not claim a system service is installed. Intentional pause prevents updates/recovery until the user resumes. Failed commits are recorded and retried on a new main SHA or a manual one-shot retry; avoid endless failed builds every minute.

Synchronization failures are retried on the next poll. Once GitHub main matches the active release again, the updater verifies local health and clears the transient failure without rebuilding or restarting that release. An unhealthy active release remains failed until health recovers. Build/probe/activation failures remain separate from synchronization failures.

Keep the small installed bootstrap stable during backend releases. If its code changes on GitHub, validate and explicitly refresh the installed copy as part of that task; backend polling does not replace its own running code.

## Public access and limits

For an explicitly configured installation, Tailscale Funnel publishes only the selected backend's loopback port through HTTPS. Verify whether background Funnel and the Tailscale Windows service are actually installed; this guide does not establish that they exist on another machine. Preserve network/auth/security settings and other routes. Inspect live Tailscale authentication and machine-key expiry instead of assuming a historical date applies. Funnel bandwidth restrictions and the PC/internet connection can affect lag. New free provider plan/terms claims require current official verification.

A browser blocked by client protections is not proof of a failed backend; preserve protections, test the public protocol and report the browser limitation. Real two-device mobile-data play remains a useful final user check.
