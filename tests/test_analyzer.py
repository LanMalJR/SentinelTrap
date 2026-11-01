
import unittest
from pathlib import Path
from sys import path

# Allow imports from the src directory
path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sentineltrap.analyzer import summarize_events, analyze_sessions


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

    def test_analyze_session_activity(self):
        """Verify authentication, commands, and session duration."""

        sessions = {
            "abc123": [
                {
                    "eventid": "cowrie.session.connect",
                    "src_ip": "192.0.2.10",
                    "timestamp": "2026-10-28T10:00:00Z",
                },
                {
                    "eventid": "cowrie.login.failed",
                    "src_ip": "192.0.2.10",
                    "timestamp": "2026-10-28T10:00:10Z",
                },
                {
                    "eventid": "cowrie.login.success",
                    "src_ip": "192.0.2.10",
                    "timestamp": "2026-10-28T10:00:20Z",
                },
                {
                    "eventid": "cowrie.command.input",
                    "input": "whoami",
                    "timestamp": "2026-10-28T10:00:30Z",
                },
                {
                    "eventid": "cowrie.session.closed",
                    "timestamp": "2026-10-28T10:02:00Z",
                },
            ]
        }

        reports = analyze_sessions(sessions)
        report = reports["abc123"]

        self.assertEqual(report["source_ip"], "192.0.2.10")
        self.assertEqual(report["total_events"], 5)
        self.assertEqual(report["successful_logins"], 1)
        self.assertEqual(report["failed_logins"], 1)
        self.assertEqual(report["commands"], ["whoami"])
        self.assertEqual(report["duration_seconds"], 120.0)

    def test_session_without_timestamps(self):
        """Verify missing timestamps do not crash the analyzer."""

        sessions = {
            "abc123": [
                {"eventid": "cowrie.session.connect"},
                {"eventid": "cowrie.login.success"},
            ]
        }

        reports = analyze_sessions(sessions)
        report = reports["abc123"]

        self.assertEqual(report["total_events"], 2)
        self.assertEqual(report["successful_logins"], 1)
        self.assertIsNone(report["duration_seconds"])

    def test_session_with_invalid_timestamp(self):
        """Verify invalid timestamps are safely ignored."""

        sessions = {
            "abc123": [
                {
                    "eventid": "cowrie.session.connect",
                    "timestamp": "invalid-timestamp",
                },
                {
                    "eventid": "cowrie.login.success",
                    "timestamp": "2026-10-28T10:00:00Z",
                },
            ]
        }

        reports = analyze_sessions(sessions)
        report = reports["abc123"]

        self.assertEqual(report["successful_logins"], 1)
        self.assertIsNone(report["duration_seconds"])


if __name__ == "__main__":
    unittest.main()
