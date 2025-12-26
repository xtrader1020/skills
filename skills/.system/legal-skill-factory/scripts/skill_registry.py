#!/usr/bin/env python3
"""
Manage registry of legal skills and capabilities.

Stores legal skills in ~/.codex/legal-skill-registry.json and tracks:
- Skill name and location
- Domain, action, subject, jurisdiction
- Usage statistics
- Last used timestamp

Usage:
    # Register a new skill
    python skill_registry.py register legal-review-nda-us --domain contract --action review --subject nda --jurisdiction us

    # Find matching skills
    python skill_registry.py find --domain contract --action review

    # List all legal skills
    python skill_registry.py list

    # Update usage stats
    python skill_registry.py use legal-review-nda-us
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


REGISTRY_PATH = Path(os.getenv("LEGAL_SKILLS_REGISTRY", str(Path.home() / ".codex" / "legal-skill-registry.json")))


def load_registry() -> Dict:
    """Load the legal skill registry from disk."""
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load registry: {e}", file=sys.stderr)
            return {"version": "1.0", "skills": {}}
    else:
        return {"version": "1.0", "skills": {}}


def save_registry(registry: Dict) -> None:
    """Save the legal skill registry to disk."""
    # Ensure directory exists
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(REGISTRY_PATH, 'w') as f:
            json.dump(registry, f, indent=2)
    except IOError as e:
        print(f"Error: Failed to save registry: {e}", file=sys.stderr)
        sys.exit(1)


def register_skill(
    skill_name: str,
    domain: Optional[str] = None,
    action: Optional[str] = None,
    subject: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    location: Optional[str] = None
) -> None:
    """Register a new legal skill in the registry."""
    registry = load_registry()
    
    if skill_name in registry["skills"]:
        print(f"Warning: Skill '{skill_name}' already exists. Updating.", file=sys.stderr)
    
    registry["skills"][skill_name] = {
        "domain": domain,
        "action": action,
        "subject": subject,
        "jurisdiction": jurisdiction,
        "location": location or "unknown",
        "usage_count": registry["skills"].get(skill_name, {}).get("usage_count", 0),
        "success_count": registry["skills"].get(skill_name, {}).get("success_count", 0),
        "created_at": registry["skills"].get(skill_name, {}).get("created_at") or datetime.now().isoformat(),
        "last_used": registry["skills"].get(skill_name, {}).get("last_used"),
        "updated_at": datetime.now().isoformat()
    }
    
    save_registry(registry)
    print(f"Successfully registered skill: {skill_name}")


def find_skills(
    domain: Optional[str] = None,
    action: Optional[str] = None,
    subject: Optional[str] = None,
    jurisdiction: Optional[str] = None
) -> List[Dict]:
    """Find skills matching the given criteria."""
    registry = load_registry()
    matches = []
    
    for skill_name, skill_info in registry["skills"].items():
        score = 0
        
        if domain and skill_info.get("domain") == domain:
            score += 2
        if action and skill_info.get("action") == action:
            score += 2
        if subject and skill_info.get("subject") == subject:
            score += 3
        if jurisdiction and skill_info.get("jurisdiction") == jurisdiction:
            score += 1
        
        # Only include if at least one criterion matches
        if score > 0:
            matches.append({
                "name": skill_name,
                "info": skill_info,
                "score": score
            })
    
    # Sort by score (highest first), then by usage count
    matches.sort(key=lambda x: (x["score"], x["info"].get("usage_count", 0)), reverse=True)
    
    return matches


def list_skills(sort_by: str = "name") -> List[Dict]:
    """List all registered legal skills."""
    registry = load_registry()
    skills = []
    
    for skill_name, skill_info in registry["skills"].items():
        skills.append({
            "name": skill_name,
            "info": skill_info
        })
    
    # Sort by specified field
    if sort_by == "usage":
        skills.sort(key=lambda x: x["info"].get("usage_count", 0), reverse=True)
    elif sort_by == "recent":
        skills.sort(
            key=lambda x: x["info"].get("last_used") or "",
            reverse=True
        )
    else:  # name
        skills.sort(key=lambda x: x["name"])
    
    return skills


def use_skill(skill_name: str, success: bool = True) -> None:
    """Update usage statistics for a skill."""
    registry = load_registry()
    
    if skill_name not in registry["skills"]:
        print(f"Error: Skill '{skill_name}' not found in registry", file=sys.stderr)
        sys.exit(1)
    
    skill_info = registry["skills"][skill_name]
    skill_info["usage_count"] = skill_info.get("usage_count", 0) + 1
    if success:
        skill_info["success_count"] = skill_info.get("success_count", 0) + 1
    skill_info["last_used"] = datetime.now().isoformat()
    
    save_registry(registry)
    print(f"Updated usage stats for: {skill_name}")


def remove_skill(skill_name: str) -> None:
    """Remove a skill from the registry."""
    registry = load_registry()
    
    if skill_name not in registry["skills"]:
        print(f"Error: Skill '{skill_name}' not found in registry", file=sys.stderr)
        sys.exit(1)
    
    del registry["skills"][skill_name]
    save_registry(registry)
    print(f"Removed skill: {skill_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage legal skills registry"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Register command
    register_parser = subparsers.add_parser("register", help="Register a new skill")
    register_parser.add_argument("skill_name", help="Name of the skill")
    register_parser.add_argument("--domain", help="Legal domain (contract, compliance, etc.)")
    register_parser.add_argument("--action", help="Action (review, draft, check, etc.)")
    register_parser.add_argument("--subject", help="Subject (nda, msa, gdpr, etc.)")
    register_parser.add_argument("--jurisdiction", help="Jurisdiction (us, eu, uk, etc.)")
    register_parser.add_argument("--location", help="Location of the skill")
    
    # Find command
    find_parser = subparsers.add_parser("find", help="Find matching skills")
    find_parser.add_argument("--domain", help="Legal domain to match")
    find_parser.add_argument("--action", help="Action to match")
    find_parser.add_argument("--subject", help="Subject to match")
    find_parser.add_argument("--jurisdiction", help="Jurisdiction to match")
    find_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all skills")
    list_parser.add_argument(
        "--sort",
        choices=["name", "usage", "recent"],
        default="name",
        help="Sort order"
    )
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # Use command
    use_parser = subparsers.add_parser("use", help="Update usage stats")
    use_parser.add_argument("skill_name", help="Name of the skill")
    use_parser.add_argument(
        "--failed",
        action="store_true",
        help="Mark as failed usage"
    )
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a skill")
    remove_parser.add_argument("skill_name", help="Name of the skill to remove")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == "register":
        register_skill(
            args.skill_name,
            domain=args.domain,
            action=args.action,
            subject=args.subject,
            jurisdiction=args.jurisdiction,
            location=args.location
        )
    
    elif args.command == "find":
        matches = find_skills(
            domain=args.domain,
            action=args.action,
            subject=args.subject,
            jurisdiction=args.jurisdiction
        )
        
        if args.json:
            print(json.dumps(matches, indent=2))
        else:
            if matches:
                print(f"Found {len(matches)} matching skill(s):\n")
                for match in matches:
                    info = match["info"]
                    print(f"  {match['name']} (score: {match['score']})")
                    print(f"    Domain: {info.get('domain', 'N/A')}")
                    print(f"    Action: {info.get('action', 'N/A')}")
                    print(f"    Subject: {info.get('subject', 'N/A')}")
                    print(f"    Jurisdiction: {info.get('jurisdiction', 'N/A')}")
                    print(f"    Location: {info.get('location', 'N/A')}")
                    print(f"    Usage: {info.get('usage_count', 0)} times")
                    if info.get('last_used'):
                        print(f"    Last used: {info['last_used']}")
                    print()
            else:
                print("No matching skills found.")
    
    elif args.command == "list":
        skills = list_skills(sort_by=args.sort)
        
        if args.json:
            print(json.dumps(skills, indent=2))
        else:
            if skills:
                print(f"Registered legal skills ({len(skills)}):\n")
                for skill in skills:
                    info = skill["info"]
                    print(f"  {skill['name']}")
                    print(f"    Domain: {info.get('domain', 'N/A')}")
                    print(f"    Action: {info.get('action', 'N/A')}")
                    print(f"    Subject: {info.get('subject', 'N/A')}")
                    print(f"    Jurisdiction: {info.get('jurisdiction', 'N/A')}")
                    print(f"    Location: {info.get('location', 'N/A')}")
                    print(f"    Usage: {info.get('usage_count', 0)} times")
                    if info.get('last_used'):
                        print(f"    Last used: {info['last_used']}")
                    print()
            else:
                print("No skills registered yet.")
    
    elif args.command == "use":
        use_skill(args.skill_name, success=not args.failed)
    
    elif args.command == "remove":
        remove_skill(args.skill_name)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
