
import json
from pathlib import Path


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


if __name__ == "__main__":
    events = read_events("cowrie-test.json")

    print(f"Total events loaded: {len(events)}")

    for event in events:
        print(
            f"Event: {event.get('eventid', 'unknown')} | "
            f"IP: {event.get('src_ip', 'unknown')} | "
            f"Session: {event.get('session', 'unknown')}"
        )
