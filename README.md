# MIZAN CORE — recovery and engineering workspace

> **Doctrine:** لا سلطة إلا للمعنى — evidence before conclusion.

This repository consolidates MIZAN CORE materials recoverable from connected project history and accessible files. It is **not yet a complete export** of every historical Base44 screen, Supabase migration, or chat-only code fragment.

## Current layout

- `src/mizan_governance.py` — pure decision and execution-state rules (`AUTHORIZED`, `DENIED`, `UNRESOLVED`; terminal `UNKNOWN`).
- `src/mizan_execution_store.py` — durable SQLite execution journal, immutable execution identity, atomic `claim_once`, compare-and-set transitions, and tamper-evident event-chain validation.
- `src/mizan_sqlite_ledger.py` — local v0.5 reference ledger with `BEGIN IMMEDIATE`, idempotency enforcement, hash-chain verification, and transactional head updates.
- `tests/test_mizan_governance.py` — governance decision and state-transition regressions.
- `tests/test_mizan_execution_store.py` — concurrent claim competition, immutable identity, terminal UNKNOWN, compare-and-set and audit-tampering tests.
- `tests/test_mizan_sqlite_ledger.py` — isolated ledger tests including 100 concurrent appends across 10 workers.
- `archive/recovered/mizan_core_v0_1.py` — earliest recovered engineering registry and quarter-car simulation scaffold.
- `archive/recovered/mizan_core_v0_2.py` — recovered engineering registry and quarter-car simulation scaffold.
- `archive/recovered/mizan_core_v04.py` — recovered Python evidence-aware registry and validation gate.
- `docs/MIZAN_CORE_RECOVERY_STATUS.md` — source provenance, limitations, and recovery steps.
- `docs/MIZAN_CORE_STATE_MACHINE.md` — governance and execution state machine.
- `docs/MIZAN_EXECUTION_STORE.md` — execution-store invariants and external-effect limitations.
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

The CI workflow has a successful regression run for commit `c5a0f232d953542aeb09c87449d7344f6b5270a4`: [view GitHub Actions](https://github.com/mnbkmorc-ops12/Moroco-atlas-/actions/runs/40429985201). This verifies the committed software tests only; it does not certify PostgreSQL concurrency, deployed security, or vehicle engineering. Documentation updates after that code commit do not change the code tested by that run.

## Recovery limits

Historical source that is not available through connected workspaces or accessible conversation/library files is marked **UNKNOWN**, not recreated and misrepresented as original. The PostgreSQL concurrency harness has **not** been run against the dedicated Supabase test project. No writes were made to the primary Supabase project during this recovery.
