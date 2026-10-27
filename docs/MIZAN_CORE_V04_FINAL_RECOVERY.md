# MIZAN CORE v0.4 FINAL — Recovery Record

## Source identity

- Source archive recovered from the connected project Library: `MIZAN_CORE_v0.4_FINAL.zip`
- Archive size: 30,735 bytes
- SHA-256: `86e4c12846a6539529fd30f8acad49adcad8b5e298a76826a824a9bb2b1d048e`
- Top-level package root inside the archive: `mizan-core/`
- Archive inventory: 26 files (source, tests, documentation, project metadata, and security notes).

## Package contents

The package includes:
- `src/mizan_core/approvals.py`
- `src/mizan_core/audit_checkpoint.py`
- `src/mizan_core/canonicalization.py`
- `src/mizan_core/execution_store.py`
- `src/mizan_core/executor.py`
- `src/mizan_core/governance.py`
- `src/mizan_core/models.py`
- `src/mizan_core/reconciliation.py`
- `tests/` with model, governance, approvals, executor, reconciliation, execution-store, checkpoint, canonicalization, integrity, and adversarial tests
- `README.md`, `SECURITY.md`, `docs/ARCHITECTURE.md`, `docs/TEST_PLAN.md`, and `pyproject.toml`.

## Verified test result

Command run from the extracted package root:

```bash
PYTHONPATH=src python -m pytest -q
```

Result: **52 passed in 0.51s**.

This result applies to the recovered local archive content. It is separate from the GitHub Actions success for the current branch's reconstructed/recovered workspace. The archive itself has not yet been committed as a ZIP artifact in this repository, so this document does not imply that GitHub CI ran those 52 archive tests.

## Engineering boundary

The package remains a prototype, not a production safety boundary. Local tests do not prove exactly-once external side effects, resistance to privileged database tampering, PostgreSQL concurrency, or vehicle safety. Read `SECURITY.md` before integrating it with any external executor. Reconcile uncertain outcomes; never treat `UNKNOWN` as success or automatically replay an uncertain side effect.
