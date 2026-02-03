#!/usr/bin/env python3
"""
Context Tracker for {{skill_name}} Skill

Success-based self-learning that tracks tool calls and their outcomes.
Learns ONLY from successful approaches. Failed attempts are stored as antipatterns.

Usage:
  python context_tracker.py track <tool> <result> <success> [context]
  python context_tracker.py confirm <positive|negative|correction> [details]
  python context_tracker.py goal <description>
  python context_tracker.py analyze
  python context_tracker.py extract
  python context_tracker.py clear
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import hashlib

def get_component_root() -> Path:
    """Get component root directory."""
    return Path(os.environ.get("COMPONENT_ROOT", Path(__file__).parent.parent))

def get_session_file() -> Path:
    """Get current session tracking file."""
    learned_dir = get_component_root() / "learned" / "sessions"
    learned_dir.mkdir(parents=True, exist_ok=True)
    session_id = os.environ.get("CLAUDE_SESSION_ID", datetime.now().strftime("%Y%m%d"))
    return learned_dir / f"session-{session_id}.json"

def load_session() -> Dict:
    """Load current session data."""
    session_file = get_session_file()
    if session_file.exists():
        with open(session_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "session_id": os.environ.get("CLAUDE_SESSION_ID", "unknown"),
        "component": "{{skill_name}}",
        "type": "skill",
        "started": datetime.now().isoformat(),
        "goal": None,
        "domain_context": [],
        "actions": [],
        "successes": [],
        "failures": [],
        "user_confirmations": []
    }

def save_session(data: Dict):
    """Save session data."""
    session_file = get_session_file()
    data["last_updated"] = datetime.now().isoformat()
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def track_action(tool: str, result: str, success: bool, context: str = "") -> Dict:
    """Track a tool action and its result."""
    session = load_session()

    action = {
        "id": f"act-{len(session['actions'])+1}",
        "timestamp": datetime.now().isoformat(),
        "tool": tool,
        "result_summary": result[:500],
        "success": success,
        "context": context,
        "result_hash": hashlib.md5(result.encode()).hexdigest()[:8]
    }

    session["actions"].append(action)

    if success:
        session["successes"].append(action["id"])
    else:
        session["failures"].append(action["id"])

    save_session(session)

    return {
        "tracked": True,
        "action_id": action["id"],
        "success": success,
        "total_actions": len(session["actions"]),
        "success_rate": len(session["successes"]) / len(session["actions"]) if session["actions"] else 0
    }

def track_user_confirmation(confirmation_type: str, details: str = "") -> Dict:
    """Track when user confirms something worked."""
    session = load_session()

    confirmation = {
        "timestamp": datetime.now().isoformat(),
        "type": confirmation_type,
        "details": details,
        "related_actions": session["actions"][-3:] if session["actions"] else []
    }

    session["user_confirmations"].append(confirmation)

    if confirmation_type == "positive" and session["successes"]:
        last_success_id = session["successes"][-1]
        for action in session["actions"]:
            if action["id"] == last_success_id:
                action["user_confirmed"] = True
                break

    save_session(session)

    return {
        "confirmation_recorded": True,
        "type": confirmation_type,
        "boosted_actions": session["successes"][-1:] if confirmation_type == "positive" else []
    }

def set_goal(goal: str) -> Dict:
    """Set the current goal/objective for context."""
    session = load_session()
    session["goal"] = goal
    session["goal_set_at"] = datetime.now().isoformat()
    save_session(session)
    return {"goal_set": True, "goal": goal}

def analyze_session() -> Dict:
    """Analyze session to identify learnable patterns."""
    session = load_session()

    by_tool = {}
    for action in session["actions"]:
        tool = action["tool"]
        if tool not in by_tool:
            by_tool[tool] = {"successes": [], "failures": []}

        if action["success"]:
            by_tool[tool]["successes"].append(action)
        else:
            by_tool[tool]["failures"].append(action)

    patterns = []

    for tool, data in by_tool.items():
        if data["successes"] and data["failures"]:
            pattern = {
                "type": "domain_knowledge",
                "tool": tool,
                "successful_approaches": [
                    {
                        "context": s.get("context", ""),
                        "user_confirmed": s.get("user_confirmed", False)
                    }
                    for s in data["successes"]
                ],
                "failed_approaches": [
                    {"context": f.get("context", "")}
                    for f in data["failures"]
                ],
                "confidence": calculate_confidence(data["successes"], data["failures"]),
                "learnable": True
            }
            patterns.append(pattern)
        elif data["successes"]:
            pattern = {
                "type": "successful_technique",
                "tool": tool,
                "approaches": [s.get("context", "") for s in data["successes"]],
                "confidence": 0.7,
                "learnable": len(data["successes"]) >= 2
            }
            patterns.append(pattern)

    confirmed_patterns = [
        p for p in patterns
        if any(s.get("user_confirmed") for s in p.get("successful_approaches", []))
    ]

    return {
        "session_id": session.get("session_id"),
        "component": "{{skill_name}}",
        "type": "skill",
        "goal": session.get("goal"),
        "total_actions": len(session["actions"]),
        "successes": len(session["successes"]),
        "failures": len(session["failures"]),
        "success_rate": len(session["successes"]) / len(session["actions"]) if session["actions"] else 0,
        "patterns_found": len(patterns),
        "learnable_patterns": len([p for p in patterns if p.get("learnable")]),
        "user_confirmed_patterns": len(confirmed_patterns),
        "patterns": patterns
    }

def calculate_confidence(successes: List, failures: List) -> float:
    """Calculate confidence based on success/failure ratio and confirmations."""
    if not successes:
        return 0.0

    base_confidence = len(successes) / (len(successes) + len(failures))
    confirmed_count = sum(1 for s in successes if s.get("user_confirmed"))
    confirmation_boost = confirmed_count * 0.1
    repetition_boost = min(0.2, (len(successes) - 1) * 0.05)

    return min(0.99, base_confidence + confirmation_boost + repetition_boost)

def extract_to_patterns() -> Dict:
    """Extract learned patterns to main patterns.json."""
    analysis = analyze_session()

    patterns_file = get_component_root() / "learned" / "patterns.json"
    if patterns_file.exists():
        with open(patterns_file, "r", encoding="utf-8") as f:
            patterns_data = json.load(f)
    else:
        patterns_data = {"patterns": [], "learning_stats": {"total_sessions": 0}}

    new_patterns = []
    for p in analysis.get("patterns", []):
        if p.get("learnable") and p.get("confidence", 0) >= 0.7:
            new_pattern = {
                "id": f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(new_patterns)}",
                "type": "context_learned",
                "source": "context_tracker",
                "component": "{{skill_name}}",
                "component_type": "skill",
                "tool": p.get("tool"),
                "description": f"Domain knowledge for {p.get('tool')}",
                "successful_approaches": p.get("successful_approaches", p.get("approaches", [])),
                "failed_approaches": p.get("failed_approaches", []),
                "confidence": p.get("confidence"),
                "learned_at": datetime.now().isoformat(),
                "session_goal": analysis.get("goal"),
                "applied": False
            }
            new_patterns.append(new_pattern)
            patterns_data["patterns"].append(new_pattern)

    patterns_data["learning_stats"]["total_sessions"] = patterns_data["learning_stats"].get("total_sessions", 0) + 1
    patterns_data["learning_stats"]["last_extraction"] = datetime.now().isoformat()

    with open(patterns_file, "w", encoding="utf-8") as f:
        json.dump(patterns_data, f, indent=2, ensure_ascii=False)

    return {
        "extraction_complete": True,
        "new_patterns_added": len(new_patterns),
        "total_patterns": len(patterns_data["patterns"]),
        "patterns": new_patterns
    }

def clear_session() -> Dict:
    """Clear current session tracking."""
    session_file = get_session_file()
    if session_file.exists():
        session_file.unlink()
    return {"cleared": True}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Action required",
            "usage": {
                "track": "track <tool> <result> <success:true/false> [context]",
                "confirm": "confirm <positive/negative/correction> [details]",
                "goal": "goal <description>",
                "analyze": "analyze",
                "extract": "extract",
                "clear": "clear"
            }
        }, indent=2))
        sys.exit(1)

    action = sys.argv[1]

    if action == "track":
        if len(sys.argv) < 5:
            result = {"error": "track requires: tool, result, success"}
        else:
            tool = sys.argv[2]
            result_text = sys.argv[3]
            success = sys.argv[4].lower() in ("true", "1", "yes", "success")
            context = sys.argv[5] if len(sys.argv) > 5 else ""
            result = track_action(tool, result_text, success, context)

    elif action == "confirm":
        conf_type = sys.argv[2] if len(sys.argv) > 2 else "positive"
        details = sys.argv[3] if len(sys.argv) > 3 else ""
        result = track_user_confirmation(conf_type, details)

    elif action == "goal":
        if len(sys.argv) < 3:
            result = {"error": "goal requires description"}
        else:
            result = set_goal(" ".join(sys.argv[2:]))

    elif action == "analyze":
        result = analyze_session()

    elif action == "extract":
        result = extract_to_patterns()

    elif action == "clear":
        result = clear_session()

    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
