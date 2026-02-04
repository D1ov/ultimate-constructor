---
name: create
description: Create a new Claude Code component (skill, agent, plugin, or hook) through guided Q&A with self-* pipeline
args:
  - name: type
    description: "Component type: skill, agent, plugin, hook"
    required: false
  - name: name
    description: Component name (optional, will be asked if not provided)
    required: false
examples:
  - "/uc:create"
  - "/uc:create skill"
  - "/uc:create agent code-reviewer"
  - "/uc:create plugin my-plugin"
model: sonnet
tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---

# Create Component Command

Create a new Claude Code component through guided Q&A with **full 16-agent pipeline validation**.

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
  {content: "Run constructor-executor agent", status: "pending", activeForm: "Running executor"},

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
| GATE 2 | Component type determined | Ask user |
| GATE 3 | Self-learning preference asked | Ask user |
| GATE 4 | Each agent invoked via Task tool | Invoke missing agents |
| GATE 5 | Final score >= 80 | Loop back to PHASE 4 |
| GATE 6 | Folder structure complete | constructor-finalizer verifies |

### HOW TO INVOKE EACH AGENT

You MUST use the Task tool with the exact subagent_type for each agent:

```
Task({
  description: "Architect design",
  prompt: "Design [component] structure...",
  subagent_type: "uc:constructor-architect"
})
```

**Available agent types (ALL 20):**

EXECUTIVE LAYER:
- `uc:constructor-architect` - Gather requirements, design structure
- `uc:constructor-planner` - Create execution plan with dependencies
- `uc:constructor-delegator` - Coordinate multi-file creation
- `uc:constructor-executor` - Create files from plan

QUALITY LAYER:
- `uc:constructor-tester` - Validate structure and content
- `uc:constructor-reviewer` - Score quality (0-100)
- `uc:constructor-qa` - Comprehensive QA checklist
- `uc:constructor-validator` - Schema validation

SECURITY LAYER:
- `uc:constructor-pentester` - Security vulnerabilities
- `uc:constructor-auditor` - Audit trail creation
- `uc:constructor-compliance` - Standards compliance

EVOLUTION LAYER:
- `uc:constructor-refactor` - Apply improvements if score < 80
- `uc:constructor-optimizer` - Optimize structure
- `uc:constructor-learner` - Extract patterns, create learned/patterns.json
- `uc:constructor-finalizer` - Complete, create hooks.json, verify structure
- `uc:constructor-acceptance` - Final quality gate

ANALYSIS & CONTEXT:
- `uc:constructor-analyzer` - Deep analysis for existing components
- `uc:constructor-applier` - Apply learned patterns
- `uc:constructor-context-reviewer` - Review extracted content
- `uc:constructor-context-accepter` - Final acceptance for context

## ⛔ MANDATORY: Component Structure

Every created component MUST have this structure:

### For Agents
```
my-agent/
├── my-agent.md              # Main agent file
├── references/
│   └── (domain-specific docs)
├── scripts/
│   ├── extract_patterns.py  # If self-learning enabled
│   └── apply_learned.py     # If self-improvement enabled
├── learned/
│   └── patterns.json        # Created by constructor-learner
└── hooks/
    └── hooks.json           # Created by constructor-finalizer
```

### For Skills
```
my-skill/
├── SKILL.md                 # Main skill file
├── references/
│   └── (detailed docs)
├── scripts/
│   └── validate.py
└── learned/
    └── patterns.json
```

### Agent Responsibilities for Structure

| Agent | Creates |
|-------|---------|
| **constructor-architect** | Designs folder structure |
| **constructor-executor** | Creates ALL folders and files |
| **constructor-learner** | Creates learned/patterns.json |
| **constructor-finalizer** | Creates hooks/hooks.json, verifies completeness |

## IMPORTANT: Full Pipeline Requirement

