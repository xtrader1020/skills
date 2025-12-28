#!/usr/bin/env python3
"""
Extract contract terms and identify risks from legal documents.

Supports PDF, DOCX, and plain text formats. Extracts key terms,
identifies potential risks, and generates review reports.

Usage:
    python extract_contract.py contract.pdf
    python extract_contract.py contract.pdf --report
    python extract_contract.py contract.pdf --output report.json
    python extract_contract.py contract.pdf --report --jurisdiction us
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


# Key terms to extract
KEY_TERMS = {
    "parties": [
        r"between\s+([A-Z][A-Za-z\s,\.]+?)(?:\s+and\s+|\s*\()",
        r"\"([A-Z][A-Za-z\s]+)\"\s*\(",
        r"party(?:ies)?[:\s]+([A-Z][A-Za-z\s,\.]+)",
    ],
    "effective_date": [
        r"effective\s+(?:as\s+of\s+)?(\w+\s+\d+,\s+\d{4})",
        r"dated\s+(?:as\s+of\s+)?(\w+\s+\d+,\s+\d{4})",
        r"date[:\s]+(\w+\s+\d+,\s+\d{4})",
    ],
    "term": [
        r"term[:\s]+(\d+)\s+(year|month|day)s?",
        r"period\s+of\s+(\d+)\s+(year|month|day)s?",
        r"for\s+a\s+period\s+of\s+(\d+)\s+(year|month|day)s?",
    ],
    "payment": [
        r"\$\s*[\d,]+(?:\.\d{2})?",
        r"(?:payment|fee|price|compensation)[:\s]+\$\s*[\d,]+(?:\.\d{2})?",
    ],
    "termination": [
        r"termin(?:ate|ation)",
        r"cancel(?:lation)?",
        r"notice\s+period",
    ],
    "liability": [
        r"liabilit(?:y|ies)",
        r"limitation\s+of\s+liability",
        r"indemnif(?:y|ication)",
    ],
    "governing_law": [
        r"governed\s+by\s+(?:the\s+)?laws?\s+of\s+([A-Za-z\s]+)",
        r"jurisdiction[:\s]+([A-Za-z\s]+)",
    ],
}

# Risk patterns
RISK_PATTERNS = {
    "high": {
        "unlimited_liability": [
            r"unlimited\s+liabilit",
            r"without\s+limit",
            r"no\s+cap\s+on\s+liabilit",
        ],
        "perpetual_term": [
            r"perpetual",
            r"indefinite\s+(?:term|period)",
            r"no\s+termination",
        ],
        "unilateral_termination": [
            r"(?:may|can|shall)\s+terminate.*without\s+cause",
            r"sole\s+discretion.*terminat",
        ],
        "broad_indemnification": [
            r"indemnif.*any\s+and\s+all",
            r"hold\s+harmless.*from\s+all",
        ],
    },
    "medium": {
        "missing_force_majeure": "force majeure",
        "missing_liability_cap": "limitation of liability",
        "ambiguous_scope": [
            r"such\s+services\s+as",
            r"reasonably\s+necessary",
            r"mutually\s+agreed",
        ],
        "short_notice": [
            r"(\d+)\s+days?\s+(?:prior\s+)?notice",
        ],
    },
    "low": {
        "ambiguous_definitions": [
            r"including\s+but\s+not\s+limited\s+to",
            r"such\s+as",
            r"and\s+other",
        ],
    },
}

# Standard provisions checklist
STANDARD_PROVISIONS = [
    "force majeure",
    "limitation of liability",
    "indemnification",
    "confidentiality",
    "intellectual property",
    "warranties",
    "termination",
    "notice",
    "governing law",
    "dispute resolution",
    "assignment",
    "severability",
    "entire agreement",
    "amendment",
]


def extract_text_from_file(file_path: Path) -> str:
    """Extract text from PDF, DOCX, or plain text file."""
    suffix = file_path.suffix.lower()
    
    if suffix == ".txt":
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif suffix == ".pdf":
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            print("Error: PyPDF2 is required for PDF processing. Install with: pip install PyPDF2", file=sys.stderr)
            print("Cannot process PDF files without PyPDF2.", file=sys.stderr)
            sys.exit(1)
    
    elif suffix == ".docx":
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            print("Error: python-docx is required for DOCX processing. Install with: pip install python-docx", file=sys.stderr)
            print("Cannot process DOCX files without python-docx.", file=sys.stderr)
            sys.exit(1)
    
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def extract_key_terms(text: str) -> Dict[str, List[str]]:
    """Extract key contractual terms from text."""
    results = {}
    
    for term, patterns in KEY_TERMS.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if found:
                # Flatten tuples from regex groups
                for match in found:
                    if isinstance(match, tuple):
                        matches.extend([m.strip() for m in match if m.strip()])
                    else:
                        matches.append(match.strip())
        
        # Deduplicate and clean
        results[term] = list(set(matches))[:5]  # Limit to top 5 matches
    
    return results


def identify_risks(text: str) -> Dict[str, List[Dict[str, str]]]:
    """Identify potential risks in the contract."""
    risks = {"high": [], "medium": [], "low": []}
    
    for severity, risk_types in RISK_PATTERNS.items():
        for risk_name, patterns in risk_types.items():
            if isinstance(patterns, str):
                patterns = [patterns]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Extract context around match
                    match_pos = text.lower().find(pattern.lower())
                    if match_pos >= 0:
                        start = max(0, match_pos - 100)
                        end = min(len(text), match_pos + 100)
                        context = text[start:end].replace('\n', ' ').strip()
                        
                        risks[severity].append({
                            "type": risk_name.replace('_', ' ').title(),
                            "pattern": pattern if isinstance(pattern, str) else pattern,
                            "context": context,
                        })
                    break  # Only report once per risk type
    
    return risks


def check_missing_provisions(text: str) -> List[str]:
    """Check for missing standard provisions."""
    missing = []
    text_lower = text.lower()
    
    for provision in STANDARD_PROVISIONS:
        # Check if provision is mentioned anywhere in text
        if provision.lower() not in text_lower:
            missing.append(provision)
    
    return missing


def generate_report(
    file_path: Path,
    text: str,
    key_terms: Dict,
    risks: Dict,
    missing_provisions: List[str],
    jurisdiction: Optional[str] = None
) -> str:
    """Generate a comprehensive review report in Markdown format."""
    report = []
    
    # Header
    report.append(f"# Contract Review Report")
    report.append(f"\n**File**: {file_path.name}")
    report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if jurisdiction:
        report.append(f"**Jurisdiction**: {jurisdiction.upper()}")
    report.append("\n---\n")
    
    # Executive Summary
    report.append("## Executive Summary\n")
    total_risks = sum(len(r) for r in risks.values())
    report.append(f"- **Total Risks Identified**: {total_risks}")
    report.append(f"  - High: {len(risks['high'])}")
    report.append(f"  - Medium: {len(risks['medium'])}")
    report.append(f"  - Low: {len(risks['low'])}")
    report.append(f"- **Missing Provisions**: {len(missing_provisions)}")
    report.append("")
    
    # Key Terms
    report.append("## Key Terms\n")
    for term, values in key_terms.items():
        if values:
            report.append(f"**{term.replace('_', ' ').title()}**:")
            for value in values:
                report.append(f"- {value}")
            report.append("")
    
    # Risk Assessment
    report.append("## Risk Assessment\n")
    
    if risks["high"]:
        report.append("### 🔴 High Risk Issues\n")
        for idx, risk in enumerate(risks["high"], 1):
            report.append(f"{idx}. **{risk['type']}**")
            report.append(f"   - Context: ...{risk['context']}...")
            report.append(f"   - **Action Required**: Negotiate this term before signing")
            report.append("")
    
    if risks["medium"]:
        report.append("### 🟡 Medium Risk Issues\n")
        for idx, risk in enumerate(risks["medium"], 1):
            report.append(f"{idx}. **{risk['type']}**")
            report.append(f"   - Context: ...{risk['context']}...")
            report.append(f"   - **Recommendation**: Consider negotiating or adding protective language")
            report.append("")
    
    if risks["low"]:
        report.append("### 🟢 Low Risk Issues\n")
        for idx, risk in enumerate(risks["low"], 1):
            report.append(f"{idx}. **{risk['type']}**")
            report.append(f"   - Context: ...{risk['context']}...")
            report.append(f"   - **Note**: Monitor but generally acceptable")
            report.append("")
    
    if not any(risks.values()):
        report.append("No significant risks identified.\n")
    
    # Missing Provisions
    if missing_provisions:
        report.append("## Missing Standard Provisions\n")
        report.append("The following standard provisions were not found:\n")
        for provision in missing_provisions:
            report.append(f"- [ ] {provision.title()}")
        report.append("\n**Recommendation**: Consider adding these provisions to protect your interests.\n")
    
    # Recommendations
    report.append("## Next Steps\n")
    if risks["high"]:
        report.append("1. **Do not sign** until high-risk issues are addressed")
        report.append("2. Request redlines addressing the high-risk items")
        report.append("3. Consult with legal counsel on negotiation strategy")
    elif risks["medium"]:
        report.append("1. Consider negotiating medium-risk items")
        report.append("2. Document risk acceptance if proceeding without changes")
        report.append("3. Ensure business stakeholders understand the risks")
    else:
        report.append("1. Review the contract in detail for any issues not caught by automation")
        report.append("2. Verify all business terms match your understanding")
        report.append("3. Consider having legal counsel do a final review")
    
    report.append("\n---\n")
    report.append("*This report was generated automatically. Always have contracts reviewed by qualified legal counsel.*")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Extract contract terms and identify risks"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Contract file (PDF, DOCX, or TXT)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed review report"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for results (JSON or MD)"
    )
    parser.add_argument(
        "--jurisdiction",
        help="Jurisdiction for review (us, eu, uk, etc.)"
    )
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    
    # Extract text
    print(f"Extracting text from {args.file.name}...", file=sys.stderr)
    text = extract_text_from_file(args.file)
    
    # Extract key terms
    print("Analyzing key terms...", file=sys.stderr)
    key_terms = extract_key_terms(text)
    
    # Identify risks
    print("Identifying risks...", file=sys.stderr)
    risks = identify_risks(text)
    
    # Check missing provisions
    print("Checking for missing provisions...", file=sys.stderr)
    missing_provisions = check_missing_provisions(text)
    
    # Generate output
    if args.report:
        report = generate_report(
            args.file, text, key_terms, risks, missing_provisions, args.jurisdiction
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\nReport saved to: {args.output}", file=sys.stderr)
        else:
            print("\n" + report)
    else:
        # JSON output
        result = {
            "file": str(args.file),
            "analyzed_at": datetime.now().isoformat(),
            "jurisdiction": args.jurisdiction,
            "key_terms": key_terms,
            "risks": risks,
            "missing_provisions": missing_provisions,
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to: {args.output}", file=sys.stderr)
        else:
            print(json.dumps(result, indent=2))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
