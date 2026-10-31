import os
import tempfile
import unittest
from unittest.mock import patch
import server

class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "test.sqlite3")
        self.patch = patch.object(server, "DB_PATH", self.db)
        self.patch.start()
        server.initialize()

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def test_submission_creates_instruction_and_task(self):
        row, duplicate = server.submit_instruction({"text": "Revisar CAPCOT", "idempotency_key": "abc"})
        self.assertFalse(duplicate)
        self.assertEqual(row["status"], "received")
        with server.connect() as db:
            task = db.execute("SELECT * FROM tasks WHERE instruction_id=?", (row["id"],)).fetchone()
            self.assertIsNotNone(task)
            self.assertEqual(task["status"], "queued")

    def test_idempotency_prevents_duplicate(self):
        first, _ = server.submit_instruction({"text": "Orden", "idempotency_key": "same"})
        second, duplicate = server.submit_instruction({"text": "Orden retransmitida", "idempotency_key": "same"})
        self.assertTrue(duplicate)
        self.assertEqual(first["id"], second["id"])
        with server.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM instructions").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 1)

    def test_invalid_priority_rejected(self):
        with self.assertRaises(ValueError):
            server.submit_instruction({"text": "Orden", "priority": "root"})

if __name__ == "__main__":
    unittest.main()
