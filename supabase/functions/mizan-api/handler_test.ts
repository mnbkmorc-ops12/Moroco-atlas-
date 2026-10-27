import { assertEquals, assertStringIncludes } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { createHandler } from "./handler.ts";

const ORIGIN = "https://mizan.example.test";
const handler = createHandler(ORIGIN);

Deno.test("GET /health is explicit about scaffold-only status", async () => {
  const response = handler(new Request("https://api.example.test/health"));
  assertEquals(response.status, 200);
  assertEquals(response.headers.get("access-control-allow-origin"), ORIGIN);
  const body = await response.json();
  assertEquals(body.service, "mizan-governance-api");
  assertEquals(body.status, "SCAFFOLD_ONLY");
  assertEquals(body.decision_authority, false);
  assertEquals(body.execution_enabled, false);
  assertStringIncludes(body.evidence, "No production governance");
});

Deno.test("OPTIONS returns preflight headers and no side effects", async () => {
  const response = handler(new Request("https://api.example.test/anything", { method: "OPTIONS" }));
  assertEquals(response.status, 204);
  assertEquals(response.headers.get("access-control-allow-origin"), ORIGIN);
  assertEquals(response.headers.get("access-control-allow-methods"), "GET, OPTIONS");
});

Deno.test("unsupported route remains unresolved and unimplemented", async () => {
  const response = handler(new Request("https://api.example.test/decisions"));
  assertEquals(response.status, 501);
  assertEquals(await response.json(), { error: "NOT_IMPLEMENTED", decision: "UNRESOLVED" });
});

Deno.test("POST is rejected rather than interpreted as authorization", async () => {
  const response = handler(new Request("https://api.example.test/health", { method: "POST" }));
  assertEquals(response.status, 501);
  assertEquals(await response.json(), { error: "NOT_IMPLEMENTED", decision: "UNRESOLVED" });
});
