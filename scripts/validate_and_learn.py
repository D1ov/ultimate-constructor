#!/usr/bin/env python3
"""
Validate component changes and extract learning patterns.
Called by self-learning PostToolUse hooks.

Usage: python validate_and_learn.py <component_name>
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def get_learned_dir(component_name: str) -> Path:
    """Get the learned directory for a component."""
    # Try to find component in NEW/skills/
    base = Path(os.environ.get("CLAUDE_PROJECT_ROOT", "."))
    component_dir = base / "NEW" / "skills" / component_name

    if component_dir.exists():
        learned_dir = component_dir / "learned"
        learned_dir.mkdir(exist_ok=True)
        return learned_dir

    # Fallback to plugin root
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "."))
    learned_dir = plugin_root / "learned"
    learned_dir.mkdir(exist_ok=True)
    return learned_dir

def load_patterns(learned_dir: Path) -> dict:
    """Load existing patterns."""
    patterns_file = learned_dir / "patterns.json"
    if patterns_file.exists():
        with open(patterns_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"patterns": [], "last_updated": None}

def save_patterns(learned_dir: Path, data: dict):
    """Save patterns to file."""
    patterns_file = learned_dir / "patterns.json"
    data["last_updated"] = datetime.now().isoformat()
    with open(patterns_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def record_edit(component_name: str, context: dict = None):
    """Record that an edit was made for learning purposes."""
    learned_dir = get_learned_dir(component_name)
    data = load_patterns(learned_dir)

    # Add edit event
    edit_event = {
        "type": "edit",
        "timestamp": datetime.now().isoformat(),
        "component": component_name
    }

    if context:
        edit_event["context"] = context

    if "edit_history" not in data:
        data["edit_history"] = []

    data["edit_history"].append(edit_event)

    # Keep only last 100 edits
    data["edit_history"] = data["edit_history"][-100:]

    save_patterns(learned_dir, data)

    return {"status": "recorded", "component": component_name}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Component name required"}))
        sys.exit(1)

    component_name = sys.argv[1]

    try:
        result = record_edit(component_name)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
