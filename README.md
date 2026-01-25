# JADE Assure — Ground-Truth Data Ingestion System

## Overview

**JADE Assure** is a schema-first, privacy-preserving data system designed to ensure ground-truth correctness, zero inference, and human-verified data ingestion. The system enforces strict validation at every layer and is intentionally designed to prevent hallucination, guessing, or automated extraction.

This repository implements a **FastAPI-based backend** with JSON schema validation, audit logging, and PostgreSQL-backed persistence.

## Core Design Principles

✓ **Schema is the single source of truth** – JSON Schema Draft 2020-12  
✓ **No inference, no guessing** – Strict validation only  
✓ **Human-in-the-loop data entry** – Manual verification required  
✓ **Immutable records** – Full audit trail  
✓ **Explicit masking** – Sensitive data marked as "MASKED"  
✓ **Local, privacy-first execution** – No external dependencies  
✓ **Full auditability** – All operations logged  

## Features

- 🔒 **JSON Schema Validation** – Enforce strict data structure compliance
- 📝 **Audit Logging** – Track all record creation and rejection events
- 🗄️ **PostgreSQL Backend** – JSONB storage for flexible, validated data
- 📊 **Schema Versioning** – Support multiple active schema versions
- 🔐 **Least-Privilege Access** – Database user with minimal permissions
- 🚀 **REST API** – FastAPI with Swagger/OpenAPI documentation

## Project Structure

```
Ja Assure/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application & endpoints
│   │   ├── schema_loader.py   # Load active schema from database
│   │   ├── validators.py      # JSON schema validation logic
│   │   ├── db.py             # Database connection management
│   │   ├── audit.py          # Audit logging functionality
│   │   └── pyrightconfig.json # Type checking configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .pylintrc             # Linting configuration
│   └── pyrightconfig.json    # Pyright configuration
├── db/
│   ├── migrations/           # SQL migration scripts
│   │   ├── 001_schema_versions.sql
│   │   ├── 002_records.sql
│   │   ├── 003_audit_logs.sql
│   │   └── 004_triggers.sql
│   ├── seed_schema.sql       # Initial schema data
│   └── README.md             # Database setup guide
├── schema/
│   ├── proposal.schema.json   # JSON Schema for proposals
│   ├── data.dictionary.md     # Human-readable data dictionary
│   └── examples/
│       ├── valid.json         # Valid example payload
│       └── masked.json        # Example with masked data
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- **Python 3.13+**
- **PostgreSQL 12+**
- **pip** and **venv**

### 1. Clone the Repository

```bash
git clone https://github.com/allu0786ansari/Secure_Jade.git
cd Secure_Jade
```

### 2. Set Up Python Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate     # Linux/macOS
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Set Up Database

**Create PostgreSQL database and user:**

```sql
-- Connect as superuser
CREATE DATABASE jade_ground_truth;
CREATE USER jade_user WITH PASSWORD 'jaassuregroup4';

-- Run migrations
psql -U jade_user -d jade_ground_truth < ../db/migrations/001_schema_versions.sql
psql -U jade_user -d jade_ground_truth < ../db/migrations/002_records.sql
psql -U jade_user -d jade_ground_truth < ../db/migrations/003_audit_logs.sql
psql -U jade_user -d jade_ground_truth < ../db/migrations/004_triggers.sql

-- Seed initial schema
psql -U jade_user -d jade_ground_truth < ../db/seed_schema.sql

-- Grant permissions (as superuser)
GRANT SELECT ON schema_versions TO jade_user;
GRANT SELECT, INSERT ON records TO jade_user;
GRANT SELECT, INSERT ON audit_logs TO jade_user;
GRANT USAGE, SELECT ON SEQUENCE audit_logs_id_seq TO jade_user;
```

### 5. Start the Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Server runs at: **`http://127.0.0.1:8000`**

## API Documentation

### POST `/records` – Create a Record

Create and validate a new record against the active schema.

**Request:**
```bash
POST http://127.0.0.1:8000/records
Content-Type: application/json

{
  "proposal_id": "PROP-001",
  "applicant_name": "John Doe",
  "applicant_email": "john@example.com",
  "has_security": true,
  "security_types": ["CCTV", "Security Guards"]
}
```

**Success Response (200 OK):**
```json
{
  "record_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "stored"
}
```

**Validation Error (422 Unprocessable Entity):**
```json
{
  "detail": "Missing required property: 'proposal_id'"
}
```

**Server Error (500 Internal Server Error):**
```json
{
  "detail": "Internal Server Error"
}
```

### Interactive API Docs

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## Testing with Postman

1. Open Postman
2. Create a **POST** request to `http://127.0.0.1:8000/records`
3. Set **Content-Type** header to `application/json`
4. Paste the example JSON payload above
5. Click **Send**

## Database Schema

### `schema_versions` Table

Stores active JSON schema versions.

