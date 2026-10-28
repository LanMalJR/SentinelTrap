
import json
import tempfile
import unittest
from pathlib import Path
from sys import path

# Allow tests to import our package from src/
path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sentineltrap.collector import read_events, filter_events, group_events_by_session

class TestCollector(unittest.TestCase):

    def test_read_valid_events(self):
        """Check that valid JSONL events are loaded correctly."""

        sample_events = [
            {"eventid": "cowrie.session.connect", "src_ip": "127.0.0.1"},
            {"eventid": "cowrie.login.success", "username": "root"}
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.jsonl"

            with file_path.open("w", encoding="utf-8") as file:
                for event in sample_events:
                    file.write(json.dumps(event) + "\n")

            events = read_events(str(file_path))

            self.assertEqual(len(events), 2)
            self.assertEqual(
                events[0]["eventid"],
                "cowrie.session.connect"
            )

    def test_filter_events(self):
        """Check that only matching event types are returned."""

        events = [
            {"eventid": "cowrie.session.connect"},
            {"eventid": "cowrie.login.success"},
            {"eventid": "cowrie.command.input"},
            {"eventid": "cowrie.login.success"}
        ]

        filtered = filter_events(events, "cowrie.login.success")

        self.assertEqual(len(filtered), 2)

        for event in filtered:
            self.assertEqual(
                event["eventid"],
                "cowrie.login.success"
            )

    def test_no_matching_events(self):
        """Check that filtering returns an empty list when no events match."""

        events = [
            {"eventid": "cowrie.session.connect"},
            {"eventid": "cowrie.command.input"}
        ]

        filtered = filter_events(events, "cowrie.login.failed")

        self.assertEqual(filtered, [])

    def test_read_invalid_json(self):
        """Verify that malformed JSON is skipped without crashing."""

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.jsonl"

            with file_path.open("w", encoding="utf-8") as file:
                file.write('{"eventid": "cowrie.session.connect"}\n')
                file.write('this is not valid JSON\n')
                file.write('{"eventid": "cowrie.login.success"}\n')

            events = read_events(str(file_path))

            self.assertEqual(len(events), 2)
            self.assertEqual(
                events[1]["eventid"],
                "cowrie.login.success"
            )


    def test_group_events_by_session(self):
        """Check that events are grouped by session identifier."""

        events = [
            {"session": "abc123", "eventid": "cowrie.session.connect"},
            {"session": "xyz789", "eventid": "cowrie.session.connect"},
            {"session": "abc123", "eventid": "cowrie.login.success"},
            {"session": "abc123", "eventid": "cowrie.command.input"},
        ]

        sessions = group_events_by_session(events)

        self.assertEqual(len(sessions), 2)
        self.assertEqual(len(sessions["abc123"]), 3)
        self.assertEqual(len(sessions["xyz789"]), 1)

    def test_group_events_without_session(self):
        """Check that events without session IDs are skipped."""

        events = [
            {"eventid": "cowrie.session.connect"},
            {"session": "abc123", "eventid": "cowrie.login.success"},
            {"session": "", "eventid": "cowrie.command.input"},
        ]

        sessions = group_events_by_session(events)

        self.assertEqual(len(sessions), 1)
        self.assertIn("abc123", sessions)

if __name__ == "__main__":
    unittest.main()