**ALWAYS** run the complete 16-agent pipeline when creating any component:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MANDATORY FULL PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: EXECUTIVE LAYER (Design & Planning)                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. constructor-architect   → Gather requirements, design structure  │   │
│  │ 2. constructor-planner     → Create execution plan                  │   │
│  │ 3. constructor-delegator   → Coordinate multi-file creation         │   │
│  │ 4. constructor-executor    → Create files from plan                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 2: QUALITY LAYER (Validation)                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. constructor-tester      → Structure and syntax validation        │   │
│  │ 6. constructor-reviewer    → Quality scoring (0-100)                │   │
│  │ 7. constructor-qa          → Comprehensive QA checklist             │   │
│  │ 8. constructor-validator   → Schema validation                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 3: SECURITY LAYER (Security Audit)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 9. constructor-pentester   → Security vulnerabilities               │   │
│  │ 10. constructor-auditor    → Audit trail creation                   │   │
│  │ 11. constructor-compliance → Standards compliance                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                        │
│  PHASE 4: EVOLUTION LAYER (Refinement & Learning)                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 12. constructor-refactor   → Apply improvements if score < 80       │   │
│  │ 13. constructor-optimizer  → Optimize structure                     │   │
│  │ 14. constructor-learner    → Extract patterns for future            │   │
│  │ 15. constructor-finalizer  → Complete, document, changelog          │   │
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

## Workflow

### Step 1: Determine Component Type

If type not provided, ask using AskUserQuestion:
- **Skill**: Domain knowledge that loads into context
- **Agent**: Specialized sub-agent for delegation
- **Plugin**: Full package with commands, agents, skills, hooks
- **Hook**: Event-driven automation script

### Step 2: Ask About Self-Learning Capabilities

**IMPORTANT**: For agents, plugins, and hooks, ALWAYS ask:

```
╔══════════════════════════════════════════════════════════════════╗
║              SELF-LEARNING & SELF-IMPROVEMENT                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Would you like to add self-learning capabilities?               ║
║                                                                  ║
║  🔄 Self-Learning:                                               ║
║     - Extracts patterns from usage                               ║
║     - Stores successful workflows                                ║
║     - Learns from errors and fixes                               ║
║     - Builds knowledge base over time                            ║
║                                                                  ║
║  🔧 Self-Improvement:                                            ║
║     - Automatically applies learned patterns                     ║
║     - Suggests improvements based on usage                       ║
║     - Refactors itself when confidence is high                   ║
║                                                                  ║
║  Options:                                                        ║
║  [1] Both (self-learning + self-improvement)                     ║
║  [2] Self-learning only                                          ║
║  [3] Self-improvement only                                       ║
║  [4] Neither (basic component)                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

If self-learning is enabled, create:
- `hooks/hooks.json` with PostToolUse events
- `learned/patterns.json` for storing patterns
- `scripts/extract_patterns.py` for pattern extraction

If self-improvement is enabled, create:
- Additional hooks for auto-applying patterns
- `scripts/apply_learned.py` for improvements

### Step 3: EXECUTIVE LAYER

**constructor-architect** (Agent 1):
- Gather requirements through questions
- Analyze best practices from knowledge-base/
- Design component structure
- Plan file organization

**constructor-planner** (Agent 2):
- Create detailed execution plan
- Define file creation order
- Identify dependencies

**constructor-delegator** (Agent 3):
- Coordinate if multiple files needed
- Manage creation sequence

**constructor-executor** (Agent 4):
- Create files from architect's plan
- Use templates from templates/
- Apply patterns from references/
- Place files in NEW/skills/<component-name>/

### Step 4: QUALITY LAYER

**constructor-tester** (Agent 5):
- Validate structure against schemas
- Check required files exist
- Verify YAML frontmatter
- Test trigger phrases

**constructor-reviewer** (Agent 6):
- Score quality (0-100)
- Identify improvements
- Check against best practices

**constructor-qa** (Agent 7):
- Run comprehensive QA checklist
- Verify all sections present
- Check for antipatterns

**constructor-validator** (Agent 8):
- Validate against JSON schemas
- Check file formats
- Verify references exist

### Step 5: SECURITY LAYER

**constructor-pentester** (Agent 9):
- Check tool permissions
- Identify dangerous patterns
- Audit Bash usage if present

**constructor-auditor** (Agent 10):
- Create audit trail
- Log creation steps
- Track decisions made

**constructor-compliance** (Agent 11):
- Check Claude Code standards
- Verify naming conventions
- Flag deviations

### Step 6: EVOLUTION LAYER

If reviewer score < 80:
- **constructor-refactor** (Agent 12): Apply improvements
- Loop back to QUALITY LAYER (max 3 iterations)

**constructor-optimizer** (Agent 13):
- Optimize file structure
- Reduce redundancy
- Improve readability

**constructor-learner** (Agent 14):
- Extract patterns from creation
- Update learned/patterns.json
- Store successful approaches

**constructor-finalizer** (Agent 15):
- Update CHANGELOG.md
- Create summary report
- Archive patterns learned
- Output completion message

### Step 7: ACCEPTANCE GATE

**constructor-acceptance**:
- Final pass/fail decision
- Verify score >= 80
- If FAIL: Return to Step 6 with feedback
- If PASS: Component complete

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
  "creation_session": {
    "date": "ISO-DATE",
    "score": 0,
    "patterns_extracted": []
  }
}
```

