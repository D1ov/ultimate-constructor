# Antipatterns

Common mistakes to avoid when creating Claude Code components.

## Skill Antipatterns

### ❌ Vague Description

**Wrong:**
```yaml
description: Helps with testing stuff.
```

**Right:**
```yaml
description: |
  Create and run API endpoint tests. Use when user mentions
  "test API", "endpoint test", "integration test".
  NOT for: unit tests, UI tests, load testing.
```

**Why:** Vague descriptions lead to incorrect activation and user confusion.

---

### ❌ Missing Boundaries

**Wrong:**
```yaml
description: Handle all testing needs.
```

**Right:**
```yaml
description: |
  API integration testing.
  NOT for: unit tests, E2E tests, performance tests.
```

**Why:** Without boundaries, skills activate incorrectly.

---

### ❌ First/Second Person in Description

**Wrong:**
```yaml
description: I help you write better tests.
```

**Right:**
```yaml
description: Create comprehensive test suites with proper assertions.
```

**Why:** Descriptions should be objective, third-person statements.

---

### ❌ Monolithic SKILL.md

**Wrong:**
- 800+ line SKILL.md with everything

**Right:**
- < 300 line SKILL.md with essentials
- references/ for detailed content
- scripts/ for automation

**Why:** Large files slow context loading and overwhelm users.

---

### ❌ No Examples

**Wrong:**
```markdown
## Usage
Use the API to create resources.
```

**Right:**
```markdown
## Usage

```javascript
const resource = await api.create({
  name: 'example',
  type: 'document'
});
```
```

**Why:** Examples are essential for understanding.

---

### ❌ Overly Broad Tool Permissions

**Wrong:**
```yaml
allowed-tools: Bash, Write, Edit, Task
```

**Right:**
```yaml
allowed-tools: Read, Write, Bash(npm:test, git:status)
```

**Why:** Minimal permissions reduce risk and unexpected behavior.

## Agent Antipatterns

### ❌ Missing Tool Restrictions

**Wrong:**
```yaml
name: code-reviewer
description: Review code
# No tools specified - inherits ALL
```

**Right:**
```yaml
name: code-reviewer
description: Review code
tools: Read, Grep, Glob
```

**Why:** Unrestricted agents can perform unintended actions.

---

### ❌ Wrong Model Selection

**Wrong:**
```yaml
# Opus for simple search
name: file-finder
model: opus
```

**Right:**
```yaml
# Haiku for simple search
name: file-finder
model: haiku
```

**Why:** Wrong model wastes resources or provides poor results.

---

### ❌ Vague Instructions

**Wrong:**
```markdown
# Agent

Do the task well.
```

**Right:**
```markdown
# Code Reviewer

## Workflow
1. Read changed files
2. Check for: security issues, performance, style
3. Output findings as JSON

## Output Format
{findings: [{file, line, issue, severity}]}
```

**Why:** Agents need specific, actionable instructions.

## Hook Antipatterns

### ❌ Hardcoded Paths

**Wrong:**
```json
{
  "command": "bash /home/user/scripts/validate.sh"
}
```

**Right:**
```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

**Why:** Hardcoded paths break on different systems.

---

### ❌ No Timeout

**Wrong:**
```json
{
  "type": "command",
  "command": "npm install"
}
```

**Right:**
```json
{
  "type": "command",
  "command": "npm install",
  "timeout": 120
}
```

**Why:** Long operations can hang without timeouts.

---

### ❌ Invalid JSON Output

**Wrong:**
```bash
echo "Error: something went wrong"
exit 2
```

**Right:**
```bash
echo '{"error": "something went wrong"}' >&2
exit 2
```

**Why:** Hooks must output valid JSON.

---

### ❌ Missing Wrapper in Plugin Hooks

**Wrong (plugin hooks.json):**
```json
{
  "PreToolUse": [...]
}
```

**Right:**
```json
{
  "hooks": {
    "PreToolUse": [...]
  }
}
```

**Why:** Plugin hooks.json requires the `hooks` wrapper.

---

### ❌ Relying on Hook Order

**Wrong:**
```json
{
  "hooks": [
    {"command": "step1.sh"},  // Must run first
    {"command": "step2.sh"}   // Depends on step1
  ]
}
```

**Why:** Hooks run in parallel, not sequentially.

## Plugin Antipatterns

### ❌ Missing Required Fields

**Wrong:**
```json
{
  "name": "my-plugin"
}
```

**Right:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description"
}
```

**Why:** Manifest validation requires name, version, description.

---

### ❌ Invalid Version Format

**Wrong:**
```json
{
  "version": "v1"
}
```

**Right:**
```json
{
  "version": "1.0.0"
}
```

**Why:** Must use semantic versioning format.

---

### ❌ Long Plugin Names

**Wrong:**
```json
{
  "name": "my-super-awesome-code-quality-and-testing-plugin"
}
```

**Right:**
```json
{
  "name": "code-quality"
}
```

**Why:** Long names make commands tedious: `/my-super-awesome...:cmd`

## General Antipatterns

### ❌ Placeholder Content

**Wrong:**
```markdown
## Examples
TODO: Add examples

## Configuration
TBD
```

**Why:** Placeholders indicate incomplete work.

---

### ❌ Outdated Information

**Wrong:**
```markdown
# Framework Guide (v1.x)
[Content for version 1, but framework is now v3]
```

**Right:**
```markdown
# Framework Guide (v3.x)
> For v1-2 migration, see references/migration.md
```

**Why:** Outdated info causes user frustration.

---

### ❌ No Error Handling Guidance

**Wrong:**
```markdown
## Usage
Call the API endpoint.
```

**Right:**
```markdown
## Usage
Call the API endpoint.

## Error Handling
- 404: Resource not found - verify ID
- 401: Authentication failed - check token
- 500: Server error - retry with backoff
```

**Why:** Users need help when things go wrong.
