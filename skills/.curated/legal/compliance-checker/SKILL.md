---
name: compliance-checker
description: Comprehensive regulatory compliance checking tool for GDPR, CCPA, HIPAA, SOX, and PCI-DSS. Analyzes policies, practices, and systems against regulatory requirements and generates compliance reports with gap analysis. Use when verifying compliance with data protection, privacy, security, or financial regulations.
metadata:
  short-description: Check regulatory compliance
---

# Compliance Checker

Automated compliance checking tool for major regulatory frameworks including GDPR, CCPA, HIPAA, SOX, and PCI-DSS.

## Quick Start

```bash
# Check GDPR compliance
python scripts/compliance_check.py --regulation gdpr --policy privacy-policy.md

# Check multiple regulations
python scripts/compliance_check.py --regulation gdpr,ccpa --policy privacy-policy.md --practices practices.md

# Generate detailed report
python scripts/compliance_check.py --regulation hipaa --policy hipaa-policy.md --report compliance-report.md
```

## Supported Regulations

### GDPR (General Data Protection Regulation)
- EU data protection law
- Applies to: EU residents' data, regardless of company location
- Key requirements: Consent, data minimization, right to erasure, breach notification
- Reference: `references/gdpr-checklist.md`

### CCPA (California Consumer Privacy Act)
- California privacy law
- Applies to: California residents' data for qualifying businesses
- Key requirements: Notice, opt-out, access rights, non-discrimination
- Reference: `references/ccpa-checklist.md`

### HIPAA (Health Insurance Portability and Accountability Act)
- US healthcare data protection law
- Applies to: Protected Health Information (PHI) handled by covered entities and business associates
- Key requirements: Privacy rule, security rule, breach notification
- Reference: `references/hipaa-checklist.md`

### SOX (Sarbanes-Oxley Act)
- US financial reporting law
- Applies to: Public companies and their accounting firms
- Key requirements: Internal controls, financial accuracy, audit trails
- Note: SOX compliance typically requires specialized financial/audit expertise

### PCI-DSS (Payment Card Industry Data Security Standard)
- Payment card data security standard
- Applies to: Organizations that store, process, or transmit cardholder data
- Key requirements: Secure network, protect cardholder data, access controls, monitoring
- Note: Full PCI-DSS compliance requires technical security assessments

## Workflow

### 1) Select Regulation(s)

Determine which regulations apply based on:
- **Geography**: Where are your customers/users located?
- **Industry**: Healthcare (HIPAA), Finance (SOX), Payments (PCI-DSS)
- **Data Types**: Personal data (GDPR/CCPA), health data (HIPAA), payment data (PCI-DSS)
- **Company Type**: Public company (SOX), business size and revenue (CCPA thresholds)

### 2) Gather Documentation

Collect relevant documents:
- Privacy policies and terms of service
- Data handling procedures and practices
- Security policies and controls
- Consent mechanisms and forms
- Data processing agreements
- Incident response plans
- Training materials

### 3) Run Compliance Check

```bash
python scripts/compliance_check.py \
  --regulation gdpr \
  --policy privacy-policy.md \
  --practices data-practices.md \
  --security security-policy.md \
  --report output-report.md
```

The script analyzes documents against the regulation's requirements and generates:
- Compliance score (percentage)
- Compliant items (✓)
- Non-compliant items (✗)
- Partially compliant items (⚠)
- Gap analysis with recommendations

### 4) Review Results

Review the compliance report sections:
- **Executive Summary**: Overall compliance score and key findings
- **Requirement Analysis**: Item-by-item compliance status
- **Gap Analysis**: Missing or inadequate controls
- **Recommendations**: Specific actions to address gaps
- **Priority Matrix**: High/medium/low priority items

### 5) Address Gaps

For each non-compliant or partially compliant item:
1. Review the specific requirement in the reference checklist
2. Implement the necessary policy, procedure, or control
3. Document the implementation
4. Re-run compliance check to verify

### 6) Ongoing Monitoring

Compliance is continuous, not one-time:
- Schedule regular compliance reviews (quarterly/annually)
- Monitor for regulation updates and changes
- Track compliance metrics over time
- Conduct periodic audits
- Update policies as practices change

## Compliance Domains

### Privacy & Data Protection (GDPR, CCPA)

**Key Areas**:
- **Transparency**: Clear privacy notices explaining data collection and use
- **Consent**: Valid, informed, freely given consent for processing
- **Rights**: Mechanisms for access, deletion, portability, correction
- **Purpose Limitation**: Use data only for stated purposes
- **Data Minimization**: Collect only necessary data
- **Security**: Appropriate technical and organizational measures
- **Breach Notification**: Procedures for detecting and reporting breaches
- **Transfers**: Safeguards for international data transfers
- **DPO/Privacy Officer**: Designated privacy leadership (GDPR)
- **Records**: Documentation of processing activities

