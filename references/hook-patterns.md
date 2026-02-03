# Hook Best Practices

Patterns for effective Claude Code hooks.

## Hook Type Selection

### When to Use Prompt Hooks

✅ Complex decision logic
✅ Context-aware validation
✅ Natural language reasoning
✅ Edge case handling

```json
{
  "type": "prompt",
  "prompt": "Analyze this file write for security issues. Check for: path traversal, sensitive file access, credential exposure. Return 'allow' or 'deny' with reason.",
  "timeout": 30
}
```

### When to Use Command Hooks

✅ Deterministic checks
✅ Fast validation
✅ External tool integration
✅ Performance-critical

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 10
}
```

## Matcher Patterns

### Exact Tool Match

```json
"matcher": "Write"
```

### Multiple Tools

```json
"matcher": "Read|Write|Edit"
```

### All File Operations

```json
"matcher": "Read|Write|Edit|Glob|Grep"
```

### All MCP Tools

```json
"matcher": "mcp__.*"
```

### Specific MCP Server

```json
"matcher": "mcp__github__.*"
```

### Dangerous Operations

```json
"matcher": "mcp__.*__(delete|remove|drop).*"
```

### All Tools

```json
"matcher": "*"
```

## PreToolUse Patterns

### Path Validation

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "prompt",
      "prompt": "Check file path safety: $TOOL_INPUT. Deny if: 1) Path contains '..', 2) Targets system files, 3) Accesses .env or credentials. Return {permissionDecision: 'allow'|'deny', reason: '...'}"
    }]
  }]
}
```

### Bash Command Validation

```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "prompt",
      "prompt": "Evaluate bash command safety: $TOOL_INPUT. DENY commands with: rm -rf, sudo, curl|bash, wget|sh. Return allow/deny with reason."
    }]
  }]
}
```

### MCP Action Approval

```json
{
  "PreToolUse": [{
    "matcher": "mcp__github__create_issue",
    "hooks": [{
      "type": "prompt",
      "prompt": "Review GitHub issue creation: $TOOL_INPUT. Ensure: clear title, appropriate labels, no sensitive info. Return allow/deny."
    }]
  }]
}
```

## PostToolUse Patterns

### Edit Quality Check

```json
{
  "PostToolUse": [{
    "matcher": "Edit",
    "hooks": [{
      "type": "prompt",
      "prompt": "Review edit result: $TOOL_RESULT. Check for: syntax errors, removed error handling, security issues. Provide feedback if issues found."
    }]
  }]
}
```

### Log Operations

```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit|Bash",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/log-operation.sh"
    }]
  }]
}
```

## Stop Patterns

### Task Completion Verification

```json
{
  "Stop": [{
    "matcher": "*",
    "hooks": [{
      "type": "prompt",
      "prompt": "Verify task completion: 1) Original request addressed? 2) Tests pass? 3) No pending TODOs? Return 'approve' to stop or 'block' with remaining work.",
      "timeout": 30
    }]
  }]
}
```

### Quality Gate

```json
{
  "Stop": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "npm test && npm run lint",
      "timeout": 120
    }]
  }]
}
```

## SessionStart Patterns

### Context Loading

```json
{
  "SessionStart": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh",
      "timeout": 10
    }]
  }]
}
```

**load-context.sh:**
```bash
#!/bin/bash
# Detect project type and load context

if [ -f "package.json" ]; then
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
  echo "Node.js project detected"
fi

if [ -f "pyproject.toml" ]; then
  echo "export PROJECT_TYPE=python" >> "$CLAUDE_ENV_FILE"
  echo "Python project detected"
fi
```

## Command Hook Script Patterns

### Standard Template

```bash
#!/bin/bash
set -euo pipefail

# Read input
input=$(cat)

# Parse with jq
tool_name=$(echo "$input" | jq -r '.tool_name')
tool_input=$(echo "$input" | jq -r '.tool_input')

# Validation logic
# ...

# Output decision
echo '{"decision": "allow"}'
exit 0
```

### Error Response

```bash
# Deny with reason
echo '{"decision": "deny", "reason": "Path traversal detected"}' >&2
exit 2
```

### System Message

```bash
# Add context for Claude
echo '{
  "decision": "allow",
  "systemMessage": "Note: This file is in a sensitive directory. Please be careful with changes."
}'
```

## Timeout Guidelines

| Hook Type | Operation | Recommended |
|-----------|-----------|-------------|
| Prompt | Simple check | 10-15s |
| Prompt | Complex analysis | 30s |
| Command | Quick validation | 5-10s |
| Command | External call | 30-60s |
| Command | Build/test | 120s+ |

## Parallel Execution Notes

All matching hooks run in parallel:

```json
{
  "PreToolUse": [{
    "matcher": "Write",
    "hooks": [
      {"type": "command", "command": "check1.sh"},  // Parallel
      {"type": "command", "command": "check2.sh"},  // Parallel
      {"type": "prompt", "prompt": "..."}           // Parallel
    ]
  }]
}
```

Design hooks to be independent - they cannot see each other's output.
