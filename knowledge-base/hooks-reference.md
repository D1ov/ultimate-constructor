# Hooks Technical Reference

Complete technical reference for Claude Code hooks configuration.

## Schema Overview

### Plugin Format
```json
{
  "description": "string (optional)",
  "hooks": {
    "<EventName>": [<HookMatcher>, ...]
  }
}
```

### HookMatcher
```json
{
  "matcher": "string (tool pattern)",
  "hooks": [<Hook>, ...]
}
```

### Hook (Prompt)
```json
{
  "type": "prompt",
  "prompt": "string",
  "timeout": 30
}
```

### Hook (Command)
```json
{
  "type": "command",
  "command": "string",
  "timeout": 60
}
```

## Event Reference

### PreToolUse

**Triggers:** Before any tool execution

**Input Fields:**
| Field | Type | Description |
|-------|------|-------------|
| tool_name | string | Name of tool being called |
| tool_input | object | Tool input parameters |

**Output Fields:**
| Field | Type | Description |
|-------|------|-------------|
| permissionDecision | string | "allow", "deny", or "ask" |
| updatedInput | object | Modified tool input (optional) |
| systemMessage | string | Message for Claude context |

**Example:**
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "prompt",
      "prompt": "Check if bash command is safe: $TOOL_INPUT. No rm -rf, no sudo. Return allow/deny."
    }]
  }]
}
```

### PostToolUse

**Triggers:** After tool completes execution

**Input Fields:**
| Field | Type | Description |
|-------|------|-------------|
| tool_name | string | Name of tool that ran |
| tool_input | object | Tool input that was used |
| tool_result | any | Tool execution result |

**Output Behavior:**
- Exit 0: stdout shown in transcript
- Exit 2: stderr fed back to Claude
- systemMessage included in context

**Example:**
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint-written-file.sh"
    }]
  }]
}
```

### Stop

**Triggers:** When main agent considers stopping

**Input Fields:**
| Field | Type | Description |
|-------|------|-------------|
| reason | string | Why agent is stopping |
| stop_reason | string | Detailed stop reason |

**Output Fields:**
| Field | Type | Description |
|-------|------|-------------|
| decision | string | "approve" or "block" |
| reason | string | Explanation of decision |
| systemMessage | string | Context for Claude |

**Example:**
```json
{
  "Stop": [{
    "matcher": "*",
    "hooks": [{
      "type": "prompt",
      "prompt": "Check: 1) Tests pass? 2) Build succeeds? 3) All files saved? Return approve/block with reason."
    }]
  }]
}
```

### SubagentStop

**Triggers:** When subagent considers stopping

Same input/output as Stop, but for subagents.

### UserPromptSubmit

**Triggers:** When user submits a prompt

**Input Fields:**
| Field | Type | Description |
|-------|------|-------------|
| user_prompt | string | User's submitted prompt |

**Output Fields:**
| Field | Type | Description |
|-------|------|-------------|
| systemMessage | string | Context to add |
| block | boolean | Block prompt submission |
| blockReason | string | Reason for blocking |

**Example:**
```json
{
  "UserPromptSubmit": [{
    "matcher": "*",
    "hooks": [{
      "type": "prompt",
      "prompt": "If prompt mentions auth/security, add security best practices reminder."
    }]
  }]
}
```

### SessionStart

**Triggers:** When Claude Code session begins

**Input Fields:**
| Field | Type | Description |
|-------|------|-------------|
| cwd | string | Current working directory |
| session_id | string | Session identifier |

**Special Capabilities:**
- Persist env vars via `$CLAUDE_ENV_FILE`
- Load project context
- Set up integrations

**Example:**
```json
{
  "SessionStart": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/detect-project.sh",
      "timeout": 10
    }]
  }]
}
```

### SessionEnd

**Triggers:** When session ends

**Use For:**
- Cleanup temporary files
- Log session metrics
- Save state

### PreCompact

**Triggers:** Before context compaction

**Use For:**
- Add critical information to preserve
- Summarize session state

### Notification

**Triggers:** When Claude sends notification to user

**Use For:**
- Log notifications
- Trigger external alerts

## Matcher Patterns

### Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `exact` | Exact tool name | `"Write"` |
| `a\|b\|c` | Any of listed | `"Read\|Write\|Edit"` |
| `*` | All tools | `"*"` |
| `regex` | Regex pattern | `"mcp__.*"` |

### Common Matchers

```json
// File operations
"matcher": "Read|Write|Edit|Glob|Grep"

// All MCP tools
"matcher": "mcp__.*"

// Specific MCP server
"matcher": "mcp__github__.*"

// Dangerous MCP operations
"matcher": "mcp__.*__(delete|remove|drop).*"

// All tools
"matcher": "*"
```

## Environment Variables

| Variable | Availability | Description |
|----------|--------------|-------------|
| `CLAUDE_PROJECT_DIR` | All hooks | Project root path |
| `CLAUDE_PLUGIN_ROOT` | Plugin hooks | Plugin directory |
| `CLAUDE_ENV_FILE` | SessionStart | File to persist env vars |
| `CLAUDE_CODE_REMOTE` | All hooks | Set if remote context |

## Command Hook Script Template

```bash
#!/bin/bash
set -euo pipefail

# Read JSON input from stdin
input=$(cat)

# Parse fields with jq
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
tool_input=$(echo "$input" | jq -r '.tool_input // empty')
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Validate inputs
if [[ -z "$tool_name" ]]; then
  echo '{"decision": "deny", "reason": "Missing tool name"}' >&2
  exit 2
fi

# Check for dangerous patterns
if [[ "$file_path" == *".."* ]]; then
  echo '{"decision": "deny", "reason": "Path traversal detected"}' >&2
  exit 2
fi

# Allow if checks pass
echo '{"decision": "allow"}'
exit 0
```

## Output JSON Schemas

### PreToolUse Output
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {}
  },
  "systemMessage": "string",
  "continue": true,
  "suppressOutput": false
}
```

### Stop/SubagentStop Output
```json
{
  "decision": "approve|block",
  "reason": "string",
  "systemMessage": "string"
}
```

### General Output
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "string"
}
```

## Timeout Defaults

| Hook Type | Default | Maximum |
|-----------|---------|---------|
| Prompt | 30s | 300s |
| Command | 60s | 600s |

## Error Handling

### Exit Codes
| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | stdout shown in transcript |
| 2 | Blocking error | stderr fed back to Claude |
| 1, 3+ | Non-blocking | Warning logged |

### Common Errors

**Invalid JSON output:**
```bash
# Bad
echo "Error occurred"

# Good
echo '{"error": "Error occurred"}' >&2
exit 2
```

**Timeout exceeded:**
- Hook killed after timeout
- Error logged
- Operation continues (fail-open)

## Debugging

### Enable Debug Logging
```bash
claude --debug
```

### Test Hook Manually
```bash
# Create test input
echo '{"tool_name":"Write","tool_input":{"file_path":"/test.txt"}}' > /tmp/test.json

# Run hook
cat /tmp/test.json | bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh

# Check output and exit code
echo "Exit: $?"
```

### Validate JSON Output
```bash
output=$(./hook.sh < input.json)
echo "$output" | jq .
```
