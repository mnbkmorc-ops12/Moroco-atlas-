# MIZAN CORE — recovery and engineering workspace

> **Doctrine:** لا سلطة إلا للمعنى — evidence before conclusion.

This repository is being used to consolidate MIZAN CORE material recoverable from connected project history and accessible files. It is **not yet a complete export** of every historical Base44 screen, Supabase migration, or chat-only code fragment.

## Current layout

- `src/mizan_sqlite_ledger.py` — new v0.5 local reference ledger with `BEGIN IMMEDIATE`, idempotency enforcement, hash-chain verification, and transactional head updates.
- `tests/test_mizan_sqlite_ledger.py` — isolated tests including 100 concurrent appends across 10 workers.

- `archive/recovered/mizan_core_v0_1.py` — earliest recovered engineering registry and quarter-car simulation scaffold.
- `archive/recovered/mizan_core_v04.py` — recovered Python evidence-aware registry and validation gate.
- `archive/recovered/mizan_core_v0_2.py` — recovered engineering registry and quarter-car simulation scaffold.
- `docs/MIZAN_CORE_RECOVERY_STATUS.md` — source provenance, limitations, and next steps.
- `tests/test_mizan_core_v04.py` — software regression tests.

## Governance invariants

1. Evidence before conclusion.
2. MIZAN evaluates ideas, permissions, and processes—not the worth of people.
3. The founder is not exempt from the rules.
4. `UNKNOWN` is not `PASS`; reconcile uncertain external effects before retry.
5. A successful software test is not proof of vehicle safety or physical validity.
6. Keep production Supabase read-only during testing; concurrency experiments belong only in the dedicated test project.
7. Never automatically process or settle pending/unresolved outbox items.
8. Do not integrate MIZAN into real vehicle actuator control without independent safety engineering and hardware-in-the-loop validation.

## Local tests

Python 3.10+:

```bash
python -m unittest discover -s tests -v
```

These tests cover software behavior only. They do not certify PostgreSQL concurrency, deployed security, or vehicle engineering.

## Recovery limits

Historical source that is not available through connected workspaces or accessible conversation/library files is marked **UNKNOWN**, not recreated and misrepresented as original. See the recovery status document for details.
