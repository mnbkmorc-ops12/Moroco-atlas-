// Pure request handler for the MIZAN Governance API scaffold.
// This module deliberately has no database client or execution adapter.
const corsHeadersFor = (allowedOrigin: string) => ({
  "Access-Control-Allow-Origin": allowedOrigin,
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Vary": "Origin",
});

export function createHandler(allowedOrigin: string) {
  const corsHeaders = corsHeadersFor(allowedOrigin);

  return (req: Request): Response => {
    if (req.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    const url = new URL(req.url);
    if (req.method === "GET" && url.pathname.endsWith("/health")) {
      return Response.json(
        {
          service: "mizan-governance-api",
          status: "SCAFFOLD_ONLY",
          decision_authority: false,
          execution_enabled: false,
          evidence: "No production governance or database connection is configured.",
        },
        { status: 200, headers: corsHeaders },
      );
    }

    return Response.json(
      { error: "NOT_IMPLEMENTED", decision: "UNRESOLVED" },
      { status: 501, headers: corsHeaders },
    );
  };
}