```sql
CREATE TABLE schema_versions (
    id SERIAL PRIMARY KEY,
    version_number TEXT UNIQUE NOT NULL,
    schema_json JSONB NOT NULL,
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### `records` Table

Immutable record storage with JSONB data.

```sql
CREATE TABLE records (
    id UUID PRIMARY KEY,
    schema_version TEXT NOT NULL,
    data JSONB NOT NULL,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### `audit_logs` Table

Complete audit trail of all operations.

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    record_id UUID,
    action TEXT NOT NULL,
    performed_by TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Development

### Type Checking

```bash
# Check types with Pyright
cd backend
python -m pyright app/
```

### Linting

```bash
# Check code with pylint
python -m pylint app/
```

### Install Dev Dependencies

```bash
pip install pylint pyright
```

## Troubleshooting

### "Permission denied for table schema_versions"

Run this as a PostgreSQL superuser:

```sql
GRANT SELECT ON schema_versions TO jade_user;
GRANT SELECT, INSERT ON records TO jade_user;
GRANT SELECT, INSERT ON audit_logs TO jade_user;
GRANT USAGE, SELECT ON SEQUENCE audit_logs_id_seq TO jade_user;
```

### "No active schema found"

Seed the database with:

```bash
psql -U jade_user -d jade_ground_truth < db/seed_schema.sql
```

### Port 8000 already in use

Kill the process:

```bash
# Windows
taskkill /F /IM python.exe

# Linux/macOS
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          FastAPI Server                          │
│                                                                   │
│  GET  /docs          → Swagger UI                               │
│  POST /records       → Validate & Store Record                  │
│  GET  /redoc         → ReDoc (API docs)                         │
└──────────────────┬──────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐  ┌────────▼────────┐
│  schema_loader │  │   validators    │
│                │  │                 │
│ Load from DB   │  │ JSON Schema     │
│ Cache in mem   │  │ Validation      │
└────────┬───────┘  └────────┬────────┘
         │                   │
         └─────────┬─────────┘
                   │
              ┌────▼─────────────┐
              │  PostgreSQL DB   │
              │                  │
              │ schema_versions  │
              │ records          │
              │ audit_logs       │
              └──────────────────┘
```

## Security

- ✓ All user input validated against JSON Schema
- ✓ Database access restricted to least-privilege user
- ✓ All operations logged immutably
- ✓ No external API calls (local execution)
- ✓ Explicit data masking support
- ✓ Type-checked Python code

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -am 'Add my feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Open a Pull Request

## License

[Your License Here]

## Authors

- **Ja Assure Team** – Ground-truth data validation
- **Backend:** FastAPI + PostgreSQL
- **Schema:** JSON Schema Draft 2020-12

Phase 3 — Backend Ingestion API

FastAPI backend

Runtime schema loading from database

Strict JSON validation

Immutable inserts

Automatic audit logging

Project Structure
JA_ASSURE/
├── schema/
│   ├── proposal.schema.json      # Canonical JSON Schema (v1.0)
│   ├── data.dictionary.md        # Human-readable data dictionary
│   └── examples/
│       ├── valid.json            # Valid example payload
│       └── masked.json           # Masked example payload
│
├── db/
│   ├── migrations/
│   │   ├── 001_schema_versions.sql
│   │   ├── 002_records.sql
│   │   ├── 003_audit_logs.sql
│   │   └── 004_triggers.sql
│   ├── seed_schema.sql
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app
│   │   ├── db.py                 # Database connection
│   │   ├── schema_loader.py      # Load active schema from DB
│   │   ├── validators.py         # JSON Schema validation
│   │   └── audit.py              # Audit logging
│   └── requirements.txt
│
└── README.md

Database Design
Tables
schema_versions

Stores versioned JSON Schemas.

Column	Purpose
version	Schema version identifier
schema_json	Canonical JSON Schema
is_active	Active schema flag

Only one schema can be active at a time.

records

Stores immutable proposal records.

Column	Purpose
id	System-generated UUID
schema_version	Schema version used
data	JSONB payload
created_by	Operator identifier
created_at	Timestamp

⚠️ Updates are disallowed by trigger.

audit_logs

Tracks all system actions.

Action Examples
CREATE_RECORD
REJECTED_RECORD
QUERY_RECORD (future)
Backend API (Implemented)
POST /records

Creates a new immutable record after validation.

Behavior

Loads active schema from database

Validates request payload

Rejects invalid or incomplete data

Inserts record with generated UUID

Writes audit log entry

Example Request
{
  "proposal_id": "PROP-001",
  "applicant_name": "Rahul Sharma",
  "applicant_email": "rahul.sharma@example.com",
  "has_security": true,
  "security_types": ["CCTV", "Security Guards"]
}

Example Response
{
  "record_id": "c1c9c3c8-7a8e-4b9e-9e9c-3d7b6d0e2a11",
  "status": "stored"
}

Validation Rules

Payload must conform exactly to the active JSON Schema

Required fields are enforced

Conditional fields are enforced

Masked data must be explicit ("MASKED" or null)

Extra fields are rejected

No automatic enrichment or inference

Technology Stack
Layer	Technology
Backend API	FastAPI
Validation	jsonschema (Draft 2020-12)
Database	PostgreSQL (JSONB)
DB Driver	psycopg2
Runtime	Local (no cloud dependencies)
Security Model

Local-only execution

No external APIs

Least-privilege DB user

Immutable data storage

Full audit logging

Masked data never reconstructed

Current Status

✅ Schema defined and validated
✅ Database created with schema authority
✅ Backend ingestion API implemented
✅ Validation and audit logging working

Next Planned Phases

Phase 4 — Query Controller (read-only, no inference)

Phase 5 — Controlled LLM interface

Phase 6 — Manual Extraction UI

Phase 7 — Security testing & documentation

Key Guarantee

If data is not explicitly present in JSON, the system will not answer.

This guarantee is enforced by design, not by prompt instructions.