# Skill Best Practices

Patterns for creating high-quality Claude Code skills.

## Description Patterns

### Specific Triggers Pattern

Include quoted phrases that should activate the skill:

```yaml
description: |
  Create API endpoint tests. Use when user mentions "test API",
  "API testing", "endpoint test", "REST test", "integration test".
  NOT for: unit tests, UI tests, load testing.
```

### Domain Shibboleth Pattern

Include technical terms that experts use:

```yaml
description: |
  Implement LangGraph workflows with StateGraph, checkpointing,
  and conditional edges. Use for: "state machine", "workflow graph",
  "LangGraph node", "edge routing".
```

### Negative Boundary Pattern

Explicitly state what NOT to handle:

```yaml
description: |
  ...
  NOT for: database migrations, schema design, ORM configuration.
```

## Structure Patterns

### Progressive Disclosure

**Layer 1: SKILL.md (< 300 lines)**
- Overview and quick start
- Most common patterns
- Links to details

**Layer 2: references/ (detailed)**
- Complete API references
- Advanced patterns
- Edge cases

**Layer 3: scripts/ (automation)**
- Validation scripts
- Example generators

### Reference Link Pattern

```markdown
## Quick Start
[Brief overview]

For advanced patterns, see [references/advanced.md](references/advanced.md).
For troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md).
```

### Section Organization

```markdown
# Skill Name

[Overview - 2-3 sentences]

## Quick Start
[Minimal working example]

## Core Concepts
[Key ideas needed to use skill]

## Patterns
[Common usage patterns]

## Examples
[3+ working examples]

## When NOT to Use
[Boundaries]

## Common Mistakes
[Antipatterns]
```

## Content Patterns

### Imperative Instructions

✅ Good:
```markdown
Create a new test file in tests/api/.
Run the test suite with `npm test`.
Check the coverage report.
```

❌ Bad:
```markdown
You should create a new test file.
I would recommend running the tests.
```

### Table-Based References

```markdown
## API Methods

| Method | Description | Example |
|--------|-------------|---------|
| `create()` | Create new resource | `api.create({...})` |
| `read()` | Read existing | `api.read(id)` |
```

### Checklist Pattern

```markdown
## Validation Checklist

- [ ] Endpoints return correct status codes
- [ ] Error responses include error messages
- [ ] Authentication required for protected routes
- [ ] Input validation rejects invalid data
```

## Tool Permission Patterns

### Minimal Permissions

Only request tools actually needed:

```yaml
# For read-only skill
allowed-tools: Read, Grep, Glob

# For file creation
allowed-tools: Read, Write, Glob

# For execution
allowed-tools: Read, Bash(npm:test, git:status)
```

### Bash Scoping

```yaml
# Specific commands only
allowed-tools: Bash(npm:test, npm:build, git:*)

# Read-only bash
allowed-tools: Bash(cat:*, ls:*, grep:*)
```

## Example Quality

### Complete Examples

Include all necessary context:

```javascript
// Complete example with imports
import { describe, it, expect } from 'vitest';
import { createApp } from './app';

describe('User API', () => {
  it('returns user by ID', async () => {
    const app = createApp();
    const response = await app.get('/api/users/1');
    expect(response.status).toBe(200);
    expect(response.body.id).toBe(1);
  });
});
```

### Before/After Examples

```markdown
### ❌ Before (Wrong)
```javascript
test('user', () => {
  // no assertions
});
```

### ✅ After (Correct)
```javascript
test('returns user data', async () => {
  const user = await getUser(1);
  expect(user.name).toBeDefined();
  expect(user.email).toMatch(/@/);
});
```
```

## Versioning Pattern

For skills with version-sensitive content:

```yaml
---
name: framework-guide
version: 2.0.0
---

# Framework Guide (v3.x)

> **Version Note:** This skill covers Framework v3.x.
> For v2.x, see [references/v2-migration.md](references/v2-migration.md).
```
