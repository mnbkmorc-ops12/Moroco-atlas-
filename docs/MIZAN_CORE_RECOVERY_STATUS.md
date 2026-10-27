# MIZAN CORE — recovery status

Snapshot date: 2026-10-27 UTC

## Recovered and committed

| Item | Status | Evidence |
|---|---|---|
| Python MIZAN Core v0.4 | PASS — source recovered | Accessible library file `mizan_core_v04.py`, archived without claiming physical validation |
| Python MIZAN Core v0.2 | PASS — source recovered | Accessible library file `mizan_core_v0_2.py` |
| Base44 app inventory | PARTIAL | Two apps named MIZAN CORE found. One is ready and exposes schemas; the second is paused for user input. |
| Base44 source export | UNKNOWN | Source browsing was blocked because Base44 workspace integration credits were exhausted. App source is not claimed to be exported. |
| Supabase primary project | IDENTIFIED | `tlpdlgzucpeurzhleycm`; no test writes permitted. |
| Supabase test project | IDENTIFIED | `wzjjengbwsfmunawcjnk`; isolated test environment. |
| Test DB ledger chain | PASS for the last read-only structural/hash verification only | Last recorded check saw 101 rows, contiguous sequence 1–101, matching head/tip, and no hash/link mismatches. |
| 100 writes / 10 independent connections | UNKNOWN | No evidence this test has run. |
| Original SQL migration definitions | UNKNOWN | Applied migration names/status were available, but complete original SQL source was not recovered in this pass. |
| All chat-only code and assets | UNKNOWN | Only files actually available through the connected library have been copied. |

## Base44 schema inventory observed

The ready MIZAN CORE app exposed `KernelLease`, `ExecutionIntent`, `GovernanceRule`, `Actor`, `LedgerEntry`, and `User`. Schema existence does not prove complete business logic is correct or deployed.

## Supabase project separation

- **Primary / read-only:** `tlpdlgzucpeurzhleycm`
- **Test-only:** `wzjjengbwsfmunawcjnk`

Never run test inserts, schema changes, or destructive actions against the primary project. Before concurrency testing, validate the connection host and username/project reference against the expected test project. If identity is ambiguous, abort before the first write.

## Known test database state from prior read-only inspection

Tables included `mizan_ledger` (101 rows), `mizan_idempotency` (101 rows), `mizan_ledger_head` (one row), and `mizan_outbox` (six rows). Three outbox records were `succeeded`, two were `pending`, and one was `unresolved` after lease expiry with an unknown external-effect outcome.

Do not delete, settle, retry, or execute these records automatically. Inspect provenance and reconcile external effects first.

The latest recorded verifier reported `ok=true`, `STRUCTURE_AND_CHAIN_CONSISTENT`, 101 rows, sequence 1–101, head matching tip, no null hash fields, and zero previous-hash/hash mismatches. This result is time-specific and should be rerun read-only before reliance.

## Next engineering gates

1. Recover/export full Base44 source when workspace access is restored; compare both app IDs before choosing the canonical app.
2. Recover exact applied SQL migration definitions from the test project or original files, preserving provenance and checksums.
3. Run local regression tests for recovered Python source.
4. Review PostgreSQL function definitions, grants, RLS, and outbox state in the test project.
5. Implement a test-only concurrency harness with strict identity checks, unique idempotency keys, no automatic retries, independent post-test reads, and explicit uncertain-commit handling.
6. Report each gate as `PASS`, `FAIL`, or `UNKNOWN`.

## Security

Never commit database passwords, service-role keys, access tokens, production secrets, personal data, or unredacted connection strings. Keep credentials in a secret manager or excluded local environment file.
