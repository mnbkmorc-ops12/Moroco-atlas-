// MIZAN Governance API — safe initial scaffold.
// No database writes, action execution, or claims of authorization are performed here.
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": Deno.env.get("MIZAN_ALLOWED_ORIGIN") ?? "http://localhost:3000",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};

serve((req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  const url = new URL(req.url);
  if (req.method === "GET" && url.pathname.endsWith("/health")) {
    return Response.json(
      {
        service: "mizan-governance-api",
        status: "SCAFFOLD_ONLY",
        decision_authority: false,
        execution_enabled: false,
        evidence: "No production governance or database connection is configured."
      },
      { headers: corsHeaders }
    );
  }

  return Response.json(
    { error: "NOT_IMPLEMENTED", decision: "UNRESOLVED" },
    { status: 501, headers: corsHeaders }
  );
});
