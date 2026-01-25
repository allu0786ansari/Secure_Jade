Ja Assure — Ground-Truth Data Ingestion System
Overview

Ja Assure is a schema-first, privacy-preserving data system designed to ensure ground-truth correctness, zero inference, and human-verified data ingestion.
The system enforces strict validation at every layer and is intentionally designed to prevent hallucination, guessing, or automated extraction.

This repository currently implements Phases 1–3 of the architecture:

Canonical schema definition

Database setup with schema authority

Secure backend ingestion with audit logging

Core Design Principles

Schema is the single source of truth

No inference, no guessing

Human-in-the-loop data entry

Immutable records

Explicit masking ("MASKED")

Local, privacy-first execution

Full auditability

Architecture (Implemented So Far)
Phase 1 — Schema & Data Dictionary

Human-readable Data Dictionary

Machine-enforceable JSON Schema (Draft 2020-12)

Example payloads for validation

Phase 2 — Database & Schema Authority

PostgreSQL with JSONB storage

Versioned schema storage

Immutable records

Audit logging

Least-privilege database access

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