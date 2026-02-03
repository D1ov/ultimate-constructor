# Ultimate Constructor

Ultimate constructor for Claude Code components with full self-* pipeline. Creates skills, agents, plugins, and hooks through guided Q&A with self-testing, self-review, self-acceptance, self-refactor, self-finalizer, and self-architect capabilities.

## Installation

### Method 1: --plugin-dir (Recommended)

```bash
claude --plugin-dir "/path/to/ultimate-constructor"
```

### Method 2: settings.json

Add to `~/.claude/settings.json`:

```json
{
  "plugins": {
    "ultimate-constructor": {
      "path": "/path/to/ultimate-constructor",
      "enabled": true
    }
  }
}
```

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

## Commands

| Command | Description |
|---------|-------------|
| `/uc:create [type] [name]` | Create new component (skill, agent, plugin, hook) |
| `/uc:extract [type]` | Extract patterns from conversation |
| `/uc:improve <path>` | Improve existing component |
| `/uc:status [detail]` | Show statistics and learned patterns |

## Quick Start

### Create a Skill

```
/uc:create skill
```

The constructor will:
1. Ask about purpose, triggers, boundaries
2. Design structure (architect)
3. Create files (executor)
4. Validate (tester)
5. Score quality (reviewer)
6. Improve if needed (refactor)
7. Finalize (finalizer)

### Extract Patterns

After a productive session:

```
/uc:extract
```

Analyzes conversation for reusable patterns.

### Improve Existing

```
/uc:improve ./my-skill
```

Runs quality analysis and suggests improvements.

## Architecture: Full Organization Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FULL ORGANIZATION PIPELINE (15+ agents)                  │
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
│  ║   Refactor ←─(loop if <80)── Optimizer → Learner → Finalizer          ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Layer | Agent | Purpose |
|-------|-------|---------|
| **Executive** | Architect | Design component structure |
| | Planner | Create execution plan |
| | Executor | Create files |
| | Delegator | Coordinate sub-agents |
| **Quality** | Tester | Validate structure |
| | Reviewer | Score quality |
| | QA | Deep quality analysis |
| | Validator | Schema validation |
| **Security** | Pentester | Find vulnerabilities |
| | Auditor | Audit trail |
| | Compliance | Standards check |
| **Evolution** | Refactor | Apply improvements |
| | Optimizer | Performance tuning |
| | Learner | Extract patterns |
| | Finalizer | Complete and document |

### Organization Levels

During creation, choose organization level:

| Level | Agents | Best For |
|-------|--------|----------|
| **Full** | 15+ | Complex agents/skills needing self-critique |
| **Core** | 8-10 | Standard components |
| **Minimal** | 1 | Simple hooks, basic components |

## Quality Scoring

Components are scored 0-100:

| Criterion | Weight |
|-----------|--------|
| Trigger specificity | 20% |
| Progressive disclosure | 15% |
| Boundaries clarity | 15% |
| Antipattern awareness | 15% |
| Resource organization | 10% |
| Writing style | 10% |
| Examples quality | 10% |
| Documentation | 5% |

Pass threshold: **80/100**

## Knowledge Base

Complete offline documentation:

- `knowledge-base/sub-agents.md` - Sub-agent creation
- `knowledge-base/plugins.md` - Plugin structure
- `knowledge-base/skills.md` - Skill format
- `knowledge-base/hooks.md` - Hook events

JSON schemas for validation:
- `schemas/skill-frontmatter.json`
- `schemas/agent-frontmatter.json`
- `schemas/plugin-manifest.json`
- `schemas/hooks-config.json`

## Self-Learning

### Constructor Self-Learning

The constructor itself learns from sessions:

- **Patterns detected**: Workflows, validations, fixes, antipatterns
- **Stored in**: `learned/patterns.json`
- **Statistics**: `learned/stats.json`

Enable via Stop and PostToolUse hooks.

### Created Components Self-Learning

During creation, Architect asks: **"Enable self-learning capability?"**

If enabled, the created component gets:

```
component-name/
├── hooks/
│   └── hooks.json          # Self-learning hooks
└── learned/
    └── patterns.json       # Pattern storage
```

**What self-learning does:**
- **Stop hook**: Analyzes each session for patterns
- **PostToolUse hook**: Validates changes and tracks edits
- **Pattern storage**: Accumulates learned knowledge
- **Self-review**: Identifies improvements automatically

**Pattern types detected:**
| Type | Description |
|------|-------------|
| `correction` | User fixed something |
| `resolution` | Error was resolved |
| `workflow` | Repeated sequence detected |
| `quality` | Improvement opportunity |

Components with self-learning become smarter over time.

## Output Location

All created components go to:

```
${PROJECT_ROOT}/NEW/skills/<component-name>/
```

Or configure via `ULTIMATE_CONSTRUCTOR_OUTPUT` environment variable.

## Component Types

### Skills
Domain knowledge files (SKILL.md + references + scripts)

### Agents
Specialized sub-agents (.md with YAML frontmatter)

### Plugins
Full packages (plugin.json + commands + agents + skills + hooks)

### Hooks
Event-driven automation (hooks.json)

## Directory Structure

```
ultimate-constructor/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/                     # User commands
│   ├── create.md
│   ├── extract.md
│   ├── improve.md
│   └── status.md
├── skills/
│   └── constructor/
│       └── SKILL.md             # Main skill
├── agents/                       # Full 15-agent organization
│   ├── constructor-architect.md      # Executive Layer
│   ├── constructor-planner.md
│   ├── constructor-executor.md
│   ├── constructor-delegator.md
│   ├── constructor-tester.md         # Quality Layer
│   ├── constructor-reviewer.md
│   ├── constructor-qa.md
│   ├── constructor-validator.md
│   ├── constructor-pentester.md      # Security Layer
│   ├── constructor-auditor.md
│   ├── constructor-compliance.md
│   ├── constructor-refactor.md       # Evolution Layer
│   ├── constructor-optimizer.md
│   ├── constructor-learner.md
│   ├── constructor-acceptance.md
│   └── constructor-finalizer.md
├── scripts/
│   ├── orchestrator.py          # Pipeline coordination
│   ├── validate_and_learn.py
│   └── ...
├── knowledge-base/               # Documentation & schemas
├── references/                   # Best practices
├── templates/
│   ├── agent-organization/       # Full agent org template
│   ├── skill-organization/       # Full skill org template
│   └── ...
├── hooks/
│   └── hooks.json               # Self-learning hooks
└── learned/                      # Patterns & stats
```

## Best Practices Applied

From analyzed examples:
- Progressive disclosure (skill-coach)
- Specific triggers (langgraph-expert)
- Debugging patterns (victoria-debug)
- Self-learning (continuous-learning)

## License

MIT
