# {{agent_name}} - Agent Organization Template

This template creates a full agent organization with 15+ sub-agents.

## Structure

```
{{agent_name}}/
├── agents/
│   │
│   │  ══════════════ MAIN ══════════════
│   ├── {{agent_name}}.md                    # Main agent
│   │
│   │  ══════════ EXECUTIVE ══════════
│   ├── {{agent_name}}-architect.md          # Designs tasks
│   ├── {{agent_name}}-planner.md            # Plans execution
│   ├── {{agent_name}}-executor.md           # Executes work
│   ├── {{agent_name}}-delegator.md          # Delegates subtasks
│   │
│   │  ══════════ QUALITY ══════════
│   ├── {{agent_name}}-tester.md             # Tests results
│   ├── {{agent_name}}-reviewer.md           # Reviews quality
│   ├── {{agent_name}}-qa.md                 # Quality assurance
│   ├── {{agent_name}}-validator.md          # Validates output
│   │
│   │  ══════════ SECURITY ══════════
│   ├── {{agent_name}}-pentester.md          # Security testing
│   ├── {{agent_name}}-auditor.md            # Audit trail
│   ├── {{agent_name}}-compliance.md         # Standards check
│   │
│   │  ══════════ EVOLUTION ══════════
│   ├── {{agent_name}}-refactor.md           # Improvements
│   ├── {{agent_name}}-optimizer.md          # Optimization
│   ├── {{agent_name}}-learner.md            # Pattern learning
│   └── {{agent_name}}-finalizer.md          # Completion
│
├── skills/
│   └── {{agent_name}}-domain/
│       └── SKILL.md                         # Domain knowledge
│
├── hooks/
│   └── hooks.json                           # Self-learning hooks
│
├── scripts/
│   ├── orchestrator.py                      # Pipeline coordination
│   ├── quality_metrics.py                   # Quality measurement
│   ├── security_scan.py                     # Security scanning
│   └── pattern_extractor.py                 # Pattern extraction
│
├── learned/
│   ├── patterns.json                        # Learned patterns
│   ├── quality-history.json                 # Quality scores
│   └── audit-trail.json                     # Audit log
│
├── references/
│   └── domain-knowledge.md                  # Domain specifics
│
└── README.md                                # This file
```

## Usage

The main agent (`{{agent_name}}.md`) orchestrates all sub-agents automatically.

## Sub-Agent Roles

### Executive Layer
- **Architect**: Analyzes tasks and designs approach
- **Planner**: Creates step-by-step execution plans
- **Executor**: Performs the actual work
- **Delegator**: Routes subtasks to specialists

### Quality Layer
- **Tester**: Validates outputs
- **Reviewer**: Scores quality
- **QA**: Deep quality analysis
- **Validator**: Schema/format checks

### Security Layer
- **Pentester**: Finds vulnerabilities
- **Auditor**: Creates audit trails
- **Compliance**: Checks standards

### Evolution Layer
- **Refactor**: Applies improvements
- **Optimizer**: Performance tuning
- **Learner**: Extracts patterns
- **Finalizer**: Completes and documents
