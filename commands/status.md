---
name: status
description: Show learned patterns, quality metrics, and component statistics
args:
  - name: detail
    description: "Detail level: summary, full, patterns, metrics"
    required: false
    default: summary
examples:
  - "/uc:status"
  - "/uc:status full"
  - "/uc:status patterns"
  - "/uc:status metrics"
model: haiku
tools: Read, Glob, Grep
---

# Status Command

Display Ultimate Constructor statistics, learned patterns, and quality metrics.

## Views

### Summary (default)

```
╔══════════════════════════════════════════════════════════════╗
║                ULTIMATE CONSTRUCTOR STATUS                    ║
╠══════════════════════════════════════════════════════════════╣
║  Components Created: 12                                       ║
║  ├── Skills: 8                                               ║
║  ├── Agents: 3                                               ║
║  └── Hooks: 1                                                ║
║                                                              ║
║  Patterns Learned: 23                                        ║
║  Average Quality Score: 84/100                               ║
║  Total Refactor Iterations: 7                                ║
║                                                              ║
║  Last Activity: 2026-02-03 14:30                             ║
╚══════════════════════════════════════════════════════════════╝
```

### Full

Shows complete details:
- All created components with scores
- All learned patterns
- Quality metrics over time
- Improvement history

### Patterns

```
Learned Patterns (23 total)

🟢 Ready to Apply (high confidence ≥90%):
  • api-error-handling (95%) - Will apply automatically
  • yaml-frontmatter-fix (91%) - Will apply automatically

🟡 Available (medium confidence 70-89%):
  • git-commit-flow (88%)
  • test-debug-cycle (85%)
  • vague-description (87%)

🔴 Needs More Evidence (<70%):
  • new-pattern-1 (62%)

By Category:
  Workflows: 8
  Validations: 6
  Antipatterns: 5
  Fixes: 4

Run: /uc:improve apply - to apply high-confidence patterns
```

### Applying Learned Patterns

```
/uc:status apply
```

Shows pending improvements and applies them:

```
╔══════════════════════════════════════════════════════════════╗
║                 APPLYING LEARNED PATTERNS                     ║
╠══════════════════════════════════════════════════════════════╣
║  High-confidence patterns available: 5                        ║
║                                                               ║
║  [1] api-error-handling (95%)                                ║
║      → Will improve error handling in 3 agents               ║
║                                                               ║
║  [2] yaml-frontmatter-fix (91%)                              ║
║      → Will update validation in constructor-tester          ║
║                                                               ║
║  Apply all? [Y/n/preview]                                    ║
╚══════════════════════════════════════════════════════════════╝
```

### Metrics

```
Quality Metrics

Score Distribution:
  90-100: ████████░░ 8 components
  80-89:  ██████░░░░ 6 components
  70-79:  ██░░░░░░░░ 2 components
  <70:    ░░░░░░░░░░ 0 components

Average Scores by Type:
  Skills: 86/100
  Agents: 82/100
  Hooks:  79/100

Refactor Success Rate: 94%
First-Pass Success Rate: 67%

Most Common Issues:
  1. Missing trigger phrases (12 occurrences)
  2. No boundaries section (8 occurrences)
  3. Missing examples (7 occurrences)
```

## Data Sources

Status reads from:
- `learned/patterns.json` - Extracted patterns
- `learned/improvements/` - Applied improvements
- `learned/test-results/` - Test history
- `CHANGELOG.md` - Creation history

## Export

Export status data:
```
/uc:status full > status-report.md
```

## Maintenance

### Clear Patterns
Remove low-confidence patterns:
```
Delete patterns with confidence < 50%? [y/N]
```

### Archive Old Data
Move old test results to archive:
```
Archive test results older than 30 days? [y/N]
```

## Integration

Status can be queried programmatically:
```bash
claude --command "/uc:status metrics" --format json
```

Returns:
```json
{
  "components_created": 12,
  "patterns_learned": 23,
  "average_score": 84,
  "by_type": {
    "skills": {"count": 8, "avg_score": 86},
    "agents": {"count": 3, "avg_score": 82},
    "hooks": {"count": 1, "avg_score": 79}
  }
}
```
