# Example: Research Paper Verification

This example demonstrates using the Gemini Reasoning Bridge 2.0 to process a research paper and ensure all claims are properly cited.

## Scenario

You have a draft research paper with multiple claims. You want to verify that every factual assertion has a valid citation with source:page:line pinpoints.

## Input

```python
haystack = """
The impact of temperature settings on large language model outputs has been 
extensively studied. Recent research by Chen et al. (2024) demonstrated that 
temperature values between 0.7-1.0 produce more creative responses while 
maintaining coherence.

In a controlled experiment with 1,000 prompts, the study found:
- Temperature=0.0 produced identical outputs across runs (100% deterministic)
- Temperature=0.7 increased lexical diversity by 45% (p<0.001)
- Temperature=1.0 maximized variation but occasionally sacrificed coherence

The findings align with earlier work by Zhang et al. (2023), who reported 
similar patterns in GPT-3 experiments. However, their study noted that 
optimal temperature varies by task type.

For code generation tasks, deterministic behavior is preferred. As noted in
the OpenAI API documentation, "temperature=0 is recommended for code completion
to ensure reproducible results."
"""

# Evidence sources that should be linked
sources = [
    {
        "id": "chen2024",
        "file": "chen_et_al_2024.pdf",
        "title": "Temperature Effects in LLM Generation",
        "page_map": {
            "42": "temperature values between 0.7-1.0...",
            "43": "controlled experiment with 1,000 prompts...",
            "44": "Temperature=0.0 produced identical outputs...",
            "45": "Temperature=0.7 increased lexical diversity by 45%",
            "46": "Temperature=1.0 maximized variation..."
        }
    },
    {
        "id": "zhang2023", 
        "file": "zhang_et_al_2023.pdf",
        "title": "Task-Specific Temperature Tuning",
        "page_map": {
            "15": "similar patterns in GPT-3 experiments",
            "16": "optimal temperature varies by task type"
        }
    },
    {
        "id": "openai_docs",
        "file": "openai_api_docs.html",
        "title": "OpenAI API Reference",
        "page_map": {
            "1": "temperature=0 is recommended for code completion"
        }
    }
]
```

## Running the Pipeline

```python
from pipeline import ReasoningBridge
import json

# Initialize bridge
bridge = ReasoningBridge("config.yml")

# Prepare haystack with embedded source references
# In practice, Evidence Manager would extract these from actual documents
full_haystack = {
    "content": haystack,
    "sources": sources
}

# Run complete pipeline
result = bridge.process_haystack(json.dumps(full_haystack))

# Check results
print(f"Status: {result['status']}")
print(f"CCC Ratio: {result['audit_report']['ccc_metric']['ratio']:.2%}")

if result['status'] == 'PASS':
    print("\n✓ All claims properly cited!")
    print(f"  {result['audit_report']['ccc_metric']['V']} verified claims")
    print(f"  {result['audit_report']['ccc_metric']['U']} total factual assertions")
else:
    print("\n✗ Citation issues found:")
    for issue in result['audit_report']['revision_guidance']:
        print(f"  - {issue['issue']}")
```

## Expected Output

### Stage 1: Evidence Manager
```
Stage 1: Evidence Manager - Normalizing haystack...
[INFO] Found 3 source documents
[INFO] Extracted 8 evidence items
[INFO] Calculated text hashes for versioning
```

### Stage 2: Context Gardener
```
Stage 2: Context Gardener - Ranking evidence by signal-to-noise...
[INFO] Ranked 8 evidence items
[INFO] Average quality score: 0.92
[INFO] Filtered 0 low-quality items (threshold: 0.7)
```

### Stage 3: Structural Drafter
```
Stage 3: Structural Drafter - Generating narrative...
[INFO] Generated 7 sentences
[INFO] Created 12 claim-evidence mappings
[INFO] All factual claims have pinpoints: YES
```

### Stage 4: Socratic Critic
```
Stage 4: Socratic Critic - Executing Logic Inversion...
[INFO] Analyzing 12 factual claims
[INFO] Validating pinpoint accuracy...
[INFO] Checking for logical contradictions...

✓ CCC Gate PASSED: 100% >= 95%
  V = 12 (all factual claims have valid pinpoints)
  |U| = 12 (total factual assertions)
  Ratio = 1.00
```

