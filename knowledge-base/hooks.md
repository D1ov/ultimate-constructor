# Hooks Documentation

Complete technical reference for Claude Code hooks: event-driven automation, validation, and integration.

Source: https://code.claude.com/docs/en/hooks

## Overview

Hooks are user-defined shell commands or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. Use hooks to:
- Validate operations before execution
- React to tool results
- Enforce completion standards
- Load project context
- Integrate external tools

## Hook Types

### Command Hooks

Execute shell commands or scripts:

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**Use for:**
- Fast deterministic validations
- File system operations
- External tool integrations
- Performance-critical checks

### Prompt Hooks

LLM-driven single-turn evaluation:

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this operation is appropriate: $ARGUMENTS",
  "timeout": 30
}
```

**Response format:**
```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

### Agent Hooks

Spawn a subagent with tool access for complex verification:

```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite. $ARGUMENTS",
  "timeout": 120
}
```

**Available tools:** Read, Grep, Glob (up to 50 turns)

## Hook Events

| Event                | When it fires                                        | Can Block? |
|----------------------|------------------------------------------------------|------------|
| `SessionStart`       | When a session begins or resumes                     | No         |
| `UserPromptSubmit`   | When user submits a prompt, before processing        | Yes        |
| `PreToolUse`         | Before a tool call executes                          | Yes        |
| `PermissionRequest`  | When a permission dialog appears                     | Yes        |
| `PostToolUse`        | After a tool call succeeds                           | No         |
| `PostToolUseFailure` | After a tool call fails                              | No         |
| `Notification`       | When Claude Code sends a notification                | No         |
| `SubagentStart`      | When a subagent is spawned                           | No         |
| `SubagentStop`       | When a subagent finishes                             | Yes        |
| `Stop`               | When Claude finishes responding                      | Yes        |
| `PreCompact`         | Before context compaction                            | No         |
| `SessionEnd`         | When a session terminates                            | No         |

## Matcher Patterns

The `matcher` field is a regex string that filters when hooks fire:

| Event | What matcher filters | Example values |
|-------|---------------------|----------------|
| PreToolUse, PostToolUse, etc. | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| SessionStart | how session started | `startup`, `resume`, `clear`, `compact` |
| SessionEnd | why session ended | `clear`, `logout`, `prompt_input_exit` |
| Notification | notification type | `permission_prompt`, `idle_prompt` |
| SubagentStart/Stop | agent type | `Bash`, `Explore`, `Plan` |
| PreCompact | trigger type | `manual`, `auto` |

**Examples:**
```json
"matcher": "Write"                 // Exact match
"matcher": "Read|Write|Edit"       // Multiple tools
"matcher": "*"                     // All (or omit matcher)
"matcher": "mcp__memory__.*"       // All memory MCP tools
"matcher": "mcp__.*__write.*"      // Any MCP write tool
```

## Configuration Formats

### Plugin Format (hooks/hooks.json)

```json
{
  "description": "Optional description",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### Settings Format (.claude/settings.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

### Skill/Agent Frontmatter

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

## Hook Input

All hooks receive JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

### Event-Specific Input Fields

**PreToolUse/PostToolUse:**
- `tool_name`: Name of the tool
- `tool_input`: Tool parameters
- `tool_use_id`: Unique identifier

**PostToolUse additionally:**
- `tool_response`: Result from tool execution

**PostToolUseFailure:**
- `error`: Error message
- `is_interrupt`: Whether user interrupted

**UserPromptSubmit:**
- `prompt`: User's prompt text

**Stop/SubagentStop:**
- `stop_hook_active`: Whether hook is already active (prevent loops)

**SessionStart:**
- `source`: `startup`, `resume`, `clear`, or `compact`
- `model`: Model identifier

## Hook Output

### Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success - parse JSON from stdout |
| 2 | Blocking error - stderr to Claude |
| Other | Non-blocking error |

### JSON Output Fields

```json
{
  "continue": true,
  "stopReason": "Message when continue is false",
  "suppressOutput": false,
  "systemMessage": "Warning for user"
}
```

## Decision Control

### PreToolUse Decision

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Explanation",
    "updatedInput": {
      "field": "modified_value"
    },
    "additionalContext": "Context for Claude"
  }
}
```

### PermissionRequest Decision

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "updatedPermissions": [],
      "message": "For deny only",
      "interrupt": false
    }
  }
}
```

### Stop/SubagentStop Decision

```json
{
  "decision": "block",
  "reason": "Must provide reason when blocking"
}
```

### UserPromptSubmit/PostToolUse Decision

```json
{
  "decision": "block",
  "reason": "Explanation shown to Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional info"
  }
}
```

## Environment Variables

| Variable | Description | Available In |
|----------|-------------|--------------|
| `$CLAUDE_PROJECT_DIR` | Project root | All hooks |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin directory | Plugin hooks |
| `$CLAUDE_ENV_FILE` | Persist env vars | SessionStart only |
| `$CLAUDE_CODE_REMOTE` | Set if remote | All hooks |

### Persist Environment (SessionStart)

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

## Async Hooks

Run hooks in background without blocking:

```json
{
  "type": "command",
  "command": "/path/to/run-tests.sh",
  "async": true,
  "timeout": 120
}
```

**Limitations:**
- Only `type: "command"` supports async
- Cannot block or return decisions
- Output delivered on next conversation turn

## Best Practices

### DO
- Use `${CLAUDE_PLUGIN_ROOT}` for portable paths
- Validate all inputs in command hooks
- Quote bash variables: `"$VAR"` not `$VAR`
- Set appropriate timeouts
- Return structured JSON
- Check `stop_hook_active` to prevent infinite loops

### DON'T
- Use hardcoded absolute paths
- Trust input without validation
- Create long-running blocking hooks
- Rely on execution order (hooks run in parallel)
- Log sensitive information
- Skip path traversal checks

## Debugging

```bash
# Enable debug mode
claude --debug

# Test command hooks
echo '{"tool_name": "Write", "tool_input": {"file_path": "/test"}}' | \
  bash script.sh
echo "Exit code: $?"

# View loaded hooks
/hooks
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Hook not firing | Wrong matcher | Check regex pattern matches tool name |
| Infinite Stop loop | Missing stop_hook_active check | Check field to prevent re-triggering |
| JSON parse error | Shell profile output | Ensure only JSON in stdout |
| Script not executing | Not executable | Run `chmod +x script.sh` |
| Paths not working | Missing ${CLAUDE_PLUGIN_ROOT} | Use env var for all paths |

## Example: Complete PreToolUse Validator

```bash
#!/bin/bash
# .claude/hooks/validate-write.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Block writes to sensitive paths
if [[ "$FILE_PATH" == /etc/* ]] || [[ "$FILE_PATH" == ~/.ssh/* ]]; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Cannot write to sensitive system paths"
    }
  }'
  exit 0
fi

# Allow safe writes
exit 0
```

## Example: Stop Hook for Task Verification

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify all tasks are complete. Check: 1) Tests pass, 2) No TODO comments, 3) Build succeeds. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```
