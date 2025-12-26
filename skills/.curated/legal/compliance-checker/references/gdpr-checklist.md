# GDPR Compliance Checklist

## Overview

The General Data Protection Regulation (GDPR) is the EU's comprehensive data protection law that came into effect on May 25, 2018.

**Applies to**: Any organization that processes personal data of EU residents, regardless of where the organization is located.

**Key Concepts**:
- **Personal Data**: Any information relating to an identified or identifiable natural person
- **Processing**: Any operation performed on personal data (collection, storage, use, disclosure, etc.)
- **Data Controller**: Entity that determines the purposes and means of processing
- **Data Processor**: Entity that processes data on behalf of the controller
- **Data Subject**: The individual whose personal data is being processed

## Core Requirements

### 1. Lawful Basis for Processing

**Requirement**: You must have a valid lawful basis for processing personal data.

**Lawful Bases** (at least one required):
- ✓ **Consent**: Freely given, specific, informed, and unambiguous
- ✓ **Contract**: Necessary for contract performance
- ✓ **Legal Obligation**: Required by law
- ✓ **Vital Interests**: To protect someone's life
- ✓ **Public Task**: Performing a task in the public interest
- ✓ **Legitimate Interest**: Necessary for legitimate interests (with balancing test)

**What to Document**:
- Which lawful basis applies to each processing activity
- For consent: How and when consent was obtained
- For legitimate interest: Legitimate Interest Assessment (LIA)

**Common Mistakes**:
- Using consent when contract basis is more appropriate
- Failing to document the lawful basis
- Bundling consent with other terms (consent must be freely given)
- Pre-ticking consent boxes

### 2. Transparency

**Requirement**: Provide clear information to data subjects about data processing.

**Privacy Notice Must Include**:
- [ ] Identity and contact details of data controller
- [ ] Contact details of Data Protection Officer (if applicable)
- [ ] Purposes of processing
- [ ] Lawful basis for each purpose
- [ ] Categories of personal data collected
- [ ] Recipients or categories of recipients
- [ ] International transfers (if any) and safeguards
- [ ] Retention periods or criteria
- [ ] Data subject rights
- [ ] Right to withdraw consent (if consent is the basis)
- [ ] Right to lodge a complaint with supervisory authority
- [ ] Whether provision is statutory/contractual requirement
- [ ] Automated decision-making and profiling (if applicable)

**Best Practices**:
- Use clear, plain language (avoid legalese)
- Make privacy notice easily accessible
- Provide at point of data collection
- Update when processing changes
- Consider layered approach (short notice + full notice)

### 3. Data Subject Rights

**Requirement**: Enable data subjects to exercise their rights.

**Rights to Implement**:

**Right to Access (Article 15)**
- [ ] Provide copy of personal data being processed
- [ ] Provide information about processing (purposes, recipients, retention, etc.)
- [ ] Respond within 1 month (extendable to 3 months for complex requests)
- [ ] First copy is free; reasonable fee for additional copies

**Right to Rectification (Article 16)**
- [ ] Allow correction of inaccurate personal data
- [ ] Allow completion of incomplete data
- [ ] Respond within 1 month

**Right to Erasure / "Right to be Forgotten" (Article 17)**
- [ ] Delete data when requested if:
  - No longer necessary for original purpose
  - Consent withdrawn (and no other legal basis)
  - Data subject objects and no overriding legitimate grounds
  - Unlawfully processed
  - Legal obligation to delete
  - Data collected from child (in context of information society services)
- [ ] Exceptions: Legal obligation, public interest, legal claims, freedom of expression

**Right to Restrict Processing (Article 18)**
- [ ] Restrict processing (store but not use) when:
  - Accuracy is contested
  - Processing is unlawful but data subject opposes erasure
  - Data no longer needed but required for legal claims
  - Object to processing pending verification of legitimate grounds

**Right to Data Portability (Article 20)**
- [ ] Provide data in structured, commonly used, machine-readable format
- [ ] Allow transmission to another controller
- [ ] Applies only to data provided by data subject, processed by automated means, on basis of consent or contract

**Right to Object (Article 21)**
- [ ] Stop processing when data subject objects, unless compelling legitimate grounds
- [ ] Always stop for direct marketing if objection made
- [ ] Inform about right to object at first communication (for direct marketing)

**Implementation Requirements**:
- [ ] Clear mechanism to submit requests (email, web form, etc.)
- [ ] Identity verification process
- [ ] Tracking system for requests
- [ ] Standard response templates
- [ ] Process documented in internal policies

### 4. Consent Management

**Requirement**: If using consent as lawful basis, obtain valid consent.

