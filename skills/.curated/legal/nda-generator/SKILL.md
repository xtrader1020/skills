---
name: nda-generator
description: Generate customized Non-Disclosure Agreements (NDAs) for various business scenarios. Supports mutual, one-way, employee, and vendor NDAs with jurisdiction-specific terms. Use when creating NDAs for protecting confidential information in business relationships, employment, vendor engagements, or partnerships.
metadata:
  short-description: Generate customized NDAs
---

# NDA Generator

Generate professional, customized Non-Disclosure Agreements (NDAs) tailored to your specific business needs.

## Quick Start

Choose the appropriate NDA template based on your scenario:

1. **Mutual NDA**: Both parties exchange confidential information
   - Use for: partnerships, joint ventures, business discussions
   - Template: `assets/templates/mutual-nda-template.md`

2. **One-Way NDA**: Only one party discloses confidential information
   - Use for: vendor engagements, consultant relationships, investor pitches
   - Template: `assets/templates/one-way-nda-template.md`

3. **Employee NDA**: For employee confidentiality obligations
   - Use for: employment relationships, protecting trade secrets
   - Template: `assets/templates/employee-nda-template.md`

4. **Vendor NDA**: For third-party service providers
   - Use for: outsourcing, supplier relationships, contractors
   - Template: `assets/templates/vendor-nda-template.md`

## Workflow

### 1) Determine NDA Type

Ask the user:
- Who are the parties? (individuals, companies)
- Who will disclose confidential information? (one or both parties)
- What is the business relationship? (partner, employee, vendor, investor)
- What jurisdiction governs? (US, EU, UK, etc.)

Based on answers, select the appropriate template.

### 2) Gather Key Information

Collect the following details:

**Parties**:
- Full legal names (individuals or company names)
- Business addresses
- Signing authorities (names and titles)

**Confidential Information**:
- What type of information will be shared? (technical, financial, business, customer data)
- Any specific categories to highlight?
- Are there any carve-outs or non-confidential items?

**Term**:
- How long should confidentiality obligations last? (2-5 years typical)
- Should obligations survive termination of the business relationship?

**Specific Provisions**:
- Return/destruction of materials clause?
- Non-solicitation of employees?
- Non-compete provisions? (may not be enforceable in all jurisdictions)
- Injunctive relief provision?

**Jurisdiction**:
- Governing law (state/country)
- Dispute resolution (arbitration, mediation, litigation)
- Venue (which courts have jurisdiction)

### 3) Customize the Template

Load the appropriate template from `assets/templates/` and customize:

1. Fill in party names and addresses
2. Define "Confidential Information" specifically for the relationship
3. Set the term duration
4. Adjust permitted uses and exceptions
5. Configure jurisdiction-specific terms (see `references/nda-standard-terms.md`)
6. Add any special provisions requested

### 4) Apply Jurisdiction Rules

Refer to `references/nda-standard-terms.md` for jurisdiction-specific guidance:
- **US**: State-by-state enforceability varies (especially non-competes)
- **EU**: GDPR considerations for personal data
- **UK**: Reasonableness standard for restrictive covenants
- **CA**: Non-compete clauses generally unenforceable

### 5) Generate and Review

1. Generate the complete NDA document
2. Review for:
   - Correct party names and addresses
   - Clear definition of confidential information
   - Appropriate exceptions (public information, prior knowledge, etc.)
   - Reasonable term duration
   - Proper jurisdiction and governing law
   - Signature blocks with correct titles

3. Provide the user with:
   - Complete NDA in requested format (Markdown, DOCX, PDF)
   - Summary of key terms
   - Explanation of any jurisdiction-specific provisions
   - Recommendation to have legal counsel review before signing

## Key NDA Components

### 1. Parties
Clearly identify:
- Disclosing Party: Who shares confidential information
- Receiving Party: Who receives confidential information
- For mutual NDAs: Both parties are disclosing and receiving

### 2. Definition of Confidential Information
Should include:
- What constitutes confidential information
- How it will be marked or identified
- Oral disclosures (how to confirm in writing)

Typical definition:
> "Confidential Information" means any information, technical data, or know-how, including, but not limited to, that which relates to research, products, services, customers, markets, software, developments, inventions, processes, designs, drawings, engineering, marketing, or finances.

### 3. Exceptions (Carve-Outs)
Standard exceptions for information that is:
- Publicly available (not through breach)
- Already known to receiving party
- Independently developed
- Rightfully received from third party
- Required to be disclosed by law

