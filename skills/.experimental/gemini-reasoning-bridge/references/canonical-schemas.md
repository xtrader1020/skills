# Canonical Object Schemas

This document defines the 6 Canonical Objects used in the Gemini Reasoning Bridge 2.0 system. All objects are versioned and use SHA-256 fingerprinting for integrity verification.

## 1. EvidenceItem_v1

Normalized source data with stable identifiers and hash-based versioning.

```json
{
  "schema_version": "v1",
  "evidence_id": "uuid-string",
  "text_hash": "sha256-hash",
  "content": "string",
  "source_metadata": {
    "file_path": "string",
    "page_number": "integer",
    "line_range": [start, end],
    "timestamp": "iso8601-datetime"
  },
  "multimodal_anchors": [
    {
      "anchor_id": "integer (1-14)",
      "anchor_type": "string (text|image|table)",
      "coordinates": {"x": "float", "y": "float"}
    }
  ],
  "quality_score": "float (0.0-1.0)"
}
```

**Fields:**
- `evidence_id`: Unique identifier (UUID) for the evidence item
- `text_hash`: SHA-256 hash of content for versioning and deduplication
- `content`: The actual evidence text or reference
- `source_metadata`: Provenance information for audit trail
- `multimodal_anchors`: For images/documents, the 14 anchor points used in "Anchor & Pivot" methodology
- `quality_score`: Signal-to-noise ratio calculated by Context Gardener

## 2. SentenceRow_v1

Trace map linking each claim in the narrative to its evidence source.

```json
{
  "schema_version": "v1",
  "sentence_id": "uuid-string",
  "sentence_text": "string",
  "claim_type": "string (factual|analytical|opinion)",
  "evidence_ids": ["uuid-string-array"],
  "pinpoints": [
    {
      "evidence_id": "uuid-string",
      "source": "string",
      "page": "integer",
      "line": "integer"
    }
  ],
  "confidence_score": "float (0.0-1.0)",
  "trace_hash": "sha256-hash"
}
```

**Fields:**
- `sentence_id`: Unique identifier for the sentence
- `sentence_text`: The actual sentence from the draft narrative
- `claim_type`: Classification of the claim (factual requires evidence)
- `evidence_ids`: Array of evidence items supporting this claim
- `pinpoints`: Exact source:page:line references for each piece of evidence
- `confidence_score`: Drafter's confidence in the claim-evidence mapping
- `trace_hash`: Hash of the complete trace for integrity verification

## 3. AuditReport_v1

Output from the Socratic Critic containing verification results and CCC metric.

```json
{
  "schema_version": "v1",
  "audit_id": "uuid-string",
  "timestamp": "iso8601-datetime",
  "audit_status": "string (PASS|FAIL)",
  "ccc_metric": {
    "V": "integer (claims with valid pinpoints)",
    "U": "integer (total factual assertions)",
    "ratio": "float (V/U)",
    "threshold": "float (0.95)"
  },
  "logic_inversion_results": {
    "anti_thesis_checks": "integer",
    "contradictions_found": "integer",
    "unsupported_claims": ["sentence-id-array"]
  },
  "revision_required": "boolean",
  "revision_guidance": [
    {
      "sentence_id": "uuid-string",
      "issue": "string",
      "suggestion": "string"
    }
  ],
  "audit_hash": "sha256-hash"
}
```

**Fields:**
- `audit_status`: Binary PASS/FAIL based on CCC threshold
- `ccc_metric`: Claim-Citation Coverage calculation (V / |U|)
- `logic_inversion_results`: Results from the Anti-Thesis Method
- `revision_required`: Whether the draft needs revision
- `revision_guidance`: Specific issues and suggestions for improvement

## 4. ClaimLedger_v1

Complete registry of all claims made in the draft narrative.

```json
{
  "schema_version": "v1",
  "ledger_id": "uuid-string",
  "claims": [
    {
      "claim_id": "uuid-string",
      "claim_text": "string",
      "claim_type": "string (factual|analytical|opinion)",
      "sentence_id": "uuid-string",
      "evidence_count": "integer",
      "has_valid_pinpoint": "boolean"
    }
  ],
  "statistics": {
    "total_claims": "integer",
    "factual_claims": "integer",
    "claims_with_evidence": "integer",
    "coverage_ratio": "float"
  },
  "ledger_hash": "sha256-hash"
}
```

**Fields:**
- `claims`: Array of all claims in the draft
- `statistics`: Aggregate metrics for audit purposes
- `ledger_hash`: Hash of complete ledger for integrity

## 5. ArchitectureLedger_v1

Registry of approved architectural decisions for the Sovereign Builder.

```json
{
  "schema_version": "v1",
  "ledger_id": "uuid-string",
  "decisions": [
    {
      "decision_id": "uuid-string",
      "title": "string",
      "description": "string",
      "status": "string (approved|pending|rejected)",
      "spec_hash": "sha256-hash",
      "timestamp": "iso8601-datetime"
    }
  ],
  "active_spec": {
    "spec_id": "uuid-string",
    "spec_hash": "sha256-hash",
    "version": "string"
  },
  "ledger_hash": "sha256-hash"
}
```

**Fields:**
- `decisions`: Array of architectural decisions
- `active_spec`: Currently approved specification for implementation
- `spec_hash`: Used to validate spec.md before code generation

## 6. SpecDocument_v1

The approved specification document for code implementation.

```json
{
  "schema_version": "v1",
  "spec_id": "uuid-string",
  "spec_hash": "sha256-hash",
  "title": "string",
  "description": "string",
  "requirements": [
    {
      "requirement_id": "uuid-string",
      "description": "string",
      "priority": "string (must|should|could)",
      "acceptance_criteria": ["string-array"]
    }
  ],
  "architecture": {
    "components": ["string-array"],
    "dependencies": ["string-array"],
    "constraints": ["string-array"]
  },
  "approval": {
    "approved_by": "string",
    "approved_at": "iso8601-datetime",
    "architecture_ledger_id": "uuid-string"
  },
  "content_hash": "sha256-hash"
}
```

**Fields:**
- `spec_hash`: Primary verification hash matched against architecture ledger
- `requirements`: Detailed requirements with acceptance criteria
- `architecture`: High-level architectural decisions
- `approval`: Approval metadata linking to architecture ledger

## Schema Validation Rules

1. **Version Control**: All schemas include a `schema_version` field for backward compatibility
2. **Hash Integrity**: Critical objects include SHA-256 hashes for verification
3. **Traceability**: All IDs are UUIDs to enable complete audit trails
4. **Timestamps**: ISO 8601 format for all datetime fields
5. **Validation**: All objects must validate against their schema before processing

## Usage in Pipeline

1. **Evidence Manager** → produces `EvidenceItem_v1` objects
2. **Context Gardener** → ranks and filters `EvidenceItem_v1` objects
3. **Structural Drafter** → consumes evidence, produces `SentenceRow_v1` and `ClaimLedger_v1`
4. **Socratic Critic** → consumes sentence map and ledger, produces `AuditReport_v1`
5. **Sovereign Builder** → validates `SpecDocument_v1` against `ArchitectureLedger_v1`, produces code
