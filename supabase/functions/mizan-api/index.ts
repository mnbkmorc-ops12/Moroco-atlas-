// MIZAN Governance API — safe initial scaffold.
// No database writes, action execution, or claims of authorization are performed here.
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createHandler } from "./handler.ts";

const allowedOrigin = Deno.env.get("MIZAN_ALLOWED_ORIGIN") ?? "http://localhost:3000";
serve(createHandler(allowedOrigin));
