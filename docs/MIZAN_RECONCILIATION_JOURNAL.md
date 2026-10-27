# MIZAN CORE — Durable UNKNOWN Reconciliation Journal

## Why this exists

The execution store treats `UNKNOWN` as terminal: uncertainty must not silently trigger a second external action. Reconciliation is therefore a durable record of what independent evidence says about the earlier external effect; it is **not** a transition that reopens the original execution.

## Contract

`src/mizan_reconciliation_journal.py` adds an append-only-by-API journal in the same SQLite database as `SQLiteExecutionStore`.

- A record may be added only when the referenced execution currently has status `UNKNOWN`.
- The observed result must be `SUCCEEDED` or `FAILED`; unresolved evidence cannot be recorded as a final observation.
- The record requires an evidence reference, the SHA-256 digest of the evidence artifact, a named actor, and a timestamp.
- A database transaction serializes concurrent writers. At most one reconciliation record can be committed per execution.
- Each record is included in a separate global SHA-256 chain with a contiguous sequence number. The verifier checks sequence, hash links, row contents, source execution status, and unique execution coverage.
- Recording reconciliation does not mutate the original execution, authorize a new intent, call a provider, dispatch work, or retry an external effect.

## Evidence boundary

The evidence reference and digest provide traceability and detect accidental or unauthenticated record changes inside this journal. They do **not** independently establish that the source document is genuine, that the digest was produced by a trusted collector, or that the external system's report is truthful. A separate WITNESS/governance procedure must authenticate and evaluate the evidence before the observation is trusted.

A subsequent action, where policy allows one, must use a distinct intent/execution and an explicit provenance link to this terminal execution. This journal deliberately does not automatically create or execute that new intent.

## Tests

`tests/test_mizan_reconciliation_journal.py` covers:
- recording an observed outcome while the original execution remains `UNKNOWN`;
- refusal to reconcile a non-`UNKNOWN` execution;
- required outcome and evidence digest/reference;
- rejection of a second reconciliation for the same execution;
- concurrent writers with distinct executions (contiguous, valid hash chain);
- concurrent attempts to reconcile one execution (one winner);
- tamper detection for evidence digests.

These are local SQLite software regression tests. They do not prove external evidence authenticity, production PostgreSQL atomicity, or exactly-once effects at a remote provider. The PostgreSQL concurrency harness remains a separate test and must target only the designated test project.
