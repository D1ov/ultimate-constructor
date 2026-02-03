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
tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Create Component Command

Create a new Claude Code component through guided Q&A with **full 15-agent pipeline validation**.

## IMPORTANT: Full Pipeline Requirement

**ALWAYS** run the complete 15-agent pipeline when creating any component:

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