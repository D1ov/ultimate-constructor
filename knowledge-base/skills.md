# Skills Documentation

Complete guide to creating Claude Code skills: structure, frontmatter, progressive disclosure, and best practices.

## Overview

Skills are domain knowledge files that load into Claude's context when activated. They provide specialized expertise for specific tasks without persistent state.

## Skill Structure

### Minimal Structure
```
my-skill/
└── SKILL.md
```

### Recommended Structure
```
my-skill/
├── SKILL.md                  # Main skill file (< 500 lines)
├── references/               # Detailed documentation
│   ├── api-guide.md
│   └── patterns.md
├── scripts/                  # Utility scripts
│   └── validate.py
└── examples/                 # Example files
    └── sample.json
```

## SKILL.md Format

### YAML Frontmatter

```yaml
---
name: my-skill
description: |
  Brief description of what the skill does.
  Use when user mentions "trigger phrase 1", "trigger phrase 2".
  NOT for: what this skill should not handle.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash(npm:*, git:*)
model: inherit
context: project
---
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase, hyphens, max 64 chars) |
| `description` | When to activate, triggers, boundaries |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `version` | Semantic version | - |
| `allowed-tools` | Pre-approved tools | Ask for permission |
| `model` | sonnet, opus, haiku, inherit | inherit |
| `context` | project, user, global | project |
| `hooks` | Skill-specific hooks | - |

## Description Best Practices

### Include
1. **What** the skill does (action verbs)
2. **When** to use it (trigger phrases)
3. **What NOT** to use it for (boundaries)

### Format
```yaml
description: |
  Create and validate API endpoints. Use when user mentions
  "create endpoint", "API route", "REST API", "add API".
  NOT for: frontend components, database schemas.
```

### Avoid
- First/second person ("I", "you", "your")
- Vague descriptions
- Missing boundaries

## Progressive Disclosure

### Layer 1: SKILL.md (< 500 lines)
Essential information for immediate use:
- Quick start / overview
- Common patterns
- Key commands
- Links to details

### Layer 2: /references/ (detailed docs)
In-depth documentation:
- Complete API references
- Advanced patterns
- Edge cases
- Troubleshooting

### Layer 3: /scripts/ (automation)
Utility scripts for validation and automation.

### Linking Pattern
```markdown
## Quick Start
[Basic usage here]

For advanced patterns, see [references/patterns.md](references/patterns.md).
```

## Tool Permissions

### Pre-approve Specific Tools
```yaml
allowed-tools: Read, Write, Edit, Glob, Grep
```

### Bash Command Scoping
```yaml
allowed-tools: Bash(git:*, npm:test, npm:build)
```

Patterns:
- `git:*` - All git commands
- `npm:test` - Only npm test
- `npm:*` - All npm commands

### MCP Tool Permissions
```yaml
allowed-tools: mcp__github__create_issue, mcp__slack__post_message
```

## Content Writing Style

### DO
- Use imperative form ("Create", "Run", "Check")
- Third-person descriptions
- Specific, actionable instructions
- Include examples
- Document boundaries (DO/DON'T)

### DON'T
- Use "I" or "you"
- Vague instructions
- Missing examples
- Monolithic content (> 500 lines)

## Activation

Skills activate when:
1. Explicitly loaded via `/skill` command
2. Description matches user intent
3. Loaded by another skill/agent

### Auto-activation
Include trigger phrases in description:
```yaml
description: |
  Use when user mentions "create hook", "add PreToolUse hook",
  "validate tool use", "event-driven automation".
```

## Skill Location

### Project Level
```
.claude/skills/my-skill/SKILL.md
```

### User Level
```
~/.claude/skills/my-skill/SKILL.md
```

### Plugin Level
```
plugin/skills/my-skill/SKILL.md
```

## Example Skill

```yaml
---
name: api-testing
description: |
  Create and run API tests. Use when user mentions "test API",
  "API testing", "endpoint testing", "REST tests", "integration tests".
  NOT for: unit tests, UI tests, load testing.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash(npm:test, curl:*)
---

# API Testing Skill

Create comprehensive API tests with proper assertions and error handling.

## Quick Start

1. Identify endpoints to test
2. Create test file in `tests/api/`
3. Write test cases with assertions
4. Run with `npm test`

## Test Structure

```javascript
describe('GET /api/users', () => {
  it('returns user list', async () => {
    const response = await request(app).get('/api/users');
    expect(response.status).toBe(200);
    expect(response.body).toBeArray();
  });
});
```

## Common Patterns

### Authentication Tests
Test protected endpoints with valid/invalid tokens.

### Error Handling
Test 400, 401, 403, 404, 500 responses.

### Validation Tests
Test input validation and error messages.

For detailed patterns, see [references/patterns.md](references/patterns.md).

## DON'T
- Test implementation details
- Use hardcoded test data in production
- Skip error case testing
- Ignore async/await properly
```

## Validation Checklist

- [ ] Name: lowercase, hyphens, ≤64 chars
- [ ] Description: has WHAT, WHEN, NOT FOR
- [ ] Description: third person, no "I"/"you"
- [ ] SKILL.md: < 500 lines
- [ ] Has references/ for detailed content
- [ ] Includes DO/DON'T sections
- [ ] Has working examples
- [ ] All referenced files exist
