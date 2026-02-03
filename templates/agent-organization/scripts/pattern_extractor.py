#!/usr/bin/env python3
"""
Pattern Extractor for {{agent_name}}

Extracts workflow and behavior patterns from file changes.
Called by PostToolUse hook after Write/Edit operations.

Usage:
  python pattern_extractor.py "{{agent_name}}"
  python pattern_extractor.py "{{agent_name}}" --analyze
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

def extract_from_change(agent_name: str, file_path: str = None, content: str = None) -> Dict:
    """Extract learnable patterns from a file change."""
    patterns_data = load_patterns()

    extracted = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "file": file_path,
        "patterns_found": []
    }

    if content:
        # Detect workflow patterns
        if "## Workflow" in content or "### Step" in content:
            extracted["patterns_found"].append({
                "type": "workflow",
                "description": "Workflow structure pattern",
                "confidence": 0.7
            })

        # Detect output format patterns
        if "## Output" in content or "```json" in content:
            extracted["patterns_found"].append({
                "type": "output_format",
                "description": "Output format definition",
                "confidence": 0.6
            })

        # Detect constraint patterns
        if "## Constraints" in content or "DON'T" in content or "NOT" in content:
            extracted["patterns_found"].append({
                "type": "constraint",
                "description": "Constraint definition",
                "confidence": 0.7
            })

        # Detect error handling
        if "error" in content.lower() or "exception" in content.lower():
            extracted["patterns_found"].append({
                "type": "error_handling",
                "description": "Error handling pattern",
                "confidence": 0.65
            })

    # Store patterns with sufficient confidence
    for pattern in extracted["patterns_found"]:
        if pattern.get("confidence", 0) >= 0.6:
            patterns_data["patterns"].append({
                "id": f"ext-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(patterns_data['patterns'])}",
                "type": "agent_learned",
                "source": "pattern_extractor.py",
                "agent": agent_name,
                "pattern_type": pattern["type"],
                "description": pattern["description"],
                "confidence": pattern["confidence"],
                "learned_at": datetime.now().isoformat(),
                "applied": False
            })

    patterns_data["learning_stats"]["last_extraction"] = datetime.now().isoformat()
    save_patterns(patterns_data)

    return {
        "extraction_complete": True,
        "agent": agent_name,
        "patterns_extracted": len(extracted["patterns_found"]),
        "patterns": extracted["patterns_found"]
    }

def analyze_agent_patterns(agent_name: str) -> Dict:
    """Analyze agent patterns for improvements."""
    patterns_data = load_patterns()
    agent_patterns = [p for p in patterns_data["patterns"] if p.get("agent") == agent_name]

    # Analyze pattern distribution
    by_type = {}
    for pattern in agent_patterns:
        ptype = pattern.get("pattern_type", "unknown")
        by_type[ptype] = by_type.get(ptype, 0) + 1

    # Identify gaps
    expected_types = ["workflow", "output_format", "constraint", "error_handling", "validation"]
    gaps = [t for t in expected_types if t not in by_type]

    # Calculate health score
    total_expected = len(expected_types)
    covered = len([t for t in expected_types if t in by_type])
    health_score = int((covered / total_expected) * 100)

    return {
        "agent": agent_name,
        "total_patterns": len(agent_patterns),
        "by_type": by_type,
        "pattern_gaps": gaps,
        "health_score": health_score,
        "recommendations": [
            f"Add {gap} patterns" for gap in gaps[:3]
        ]
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Agent name required",
            "usage": "pattern_extractor.py <agent_name> [--analyze]"
        }, indent=2))
        sys.exit(1)

    agent_name = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--analyze":
        result = analyze_agent_patterns(agent_name)
    else:
        # Get file change info from environment
        file_path = os.environ.get("TOOL_FILE_PATH", None)
        content = os.environ.get("TOOL_CONTENT", None)
        result = extract_from_change(agent_name, file_path, content)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
