# Pipeline Architecture

## Overview

The Gemini Reasoning Bridge 2.0 implements a **Producer-Critic topology** with strict persona isolation to prevent instruction neglect and maintain the Zero-Hallucination Protocol.

## Architectural Principles

### 1. Persona Isolation
Each agent operates with separate prompts and distinct roles to maintain clear separation of concerns:
- **Evidence Manager**: Data normalization specialist
- **Context Gardener**: Information quality ranker
- **Structural Drafter**: Narrative synthesis producer
- **Socratic Critic**: Independent logic auditor
- **Sovereign Builder**: Deterministic code generator

### 2. Schema-First Design
All inter-agent communication uses versioned JSON schemas (the 6 Canonical Objects) to ensure:
- Type safety and validation
- Backward compatibility via versioning
- Complete audit trails via SHA-256 hashing
- Reproducible results

### 3. The CCC Hard Gate
The **Claim-Citation Coverage (CCC) Metric** serves as a binary quality gate:

```
CCC = V / |U|

where:
  V = unique claims with valid source:page:line pinpoints
  |U| = total factual assertions in draft
  
GATE: CCC >= 0.95 → PASS
      CCC < 0.95 → FAIL → trigger REVISE loop
```

### 4. Zero-Hallucination Protocol
Enforced through:
- Mandatory evidence pinpoints for all factual claims
- Independent critic validation (separate model)
- Logic inversion passes (Anti-Thesis Method)
- Automated revision loops until CCC threshold met

## Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INGESTION PHASE                                          │
│    Raw Haystack → Evidence Manager → EvidenceItem_v1[]     │
│    (Gemini 3 Pro, 2M context, Anchor & Pivot)              │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. TRIAGE PHASE                                             │
│    EvidenceItems → Context Gardener → Ranked Evidence      │
│    (Signal-to-Noise filtering, Quality scoring)            │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SYNTHESIS PHASE                                          │
│    Ranked Evidence → Structural Drafter →                   │
│    SentenceRow_v1[] + ClaimLedger_v1                       │
│    (Narrative generation with mandatory trace maps)        │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. AUDIT PHASE (The Hard Gate)                             │
│    ClaimLedger + SentenceMap → Socratic Critic →           │
│    AuditReport_v1 with CCC calculation                      │
│    (GPT-5.2, temp=1.0, Logic Inversion)                    │
└───────────────┬─────────────────────────────────────────────┘
                │
         ┌──────┴──────┐
         │ CCC >= 0.95?│
         └──────┬──────┘
                │
        ┌───────┴───────┐
        │               │
       YES             NO
        │               │
        ▼               ▼
    ┌────────┐    ┌──────────┐
    │  PASS  │    │ REVISE   │
    │ Output │    │ (max 3x) │
    └────────┘    └─────┬────┘
                        │
                        └──→ Back to Drafter
```

## Model Assignment Strategy

### Why Gemini 3 Pro for Evidence & Context?
- 2M token context window handles massive haystacks
- Strong multimodal capabilities for "Anchor & Pivot"
- Cost-effective for high-volume processing

### Why GPT-5.2 for Critic?
- Superior reasoning capabilities for logic inversion
- Temperature=1.0 enables Monte Carlo diversity
- External model prevents "approval bias"

### Why Qwen3-Next for Builder?
- Deterministic code generation (temperature=0.0)
- Strong adherence to specifications
- Fast iteration cycles

## Communication Protocol

All agents communicate via JSON objects conforming to Canonical Schemas:

1. **Evidence Manager** outputs:
   ```json
   {"schema_version": "v1", "evidence_id": "...", ...}
   ```

2. **Context Gardener** enriches with:
   ```json
   {"quality_score": 0.85, "ranking": 1, ...}
   ```

3. **Structural Drafter** produces:
   ```json
   {"sentence_id": "...", "pinpoints": [...], ...}
   ```

4. **Socratic Critic** validates and returns:
   ```json
   {"audit_status": "PASS|FAIL", "ccc_metric": {...}, ...}
   ```

## Error Handling

### Revision Loop Strategy
- Maximum 3 revision cycles to prevent infinite loops
- Each revision receives specific guidance from Critic
- Failed audits include targeted suggestions for improvement

### Spec-First Protocol Lock
The Sovereign Builder enforces a hard requirement:
```python
if spec_hash != architecture_ledger['active_spec']['spec_hash']:
    raise SpecVerificationError("No code without approved spec")
```

### Hash Verification Chain
Every object includes SHA-256 hashes:
- Evidence items: `text_hash` for content deduplication
- Trace maps: `trace_hash` for integrity validation
- Audit reports: `audit_hash` for tamper detection
- Specs: `spec_hash` for approval verification

## Performance Considerations

### Context Management
- Context Gardener filters low-quality evidence before passing to Drafter
- Progressive disclosure: only load full evidence when needed
- Hash-based deduplication prevents redundant processing

### Parallel Processing
While the main pipeline is sequential, internal operations can parallelize:
- Evidence normalization can batch process
- Multiple claims can be audited concurrently
- Signal-to-noise scoring parallelizes across evidence items

### Optimization Hooks
The pipeline supports DSPy's automatic optimization:
```python
# Signatures can be optimized based on training data
optimizer = dspy.BootstrapFewShot()
optimized_drafter = optimizer.compile(drafter, trainset=examples)
```

## Extension Points

### Custom Agents
Add new agents by defining DSPy Signatures:
```python
class CustomAgent(dspy.Signature):
    """Your agent description and instructions"""
    input_field = dspy.InputField(desc="...")
    output_field = dspy.OutputField(desc="...")
```

### Custom Schemas
Extend Canonical Objects by:
1. Creating new schema version (e.g., `EvidenceItem_v2`)
2. Updating `config.yml` schema versions
3. Implementing backward compatibility in parsers

### Pipeline Hooks
Insert custom logic at key points:
```python
class ExtendedBridge(ReasoningBridge):
    def _post_evidence_hook(self, evidence):
        # Custom processing after evidence stage
        return enhanced_evidence
```
