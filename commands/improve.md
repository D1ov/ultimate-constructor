---
name: improve
description: Analyze and improve existing Claude Code components with full organization analysis
args:
  - name: target
    description: "Path to component, 'apply' for patterns, or 'analyze' for deep analysis"
    required: false
  - name: options
    description: "--auto, --preview, --full, --plan-only"
    required: false
examples:
  - "/uc:improve ./my-skill"
  - "/uc:improve agents/code-reviewer.md"
  - "/uc:improve apply"
  - "/uc:improve apply --auto"
  - "/uc:improve analyze ./my-agent"
  - "/uc:improve analyze ./my-skill --full"
model: sonnet
tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Improve Component Command

Analyze and improve existing Claude Code components using the full self-* organization.

## Modes

### Mode 1: Improve Specific Component
```
/uc:improve ./my-skill
/uc:improve agents/code-reviewer.md
```

### Mode 2: Apply Learned Patterns
```
/uc:improve apply              # Interactive - asks before applying
/uc:improve apply --auto       # Auto-apply high-confidence patterns
/uc:improve apply --preview    # Preview only, don't apply
```

### Mode 3: Deep Analysis (NEW)
```
/uc:improve analyze ./my-agent           # Full organization analysis
/uc:improve analyze ./my-skill --full    # Maximum depth analysis
/uc:improve analyze ./my-plugin --plan-only  # Only create plan, don't apply
```

## Deep Analysis Mode

When using `analyze`, the full organization is deployed to examine the component:

```
/uc:improve analyze ./my-agent

╔══════════════════════════════════════════════════════════════════╗
║                 FULL ORGANIZATION ANALYSIS                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Component: my-agent                                             ║
║  Type: Agent                                                     ║
║  Location: agents/my-agent.md                                    ║
║                                                                  ║
║  Deploying analysis organization...                              ║
║                                                                  ║
║  ┌─────────────────────────────────────────────────────────────┐ ║
║  │ EXECUTIVE LAYER                                              │ ║
║  │ ├── constructor-architect → Analyzing structure             │ ║
║  │ └── constructor-planner → Creating improvement plan         │ ║
║  ├─────────────────────────────────────────────────────────────┤ ║
║  │ QUALITY LAYER                                                │ ║
║  │ ├── constructor-tester → Running validation tests           │ ║
║  │ ├── constructor-reviewer → Quality analysis                 │ ║
║  │ ├── constructor-qa → Comprehensive QA check                 │ ║
║  │ └── constructor-validator → Schema validation               │ ║
║  ├─────────────────────────────────────────────────────────────┤ ║
║  │ SECURITY LAYER                                               │ ║
║  │ ├── constructor-pentester → Security testing                │ ║
║  │ ├── constructor-auditor → Audit trail review                │ ║
║  │ └── constructor-compliance → Standards compliance           │ ║
║  ├─────────────────────────────────────────────────────────────┤ ║
║  │ EVOLUTION LAYER                                              │ ║
║  │ ├── constructor-analyzer → Deep analysis                    │ ║
║  │ ├── constructor-optimizer → Performance optimization        │ ║
║  │ └── constructor-learner → Pattern extraction                │ ║
║  └─────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Analysis Workflow

#### Step 1: Launch Analyzer Agent

**constructor-analyzer** performs deep examination:

```
╔══════════════════════════════════════════════════════════════════╗
║                    DEEP ANALYSIS RESULTS                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STRUCTURE ANALYSIS                                              ║
║  ├── Frontmatter: ✅ Valid YAML                                  ║
║  ├── Sections: ⚠️ Missing "Output Format"                        ║
║  ├── Line count: ✅ 156 lines (under 500)                        ║
║  └── References: ✅ All exist                                    ║
║                                                                  ║
║  CONTENT ANALYSIS                                                ║
║  ├── Description triggers: ⚠️ Too vague (2 specific triggers)   ║
║  ├── Boundaries: ❌ Missing "NOT for:" section                   ║
║  ├── Workflow: ✅ Clear 5-step process                           ║
║  └── Examples: ⚠️ Only 1 example (recommend 3+)                  ║
║                                                                  ║
║  TOOL ANALYSIS                                                   ║
║  ├── Tools defined: Read, Grep, Glob, Bash                      ║
║  ├── Tools restrictive: ⚠️ Bash may be too broad                ║
║  └── Model: sonnet (appropriate for complexity)                  ║
║                                                                  ║
║  INTEGRATION ANALYSIS                                            ║
║  ├── Skills referenced: None                                     ║
║  ├── Hooks defined: None                                         ║
║  └── Self-learning: ❌ Not enabled                               ║
║                                                                  ║
║  QUALITY METRICS                                                 ║
║  ├── Overall Score: 62/100                                       ║
║  ├── Structure: 85/100                                           ║
║  ├── Content: 55/100                                             ║
║  ├── Security: 70/100                                            ║
║  └── Evolution readiness: 30/100                                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

