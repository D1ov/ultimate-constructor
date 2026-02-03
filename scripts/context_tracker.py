#!/usr/bin/env python3
"""
Context Tracker for Success-Based Self-Learning

Tracks tool calls and their outcomes during a session to learn
only from successful approaches. Failed attempts are stored
as "what not to do" (antipatterns).

Includes review/accept flow for quality control.

Usage:
  python context_tracker.py track <tool> <result> <success>
  python context_tracker.py confirm <positive/negative/correction> [details]
  python context_tracker.py goal <description>
  python context_tracker.py analyze
  python context_tracker.py review              # Review patterns before saving
  python context_tracker.py accept              # Accept reviewed patterns
  python context_tracker.py extract             # Extract without review (auto)
  python context_tracker.py extract --review    # Extract with review/accept
  python context_tracker.py clear
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

def get_plugin_root() -> Path:
    """Get plugin root directory."""
    return Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).parent.parent))

def get_session_file() -> Path:
    """Get current session tracking file."""
    learned_dir = get_plugin_root() / "learned" / "sessions"
    learned_dir.mkdir(parents=True, exist_ok=True)

    # Use session ID from environment or create one
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
        "started": datetime.now().isoformat(),
        "goal": None,
        "context": [],
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
        "result_summary": result[:500],  # Truncate long results
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
        "type": confirmation_type,  # "positive", "negative", "correction"
        "details": details,
        "related_actions": session["actions"][-3:] if session["actions"] else []  # Last 3 actions
    }

    session["user_confirmations"].append(confirmation)

    # If positive confirmation, boost confidence of recent successes
    if confirmation_type == "positive" and session["successes"]:
        # Mark last success as confirmed
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

    # Group actions by tool
    by_tool = {}
    for action in session["actions"]:
        tool = action["tool"]
        if tool not in by_tool:
            by_tool[tool] = {"successes": [], "failures": []}

        if action["success"]:
            by_tool[tool]["successes"].append(action)
        else:
            by_tool[tool]["failures"].append(action)

    # Find patterns
    patterns = []

    for tool, data in by_tool.items():
        if data["successes"] and data["failures"]:
            # We have both - can learn what works vs doesn't
            pattern = {
                "type": "tool_usage",
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
            # Only successes - good pattern but less contrast
            pattern = {
                "type": "successful_approach",
                "tool": tool,
                "approaches": [s.get("context", "") for s in data["successes"]],
                "confidence": 0.7,  # Lower confidence without failure contrast
                "learnable": len(data["successes"]) >= 2  # Need at least 2 successes
            }
            patterns.append(pattern)

    # Check for user confirmations
    confirmed_patterns = [
        p for p in patterns
        if any(s.get("user_confirmed") for s in p.get("successful_approaches", []))
    ]

    return {
        "session_id": session.get("session_id"),
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

    # Boost for user confirmations
    confirmed_count = sum(1 for s in successes if s.get("user_confirmed"))
    confirmation_boost = confirmed_count * 0.1

    # Boost for multiple successes
    repetition_boost = min(0.2, (len(successes) - 1) * 0.05)

    return min(0.99, base_confidence + confirmation_boost + repetition_boost)

def extract_to_patterns() -> Dict:
    """Extract learned patterns to main patterns.json."""
    analysis = analyze_session()

    # Load existing patterns
    patterns_file = get_plugin_root() / "learned" / "patterns.json"
    if patterns_file.exists():
        with open(patterns_file, "r", encoding="utf-8") as f:
            patterns_data = json.load(f)
    else:
        patterns_data = {"patterns": [], "learning_stats": {"total_sessions": 0}}

    # Add learnable patterns
    new_patterns = []
    for p in analysis.get("patterns", []):
        if p.get("learnable") and p.get("confidence", 0) >= 0.7:
            new_pattern = {
                "id": f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(new_patterns)}",
                "type": "context_learned",
                "source": "context_tracker",
                "tool": p.get("tool"),
                "description": f"Successful {p.get('tool')} usage pattern",
                "successful_approaches": p.get("successful_approaches", p.get("approaches", [])),
                "failed_approaches": p.get("failed_approaches", []),
                "confidence": p.get("confidence"),
                "learned_at": datetime.now().isoformat(),
                "session_goal": analysis.get("goal"),
                "applied": False
            }
            new_patterns.append(new_pattern)
            patterns_data["patterns"].append(new_pattern)

    # Update stats
    patterns_data["learning_stats"]["total_sessions"] = patterns_data["learning_stats"].get("total_sessions", 0) + 1
    patterns_data["learning_stats"]["last_extraction"] = datetime.now().isoformat()

    # Save
    with open(patterns_file, "w", encoding="utf-8") as f:
        json.dump(patterns_data, f, indent=2, ensure_ascii=False)

    return {
        "extraction_complete": True,
        "new_patterns_added": len(new_patterns),
        "total_patterns": len(patterns_data["patterns"]),
        "patterns": new_patterns
    }

def review_patterns(patterns: List[Dict]) -> Dict:
    """Review patterns for quality before acceptance.

    Scores each pattern on:
    - Evidence quality (successful uses, user confirmations)
    - Reproducibility (clear steps, context independence)
    - Reusability (generalizability, trigger clarity)
    """
    reviewed = []

    for p in patterns:
        # Calculate evidence quality score
        evidence_score = 0
        success_count = len(p.get("successful_approaches", p.get("approaches", [])))
        has_confirmation = any(
            s.get("user_confirmed")
            for s in p.get("successful_approaches", [])
        )

        evidence_score += min(40, success_count * 15)  # Up to 40 for successes
        evidence_score += 30 if has_confirmation else 0  # 30 for user confirmation
        evidence_score += 20 if p.get("failed_approaches") else 0  # 20 for contrast
        evidence_score += 10 if success_count >= 3 else 0  # 10 for repetition

        # Reproducibility score (simplified)
        reproducibility_score = 70  # Base score
        if p.get("context"):
            reproducibility_score += 15
        if success_count >= 2:
            reproducibility_score += 15

        # Reusability score (simplified)
        reusability_score = 75  # Base score
        if p.get("tool"):
            reusability_score += 15
        if p.get("description"):
            reusability_score += 10

        # Calculate overall score
        overall = int(
            (evidence_score * 0.4) +
            (reproducibility_score * 0.3) +
            (reusability_score * 0.3)
        )

        # Make recommendation
        if overall >= 85:
            recommendation = "approve"
        elif overall >= 70:
            recommendation = "approve_with_notes"
        elif overall >= 50:
            recommendation = "needs_more_evidence"
        else:
            recommendation = "reject"

        reviewed.append({
            "pattern": p,
            "review": {
                "evidence_score": evidence_score,
                "reproducibility_score": reproducibility_score,
                "reusability_score": reusability_score,
                "overall_score": overall,
                "recommendation": recommendation,
                "reviewed_at": datetime.now().isoformat()
            }
        })

    # Summary
    approved = len([r for r in reviewed if r["review"]["recommendation"].startswith("approve")])
    rejected = len([r for r in reviewed if r["review"]["recommendation"] == "reject"])
    pending = len(reviewed) - approved - rejected

    return {
        "review_complete": True,
        "patterns_reviewed": len(reviewed),
        "approved": approved,
        "rejected": rejected,
        "pending": pending,
        "reviewed_patterns": reviewed
    }

def accept_patterns(reviewed_patterns: List[Dict], min_score: int = 70) -> Dict:
    """Accept reviewed patterns that meet the minimum score threshold.

    Only patterns with score >= min_score will be accepted and saved.
    """
    accepted = []
    rejected = []

    for rp in reviewed_patterns:
        score = rp.get("review", {}).get("overall_score", 0)
        recommendation = rp.get("review", {}).get("recommendation", "reject")

        if score >= min_score and recommendation != "reject":
            pattern = rp["pattern"].copy()
            pattern["reviewed"] = True
            pattern["review_score"] = score
            pattern["accepted"] = True
            pattern["accepted_at"] = datetime.now().isoformat()
            pattern["acceptance_notes"] = f"Score: {score}/100, Recommendation: {recommendation}"
            accepted.append(pattern)
        else:
            pattern = rp["pattern"].copy()
            pattern["reviewed"] = True
            pattern["review_score"] = score
            pattern["accepted"] = False
            pattern["rejection_reason"] = f"Score {score} below threshold {min_score}" if score < min_score else recommendation
            rejected.append(pattern)

    return {
        "acceptance_complete": True,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "accepted_patterns": accepted,
        "rejected_patterns": rejected
    }

def extract_with_review() -> Dict:
    """Extract patterns with review and acceptance flow.

    1. Analyze session to find patterns
    2. Review each pattern for quality
    3. Accept only high-quality patterns
    4. Save accepted patterns to patterns.json
    """
    # Step 1: Analyze
    analysis = analyze_session()
    learnable = [p for p in analysis.get("patterns", []) if p.get("learnable")]

    if not learnable:
        return {
            "extraction_complete": True,
            "with_review": True,
            "patterns_found": 0,
            "patterns_accepted": 0,
            "message": "No learnable patterns found in session"
        }

    # Step 2: Review
    review_result = review_patterns(learnable)

    # Step 3: Accept
    accept_result = accept_patterns(review_result["reviewed_patterns"])

    # Step 4: Save accepted patterns
    if accept_result["accepted_patterns"]:
        patterns_file = get_plugin_root() / "learned" / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file, "r", encoding="utf-8") as f:
                patterns_data = json.load(f)
        else:
            patterns_data = {"patterns": [], "learning_stats": {"total_sessions": 0}}

        # Add accepted patterns with full metadata
        for p in accept_result["accepted_patterns"]:
            new_pattern = {
                "id": f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(patterns_data['patterns'])}",
                "type": "context_learned",
                "source": "context_tracker_reviewed",
                "tool": p.get("tool"),
                "description": f"Reviewed: {p.get('tool')} usage pattern",
                "successful_approaches": p.get("successful_approaches", p.get("approaches", [])),
                "failed_approaches": p.get("failed_approaches", []),
                "confidence": p.get("confidence"),
                "reviewed": True,
                "review_score": p.get("review_score"),
                "accepted": True,
                "accepted_at": p.get("accepted_at"),
                "learned_at": datetime.now().isoformat(),
                "session_goal": analysis.get("goal"),
                "applied": False
            }
            patterns_data["patterns"].append(new_pattern)

        # Update stats
        patterns_data["learning_stats"]["total_sessions"] = patterns_data["learning_stats"].get("total_sessions", 0) + 1
        patterns_data["learning_stats"]["last_reviewed_extraction"] = datetime.now().isoformat()
        patterns_data["learning_stats"]["patterns_reviewed"] = patterns_data["learning_stats"].get("patterns_reviewed", 0) + review_result["patterns_reviewed"]
        patterns_data["learning_stats"]["patterns_accepted"] = patterns_data["learning_stats"].get("patterns_accepted", 0) + accept_result["accepted_count"]

        with open(patterns_file, "w", encoding="utf-8") as f:
            json.dump(patterns_data, f, indent=2, ensure_ascii=False)

    return {
        "extraction_complete": True,
        "with_review": True,
        "patterns_found": len(learnable),
        "patterns_reviewed": review_result["patterns_reviewed"],
        "patterns_accepted": accept_result["accepted_count"],
        "patterns_rejected": accept_result["rejected_count"],
        "review_summary": {
            "approved": review_result["approved"],
            "pending": review_result["pending"],
            "rejected": review_result["rejected"]
        },
        "accepted_patterns": [
            {
                "tool": p.get("tool"),
                "confidence": p.get("confidence"),
                "review_score": p.get("review_score")
            }
            for p in accept_result["accepted_patterns"]
        ],
        "rejected_patterns": [
            {
                "tool": p.get("tool"),
                "reason": p.get("rejection_reason")
            }
            for p in accept_result["rejected_patterns"]
        ]
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
                "review": "review (analyze and review patterns)",
                "accept": "accept (accept reviewed patterns)",
                "extract": "extract [--review] (extract patterns, optionally with review)",
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

    elif action == "review":
        # Analyze and review patterns
        analysis = analyze_session()
        learnable = [p for p in analysis.get("patterns", []) if p.get("learnable")]
        if learnable:
            result = review_patterns(learnable)
        else:
            result = {"review_complete": True, "patterns_reviewed": 0, "message": "No learnable patterns"}

    elif action == "accept":
        # Accept patterns (expects review data in session or re-reviews)
        analysis = analyze_session()
        learnable = [p for p in analysis.get("patterns", []) if p.get("learnable")]
        if learnable:
            review_result = review_patterns(learnable)
            min_score = int(sys.argv[2]) if len(sys.argv) > 2 else 70
            result = accept_patterns(review_result["reviewed_patterns"], min_score)
        else:
            result = {"acceptance_complete": True, "accepted_count": 0, "message": "No patterns to accept"}

    elif action == "extract":
        # Check for --review flag
        if len(sys.argv) > 2 and sys.argv[2] == "--review":
            result = extract_with_review()
        else:
            result = extract_to_patterns()

    elif action == "clear":
        result = clear_session()

    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
