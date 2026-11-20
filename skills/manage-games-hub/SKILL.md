---
name: manage-games-hub
description: Add, update, or publish game listings in Yigit Efe Oktar's Games Hub. Use when explicitly invoked or when the user requests a Games Hub listing change in natural language, such as "put it on my website", "add this game to my site", or "update its Game Hub listing", when context identifies the website as the user's Games Hub, including clear follow-ups. Do not activate for unrelated website work or a passing mention of the hub. Gather listing details, then route implementation to the saved game hub project; do not launch a chat for read-only questions.
---

# Manage Games Hub

Maintain the Games Hub catalogue without changing unrelated games or page design. New listings are catalogue-only by default unless the user explicitly requests another placement. Do not ask whether to feature a game when the user has not requested it.

## Repository and deployment

- GitHub repository: `yigitefeoktar/game-hub`
- Repository URL: `https://github.com/yigitefeoktar/game-hub`
- Default branch: `main`
- Live Games Hub: `https://game-hub-nu-three.vercel.app`
- Pushing an accepted commit to `main` triggers the existing Vercel deployment.

Clone the repository when it is not already available locally. If it is available, fetch and fast-forward it before editing unless the worktree contains user changes. Never discard unrelated changes.

## Start the Game Hub task

For a user request to add, update, or publish a game listing, first gather the listing details in the current conversation. Use values the user supplied or that can be reliably verified from the game repository and its production deployment. For a new listing, resolve the displayed name, one of the supported status tags, the playable production URL, and an icon file or source. Use catalogue-only placement unless the user explicitly requests otherwise; include that resolved placement in the publishing chat without asking for confirmation. Ask the user for only the missing or ambiguous decisions; group related questions when practical. If the user explicitly requests featured placement, inspect the existing featured schema and obtain any additional subtitle, description, or cover asset needed for that entry. For an existing listing, determine which fields the user actually wants changed and preserve the rest, including its existing placement unless the user requests a placement change. Do not require the user to repeat values already known.

Once the required details are settled, use Codex project tools to find the saved local project labeled `game hub` (verify its repository path or Git remote rather than assuming a project ID). Create a new visible, normal Codex chat in that project using its existing local folder. Call `create_thread` with `target.type: "project"`, the verified `projectId`, and `target.environment: { type: "local" }`. Do not select a worktree environment or create a separate Git worktree for this workflow. Give the task the resolved values, source paths or URLs for assets, the user's requested scope, and an explicit instruction to execute the catalogue, validation, and deployment steps below **in that task** without creating another task. The source conversation must not edit or deploy the Game Hub itself. Open the created task in the app when it has a ready task ID so the user can watch and continue there, and wait for its first progress. If project setup is still queued, report that state and do not treat its client ID as a ready task ID.

If already working in the saved Game Hub project on a task explicitly assigned to execute the listing change, do the work there instead of creating a duplicate task. Never launch a new task merely to answer a question or inspect the catalogue. If the saved project cannot be found, ask the user to add it rather than creating a projectless task or working in a different repository.

## Canonical catalogue schema

Game catalogue data is defined in `src/App.tsx`.

Every ordinary game belongs in `ALL_GAMES` and needs these four user-facing values:

```ts
{
  id: 'unique-lowercase-slug',
  title: 'Game Name',
  iconUrl: '/icons/game-icon.png',
  gameUrl: 'https://production-game.example',
  status: 'Live',
}
```

- `title` is the displayed game name.
- `status` is the displayed tag. Supported catalogue values are `Live`, `Beta`, `Prototype`, and `Coming Soon`.
- `gameUrl` stores the playable production URL. URLs are stored directly on each game object, not in a separate configuration file.
- `iconUrl` is normally a root-relative `/icons/...` URL backed by a real file in `public/icons/`.
- `id` must remain unique and stable. Use a lowercase hyphenated slug for new games.

The current code sorts games by status and then title. Do not manually rearrange entries merely to alter display order.

## Update an existing game

1. Search `src/App.tsx` by the game's `id`, title, current URL, and icon filename.
2. Update only the fields requested by the user.
3. A featured game may exist in both `FEATURED_GAMES` and `ALL_GAMES`. Update every applicable occurrence so its name, URL, icon, or tag does not become inconsistent.
4. Preserve its ID, description, status, cover, and other metadata unless the user asked to change them.
5. Search for the old value afterward and confirm no stale applicable occurrence remains.

For featured entries, `FEATURED_GAMES` uses `tag` rather than `status` and may also include `subtitle`, `description`, and `coverUrl`. A featured cover is normally referenced as `/assets/...` and backed by `public/assets/`.

## Add a new game

1. Use the name, tag/status, production URL, icon, and placement resolved before this task was created. If no other placement was explicitly requested, use catalogue-only without asking. Ask only if an essential value remains unavailable or a source proves inconsistent.
2. Put the icon file in `public/icons/` with a stable descriptive filename.
3. Add one unique entry to `ALL_GAMES` using the canonical schema above.
4. Add the game to `FEATURED_GAMES` only if the user explicitly requested featured placement.
5. Do not add a GitHub project card or change unrelated metadata unless requested.

If any required value is missing and cannot be found from the game repository or deployment, ask for it rather than inventing it.

## Validate and publish

1. If dependencies are absent, run `npm install --no-package-lock` so validation does not introduce an unrequested lockfile.
2. Run `npm run lint`.
3. Run `npm run build`.
4. Run `git diff --check`, inspect the complete diff, and confirm only intended catalogue/assets changed.
5. Confirm the game URL responds successfully and every referenced icon or cover file exists.
6. Commit the intended files and safely push the commit to `origin/main` when the user has authorized publishing through the established direct-to-main workflow. From a worktree branch, ensure the push is a fast-forward of `main`; do not force-push or discard newer remote work.
7. Wait for the live Games Hub deployment. If Vercel marks the new production deployment as `Staged` or reports that custom-domain assignment was skipped because an Instant Rollback is active, explicitly promote that deployment before testing the public domain.
8. Verify the live card displays the right name/tag/icon and opens the intended URL. Checking only a protected deployment URL or source bundle is not enough.
9. Report the commit, live Games Hub URL, and playable game URL.

Never expose credentials, add analytics, alter game code, or redesign the hub as part of a catalogue-only request.