### 3. scripts/extract_patterns.py (created by constructor-executor)
Basic pattern extraction script template.

### Agent Execution Checklist

```
constructor-architect:
  □ Gather requirements via AskUserQuestion
  □ Design target structure with references/, scripts/, learned/, hooks/
  □ Document what files need to be created

constructor-executor:
  □ Create references/ folder
  □ Create scripts/ folder
  □ Create learned/ folder
  □ Create hooks/ folder
  □ Create all planned files

constructor-learner:
  □ Create learned/patterns.json
  □ Extract patterns from creation session
  □ Document successful approaches
  □ Save workflow patterns

constructor-finalizer:
  □ Create hooks/hooks.json with self-learning
  □ Verify ALL folders exist
  □ Verify ALL required files exist
  □ Update CHANGELOG if exists
  □ Create creation report
```

## Output Location

All components created in:
```
${PROJECT_ROOT}/NEW/skills/<component-name>/
```

## Example Flow

```
User: /uc:create agent

Claude: What type of agent would you like to create?
User: A code reviewer agent

Claude: Would you like to add self-learning capabilities?
       [1] Both (self-learning + self-improvement)
       [2] Self-learning only
       [3] Self-improvement only
       [4] Neither (basic component)
User: 1 (Both)

╔══════════════════════════════════════════════════════════════════╗
║                    EXECUTIVE LAYER                               ║
╠══════════════════════════════════════════════════════════════════╣
║ [Architect] Gathering requirements...                            ║
║   → What should trigger this agent?                              ║
║   → What should it NOT do?                                       ║
║   → What tools does it need?                                     ║
║ [Planner] Creating execution plan...                             ║
║ [Delegator] Single file needed, no coordination required         ║
║ [Executor] Creating agent file + self-learning hooks...          ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                    QUALITY LAYER                                 ║
╠══════════════════════════════════════════════════════════════════╣
║ [Tester] Validating structure... ✅                              ║
║ [Reviewer] Quality score: 72/100 ⚠️                              ║
║   Issues: Missing Output Format section                          ║
║ [QA] Running checklist... 8/10 passed                            ║
║ [Validator] Schema validation... ✅                              ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                    SECURITY LAYER                                ║
╠══════════════════════════════════════════════════════════════════╣
║ [Pentester] Checking permissions... ✅ No dangerous tools        ║
║ [Auditor] Creating audit trail... ✅                             ║
║ [Compliance] Standards check... ✅                               ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                    EVOLUTION LAYER (Iteration 1)                 ║
╠══════════════════════════════════════════════════════════════════╣
║ [Refactor] Score < 80, applying improvements...                  ║
║   → Adding Output Format section                                 ║
║   → Improving trigger specificity                                ║
║ [Re-testing] New score: 85/100 ✅                                ║
║ [Optimizer] Optimizing structure... ✅                           ║
║ [Learner] Extracting patterns... ✅                              ║
║ [Finalizer] Updating changelog... ✅                             ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                    ACCEPTANCE GATE                               ║
╠══════════════════════════════════════════════════════════════════╣
║ [Acceptance] Final check: 85/100 >= 80 threshold                 ║
║ Result: ✅ PASS                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Component created: NEW/skills/code-reviewer/
├── agents/code-reviewer.md
├── hooks/hooks.json (self-learning enabled)
├── learned/patterns.json
└── scripts/
    ├── extract_patterns.py
    └── apply_learned.py
```

## Knowledge Base Access

This command reads from:
- `knowledge-base/schemas/` - For validation
- `knowledge-base/*.md` - For best practices
- `templates/` - For file templates
- `references/` - For patterns
