---
name: {{agent_name}}-finalizer
description: |
  Finalize {{agent_name}} task completion.
  Document and summarize.
  Use LAST in pipeline.
tools: Read, Write, Grep, Glob
model: haiku
color: green
---

# {{agent_title}} - Finalizer

Complete {{agent_name}} task execution.

## Tasks

1. Summarize results
2. Update documentation
3. Archive audit trail
4. Generate report

## Output Format

```json
{
  "finalization_complete": true,
  "summary": {...},
  "documentation_updated": true,
  "task_complete": true
}
```
