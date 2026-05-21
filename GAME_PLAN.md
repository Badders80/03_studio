# {{PROJECT_NAME}} — Game Plan

**Status:** 🔴 Phase 0 — Scaffolding
**Created:** {{DATE}}
**Last Updated:** {{DATE}}

---

## Workspace Boundary

| Workspace | Purpose | What Lives Here |
|-----------|---------|-----------------|
| `{{PROJECT_FOLDER}}/` | **{{ROLE}}** | {{WHAT_IT_BUILDS}} |

**Rule:** This project never writes canonical truth. It consumes from `01_evolution/` via HTTP API. All data flows: `{{PROJECT_FOLDER}}/` → `POST /api/...` → `01_evolution/` → Firestore/GCS.

---

## Goal

{{ONE_SENTENCE_GOAL}}

**Scope:**
- {{SCOPED_ITEM_1}}
- {{SCOPED_ITEM_2}}

**Non-Goals (current phase):**
- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}

---

## Architecture Decisions (Locked)

| Decision | Choice | Rationale | Date |
|----------|--------|-----------|------|
| Tech stack | {{TECH}} | {{WHY}} | {{DATE}} |

---

## Phase 1 Definition of Done

1. {{CHECKPOINT_1}}
2. {{CHECKPOINT_2}}
3. No errors in production build
4. Integration with `01_evolution/` APIs verified

---

## Related Documents

- **Current status:** [`MEMORY.md`](MEMORY.md)
- **Agent rules:** [`AGENTS.md`](AGENTS.md)
- **API contract:** [`HANDSHAKE.md`](HANDSHAKE.md)
- **Build map:** [`BUILD_SUMMARY.md`](BUILD_SUMMARY.md)
- **Task hub:** [`../01_evolution/docs/PROGRESS.md`](../01_evolution/docs/PROGRESS.md)
