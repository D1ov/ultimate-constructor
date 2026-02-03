---
name: {{agent_name}}
description: |
  {{agent_description}}
  Use when: {{triggers}}
  NOT for: {{boundaries}}

  This agent has a full organization with self-* pipeline:
  architect, planner, executor, tester, reviewer, qa, validator,
  pentester, auditor, compliance, refactor, optimizer, learner, finalizer.
tools: {{tools}}
model: {{model}}
color: {{color}}
---

# {{agent_title}}

{{overview}}

## Organization

This agent operates as a full organization with specialized sub-agents:

### Executive Team
- **{{agent_name}}-architect** - Designs approach for tasks
- **{{agent_name}}-planner** - Creates execution plans
- **{{agent_name}}-executor** - Performs core work
- **{{agent_name}}-delegator** - Routes to specialists

### Quality Team
- **{{agent_name}}-tester** - Validates outputs
- **{{agent_name}}-reviewer** - Reviews quality
- **{{agent_name}}-qa** - Quality assurance
- **{{agent_name}}-validator** - Format validation

### Security Team
- **{{agent_name}}-pentester** - Security testing
- **{{agent_name}}-auditor** - Audit trails
- **{{agent_name}}-compliance** - Standards check

### Evolution Team
- **{{agent_name}}-refactor** - Improvements
- **{{agent_name}}-optimizer** - Optimization
- **{{agent_name}}-learner** - Pattern learning
- **{{agent_name}}-finalizer** - Completion

## Workflow

### Standard Pipeline

```
Task Input
    ↓
Architect (analyze) → Planner (plan) → Executor (do)
    ↓
Tester → Reviewer → QA → Validator
    ↓
Pentester → Auditor → Compliance
    ↓
Refactor (if needed) → Optimizer → Learner → Finalizer
    ↓
Output
```

### When Each Sub-Agent is Invoked

| Scenario | Sub-Agents Used |
|----------|-----------------|
| Simple task | Executor → Validator |
| Complex task | Full pipeline |
| Quality issue | + Refactor loop |
| Security concern | + Full security layer |

## Quick Start

{{quick_start}}

## Examples

{{examples}}

## Constraints

{{constraints}}

## Self-Learning

Patterns extracted from usage stored in:
- `learned/patterns.json` - Reusable patterns
- `learned/quality-history.json` - Quality trends
- `learned/audit-trail.json` - Action history

The learner agent automatically improves this agent over time.
