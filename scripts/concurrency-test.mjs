#!/usr/bin/env node
/**
 * MIZAN CORE PostgreSQL concurrency test harness.
 *
 * TEST-ONLY: refuses the primary project and requires the exact test DB host.
 * No retries are performed. Any uncertain result requires independent reconciliation.
 *
 * Prerequisite: npm install pg
 * Usage: MIZAN_TEST_CONFIRM=YES DATABASE_URL='...' node scripts/concurrency-test.mjs
 */
import crypto from "node:crypto";
import pg from "pg";

const { Pool, Client } = pg;
const EXPECTED_REF = "wzjjengbwsfmunawcjnk";
const EXPECTED_HOST = `db.${EXPECTED_REF}.supabase.co`;
const COUNT = 100;
const CONCURRENCY = 10;

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}
function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonicalJson(value[k])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}
function assertTarget(urlString) {
  const url = new URL(urlString);
  const user = decodeURIComponent(url.username);
  if (url.hostname !== EXPECTED_HOST) {
    throw new Error(`Refusing writes: expected host ${EXPECTED_HOST}, got ${url.hostname}`);
  }
  if (!["postgres", `postgres.${EXPECTED_REF}`].includes(user)) {
    throw new Error(`Refusing writes: unexpected database username '${user}'`);
  }
  if (url.hostname.includes("tlpdlgzucpeurzhleycm")) {
    throw new Error("Refusing writes: primary project is prohibited.");
  }
}
function assert(condition, message) {
  if (!condition) throw new Error(message);
}
async function identity(client) {
  const result = await client.query(`
    select current_database() as database_name,
           current_user as database_user,
           inet_server_addr()::text as server_address,
           current_setting('server_version') as server_version
  `);
  return result.rows[0];
}
async function snapshot(client) {
  const [ledger, verifier] = await Promise.all([
    client.query(`
      select count(*)::int as rows,
             min(seq)::int as min_seq,
             max(seq)::int as max_seq,
             count(distinct seq)::int as unique_seq
      from public.mizan_ledger
    `),
    client.query("select public.mizan_verify_ledger_chain() as report")
  ]);
  return { ledger: ledger.rows[0], verifier: verifier.rows[0].report };
}
function makeEvent(runId, i) {
  const payload = {
    test_only: true,
    run_id: runId,
    write_index: i,
    project_ref: EXPECTED_REF,
  };
  const payloadHash = sha256(canonicalJson(payload));
  return {
    event: "TEST_CONCURRENCY_WRITE",
    intent_id: `mizan-concurrency-${runId}-${String(i).padStart(3, "0")}`,
    actor_name: "mizan-concurrency-test",
    domain: "TEST_ONLY",
    action: "CONCURRENCY_WRITE",
    decision: "TEST_ONLY",
    payload_hash: payloadHash,
    detail: JSON.stringify({ idempotency_key: `mizan-concurrency-${runId}-key-${i}`, payload }),
    recorded_at: new Date().toISOString(),
  };
}

async function main() {
  const connectionString = process.env.DATABASE_URL;
  assert(connectionString, "DATABASE_URL is required; no connection attempted.");
  assert(process.env.MIZAN_TEST_CONFIRM === "YES",
    "Set MIZAN_TEST_CONFIRM=YES only after confirming this is the isolated test project.");
  assert(process.env.MIZAN_TEST_PROJECT_REF === EXPECTED_REF,
    `Set MIZAN_TEST_PROJECT_REF=${EXPECTED_REF}; refusing ambiguous target.`);
  assert(process.env.MIZAN_ALLOW_TEST_WRITES === "YES",
    "Set MIZAN_ALLOW_TEST_WRITES=YES to explicitly authorize test writes.");
  assertTarget(connectionString);

  const pool = new Pool({ connectionString, max: CONCURRENCY, connectionTimeoutMillis: 10000,
    idleTimeoutMillis: 10000, application_name: "mizan-core-concurrency-test" });
  const independentReader = new Client({ connectionString, application_name: "mizan-core-independent-verifier" });
  const runId = `${Date.now()}-${crypto.randomBytes(4).toString("hex")}`;
  const results = [];
  let before;
  let after;
  try {
    await independentReader.connect();
    const readerIdentity = await identity(independentReader);
    assert(readerIdentity.database_user && readerIdentity.server_version,
      "Independent reader identity check incomplete.");
    const writer = await pool.connect();
    try {
      const writerIdentity = await identity(writer);
      assert(writerIdentity.database_user === readerIdentity.database_user,
        "Writer and independent reader identities disagree.");
      before = await snapshot(independentReader);
      const initialVerifier = before.verifier;
      assert(initialVerifier && initialVerifier.ok === true,
        "Preflight chain verifier did not return ok=true; zero writes performed.");
      writer.release();
    } catch (error) {
      writer.release(error);
      throw error;
    }

    // Ten independent checked-out PostgreSQL connections in the first wave.
    for (let offset = 0; offset < COUNT; offset += CONCURRENCY) {
      const batch = Array.from({ length: Math.min(CONCURRENCY, COUNT - offset) },
        (_, j) => offset + j);
      const batchResults = await Promise.all(batch.map(async i => {
        const client = await pool.connect();
        try {
          const who = await identity(client);
          assert(who.database_user === readerIdentity.database_user,
            `Connection identity mismatch at index ${i}; no retry attempted.`);
          const event = makeEvent(runId, i);
          const result = await client.query(
            "select public.mizan_append_ledger($1::jsonb) as result",
            [JSON.stringify(event)]
          );
          return { index: i, response: result.rows[0]?.result ?? null };
        } catch (error) {
          return { index: i, error: String(error?.message || error), uncertain: true };
        } finally {
          client.release();
        }
      }));
      results.push(...batchResults);
      // Deliberately no retries: reconcile the database before any rerun.
      if (batchResults.some(r => r.error)) break;
    }

    // Independent connection verifies persisted state even after a partial/uncertain batch.
    after = await snapshot(independentReader);
    const failures = results.filter(r => r.error);
    const responses = results.filter(r => !r.error);
    const uniqueSeqs = new Set(responses.map(r => r.response?.seq).filter(Number.isSafeInteger));
    const validResponseShape = responses.every(r =>
      Number.isSafeInteger(r.response?.seq) && r.response.seq >= 1 &&
      typeof r.response?.hash === "string" && r.response.hash.length === 64
    );
    const report = {
      run_id: runId,
      target_project_ref: EXPECTED_REF,
      target_host: EXPECTED_HOST,
      requested_writes: COUNT,
      completed_responses: responses.length,
      uncertain_or_failed_calls: failures.length,
      unique_returned_sequences: uniqueSeqs.size,
      all_responses_have_seq_and_hash: validResponseShape,
      before,
      after,
      chain_verifier_after: after.verifier,
      status: failures.length === 0 && responses.length === COUNT &&
        uniqueSeqs.size === COUNT && validResponseShape &&
        after.verifier?.ok === true &&
        after.ledger.rows - before.ledger.rows === COUNT ? "PASS" : "FAIL_OR_UNKNOWN",
      warning: "A failed/timeout response may have committed. Do not rerun blindly; reconcile run_id and intent_id values first."
    };
    console.log(JSON.stringify(report, null, 2));
    if (report.status !== "PASS") process.exitCode = 2;
  } finally {
    await pool.end();
    await independentReader.end().catch(() => {});
  }
}

main().catch(error => {
  console.error(JSON.stringify({ status: "ABORTED_BEFORE_CONFIRMED_SUCCESS", error: String(error?.message || error) }, null, 2));
  process.exitCode = 1;
});
