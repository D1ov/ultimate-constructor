# Plugins Documentation

Complete guide to creating Claude Code plugins: structure, manifest, components, and distribution.

## Overview

Plugins are packaged collections of Claude Code extensions that bundle:
- Commands (user-invocable slash commands)
- Agents (custom sub-agents)
- Skills (domain knowledge)
- Hooks (event-driven automation)
- MCP servers (external integrations)

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── commands/                 # Slash commands
│   ├── my-command.md
│   └── another.md
├── agents/                   # Custom agents
│   └── my-agent.md
├── skills/                   # Skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/
│   └── hooks.json           # Hook configurations
├── .mcp.json                # MCP server configs (optional)
└── README.md                # Documentation
```

## Plugin Manifest (plugin.json)

The manifest defines plugin metadata and component locations:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of plugin functionality",
  "author": {
    "name": "Developer Name",
    "email": "dev@example.com"
  },
  "keywords": ["keyword1", "keyword2"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcp": "./.mcp.json",
  "repository": "https://github.com/user/my-plugin"
}
```

### Required Fields
- `name`: Lowercase identifier with hyphens
- `version`: Semantic version (e.g., "1.0.0")
- `description`: Brief functionality description

### Optional Fields
- `author`: Author information object
- `keywords`: Search terms for marketplace
- `commands`, `agents`, `skills`, `hooks`: Component paths
- `repository`, `homepage`: URLs
- `license`: SPDX identifier
- `engines`: Claude Code version requirements
- `dependencies`: Other plugin dependencies

## Commands

Commands are slash commands prefixed with plugin name.

### Command File Format
```yaml
---
name: my-command
description: Brief description shown in help
args:
  - name: arg1
    description: First argument
    required: true
  - name: arg2
    description: Optional argument
    default: "value"
examples:
  - "/plugin:my-command arg1-value"
  - "/plugin:my-command arg1 --arg2=custom"
---

# Command Instructions

Detailed instructions for Claude when this command is invoked.

## Workflow
1. Step one
2. Step two
3. Step three
```

### Command Invocation
```
/plugin-name:command-name [arguments]
```

Example:
```
/uc:create skill my-new-skill
```

## Skills in Plugins

Skills provide domain knowledge that loads into context.

### Skill Structure
```
skills/
└── my-skill/
    ├── SKILL.md              # Main skill file
    ├── references/           # Detailed documentation
    └── scripts/              # Utility scripts
```

### SKILL.md Format
```yaml
---
name: my-skill
description: When to activate this skill. Include trigger phrases.
allowed-tools: Read, Write, Bash(npm:*)
---

# Skill Content

Instructions and knowledge for Claude.
```

## Agents in Plugins

Custom agents for specialized tasks.

### Agent File Format
```yaml
---
name: my-agent
description: When to delegate to this agent
tools: Read, Grep, Glob
model: sonnet
---

# Agent Instructions

Detailed behavior instructions.
```

## Hooks in Plugins

Event-driven automation via hooks.json.

### hooks/hooks.json Format
```json
{
  "description": "Plugin hooks description",
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Stop": [...],
    "SessionStart": [...]
  }
}
```

Note: Plugin hooks use wrapper format with `"hooks": {}` container.

## Plugin Installation

### From Marketplace
```bash
claude plugin install plugin-name
```

### From Git Repository
```bash
claude plugin install https://github.com/user/plugin
```

### Local Development
```bash
claude plugin link /path/to/plugin
```

## Plugin Development

### Create New Plugin
```bash
claude plugin create my-plugin
```

### Validate Plugin
```bash
claude plugin validate
```

### Test Locally
```bash
claude plugin link .
claude  # Start Claude Code with plugin loaded
```

### Publish to Marketplace
```bash
claude plugin publish
```

## Best Practices

### Structure
1. Keep plugin.json minimal and accurate
2. Organize components by type (commands/, agents/, skills/)
3. Include README.md with usage examples
4. Add CHANGELOG.md for version history

### Commands
1. Use descriptive names
2. Document all arguments
3. Provide usage examples
4. Handle errors gracefully

### Skills
1. Clear trigger phrases in description
2. Progressive disclosure (main file < 500 lines)
3. Move details to references/

### Agents
1. Minimal tool permissions
2. Specific, actionable instructions
3. Appropriate model selection

### Hooks
1. Use ${CLAUDE_PLUGIN_ROOT} for paths
2. Set appropriate timeouts
3. Prefer prompt hooks for complex logic

## Distribution

### Marketplace Requirements
- Valid plugin.json manifest
- README with documentation
- No security vulnerabilities
- Tested functionality
- Clear description and keywords

### Versioning
Use semantic versioning:
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Example Plugin

```json
{
  "name": "code-quality",
  "version": "1.0.0",
  "description": "Code quality tools: linting, review, documentation",
  "author": {"name": "Developer"},
  "keywords": ["code-quality", "linting", "review"],
  "commands": "./commands/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json"
}
```

Commands:
- `/code-quality:lint` - Run linting
- `/code-quality:review` - Code review
- `/code-quality:docs` - Generate docs

Agents:
- `quality-reviewer` - Automated code review
- `doc-generator` - Documentation generation

Hooks:
- PreToolUse on Write/Edit: Validate code quality
- Stop: Ensure tests pass before completion
