# Sub-Agents Documentation

Complete guide to sub-agents in Claude Code: built-in agents, custom agent creation, configuration, and delegation patterns.

## Overview

Sub-agents are specialized Claude instances that can be launched via the Task tool to handle specific tasks autonomously. They run with their own context, tools, and optionally different models.

## Built-in Sub-Agents

### Explore Agent
- **Type:** `Explore`
- **Model:** Haiku (fast, cost-effective)
- **Tools:** All read-only tools (Glob, Grep, Read, WebFetch, WebSearch)
- **Purpose:** Fast codebase exploration and search
- **Thoroughness levels:** "quick", "medium", "very thorough"

**Usage:**
```
Task(subagent_type="Explore", prompt="Find all API endpoints", description="Find API endpoints")
```

### Plan Agent
- **Type:** `Plan`
- **Model:** Sonnet
- **Tools:** All tools except Task, ExitPlanMode, Edit, Write, NotebookEdit
- **Purpose:** Design implementation plans

### General-Purpose Agent
- **Type:** `general-purpose`
- **Model:** Sonnet
- **Tools:** All tools (*)
- **Purpose:** Complex multi-step tasks

## Custom Agents

### File Location

Custom agents are markdown files in:
- `.claude/agents/` (project-level)
- `~/.claude/agents/` (user-level)
- Plugin `agents/` directory

### File Format

```yaml
---
name: agent-name
description: When Claude should delegate to this agent. Include triggers.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
skills: skill-1, skill-2
---

# Agent Instructions

Your detailed instructions here...
```

### Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (lowercase, hyphens) |
| `description` | string | When to use, triggers. Add "use proactively" for auto-invocation |
| `tools` | string | Comma-separated tools. Omit to inherit ALL |
| `disallowedTools` | string | Tools to explicitly deny |
| `model` | enum | sonnet, opus, haiku, inherit |
| `permissionMode` | enum | default, acceptEdits, dontAsk, bypassPermissions, plan |
| `skills` | string | Comma-separated skills to auto-load |
| `hooks` | object | Lifecycle hooks scoped to this agent |

### Permission Modes

- **default**: Ask for tool permissions normally
- **acceptEdits**: Auto-accept file edits
- **dontAsk**: Skip permission prompts (risky)
- **bypassPermissions**: Full bypass (requires trust)
- **plan**: Read-only planning mode

## Tool Restrictions

### Specifying Tools
```yaml
tools: Read, Grep, Glob, Bash
```

### Bash Scoping
```yaml
tools: Read, Bash(git:*, npm:test)
```

### Disallowing Tools
```yaml
disallowedTools: Write, Edit
```

## Launching Sub-Agents

### Via Task Tool
```json
{
  "description": "Review code changes",
  "prompt": "Review the changes in src/",
  "subagent_type": "code-reviewer"
}
```

### Parallel Execution
Launch multiple agents in parallel:
```json
[
  {"subagent_type": "Explore", "prompt": "Find tests", "description": "Find tests"},
  {"subagent_type": "Explore", "prompt": "Find configs", "description": "Find configs"}
]
```

### Resuming Agents
```json
{
  "resume": "agent-id-from-previous-run",
  "prompt": "Continue with the refactoring"
}
```

## Delegation Patterns

### Sweet Spot: Repetitive + Judgment

Best for sub-agents:
- Auditing multiple files
- Updating patterns across codebase
- Research across multiple sources
- Validation with context

### Prompt Template Structure
```markdown
For each [item]:
1. Read [source file]
2. Verify with [external check]
3. Check [authoritative source]
4. Evaluate/score
5. FIX issues found  ← Key instruction

Items: [list of 5-8 items]
```

### Batch Sizing
- 5-8 items per agent
- 2-4 agents in parallel
- Agents edit, human commits

### When NOT to Use Sub-Agents
- Single complex task (do it yourself)
- Simple find-replace (use scripts)
- Tasks with dependencies between items
- Creative/subjective decisions

## /agents Command

Interactive agent management:
```
/agents              # List available agents
/agents create       # Create new agent
/agents edit <name>  # Edit agent
/agents delete <name># Delete agent
```

## CLI Configuration

Override agents via CLI:
```bash
claude --agents '{"code-reviewer": {"model": "opus"}}'
```

## Disabling Built-in Agents

In settings, use Task permission rules:
```json
{
  "permissions": {
    "deny": ["Task(Explore)"]
  }
}
```

## Best Practices

1. **Specific descriptions**: Include trigger phrases and boundaries
2. **Minimal tools**: Only grant needed tools
3. **Appropriate model**: Use haiku for simple tasks, sonnet for complex
4. **Clear instructions**: Body should be actionable
5. **Test incrementally**: Start with small batches
6. **Human commits**: Let agents edit, you commit

## Example Agents

### Code Reviewer
```yaml
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Review code for:
- Security vulnerabilities
- Performance issues
- Code style consistency
- Best practices violations

Provide specific, actionable feedback.
```

### Documentation Writer
```yaml
---
name: doc-writer
description: Generate documentation from code. Use for README, API docs.
tools: Read, Grep, Glob, Write
model: sonnet
---

Generate clear, accurate documentation:
- Extract function signatures
- Document parameters and returns
- Include usage examples
- Follow project conventions
```
