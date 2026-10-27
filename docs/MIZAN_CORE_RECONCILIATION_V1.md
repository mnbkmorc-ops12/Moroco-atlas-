# MIZAN CORE — External Outcome Reconciliation v1

## Invariant

Authorization to execute and confirmation of an external effect are separate facts.
A timeout or lost response may leave the outcome **UNKNOWN** even if the external
system completed the action. MIZAN must not infer success or failure from transport
failure alone.

## State rules

- `PENDING -> RUNNING`: authorized dispatch may begin through the governed executor.
- `PENDING/RUNNING -> UNKNOWN`: record a non-empty uncertainty reason.
- `UNKNOWN` is terminal for the original execution and never automatically replayable.
- Reconciliation produces a separate observation (`SUCCEEDED` or `FAILED`) backed by
  an evidence reference. It does not overwrite or reopen the original `UNKNOWN` state.
- `src/mizan_reconciliation.py` is a pure policy model; it does not authenticate evidence
  or provide durable storage.
- `src/mizan_reconciliation_journal.py` stores evidence reference + SHA-256 digest in
  a separate durable hash chain in the execution store's SQLite database. It records
  the observation without changing execution state or dispatching work.

## Evidence and execution boundary

A reference and digest enable traceability and tamper detection in the stored record,
but do not by themselves prove the external document is genuine. A trusted WITNESS
process must authenticate the source, check the observed operation ID against the
original request, and verify the evidence digest before trusting the observation.

Any subsequent action must be a **new governed intent** with explicit provenance to
the terminal execution and the reconciliation record. This code does not create that
intent automatically and never retries the prior external operation.

## Verification scope

Unit tests cover state transitions, retry blocking, durable reconciliation, unique
reconciliation per execution, concurrent writes, and journal tamper detection. They
do not prove exactly-once execution across independent systems or evidence authenticity.
Production PostgreSQL concurrency and provider-specific idempotency/reconciliation
remain separate integration tests.
