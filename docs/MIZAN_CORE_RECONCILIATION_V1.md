# MIZAN CORE — External Outcome Reconciliation v1

## Invariant

Authorization to execute and confirmation of an external effect are separate facts.
A timeout or lost response may leave the outcome **UNKNOWN** even if the external
system completed the action. MIZAN must not infer success or failure from transport
failure alone.

## State rules

- `PENDING -> RUNNING`: dispatch may begin through the authorized executor.
- `PENDING/RUNNING -> UNKNOWN`: record a non-empty uncertainty reason.
- `UNKNOWN -> SUCCEEDED/FAILED`: only through explicit reconciliation with an
  evidence reference (for example, a provider receipt or independently queried
  operation status).
- `UNKNOWN` is never automatically replayable.
- This reference module does not itself dispatch external work, verify evidence
  authenticity, or provide durable storage. Those require a trusted adapter,
  evidence validation, and a persistent append-only audit record.

## Verification scope

Unit tests cover transition rules and retry blocking. They do not prove exactly-once
execution across independent systems. That requires idempotency at the external
provider or a provider-specific reconciliation API, plus integration testing.
