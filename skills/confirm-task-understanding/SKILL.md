---
name: confirm-task-understanding
description: Confirm task understanding when explicitly invoked, or clarify consequential uncertainty that remains after checking available context. Do not activate merely for typos, informal wording, or a routine question such as "Do you understand?" when the task is clear.
---

# Confirm Task Understanding

In T3 Code with Codex or Claude Code, follow the shared global instructions and `T3_SETUP.md` runtime guide. Use the current session tools instead of assuming Codex desktop APIs or plugins; preserve this skill's activation and authorization boundaries.

## Purpose

Help the user deliberately check a task interpretation, or resolve uncertainty that could cause meaningfully different work. Keep clarification conversational and proportional.

## When to use this skill

- **Explicit invocation:** Use the confirmation workflow when the user invokes `$confirm-task-understanding` or deliberately requests that workflow.
- **Implicit activation:** Use it only when you genuinely cannot determine an important part of the intended task after checking relevant available context. Plausible interpretations must lead to meaningfully different outcomes, scope, or work.
- A casual "Do you understand?", "What did you understand?", or request to explain a plan or assumptions is not by itself an invocation. When the task is clear, answer briefly in ordinary conversation without a formal checklist or extra confirmation cycle. Follow any explicit instruction to wait before acting.
- Typos, rushed wording, a short prompt, or safely inferable details alone do not justify activation. Correct obvious spelling silently and proceed with reasonable assumptions; mention an assumption briefly only when useful.
- Discussing, reviewing, or editing this skill does not itself activate its confirmation workflow.

## Explicit confirmation workflow

Inspect relevant context read-only first when needed to produce an accurate interpretation. Present a compact checklist using these labels:

- **My understanding:** The goal, concrete deliverable, and important constraints.
- **What I'll do:** A short sequence of the main actions.
- **Assumptions or questions:** Only consequential assumptions or unresolved questions; omit this item when unnecessary.
- **Done means:** The observable result that counts as completion.

Keep each item brief and proportional to the task. Omit empty sections; do not require confidence ratings, "safe/material" labels, or an exhaustive form. This checklist is the default for explicit understanding checks. Implicit clarification uses a focused question instead.

Wait for confirmation before implementing unless the user explicitly says to confirm and continue automatically. A short invitation such as "If that matches your intent, say continue; otherwise correct it" is sufficient. Handle corrections to that invitation as described below; a minor correction does not require the literal word "continue". With confirm-and-continue authorization, state the interpretation and proceed unless consequential uncertainty remains unresolved. Respect existing authorization and actual tool requirements; this skill does not create new permission requirements or grants.

## Clarify consequential uncertainty

1. Identify the specific uncertainty and why the answer would change the work.
2. Check relevant conversation, files, tools, or current state for discoverable answers. Keep inspection scoped; do not ask the user for information you can safely discover.
3. If uncertainty remains consequential, ask the smallest useful question, explaining the differing outcomes when helpful. Prefer one focused question over a full task restatement.
4. Hold only the work that depends on that answer; continue useful independent work when possible. Do not silently choose between materially different interpretations.

Once the answer resolves the uncertainty, continue within the user's authorized scope without adding a separate confirmation round. If the apparent ambiguity is resolved by context or a safe assumption, proceed normally without this workflow.

## Number questions

Always present questions as a numbered list starting at 1, even when there is only one question. Apply this to explicit understanding checks, implicit clarification, and follow-up questions. Give each independently answerable question its own number so the user can reply by number. Keep assumptions and explanations separate from the numbered questions, and match numbered answers to their questions without requiring the user to repeat them.

## Corrections and continuation

Treat user corrections as explicit instructions and update the interpretation immediately. When replying to a confirmation request:

- **Minor, clear adjustment:** Fold it into the plan, briefly acknowledge the change, and proceed without another confirmation cycle or requiring the user to say "continue". Examples include changing a label, color, parameter, or small detail while retaining the same goal, deliverable, and overall scope. A clear minor correction is sufficient direction to proceed with the adjusted plan; silence is not.
- **Significant plan change:** Present an updated compact checklist, focusing on what changed, and ask for "continue" again before implementing the revised plan. This applies even when the new instructions are clear if they substantially change the goal, deliverables, scope, or overall approach. For example, replacing a targeted fix with a full redesign warrants another cycle.
- Judge significance by the impact on the work, not the length of the user's message. If a correction leaves consequential uncertainty, ask the focused question needed to resolve it. Avoid repeating the whole plan for a small adjustment.
- Honor explicit instructions to wait, keep discussing, or proceed with the revised plan, including confirm-and-continue authorization. Do not infer permission for separate consequential actions from a minor correction.

After confirmation or a resolving answer, execute the agreed task without reopening settled decisions. Reconfirm significant revisions as above; otherwise ask again only for new consequential uncertainty.

Preserve the user's scope and priorities. Do not add features or change completion criteria during clarification. Distinguish inspected facts from assumptions and unknowns, and never treat silence as approval. Before reporting completion, compare the result with the agreed outcome and identify any unmet conditions honestly.
