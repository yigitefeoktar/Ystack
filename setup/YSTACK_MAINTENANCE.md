# Ystack maintenance

This guide applies when maintaining Yigit Efe Oktar's shared Codex and Claude Code instructions or a personal skill published in [Ystack](https://github.com/yigitefeoktar/Ystack). The procedure works from the dedicated maintenance chat or any regular chat where Yigit asks for an edit. For the shared files and provider setup, see [T3_SETUP.md](T3_SETUP.md).

1. Identify the canonical installed file and its matching public copy. Shared instruction files are under `setup/` in Ystack. Published skills are under `skills/`. Codex and Claude Code share those sources, so edit each canonical source once. Verify the Ystack checkout and its Git remote before publishing.
2. Update the matching Ystack files and any affected usage documentation in the same task. Preserve public redactions and portability notes. Keep credentials, private endpoints, runtime state, and unrelated system, plugin, or disabled skills out of the public repository.
3. Run the relevant validation described in the repository setup guide. Review the diff, preserve unrelated work, and safely reconcile newer remote changes. Commit and push the task changes to `main` under Yigit's standing authorization for this sync.
4. Report what changed and whether it was published. If synchronization is blocked, say what still needs to be synced and why.

For adopters, keep personal changes local or point your maintenance instructions at your own fork. Yigit's standing authorization applies only to his setup.
