# MIZAN CORE decision and execution state machine

## Decision semantics

- `AUTHORIZED`: explicit rule match and all required evidence items are present, structurally valid, and marked independently verified.
- `DENIED`: explicit policy/rule mismatch.
- `UNRESOLVED`: policy match may exist, but required evidence is missing or not independently verified.

This is a reference policy primitive, not a substitute for the deployed ORIS policy store, identity verification, or human safety review.

## Execution semantics

Allowed path:

`PENDING -> CLAIMED -> RUNNING -> SUCCEEDED | FAILED | UNKNOWN`

Additional safe transitions:
- `PENDING -> CANCELLED`
- `CLAIMED -> CANCELLED`
- `CLAIMED -> PENDING` only when no external action has started.
- `CLAIMED -> UNKNOWN` if claim expiry leaves external outcome uncertain.

Rules:
1. `UNKNOWN` is terminal for that intent. Reconciliation creates a new intent; it does not silently reopen the old one.
2. Never automatically retry an uncertain external effect.
3. `RUNNING -> PENDING` is forbidden.
4. Authorization does not itself execute an action.
5. Evidence is only considered verified when an independent verification process attests to it; the boolean flag in this local test model is not a cryptographic trust boundary.
6. These pure Python tests do not change Supabase or Base44 state.
