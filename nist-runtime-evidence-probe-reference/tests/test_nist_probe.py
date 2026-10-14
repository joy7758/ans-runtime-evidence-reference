import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = REPOSITORY_ROOT / "examples"
VALIDATOR_PATH = REPOSITORY_ROOT / "nist_probe" / "validator.py"
SPEC = importlib.util.spec_from_file_location("nist_runtime_probe", VALIDATOR_PATH)
assert SPEC and SPEC.loader
PROBE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PROBE
SPEC.loader.exec_module(PROBE)


def fixture(name: str) -> Path:
    return EXAMPLES / name


def write_variant(tmp_path: Path, source_name: str, mutate) -> Path:
    source = fixture(source_name)
    value = json.loads(source.read_text(encoding="utf-8"))
    mutate(value)
    target = tmp_path / source.name
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    shutil.copytree(EXAMPLES / "evidence", tmp_path / "evidence")
    return target


def test_passes_successful_execution():
    evaluation = PROBE.evaluate_probe(fixture("successful_execution.json"))
    assert evaluation.result == PROBE.PASS
    assert set(evaluation.checked_dimensions) == {
        "Identity",
        "Authorization",
        "Tool Invocation",
        "Execution Trace",
        "Outcome",
        "Integrity",
        "Auditability",
    }


def test_rejects_unauthorized_tool_call():
    evaluation = PROBE.evaluate_probe(fixture("unauthorized_tool_call.json"))
    assert evaluation.result == PROBE.FAIL_UNAUTHORIZED_TOOL_CALL


def test_missing_evidence_fails_closed():
    evaluation = PROBE.evaluate_probe(fixture("missing_evidence.json"))
    assert evaluation.result == PROBE.FAIL_MISSING_EVIDENCE


def test_rejects_evidence_tampering():
    evaluation = PROBE.evaluate_probe(fixture("evidence_tampering.json"))
    assert evaluation.result == PROBE.FAIL_EVIDENCE_TAMPERING
    assert "does not match computed digest" in evaluation.reasons[0]


def test_rejects_outcome_mismatch():
    evaluation = PROBE.evaluate_probe(fixture("outcome_mismatch.json"))
    assert evaluation.result == PROBE.FAIL_OUTCOME_MISMATCH


def test_rejects_evidence_only_unauthorized_tool_with_recomputed_hash(tmp_path):
    variant = write_variant(
        tmp_path,
        "successful_execution.json",
        lambda value: None,
    )
    evidence_path = tmp_path / "evidence" / "case-004-execution-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["tool_invocations"][0]["tool"] = "shell.exec"
    evidence_path.write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )

    value = json.loads(variant.read_text(encoding="utf-8"))
    value["evidence_reference"]["sha256"] = (
        "sha256:" + hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    )
    variant.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    evaluation = PROBE.evaluate_probe(variant)
    assert evaluation.result == PROBE.FAIL_UNAUTHORIZED_TOOL_CALL
    assert "evidence:shell.exec" in evaluation.reasons[0]


def test_declared_verification_result_is_not_trusted(tmp_path):
    def forge_declared_result(value):
        value["verification_result"] = "FAIL_OUTCOME_MISMATCH"

    variant = write_variant(
        tmp_path,
        "successful_execution.json",
        forge_declared_result,
    )
    evaluation = PROBE.evaluate_probe(variant)
    assert evaluation.result == PROBE.PASS


def test_schema_rejects_unknown_top_level_fields(tmp_path):
    def add_unknown(value):
        value["official_nist_approval"] = True

    variant = write_variant(
        tmp_path,
        "successful_execution.json",
        add_unknown,
    )
    evaluation = PROBE.evaluate_probe(variant)
    assert evaluation.result == PROBE.ERROR_INVALID_PROBE


def test_rejects_evidence_path_escape(tmp_path):
    def escape_fixture_root(value):
        value["evidence_reference"]["uri"] = "../outside.json"

    variant = write_variant(
        tmp_path,
        "successful_execution.json",
        escape_fixture_root,
    )
    evaluation = PROBE.evaluate_probe(variant)
    assert evaluation.result == PROBE.ERROR_INVALID_PROBE
    assert "escapes the fixture root" in evaluation.reasons[0]


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("successful_execution.json", "PASS"),
        ("unauthorized_tool_call.json", "FAIL_UNAUTHORIZED_TOOL_CALL"),
        ("missing_evidence.json", "FAIL_MISSING_EVIDENCE"),
        ("evidence_tampering.json", "FAIL_EVIDENCE_TAMPERING"),
        ("outcome_mismatch.json", "FAIL_OUTCOME_MISMATCH"),
    ],
)
def test_example_expected_results_match_computed_results(name, expected):
    value = json.loads(fixture(name).read_text(encoding="utf-8"))
    assert value["verification_result"] == expected
    assert PROBE.evaluate_probe(fixture(name)).result == expected
