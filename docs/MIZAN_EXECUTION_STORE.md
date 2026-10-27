# MIZAN CORE — Durable Execution Store

## Purpose

`src/mizan_execution_store.py` is a local SQLite reference implementation for the MIZAN execution journal. It is designed to make claim ownership and execution-state changes atomic and auditable. It does not execute commands or call external services.

## Invariants

1. **Immutable identity:** an `execution_id` is bound to one `intent_id`, one `idempotency_key`, and one SHA-256 request digest. Reusing the ID with different data is rejected.
2. **Single claim:** `claim_once` takes a SQLite `BEGIN IMMEDIATE` transaction and changes only `PENDING → CLAIMED`. Competing claimants cannot both win.
3. **No automatic reclaim:** `CLAIMED` is never returned to `PENDING` by this API. A process restart or lost worker is not proof that no side effect occurred.
4. **Unknown remains terminal:** `UNKNOWN` cannot be reopened. Investigate/reconcile the external system and create a new explicitly linked intent after evidence establishes the prior outcome.
5. **Compare-and-set transitions:** callers provide the expected current state; stale or conflicting transitions fail.
6. **Audit trail:** each state change adds an event to a global SHA-256 hash chain. The verifier checks event sequence, hash links, legal per-execution transitions, event coverage, and agreement between the final event and each current execution row.

## Allowed transitions

- `PENDING → CLAIMED | CANCELLED`
- `CLAIMED → RUNNING | UNKNOWN | CANCELLED`
- `RUNNING → SUCCEEDED | FAILED | UNKNOWN`
- `SUCCEEDED`, `FAILED`, `UNKNOWN`, and `CANCELLED` are terminal.

This model intentionally has no automatic retry path. Retry policy, if ever required, must be a separate governed decision with evidence; it must not be implemented by changing a terminal record back to an executable state.

## Test coverage

`tests/test_mizan_execution_store.py` covers:
- concurrent attempts to claim one execution (24 callers; exactly one winner expected);
- immutable execution identity and idempotency-key ownership;
- terminal `UNKNOWN` behavior;
- compare-and-set rejection of stale status;
- terminal state enforcement;
- missing execution rejection; and
- detection of an out-of-band status change that does not match the audit trail.

The tests are software regression tests, not a certification that every database/runtime configuration is safe.

## Important boundary

A local transaction can guarantee one database claim in this store. It cannot, by itself, guarantee exactly-once behavior for an external side effect. For example, a worker may send a request to a remote service and crash before recording the response. In that case, the correct state is `UNKNOWN` until the remote service is independently reconciled. Prefer end-to-end idempotency keys and provider-side status queries where the external system supports them.

This file is not the production Supabase ledger. Do not point test scripts at the primary project. The independent PostgreSQL concurrency harness remains unexecuted until it is explicitly configured for the test project and run with correct credentials.
