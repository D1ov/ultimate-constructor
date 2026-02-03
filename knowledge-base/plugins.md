# Plugins Documentation

Complete technical reference for Claude Code plugin system based on official documentation.

Source: https://code.claude.com/docs/en/plugins-reference

## Overview

Plugins are packaged collections of Claude Code extensions that bundle:
- **Skills** - `/name` shortcuts that you or Claude can invoke
- **Agents** - Specialized subagents for specific tasks
- **Commands** - Legacy skill format (use skills/ for new skills)
- **Hooks** - Event handlers that respond to Claude Code events
- **MCP servers** - External tool integrations via Model Context Protocol
- **LSP servers** - Language Server Protocol for code intelligence

## Plugin Directory Structure

```
enterprise-plugin/
├── .claude-plugin/           # Metadata directory
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Default command location (legacy)
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history
```

**IMPORTANT**: The `.claude-plugin/` directory contains ONLY `plugin.json`. All other directories (commands/, agents/, skills/, hooks/) must be at the plugin root, NOT inside `.claude-plugin/`.

## Plugin Manifest Schema (plugin.json)

### Complete Schema

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Required Fields

| Field  | Type   | Description                               | Example              |
|--------|--------|-------------------------------------------|----------------------|
| `name` | string | Unique identifier (kebab-case, no spaces) | `"deployment-tools"` |

### Metadata Fields

| Field         | Type   | Description                         | Example                                            |
|---------------|--------|-------------------------------------|---------------------------------------------------|
| `version`     | string | Semantic version                    | `"2.1.0"`                                          |
| `description` | string | Brief explanation of plugin purpose | `"Deployment automation tools"`                    |
| `author`      | object | Author information                  | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | Documentation URL                   | `"https://docs.example.com"`                       |
| `repository`  | string | Source code URL                     | `"https://github.com/user/plugin"`                 |
| `license`     | string | License identifier                  | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Discovery tags                      | `["deployment", "ci-cd"]`                          |

### Component Path Fields

| Field          | Type           | Description                              | Example                                |
|----------------|----------------|------------------------------------------|----------------------------------------|
| `commands`     | string\|array  | Additional command files/directories     | `"./custom/cmd.md"` or `["./cmd1.md"]` |
| `agents`       | string\|array  | Additional agent files                   | `"./custom/agents/"`                   |
| `skills`       | string\|array  | Additional skill directories             | `"./custom/skills/"`                   |
| `hooks`        | string\|object | Hook config path or inline config        | `"./hooks.json"`                       |
| `mcpServers`   | string\|object | MCP config path or inline config         | `"./mcp-config.json"`                  |
| `outputStyles` | string\|array  | Additional output style files/dirs       | `"./styles/"`                          |
| `lspServers`   | string\|object | LSP config for code intelligence         | `"./.lsp.json"`                        |

### Path Behavior Rules

**IMPORTANT**: Custom paths supplement default directories - they don't replace them.

- If `commands/` exists, it's loaded in addition to custom command paths
- All paths must be relative to plugin root and start with `./`
- Commands from custom paths use the same naming and namespacing rules
- Multiple paths can be specified as arrays for flexibility

```json
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Environment Variables

**`${CLAUDE_PLUGIN_ROOT}`**: Contains the absolute path to your plugin directory. Use this in hooks, MCP servers, and scripts.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

## Skills

Skills are directories with `SKILL.md` that create `/name` shortcuts.

### Skill Structure

```
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

### Integration Behavior

- Skills are automatically discovered when the plugin is installed
- Claude can invoke them automatically based on task context
- Skills can include supporting files alongside SKILL.md

## Agents

Agents are specialized subagents defined in markdown files.

### Agent File Format

```markdown
---
description: What this agent specializes in
capabilities: ["task1", "task2", "task3"]
---

# Agent Name

Detailed description of the agent's role, expertise, and when Claude should invoke it.

## Capabilities
- Specific task the agent excels at
- Another specialized capability
- When to use this agent vs others

## Context and examples
Provide examples of when this agent should be used.
```

### Integration Points

- Agents appear in the `/agents` interface
- Claude can invoke agents automatically based on task context
- Agents can be invoked manually by users
- Plugin agents work alongside built-in Claude agents

## Hooks

Hooks are event handlers in `hooks/hooks.json` or inline in plugin.json.

