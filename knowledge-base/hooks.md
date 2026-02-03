# Hooks Documentation

Complete guide to Claude Code hooks: event-driven automation, validation, and integration.

## Overview

Hooks are event-driven automation scripts that execute in response to Claude Code events. Use hooks to:
- Validate operations before execution
- React to tool results
- Enforce completion standards
- Load project context
- Integrate external tools

## Hook Types

### Prompt-Based Hooks (Recommended)

LLM-driven decision making for context-aware validation:

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this operation is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

**Benefits:**
- Context-aware decisions
- Flexible evaluation logic
- Better edge case handling
- Easier to maintain

**Supported events:** Stop, SubagentStop, UserPromptSubmit, PreToolUse

### Command Hooks

Bash commands for deterministic checks:

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**Use for:**
- Fast deterministic validations
- File system operations
- External tool integrations
- Performance-critical checks

## Hook Events

| Event | When | Use For |
|-------|------|---------|
| PreToolUse | Before tool runs | Validation, modification |
| PostToolUse | After tool completes | Feedback, logging |
| UserPromptSubmit | User sends prompt | Context, validation |
| Stop | Agent considers stopping | Completeness check |
| SubagentStop | Subagent completes | Task validation |
| SessionStart | Session begins | Context loading |
| SessionEnd | Session ends | Cleanup, logging |
| PreCompact | Before context compact | Preserve info |
| Notification | User notified | Logging, reactions |

## Configuration Formats

### Plugin Format (hooks/hooks.json)

```json
{
  "description": "Optional description",
  "hooks": {
    "PreToolUse": [...],
    "Stop": [...],
    "SessionStart": [...]
  }
}
```

**Note:** Plugin hooks require the `"hooks": {}` wrapper.

### Settings Format (.claude/settings.json)

```json
{
  "PreToolUse": [...],
  "Stop": [...],
  "SessionStart": [...]
}
```

**Note:** Settings format has events at top level (no wrapper).

## Matchers

### Exact Match
```json
"matcher": "Write"
```

### Multiple Tools
```json
"matcher": "Read|Write|Edit"
```

### Wildcard (All)
```json
"matcher": "*"
```

### Regex Patterns
```json
"matcher": "mcp__.*__delete.*"
```

### Common Patterns
- `mcp__.*` - All MCP tools
- `Read|Write|Edit` - File operations
- `Bash` - Shell commands
- `mcp__github__.*` - GitHub MCP tools

## PreToolUse

Execute before tool runs. Approve, deny, or modify.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate file write safety. Check: system paths, credentials, path traversal. Return 'approve' or 'deny'."
        }
      ]
    }
  ]
}
```

**Output:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explanation for Claude"
}
```

## PostToolUse

Execute after tool completes. React to results.

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze edit for potential issues: syntax errors, security vulnerabilities."
        }
      ]
    }
  ]
}
```

## Stop

Execute when agent considers stopping. Validate completeness.

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify task completion: tests run, build succeeded. Return 'approve' to stop or 'block' to continue."
        }
      ]
    }
  ]
}
```

**Decision output:**
```json
{
  "decision": "approve|block",
  "reason": "Explanation",
  "systemMessage": "Additional context"
}
```

## SessionStart

Execute when session begins. Load context.

```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Persist environment variables:**
```bash
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
```

## Environment Variables

Available in command hooks:
- `$CLAUDE_PROJECT_DIR` - Project root
- `$CLAUDE_PLUGIN_ROOT` - Plugin directory
- `$CLAUDE_ENV_FILE` - SessionStart only: persist env vars
- `$CLAUDE_CODE_REMOTE` - Set if remote context

**Always use ${CLAUDE_PLUGIN_ROOT} for portable paths.**

## Hook Input

All hooks receive JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse"
}
```

**Event-specific fields:**
- PreToolUse/PostToolUse: `tool_name`, `tool_input`, `tool_result`
- UserPromptSubmit: `user_prompt`
- Stop/SubagentStop: `reason`

Access in prompts: `$TOOL_INPUT`, `$TOOL_RESULT`, `$USER_PROMPT`

## Hook Output

### Standard Output
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

### Exit Codes
- `0` - Success (stdout in transcript)
- `2` - Blocking error (stderr to Claude)
- Other - Non-blocking error

## Execution Model

### Parallel Execution
All matching hooks run in parallel:
- Hooks don't see each other's output
- Non-deterministic ordering
- Design for independence

### Timeouts
- Command hooks: 60s default
- Prompt hooks: 30s default

## Lifecycle

**Hooks load at session start.** Changes require restart.

To test changes:
1. Edit hook configuration
2. Exit Claude Code
3. Restart: `claude`
4. Test with `claude --debug`

## Debugging

### Enable Debug Mode
```bash
claude --debug
```

### Test Command Hooks
```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "/test"}}' | \
  bash script.sh
echo "Exit code: $?"
```

### View Loaded Hooks
```
/hooks
```

## Best Practices

### DO
- ✅ Use prompt hooks for complex logic
- ✅ Use ${CLAUDE_PLUGIN_ROOT} for paths
- ✅ Validate all inputs in command hooks
- ✅ Quote bash variables
- ✅ Set appropriate timeouts
- ✅ Return structured JSON

### DON'T
- ❌ Use hardcoded paths
- ❌ Trust input without validation
- ❌ Create long-running hooks
- ❌ Rely on execution order
- ❌ Log sensitive information
