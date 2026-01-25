# Data Dictionary — Proposal Record (v1.0)

This document defines the canonical fields extracted manually from proposal forms.
All fields follow schema-first, ground-truth-only rules.

---

## Core Identifiers

### proposal_id
- **Type:** string
- **Required:** Yes
- **Description:** Unique identifier for the proposal
- **Allowed Values:** Any non-empty string
- **Masking Allowed:** No

---

## Applicant Information

### applicant_name
- **Type:** string
- **Required:** Yes
- **Description:** Full name of the applicant
- **Allowed Values:** Alphabetic characters and spaces
- **Masking Allowed:** Yes

---

### applicant_email
- **Type:** string
- **Required:** No
- **Description:** Email address of the applicant
- **Allowed Values:** Valid email format
- **Masking Allowed:** Yes

---

## Security Information

### has_security
- **Type:** boolean
- **Required:** Yes
- **Description:** Indicates whether the proposal includes any security arrangements
- **Allowed Values:** true, false
- **Masking Allowed:** No

---

### security_types
- **Type:** array[string]
- **Required:** Conditional
- **Condition:** Required only if `has_security = true`
- **Description:** List of security mechanisms mentioned in the proposal
- **Allowed Values:** Free-text strings
- **Masking Allowed:** Yes

---

## Masking Rules

- Masked fields must contain the literal string `"MASKED"`
- Masked data must never be inferred or reconstructed
- Missing fields must be treated as `"Information not available"`

---

## Notes

- All data is manually transcribed by a human operator
- No OCR or automated extraction is permitted
- This dictionary is the single source of truth
