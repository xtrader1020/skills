---
name: legal-skill-factory
description: Meta-skill that detects when a legal task is requested but no skill exists, then creates and installs new legal skills on-demand. Use when a legal domain request (contracts, compliance, litigation, IP, corporate, regulatory) is made and no appropriate skill is found. Supports domains like contract review, NDA generation, compliance checking, redlining, and legal analysis.
metadata:
  short-description: Create legal skills on-demand
---

# Legal Skill Factory

Meta-skill that enables self-service legal skill creation. Detects missing legal capabilities and creates new skills automatically.

## When to Use

Use this skill when:
- A legal task is requested (contract review, compliance check, NDA drafting, etc.)
- No existing skill matches the request
- The task follows a legal domain pattern (contracts, compliance, litigation, IP, corporate, regulatory)

## Workflow

### 1) Detect Legal Capability Gap

Run `scripts/detect_capability.py` to analyze the user's request:

```bash
python scripts/detect_capability.py "<user request>"
```

This parses the request into components:
- **Domain**: contract, compliance, litigation, IP, corporate, regulatory
- **Action**: review, draft, redline, analyze, compare, summarize, check, validate, generate, extract
- **Subject**: nda, msa, employment-agreement, gdpr, ccpa, patent, etc.
- **Jurisdiction**: us, eu, uk, ca, etc. (optional)

### 2) Check Existing Skills

The script searches for matching skills in:
- `~/.codex/legal-skill-registry.json` (tracked legal skills)
- `skills/.curated/legal/` (curated legal skills)
- User's installed skills

If a match is found, suggest using the existing skill.

### 3) Gather Requirements

If no skill exists, ask the user:
- What is the exact legal task? (be specific)
- What jurisdiction(s) should be supported? (US, EU, UK, etc.)
- What input format? (PDF, DOCX, plain text, etc.)
- What output is expected? (report, redlined document, checklist, etc.)
- Are there specific regulations or standards to follow?
- Do they have templates or reference materials to include?

### 4) Create the Skill

Use the existing `$skill-creator` skill to create the new legal skill:

1. Generate skill name following convention: `legal-[action]-[subject]-[jurisdiction]`
   - Examples: `legal-review-nda-us`, `legal-draft-msa-eu`, `legal-check-gdpr-compliance`

2. Plan the skill structure:
   - **scripts/**: For parsing documents, checking compliance, generating reports
   - **references/**: For jurisdiction-specific rules, regulation checklists, legal standards
   - **assets/templates/**: For document templates (contracts, agreements, checklists)

3. Create the skill using `$skill-creator` with gathered requirements

### 5) Auto-Install and Execute

After creating the skill:

1. Register it in `~/.codex/legal-skill-registry.json`:
   ```bash
   python scripts/skill_registry.py register <skill-name> --domain <domain> --action <action> --subject <subject>
   ```

2. Install the skill using `$skill-installer`

3. Execute the new skill on the user's original request

### 6) Offer to Save

After successful execution, ask the user:
- "This skill worked well. Would you like to save it for future use?"
- If yes, commit it to their private legal-skills repository or the public curated collection

## Skill Naming Convention

All legal skills MUST follow: `legal-[action]-[subject]-[jurisdiction]`

**Actions**: review, draft, redline, analyze, compare, summarize, check, validate, generate, extract

**Examples**:
- `legal-review-nda-us` - Review NDAs under US law
- `legal-draft-msa-eu` - Draft Master Service Agreements for EU
- `legal-check-gdpr-compliance` - Check GDPR compliance
- `legal-redline-employment-uk` - Redline employment agreements for UK
- `legal-analyze-patent-us` - Analyze patents under US law

## Registry Management

The skill maintains a registry at `~/.codex/legal-skill-registry.json` tracking:
- Skill name and location
- Domain, action, subject, jurisdiction
- Usage count and success rate
- Last used timestamp

Commands:
```bash
# Register a new skill
python scripts/skill_registry.py register <skill-name> --domain contract --action review --subject nda

# Find matching skills
python scripts/skill_registry.py find --domain contract --action review

# List all legal skills
python scripts/skill_registry.py list

# Update usage stats
python scripts/skill_registry.py use <skill-name>
```

## Integration with Existing Skills

This meta-skill works seamlessly with:
- **skill-creator**: For creating new skills with proper structure
- **skill-installer**: For installing skills into Codex
- **Private repositories**: For confidential legal templates and firm-specific knowledge

## Progressive Disclosure

1. Use `scripts/detect_capability.py` first - it's fast and requires minimal context
2. Only load full skill creation workflow if no match is found
3. Registry lookup is O(1) for common legal tasks
4. Create skills only when truly needed

## Examples

**Example 1: NDA Review Request**
```
User: "Can you review this NDA for red flags?"
→ detect_capability.py finds no exact match
→ Suggests creating: legal-review-nda-us
→ Gathers requirements: jurisdiction, risk areas to check
→ Creates skill with contract extraction + risk analysis scripts
→ Installs and executes immediately
→ Registers for future use
```

**Example 2: GDPR Compliance Check**
```
User: "Check if our privacy policy is GDPR compliant"
→ detect_capability.py identifies: domain=compliance, action=check, subject=gdpr
→ Finds existing: legal-check-gdpr-compliance (in curated/legal/)
→ Uses existing skill instead of creating new one
```

## Best Practices

1. **Reuse over recreation**: Always check registry first
2. **Specific over general**: Create targeted skills (legal-review-nda-us) rather than broad ones (legal-review-contract)
3. **Include references**: Legal skills should bundle jurisdiction-specific rules
4. **Test thoroughly**: Legal work requires high accuracy
5. **Version control**: Track skill iterations for compliance and audit
6. **Privacy-aware**: Support both public and private skill repositories

## Notes

- Legal skills are especially valuable because legal knowledge is:
  - Jurisdiction-specific (US law ≠ EU law)
  - Format-specific (NDAs ≠ MSAs ≠ Employment Agreements)
  - Regulation-specific (GDPR ≠ CCPA ≠ HIPAA)
  
- The factory pattern prevents recreating similar legal workflows repeatedly

- Skills can be shared within legal teams while keeping client-specific templates private