### 4. Obligations
Receiving party must:
- Keep information confidential
- Use only for permitted purposes
- Limit disclosure to need-to-know employees/contractors
- Protect with reasonable security measures
- Not reverse engineer (if applicable)

### 5. Term and Survival
- Agreement duration (e.g., 3 years from effective date)
- Confidentiality obligations survive termination (e.g., 5 years)
- Return/destruction obligations upon termination

### 6. Remedies
- Acknowledgment that breach causes irreparable harm
- Agreement that injunctive relief is appropriate
- Preservation of other legal remedies (damages)

### 7. General Provisions
- Governing law and jurisdiction
- No license or rights granted beyond specified uses
- No warranty as to accuracy of information
- Assignment restrictions
- Amendment procedures
- Entire agreement clause

## Common Mistakes to Avoid

❌ **Too Broad Definition**: "All information shared" is not specific enough
✅ **Specific**: Define categories relevant to the relationship

❌ **Perpetual Term**: Courts may not enforce indefinite terms
✅ **Reasonable Duration**: 2-5 years for most business relationships

❌ **No Exceptions**: Receiving party needs protection too
✅ **Standard Carve-Outs**: Include all five standard exceptions

❌ **Unclear Marking**: How to identify confidential oral information?
✅ **Written Confirmation**: Oral disclosures confirmed in writing within X days

❌ **Missing Jurisdiction**: Leaves enforcement uncertain
✅ **Clear Governing Law**: Specify state/country law

## Template Descriptions

### Mutual NDA
Use when both parties will exchange confidential information:
- Business partnerships
- Joint development projects
- Merger/acquisition discussions
- Strategic collaborations

**Key Features**:
- Balanced obligations
- Both parties are disclosing and receiving
- Mutual indemnification
- Reciprocal terms

### One-Way NDA
Use when only one party discloses information:
- Vendor evaluations
- Consultant engagements
- Investor presentations
- Customer pilots

**Key Features**:
- Single disclosing party
- Receiving party has all obligations
- Simpler structure
- Often shorter term

### Employee NDA
Use for employment relationships:
- New hires
- Promotions to sensitive roles
- Access to trade secrets
- Separation agreements

**Key Features**:
- Broader scope (all company information)
- Longer duration (often perpetual for trade secrets)
- Integrated with employment terms
- Return of materials on termination

**Important**: Check state law—some states (like California) restrict employee NDAs, especially for wage discussions and workplace conditions.

### Vendor NDA
Use for third-party service providers:
- Outsourcing partners
- Suppliers with access to sensitive data
- Contractors and consultants
- Technology vendors

**Key Features**:
- Covers vendor employees and subcontractors
- May include data protection/security requirements
- Return/destruction upon project completion
- Indemnification for vendor breaches

## Jurisdiction-Specific Notes

### United States
- Governed by state law (no federal NDA law)
- California: Very limited non-compete enforceability
- Enforceability varies by state for non-solicitation
- Trade secret protection available under state and federal law (DTSA)

### European Union
- GDPR applies to personal data in confidential information
- Must have lawful basis for processing personal data
- Cannot circumvent data subject rights with NDA
- Consider cross-border data transfer restrictions

### United Kingdom
- Reasonableness test for restrictive covenants
- Must protect legitimate business interests
- Cannot be broader than necessary
- Consider post-Brexit data adequacy

## Best Practices

1. **Be Specific**: Tailor the NDA to the specific relationship and information
2. **Reasonable Term**: 2-5 years for most business relationships; perpetual only for true trade secrets
3. **Mutual When Possible**: Balanced agreements are more likely to be enforced
4. **Include Standard Exceptions**: Protects both parties and is market standard
5. **Mark Confidential Materials**: Make it easy to identify protected information
6. **Limit Access**: Only share with those who need to know
7. **Document**: Keep records of what was shared and when
8. **Review Regularly**: Ensure NDA terms still match business relationship

## References

See `references/nda-standard-terms.md` for:
- Standard NDA clauses and language
- Jurisdiction-specific considerations
- Industry best practices
- Common negotiation points

## Integration

This skill works with:
- Document generation tools (for DOCX/PDF output)
- E-signature platforms (DocuSign, Adobe Sign)
- Contract management systems (for tracking)
- Legal knowledge bases (for storage and reuse)