#### Step 2: Generate Improvement Plan

Based on analysis, create prioritized plan:

```
╔══════════════════════════════════════════════════════════════════╗
║                    IMPROVEMENT PLAN                              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Priority 1: CRITICAL (Score Impact: +15)                        ║
║  ┌────────────────────────────────────────────────────────────┐  ║
║  │ [1.1] Add boundaries section                               │  ║
║  │       Add "NOT for:" section in description                │  ║
║  │       Estimated impact: +10 points                         │  ║
║  │                                                            │  ║
║  │ [1.2] Improve trigger specificity                          │  ║
║  │       Current: "Use for code review"                       │  ║
║  │       Proposed: "Use when user says 'review my code',      │  ║
║  │                 'check for bugs', 'analyze this function'" │  ║
║  │       Estimated impact: +5 points                          │  ║
║  └────────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║  Priority 2: HIGH (Score Impact: +12)                            ║
║  ┌────────────────────────────────────────────────────────────┐  ║
║  │ [2.1] Add Output Format section                            │  ║
║  │       Define expected output structure                     │  ║
║  │       Estimated impact: +7 points                          │  ║
║  │                                                            │  ║
║  │ [2.2] Add more examples (2 additional)                     │  ║
║  │       Estimated impact: +5 points                          │  ║
║  └────────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║  Priority 3: MEDIUM (Score Impact: +8)                           ║
║  ┌────────────────────────────────────────────────────────────┐  ║
║  │ [3.1] Restrict Bash tool to specific commands              │  ║
║  │       Or remove if not essential                           │  ║
║  │       Estimated impact: +5 points                          │  ║
║  │                                                            │  ║
║  │ [3.2] Enable self-learning capability                      │  ║
║  │       Add hooks for pattern extraction                     │  ║
║  │       Estimated impact: +3 points                          │  ║
║  └────────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║  PROJECTED SCORE: 62 → 97/100                                    ║
║                                                                  ║
║  Apply improvements? [Y/n/select/plan-only]                      ║
╚══════════════════════════════════════════════════════════════════╝
```

#### Step 3: User Selection

Options:
- **Y** - Apply all improvements
- **n** - Cancel
- **select** - Choose specific improvements
- **plan-only** - Save plan, don't apply

#### Step 4: Apply via Full Pipeline

If approved, deploy organization:

1. **constructor-executor** → Makes changes
2. **constructor-tester** → Validates
3. **constructor-reviewer** → Quality check
4. **constructor-qa** → Comprehensive verification
5. **constructor-optimizer** → Fine-tune
6. **constructor-finalizer** → Complete

#### Step 5: Show Results

