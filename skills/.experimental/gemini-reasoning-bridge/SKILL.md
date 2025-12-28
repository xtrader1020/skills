---
name: gemini-reasoning-bridge
description: Modular reasoning pipeline implementing the Hardened Legal Toolchain and Producer-Critic topology for zero-hallucination verification. Use when you need to process large documents or research with strict citation requirements, verify factual claims against source evidence with traceable pinpoints, generate narratives with mandatory evidence backing (CCC at least 0.95), or implement code from specifications with hash-verified approval gates. Ideal for legal research, academic papers, compliance documentation, or any task requiring auditable truth claims.
---

# Gemini Reasoning Bridge 2.0

## Overview

The Gemini Reasoning Bridge is a **schema-first, multi-agent reasoning pipeline** that transforms raw research data into verified, traceable output with zero-hallucination guarantees. It implements a **Producer-Critic topology** with strict persona isolation and enforces the **Zero-Hallucination Protocol** via the CCC (Claim-Citation Coverage) Hard Gate.

**Core capability:** Every factual claim in generated output is automatically linked to a specific `source:page:line` pinpoint, independently audited, and rejected if coverage falls below 95%.

## When to Use This Skill

Use the Gemini Reasoning Bridge when you need:

1. **Research Verification**: Process academic papers, legal documents, or technical reports with strict citation requirements
2. **Evidence-Based Writing**: Generate narratives where every claim must be backed by verifiable source evidence
3. **Compliance Documentation**: Create audit-ready documents with complete traceability
4. **Truth Validation**: Verify existing documents to ensure all factual assertions have valid citations
5. **Spec-First Development**: Generate code only from hash-verified, approved specifications

## Quick Start

### Basic Usage: Verify a Document

```python
from scripts.pipeline import ReasoningBridge

# Initialize the pipeline
bridge = ReasoningBridge("scripts/config.yml")

# Process your research data
haystack = """
Your research content with sources...
Study A (2024, p.42) found that X...
According to Report B (2023, p.15), Y...
"""

result = bridge.process_haystack(haystack)

# Check if all claims are properly cited
if result['status'] == 'PASS':
    print(f"✓ Verified! CCC: {result['audit_report']['ccc_metric']['ratio']:.0%}")
else:
    print(f"✗ Issues found:")
    for issue in result['audit_report']['revision_guidance']:
        print(f"  - {issue['issue']}")
```

### Generate Code with Spec-First Protocol

```python
# Only generates code if spec hash matches architecture ledger
spec_md = open('approved_spec.md').read()
architecture_ledger = load_architecture_ledger()

code = bridge.generate_code(spec_md, architecture_ledger)
```

## Pipeline Architecture

The bridge operates in 5 sequential stages with automatic revision loops:

```
Raw Data → Evidence Manager → Context Gardener → Structural Drafter
         → Socratic Critic (CCC Gate) → PASS/REVISE → Output
```

### Stage 1: Evidence Manager (Gemini 3 Pro)
Normalizes raw source data into `EvidenceItem_v1` objects with:
- SHA-256 hashes for versioning
- Source metadata (file, page, line)
- Multimodal anchor points (14 per image/document)

### Stage 2: Context Gardener (Gemini 3 Pro)
Ranks evidence by Signal-to-Noise ratio:
- Filters low-quality sources (threshold: 0.7)
- Prioritizes high-value evidence for synthesis
- Maintains complete provenance chain

### Stage 3: Structural Drafter
Generates narrative with mandatory trace maps:
- Creates `SentenceRow_v1` objects linking claims to evidence
- Builds `ClaimLedger_v1` registry of all assertions
- **MANDATE**: No claims without evidence pinpoints

### Stage 4: Socratic Critic (GPT-5.2)
Independent audit using Logic Inversion:
- Calculates CCC metric: `V / |U|` (valid claims / total claims)
- Executes Anti-Thesis Method to find contradictions
- **HARD GATE**: CCC < 0.95 → FAIL → trigger revision

### Stage 5: Revision Loop (if needed)
Automatic refinement (max 3 cycles):
- Receives specific guidance from Critic
- Re-generates narrative addressing issues
- Re-audits until CCC threshold met

## Configuration

All pipeline behavior is controlled via `scripts/config.yml`:

```yaml
# Adjust CCC threshold (default: 0.95 = 95% coverage)
socratic_critic:
  ccc_threshold: 0.95  # Stricter: 0.98, More lenient: 0.90
  temperature: 1.0     # Keep at 1.0 for logic diversity

# Control revision behavior
pipeline:
  max_revision_cycles: 3  # Increase if needed
  zero_hallucination_protocol: true  # Never disable

# Set model assignments
evidence_manager:
  model: gemini-3-pro  # 2M token context
  
socratic_critic:
  model: gpt-5.2       # External auditor
```

## The 6 Canonical Objects

All agents communicate via versioned JSON schemas. See `references/canonical-schemas.md` for complete specifications:

1. **EvidenceItem_v1**: Normalized source data with hashes
2. **SentenceRow_v1**: Claim-to-evidence trace map
3. **ClaimLedger_v1**: Registry of all factual assertions
4. **AuditReport_v1**: Critic's verification results with CCC metric
5. **ArchitectureLedger_v1**: Approved architectural decisions
6. **SpecDocument_v1**: Hash-verified specifications for code generation

## Key Concepts

### The CCC Metric (Claim-Citation Coverage)

```
CCC = V / |U|

where:
  V = claims with valid source:page:line pinpoints
  |U| = total factual assertions in draft
```

**Example:**
- Draft contains 20 factual claims
- 19 have valid citations with pinpoints
- 1 is unsupported
- CCC = 19/20 = 0.95 (exactly at threshold → PASS)

### Persona Isolation

Each agent uses a separate DSPy Signature to prevent "instruction neglect":
- Evidence Manager: Normalizer persona
- Structural Drafter: Producer persona  
- Socratic Critic: Logic Governor persona (external model)

This separation ensures the Critic independently validates without bias from the Drafter's reasoning process.

### Spec-First Protocol

The Sovereign Builder **cannot generate code** without:
1. An approved `spec.md` document
2. Matching `spec_hash` in the architecture ledger
3. Verified alignment with architectural decisions

This prevents "premature implementation" and ensures all code is traceable to approved requirements.

## Resources

### scripts/
- **signatures.py**: DSPy Signature definitions for all agents
- **pipeline.py**: Complete pipeline orchestration with CCC enforcement
- **config.yml**: Pipeline configuration (models, thresholds, behavior)

### references/
- **canonical-schemas.md**: JSON schema definitions for the 6 Canonical Objects
- **architecture.md**: Detailed pipeline architecture and design principles
- **example-usage.md**: Complete worked example with research paper verification

## Advanced Usage

### Custom CCC Threshold

For different use cases, adjust the threshold:

```python
# In config.yml
socratic_critic:
  ccc_threshold: 0.98  # Near-perfect citations (legal/medical)
  # or
  ccc_threshold: 0.90  # More lenient (exploratory research)
```

### Extending with Custom Agents

Add new agents by defining DSPy Signatures:

```python
import dspy

class CustomAgent(dspy.Signature):
    """Your agent role and instructions"""
    input_data = dspy.InputField(desc="...")
    output_data = dspy.OutputField(desc="...")

# Integrate into pipeline
custom_agent = dspy.ChainOfThought(CustomAgent)
result = custom_agent(input_data=your_data)
```

### Monitoring Pipeline Performance

```python
result = bridge.process_haystack(haystack)

print(f"Evidence items processed: {len(result['evidence'])}")
print(f"Claims generated: {len(result['draft']['claim_ledger']['claims'])}")
print(f"Revision cycles used: {result.get('revision_count', 0)}")
print(f"Final CCC: {result['audit_report']['ccc_metric']['ratio']:.2%}")
```

## Best Practices

1. **Provide Complete Sources**: Include page and line numbers in source documents for accurate pinpoints
2. **Start with Good Evidence**: Higher quality input = fewer revision cycles
3. **Monitor CCC Trends**: Consistently low CCC suggests source quality issues
4. **Use Hash Verification**: Always validate spec_hash before code generation
5. **Review Audit Reports**: Check `revision_guidance` for insight into common issues

## Troubleshooting

**CCC keeps failing (<0.95):**
- Verify source documents include page/line numbers
- Check evidence quality scores from Context Gardener
- Increase `max_revision_cycles` if progress is being made

**Evidence Manager missing sources:**
- Ensure source references are clearly formatted
- Add explicit document boundaries in haystack
- Check multimodal anchor detection for images/PDFs

**Spec-First Protocol blocking code generation:**
- Verify `spec_hash` calculation matches exactly
- Check architecture ledger contains the approved spec hash
- Ensure spec.md hasn't been modified after approval

For detailed examples, see `references/example-usage.md`.
