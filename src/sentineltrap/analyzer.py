
from collections import Counter
from datetime import datetime


def summarize_events(events: list[dict]) -> dict:
    """Generate summary statistics from Cowrie security events."""

    event_counts = Counter()
    unique_sessions = set()

    for event in events:
        event_type = event.get("eventid")

        if event_type:
            event_counts[event_type] += 1

        session_id = event.get("session")

        if session_id:
            unique_sessions.add(session_id)

    return {
        "total_events": len(events),
        "total_sessions": len(unique_sessions),
        "ssh_connections": event_counts["cowrie.session.connect"],
        "successful_logins": event_counts["cowrie.login.success"],
        "failed_logins": event_counts["cowrie.login.failed"],
        "commands_entered": event_counts["cowrie.command.input"],
    }


def analyze_sessions(sessions: dict[str, list[dict]]) -> dict:
    """Generate security statistics for individual SSH sessions."""

    session_reports = {}

    for session_id, events in sessions.items():

        login_success = 0
        login_failed = 0
        commands = []
        timestamps = []
        source_ip = "unknown"

        for event in events:
            event_type = event.get("eventid")

            if event_type == "cowrie.login.success":
                login_success += 1

            elif event_type == "cowrie.login.failed":
                login_failed += 1

            elif event_type == "cowrie.command.input":
                commands.append(event.get("input", ""))

            if event.get("src_ip"):
                source_ip = event["src_ip"]

            timestamp = event.get("timestamp")

            if timestamp:
                try:
                    parsed_time = datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )
                    timestamps.append(parsed_time)

                except (ValueError, TypeError):
                    pass

        duration_seconds = None

        if len(timestamps) >= 2:
            try:
                duration_seconds = (
                    max(timestamps) - min(timestamps)
                ).total_seconds()

            except TypeError:
                pass

        session_reports[session_id] = {
            "source_ip": source_ip,
            "total_events": len(events),
            "successful_logins": login_success,
            "failed_logins": login_failed,
            "commands": commands,
            "duration_seconds": duration_seconds,
        }

    return session_reports
