---
name: ultimate-constructor
description: |
  Ultimate constructor for Claude Code components with full self-* pipeline.
  Use when user wants to: "create a skill", "create an agent", "create a plugin",
  "create hooks", "build component", "make a new skill", "generate agent",
  "extract skill from chat", "extract patterns", "improve skill", "improve agent".

  Provides guided Q&A for component creation with self-testing, self-review,
  self-acceptance, self-refactor, self-finalizer, and self-architect capabilities.

  NOT for: running existing skills, debugging code, general development,
  modifying existing components outside NEW/skills/.
version: 1.0.0
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Ultimate Constructor

Create Claude Code skills, agents, plugins, and hooks through guided Q&A with comprehensive self-* pipeline validation.

## IMPORTANT: Initial Interaction

When the user invokes `/ultimate-constructor` (or `/uc:constructor`) without a specific subcommand, you MUST first ask what action they want to perform using AskUserQuestion with these options:

1. **Create Component** - Create a new skill, agent, plugin, or hook
2. **Improve Existing** - Analyze and improve an existing component
3. **Extract Patterns** - Extract reusable patterns from conversation
4. **Check Status** - View learned patterns and metrics

DO NOT assume the user wants to create something. Always offer all options first.

If the user directly uses a subcommand (e.g., `/uc:create`, `/uc:improve`), skip this step and proceed with that action.

## Available Commands

| Command | Description |
|---------|-------------|
| `/uc:create [type] [name]` | Create new component (skill, agent, plugin, hook) |
| `/uc:improve <path>` | Analyze and improve existing component |
| `/uc:extract [type]` | Extract patterns from conversation |
| `/uc:status [detail]` | View learned patterns and metrics |

## Quick Start

### Create a Component
```
/uc:create [type] [name]
```
Types: skill, agent, plugin, hook

### Extract Patterns
```
/uc:extract [type]
```
Analyze conversation for reusable patterns.

### Improve Existing
```
/uc:improve <path>
```
Analyze and improve existing component.

### Check Status
```
/uc:status [detail]
```
View learned patterns and metrics.

## Component Types

### Skills
Domain knowledge files that load into Claude's context.
- Structure: `SKILL.md` + optional references/scripts
- Location: `.claude/skills/` or plugin `skills/`

### Agents
Specialized sub-agents for task delegation.
- Structure: Single `.md` file with YAML frontmatter
- Location: `.claude/agents/` or plugin `agents/`

### Plugins
Full packages bundling commands, agents, skills, hooks.
- Structure: Directory with `.claude-plugin/plugin.json`
- Includes: commands/, agents/, skills/, hooks/

### Hooks
Event-driven automation scripts.
- Structure: `hooks/hooks.json` configuration
- Events: PreToolUse, PostToolUse, Stop, SessionStart, etc.

## Self-* Pipeline: Full Organization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FULL ORGANIZATION PIPELINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║                        EXECUTIVE LAYER                                ║ │
│  ║   Architect → Planner → Executor → Delegator                          ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                    ↓                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║                        QUALITY LAYER                                  ║ │
│  ║   Tester → Reviewer → QA → Validator                                  ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                    ↓                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║                       SECURITY LAYER                                  ║ │
│  ║   Pentester → Auditor → Compliance                                    ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                    ↓                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║                      EVOLUTION LAYER                                  ║ │
│  ║   Refactor → Optimizer → Learner → Finalizer                          ║ │
│  ║      ↑                                                                ║ │
│  ║      └──────── (loop if score < 80) ──────────┘                       ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Executive Layer

| Agent | Purpose |
|-------|---------|
| constructor-architect | Design structure, ask questions |
| constructor-planner | Create execution plan with dependencies |
| constructor-executor | Create files from design |
| constructor-delegator | Coordinate multi-agent work |

### Quality Layer

| Agent | Purpose |
|-------|---------|
| constructor-tester | Validate structure and content |
| constructor-reviewer | Score quality, identify improvements |
| constructor-qa | Comprehensive quality assurance |
| constructor-validator | Schema and format validation |

### Security Layer

| Agent | Purpose |
|-------|---------|
| constructor-pentester | Find security vulnerabilities |
| constructor-auditor | Create audit trail, verify integrity |
| constructor-compliance | Check standards compliance |

### Evolution Layer

| Agent | Purpose |
|-------|---------|
| constructor-refactor | Apply improvements |
| constructor-optimizer | Optimize performance |
| constructor-learner | Extract patterns for future |
| constructor-finalizer | Complete and document |
| constructor-acceptance | Final quality gate |

## Knowledge Base

Comprehensive documentation in `knowledge-base/`:

### Documentation
- `sub-agents.md` - Sub-agent creation guide
- `plugins.md` - Plugin structure and manifest
- `skills.md` - Skill format and best practices
- `hooks.md` - Hook events and configuration
- `hooks-reference.md` - Technical hook reference
- `output-styles.md` - Output formatting

### Schemas
- `skill-frontmatter.json` - SKILL.md validation
- `agent-frontmatter.json` - Agent file validation
- `plugin-manifest.json` - plugin.json validation
- `hooks-config.json` - hooks.json validation
- `command-frontmatter.json` - Command validation

## Output Location

All created components go to:
```
${PROJECT_ROOT}/NEW/skills/<component-name>/
```

## Self-Learning

Patterns extracted from sessions stored in:
```
learned/
├── patterns.json        # Extracted patterns
├── test-results/        # Test history
└── improvements/        # Applied improvements
```

### Pattern Types
- **Workflows**: Repeated tool sequences
- **Validations**: Error prevention patterns
- **Antipatterns**: What NOT to do
- **Fixes**: Error → resolution pairs

## Quality Criteria

Components scored on (0-100):

| Criterion | Weight |
|-----------|--------|
| Trigger specificity | 20% |
| Progressive disclosure | 15% |
| Boundaries clarity | 15% |
| Anti-pattern awareness | 15% |
| Resource organization | 10% |
| Writing style | 10% |
| Examples quality | 10% |
| Documentation | 5% |

**Pass threshold: 80/100**

## Workflow Guidelines

### Creating Skills
1. Define clear trigger phrases
2. Specify boundaries (DO/DON'T)
3. Use progressive disclosure (< 500 lines)
4. Include working examples
5. Move details to references/

### Creating Agents
1. Minimal tool permissions
2. Appropriate model selection
3. Clear, actionable instructions
4. Specific delegation criteria

### Creating Plugins
1. Logical component organization
2. Complete plugin.json manifest
3. Namespaced commands
4. Documentation with examples

### Creating Hooks
1. Use prompt hooks for complex logic
2. Use ${CLAUDE_PLUGIN_ROOT} for paths
3. Set appropriate timeouts
4. Return structured JSON

## References

For detailed patterns and best practices:
- `references/skill-patterns.md`
- `references/agent-patterns.md`
- `references/hook-patterns.md`
- `references/plugin-patterns.md`
- `references/antipatterns.md`
- `references/quality-criteria.md`
