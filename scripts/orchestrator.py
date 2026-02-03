#!/usr/bin/env python3
"""
Ultimate Constructor Pipeline Orchestrator

Coordinates the full self-* pipeline for component creation:
Executive Layer → Quality Layer → Security Layer → Evolution Layer

Usage:
  python orchestrator.py start <task>    - Start new pipeline
  python orchestrator.py advance         - Advance to next stage
  python orchestrator.py status          - Get current status
  python orchestrator.py report          - Generate pipeline report
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Full Organization Pipeline
PIPELINE = {
    "executive": {
        "agents": ["architect", "planner", "executor", "delegator"],
        "purpose": "Design and execute component creation"
    },
    "quality": {
        "agents": ["tester", "reviewer", "qa", "validator"],
        "purpose": "Validate and score component quality"
    },
    "security": {
        "agents": ["pentester", "auditor", "compliance"],
        "purpose": "Security testing and compliance"
    },
    "evolution": {
        "agents": ["refactor", "optimizer", "learner", "finalizer", "acceptance"],
        "purpose": "Improve and finalize component"
    }
}

# Quality thresholds
THRESHOLDS = {
    "pass": 80,
    "excellent": 90,
    "critical_fail": 60
}

def get_data_dir() -> Path:
    """Get the data directory for pipeline state."""
    data_dir = Path(__file__).parent.parent / "learned" / "pipeline"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def load_state() -> Dict:
    """Load pipeline state."""
    state_file = get_data_dir() / "state.json"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"runs": [], "current": None, "stats": {"total_runs": 0, "successful": 0, "failed": 0}}

def save_state(state: Dict):
    """Save pipeline state."""
    state_file = get_data_dir() / "state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def start_pipeline(task: str, component_type: str = "unknown") -> Dict:
    """Start a new pipeline run."""
    state = load_state()

    run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    run = {
        "id": run_id,
        "task": task,
        "component_type": component_type,
        "started": datetime.now().isoformat(),
        "current_layer": "executive",
        "current_agent": "architect",
        "completed_layers": [],
        "completed_agents": [],
        "scores": {},
        "issues": [],
        "refactor_count": 0,
        "status": "in_progress"
    }

    state["current"] = run
    state["runs"].append(run)
    state["stats"]["total_runs"] += 1
    save_state(state)

    return {
        "status": "started",
        "run_id": run_id,
        "first_agent": "constructor-architect",
        "message": f"Pipeline started for: {task}"
    }

def advance_pipeline(agent_result: Optional[Dict] = None) -> Dict:
    """Advance to next stage in pipeline."""
    state = load_state()
    current = state.get("current")

    if not current:
        return {"error": "No active pipeline", "suggestion": "Run 'start' first"}

    # Record agent result if provided
    if agent_result:
        current["scores"][current["current_agent"]] = agent_result.get("score", 100)
        if agent_result.get("issues"):
            current["issues"].extend(agent_result["issues"])

    # Mark current agent as completed
    current["completed_agents"].append(current["current_agent"])

    # Check for refactor loop
    if current["current_agent"] == "reviewer":
        score = current["scores"].get("reviewer", 100)
        if score < THRESHOLDS["pass"] and current["refactor_count"] < 3:
            current["refactor_count"] += 1
            current["current_layer"] = "evolution"
            current["current_agent"] = "refactor"
            save_state(state)
            return {
                "status": "refactor_loop",
                "reason": f"Score {score} < {THRESHOLDS['pass']}",
                "iteration": current["refactor_count"],
                "next_agent": "constructor-refactor"
            }

    # Find next agent
    layer = current["current_layer"]
    agents = PIPELINE[layer]["agents"]
    agent_idx = agents.index(current["current_agent"]) if current["current_agent"] in agents else -1

    if agent_idx < len(agents) - 1:
        # Next agent in same layer
        current["current_agent"] = agents[agent_idx + 1]
        save_state(state)
        return {
            "status": "advanced",
            "layer": layer,
            "next_agent": f"constructor-{current['current_agent']}"
        }
    else:
        # Move to next layer
        current["completed_layers"].append(layer)
        layers = list(PIPELINE.keys())
        layer_idx = layers.index(layer)

        if layer_idx < len(layers) - 1:
            next_layer = layers[layer_idx + 1]
            current["current_layer"] = next_layer
            current["current_agent"] = PIPELINE[next_layer]["agents"][0]
            save_state(state)
            return {
                "status": "layer_complete",
                "completed_layer": layer,
                "next_layer": next_layer,
                "next_agent": f"constructor-{current['current_agent']}"
            }
        else:
            # Pipeline complete
            current["status"] = "completed"
            current["completed"] = datetime.now().isoformat()
            current["final_score"] = calculate_final_score(current["scores"])

            if current["final_score"] >= THRESHOLDS["pass"]:
                state["stats"]["successful"] += 1
            else:
                state["stats"]["failed"] += 1

            save_state(state)
            return {
                "status": "completed",
                "final_score": current["final_score"],
                "passed": current["final_score"] >= THRESHOLDS["pass"],
                "summary": generate_summary(current)
            }

def calculate_final_score(scores: Dict) -> int:
    """Calculate weighted final score."""
    weights = {
        "tester": 0.20,
        "reviewer": 0.25,
        "qa": 0.15,
        "validator": 0.10,
        "pentester": 0.15,
        "compliance": 0.10,
        "learner": 0.05
    }

    total_weight = 0
    weighted_sum = 0

    for agent, weight in weights.items():
        if agent in scores:
            weighted_sum += scores[agent] * weight
            total_weight += weight

    if total_weight == 0:
        return 100

    return int(weighted_sum / total_weight)

def generate_summary(run: Dict) -> Dict:
    """Generate pipeline run summary."""
    return {
        "task": run["task"],
        "component_type": run["component_type"],
        "duration": calculate_duration(run.get("started"), run.get("completed")),
        "layers_completed": run["completed_layers"],
        "agents_invoked": len(run["completed_agents"]),
        "refactor_iterations": run["refactor_count"],
        "issues_found": len(run["issues"]),
        "final_score": run.get("final_score", 0)
    }

def calculate_duration(start: str, end: str) -> str:
    """Calculate duration between timestamps."""
    if not start or not end:
        return "unknown"

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    delta = end_dt - start_dt

    seconds = int(delta.total_seconds())
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"

def get_status() -> Dict:
    """Get current pipeline status."""
    state = load_state()
    current = state.get("current")

    if not current:
        return {
            "status": "idle",
            "stats": state["stats"],
            "recent_runs": len(state["runs"])
        }

    return {
        "status": current["status"],
        "run_id": current["id"],
        "task": current["task"],
        "current_layer": current["current_layer"],
        "current_agent": current["current_agent"],
        "progress": {
            "layers_completed": current["completed_layers"],
            "agents_completed": len(current["completed_agents"]),
            "refactor_iterations": current["refactor_count"]
        },
        "scores": current["scores"],
        "issues": len(current["issues"])
    }

def generate_report() -> Dict:
    """Generate full pipeline report."""
    state = load_state()

    return {
        "generated": datetime.now().isoformat(),
        "statistics": state["stats"],
        "success_rate": (
            state["stats"]["successful"] / state["stats"]["total_runs"] * 100
            if state["stats"]["total_runs"] > 0 else 0
        ),
        "recent_runs": [
            {
                "id": run["id"],
                "task": run["task"],
                "status": run["status"],
                "score": run.get("final_score", "N/A")
            }
            for run in state["runs"][-10:]
        ],
        "pipeline_structure": PIPELINE,
        "thresholds": THRESHOLDS
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Action required",
            "actions": ["start <task>", "advance", "status", "report"]
        }, indent=2))
        sys.exit(1)

    action = sys.argv[1]

    if action == "start":
        task = sys.argv[2] if len(sys.argv) > 2 else "component creation"
        comp_type = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        result = start_pipeline(task, comp_type)
    elif action == "advance":
        agent_result = None
        if len(sys.argv) > 2:
            try:
                agent_result = json.loads(sys.argv[2])
            except json.JSONDecodeError:
                pass
        result = advance_pipeline(agent_result)
    elif action == "status":
        result = get_status()
    elif action == "report":
        result = generate_report()
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
