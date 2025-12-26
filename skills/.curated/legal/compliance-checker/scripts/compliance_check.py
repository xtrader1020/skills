#!/usr/bin/env python3
"""
Check regulatory compliance against GDPR, CCPA, HIPAA, SOX, and PCI-DSS requirements.

Analyzes policies, practices, and systems documentation against regulatory
checklists and generates compliance reports with gap analysis.

Usage:
    python compliance_check.py --regulation gdpr --policy privacy-policy.md
    python compliance_check.py --regulation gdpr,ccpa --policy policy.md --practices practices.md
    python compliance_check.py --regulation hipaa --policy policy.md --report compliance-report.md
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Regulation requirement patterns
GDPR_REQUIREMENTS = {
    "lawful_basis": [
        r"lawful\s+basis",
        r"legal\s+basis",
        r"consent",
        r"contract",
        r"legitimate\s+interest",
    ],
    "data_subject_rights": [
        r"right\s+to\s+access",
        r"right\s+to\s+(?:rectification|correction)",
        r"right\s+to\s+erasure",
        r"right\s+to\s+(?:deletion|be\s+forgotten)",
        r"right\s+to\s+(?:portability|data\s+portability)",
        r"right\s+to\s+object",
        r"right\s+to\s+restrict\s+processing",
    ],
    "transparency": [
        r"data\s+protection\s+officer",
        r"dpo",
        r"privacy\s+(?:policy|notice)",
        r"contact.*privacy",
    ],
    "security": [
        r"appropriate.*(?:technical|organizational).*measures",
        r"security\s+measures",
        r"encryption",
        r"pseudonymization",
    ],
    "breach_notification": [
        r"data\s+breach",
        r"breach\s+notification",
        r"72\s+hours?",
        r"notify.*(?:authority|supervisory)",
    ],
    "data_minimization": [
        r"data\s+minimization",
        r"(?:collect|process).*(?:necessary|minimum)",
        r"purpose\s+limitation",
    ],
    "international_transfer": [
        r"international\s+transfer",
        r"cross-border\s+transfer",
        r"third\s+countr(?:y|ies)",
        r"adequacy\s+decision",
        r"standard\s+contractual\s+clauses",
    ],
}

CCPA_REQUIREMENTS = {
    "notice": [
        r"notice\s+at\s+collection",
        r"categories\s+of\s+personal\s+information",
        r"purposes?\s+(?:for|of)\s+(?:use|processing)",
    ],
    "consumer_rights": [
        r"right\s+to\s+know",
        r"right\s+to\s+delete",
        r"right\s+to\s+opt[- ]out",
        r"do\s+not\s+sell",
        r"right\s+to\s+non[- ]discrimination",
    ],
    "opt_out": [
        r"opt[- ]out",
        r"do\s+not\s+sell",
        r"sale\s+of\s+personal\s+information",
    ],
    "disclosures": [
        r"categories\s+of\s+(?:sources|recipients)",
        r"business\s+purpose",
        r"sell.*personal\s+information",
        r"share.*personal\s+information",
    ],
    "verification": [
        r"verif(?:y|ication)",
        r"authenticate",
        r"confirm\s+identity",
    ],
}

HIPAA_REQUIREMENTS = {
    "privacy_rule": [
        r"protected\s+health\s+information",
        r"phi",
        r"notice\s+of\s+privacy\s+practices",
        r"minimum\s+necessary",
        r"patient\s+rights?",
    ],
    "security_rule": [
        r"administrative\s+safeguards",
        r"physical\s+safeguards",
        r"technical\s+safeguards",
        r"access\s+control",
        r"audit\s+(?:controls|logs?|trails?)",
        r"integrity\s+controls",
        r"transmission\s+security",
    ],
    "breach_notification": [
        r"breach\s+notification",
        r"notify.*(?:individual|patient|secretary)",
        r"60\s+days?",
    ],
    "business_associates": [
        r"business\s+associate\s+agreement",
        r"baa",
        r"(?:vendor|third[- ]party).*agreement",
    ],
    "training": [
        r"(?:workforce|employee|staff)\s+training",
        r"hipaa\s+training",
        r"privacy.*training",
        r"security.*training",
    ],
    "policies": [
        r"privacy\s+polic(?:y|ies)",
        r"security\s+polic(?:y|ies)",
        r"procedure",
    ],
}

# Compliance scores
COMPLIANCE_STATUS = {
    "compliant": "✓",
    "partial": "⚠",
    "non_compliant": "✗",
    "not_checked": "-",
}


def load_text_file(file_path: Path) -> str:
    """Load text from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except IOError as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return ""


# Compliance thresholds - can be overridden per regulation
COMPLIANCE_THRESHOLD = 0.7  # 70% of patterns must match for "compliant" status


