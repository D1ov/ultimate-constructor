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
tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---

# Improve Component Command

Analyze and improve existing Claude Code components using the full self-* organization with ALL 16 agents.

## ⛔ CRITICAL: MANDATORY EXECUTION PROTOCOL ⛔

**YOU MUST FOLLOW THIS PROTOCOL EXACTLY. NO SHORTCUTS. NO SKIPPING AGENTS.**

### STEP 0: CREATE FULL TODO LIST IMMEDIATELY

Before doing ANYTHING else, you MUST use TodoWrite to create tasks for ALL 16 agents:

```
TodoWrite([
  // PHASE 1: EXECUTIVE LAYER
  {content: "Run constructor-architect agent", status: "pending", activeForm: "Running architect"},
  {content: "Run constructor-planner agent", status: "pending", activeForm: "Running planner"},
  {content: "Run constructor-delegator agent", status: "pending", activeForm: "Running delegator"},

  // PHASE 2: QUALITY LAYER
  {content: "Run constructor-tester agent", status: "pending", activeForm: "Running tester"},
  {content: "Run constructor-reviewer agent", status: "pending", activeForm: "Running reviewer"},
  {content: "Run constructor-qa agent", status: "pending", activeForm: "Running QA"},
  {content: "Run constructor-validator agent", status: "pending", activeForm: "Running validator"},

  // PHASE 3: SECURITY LAYER
  {content: "Run constructor-pentester agent", status: "pending", activeForm: "Running pentester"},
  {content: "Run constructor-auditor agent", status: "pending", activeForm: "Running auditor"},
  {content: "Run constructor-compliance agent", status: "pending", activeForm: "Running compliance"},

  // PHASE 4: EVOLUTION LAYER
  {content: "Run constructor-executor agent", status: "pending", activeForm: "Running executor"},
  {content: "Run constructor-refactor agent", status: "pending", activeForm: "Running refactor"},
  {content: "Run constructor-optimizer agent", status: "pending", activeForm: "Running optimizer"},
  {content: "Run constructor-learner agent", status: "pending", activeForm: "Running learner"},
  {content: "Run constructor-finalizer agent", status: "pending", activeForm: "Running finalizer"},

  // PHASE 5: ACCEPTANCE GATE
  {content: "Run constructor-acceptance agent", status: "pending", activeForm: "Running acceptance"}
])
```

### ⛔ STOP GATES - YOU CANNOT PROCEED WITHOUT THESE

| Gate | Requirement | Action if Failed |
|------|-------------|------------------|
| GATE 1 | Todo list created with 16 items | Create it NOW |
| GATE 2 | Component + ALL linked files read | Read them ALL |
| GATE 3 | Each agent invoked via Task tool | Invoke missing agents |
| GATE 4 | Final score >= 80 | Loop back to PHASE 4 |
| GATE 5 | Folder structure complete | constructor-finalizer verifies |
| GATE 6 | Self-learning enabled | constructor-learner creates patterns.json |

### HOW TO INVOKE EACH AGENT

You MUST use the Task tool with the exact subagent_type for each agent:

```
Task({
  description: "Architect analysis",
  prompt: "Analyze [component] structure and design...",
  subagent_type: "uc:constructor-architect"
})
```

**Available agent types (ALL 20):**

EXECUTIVE LAYER:
- `uc:constructor-architect` - Design structure, ask questions
- `uc:constructor-planner` - Create execution plan with dependencies
- `uc:constructor-executor` - Create files from design
- `uc:constructor-delegator` - Coordinate multi-agent work

QUALITY LAYER:
- `uc:constructor-tester` - Validate structure and content
- `uc:constructor-reviewer` - Score quality, identify improvements
- `uc:constructor-qa` - Comprehensive quality assurance
- `uc:constructor-validator` - Schema and format validation

SECURITY LAYER:
- `uc:constructor-pentester` - Find security vulnerabilities
- `uc:constructor-auditor` - Create audit trail, verify integrity
- `uc:constructor-compliance` - Check standards compliance

EVOLUTION LAYER:
- `uc:constructor-refactor` - Apply improvements
- `uc:constructor-optimizer` - Optimize performance
- `uc:constructor-learner` - Extract patterns for future
- `uc:constructor-finalizer` - Complete and document
- `uc:constructor-acceptance` - Final quality gate

ANALYSIS & CONTEXT:
- `uc:constructor-analyzer` - Deep analysis for existing components
- `uc:constructor-applier` - Apply learned patterns
- `uc:constructor-context-reviewer` - Review extracted content
- `uc:constructor-context-accepter` - Final acceptance for context

