from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "ans-evidence-extension.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "agent_identity_with_execution_evidence.json"
VERIFIER_PATH = ROOT / "verify_extension.py"

module_spec = importlib.util.spec_from_file_location(
    "ans_evidence_verifier", VERIFIER_PATH
)
assert module_spec is not None and module_spec.loader is not None
verifier = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(verifier)


@pytest.fixture
def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def example() -> dict:
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


def test_identity_can_link_to_execution_evidence(example: dict, schema: dict) -> None:
    verifier.validate_document(example, schema)

    ans_id = example["agent_identity_reference"]["ansId"]
    assert ans_id == example["execution_evidence_reference"]["ansId"]
    assert ans_id == example["evidence_object"]["ansId"]
    assert (
        example["execution_evidence_reference"]["execution_evidence_id"]
        == example["evidence_object"]["execution_evidence_id"]
    )
    assert (
        example["execution_evidence_reference"]["evidence_object_id"]
        == example["evidence_object"]["object_id"]
    )


def test_evidence_hash_can_be_verified(example: dict, schema: dict) -> None:
    report = verifier.verify_document(example, schema)

    assert report["verification_status"] == "PASS"
    assert report["checks"]["evidence_hash"] == "PASS"
    assert (
        report["computed_evidence_sha256"]
        == example["execution_evidence_reference"]["evidence_sha256"]
    )

    tampered = copy.deepcopy(example)
    tampered["evidence_object"]["result"]["summary"] = "Tampered result"
    tampered_report = verifier.verify_document(tampered, schema)
    assert tampered_report["verification_status"] == "FAIL"
    assert tampered_report["checks"]["evidence_hash"] == "FAIL"
    assert "EVIDENCE_HASH_MISMATCH" in tampered_report["failure_reasons"]


def test_missing_evidence_fails_closed(example: dict, schema: dict) -> None:
    missing_evidence = copy.deepcopy(example)
    del missing_evidence["evidence_object"]

    report = verifier.verify_document(missing_evidence, schema)

    assert report["verification_status"] == "FAIL"
    assert report["checks"]["schema"] == "FAIL"
    assert report["checks"]["evidence_present"] == "FAIL"
    assert report["failure_reasons"][0].startswith("SCHEMA_INVALID:")


def test_invalid_identity_reference_is_rejected(example: dict, schema: dict) -> None:
    invalid_identity = copy.deepcopy(example)
    invalid_identity["agent_identity_reference"]["ansId"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        verifier.validate_document(invalid_identity, schema)

    report = verifier.verify_document(invalid_identity, schema)
    assert report["verification_status"] == "FAIL"
    assert report["checks"]["schema"] == "FAIL"


def test_unavailable_evidence_fails_closed(example: dict, schema: dict) -> None:
    unavailable = copy.deepcopy(example)
    unavailable["execution_evidence_reference"]["availability_status"] = "UNAVAILABLE"

    report = verifier.verify_document(unavailable, schema)

    assert report["verification_status"] == "FAIL"
    assert report["checks"]["evidence_present"] == "FAIL"
    assert "EVIDENCE_MISSING_OR_UNAVAILABLE" in report["failure_reasons"]


def test_fail_status_requires_a_failure_reason(example: dict, schema: dict) -> None:
    invalid_result = copy.deepcopy(example)
    invalid_result["verification_result"]["verification_status"] = "FAIL"
    invalid_result["verification_result"]["checks"]["evidence_hash"] = "FAIL"

    with pytest.raises(ValidationError):
        verifier.validate_document(invalid_result, schema)


def test_audit_pointer_mismatch_fails_closed(example: dict, schema: dict) -> None:
    mismatched_audit = copy.deepcopy(example)
    mismatched_audit["audit_pointer"]["verification_result_id"] = (
        "urn:titmas:verification:different-result"
    )

    report = verifier.verify_document(mismatched_audit, schema)

    assert report["verification_status"] == "FAIL"
    assert report["checks"]["audit_linkage"] == "FAIL"
    assert "AUDIT_POINTER_MISMATCH" in report["failure_reasons"]


def test_evidence_reference_mismatch_fails_closed(example: dict, schema: dict) -> None:
    mismatched_reference = copy.deepcopy(example)
    mismatched_reference["execution_evidence_reference"]["execution_evidence_id"] = (
        "urn:titmas:execution-evidence:different-operation"
    )

    report = verifier.verify_document(mismatched_reference, schema)

    assert report["verification_status"] == "FAIL"
    assert report["checks"]["evidence_reference"] == "FAIL"
    assert "EVIDENCE_REFERENCE_MISMATCH" in report["failure_reasons"]
