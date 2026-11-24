"""Regression tests for the SQLite task store; run with python -m unittest discover -s tests."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_tasks.db"
        self.database_patch = patch.object(database, "DATABASE_NAME", str(self.db_path))
        self.database_patch.start()
        database.initialize_database()

    def tearDown(self):
        self.database_patch.stop()
        self.temp_dir.cleanup()

    def test_add_and_list_tasks_newest_first(self):
        database.add_task(" First ", "description", "2026-12-01")
        database.add_task("Second")
        tasks = database.get_tasks()
        self.assertEqual([row[1] for row in tasks], ["Second", "First"])
        self.assertEqual(tasks[0][4], "Pending")
        self.assertEqual(tasks[1][1], "First")

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            database.add_task("   ")

    def test_update_delete_and_missing_ids(self):
        database.add_task("Initial")
        task_id = database.get_tasks()[0][0]
        self.assertTrue(database.update_task(task_id, "Updated", "notes", "2026-12-01"))
        self.assertEqual(database.get_tasks()[0][1:4], ("Updated", "notes", "2026-12-01"))
        self.assertFalse(database.update_task(999, "Missing", "", ""))
        self.assertTrue(database.delete_task(task_id))
        self.assertFalse(database.delete_task(task_id))
        self.assertEqual(database.get_tasks(), [])

    def test_toggle_status_and_missing_id(self):
        database.add_task("Task")
        task_id = database.get_tasks()[0][0]
        self.assertTrue(database.toggle_task_status(task_id))
        self.assertEqual(database.get_tasks()[0][4], "Completed")
        self.assertTrue(database.toggle_task_status(task_id))
        self.assertEqual(database.get_tasks()[0][4], "Pending")
        self.assertFalse(database.toggle_task_status(999))

    def test_initialize_is_idempotent(self):
        database.initialize_database()
        database.add_task("Still works")
        self.assertEqual(len(database.get_tasks()), 1)


if __name__ == "__main__":
    unittest.main()