## Detailed Audit Report

```json
{
  "audit_id": "550e8400-e29b-41d4-a716-446655440000",
  "audit_status": "PASS",
  "ccc_metric": {
    "V": 12,
    "U": 12,
    "ratio": 1.0,
    "threshold": 0.95
  },
  "logic_inversion_results": {
    "anti_thesis_checks": 12,
    "contradictions_found": 0,
    "unsupported_claims": []
  },
  "revision_required": false,
  "quality_summary": {
    "strong_claims": 12,
    "weak_claims": 0,
    "opinion_claims": 0
  }
}
```

## Example Sentence Trace Map

One sentence from the output with its complete trace:

```json
{
  "sentence_id": "sent-001",
  "sentence_text": "Temperature=0.7 increased lexical diversity by 45% (p<0.001)",
  "claim_type": "factual",
  "evidence_ids": ["evid-005"],
  "pinpoints": [
    {
      "evidence_id": "evid-005",
      "source": "chen_et_al_2024.pdf",
      "page": 45,
      "line": 12
    }
  ],
  "confidence_score": 0.98,
  "trace_hash": "a3f5e8c9..."
}
```

## Handling Failed Audits

If CCC < 0.95, the pipeline automatically triggers revision:

```
✗ CCC Gate FAILED: 83% < 95%
  V = 10 (claims with valid pinpoints)
  |U| = 12 (total factual assertions)
  Ratio = 0.83

Triggering revision cycle 1/3...
[INFO] Revision guidance:
  - Sentence sent-007: Missing source pinpoint for claim about GPT-3
  - Sentence sent-011: Needs page number for API documentation reference

Stage 3: Structural Drafter - Revising narrative...
[INFO] Added 2 missing pinpoints
[INFO] Updated claim ledger

Stage 4: Socratic Critic - Re-auditing...
✓ CCC Gate PASSED: 100% >= 95%
```

## Integration with Code Generation

After verifying research, use the Sovereign Builder:

```python
# Create approved spec
spec_md = """
# Implementation Spec: Temperature Controller

## Requirements
- Implement temperature parameter validation (Requirement R1, approved)
- Support range 0.0-2.0 with 0.1 precision (Requirement R2, approved)
- Default to 0.7 for creative tasks (based on Chen et al. 2024, p.42)
- Default to 0.0 for code generation (OpenAI best practice)

## Architecture
- TemperatureValidator class with range checks
- TaskType enum (Creative, Code, Analytical)
- get_optimal_temperature(task_type) -> float
"""

# Calculate spec hash and add to architecture ledger
import hashlib
spec_hash = hashlib.sha256(spec_md.encode('utf-8')).hexdigest()

architecture_ledger = {
    "ledger_id": "ledger-001",
    "active_spec": {
        "spec_id": "spec-temp-001",
        "spec_hash": spec_hash,
        "version": "1.0"
    },
    "decisions": [...]
}

# Generate code (only works if spec_hash matches)
code = bridge.generate_code(spec_md, architecture_ledger)
print(code)
```

## Tips for Best Results

1. **Provide Complete Sources**: Include all reference materials in the haystack
2. **Use Structured References**: Page numbers and line numbers improve pinpoint accuracy
3. **Set Appropriate Thresholds**: Default CCC=0.95 is strict; adjust in config if needed
4. **Monitor Revision Cycles**: If consistently hitting max revisions, improve source quality
5. **Validate Hashes**: Always verify spec_hash before code generation

## Common Issues

### Issue: CCC keeps failing
**Solution**: Check that sources include page and line numbers. Without these, pinpoints can't be validated.

### Issue: Evidence Manager missing sources
**Solution**: Ensure sources are properly formatted in the haystack with clear document boundaries.

### Issue: Spec-first protocol blocks code generation
**Solution**: Verify spec_hash matches the architecture ledger's active_spec.spec_hash exactly.
