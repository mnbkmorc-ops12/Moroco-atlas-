# MIZAN CORE API Contract — Scaffold v0.1

## Purpose
This contract documents the current read-only API boundary. It is not an authorization to connect a database, approve actions, or execute external effects.

## GET /health
Expected HTTP status: `200`

Required response fields:
- `service`: `mizan-governance-api`
- `status`: `SCAFFOLD_ONLY`
- `decision_authority`: `false`
- `execution_enabled`: `false`
- `evidence`: a string explaining that production governance/database connection is not configured

This response proves only that the scaffold handler responds. It does not prove governance correctness or database connectivity.

## OPTIONS /*
Expected behavior: return a preflight response with the configured CORS headers. Allowed methods remain `GET, OPTIONS`.

## Unimplemented routes and methods
All routes other than `GET /health` and `OPTIONS` return HTTP `501` with:
`{ "error": "NOT_IMPLEMENTED", "decision": "UNRESOLVED" }`

No route may write to the database or trigger an external effect in this scaffold.

## Security invariants
1. The API must not claim decision authority or execution capability.
2. Unknown outcomes remain `UNRESOLVED`; they must not be treated as success.
3. No automatic retry or external effect is allowed for unresolved outcomes.
4. CORS is not authentication. Before hosted integration, validate authentication, authorization, RLS, allowed origins, and test-project identity separately.
5. Never connect this scaffold to the primary ledger as part of a smoke test.

## Required tests before integration
- Assert health status and all safety flags.
- Assert unsupported methods/routes return HTTP 501 and `UNRESOLVED`.
- Assert OPTIONS returns the configured CORS headers.
- Assert no database client or write path is imported by this scaffold.
- Run integration tests only against the explicitly verified test project, with separate approval for test writes.