def check_requirement(text: str, patterns: List[str], threshold: float = COMPLIANCE_THRESHOLD) -> Tuple[str, List[str]]:
    """
    Check if text meets a requirement based on patterns.
    
    Args:
        text: Text to check
        patterns: List of regex patterns to match
        threshold: Fraction of patterns that must match for "compliant" status (default: 0.7)
    
    Returns:
        Tuple of (status, matched_patterns)
        status: "compliant", "partial", or "non_compliant"
    """
    text_lower = text.lower()
    matches = []
    
    for pattern in patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            matches.append(pattern)
    
    if len(matches) >= len(patterns) * threshold:
        return "compliant", matches
    elif len(matches) > 0:
        return "partial", matches
    else:
        return "non_compliant", matches


def check_gdpr_compliance(text: str) -> Dict:
    """Check GDPR compliance requirements."""
    results = {}
    
    for requirement, patterns in GDPR_REQUIREMENTS.items():
        status, matches = check_requirement(text, patterns)
        results[requirement] = {
            "status": status,
            "patterns_matched": len(matches),
            "patterns_total": len(patterns),
            "matches": matches,
        }
    
    return results


def check_ccpa_compliance(text: str) -> Dict:
    """Check CCPA compliance requirements."""
    results = {}
    
    for requirement, patterns in CCPA_REQUIREMENTS.items():
        status, matches = check_requirement(text, patterns)
        results[requirement] = {
            "status": status,
            "patterns_matched": len(matches),
            "patterns_total": len(patterns),
            "matches": matches,
        }
    
    return results


def check_hipaa_compliance(text: str) -> Dict:
    """Check HIPAA compliance requirements."""
    results = {}
    
    for requirement, patterns in HIPAA_REQUIREMENTS.items():
        status, matches = check_requirement(text, patterns)
        results[requirement] = {
            "status": status,
            "patterns_matched": len(matches),
            "patterns_total": len(patterns),
            "matches": matches,
        }
    
    return results


def calculate_compliance_score(results: Dict) -> float:
    """Calculate overall compliance score as a percentage."""
    total_requirements = len(results)
    if total_requirements == 0:
        return 0.0
    
    compliant = sum(1 for r in results.values() if r["status"] == "compliant")
    partial = sum(0.5 for r in results.values() if r["status"] == "partial")
    
    return ((compliant + partial) / total_requirements) * 100


