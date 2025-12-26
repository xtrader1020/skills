---
name: contract-review
description: Comprehensive contract review and analysis tool for legal teams. Extracts key terms, identifies risks, checks compliance with standard provisions, and generates detailed review reports. Use when reviewing contracts, agreements, or legal documents to identify potential issues, missing clauses, unfavorable terms, or compliance gaps.
metadata:
  short-description: Review contracts and identify risks
---

# Contract Review

Comprehensive contract analysis tool that extracts key terms, identifies risks, and generates detailed review reports.

## Quick Start

```bash
# Review a contract file
python scripts/extract_contract.py <contract.pdf>

# Generate review report
python scripts/extract_contract.py <contract.pdf> --report
```

## Features

1. **Key Term Extraction**: Automatically identifies and extracts:
   - Parties and their roles
   - Effective dates and term lengths
   - Payment terms and amounts
   - Termination clauses
   - Liability limitations
   - Indemnification provisions
   - Governing law and jurisdiction
   - Confidentiality obligations
   - IP ownership and licensing terms

2. **Risk Identification**: Flags potential issues:
   - One-sided or unfavorable terms
   - Missing standard provisions
   - Unusual liability exposure
   - Ambiguous language
   - Conflicting clauses
   - Compliance gaps

3. **Compliance Checking**: Verifies against standard requirements:
   - Industry-standard terms
   - Jurisdiction-specific requirements
   - Company policy compliance
   - Regulatory requirements

## Workflow

### 1) Extract Contract Content

```bash
python scripts/extract_contract.py <contract.pdf> --output <output.json>
```

This parses the document and extracts structured data in JSON format.

Supported formats:
- PDF (.pdf)
- Word documents (.docx)
- Plain text (.txt)

### 2) Analyze Key Terms

Review the extracted terms section by section:
- **Parties**: Verify correct legal entity names and addresses
- **Term**: Check duration, renewal terms, and termination conditions
- **Payment**: Review amounts, schedules, payment terms, late fees
- **Scope**: Verify deliverables, services, or products clearly defined
- **Warranties**: Check representations, warranties, and disclaimers
- **Liability**: Review limitation of liability and indemnification clauses
- **IP**: Verify intellectual property ownership and license grants
- **Confidentiality**: Check NDA provisions and confidentiality obligations
- **Dispute Resolution**: Review arbitration, mediation, and jurisdiction clauses

### 3) Identify Risks

The script automatically flags:
- **High risk**: Unlimited liability, broad indemnification, perpetual terms
- **Medium risk**: Unclear termination rights, missing force majeure, one-sided terms
- **Low risk**: Minor ambiguities, non-standard but acceptable terms

### 4) Generate Review Report

```bash
python scripts/extract_contract.py <contract.pdf> --report --output review_report.md
```

Generates a comprehensive Markdown report with:
- Executive summary
- Key terms table
- Risk assessment with severity ratings
- Recommendations for negotiation
- Missing provisions checklist
- Comparison to standard terms

### 5) Apply Jurisdiction Rules

The skill includes jurisdiction-specific guidance in `references/`:
- `us-contract-law.md` - US contract law principles
- `eu-contract-law.md` - EU contract considerations
- `uk-contract-law.md` - UK contract requirements

Load the relevant reference file when reviewing contracts for specific jurisdictions.

## Risk Categories

**High Risk** (requires immediate attention):
- Unlimited liability exposure
- Unilateral termination rights (favoring counterparty)
- Broad indemnification without caps
- Automatic renewal without notice period
- Exclusive rights without time limits
- Waiver of consequential damages (one-sided)
- Assignment rights without consent
- Perpetual confidentiality obligations

**Medium Risk** (negotiate if possible):
- Missing limitation of liability clause
- Unclear scope of work or deliverables
- Ambiguous payment terms or milestones
- One-sided warranties
- Missing force majeure provision
- Short notice periods for termination
- Non-compete clauses

**Low Risk** (monitor but acceptable):
- Minor ambiguities in definitions
- Non-standard but reasonable terms
- Boilerplate variations
- Style and formatting issues

## Common Missing Provisions

Standard clauses to check for:
- [ ] Force majeure
- [ ] Limitation of liability
- [ ] Indemnification (mutual)
- [ ] Confidentiality
- [ ] IP ownership and licenses
- [ ] Warranties and disclaimers
- [ ] Termination rights
- [ ] Notice provisions
- [ ] Governing law
- [ ] Dispute resolution
- [ ] Assignment and subcontracting
- [ ] Severability
- [ ] Entire agreement
- [ ] Amendment procedures

## References

See `references/` directory for jurisdiction-specific guidance:
- `us-contract-law.md` - US contract law principles and common terms
- Standard provision templates and examples
- Industry-specific considerations

## Example Usage

**Example 1: Review NDA**
```bash
python scripts/extract_contract.py client-nda.pdf --report
```

Output:
- Identifies parties and scope
- Checks for mutual vs. one-way obligations
- Reviews term and survival clauses
- Flags unlimited duration if present
- Verifies exceptions (public information, prior knowledge, etc.)

**Example 2: Review MSA**
```bash
python scripts/extract_contract.py vendor-msa.pdf --report --jurisdiction us
```

Output:
- Extracts payment terms and SOW process
- Reviews liability limitations and caps
- Checks indemnification provisions
- Identifies IP ownership terms
- Flags missing provisions

## Tips

- Always review the full contract text, not just the extracted summary
- Pay special attention to definitions section - it affects interpretation throughout
- Check for conflicts between different sections
- Verify all defined terms are actually defined
- Look for hand-written amendments or addendums
- Note any exhibits or schedules that may be missing
- Consider the business context and risk tolerance
- When in doubt, escalate to legal counsel

## Integration

This skill works with:
- Document management systems (for retrieving contracts)
- Notion or other knowledge bases (for storing reviews)
- Redlining tools (for proposing changes)
- Signature platforms (for tracking execution)
