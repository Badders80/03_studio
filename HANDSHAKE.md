# API Handshake — {{PROJECT_NAME}} ↔ 01_evolution

**Version:** 1.0
**Last Updated:** {{DATE}}

---

## Overview

This document defines how `{{PROJECT_FOLDER}}/` connects to the backend (`01_evolution/`).

**Architecture:**
```
{{PROJECT_NAME}} → HTTP API Calls → 01_evolution (GCP Cloud Functions)
```

---

## Backend Endpoints

### SSOT API
**Base URL:** `https://australia-southeast1-evolution-engine.cloudfunctions.net/ssot`

| Endpoint | Method | Use | Response |
|----------|--------|-----|----------|
| `/horses` | GET | Browse horses | `Horse[]` |
| `/horses/{microchip}` | GET | Horse detail | `Horse` |

### Assets API
**Base URL:** `https://australia-southeast1-evolution-engine.cloudfunctions.net/assets`

| Endpoint | Method | Use | Response |
|----------|--------|-----|----------|
| `/upload` | POST | Upload images | `{ asset_id, gcs_url }` |
| `/retrieve` | GET | Get images | `Asset[]` |

---

## Environment Variables

```env
NEXT_PUBLIC_API_BASE=https://australia-southeast1-evolution-engine.cloudfunctions.net
```

---

## Authentication Flow

```typescript
// Frontend: Login via Firebase Auth
const user = await signInWithEmailAndPassword(auth, email, password);
const idToken = await user.getIdToken();
```

---

## Error Handling

```typescript
try {
  const data = await apiCall('/endpoint');
} catch (error) {
  if (error.message.includes('401')) {
    router.push('/auth/login');
  } else {
    showToast('Something went wrong');
  }
}
```

---

## Related
- [`../01_evolution/api/README.md`](../01_evolution/api/README.md) — Backend API docs
