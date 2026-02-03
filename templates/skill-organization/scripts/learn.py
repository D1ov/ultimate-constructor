#!/usr/bin/env python3
"""
Learning Script for {{skill_name}} Skill

Extracts domain knowledge and patterns from file changes.
Called by PostToolUse hook after Write/Edit operations.

Usage:
  python learn.py "{{skill_name}}"
  python learn.py "{{skill_name}}" --analyze
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

def get_component_root() -> Path:
    """Get component root directory."""
    return Path(os.environ.get("COMPONENT_ROOT", Path(__file__).parent.parent))

def load_patterns() -> Dict:
    """Load learned patterns."""
    patterns_file = get_component_root() / "learned" / "patterns.json"
    if patterns_file.exists():
        with open(patterns_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"patterns": [], "learning_stats": {"total_sessions": 0}}

def save_patterns(data: Dict):
    """Save learned patterns."""
    patterns_file = get_component_root() / "learned" / "patterns.json"
    patterns_file.parent.mkdir(parents=True, exist_ok=True)
    with open(patterns_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_from_change(skill_name: str, file_path: str = None, content: str = None) -> Dict:
    """Extract learnable patterns from a file change."""
    patterns_data = load_patterns()

    # Look for domain-specific patterns in the change
    extracted = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "file": file_path,
        "patterns_found": []
    }

    if content:
        # Detect common patterns in the content
        if "```" in content:
            extracted["patterns_found"].append({
                "type": "code_example",
                "description": "Code example added",
                "confidence": 0.6
            })

        if "## " in content or "### " in content:
            extracted["patterns_found"].append({
                "type": "documentation",
                "description": "Documentation structure added",
                "confidence": 0.5
            })

        if "error" in content.lower() or "fix" in content.lower():
            extracted["patterns_found"].append({
                "type": "error_handling",
                "description": "Error handling pattern",
                "confidence": 0.7
            })

    # Store if any patterns found with sufficient confidence
    for pattern in extracted["patterns_found"]:
        if pattern.get("confidence", 0) >= 0.6:
            patterns_data["patterns"].append({
                "id": f"learn-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(patterns_data['patterns'])}",
                "type": "skill_learned",
                "source": "learn.py",
                "skill": skill_name,
                "pattern_type": pattern["type"],
                "description": pattern["description"],
                "confidence": pattern["confidence"],
                "learned_at": datetime.now().isoformat(),
                "applied": False
            })

    patterns_data["learning_stats"]["last_learning"] = datetime.now().isoformat()
    save_patterns(patterns_data)

    return {
        "learning_complete": True,
        "skill": skill_name,
        "patterns_extracted": len(extracted["patterns_found"]),
        "patterns": extracted["patterns_found"]
    }

def analyze_skill_domain(skill_name: str) -> Dict:
    """Analyze skill domain for knowledge gaps."""
    patterns_data = load_patterns()
    skill_patterns = [p for p in patterns_data["patterns"] if p.get("skill") == skill_name]

    # Analyze pattern distribution
    by_type = {}
    for pattern in skill_patterns:
        ptype = pattern.get("pattern_type", "unknown")
        by_type[ptype] = by_type.get(ptype, 0) + 1

    # Identify gaps
    expected_types = ["code_example", "documentation", "error_handling", "best_practice", "antipattern"]
    gaps = [t for t in expected_types if t not in by_type]

    return {
        "skill": skill_name,
        "total_patterns": len(skill_patterns),
        "by_type": by_type,
        "knowledge_gaps": gaps,
        "recommendations": [
            f"Add {gap} patterns" for gap in gaps[:3]
        ]
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Skill name required",
            "usage": "learn.py <skill_name> [--analyze]"
        }, indent=2))
        sys.exit(1)

    skill_name = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--analyze":
        result = analyze_skill_domain(skill_name)
    else:
        # Get file change info from environment
        file_path = os.environ.get("TOOL_FILE_PATH", None)
        content = os.environ.get("TOOL_CONTENT", None)
        result = extract_from_change(skill_name, file_path, content)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
