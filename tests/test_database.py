
import sqlite3
import tempfile
import unittest
from pathlib import Path
from sys import path

# Allow imports from src/
path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sentineltrap.database import initialize_database


class TestDatabase(unittest.TestCase):

    def test_database_initialization(self):
        """Verify that initializing the database creates the events table."""

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"

            initialize_database(str(db_path))

            self.assertTrue(db_path.exists())

            with sqlite3.connect(db_path) as connection:
                result = connection.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                    AND name = 'security_events'
                """).fetchone()

            self.assertIsNotNone(result)

    def test_database_initialization_twice(self):
        """Verify that database initialization is repeatable."""

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"

            initialize_database(str(db_path))
            initialize_database(str(db_path))

            self.assertTrue(db_path.exists())


if __name__ == "__main__":
    unittest.main()
