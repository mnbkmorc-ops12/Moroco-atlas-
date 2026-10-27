# MIZAN CORE — recovery and engineering workspace

> **Doctrine:** لا سلطة إلا للمعنى — evidence before conclusion.

This repository consolidates MIZAN CORE materials recoverable from connected project history and accessible files. It is **not yet a complete export** of every historical Base44 screen, Supabase migration, or chat-only code fragment.

## Current layout

- `src/mizan_governance.py` — pure decision and execution-state rules (`AUTHORIZED`, `DENIED`, `UNRESOLVED`; terminal `UNKNOWN`).
- `src/mizan_execution_store.py` — durable SQLite execution journal, immutable execution identity, atomic `claim_once`, compare-and-set transitions, and tamper-evident event-chain validation.
- `src/mizan_reconciliation.py` — pure reconciliation policy; `UNKNOWN` stays terminal while observed outcomes remain separate facts.
- `src/mizan_reconciliation_journal.py` — durable evidence reference + SHA-256 journal for `UNKNOWN` executions; does not reopen or retry prior work.
- `src/mizan_sqlite_ledger.py` — local v0.5 reference ledger with `BEGIN IMMEDIATE`, idempotency enforcement, hash-chain verification, and transactional head updates.
- `tests/test_mizan_governance.py` — governance decision and state-transition regressions.
- `tests/test_mizan_execution_store.py` — concurrent claim competition, immutable identity, terminal UNKNOWN, compare-and-set and audit-tampering tests.
- `tests/test_mizan_reconciliation.py` — UNKNOWN terminal policy and evidence-gated observation model.
- `tests/test_mizan_reconciliation_journal.py` — durable reconciliation, concurrent writers, unique resolution, and evidence-tamper tests.
- `tests/test_mizan_sqlite_ledger.py` — isolated ledger tests including 100 concurrent appends across 10 workers.
- `archive/recovered/mizan_core_v0_1.py` — earliest recovered engineering registry and quarter-car simulation scaffold.
- `archive/recovered/mizan_core_v0_2.py` — recovered engineering registry and quarter-car simulation scaffold.
- `archive/recovered/mizan_core_v04.py` — recovered Python evidence-aware registry and validation gate.
- `docs/MIZAN_CORE_RECOVERY_STATUS.md` — source provenance, limitations, and recovery steps.
- `docs/MIZAN_CORE_STATE_MACHINE.md` — governance and execution state machine.
- `docs/MIZAN_EXECUTION_STORE.md` — execution-store invariants and external-effect limitations.
- `docs/MIZAN_CORE_RECONCILIATION_V1.md` — terminal UNKNOWN policy and external-effect boundaries.
- `docs/MIZAN_RECONCILIATION_JOURNAL.md` — durable evidence journal contract and tests.
- `scripts/concurrency-test.mjs` — guarded, test-project-only PostgreSQL concurrency harness.
- `.github/workflows/mizan-core-tests.yml` — CI compile and regression workflow.

## Governance invariants

1. Evidence before conclusion.
2. MIZAN evaluates ideas, permissions, and processes—not the worth of people.
3. The founder is not exempt from the rules.
4. `UNKNOWN` is not `PASS`; reconcile uncertain external effects before a new governed intent.
5. A successful software test is not proof of vehicle safety or physical validity.
6. Keep primary Supabase read-only during testing; concurrency experiments belong only in the dedicated test project.
7. Never automatically process, delete, retry, or settle unresolved outbox records without evidence and an explicit governed decision.
8. Do not integrate MIZAN into real vehicle actuator control without independent safety engineering and hardware-in-the-loop validation.

## Local tests

Python 3.10+:

```bash
python -m unittest discover -s tests -v
```

Current-branch compilation and unit-test results are tracked in [GitHub Actions](https://github.com/mnbkmorc-ops12/Moroco-atlas-/actions?query=branch%3Amizan-core-recovery-2026-10-27). A green run verifies only the code at that commit and the tests that ran; it does not certify real PostgreSQL concurrency, deployed security, external-evidence authenticity, or vehicle engineering.

## Recovery limits

Historical source that is not available through connected workspaces or accessible conversation/library files is marked **UNKNOWN**, not recreated and misrepresented as original. The PostgreSQL concurrency harness has **not** been run against the dedicated Supabase test project. No writes were made to the primary Supabase project during this recovery.
