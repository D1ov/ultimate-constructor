#!/usr/bin/env python3
"""
Pipeline Orchestrator for {{agent_name}}

Coordinates the full organization pipeline:
Executive → Quality → Security → Evolution

Usage: python orchestrator.py <action> [args]
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Pipeline stages
PIPELINE = {
    "executive": ["architect", "planner", "executor", "delegator"],
    "quality": ["tester", "reviewer", "qa", "validator"],
    "security": ["pentester", "auditor", "compliance"],
    "evolution": ["refactor", "optimizer", "learner", "finalizer"]
}

def get_learned_dir() -> Path:
    """Get the learned directory."""
    return Path(__file__).parent.parent / "learned"

def load_state() -> Dict:
    """Load pipeline state."""
    state_file = get_learned_dir() / "pipeline-state.json"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"runs": [], "current": None}

def save_state(state: Dict):
    """Save pipeline state."""
    state_file = get_learned_dir() / "pipeline-state.json"
    state_file.parent.mkdir(exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def start_pipeline(task: str) -> Dict:
    """Start a new pipeline run."""
    state = load_state()

    run = {
        "id": f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "task": task,
        "started": datetime.now().isoformat(),
        "stages_completed": [],
        "current_stage": "executive",
        "current_agent": "architect",
        "status": "in_progress"
    }

    state["current"] = run
    state["runs"].append(run)
    save_state(state)

    return run

def advance_pipeline() -> Dict:
    """Advance to next stage/agent."""
    state = load_state()
    current = state.get("current")

    if not current:
        return {"error": "No active pipeline"}

    # Find next agent
    stage = current["current_stage"]
    agent_idx = PIPELINE[stage].index(current["current_agent"])

    if agent_idx < len(PIPELINE[stage]) - 1:
        # Next agent in same stage
        current["current_agent"] = PIPELINE[stage][agent_idx + 1]
    else:
        # Move to next stage
        current["stages_completed"].append(stage)
        stages = list(PIPELINE.keys())
        stage_idx = stages.index(stage)

        if stage_idx < len(stages) - 1:
            next_stage = stages[stage_idx + 1]
            current["current_stage"] = next_stage
            current["current_agent"] = PIPELINE[next_stage][0]
        else:
            # Pipeline complete
            current["status"] = "completed"
            current["completed"] = datetime.now().isoformat()

    state["current"] = current
    save_state(state)

    return current

def get_status() -> Dict:
    """Get current pipeline status."""
    state = load_state()
    current = state.get("current")

    if not current:
        return {"status": "idle", "message": "No active pipeline"}

    return {
        "status": current["status"],
        "current_stage": current.get("current_stage"),
        "current_agent": current.get("current_agent"),
        "completed_stages": current.get("stages_completed", []),
        "task": current.get("task")
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Action required: start|advance|status"}))
        sys.exit(1)

    action = sys.argv[1]

    if action == "start":
        task = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        result = start_pipeline(task)
    elif action == "advance":
        result = advance_pipeline()
    elif action == "status":
        result = get_status()
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
