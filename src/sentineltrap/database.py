
import sqlite3
import hashlib
import json
from pathlib import Path


def initialize_database(db_path: str = "sentineltrap.db") -> None:
    """Create the database and security events table if needed."""

    path = Path(db_path)

    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_uuid TEXT UNIQUE,
                session_id TEXT,
                event_type TEXT NOT NULL,
                timestamp TEXT,
                source_ip TEXT,
                raw_event TEXT NOT NULL
            )
        """)

        connection.commit()


def insert_events(
    events: list[dict],
    db_path: str = "sentineltrap.db"
) -> int:
    """Insert Cowrie events and skip duplicate records."""

    initialize_database(db_path)

    inserted_count = 0

    with sqlite3.connect(db_path) as connection:
        for event in events:
            event_type = event.get("eventid")

            # Skip events without a valid event type
            if not isinstance(event_type, str) or not event_type:
                continue

            # Remove common sensitive authentication fields
            safe_event = {
                key: value
                for key, value in event.items()
                if key.lower() not in {
                    "password", "passwd", "secret", "token"
                }
            }

            # Convert the sanitised event into JSON text
            raw_event = json.dumps(
                safe_event,
                sort_keys=True,
                ensure_ascii=False
            )

            # Generate a consistent identifier for duplicate detection
            event_id = hashlib.sha256(
                raw_event.encode("utf-8")
            ).hexdigest()

            # Insert only if the event is not already stored
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO security_events (
                    event_uuid,
                    session_id,
                    event_type,
                    timestamp,
                    source_ip,
                    raw_event
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    event.get("session"),
                    event_type,
                    event.get("timestamp"),
                    event.get("src_ip"),
                    raw_event
                )
            )

            inserted_count += cursor.rowcount

        connection.commit()

    return inserted_count
