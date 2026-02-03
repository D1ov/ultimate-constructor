# Plugin Best Practices

Patterns for well-structured Claude Code plugins.

## Manifest Patterns

### Minimal Manifest

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of functionality"
}
```

### Complete Manifest

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Full-featured plugin for X",
  "author": {
    "name": "Developer Name",
    "email": "dev@example.com",
    "url": "https://example.com"
  },
  "keywords": ["keyword1", "keyword2"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "repository": "https://github.com/user/plugin",
  "license": "MIT"
}
```

## Directory Structure Patterns

### Minimal Plugin

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── main.md
```

### Standard Plugin

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── create.md
│   └── status.md
├── agents/
│   └── helper.md
├── skills/
│   └── domain-skill/
│       └── SKILL.md
└── README.md
```

### Full Plugin

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── create.md
│   ├── update.md
│   ├── delete.md
│   └── status.md
├── agents/
│   ├── analyzer.md
│   └── executor.md
├── skills/
│   └── domain-knowledge/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── hooks/
│   └── hooks.json
├── scripts/
│   └── utilities.py
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## Command Patterns

### Simple Command

```yaml
---
name: status
description: Show current status
---

# Status Command

Display plugin status and statistics.

## Output
- Component count
- Last activity
- Health check
```

### Command with Arguments

```yaml
---
name: create
description: Create a new resource
args:
  - name: type
    description: Resource type
    required: true
  - name: name
    description: Resource name
    required: false
examples:
  - "/plugin:create user"
  - "/plugin:create user john"
---
```

### Command with Tools

```yaml
---
name: analyze
description: Analyze codebase
tools: Read, Grep, Glob
model: haiku
---
```

## Namespacing Pattern

Commands are automatically namespaced:

```
/plugin-name:command-name [args]
```

Examples:
- `/uc:create skill` (ultimate-constructor)
- `/gh:pr create` (github helper)
- `/db:migrate` (database tools)

Choose short, memorable plugin names for easy command invocation.

## Component Integration Patterns

### Command Delegates to Agent

```yaml
---
name: review
description: Review code changes
---

# Review Command

1. Gather changed files
2. Delegate to `code-reviewer` agent
3. Report findings

## Workflow
Launch Task with subagent_type="code-reviewer"
```

### Agent Uses Skill

```yaml
---
name: api-tester
description: Test API endpoints
skills: api-testing-patterns
---
```

### Hook Invokes Command

```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "claude /plugin:validate"
    }]
  }]
}
```

## Hook Configuration Patterns

### Plugin Hooks Wrapper

Always use wrapper format in plugin hooks.json:

```json
{
  "description": "Plugin validation hooks",
  "hooks": {
    "PreToolUse": [...],
    "Stop": [...]
  }
}
```

### Hooks Reference Plugin Root

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/init.sh"
      }]
    }]
  }
}
```

## Documentation Patterns

### README Structure

```markdown
# Plugin Name

Brief description.

## Installation

```bash
claude plugin install plugin-name
```

## Commands

| Command | Description |
|---------|-------------|
| `/name:cmd1` | Description |
| `/name:cmd2` | Description |

## Usage

### Basic Example
[Example usage]

### Advanced Example
[More complex usage]

## Configuration

[Any configuration options]

## License

MIT
```

### CHANGELOG Format

```markdown
# Changelog

## [Unreleased]

### Added
- New feature

### Changed
- Updated behavior

### Fixed
- Bug fix

## [1.0.0] - 2026-01-01

Initial release.
```

## Versioning Pattern

Follow semantic versioning:

- **MAJOR**: Breaking changes to commands or behavior
- **MINOR**: New commands or features (backward compatible)
- **PATCH**: Bug fixes

## Distribution Patterns

### Local Development

```bash
# Link for testing
claude plugin link /path/to/plugin

# Unlink when done
claude plugin unlink plugin-name
```

### Publication

```bash
# Validate before publishing
claude plugin validate

# Publish to marketplace
claude plugin publish
```

## Testing Pattern

Create a test command for plugin validation:

```yaml
---
name: test
description: Run plugin self-tests
tools: Read, Bash
---

# Test Command

Validate plugin components:

1. Check all files exist
2. Validate JSON/YAML syntax
3. Test hook scripts
4. Verify command functionality
```
