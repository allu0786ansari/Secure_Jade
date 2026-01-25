"""Payload validation against active JSON schema."""

from __future__ import annotations

from typing import Any

from jsonschema.exceptions import ValidationError


def validate_payload(validator: Any, payload: Any) -> None:
    """Validate payload against the provided JSON schema validator."""
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)

    if errors:
        raise ValidationError(errors[0].message)
