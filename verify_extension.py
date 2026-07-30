#!/usr/bin/env python3
"""Offline verifier for the independent ANS runtime evidence companion profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parent
DEFAULT_SCHEMA = ROOT / "schema" / "ans-evidence-extension.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def canonical_json_bytes(value: object) -> bytes:
    """Return the extension's deterministic RFC 8259 JSON serialization."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_digest(value: object) -> str:
    return f"sha256:{hashlib.sha256(canonical_json_bytes(value)).hexdigest()}"


def validate_document(document: dict[str, Any], schema: dict[str, Any]) -> None:
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(document)


def verify_document(document: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """Verify schema, linkage, evidence presence, and content integrity.

    Any missing, malformed, unlinked, or tampered input produces ``FAIL``.
    """

    failures: list[str] = []
    try:
        validate_document(document, schema)
    except (ValidationError, ValueError, TypeError) as exc:
        reason = exc.message if isinstance(exc, ValidationError) else str(exc)
        return {
            "verification_status": "FAIL",
            "checks": {
                "schema": "FAIL",
                "identity_linkage": "FAIL",
                "evidence_present": "FAIL",
                "evidence_hash": "FAIL",
                "audit_linkage": "FAIL",
            },
            "failure_reasons": [f"SCHEMA_INVALID: {reason}"],
        }

    identity = document["agent_identity_reference"]
    evidence_reference = document["execution_evidence_reference"]
    evidence_object = document["evidence_object"]
    declared_result = document["verification_result"]
    audit_pointer = document["audit_pointer"]

    identity_linked = (
        identity["ansId"] == evidence_reference["ansId"] == evidence_object["ansId"]
    )
    if not identity_linked:
        failures.append("IDENTITY_LINKAGE_MISMATCH")

    evidence_present = (
        bool(evidence_object)
        and evidence_reference["availability_status"] == "AVAILABLE"
    )
    if not evidence_present:
        failures.append("EVIDENCE_MISSING_OR_UNAVAILABLE")

    reference_linked = (
        evidence_reference["execution_evidence_id"]
        == evidence_object["execution_evidence_id"]
        and evidence_reference["evidence_object_id"] == evidence_object["object_id"]
    )
    if not reference_linked:
        failures.append("EVIDENCE_REFERENCE_MISMATCH")

    digest_matches = (
        evidence_present
        and sha256_digest(evidence_object) == evidence_reference["evidence_sha256"]
    )
    if not digest_matches:
        failures.append("EVIDENCE_HASH_MISMATCH")

    audit_linked = (
        audit_pointer["verification_result_id"]
        == declared_result["verification_result_id"]
    )
    if not audit_linked:
        failures.append("AUDIT_POINTER_MISMATCH")

    declared_checks_match = (
        declared_result["verification_status"] == "PASS"
        and declared_result["checks"]
        == {
            "identity_linkage": "PASS",
            "evidence_present": "PASS",
            "evidence_hash": "PASS",
        }
        and not declared_result["failure_reasons"]
    )
    if not declared_checks_match:
        failures.append("DECLARED_VERIFICATION_RESULT_MISMATCH")

    return {
        "verification_status": "PASS" if not failures else "FAIL",
        "checks": {
            "schema": "PASS",
            "identity_linkage": "PASS" if identity_linked else "FAIL",
            "evidence_present": "PASS" if evidence_present else "FAIL",
            "evidence_reference": "PASS" if reference_linked else "FAIL",
            "evidence_hash": "PASS" if digest_matches else "FAIL",
            "audit_linkage": "PASS" if audit_linked else "FAIL",
            "declared_result": "PASS" if declared_checks_match else "FAIL",
        },
        "computed_evidence_sha256": sha256_digest(evidence_object),
        "failure_reasons": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify an independent ANS runtime evidence reference document."
    )
    parser.add_argument("document", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()

    try:
        document = load_json(args.document)
        schema = load_json(args.schema)
        report = verify_document(document, schema)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report = {
            "verification_status": "FAIL",
            "checks": {"input": "FAIL"},
            "failure_reasons": [f"INPUT_INVALID: {exc}"],
        }

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verification_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
