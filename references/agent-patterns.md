# Agent Best Practices

Patterns for creating effective Claude Code agents.

## Description Patterns

### Clear Delegation Criteria

```yaml
description: |
  Expert code reviewer for security and performance.
  Use proactively after code changes to src/.
  NOT for: documentation review, test review.
```

### Proactive Invocation

Add "use proactively" for automatic delegation:

```yaml
description: |
  Test runner agent. Use proactively after code edits
  to verify tests still pass.
```

### Specific Task Scope

```yaml
description: |
  Analyze database queries for N+1 problems and missing indexes.
  Use when: "optimize queries", "slow database", "N+1".
  Outputs: List of issues with fix suggestions.
```

## Tool Configuration Patterns

### Minimal Permissions

Grant only necessary tools:

```yaml
# Read-only analysis
tools: Read, Grep, Glob

# Code modification
tools: Read, Write, Edit, Glob

# With limited bash
tools: Read, Grep, Bash(git:status, npm:test)
```

### Deny Dangerous Tools

```yaml
tools: Read, Write, Edit, Grep
disallowedTools: Bash, Task
```

### MCP Tool Access

```yaml
tools: Read, Grep, mcp__github__create_issue, mcp__slack__post_message
```

## Model Selection

### Haiku (Fast, Cost-effective)

```yaml
model: haiku
```

Use for:
- Simple validation tasks
- Quick searches
- Status checks
- Formatting

### Sonnet (Balanced)

```yaml
model: sonnet
```

Use for:
- Code review
- Complex analysis
- Multi-step tasks
- Most general work

### Opus (Maximum Quality)

```yaml
model: opus
```

Use for:
- Critical decisions
- Complex architecture
- Security analysis
- High-stakes tasks

### Inherit (From Parent)

```yaml
model: inherit
```

Use when agent should match parent's model.

## Permission Modes

### Default (Recommended)

```yaml
permissionMode: default
```

Normal permission prompts.

### Accept Edits

```yaml
permissionMode: acceptEdits
```

Auto-accept file modifications. Use for trusted edit agents.

### Don't Ask

```yaml
permissionMode: dontAsk
```

Skip all prompts. Use carefully.

## Workflow Patterns

### Linear Workflow

```markdown
## Workflow

### Step 1: Gather Information
Read relevant files and understand context.

### Step 2: Analyze
Apply analysis logic to gathered data.

### Step 3: Report
Output findings in structured format.
```

### Conditional Workflow

```markdown
## Workflow

### Step 1: Assess Scope
Determine if task is small, medium, or large.

### Step 2a: Small Task
Handle directly with quick fix.

### Step 2b: Medium Task
Break into subtasks and execute.

### Step 2c: Large Task
Create plan and request approval.
```

### Loop Workflow

```markdown
## Workflow

### Step 1: Initialize
Set up iteration state.

### Step 2: Process Item
For each item in batch:
1. Read item
2. Validate
3. Transform
4. Record result

### Step 3: Summarize
Aggregate results and report.
```

## Output Patterns

### Structured JSON Output

```markdown
## Output Format

```json
{
  "status": "success|failure",
  "findings": [
    {"file": "path", "line": 42, "issue": "description"}
  ],
  "summary": "Brief summary",
  "recommendations": ["action1", "action2"]
}
```
```

### Report Output

```markdown
## Output Format

# Analysis Report

## Summary
[Brief overview]

## Findings
| File | Issue | Severity |
|------|-------|----------|
| ... | ... | ... |

## Recommendations
1. [Action item]
2. [Action item]
```

## Constraint Patterns

### Scope Constraints

```markdown
## Constraints

- Only analyze files in src/ directory
- Maximum 10 files per run
- Skip files larger than 1000 lines
```

### Quality Constraints

```markdown
## Constraints

- All suggestions must include code examples
- Never suggest removing error handling
- Always verify changes compile
```

### Communication Constraints

```markdown
## Constraints

- Report progress every 5 items
- Ask for clarification if requirements unclear
- Summarize changes before making them
```

## Batch Processing Pattern

```markdown
## Workflow

Process items in batches of 5-8:

1. Load batch of items
2. For each item:
   - Read source
   - Analyze
   - Fix if needed
3. Report batch results
4. Continue to next batch

Maximum parallel agents: 3
```
