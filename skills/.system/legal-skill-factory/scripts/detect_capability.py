#!/usr/bin/env python3
"""
Detect legal capability gaps and suggest skill names.

Parses legal requests into components (domain, subject, action, jurisdiction)
and searches for matching existing skills.

Usage:
    python detect_capability.py "Review this NDA for compliance"
    python detect_capability.py "Draft a Master Service Agreement for EU"
    python detect_capability.py "Check GDPR compliance in our privacy policy"
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


# Supported legal domains
DOMAINS = {
    "contract", "compliance", "litigation", "ip", "intellectual property",
    "corporate", "regulatory", "employment", "real estate", "tax"
}

# Supported actions
ACTIONS = {
    "review", "draft", "redline", "analyze", "compare", "summarize",
    "check", "validate", "generate", "extract", "create", "audit"
}

# Common legal subjects
SUBJECTS = {
    # Contracts
    "nda", "non-disclosure", "confidentiality", "msa", "master service agreement",
    "sow", "statement of work", "employment agreement", "contractor agreement",
    "license", "licensing", "partnership", "joint venture", "merger",
    "acquisition", "lease", "terms of service", "tos", "privacy policy",
    "sla", "service level agreement", "vendor agreement",
    
    # Compliance
    "gdpr", "ccpa", "hipaa", "sox", "sarbanes-oxley", "pci-dss", "pci",
    "ferpa", "coppa", "glba", "fcra", "tcpa", "cpa", "data protection",
    
    # IP
    "patent", "trademark", "copyright", "trade secret", "ip portfolio",
    
    # Corporate
    "articles of incorporation", "bylaws", "shareholder agreement",
    "stock option", "equity", "board resolution"
}

# Jurisdiction codes
JURISDICTIONS = {
    "us", "usa", "united states", "eu", "european union", "uk", "united kingdom",
    "ca", "canada", "au", "australia", "de", "germany", "fr", "france",
    "jp", "japan", "cn", "china", "in", "india", "sg", "singapore"
}


def normalize_text(text: str) -> str:
    """Normalize text to lowercase and clean whitespace."""
    return re.sub(r'\s+', ' ', text.lower().strip())


def extract_components(request: str) -> Dict[str, Optional[str]]:
    """
    Extract domain, action, subject, and jurisdiction from a legal request.
    
    Returns:
        Dict with keys: domain, action, subject, jurisdiction
    """
    normalized = normalize_text(request)
    
    # Extract action
    action = None
    for act in ACTIONS:
        if act in normalized:
            action = act
            break
    
    # Extract domain
    domain = None
    for dom in DOMAINS:
        if dom in normalized:
            if dom == "intellectual property":
                domain = "ip"
            else:
                domain = dom
            break
    
    # If no explicit domain, infer from subject
    if not domain:
        if any(subj in normalized for subj in ["nda", "msa", "sow", "agreement", "contract", "license"]):
            domain = "contract"
        elif any(subj in normalized for subj in ["gdpr", "ccpa", "hipaa", "compliance", "regulation"]):
            domain = "compliance"
        elif any(subj in normalized for subj in ["patent", "trademark", "copyright"]):
            domain = "ip"
    
    # Extract subject
    subject = None
    for subj in SUBJECTS:
        if subj in normalized:
            # Normalize common variations
            if subj in ["non-disclosure", "confidentiality"]:
                subject = "nda"
            elif subj in ["master service agreement"]:
                subject = "msa"
            elif subj in ["statement of work"]:
                subject = "sow"
            elif subj in ["terms of service"]:
                subject = "tos"
            elif subj in ["sarbanes-oxley"]:
                subject = "sox"
            elif subj in ["pci-dss", "pci"]:
                subject = "pci"
            else:
                subject = subj.replace(" ", "-")
            break
    
    # Extract jurisdiction
    jurisdiction = None
    for juris in JURISDICTIONS:
        pattern = r'\b' + re.escape(juris) + r'\b'
        if re.search(pattern, normalized):
            # Normalize to short codes
            if juris in ["usa", "united states"]:
                jurisdiction = "us"
            elif juris in ["european union"]:
                jurisdiction = "eu"
            elif juris in ["united kingdom"]:
                jurisdiction = "uk"
            elif juris in ["canada"]:
                jurisdiction = "ca"
            elif juris in ["australia"]:
                jurisdiction = "au"
            elif juris in ["germany"]:
                jurisdiction = "de"
            elif juris in ["france"]:
                jurisdiction = "fr"
            elif juris in ["japan"]:
                jurisdiction = "jp"
            elif juris in ["china"]:
                jurisdiction = "cn"
            elif juris in ["india"]:
                jurisdiction = "in"
            elif juris in ["singapore"]:
                jurisdiction = "sg"
            else:
                jurisdiction = juris
            break
    
    return {
        "domain": domain,
        "action": action,
        "subject": subject,
        "jurisdiction": jurisdiction
    }


def suggest_skill_name(components: Dict[str, Optional[str]]) -> str:
    """
    Suggest a skill name following the convention:
    legal-[action]-[subject]-[jurisdiction]
    """
    parts = ["legal"]
    
    if components["action"]:
        parts.append(components["action"])
    
    if components["subject"]:
        parts.append(components["subject"])
    
    if components["jurisdiction"]:
        parts.append(components["jurisdiction"])
    
    return "-".join(parts)


def find_existing_skills(components: Dict[str, Optional[str]]) -> List[Dict[str, str]]:
    """
    Search for existing legal skills that match the request.
    
    Checks:
    1. ~/.codex/legal-skill-registry.json
    2. skills/.curated/legal/
    3. Installed skills
    """
    matches = []
    
    # Check registry file
    registry_path = Path.home() / ".codex" / "legal-skill-registry.json"
    if registry_path.exists():
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                for skill_name, skill_info in registry.get("skills", {}).items():
                    score = 0
                    if components["domain"] and skill_info.get("domain") == components["domain"]:
                        score += 2
                    if components["action"] and skill_info.get("action") == components["action"]:
                        score += 2
                    if components["subject"] and skill_info.get("subject") == components["subject"]:
                        score += 3
                    if components["jurisdiction"] and skill_info.get("jurisdiction") == components["jurisdiction"]:
                        score += 1
                    
                    if score >= 3:  # Threshold for a match
                        matches.append({
                            "name": skill_name,
                            "location": skill_info.get("location", "unknown"),
                            "score": score,
                            "source": "registry"
                        })
        except (json.JSONDecodeError, IOError):
            pass
    
    # Check curated legal skills directory
    # Try to find curated legal skills relative to script, or use environment variable
    curated_legal_env = os.getenv("LEGAL_SKILLS_PATH")
    if curated_legal_env:
        curated_legal = Path(curated_legal_env)
    else:
        curated_legal = Path(__file__).parent.parent.parent / ".curated" / "legal"
    
    if curated_legal.exists():
        for skill_dir in curated_legal.iterdir():
            if skill_dir.is_dir():
                skill_name = skill_dir.name
                # Parse skill name to extract components
                parts = skill_name.split("-")
                if parts and parts[0] == "legal":
                    score = 0
                    skill_action = parts[1] if len(parts) > 1 else None
                    skill_subject = parts[2] if len(parts) > 2 else None
                    skill_jurisdiction = parts[3] if len(parts) > 3 else None
                    
                    if components["action"] and skill_action == components["action"]:
                        score += 2
                    if components["subject"] and skill_subject == components["subject"]:
                        score += 3
                    if components["jurisdiction"] and skill_jurisdiction == components["jurisdiction"]:
                        score += 1
                    
                    if score >= 3:
                        matches.append({
                            "name": skill_name,
                            "location": str(skill_dir),
                            "score": score,
                            "source": "curated"
                        })
    
    # Sort by score (highest first)
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    return matches


def main():
    parser = argparse.ArgumentParser(
        description="Detect legal capability gaps and suggest skill names"
    )
    parser.add_argument(
        "request",
        help="Legal task request to analyze"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    # Extract components
    components = extract_components(args.request)
    
    # Suggest skill name
    suggested_name = suggest_skill_name(components)
    
    # Find existing skills
    existing_skills = find_existing_skills(components)
    
    # Prepare output
    result = {
        "request": args.request,
        "components": components,
        "suggested_skill_name": suggested_name,
        "existing_skills": existing_skills,
        "recommendation": None
    }
    
    # Determine recommendation
    if existing_skills:
        best_match = existing_skills[0]
        result["recommendation"] = f"Use existing skill: {best_match['name']}"
    else:
        result["recommendation"] = f"Create new skill: {suggested_name}"
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Request: {args.request}")
        print(f"\nParsed Components:")
        print(f"  Domain: {components['domain'] or 'not detected'}")
        print(f"  Action: {components['action'] or 'not detected'}")
        print(f"  Subject: {components['subject'] or 'not detected'}")
        print(f"  Jurisdiction: {components['jurisdiction'] or 'not detected'}")
        print(f"\nSuggested Skill Name: {suggested_name}")
        
        if existing_skills:
            print(f"\nExisting Skills Found ({len(existing_skills)}):")
            for skill in existing_skills:
                print(f"  - {skill['name']} (score: {skill['score']}, source: {skill['source']})")
                print(f"    Location: {skill['location']}")
        else:
            print("\nNo existing skills found.")
        
        print(f"\nRecommendation: {result['recommendation']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
