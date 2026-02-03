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

Create a new Claude Code component through guided Q&A with full self-* pipeline validation.

## Workflow

### Step 1: Determine Component Type

If type not provided, ask:
- **Skill**: Domain knowledge that loads into context
- **Agent**: Specialized sub-agent for delegation
- **Plugin**: Full package with commands, agents, skills, hooks
- **Hook**: Event-driven automation script

### Step 2: Launch Self-Architect Agent

Delegate to `constructor-architect` agent to:
1. Gather requirements through questions
2. Analyze best practices from knowledge-base/
3. Design component structure
4. Plan file organization

### Step 3: Launch Self-Executor Agent

Delegate to `constructor-executor` agent to:
1. Create files from architect's plan
2. Use templates from templates/
3. Apply patterns from references/
4. Place files in NEW/skills/<component-name>/

### Step 4: Launch Self-Tester Agent

Delegate to `constructor-tester` agent to:
1. Validate structure against schemas
2. Check required files exist
3. Verify YAML frontmatter
4. Test trigger phrases

### Step 5: Launch Self-Reviewer Agent

Delegate to `constructor-reviewer` agent to:
1. Score quality (0-100)
2. Identify improvements
3. Check against best practices
4. Recommend approve/refactor

### Step 6: Quality Gate

If reviewer score < 80:
- Launch `constructor-refactor` agent
- Apply improvements
- Return to Step 4 (max 3 iterations)

If reviewer score >= 80:
- Launch `constructor-acceptance` agent
- Final pass/fail decision

### Step 7: Launch Self-Finalizer Agent

Delegate to `constructor-finalizer` agent to:
1. Update CHANGELOG.md
2. Create summary report
3. Archive patterns learned
4. Output completion message

## Output Location

All components created in:
```
${PROJECT_ROOT}/NEW/skills/<component-name>/
```

## Example Flow

```
User: /uc:create skill

Architect: What problem does this skill solve?
User: Help with API testing

Architect: What phrases should trigger this skill?
User: "test API", "API tests", "endpoint testing"

Architect: What should it NOT handle?
User: UI testing, load testing

[Architect designs structure]
[Executor creates files]
[Tester validates: Score 75/100]
[Reviewer: "Missing examples section"]
[Refactor: Adds examples]
[Tester re-validates: Score 88/100]
[Acceptance: PASS]
[Finalizer: Updates CHANGELOG]

Result: api-testing skill created in NEW/skills/api-testing/
```

## Knowledge Base Access

This command reads from:
- `knowledge-base/schemas/` - For validation
- `knowledge-base/*.md` - For best practices
- `templates/` - For file templates
- `references/` - For patterns