# Changelog

All notable changes to Ultimate Constructor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-02-03

### Added

#### Commands
- `/uc:create` - Create new Claude Code components (skills, agents, plugins, hooks)
- `/uc:extract` - Extract reusable patterns from conversation
- `/uc:improve` - Improve existing components with self-review pipeline
- `/uc:status` - Show learned patterns and quality metrics

#### Self-* Agents
- `constructor-architect` - Design component structure through Q&A
- `constructor-executor` - Create files from architect design
- `constructor-tester` - Validate structure and content
- `constructor-reviewer` - Quality analysis and scoring (0-100)
- `constructor-refactor` - Apply improvements (max 3 iterations)
- `constructor-acceptance` - Final quality gate
- `constructor-finalizer` - Update changelog and complete

#### Knowledge Base
- Complete Claude Code documentation (sub-agents, plugins, skills, hooks)
- JSON schemas for validation (skill, agent, plugin, hooks, MCP, LSP)
- Best practice references and antipattern documentation

#### Scripts
- `extract_patterns.py` - Pattern extraction from transcripts
- `validate_component.py` - Component validation
- `run_self_tests.py` - Self-test execution
- `analyze_quality.py` - Quality metrics analysis
- `update_changelog.py` - Changelog automation
- `self_improve.py` - Self-learning engine

#### Templates
- Skill template (SKILL.md structure)
- Agent template (agent.md structure)
- Hooks template (hooks.json structure)
- Plugin template (full plugin structure)

#### References
- `skill-patterns.md` - Skill best practices
- `agent-patterns.md` - Agent best practices
- `hook-patterns.md` - Hook best practices
- `plugin-patterns.md` - Plugin best practices
- `antipatterns.md` - Common mistakes to avoid
- `quality-criteria.md` - Scoring criteria

#### Self-Learning
- Stop hook for pattern extraction
- PostToolUse validation for file changes
- Pattern storage in learned/patterns.json
- Statistics tracking in learned/stats.json

### Quality Metrics
- Pass threshold: 80/100
- Maximum refactor iterations: 3
- Criteria: triggers, disclosure, boundaries, antipatterns, organization, style, examples, documentation