### Hook Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

### Available Events

| Event                | When it fires                            |
|----------------------|------------------------------------------|
| `PreToolUse`         | Before a tool call executes. Can block   |
| `PostToolUse`        | After a tool call succeeds               |
| `PostToolUseFailure` | After a tool call fails                  |
| `PermissionRequest`  | When a permission dialog appears         |
| `UserPromptSubmit`   | When user submits a prompt               |
| `Notification`       | When Claude Code sends notifications     |
| `Stop`               | When Claude finishes responding          |
| `SubagentStart`      | When a subagent is spawned               |
| `SubagentStop`       | When a subagent finishes                 |
| `SessionStart`       | At the beginning of sessions             |
| `SessionEnd`         | At the end of sessions                   |
| `PreCompact`         | Before conversation history is compacted |

### Hook Types

- **`command`**: Execute shell commands or scripts
- **`prompt`**: Evaluate a prompt with an LLM
- **`agent`**: Run an agentic verifier with tools

## MCP Servers

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

## LSP Servers

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

### Required LSP Fields

| Field                 | Description                                  |
|-----------------------|----------------------------------------------|
| `command`             | The LSP binary to execute (must be in PATH)  |
| `extensionToLanguage` | Maps file extensions to language identifiers |

### Optional LSP Fields

| Field                   | Description                                          |
|-------------------------|------------------------------------------------------|
| `args`                  | Command-line arguments for the LSP server            |
| `transport`             | Communication: `stdio` (default) or `socket`         |
| `env`                   | Environment variables                                |
| `initializationOptions` | Options passed during initialization                 |
| `settings`              | Settings via `workspace/didChangeConfiguration`      |
| `startupTimeout`        | Max time to wait for startup (ms)                    |
| `shutdownTimeout`       | Max time to wait for shutdown (ms)                   |
| `restartOnCrash`        | Auto-restart if server crashes                       |
| `maxRestarts`           | Maximum restart attempts                             |

## Plugin Installation Scopes

| Scope     | Settings file                 | Use case                                    |
|-----------|-------------------------------|---------------------------------------------|
| `user`    | `~/.claude/settings.json`     | Personal plugins across all projects        |
| `project` | `.claude/settings.json`       | Team plugins shared via version control     |
| `local`   | `.claude/settings.local.json` | Project-specific plugins, gitignored        |
| `managed` | `managed-settings.json`       | Managed plugins (read-only, update only)    |

## CLI Commands

### Install Plugin

```bash
claude plugin install <plugin> [options]

# Examples:
claude plugin install formatter@my-marketplace
claude plugin install formatter@my-marketplace --scope project
claude plugin install formatter@my-marketplace --scope local
```

### Uninstall Plugin

```bash
claude plugin uninstall <plugin> [options]
# Aliases: remove, rm
```

### Enable/Disable Plugin

```bash
claude plugin enable <plugin> [options]
claude plugin disable <plugin> [options]
```

### Update Plugin

```bash
claude plugin update <plugin> [options]
```

## Debugging

```bash
claude --debug
```

Shows:
- Which plugins are being loaded
- Any errors in plugin manifests
- Command, agent, and hook registration
- MCP server initialization

### Common Issues

| Issue                  | Cause                           | Solution                                      |
|------------------------|--------------------------------|-----------------------------------------------|
| Plugin not loading     | Invalid `plugin.json`          | Validate JSON syntax                          |
| Commands not appearing | Wrong directory structure      | Ensure `commands/` at root, not in `.claude-plugin/` |
| Hooks not firing       | Script not executable          | Run `chmod +x script.sh`                      |
| MCP server fails       | Missing `${CLAUDE_PLUGIN_ROOT}`| Use variable for all plugin paths             |
| Path errors            | Absolute paths used            | All paths must be relative and start with `./`|

## Plugin Caching

Claude Code copies plugins to a cache directory for security:

- Plugins cannot reference files outside their copied directory
- Paths that traverse outside the plugin root (like `../shared-utils`) won't work
- Use symlinks for external dependencies if needed

## Version Management

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

Best practices:
- Start at `1.0.0` for first stable release
- Update version in `plugin.json` before distributing
- Document changes in `CHANGELOG.md`
- Use pre-release versions like `2.0.0-beta.1` for testing
