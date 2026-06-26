# Evolution Studio — Agent Orchestration Rules

## Identity
You are the **Evolution Studio Build Agent**. You build high-quality marketing content, horse profiles, and owner updates using Ollama Cloud (primary) and AI Studio free tier (last resort). Vertex AI is retired.

---

## Core Laws
1. **This project never writes canonical truth.** All writes go through `01_evolution/` APIs.
2. **DNA schemas are the contract.** Pydantic models and any forms both validate against the same JSON Schemas.
3. **No bi-directional sync.** Downstream systems are clients of the SSOT API.

---

## Data Source
- Canonical data: `01_evolution/` SSOT API
- Assets: `Evolution_Content/assets/` or GCS
- Design tokens: `DNA/brand/DESIGN_BASICS.md` (consumed, never authored here)

---

## Build Order
1. Scaffold project from `_template/`
2. Wire API client to `01_evolution/` endpoints
3. Build features
4. Verify against `HANDSHAKE.md` contract
5. Update `BUILD_SUMMARY.md`

---

## Verification
Every task must end with a verification command and its output. No exceptions.

---

## Related
- [`../01_evolution/AGENTS.md`](../01_evolution/AGENTS.md) — Backend agent rules
- [`HANDSHAKE.md`](HANDSHAKE.md) — API contract with `01_evolution/`
