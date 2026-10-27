# MIZAN CORE implementation status

## Scope of this scaffold

- Development container: Node.js 22 and Python 3.12.
- Web: Arabic-first Next.js interface for local preview.
- Governance API: read-only health response; all other routes return HTTP 501.
- Existing Python governance and durable execution store remain the source of policy logic.

## Explicitly not enabled

- No production deployment workflow.
- No Supabase database writes from the new function.
- No automatic retries for UNKNOWN outcomes.
- No UI authority to approve or execute actions.
- No connection to the primary Supabase project.

## Required before enabling deployment

1. Add and run a package lockfile-based build in CI.
2. Add API contract tests and a test-project-only integration test.
3. Verify the test project reference and deployment credentials.
4. Review auth/RLS and allowed-origin configuration.
5. Obtain explicit approval before deploying or changing hosted services.
