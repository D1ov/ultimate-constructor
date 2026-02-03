# Checkpointing Documentation

Automatically track and rewind Claude's edits to quickly recover from unwanted changes.

Source: https://code.claude.com/docs/en/checkpointing

## Overview

Claude Code automatically tracks Claude's file edits as you work, allowing you to quickly undo changes and rewind to previous states if anything gets off track.

## How Checkpoints Work

As you work with Claude, checkpointing automatically captures the state of your code before each edit. This safety net lets you pursue ambitious, wide-scale tasks knowing you can always return to a prior code state.

### Automatic Tracking

Claude Code tracks all changes made by its file editing tools:

- Every user prompt creates a new checkpoint
- Checkpoints persist across sessions (accessible in resumed conversations)
- Automatically cleaned up along with sessions after 30 days (configurable)

### Rewinding Changes

Press `Esc` twice (`Esc` + `Esc`) or use the `/rewind` command to open the rewind menu.

You can choose to restore:

| Option | Description |
|--------|-------------|
| **Conversation only** | Rewind to a user message while keeping code changes |
| **Code only** | Revert file changes while keeping the conversation |
| **Both code and conversation** | Restore both to a prior point in the session |

## Common Use Cases

### Exploring Alternatives

Try different implementation approaches without losing your starting point:

1. Start implementation approach A
2. Decide to try approach B
3. Press `Esc` + `Esc` to rewind
4. Try approach B
5. Compare results and choose the best

### Recovering from Mistakes

Quickly undo changes that introduced bugs or broke functionality:

1. Claude makes changes that break something
2. Press `Esc` + `Esc`
3. Rewind to before the problematic changes
4. Provide better guidance to Claude

### Iterating on Features

Experiment with variations knowing you can revert to working states:

1. Get feature working
2. Try optimization
3. If optimization fails, rewind to working state
4. Try different optimization approach

## Limitations

### Bash Command Changes Not Tracked

Checkpointing does **NOT** track files modified by bash commands:

```bash
rm file.txt          # NOT tracked
mv old.txt new.txt   # NOT tracked
cp source.txt dest.txt  # NOT tracked
```

These file modifications cannot be undone through rewind. Only direct file edits made through Claude's file editing tools (Write, Edit) are tracked.

### External Changes Not Tracked

Checkpointing only tracks files that have been edited within the current session:

- Manual changes you make to files outside of Claude Code are not captured
- Edits from other concurrent sessions are not captured
- Exception: If external changes happen to modify the same files as the current session

### Not a Replacement for Version Control

Checkpoints are designed for quick, session-level recovery:

| Checkpoints | Version Control (Git) |
|-------------|----------------------|
| Local undo | Permanent history |
| Session-level | Project-level |
| 30-day retention | Forever |
| Quick recovery | Collaboration & branching |

**Recommendation**: Continue using Git for commits, branches, and long-term history. Think of checkpoints as "local undo" and Git as "permanent history".

## Integration with Self-Learning

For components with self-learning capabilities, checkpointing can be useful for:

1. **Pattern extraction testing**: Try different approaches, rewind if extraction produces poor results
2. **Agent training**: Test agent modifications, rewind if they don't work
3. **Workflow experimentation**: Try different workflows, rewind to find optimal approach

## Commands

| Command | Description |
|---------|-------------|
| `Esc` + `Esc` | Open rewind menu |
| `/rewind` | Open rewind menu |

## Best Practices

1. **Use checkpoints for experimentation**: Don't be afraid to try bold changes
2. **Combine with Git**: Checkpoint for quick iterations, Git for permanent saves
3. **Understand limitations**: Bash commands and external changes aren't tracked
4. **Use before major changes**: If about to make significant changes, ensure checkpoint is created

## Related Features

- [Interactive mode](/en/interactive-mode) - Keyboard shortcuts and session controls
- [Built-in commands](/en/interactive-mode#built-in-commands) - Accessing checkpoints using `/rewind`
- [CLI reference](/en/cli-reference) - Command-line options