## IMPORTANT: Full Pipeline Requirement

**ALWAYS** run the complete 16-agent pipeline for any improvement:

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

## ⛔ MANDATORY: Analyze ALL Linked Components

### For Agents with `skills:` field

**YOU MUST:**
1. Parse `skills:` from frontmatter
2. Search for each skill file using Glob
3. Read ALL found skill files
4. Add to improvement queue

```
Example agent frontmatter:
  skills: victoria-api-tester, victoria-mock-data, victoria-redis-debug

YOU MUST find and read:
  - **/victoria-api-tester/**/SKILL.md
  - **/victoria-mock-data/**/SKILL.md
  - **/victoria-redis-debug/**/SKILL.md
```

### For Plugins
**YOU MUST:**
1. Read plugin.json
2. List ALL components (agents/, skills/, commands/, hooks/)
3. Ask user which to include (default: ALL)
4. Process each through full pipeline

### For Skills with references
**YOU MUST:**
1. Check if references/ exists → read all files
2. Check if scripts/ exists → read all files
3. Include in analysis scope

## ⛔ MANDATORY: Create Full Folder Structure

After improvement, the component MUST have this structure:

### For Agents
```
my-agent/
├── my-agent.md              # Main agent file
├── references/
│   ├── patterns.md          # Workflow patterns
│   ├── schemas.md           # Data schemas used
│   └── api-reference.md     # API docs if applicable
├── scripts/
│   ├── validate.py          # Validation script
│   └── test.py              # Test script
├── learned/
│   ├── patterns.json        # Extracted patterns
│   └── improvements/        # Applied improvements history
└── hooks/
    └── hooks.json           # Self-learning hooks
```

### For Skills
```
my-skill/
├── SKILL.md                 # Main skill file
├── references/
│   ├── detailed-guide.md    # Detailed documentation
│   ├── examples.md          # Extended examples
│   └── troubleshooting.md   # Common issues
├── scripts/
│   └── validate.py          # Validation script
└── learned/
    └── patterns.json        # Extracted patterns
```

### Agent Responsibilities for Structure

| Agent | Responsibility |
|-------|----------------|
| **constructor-architect** | Design folder structure in improvement plan |
| **constructor-planner** | Include structure tasks in execution plan |
| **constructor-executor** | Create ALL folders and placeholder files |
| **constructor-learner** | Create learned/patterns.json, extract patterns |
| **constructor-finalizer** | Verify structure complete, create hooks.json |

## ⛔ MANDATORY: Self-Learning Integration

**constructor-learner** and **constructor-finalizer** MUST create:

### 1. hooks/hooks.json (created by constructor-finalizer)
```json
{
  "hooks": [
    {
      "event": "Stop",
      "script": "python ${COMPONENT_PATH}/scripts/extract_patterns.py",
      "timeout": 30000
    }
  ],
  "context_tracking": {
    "enabled": true,
    "track_tool_outcomes": true,
    "min_confidence": 0.7
  }
}
```

### 2. learned/patterns.json (created by constructor-learner)
```json
{
  "patterns": [],
  "antipatterns": [],
  "workflows": [],
  "last_updated": "ISO-DATE",
  "sessions_analyzed": 1,
  "improvement_session": {
    "date": "ISO-DATE",
    "before_score": 0,
    "after_score": 0,
    "changes_applied": []
  }
}
```

### 3. scripts/extract_patterns.py (created by constructor-executor)
Basic pattern extraction script template.

### Agent Execution Checklist

```
constructor-architect:
  □ Analyze current structure
  □ Design target structure with references/, scripts/, learned/, hooks/
  □ Document what files need to be created

constructor-executor:
  □ Create references/ folder
  □ Create scripts/ folder
  □ Create learned/ folder
  □ Create hooks/ folder
  □ Create placeholder files

constructor-learner:
  □ Create learned/patterns.json
  □ Extract patterns from improvement session
  □ Document antipatterns found
  □ Save workflow patterns

constructor-finalizer:
  □ Create hooks/hooks.json with self-learning
  □ Verify ALL folders exist
  □ Verify ALL required files exist
  □ Update CHANGELOG if exists
  □ Create improvement report
```

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

### Mode 3: Deep Analysis
```
/uc:improve analyze ./my-agent           # Full organization analysis
/uc:improve analyze ./my-skill --full    # Maximum depth analysis
/uc:improve analyze ./my-plugin --plan-only  # Only create plan, don't apply
```

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
