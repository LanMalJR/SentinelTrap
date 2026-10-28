
from collections import Counter


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
