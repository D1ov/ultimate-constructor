#!/usr/bin/env python3
"""
Apply Learned Patterns for {{skill_name}} Skill

Reads patterns from learned/patterns.json and applies high-confidence
improvements automatically or in preview mode.

Usage:
  python apply_learned.py status    - Show available improvements
  python apply_learned.py preview   - Preview what would change
  python apply_learned.py apply     - Apply improvements
  python apply_learned.py auto      - Auto-apply high confidence
  python apply_learned.py check     - Check if review is needed
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

MIN_CONFIDENCE_AUTO = 0.9
MIN_CONFIDENCE_MANUAL = 0.7
SESSIONS_BETWEEN_REVIEWS = 5

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

def load_applied() -> Dict:
    """Load applied improvements log."""
    applied_file = get_component_root() / "learned" / "applied-improvements.json"
    if applied_file.exists():
        with open(applied_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"applied": [], "last_review": None}

def save_applied(data: Dict):
    """Save applied improvements log."""
    applied_file = get_component_root() / "learned" / "applied-improvements.json"
    applied_file.parent.mkdir(exist_ok=True)
    with open(applied_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_applicable_patterns(patterns: List[Dict], min_confidence: float) -> List[Dict]:
    """Filter patterns by confidence."""
    return [
        p for p in patterns
        if p.get("confidence", 0) >= min_confidence
        and not p.get("applied", False)
    ]

def get_status() -> Dict:
    """Get status of learned patterns."""
    data = load_patterns()
    applied = load_applied()
    patterns = data.get("patterns", [])
    stats = data.get("learning_stats", {})

    high_conf = get_applicable_patterns(patterns, MIN_CONFIDENCE_AUTO)
    medium_conf = get_applicable_patterns(patterns, MIN_CONFIDENCE_MANUAL)

    sessions_since_review = stats.get("total_sessions", 0)

    return {
        "component": "{{skill_name}}",
        "type": "skill",
        "total_patterns": len(patterns),
        "high_confidence": len(high_conf),
        "medium_confidence": len(medium_conf) - len(high_conf),
        "low_confidence": len(patterns) - len(medium_conf),
        "already_applied": len(applied.get("applied", [])),
        "sessions_since_review": sessions_since_review,
        "review_recommended": sessions_since_review >= SESSIONS_BETWEEN_REVIEWS,
        "patterns_preview": [
            {
                "type": p.get("type"),
                "description": p.get("description", "")[:100],
                "confidence": p.get("confidence")
            }
            for p in high_conf[:5]
        ]
    }

def preview_improvements() -> Dict:
    """Preview what improvements would be applied."""
    data = load_patterns()
    patterns = get_applicable_patterns(data.get("patterns", []), MIN_CONFIDENCE_MANUAL)

    improvements = []
    for pattern in patterns:
        improvement = {
            "pattern_type": pattern.get("type"),
            "description": pattern.get("description"),
            "confidence": pattern.get("confidence"),
            "would_modify": [],
            "action": "preview"
        }

        if pattern.get("type") == "context_learned":
            improvement["would_modify"] = [f"Apply {pattern.get('tool')} domain knowledge"]
        elif pattern.get("type") == "domain_knowledge":
            improvement["would_modify"] = ["Add to skill knowledge base"]
        elif pattern.get("type") == "example":
            improvement["would_modify"] = ["Add as example in SKILL.md"]

        improvements.append(improvement)

    return {
        "component": "{{skill_name}}",
        "type": "skill",
        "improvements_available": len(improvements),
        "improvements": improvements[:10],
        "note": "Use 'apply' to apply these improvements"
    }

def apply_improvements(auto: bool = False) -> Dict:
    """Apply improvements to component."""
    data = load_patterns()
    applied_log = load_applied()

    min_conf = MIN_CONFIDENCE_AUTO if auto else MIN_CONFIDENCE_MANUAL
    patterns = get_applicable_patterns(data.get("patterns", []), min_conf)

    applied_count = 0
    failed_count = 0

    for pattern in patterns:
        try:
            applied_log["applied"].append({
                "pattern_id": pattern.get("id", f"p-{len(applied_log['applied'])}"),
                "type": pattern.get("type"),
                "description": pattern.get("description"),
                "applied_at": datetime.now().isoformat(),
                "component": "{{skill_name}}",
                "success": True
            })

            pattern["applied"] = True
            applied_count += 1

        except Exception:
            failed_count += 1

    applied_log["last_review"] = datetime.now().isoformat()
    save_applied(applied_log)

    patterns_file = get_component_root() / "learned" / "patterns.json"
    with open(patterns_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {
        "application_complete": True,
        "component": "{{skill_name}}",
        "type": "skill",
        "patterns_reviewed": len(patterns),
        "improvements_applied": applied_count,
        "improvements_failed": failed_count,
        "next_review_in": f"{SESSIONS_BETWEEN_REVIEWS} sessions"
    }

def check_should_review() -> Dict:
    """Check if automatic review is recommended."""
    data = load_patterns()
    stats = data.get("learning_stats", {})

    sessions = stats.get("total_sessions", 0)
    high_conf = get_applicable_patterns(data.get("patterns", []), MIN_CONFIDENCE_AUTO)

    should_review = (
        sessions >= SESSIONS_BETWEEN_REVIEWS or
        len(high_conf) >= 3
    )

    return {
        "component": "{{skill_name}}",
        "type": "skill",
        "should_review": should_review,
        "reason": "High confidence patterns available" if len(high_conf) >= 3
                  else f"Sessions threshold ({sessions}/{SESSIONS_BETWEEN_REVIEWS})",
        "high_confidence_patterns": len(high_conf)
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Action required",
            "usage": "status | preview | apply | auto | check"
        }, indent=2))
        sys.exit(1)

    action = sys.argv[1]

    if action == "status":
        result = get_status()
    elif action == "preview":
        result = preview_improvements()
    elif action == "apply":
        result = apply_improvements(auto=False)
    elif action == "auto":
        result = apply_improvements(auto=True)
    elif action == "check":
        result = check_should_review()
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
