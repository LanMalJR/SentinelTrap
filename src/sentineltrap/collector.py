
import json
from pathlib import Path
from sentineltrap.analyzer import summarize_events


def read_events(file_path: str) -> list[dict]:
    """Read security events from a Cowrie JSON Lines file."""

    events = []
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                event = json.loads(line)

                if not isinstance(event, dict):
                    print(f"Skipping line {line_number}: not a JSON object")
                    continue

                events.append(event)

            except json.JSONDecodeError as error:
                print(f"Invalid JSON on line {line_number}: {error}")

    return events


def filter_events(events: list[dict], event_type: str) -> list[dict]:
    """Return events matching a specified Cowrie event type."""

    filtered_events = []

    for event in events:
        if event.get("eventid") == event_type:
            filtered_events.append(event)

    return filtered_events


def group_events_by_session(events: list[dict]) -> dict[str, list[dict]]:
    """Group Cowrie security events by their session identifier."""

    sessions = {}

    for event in events:
        session_id = event.get("session")

        if not session_id:
            continue

        if session_id not in sessions:
            sessions[session_id] = []

        sessions[session_id].append(event)

    return sessions

if __name__ == "__main__":
    events = read_events("cowrie-test.json")

    print(f"Total events loaded: {len(events)}")

    # Filter events by category
    login_events = filter_events(events, "cowrie.login.success")
    command_events = filter_events(events, "cowrie.command.input")
    connection_events = filter_events(events, "cowrie.session.connect")

    # Display event statistics
    print(f"Successful logins: {len(login_events)}")
    print(f"Commands entered: {len(command_events)}")
    print(f"SSH connections: {len(connection_events)}")

    # Display recorded commands
    print("\nRecorded commands:")

    for event in command_events:
        print(f"- {event.get('input', 'unknown')}")

    # Display individual event information
    print("\nAll security events:")

    for event in events:
        print(
            f"Event: {event.get('eventid', 'unknown')} | "
            f"IP: {event.get('src_ip', 'unknown')} | "
            f"Session: {event.get('session', 'unknown')}"
        )
    
    # Group security events by SSH session
    sessions = group_events_by_session(events)

    print(f"\nTotal SSH sessions: {len(sessions)}")

    for session_id, session_events in sessions.items():
        print(f"\nSession: {session_id}")
        print(f"Total events: {len(session_events)}")

        for event in session_events:
            event_type = event.get("eventid", "unknown")
            print(f"  - {event_type}")


    # Generate security statistics
    summary = summarize_events(events)

    print("\nSecurity Summary")
    print("-" * 30)

    for metric, value in summary.items():
        print(f"{metric}: {value}")