# Context-Aware Learning

Success-based self-learning system that tracks dialog context to learn only from successful approaches.

## Overview

Traditional learning extracts patterns from all actions. Context-aware learning distinguishes between:
- **Successes**: Actions that achieved the intended goal
- **Failures**: Actions that did not work or caused errors
- **User confirmations**: Explicit feedback that boosts confidence

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT-AWARE LEARNING FLOW                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dialog Starts                                                  │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                               │
│  │ SessionStart│ → Clear previous context                      │
│  │    Hook     │ → Check for patterns to apply                 │
│  └─────────────┘                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                               │
│  │ Tool Call   │ ◄─────────────────────────────┐               │
│  │  Executed   │                               │               │
│  └─────────────┘                               │               │
│       │                                        │               │
│       ▼                                        │               │
│  ┌─────────────┐                               │               │
│  │PostToolUse  │                               │               │
│  │    Hook     │                               │               │
│  └─────────────┘                               │               │
│       │                                        │               │
│       ▼                                        │               │
│  ┌─────────────────────────────┐               │               │
│  │ context_tracker.py track    │               │               │
│  │ - Tool name                 │               │               │
│  │ - Result (truncated)        │               │               │
│  │ - Success/Failure           │───────────────┘               │
│  │ - Context                   │                               │
│  └─────────────────────────────┘                               │
│       │                                                         │
│       ▼ (Dialog continues...)                                   │
│                                                                 │
│  Dialog Ends                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                               │
│  │  Stop Hook  │                                               │
│  └─────────────┘                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────┐                               │
│  │ context_tracker.py analyze  │                               │
│  │ - Group by tool             │                               │
│  │ - Calculate success rates   │                               │
│  │ - Identify patterns         │                               │
│  └─────────────────────────────┘                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────┐                               │
│  │ context_tracker.py extract  │                               │
│  │ - Filter high-confidence    │                               │
│  │ - Save to patterns.json     │                               │
│  │ - Mark as context_learned   │                               │
│  └─────────────────────────────┘                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Example Scenario

**Goal**: Test API and get response

```
Session Start
├── [1] Bash: curl api.example.com → ERROR (connection refused)
│       ↳ Tracked as FAILURE
├── [2] Bash: curl api.example.com:8080 → ERROR (404)
│       ↳ Tracked as FAILURE
├── [3] Read: docs/api.md → SUCCESS (found correct endpoint)
│       ↳ Tracked as SUCCESS
├── [4] Bash: curl api.example.com:8080/v1/status → SUCCESS (200 OK)
│       ↳ Tracked as SUCCESS
└── User: "Great, that worked!"
        ↳ Confirmation tracked → Boosts [4] confidence

Session Analysis:
- Tool "Bash" has both successes and failures
- Successful approach: Read docs first, then use correct endpoint
- Failed approach: Guessing endpoints without checking docs

Learned Pattern:
{
  "type": "context_learned",
  "tool": "Bash",
  "description": "Read documentation before calling APIs",
  "successful_approaches": [
    {"context": "Read docs first, use /v1/status endpoint"}
  ],
  "failed_approaches": [
    {"context": "Guessed root endpoint"},
    {"context": "Guessed without port"}
  ],
  "confidence": 0.85,
  "user_confirmed": true
}
```

## Confidence Calculation

```python
base_confidence = successes / (successes + failures)

# Boost for user confirmations (+10% each)
confirmation_boost = confirmed_count * 0.1

# Boost for multiple successes (+5% each, max 20%)
repetition_boost = min(0.2, (success_count - 1) * 0.05)

final_confidence = min(0.99, base_confidence + confirmation_boost + repetition_boost)
```

| Scenario | Base | Confirmations | Repetitions | Final |
|----------|------|---------------|-------------|-------|
| 1 success, 0 failures | 1.0 | 0 | 0 | 1.0 |
| 2 successes, 1 failure | 0.67 | 0 | 0.05 | 0.72 |
| 3 successes, 1 failure, 1 confirmed | 0.75 | 0.1 | 0.1 | 0.95 |

## Thresholds

| Confidence | Action |
|------------|--------|
| ≥ 90% | Auto-apply in future sessions |
| 70-89% | Available for manual review |
| < 70% | Needs more evidence, not saved |

## Files Created

When context tracking is enabled:

```
component/
├── scripts/
│   ├── context_tracker.py    # Main tracking script
│   └── apply_learned.py      # Apply patterns script
├── hooks/
│   └── hooks.json            # With PostToolUse tracking
└── learned/
    ├── patterns.json         # Saved patterns
    └── sessions/             # Session tracking data
        └── session-YYYYMMDD.json
```

## API Reference

### context_tracker.py

```bash
# Track a tool action
python context_tracker.py track <tool> <result> <success> [context]

# Track user confirmation
python context_tracker.py confirm <positive|negative|correction> [details]

# Set session goal
python context_tracker.py goal "Description of what we're trying to achieve"

# Analyze session patterns
python context_tracker.py analyze

# Extract learned patterns to patterns.json
python context_tracker.py extract

# Clear session data
python context_tracker.py clear
```

### Session Data Format

```json
{
  "session_id": "20260203",
  "started": "2026-02-03T10:00:00",
  "goal": "Test API connectivity",
  "actions": [
    {
      "id": "act-1",
      "timestamp": "2026-02-03T10:01:00",
      "tool": "Bash",
      "result_summary": "curl: connection refused",
      "success": false,
      "context": "curl api.example.com"
    },
    {
      "id": "act-2",
      "timestamp": "2026-02-03T10:02:00",
      "tool": "Read",
      "result_summary": "API docs content...",
      "success": true,
      "context": "docs/api.md"
    }
  ],
  "successes": ["act-2", "act-4"],
  "failures": ["act-1", "act-3"],
  "user_confirmations": [
    {
      "timestamp": "2026-02-03T10:05:00",
      "type": "positive",
      "details": "That worked!"
    }
  ]
}
```

## Integration with Self-Learning Pipeline

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│  Context Tracker  │ ──▶ │ Pattern Extractor │ ──▶ │  Pattern Applier  │
│  (tracks actions) │     │  (analyzes)       │     │  (applies)        │
└───────────────────┘     └───────────────────┘     └───────────────────┘
        │                         │                         │
        ▼                         ▼                         ▼
   sessions/              patterns.json             Component improved
   session-*.json         (high confidence)         automatically
```

## Best Practices

1. **Set a Goal**: Call `goal` command at session start for better pattern context
2. **Be Specific**: Provide context when tracking for better pattern matching
3. **Confirm Success**: User confirmations significantly boost confidence
4. **Regular Reviews**: Run `/uc:status patterns` to see what's been learned
5. **Apply Patterns**: Use `/uc:improve apply` to apply learned patterns

## Antipattern Storage

Failed approaches are stored as antipatterns with:
- What was attempted
- Why it failed
- What worked instead

These antipatterns help the component avoid repeating mistakes.

```json
{
  "antipattern": {
    "tool": "Bash",
    "what_not_to_do": "Guess API endpoints without reading documentation",
    "why": "Results in connection errors and 404s",
    "better_approach": "Read API documentation first to find correct endpoints",
    "learned_from_session": "20260203"
  }
}
```