**Common Gaps**:
- Vague privacy policies
- No consent for non-essential cookies
- No deletion mechanism
- Inadequate data security
- No breach response plan
- Third-party vendors not assessed

### Healthcare (HIPAA)

**Key Areas**:
- **Privacy Rule**: Patient rights, notice, consent, minimum necessary
- **Security Rule**: Administrative, physical, technical safeguards
- **Breach Notification**: Timely notification of breaches
- **Business Associates**: Contracts with vendors handling PHI
- **Access Controls**: Role-based access, unique user IDs
- **Audit Trails**: Logging and monitoring of PHI access
- **Training**: Workforce training on HIPAA requirements
- **Policies**: Written privacy and security policies
- **Risk Analysis**: Regular security risk assessments

**Common Gaps**:
- Missing Business Associate Agreements (BAAs)
- No risk assessment conducted
- Inadequate access controls
- No audit logging
- Staff not trained
- Weak encryption

### Payment Security (PCI-DSS)

**Key Areas**:
- **Build & Maintain**: Secure network and systems
- **Protect**: Cardholder data encrypted and secured
- **Vulnerability Management**: Antivirus, secure systems, patching
- **Access Control**: Restrict access on need-to-know basis
- **Monitor & Test**: Track access, test security regularly
- **Information Security**: Maintain security policies

**Common Gaps**:
- Storing cardholder data unnecessarily
- Weak encryption or no encryption
- Default passwords not changed
- No network segmentation
- Security not regularly tested
- No incident response plan

## Automation Limitations

**What This Tool Can Do**:
- Check for presence of required policy elements
- Identify missing documentation
- Compare practices against regulatory checklists
- Generate gap analysis reports
- Prioritize compliance efforts

**What This Tool Cannot Do**:
- Verify actual implementation (policies vs. practice)
- Assess technical controls in production systems
- Determine legal interpretation of ambiguous regulations
- Replace qualified compliance professionals
- Provide legal advice or opinions

**Always Recommended**:
- Have policies reviewed by qualified legal counsel
- Conduct technical security assessments
- Engage compliance consultants for complex regulations
- Perform regular audits by independent assessors
- Obtain certifications where required (e.g., PCI-DSS AOC)

## References

Detailed requirement checklists for each regulation:

- `references/gdpr-checklist.md` - GDPR requirements and guidance
- `references/ccpa-checklist.md` - CCPA requirements and guidance  
- `references/hipaa-checklist.md` - HIPAA requirements and guidance

These references provide:
- Complete requirement lists
- Explanation of each requirement
- Examples of compliant implementations
- Common pitfalls and mistakes
- Links to official guidance and resources

## Integration

This skill works with:
- **Document management**: For storing policies and procedures
- **Notion**: For tracking compliance tasks and status
- **Ticketing systems**: For managing remediation work
- **Audit tools**: For technical compliance validation
- **Training platforms**: For required compliance training

## Best Practices

1. **Compliance is Ongoing**: Not a one-time checkbox
2. **Document Everything**: Policies, procedures, decisions, assessments
3. **Regular Reviews**: Schedule periodic compliance reviews
4. **Training**: Ensure workforce understands requirements
5. **Vendor Management**: Assess third-party compliance
6. **Incident Preparedness**: Have breach/incident response plans ready
7. **Stay Updated**: Regulations evolve; monitor for changes
8. **Privacy by Design**: Build compliance into products and processes
9. **Cross-Functional**: Involve legal, security, engineering, and business teams
10. **Professional Help**: Engage experts for complex compliance needs

## Example Usage

**Example 1: GDPR Privacy Policy Check**
```bash
python scripts/compliance_check.py --regulation gdpr --policy privacy-policy.md
```
Output:
- Checks for required GDPR elements (legal basis, rights, DPO, transfers)
- Identifies missing data subject rights
- Flags vague language that needs clarification
- Generates recommendations for improvement

**Example 2: HIPAA Security Assessment**
```bash
python scripts/compliance_check.py --regulation hipaa --security security-policy.md --practices practices.md
```
Output:
- Verifies administrative, physical, and technical safeguards
- Checks for required policies (access control, audit, breach notification)
- Identifies missing Business Associate Agreements
- Recommends encryption and access controls

**Example 3: Multi-Regulation Check**
```bash
python scripts/compliance_check.py --regulation gdpr,ccpa,hipaa --policy all-policies.md --report full-compliance.md
```
Output:
- Comprehensive analysis across multiple frameworks
- Identifies overlapping requirements
- Prioritizes gaps by severity
- Generates unified action plan
