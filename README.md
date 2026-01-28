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
- 📊 **Schema Versioning** – Support multiple active schema versions (v1.1 active)
- 🔐 **Least-Privilege Access** – Database user with minimal permissions
- 🚀 **REST API** – FastAPI with Swagger/OpenAPI documentation
- 🔍 **Field-Level Queries** – Query nested fields using dot notation
- 🛡️ **Query Validation** – Reject disallowed queries with audit trail

## Project Structure

```
Ja Assure/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application & endpoints
│   │   ├── schema_loader.py   # Load active schema from database
│   │   ├── validators.py      # JSON schema validation logic
│   │   ├── db.py              # Database connection management
│   │   ├── audit.py           # Audit logging functionality
│   │   ├── query_controller.py # Record retrieval by ID
│   │   ├── field_resolver.py  # Resolve nested field queries
│   │   ├── query_rejection.py # Query rejection handling
│   │   ├── query_rules.py     # Field access rules
│   │   └── pyrightconfig.json # Type checking configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .pylintrc              # Linting configuration
│   └── pyrightconfig.json     # Pyright configuration
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
- **pip** and **venv** along with **pdfplumber**

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

**Or with the virtual environment on Windows:**
```powershell
cd backend
& "../.venv/Scripts/python.exe" -m uvicorn app.main:app --reload
```

## API Documentation

### POST `/records` – Create a Record

Create and validate a new record against the active schema (v1.1).

**Request:**
```bash
POST http://127.0.0.1:8000/records
Content-Type: application/json

{
  "proposal_id": "PROP-001",
  "proposer": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "security": {
    "has_security": true,
    "cctv": {
      "installed": true,
      "coverage_areas": ["entrance", "parking"]
    },
    "alarm_system": {
      "installed": true,
      "type": "Fire"
    }
  }
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

### GET `/records/{record_id}` – Retrieve a Record

Retrieve a stored record by its unique ID.

**Request:**
```bash
GET http://127.0.0.1:8000/records/550e8400-e29b-41d4-a716-446655440000
```

**Success Response (200 OK):**
```json
{
  "record_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {
    "proposal_id": "PROP-001",
    "proposer": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "security": {
      "has_security": true,
      "cctv": {
        "installed": true
      }
    }
  }
}
```

### POST `/query` – Query a Specific Field

Query a specific field from a record using dot notation for nested fields.

**Request:**
```bash
POST http://127.0.0.1:8000/query
Content-Type: application/json

{
  "record_id": "550e8400-e29b-41d4-a716-446655440000",
  "field": "security.cctv.installed"
}
```

**Success Response (200 OK):**
```json
{
  "record_id": "550e8400-e29b-41d4-a716-446655440000",
  "field": "security.cctv.installed",
  "answer": true
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Query type not supported"
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

## Schema Version: v1.1

The active schema version is **v1.1**, which defines the structure for proposal records including:

- **Proposer Details**: Name and email (supports masking)
- **Premises Information**: Address and construction type
- **Security Details**: CCTV, alarm systems, security guards
- **Claims History**: Past claims and remarks

The schema follows JSON Schema Draft 2020-12 and enforces:
- Required fields: `proposal_id` and `security.has_security`
- Conditional validation: If `has_security` is true, CCTV and alarm_system details are required
- Support for `null` values to represent masked data
- Type safety for all fields

See [schema/proposal.schema.json](schema/proposal.schema.json) for the complete schema definition and [schema/data.dictionary.md](schema/data.dictionary.md) for field-level documentation.

## Database Schema

### `schema_versions` Table

Stores active JSON schema versions.

```sql
CREATE TABLE schema_versions (
    id SERIAL PRIMARY KEY,
    version TEXT UNIQUE NOT NULL,
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

