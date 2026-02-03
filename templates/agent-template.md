---
name: {{name}}
description: |
  {{description}}
  Use when: {{triggers}}
  NOT for: {{boundaries}}
tools: {{tools}}
model: {{model}}
permissionMode: {{permission_mode}}
---

# {{title}}

{{overview}}

## Workflow

### Step 1: {{step1_title}}

{{step1_description}}

### Step 2: {{step2_title}}

{{step2_description}}

### Step 3: {{step3_title}}

{{step3_description}}

## Input Format

```json
{
  {{input_schema}}
}
```

## Output Format

```json
{
  {{output_schema}}
}
```

## Constraints

- {{constraint1}}
- {{constraint2}}
- {{constraint3}}

## Examples

### Example: {{example_title}}

**Input:**
```
{{example_input}}
```

**Output:**
```
{{example_output}}
```
