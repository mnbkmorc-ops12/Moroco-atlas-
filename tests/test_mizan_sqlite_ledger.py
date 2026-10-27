"""Regression and concurrency tests for the isolated SQLite reference ledger."""
import concurrent.futures
import tempfile
import threading
import unittest
from pathlib import Path

from mizan_sqlite_ledger import LedgerError, SQLiteAuditLedger


class SQLiteLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = str(Path(self.tmp.name) / "ledger.sqlite3")
        self.ledger = SQLiteAuditLedger(self.db)

    def append_one(self, i):
        return self.ledger.append(
            event_id=f"evt-{i}", idempotency_key=f"key-{i}",
            event_type="TEST", payload={"i": i}, recorded_at=f"2026-10-27T00:00:{i:02d}Z")

    def test_empty_ledger_verifies(self):
        report = self.ledger.verify()
        self.assertTrue(report["ok"])
        self.assertEqual(report["rows"], 0)

    def test_idempotent_retry_returns_same_record(self):
        first = self.append_one(1)
        duplicate = self.append_one(1)
        self.assertFalse(first.duplicate)
        self.assertTrue(duplicate.duplicate)
        self.assertEqual(first.seq, duplicate.seq)
        self.assertEqual(first.hash, duplicate.hash)
        self.assertEqual(self.ledger.verify()["rows"], 1)

    def test_key_cannot_be_reused_for_different_event(self):
        self.append_one(1)
        with self.assertRaises(LedgerError):
            self.ledger.append(event_id="evt-other", idempotency_key="key-1",
                               event_type="TEST", payload={}, recorded_at="2026-10-27T00:00:01Z")

    def test_concurrent_unique_appends_have_contiguous_sequence(self):
        count = 100
        barrier = threading.Barrier(10)

        def worker(i):
            barrier.wait(timeout=10)
            return self.append_one(i)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(worker, range(count)))
        seqs = sorted(item.seq for item in results)
        self.assertEqual(seqs, list(range(1, count + 1)))
        report = self.ledger.verify()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["rows"], count)

    def test_repeated_idempotency_key_does_not_create_duplicate(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda _: self.append_one(7), range(10)))
        self.assertEqual(len({item.seq for item in results}), 1)
        self.assertEqual(sum(item.duplicate for item in results), 9)
        self.assertTrue(self.ledger.verify()["ok"])


if __name__ == "__main__":
    unittest.main()
