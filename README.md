
# SentinelTrap

**An SSH Honeypot and Security Event Monitoring System**

SentinelTrap is a cybersecurity project focused on capturing, monitoring, and analysing suspicious SSH activity within a controlled environment.

The project uses a containerised SSH honeypot to simulate a Linux server and record connection attempts, authentication activity, and commands executed within an emulated terminal.

> **Project Status:** In Development — v0.1.0

## 1. Project Overview

SentinelTrap provides a controlled environment for observing interactions with a simulated SSH service.

The system currently uses [Cowrie](https://github.com/cowrie/cowrie), an SSH honeypot capable of emulating a Linux shell and recording user interactions without granting access to a real operating system.

The long-term objective is to develop a security monitoring application that can process honeypot events, identify suspicious behaviour, and visualise security activity.

## 2. Project Objectives

The primary objectives are to:

- Deploy an isolated SSH honeypot using Docker.
- Capture SSH connections and authentication attempts.
- Record commands executed within the simulated Linux environment.
- Preserve security events using persistent storage.
- Develop a Python-based security event collector.
- Implement security analytics and visualisation capabilities.

## 3. Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Event collection and processing |
| Cowrie | SSH honeypot and shell emulation |
| Docker | Containerised deployment |
| Docker Compose | Container orchestration and persistent storage |
| Git & GitHub | Version control |
| Visual Studio Code | Development environment |

Additional technologies will be introduced as the project develops.

## 4. System Architecture

The current implementation consists of a Cowrie honeypot, Docker persistent storage, and an initial Python event collector.

```text
       SSH Client
           |
           | Port 2222
           v
    +----------------+
    | Cowrie         |
    | SSH Honeypot   |
    +----------------+
           |
           v
    +----------------+
    | Docker Volume  |
    | Security Logs  |
    +----------------+
           |
           v
    +----------------+
    | Python Event   |
    | Collector      |
    +----------------+
```

The Python collector currently reads a local copy of the Cowrie event logs. Direct integration with persistent storage is planned.

## 5. Current Implementation

### 5.1 SSH Honeypot

Cowrie is deployed using Docker Compose and configured to listen on port `2222`, accessible only through `127.0.0.1`.

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
- Authentication attempts.
- Commands entered in the emulated shell.
- Session termination events.

A Docker named volume has been configured to support persistent log storage. Final persistence verification remains in progress.

### 5.3 Python Event Collector

An initial Python event collector has been developed to:

- Read JSON Lines records.
- Parse security events.
- Identify malformed records.
- Extract event types, IP addresses, and session identifiers.

Validation against the original Cowrie JSONL file is ongoing.

## 6. Project Structure

```text
SentinelTrap/
├── src/
│   └── sentineltrap/
│       ├── __init__.py
│       └── collector.py
├── tests/
├── docker-compose.yml
├── .gitignore
└── README.md
```

Captured logs, authentication data, and local backups are excluded from Git version control.

## 7. Getting Started

### Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose
- Python 3.9 or later
- Git
- SSH client

### Installation

Clone the repository:

```bash
git clone https://github.com/LanMalJR/SentinelTrap.git
cd SentinelTrap
```

Start the honeypot:

```bash
docker compose up -d
```

Check its status:

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

View Cowrie's container logs:

```bash
docker compose logs --tail=50 cowrie
```

### Stopping the Honeypot

```bash
docker compose down
```

**Note:** Avoid using `docker compose down -v` unless intentionally deleting persistent volumes.

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
- [x] Implement the first JSONL event reader.
- [ ] Validate the collector against original Cowrie logs.
- [ ] Implement event filtering and normalisation.
- [ ] Add automated unit tests.
- [ ] Integrate the collector with persistent storage.

### Phase 3 — Security Analytics

- [ ] Analyse authentication attempts and session activity.
- [ ] Implement security event statistics.
- [ ] Identify suspicious activity patterns.
- [ ] Develop an interactive monitoring dashboard.

## 9. Security Considerations

SentinelTrap is intended for educational purposes and authorised defensive security research.

The initial deployment is restricted to localhost and should not be publicly exposed without additional security controls.

Honeypot logs may contain IP addresses, attempted passwords, and session data. These records must not be committed to the public repository.

## 10. Development Status

SentinelTrap is actively being developed.

The architecture, implementation details, testing procedures, and documentation will be updated as additional components are completed and verified.
