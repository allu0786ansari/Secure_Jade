# Data Dictionary — Proposal Record (v1.1)

This document defines the canonical, human-curated fields extracted manually from masked proposal forms.
The JSON schema is derived directly from this dictionary.

Core principles:
- Human-in-the-loop extraction only
- No OCR or automated inference
- Masked data must remain masked
- Schema is the single source of truth

---

## Core Identifier

### proposal_id
- **Type:** string
- **Required:** Yes
- **Description:** Unique identifier for the proposal
- **Source:** Proposal Form (Header)
- **Masking Allowed:** No

---

## Proposer Details

### proposer.name
- **Type:** string | null
- **Required:** No
- **Description:** Name of the proposer
- **Source:** Proposal Form – Proposer Details
- **Masking Allowed:** Yes
- **Masking Value:** `"MASKED"`

---

### proposer.email
- **Type:** string | null
- **Required:** No
- **Description:** Email address of the proposer
- **Source:** Proposal Form – Proposer Details
- **Masking Allowed:** Yes
- **Format Rule:** Valid email format

---

## Premises Details

### premises.address
- **Type:** string | null
- **Required:** No
- **Description:** Risk location / premises address
- **Source:** Proposal Form – Risk Location
- **Masking Allowed:** Yes

---

### premises.construction_type
- **Type:** string | null
- **Required:** No
- **Description:** Construction type of premises (e.g., RCC, Brick, Mixed)
- **Source:** Proposal Form – Construction Details
- **Masking Allowed:** Yes

---

## Security Details

### security.has_security
- **Type:** boolean
- **Required:** Yes
- **Description:** Indicates whether any security arrangements exist
- **Source:** Proposal Form – Security Section
- **Allowed Values:** true, false

---

### security.cctv.installed
- **Type:** boolean | null
- **Required:** Conditional
- **Condition:** Required if `security.has_security = true`
- **Description:** Whether CCTV system is installed
- **Source:** Proposal Form – CCTV Details

---

### security.cctv.coverage_areas
- **Type:** array[string]
- **Required:** No
- **Description:** Areas covered by CCTV cameras
- **Source:** Proposal Form – CCTV Coverage

---

### security.alarm_system.installed
- **Type:** boolean | null
- **Required:** Conditional
- **Description:** Whether alarm system is installed
- **Source:** Proposal Form – Alarm Details

---

### security.alarm_system.type
- **Type:** string | null
- **Required:** No
- **Description:** Type of alarm system (Burglar / Fire / Combined)
- **Source:** Proposal Form – Alarm Details

---

### security.guards.present
- **Type:** boolean | null
- **Required:** No
- **Description:** Whether security guards are present
- **Source:** Proposal Form – Guard Details

---

### security.guards.armed
- **Type:** boolean | null
- **Required:** No
- **Description:** Whether guards are armed
- **Source:** Proposal Form – Guard Details

---

## Claims History

### claims_history.has_claims
- **Type:** boolean | null
- **Required:** No
- **Description:** Indicates whether claims occurred in past years
- **Source:** Proposal Form – Claims History

---

### claims_history.remarks
- **Type:** string | null
- **Required:** No
- **Description:** Claim details or NIL
- **Source:** Proposal Form – Claims History

---

## Normalization Rules

- Currency values (if added later) must be normalized to a single currency
- Dates must follow ISO-8601 format
- Checked boxes → `true`
- Unchecked boxes → `false`
- “Nil”, “N.A.” → `null`
- Masked values must be explicitly marked `"MASKED"`

---

## Notes

- All data is manually transcribed
- No data is inferred or reconstructed
- This dictionary is authoritative for schema and validation