**Valid Consent Must Be**:
- [ ] **Freely Given**: Not conditional, no imbalance of power
- [ ] **Specific**: Separate consent for different purposes
- [ ] **Informed**: Clear information about processing
- [ ] **Unambiguous**: Clear affirmative action (not silence, pre-ticked boxes, or inactivity)

**Consent Requirements**:
- [ ] Request consent in clear, plain language
- [ ] Separate consent from other terms
- [ ] Provide granular options (different purposes)
- [ ] Make it easy to withdraw consent
- [ ] Document when and how consent was obtained
- [ ] Keep evidence of consent
- [ ] Review consent regularly (no specific time limit, but should be reasonable)

**Special Categories** (Sensitive Data):
- [ ] Explicit consent required for:
  - Health data
  - Racial or ethnic origin
  - Political opinions
  - Religious or philosophical beliefs
  - Trade union membership
  - Genetic data
  - Biometric data (for identification)
  - Sex life or sexual orientation

**Children's Data**:
- [ ] Parental consent required for information society services offered to children under 16 (or lower age set by member state, minimum 13)
- [ ] Age verification mechanism
- [ ] Reasonable efforts to verify parental responsibility

### 5. Data Protection by Design and Default

**Requirement**: Implement appropriate technical and organizational measures.

**By Design**:
- [ ] Consider data protection from the start of projects
- [ ] Minimize data collection (only what's necessary)
- [ ] Implement privacy-enhancing technologies
- [ ] Conduct Data Protection Impact Assessments (DPIAs) for high-risk processing

**By Default**:
- [ ] Only collect and process data necessary for specific purpose
- [ ] Limit access to personal data
- [ ] Limit storage period
- [ ] Default privacy settings should be most protective

**Technical Measures**:
- [ ] Encryption (in transit and at rest)
- [ ] Pseudonymization where possible
- [ ] Access controls and authentication
- [ ] Logging and monitoring
- [ ] Secure deletion capabilities
- [ ] Backup and recovery procedures

**Organizational Measures**:
- [ ] Staff training on data protection
- [ ] Privacy policies and procedures
- [ ] Data protection governance
- [ ] Vendor management and due diligence
- [ ] Incident response procedures

### 6. Data Protection Impact Assessment (DPIA)

**Requirement**: Conduct DPIA for processing likely to result in high risk.

**When Required**:
- [ ] Systematic and extensive profiling with significant effects
- [ ] Large-scale processing of special category data
- [ ] Systematic monitoring of publicly accessible areas (e.g., CCTV)
- [ ] Use of new technologies
- [ ] Processing that prevents data subjects from exercising rights

**DPIA Must Include**:
- [ ] Description of processing operations and purposes
- [ ] Assessment of necessity and proportionality
- [ ] Assessment of risks to rights and freedoms
- [ ] Measures to address risks
- [ ] Safeguards, security measures, and mechanisms

**Process**:
- [ ] Consult DPO (if appointed)
- [ ] Seek views of data subjects (where appropriate)
- [ ] Consult supervisory authority if high risk remains after mitigation

### 7. Data Breach Notification

**Requirement**: Notify authorities and individuals of personal data breaches.

**To Supervisory Authority**:
- [ ] Notify within **72 hours** of becoming aware
- [ ] Include:
  - Nature of breach
  - Categories and approximate number of data subjects affected
  - Categories and approximate number of records affected
  - Contact details of DPO or other contact point
  - Likely consequences
  - Measures taken or proposed to address breach and mitigate effects
- [ ] If not notified within 72 hours, provide reasons for delay

**To Data Subjects**:
- [ ] Notify without undue delay if breach likely to result in high risk to rights and freedoms
- [ ] Use clear and plain language
- [ ] Describe nature of breach and likely consequences
- [ ] Provide contact details of DPO or other contact point
- [ ] Describe measures taken or proposed

**Exceptions to Individual Notification**:
- Appropriate technical and organizational protection measures applied (e.g., encryption)
- Subsequent measures ensure high risk is no longer likely
- Would involve disproportionate effort (public communication may suffice)

**Documentation**:
- [ ] Maintain record of all breaches (even if not required to notify)
- [ ] Document facts, effects, and remedial actions

### 8. International Data Transfers

**Requirement**: Ensure adequate protection when transferring data outside EU/EEA.

**Transfer Mechanisms**:
- [ ] **Adequacy Decision**: Transfer to countries with adequate protection (e.g., UK, Japan, Israel)
- [ ] **Standard Contractual Clauses (SCCs)**: Use EU-approved contract clauses
- [ ] **Binding Corporate Rules (BCRs)**: Internal rules for multinational groups
- [ ] **Derogations**: Specific situations (consent, contract necessity, legal claims, etc.)

**Post-Schrems II Requirements**:
- [ ] Assess laws in destination country
- [ ] Conduct Transfer Impact Assessment (TIA)
- [ ] Implement supplementary measures if needed (e.g., encryption, pseudonymization)
- [ ] Document assessment

**What to Document**:
- [ ] List of countries where data is transferred
- [ ] Transfer mechanism used for each
- [ ] Copies of SCCs or other agreements
- [ ] Transfer Impact Assessments

### 9. Records of Processing Activities

**Requirement**: Maintain records of processing activities (unless organization has < 250 employees and processing is low risk).

**Controller Records Must Include**:
- [ ] Name and contact details of controller and DPO
- [ ] Purposes of processing
- [ ] Categories of data subjects
- [ ] Categories of personal data
- [ ] Categories of recipients
- [ ] International transfers and safeguards
- [ ] Retention periods
- [ ] Security measures

**Processor Records Must Include**:
- [ ] Name and contact details of processor and DPO
- [ ] Name and contact details of each controller
- [ ] Categories of processing
- [ ] International transfers and safeguards
- [ ] Security measures

### 10. Data Protection Officer (DPO)

**Requirement**: Appoint DPO if:
- You are a public authority
- Core activities require regular and systematic monitoring of data subjects on a large scale
- Core activities consist of large-scale processing of special category data or data relating to criminal convictions

**DPO Requirements**:
- [ ] Appointed based on professional qualities and data protection expertise
- [ ] Reports to highest management level
- [ ] Independent (no conflict of interest)
- [ ] Provided adequate resources
- [ ] Contact details published and communicated to supervisory authority

**DPO Tasks**:
- [ ] Inform and advise on GDPR obligations
- [ ] Monitor compliance
- [ ] Provide advice on DPIAs
- [ ] Cooperate with supervisory authority
- [ ] Act as contact point for supervisory authority and data subjects

### 11. Vendor Management / Data Processors

**Requirement**: Only use processors that provide sufficient guarantees.

**Data Processing Agreement (DPA) Must Include**:
- [ ] Subject matter and duration of processing
- [ ] Nature and purpose of processing
- [ ] Type of personal data
- [ ] Categories of data subjects
- [ ] Obligations and rights of controller
- [ ] Processor obligations:
  - Only process on documented instructions
  - Ensure confidentiality of processing staff
  - Implement appropriate security measures
  - Respect conditions for sub-processors
  - Assist with data subject rights
  - Assist with security and breach obligations
  - Delete or return data after end of services
  - Make available information to demonstrate compliance
  - Allow and contribute to audits

**Sub-Processors**:
- [ ] General or specific written authorization required
- [ ] Notify controller of intended changes
- [ ] Same obligations flow down to sub-processors

### 12. Accountability

**Requirement**: Demonstrate compliance with GDPR.

**Documentation to Maintain**:
- [ ] Records of processing activities
- [ ] Data protection policies
- [ ] Privacy impact assessments
- [ ] Consent records
- [ ] Data subject rights requests and responses
- [ ] Data breach logs
- [ ] Training records
- [ ] Vendor due diligence
- [ ] Data protection agreements
- [ ] Audit logs

## Penalties

**Maximum Fines**:
- **Up to €20 million or 4% of global annual turnover** (whichever is higher) for:
  - Violations of basic principles
  - Data subject rights
  - International transfers
  - Compliance with supervisory authority orders

- **Up to €10 million or 2% of global annual turnover** for:
  - Processor obligations
  - Certification body requirements
  - Monitoring body requirements

**Note**: Fines are discretionary; authorities consider various factors including nature/severity of infringement, intent, mitigating measures, and cooperation.

## Quick Checklist

**Foundation**:
- [ ] Documented lawful basis for each processing activity
- [ ] Privacy notice published and accessible
- [ ] Mechanism to handle data subject rights requests
- [ ] Records of processing activities maintained

**Security**:
- [ ] Appropriate technical and organizational measures
- [ ] Staff trained on data protection
- [ ] Data breach notification procedures
- [ ] Vendor management and due diligence

**Governance**:
- [ ] DPO appointed (if required)
- [ ] Policies and procedures documented
- [ ] Regular compliance reviews
- [ ] Accountability documentation

**Special Situations**:
- [ ] Valid consent mechanism (if using consent)
- [ ] DPIA for high-risk processing
- [ ] International transfer safeguards
- [ ] Special category data protections

## Resources

- **Official Guidance**: https://edpb.europa.eu/
- **GDPR Text**: https://gdpr-info.eu/
- **ICO Guide** (UK): https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/
- **CNIL Guide** (France): https://www.cnil.fr/en/home
