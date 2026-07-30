# ANS Reference Publication Checklist

Status: `PUBLIC_REFERENCE_VERIFIED_ISSUE_FINAL_DRAFT_HUMAN_COMMIT_REQUIRED`

This checklist covers the independent reference repository only. It does not
authorize an official ANS Issue or Pull Request.

## Scope

- [x] Package contains only the standalone README, Apache-2.0 LICENSE,
  verification configuration, schema, synthetic example, verifier, tests,
  proposal, Issue draft, checklist, and implementation/readiness reports.
- [x] No source repository `.git` directory or history was copied.
- [x] No unrelated `agent-evidence` source, research, email, governance,
  credential, or customer material was copied.
- [x] The private source repository remains unchanged.

## Current ANS Alignment

- [x] Upstream source checked at
  `d8ed4bb6b105863710a07dfce9ceb1c3145de486`.
- [x] `ansId` and `ansName` are represented as separate concepts.
- [x] The proposal records the signed JCS event, shared Merkle transparency
  log, SCITT COSE receipt, lifecycle status, and offline verification context.
- [x] The proposal compares existing-event metadata, a new evidence-reference
  event, and an external companion profile.
- [x] The first-discussion recommendation is the non-invasive companion
  profile.
- [x] No field or event is claimed to be accepted by ANS.

## License and Attribution

- [x] Source repository license is explicitly Apache-2.0.
- [x] The same LICENSE is included without modification.
- [x] README identifies the source repository and exact source commits.
- [x] No upstream ANS source code is copied.
- [x] Human confirmed contribution rights and signed the public base commit.

## Content and Security

- [x] Example data is synthetic and uses `example.test` or `urn:example`
  identifiers.
- [x] No real personal, medical, customer, or runtime data is included in the
  schema or synthetic example. The contributor name and email appear only in
  attribution and the explicitly requested DCO handoff.
- [x] No API key, token, password, private key, `.env` content, or private
  communication is intentionally included.
- [x] No private local absolute path is intentionally included.
- [x] The project says independent and development-stage.
- [x] The project denies official ANS status, endorsement, conformance,
  production readiness, and legal non-repudiation.
- [x] Identity, execution evidence, authorization, verification, and truth
  remain separate.

## Verification

- [x] JSON Schema is structurally valid.
- [x] Synthetic example validates and returns `PASS`.
- [x] Missing evidence fails closed.
- [x] Unavailable evidence fails closed.
- [x] Invalid identity reference is rejected.
- [x] Tampered evidence is rejected.
- [x] `pytest` passes: `8 passed`.
- [x] `ruff check .` passes.
- [x] `pre-commit run --all-files` passes.
- [x] All eight Issue-draft repository and artifact links returned HTTP 200
  without GitHub authentication.
- [x] Secret, private-path, example-data, and overclaim scans pass.

The final results are recorded in `PUBLIC_RELEASE_READINESS_REPORT.md`.

## Human DCO Gate

```text
PUBLIC_BASE_COMMIT=0188da00cba8cc43c1257cd7e6126974a92a1ef1
PUBLIC_BASE_DCO_SIGNOFF_PRESENT=true
AI_DCO_SIGNOFF_PERFORMED=false
HUMAN_DCO_SIGNOFF_REQUIRED=true
FINAL_DRAFT_COMMIT_CREATED=false
```

Codex must not add `Signed-off-by:`. After reviewing the staged Issue-finalization
diff and accepting the Developer Certificate of Origin, Bin Zhang may run:

```bash
git commit -s -m "Finalize ANS upstream discussion draft"
```

Before that command, verify the local identity:

```bash
git config --local user.name
git config --local user.email
git diff --cached --check
git diff --cached --stat
```

Expected identity:

```text
Bin Zhang
joy7759@gmail.com
```

## External Actions

```text
PUBLIC_GITHUB_REPOSITORY_CREATED=true
REFERENCE_REPOSITORY_PUSHED=true
OFFICIAL_ANS_ISSUE_CREATED=false
OFFICIAL_ANS_PULL_REQUEST_CREATED=false
ANS_MAINTAINER_REVIEW_OBSERVED=false
```

The public base repository and immutable artifact links are verified. The
Issue-finalization commit and any push remain human actions. Posting the Issue
requires explicit `CONFIRM_ANS_EXTERNAL_SUBMISSION`; a later Pull Request
requires maintainer scope acceptance and separate authorization.
