
# SentinelTrap

**An SSH Honeypot and Security Event Monitoring System**

SentinelTrap is a Python-based cybersecurity project focused on capturing, monitoring, storing, and analysing SSH activity within a controlled honeypot environment.

The project uses a containerised SSH honeypot to emulate a Linux server and record connection attempts, authentication activity, and commands entered within a simulated terminal.

SentinelTrap is being developed as a modular security monitoring application, combining honeypot deployment, event collection, security analytics, and persistent storage.

> **Project Status:** In Development — Phase 4: SQLite Database Integration

## 1. Project Overview

SentinelTrap provides a controlled environment for observing interactions with a simulated SSH service.

The system uses [Cowrie](https://github.com/cowrie/cowrie), an SSH honeypot capable of emulating a Linux shell and recording interactions without granting access to a real operating system.

Captured security events are processed using Python modules responsible for event collection, filtering, session grouping, and security analysis.

The project is currently expanding its SQLite database functionality to support persistent event storage and historical analysis.

The long-term objective is to develop a security monitoring application capable of identifying suspicious activity patterns, generating security reports, and visualising security events through an interactive dashboard.

## 2. Project Objectives

The primary objectives are to:

- Deploy an isolated SSH honeypot using Docker.
- Capture SSH connections and authentication attempts.
- Record commands executed within the simulated Linux environment.
- Preserve security events using persistent storage.
- Develop a Python-based security event collector.
- Validate and filter structured security events.
- Group related events into individual SSH sessions.
- Analyse authentication activity, command execution, and session durations.
- Implement local security event storage using SQLite.
- Prevent duplicate event ingestion.
- Develop automated tests for system reliability.
- Implement security analytics and visualisation capabilities.

## 3. Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Security event collection, processing, and analysis |
| Cowrie | SSH honeypot and Linux shell emulation |
| Docker | Containerised deployment |
| Docker Compose | Container configuration and persistent storage |
| SQLite | Local security event database |
| unittest | Automated Python testing |
| Git & GitHub | Version control and project management |
| Visual Studio Code | Development environment |

Additional technologies will be introduced as the project develops.

## 4. System Architecture

SentinelTrap follows a modular architecture that separates event collection, security analysis, and database operations.

```text
                  SSH Client
                      |
                      | Port 2222
                      v
             +------------------+
             | Cowrie           |
             | SSH Honeypot     |
             | Docker Container |
             +------------------+
                      |
                      v
             +------------------+
             | Docker Volume    |
             | Cowrie JSONL Logs|
             +------------------+
                      |
              Local Log Export
                      |
                      v
             +------------------+
             | Python Event     |
             | Collector        |
             | collector.py     |
             +------------------+
                      |
              +-------+-------+
              |               |
              v               v
     +----------------+  +----------------+
     | Security       |  | SQLite         |
     | Analyzer       |  | Database       |
     | analyzer.py    |  | database.py    |
     +----------------+  +----------------+
              |               |
              +-------+-------+
                      |
                      v
             +------------------+
             | Security         |
             | Dashboard        |
             | (Planned)        |
             +------------------+
```

**Current architecture status:**

- Cowrie generates structured JSONL security logs.
- The Python collector processes locally exported Cowrie logs.
- The analyzer generates event summaries and individual session reports.
- The SQLite database module supports schema creation and is being extended with event insertion and duplicate prevention.
- Direct database ingestion and dashboard integration are planned.

The diagram represents the intended architecture. The modules are not yet connected into a fully automated processing pipeline.

## 5. Current Implementation

### 5.1 SSH Honeypot

Cowrie is deployed using Docker Compose and configured to listen on port `2222`, accessible through `127.0.0.1`.

Initial testing confirmed that the honeypot can:

- Accept SSH connections.
- Simulate authentication.
- Present an emulated Linux terminal.
- Record commands such as `whoami` and `ls`.
- Capture connection and session information.

### 5.2 Security Event Logging

Cowrie generates structured JSON Lines (JSONL) records containing:

- Session identifiers and timestamps.
- Source IP addresses.
- Authentication attempts and outcomes.
- Commands entered in the emulated shell.
- Session termination events.

A Docker named volume has been configured for persistent log storage.

Volume ownership and permission issues encountered during development were identified and corrected. Final persistence verification across container recreation remains outstanding.

### 5.3 Python Event Collector

The event collector is implemented in `collector.py`.

It provides the following functionality:

- Read Cowrie JSONL files.
- Parse JSON records into Python dictionaries.
- Skip malformed JSON records.
- Ignore records that are not JSON objects.
- Filter events by their event identifiers.
- Group related events by SSH session identifiers.
- Display security event information.

The collector currently operates on local exported log files.

### 5.4 Security Event Analysis

The security analysis module is implemented in `analyzer.py`.

It provides two main functions:

**Overall event analysis — `summarize_events()`**

Calculates:

- Total security events.
- Total unique SSH sessions.
- SSH connections.
- Successful simulated logins.
- Failed login attempts.
- Commands entered.

**Individual session analysis — `analyze_sessions()`**

Calculates:

- Source IP address.
- Total events per session.
- Successful and failed login counts.
- Recorded commands.
- Estimated session duration.

Session duration is calculated using available event timestamps and may differ from the exact connection duration when timestamps are missing.

### 5.5 SQLite Database

SentinelTrap uses Python's built-in `sqlite3` library for local event storage.

The `database.py` module includes:

- Database initialization.
- Automatic creation of the `security_events` table.
- Database schema support for event metadata and JSON records.

The event insertion implementation is being developed to support:

- Storing Cowrie security events.
- Duplicate event prevention using deterministic identifiers.
- Excluding selected sensitive fields before storage.
- Tracking newly inserted records.

Database insertion, retrieval, and collector integration are not yet fully validated.

### 5.6 Automated Testing

SentinelTrap uses Python's built-in `unittest` framework.

The test suite covers:

- Reading valid JSONL records.
- Handling malformed JSON records.
- Filtering security events.
- Grouping events by SSH session.
- Handling records without session identifiers.
- Generating security statistics.
- Analysing individual session activity.
- Handling missing and invalid timestamps.
- Initialising SQLite databases.

**Testing status:**

- 13 automated tests confirmed passing during development.
- Additional database insertion tests are being introduced.
- Integration and end-to-end testing remain planned.

Tests use temporary files, temporary databases, and fictional event data.

## 6. Project Structure

```text
SentinelTrap/
├── src/
│   └── sentineltrap/
│       ├── __init__.py
│       ├── collector.py
│       ├── analyzer.py
│       └── database.py
├── tests/
│   ├── test_collector.py
│   ├── test_analyzer.py
│   └── test_database.py
├── docker-compose.yml
├── .gitignore
└── README.md
```

Generated security logs, local databases, captured authentication data, and backups are excluded from version control.

## 7. Getting Started

### Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose
- Python 3.9 or later
- Git
- An SSH client

### Installation

Clone the repository:

```bash
git clone https://github.com/LanMalJR/SentinelTrap.git
cd SentinelTrap
```

Start the Cowrie honeypot:

```bash
docker compose up -d
```

Check the container status:

```bash
docker compose ps
```

### Testing the Honeypot

From another terminal, connect using SSH:

```bash
ssh -p 2222 root@127.0.0.1
```

Use fictional test credentials only.

Once authenticated, try commands such as:

```bash
whoami
pwd
ls
exit
```

### Inspecting Logs

View Cowrie's container output:

```bash
docker compose logs --tail=50 cowrie
```

Cowrie's structured JSONL event log is stored inside the container at:

```text
/cowrie/cowrie-git/var/log/cowrie/cowrie.json
```

To copy the log into the project directory for local testing:

```bash
docker cp \
  sentineltrap-cowrie:/cowrie/cowrie-git/var/log/cowrie/cowrie.json \
  ./cowrie-test.json
```

The copied file contains JSON Lines data despite its `.json` extension.

### Running the Python Collector

From the project root:

```bash
PYTHONPATH=src python3 -m sentineltrap.collector
```

The collector processes `cowrie-test.json` and displays event statistics and session reports.

The file must contain the original JSONL format rather than a formatted JSON array.

### Running Automated Tests

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

To run only database tests:

```bash
python3 -m unittest discover -s tests -p "test_database.py" -v
```

### Stopping the Honeypot

```bash
docker compose down
```

**Note:** Avoid using `docker compose down -v` unless intentionally deleting persistent Docker volumes.

## 8. Development Roadmap

### Phase 1 — Honeypot Deployment

- [x] Initialise the GitHub repository.
- [x] Configure the Cowrie Docker container.
- [x] Establish SSH connectivity.
- [x] Test authentication and shell emulation.
- [x] Verify command recording.
- [x] Inspect Cowrie JSON security events.
- [x] Configure persistent Docker storage.
- [x] Resolve Docker volume permission issues.
- [ ] Complete persistent storage verification.

### Phase 2 — Python Event Collection

- [x] Create the initial Python project structure.
- [x] Implement the JSONL event reader.
- [x] Implement event filtering.
- [x] Implement SSH session grouping.
- [x] Add automated collector tests.
- [ ] Implement comprehensive event validation and normalisation.
- [ ] Integrate the collector directly with Cowrie's persistent storage.

### Phase 3 — Security Analytics

- [x] Implement overall security event statistics.
- [x] Analyse successful and failed authentication attempts.
- [x] Analyse individual SSH sessions.
- [x] Calculate estimated session durations.
- [x] Implement automated analyzer tests.
- [ ] Implement advanced suspicious activity detection.
- [ ] Develop security reporting capabilities.

### Phase 4 — Database Integration

- [x] Create the SQLite database module.
- [x] Implement database initialization.
- [x] Define the security events table.
- [x] Implement database initialization tests.
- [ ] Complete and validate event insertion.
- [ ] Verify duplicate prevention.
- [ ] Implement historical event retrieval.
- [ ] Implement session-based database queries.
- [ ] Integrate the event collector with SQLite.

### Phase 5 — Dashboard Development

- [ ] Select the dashboard framework.
- [ ] Develop a security overview dashboard.
- [ ] Visualise SSH connections and authentication activity.
- [ ] Display individual SSH session histories.
- [ ] Implement event filtering and searching.
- [ ] Display historical security statistics.

### Phase 6 — Detection and Monitoring

- [ ] Implement suspicious activity detection rules.
- [ ] Identify repeated authentication failures.
- [ ] Analyse potentially suspicious command patterns.
- [ ] Develop configurable monitoring alerts.
- [ ] Improve automated event ingestion.

### Phase 7 — Testing and Documentation

- [ ] Add database retrieval tests.
- [ ] Implement integration tests.
- [ ] Verify end-to-end event processing.
- [ ] Review sensitive-data handling.
- [ ] Improve deployment documentation.
- [ ] Finalise the project README and architecture documentation.

## 9. Security Considerations

SentinelTrap is intended for educational purposes and authorised defensive cybersecurity research.

The current deployment is restricted to localhost and should not be publicly exposed without additional isolation, network controls, monitoring, and risk assessment.

Honeypot logs may contain sensitive information such as:

- Source IP addresses.
- Attempted usernames and passwords.
- Session identifiers.
- Commands entered within the simulated environment.
- Other captured session metadata.

The project uses `.gitignore` to exclude real security data, database files, and local backups from normal Git tracking.

The SQLite insertion implementation removes selected top-level authentication secret fields before storing events. This is not yet a comprehensive sanitisation mechanism.

**Actual honeypot logs, credentials, session recordings, and databases must not be committed to the public repository.**

Only fictional or appropriately sanitised test data should be included in public examples.

## 10. Development Status

SentinelTrap is an ongoing cybersecurity and software engineering project.

The initial honeypot deployment, Python event collector, security analyzer, and database initialization are implemented.

Current development focuses on completing SQLite event insertion, verifying duplicate prevention, and introducing historical event retrieval.

Subsequent development will focus on connecting the components into a unified processing pipeline, followed by security monitoring, suspicious activity detection, and dashboard visualisation.

The project documentation will be updated as additional functionality is implemented and verified.
