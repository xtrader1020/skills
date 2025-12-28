# Gemini Reasoning Bridge 2.0 - Quick Reference

## What is this?

A **zero-hallucination verification pipeline** that ensures every factual claim in generated content has a traceable citation to source materials with exact `source:page:line` pinpoints.

## Key Features

- **95% Citation Coverage Minimum**: Automatically enforced via the CCC Hard Gate
- **Independent Auditing**: Separate model (GPT-5.2) validates all claims
- **Automatic Revision**: Up to 3 cycles to fix citation issues
- **Spec-First Code Generation**: No code without hash-verified specifications
- **Complete Audit Trail**: SHA-256 hashes for all artifacts

## Pipeline Stages

```
1. Evidence Manager → Normalizes sources
2. Context Gardener → Ranks by quality  
3. Structural Drafter → Generates narrative with citations
4. Socratic Critic → Validates (CCC Hard Gate)
5. [If needed] → Revision loop back to step 3
```

## Quick Start

```python
from scripts.pipeline import ReasoningBridge

bridge = ReasoningBridge("scripts/config.yml")
result = bridge.process_haystack(your_research_data)

if result['status'] == 'PASS':
    print(f"✓ {result['audit_report']['ccc_metric']['ratio']:.0%} coverage")
```

## The CCC Formula

```
CCC = V / |U|

V  = Claims with valid pinpoints
|U| = Total factual assertions

PASS if CCC >= 0.95
FAIL if CCC < 0.95 → automatic revision
```

## Model Assignments

- **Evidence Manager**: Gemini 3 Pro (2M context, temp=0.3)
- **Context Gardener**: Gemini 3 Pro (temp=0.3)
- **Structural Drafter**: Gemini 3 Pro (temp=0.5)
- **Socratic Critic**: GPT-5.2 (temp=1.0 for diversity)
- **Sovereign Builder**: Qwen3-Next (temp=0.0 for deterministic code)

## Configuration

Edit `scripts/config.yml` to adjust:
- CCC threshold (default: 0.95)
- Max revision cycles (default: 3)
- Model assignments
- Temperature settings

## Important Files

- **SKILL.md**: Complete documentation and usage guide
- **scripts/signatures.py**: DSPy signature definitions
- **scripts/pipeline.py**: Pipeline orchestration
- **scripts/config.yml**: Configuration settings
- **references/canonical-schemas.md**: Schema definitions
- **references/architecture.md**: Architecture details
- **references/example-usage.md**: Complete worked example

## Common Use Cases

1. **Legal Research**: Verify all case citations are accurate
2. **Academic Papers**: Ensure every claim has source backing
3. **Compliance Docs**: Generate audit-ready documentation
4. **Research Validation**: Check existing documents for citation gaps
5. **Spec-to-Code**: Generate implementation from approved specs

## Key Principles

1. **Persona Isolation**: Each agent has separate prompts
2. **Schema-First**: All communication via versioned JSON
3. **Zero-Hallucination**: Enforce 95%+ citation coverage
4. **Independent Audit**: External model validates claims
5. **Hash Verification**: SHA-256 for all critical artifacts

## Troubleshooting

**CCC keeps failing?**
- Check source documents have page/line numbers
- Increase max_revision_cycles if making progress
- Review Context Gardener quality scores

**Missing citations?**
- Ensure sources are properly formatted in haystack
- Check evidence extraction in Stage 1 output

**Spec verification fails?**
- Verify spec_hash matches architecture ledger
- Ensure spec.md hasn't changed after approval