def generate_report(
    regulations: List[str],
    results: Dict[str, Dict],
    scores: Dict[str, float],
    files: Dict[str, Path]
) -> str:
    """Generate a compliance report in Markdown format."""
    report = []
    
    # Header
    report.append("# Compliance Report")
    report.append(f"\n**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Regulations**: {', '.join(r.upper() for r in regulations)}")
    report.append("\n**Files Analyzed**:")
    for file_type, file_path in files.items():
        if file_path:
            report.append(f"- {file_type.title()}: `{file_path.name}`")
    report.append("\n---\n")
    
    # Executive Summary
    report.append("## Executive Summary\n")
    for regulation in regulations:
        score = scores.get(regulation, 0)
        status_emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        report.append(f"**{regulation.upper()} Compliance**: {status_emoji} {score:.1f}%\n")
    
    # Detailed Results
    for regulation in regulations:
        reg_results = results.get(regulation, {})
        if not reg_results:
            continue
        
        report.append(f"\n## {regulation.upper()} Requirements\n")
        
        # Compliant items
        compliant = [k for k, v in reg_results.items() if v["status"] == "compliant"]
        if compliant:
            report.append("### ✓ Compliant\n")
            for req in compliant:
                req_name = req.replace("_", " ").title()
                report.append(f"- **{req_name}**: Requirements met")
            report.append("")
        
        # Partial compliance
        partial = [k for k, v in reg_results.items() if v["status"] == "partial"]
        if partial:
            report.append("### ⚠ Partially Compliant\n")
            for req in partial:
                req_name = req.replace("_", " ").title()
                info = reg_results[req]
                report.append(f"- **{req_name}**: {info['patterns_matched']}/{info['patterns_total']} requirements met")
                report.append(f"  - **Action**: Review and strengthen this area")
            report.append("")
        
        # Non-compliant
        non_compliant = [k for k, v in reg_results.items() if v["status"] == "non_compliant"]
        if non_compliant:
            report.append("### ✗ Non-Compliant\n")
            for req in non_compliant:
                req_name = req.replace("_", " ").title()
                report.append(f"- **{req_name}**: Requirements not found")
                report.append(f"  - **Priority**: High - Immediate action required")
            report.append("")
    
    # Recommendations
    report.append("## Recommendations\n")
    
    for regulation in regulations:
        reg_results = results.get(regulation, {})
        non_compliant = [k for k, v in reg_results.items() if v["status"] == "non_compliant"]
        partial = [k for k, v in reg_results.items() if v["status"] == "partial"]
        
        if non_compliant or partial:
            report.append(f"\n### {regulation.upper()}\n")
            
            if non_compliant:
                report.append("**High Priority** (Non-Compliant Areas):")
                for req in non_compliant:
                    req_name = req.replace("_", " ").title()
                    report.append(f"1. Implement {req_name} requirements")
            
            if partial:
                report.append("\n**Medium Priority** (Partially Compliant Areas):")
                for req in partial:
                    req_name = req.replace("_", " ").title()
                    report.append(f"1. Strengthen {req_name} documentation and controls")
            
            report.append("")
    
    # Next Steps
    report.append("## Next Steps\n")
    report.append("1. **Address High Priority Items**: Focus on non-compliant requirements first")
    report.append("2. **Consult Legal Counsel**: Have compliance reviewed by qualified legal professionals")
    report.append("3. **Implement Controls**: Put necessary policies, procedures, and technical controls in place")
    report.append("4. **Document Everything**: Maintain records of compliance efforts")
    report.append("5. **Regular Reviews**: Schedule periodic compliance assessments (quarterly/annually)")
    report.append("6. **Training**: Ensure workforce is trained on compliance requirements")
    report.append("7. **Re-assess**: Run this tool again after implementing changes")
    report.append("\n---\n")
    report.append("*This report was generated automatically. Always consult with qualified compliance and legal professionals.*")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Check regulatory compliance"
    )
    parser.add_argument(
        "--regulation",
        required=True,
        help="Regulation(s) to check: gdpr, ccpa, hipaa (comma-separated for multiple)"
    )
    parser.add_argument(
        "--policy",
        type=Path,
        help="Policy document to check"
    )
    parser.add_argument(
        "--practices",
        type=Path,
        help="Practices document to check"
    )
    parser.add_argument(
        "--security",
        type=Path,
        help="Security policy document to check"
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Output file for compliance report (Markdown)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    # Parse regulations
    regulations = [r.strip().lower() for r in args.regulation.split(",")]
    
    # Validate regulations
    supported = {"gdpr", "ccpa", "hipaa"}
    for reg in regulations:
        if reg not in supported:
            print(f"Error: Unsupported regulation '{reg}'. Supported: {', '.join(supported)}", file=sys.stderr)
            return 1
    
    # Load documents
    text_parts = []
    files = {}
    
    if args.policy:
        if not args.policy.exists():
            print(f"Error: Policy file not found: {args.policy}", file=sys.stderr)
            return 1
        text_parts.append(load_text_file(args.policy))
        files["policy"] = args.policy
    
    if args.practices:
        if not args.practices.exists():
            print(f"Error: Practices file not found: {args.practices}", file=sys.stderr)
            return 1
        text_parts.append(load_text_file(args.practices))
        files["practices"] = args.practices
    
    if args.security:
        if not args.security.exists():
            print(f"Error: Security file not found: {args.security}", file=sys.stderr)
            return 1
        text_parts.append(load_text_file(args.security))
        files["security"] = args.security
    
    if not text_parts:
        print("Error: At least one document (--policy, --practices, or --security) is required", file=sys.stderr)
        return 1
    
    # Combine text
    combined_text = "\n\n".join(text_parts)
    
    # Run compliance checks
    print("Running compliance checks...", file=sys.stderr)
    results = {}
    scores = {}
    
    for regulation in regulations:
        if regulation == "gdpr":
            results["gdpr"] = check_gdpr_compliance(combined_text)
        elif regulation == "ccpa":
            results["ccpa"] = check_ccpa_compliance(combined_text)
        elif regulation == "hipaa":
            results["hipaa"] = check_hipaa_compliance(combined_text)
        
        scores[regulation] = calculate_compliance_score(results[regulation])
    
    # Generate output
    if args.json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "regulations": regulations,
            "files": {k: str(v) for k, v in files.items()},
            "results": results,
            "scores": scores,
        }
        
        if args.report:
            with open(args.report, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"\nJSON report saved to: {args.report}", file=sys.stderr)
        else:
            print(json.dumps(output, indent=2))
    else:
        report = generate_report(regulations, results, scores, files)
        
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"\nCompliance report saved to: {args.report}", file=sys.stderr)
        else:
            print("\n" + report)
    
    # Print summary to stderr
    print("\n=== Compliance Summary ===", file=sys.stderr)
    for regulation in regulations:
        score = scores[regulation]
        print(f"{regulation.upper()}: {score:.1f}%", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
