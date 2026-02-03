# {{skill_name}} - Skill Organization Template

This template creates a full skill organization with comprehensive structure.

## Structure

```
{{skill_name}}/
├── skills/
│   └── {{skill_name}}/
│       └── SKILL.md                         # Main skill
│
├── agents/
│   │  ══════════ EXECUTIVE ══════════
│   ├── {{skill_name}}-architect.md          # Designs approaches
│   ├── {{skill_name}}-planner.md            # Plans execution
│   ├── {{skill_name}}-executor.md           # Executes tasks
│   │
│   │  ══════════ QUALITY ══════════
│   ├── {{skill_name}}-tester.md             # Tests results
│   ├── {{skill_name}}-reviewer.md           # Reviews quality
│   ├── {{skill_name}}-validator.md          # Validates output
│   │
│   │  ══════════ EVOLUTION ══════════
│   ├── {{skill_name}}-refactor.md           # Improvements
│   ├── {{skill_name}}-learner.md            # Pattern learning
│   └── {{skill_name}}-finalizer.md          # Completion
│
├── hooks/
│   └── hooks.json                           # Self-learning hooks
│
├── scripts/
│   ├── validate.py                          # Validation script
│   └── learn.py                             # Learning script
│
├── references/
│   ├── patterns.md                          # Best practices
│   ├── antipatterns.md                      # What NOT to do
│   └── examples.md                          # Working examples
│
├── learned/
│   └── patterns.json                        # Learned patterns
│
└── README.md                                # This file
```

## Usage

The main skill (`SKILL.md`) provides domain knowledge and can invoke supporting agents for complex tasks.

## Supporting Agents

Skills with full organization get supporting agents for:
- **Architect**: Designing approach for complex tasks
- **Planner**: Breaking tasks into steps
- **Executor**: Performing domain-specific work
- **Tester**: Validating results
- **Reviewer**: Quality assessment
- **Validator**: Format/schema checks
- **Refactor**: Improvements
- **Learner**: Pattern extraction
- **Finalizer**: Completion