```
╔══════════════════════════════════════════════════════════════════╗
║                 IMPROVEMENT COMPLETE                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Component: my-agent                                             ║
║                                                                  ║
║  BEFORE → AFTER                                                  ║
║  ┌─────────────┬─────────────┐                                   ║
║  │ Structure   │   85 →  95  │ ████████████████████████████░░   ║
║  │ Content     │   55 →  90  │ ██████████████████████████████   ║
║  │ Security    │   70 →  85  │ ████████████████████████████░░   ║
║  │ Evolution   │   30 →  75  │ ██████████████████████░░░░░░░░   ║
║  ├─────────────┼─────────────┤                                   ║
║  │ OVERALL     │   62 →  89  │ ██████████████████████████████   ║
║  └─────────────┴─────────────┘                                   ║
║                                                                  ║
║  Changes Applied:                                                ║
║  ├── ✅ [1.1] Added boundaries section                           ║
║  ├── ✅ [1.2] Improved trigger specificity                       ║
║  ├── ✅ [2.1] Added Output Format section                        ║
║  ├── ✅ [2.2] Added 2 more examples                              ║
║  ├── ✅ [3.1] Restricted Bash to 'git' commands only             ║
║  └── ✅ [3.2] Enabled self-learning hooks                        ║
║                                                                  ║
║  Files modified:                                                 ║
║  ├── agents/my-agent.md                                          ║
║  └── agents/my-agent/hooks/hooks.json (new)                      ║
║                                                                  ║
║  Backup: .backup/my-agent-20260203/                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Standard Improvement Workflow

For non-analyze mode (`/uc:improve ./my-skill`):

### Step 1: Identify Component

Determine component type from path:
- Directory with SKILL.md → Skill
- .md file with agent frontmatter → Agent
- hooks.json → Hooks configuration
- Directory with plugin.json → Plugin

### Step 2: Launch Self-Tester Agent

Run validation tests:
- Structure tests (files exist, valid YAML)
- Content tests (triggers, boundaries)
- Quality tests (examples, antipatterns)

Output: Current score and issues list

### Step 3: Launch Self-Reviewer Agent

Deep quality analysis:
- Compare against best practices
- Identify improvement opportunities
- Score current quality (0-100)
- Prioritize improvements by impact

### Step 4: Present Analysis

```
Component: my-skill
Type: Skill
Current Score: 67/100

Issues Found:
1. [HIGH] Description lacks specific triggers
2. [MEDIUM] Missing boundaries (DON'T section)
3. [LOW] No examples provided

Recommended Improvements:
1. Add trigger phrases: "phrase1", "phrase2"
2. Add "## DON'T" section
3. Add working examples
```

### Step 5: User Approval

Ask which improvements to apply:
- All recommended
- Select specific
- Skip and keep current

### Step 6: Apply and Validate

1. Make targeted edits
2. Re-run validation
3. Show before/after comparison
4. Update changelog

## Applying Learned Patterns

```
/uc:improve apply

╔══════════════════════════════════════════════════════════════════╗
║                 LEARNED PATTERNS AVAILABLE                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🟢 High Confidence (auto-apply ready):                          ║
║     [1] api-error-handling (95%)                                 ║
║         Applies to: 3 agents                                     ║
║     [2] yaml-validation-fix (91%)                                ║
║         Applies to: constructor-tester                           ║
║                                                                  ║
║  🟡 Medium Confidence (manual approval):                         ║
║     [3] workflow-optimization (78%)                              ║
║     [4] antipattern-detection (72%)                              ║
║                                                                  ║
║  Apply [1,2] automatically? [Y/n/all/preview]                    ║
╚══════════════════════════════════════════════════════════════════╝
```

### Options

| Flag | Effect |
|------|--------|
| (none) | Interactive mode, asks before applying |
| --auto | Auto-apply patterns with confidence ≥90% |
| --preview | Show what would change without modifying |
| --full | Include low-confidence patterns for review |

## Non-Destructive Mode

All improvements are non-destructive:
- Creates backup before changes: `.backup/{component}-{date}/`
- Shows diff before applying
- Can revert if needed: `/uc:improve revert ./my-skill`

## Organization Agents Used

| Agent | Role in Analysis |
|-------|------------------|
| constructor-analyzer | Deep structural and content analysis |
| constructor-architect | Reviews design and suggests restructuring |
| constructor-tester | Validates structure and syntax |
| constructor-reviewer | Quality scoring and recommendations |
| constructor-qa | Comprehensive quality assurance |
| constructor-validator | Schema and format validation |
| constructor-pentester | Security vulnerability check |
| constructor-optimizer | Performance and efficiency suggestions |
| constructor-learner | Extracts patterns from component |
| constructor-refactor | Applies improvements |
| constructor-finalizer | Completes and documents changes |
