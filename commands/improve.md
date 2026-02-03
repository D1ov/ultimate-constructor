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

Analyze and improve existing Claude Code components using the full self-* organization with ALL 15 agents.

## IMPORTANT: Full Pipeline Requirement

**ALWAYS** run the complete 15-agent pipeline for any improvement:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MANDATORY FULL PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: EXECUTIVE LAYER (Analysis & Planning)                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. constructor-architect   → Analyze structure, identify issues     │   │
│  │ 2. constructor-planner     → Create improvement plan                │   │
│  │ 3. constructor-delegator   → Coordinate if multiple components      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 2: QUALITY LAYER (Validation)                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. constructor-tester      → Structure and syntax validation        │   │
│  │ 5. constructor-reviewer    → Quality scoring (0-100)                │   │
│  │ 6. constructor-qa          → Comprehensive QA checklist             │   │
│  │ 7. constructor-validator   → Schema validation                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 3: SECURITY LAYER (Security Audit)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 8. constructor-pentester   → Security vulnerabilities               │   │
│  │ 9. constructor-auditor     → Audit trail, integrity check           │   │
│  │ 10. constructor-compliance → Standards compliance                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 4: EVOLUTION LAYER (Improvement & Learning)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 11. constructor-executor   → Apply approved changes                 │   │
│  │ 12. constructor-refactor   → Code/structure improvements            │   │
│  │ 13. constructor-optimizer  → Performance optimization               │   │
│  │ 14. constructor-learner    → Extract patterns for future            │   │
│  │ 15. constructor-finalizer  → Complete, document, update changelog   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 5: ACCEPTANCE GATE                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ constructor-acceptance     → Final quality gate (score >= 80?)      │   │
│  │                              If FAIL → Loop back to PHASE 4         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## IMPORTANT: Check Linked Components

When improving an **Agent** that has `skills:` in frontmatter:
1. Parse the skills list from frontmatter
2. Find each linked skill file
3. Ask user: "This agent uses X skills. Improve them too?"
4. If yes, add them to improvement queue

When improving a **Plugin**:
1. List all agents, skills, commands, hooks in plugin
2. Ask user which components to include
3. Process selected components through full pipeline

When improving a **Skill** that references other files:
1. Check references/ directory
2. Check for scripts/ directory
3. Offer to analyze referenced files

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

**ALL improvements use the full 15-agent pipeline.**

### Step 1: Identify Component & Linked Components

Determine component type from path:
- Directory with SKILL.md → Skill
- .md file with agent frontmatter → Agent
- hooks.json → Hooks configuration
- Directory with plugin.json → Plugin

**Check for linked components:**
```
If Agent:
  - Parse `skills:` field from frontmatter
  - Find each skill file
  - Ask: "Improve linked skills too? [Y/n/select]"

If Skill:
  - Check for references/ directory
  - Check for scripts/ directory

If Plugin:
  - List all components (agents/, skills/, commands/, hooks/)
  - Ask which to include in improvement
```

### Step 2: EXECUTIVE LAYER

**constructor-architect** (Agent 1):
- Analyze overall structure
- Identify architectural issues
- Suggest restructuring if needed

**constructor-planner** (Agent 2):
- Create detailed improvement plan
- Prioritize by impact
- Estimate score improvements

**constructor-delegator** (Agent 3):
- If multiple components, coordinate order
- Manage dependencies between components

### Step 3: QUALITY LAYER

**constructor-tester** (Agent 4):
- Structure tests (files exist, valid YAML)
- Content tests (triggers, boundaries)
- Quality tests (examples, antipatterns)

**constructor-reviewer** (Agent 5):
- Deep quality analysis
- Compare against best practices
- Score current quality (0-100)

**constructor-qa** (Agent 6):
- Comprehensive QA checklist
- Edge case verification
- Integration testing

**constructor-validator** (Agent 7):
- Schema validation
- Format validation
- Reference validation

### Step 4: SECURITY LAYER

**constructor-pentester** (Agent 8):
- Check for dangerous tool permissions
- Identify injection risks
- Audit Bash commands if present

**constructor-auditor** (Agent 9):
- Create audit trail
- Verify integrity
- Log all findings

**constructor-compliance** (Agent 10):
- Check Claude Code standards
- Verify best practices compliance
- Flag deviations

### Step 5: Present Analysis & Get Approval

```
╔══════════════════════════════════════════════════════════════════╗
║                    FULL ANALYSIS REPORT                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Component: my-agent                                             ║
║  Type: Agent                                                     ║
║  Linked Skills: 3 (victoria-api-tester, victoria-mock-data, ...) ║
║                                                                  ║
║  EXECUTIVE LAYER FINDINGS:                                       ║
║  - Architecture: Minor issues                                    ║
║  - Plan: 5 improvements identified                               ║
║                                                                  ║
║  QUALITY LAYER SCORES:                                           ║
║  - Tester: 78/100                                                ║
║  - Reviewer: 76/100                                              ║
║  - QA: PASS (3 warnings)                                         ║
║  - Validator: PASS                                               ║
║                                                                  ║
║  SECURITY LAYER:                                                 ║
║  - Pentester: 1 medium risk (Bash too broad)                     ║
║  - Auditor: Clean                                                ║
║  - Compliance: 2 deviations                                      ║
║                                                                  ║
║  Apply improvements? [Y/n/select]                                ║
║  Also improve linked skills? [Y/n/select]                        ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 6: EVOLUTION LAYER (Apply Changes)

**constructor-executor** (Agent 11):
- Apply approved changes
- Make targeted edits

**constructor-refactor** (Agent 12):
- Apply code/structure improvements
- Clean up redundancy

**constructor-optimizer** (Agent 13):
- Optimize performance
- Reduce file size if needed

**constructor-learner** (Agent 14):
- Extract patterns for future
- Update learned/patterns.json

**constructor-finalizer** (Agent 15):
- Update CHANGELOG.md
- Create summary report
- Archive session data

### Step 7: ACCEPTANCE GATE

**constructor-acceptance**:
- Re-run quality checks
- Verify score >= 80
- If FAIL: Loop back to Step 6 (max 3 iterations)
- If PASS: Complete

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
