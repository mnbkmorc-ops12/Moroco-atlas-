"""Static safety-contract checks for the Deno API scaffold.

These tests inspect source invariants only; they do not claim to execute or
integration-test the hosted Edge Function.
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
API_SOURCE = ROOT / "supabase" / "functions" / "mizan-api" / "index.ts"
CONTRACT = ROOT / "docs" / "API_CONTRACT.md"


class ApiScaffoldContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = API_SOURCE.read_text(encoding="utf-8")
        cls.contract = CONTRACT.read_text(encoding="utf-8")

    def test_health_response_disclaims_authority_and_execution(self):
        self.assertIn('service: "mizan-governance-api"', self.source)
        self.assertIn('status: "SCAFFOLD_ONLY"', self.source)
        self.assertIn("decision_authority: false", self.source)
        self.assertIn("execution_enabled: false", self.source)
        self.assertIn("No production governance or database connection is configured.", self.source)

    def test_unimplemented_requests_are_unresolved_and_not_implemented(self):
        self.assertIn('error: "NOT_IMPLEMENTED"', self.source)
        self.assertIn('decision: "UNRESOLVED"', self.source)
        self.assertIn("{ status: 501, headers: corsHeaders }", self.source)

    def test_only_get_and_options_are_advertised(self):
        self.assertIn('"Access-Control-Allow-Methods": "GET, OPTIONS"', self.source)
        self.assertIn("req.method === \"OPTIONS\"", self.source)
        self.assertIn('req.method === "GET" && url.pathname.endsWith("/health")', self.source)

    def test_scaffold_has_no_database_or_execution_integration(self):
        forbidden_markers = (
            "createClient(",
            "supabase.from(",
            ".insert(",
            ".upsert(",
            ".update(",
            ".delete(",
            "fetch(",
            "executeAction(",
        )
        for marker in forbidden_markers:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.source)

    def test_contract_documents_that_cors_is_not_authentication(self):
        self.assertIn("CORS is not authentication", self.contract)
        self.assertIn("Never connect this scaffold to the primary ledger", self.contract)
        self.assertIn("No automatic retry or external effect", self.contract)


if __name__ == "__main__":
    unittest.main()
