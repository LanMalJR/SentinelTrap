
import unittest
from pathlib import Path
from sys import path

# Allow imports from the src directory
path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sentineltrap.analyzer import summarize_events


class TestAnalyzer(unittest.TestCase):

    def test_summarize_events(self):
        """Verify that security statistics are calculated correctly."""

        events = [
            {"session": "abc123", "eventid": "cowrie.session.connect"},
            {"session": "abc123", "eventid": "cowrie.login.success"},
            {"session": "abc123", "eventid": "cowrie.command.input"},
            {"session": "xyz789", "eventid": "cowrie.session.connect"},
            {"session": "xyz789", "eventid": "cowrie.login.failed"},
        ]

        summary = summarize_events(events)

        self.assertEqual(summary["total_events"], 5)
        self.assertEqual(summary["total_sessions"], 2)
        self.assertEqual(summary["ssh_connections"], 2)
        self.assertEqual(summary["successful_logins"], 1)
        self.assertEqual(summary["failed_logins"], 1)
        self.assertEqual(summary["commands_entered"], 1)

    def test_empty_events(self):
        """Verify that an empty event list produces zero counts."""

        summary = summarize_events([])

        self.assertEqual(summary["total_events"], 0)
        self.assertEqual(summary["total_sessions"], 0)
        self.assertEqual(summary["ssh_connections"], 0)
        self.assertEqual(summary["successful_logins"], 0)
        self.assertEqual(summary["failed_logins"], 0)
        self.assertEqual(summary["commands_entered"], 0)


if __name__ == "__main__":
    unittest.main()
