---
name: extract
description: Extract components or learning patterns from current chat context
args:
  - name: mode
    description: "Mode: 'component' (create skill/agent), 'learn' (extract patterns), 'analyze' (just analyze)"
    required: false
    default: component
  - name: type
    description: "For component mode: skill, agent, plugin, hook"
    required: false
examples:
  - "/uc:extract"
  - "/uc:extract component skill"
  - "/uc:extract component agent"
  - "/uc:extract learn"
  - "/uc:extract analyze"
model: sonnet
tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Extract from Context Command

Extract reusable components or learning patterns from current conversation context.

## Modes

### Mode 1: Component Extraction (Default)
```
/uc:extract                    # Auto-detect best component type
/uc:extract component skill    # Extract as skill
/uc:extract component agent    # Extract as agent
/uc:extract component plugin   # Extract as plugin
/uc:extract component hook     # Extract as hook
```

### Mode 2: Learning Extraction
```
/uc:extract learn              # Extract patterns for self-learning
/uc:extract learn --review     # With mandatory review before saving
```

### Mode 3: Analysis Only
```
/uc:extract analyze            # Analyze without creating anything
```

## Component Extraction Workflow

### Step 1: Context Analysis

Analyze entire conversation for:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT ANALYSIS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔍 Scanning conversation...                                    │
│                                                                 │
│  Found:                                                         │
│  ├── Domain expertise demonstrated: API testing, debugging     │
│  ├── Workflows repeated: 3 (test→fix→verify cycle)            │
│  ├── Error resolutions: 5 (connection, auth, parsing...)      │
│  ├── User corrections: 2 (endpoint format, header syntax)      │
│  ├── Tools used frequently: Bash, Read, WebFetch              │
│  └── Code patterns: retry logic, error handling               │
│                                                                 │
│  Recommended component: Skill "api-testing-expert"              │
│  Confidence: 87%                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Extraction sources:**
- **User requests**: What the user asked for
- **Successful solutions**: What actually worked
- **Domain knowledge**: Technical concepts discussed
- **Tool sequences**: Repeating patterns of tool usage
- **Error handling**: How errors were resolved
- **Corrections**: What user corrected in Claude's approach

### Step 2: Launch Context Reviewer

Before creating component, **constructor-context-reviewer** validates:

```
╔══════════════════════════════════════════════════════════════════╗
║                    CONTEXT REVIEW                                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Reviewer Analysis:                                              ║
║                                                                  ║
║  ✅ Domain coherence: HIGH (single topic: API testing)          ║
║  ✅ Knowledge quality: GOOD (5 working solutions demonstrated)   ║
║  ⚠️  Completeness: MEDIUM (missing error types documentation)    ║
║  ✅ Reusability: HIGH (patterns apply to other APIs)            ║
║                                                                  ║
║  Recommendation: APPROVE with minor additions                    ║
║                                                                  ║
║  Suggested additions:                                            ║
║  - Add timeout handling (not discussed in chat)                  ║
║  - Document rate limiting (mentioned but not resolved)           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 3: Launch Context Accepter

**constructor-context-accepter** makes final decision:

```
╔══════════════════════════════════════════════════════════════════╗
║                    ACCEPTANCE DECISION                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Accepter Verdict: ✅ APPROVED                                   ║
║                                                                  ║
║  Quality Score: 82/100                                           ║
║  - Content quality: 85                                           ║
║  - Extraction accuracy: 80                                       ║
║  - Reusability potential: 81                                     ║
║                                                                  ║
║  Extracted for component:                                        ║
║  - 5 workflow patterns                                           ║
║  - 3 error handling strategies                                   ║
║  - 2 antipatterns (what NOT to do)                              ║
║  - 8 trigger phrases                                             ║
║  - 4 example scenarios                                           ║
║                                                                  ║
║  Proceed with creation? [Y/n/modify]                            ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 4: User Confirmation

Present extraction summary:

```
Extracted from Chat:

Component: api-testing-expert
Type: Skill
Organization Level: Full (9 sub-agents)

Content to include:
├── Workflows
│   ├── API endpoint testing flow
│   ├── Authentication debugging
│   └── Response validation
├── Error Handling
│   ├── Connection errors → retry with backoff
│   ├── Auth errors → refresh token flow
│   └── Parse errors → fallback strategies
├── Antipatterns
│   ├── DON'T: hardcode credentials
│   └── DON'T: ignore status codes
└── Examples
    ├── REST API testing
    ├── GraphQL query validation
    └── WebSocket connection

Proceed with creation? [Y/n/customize]
```

### Step 5: Create via Standard Pipeline

If approved, launch creation pipeline:
1. **constructor-architect** → designs structure from extracted content
2. **constructor-executor** → creates files
3. **constructor-tester** → validates
4. **constructor-reviewer** → quality check
5. **constructor-finalizer** → complete

## Learning Extraction Workflow

### Step 1: Analyze for Patterns

```
/uc:extract learn
```

Extract learning patterns with confidence scores:

```
╔══════════════════════════════════════════════════════════════════╗
║                  LEARNING PATTERNS FOUND                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Pattern 1: api-retry-strategy                                   ║
║  Type: workflow                                                  ║
║  Confidence: 91%                                                 ║
║  Source: Turns 15, 23, 45 (repeated 3 times successfully)        ║
║  Description: Exponential backoff for API failures               ║
║                                                                  ║
║  Pattern 2: header-format-correction                             ║
║  Type: correction                                                ║
║  Confidence: 88%                                                 ║
║  Source: Turn 32 (user corrected approach)                       ║
║  Description: Use Bearer token format, not Basic auth            ║
║                                                                  ║
║  Pattern 3: response-validation-order                            ║
║  Type: workflow                                                  ║
║  Confidence: 75%                                                 ║
║  Source: Turns 50-55                                             ║
║  Description: Check status → headers → body order                ║
║                                                                  ║
║  Pattern 4: hardcoded-url-antipattern                            ║
║  Type: antipattern                                               ║
║  Confidence: 95%                                                 ║
║  Source: Turn 28 (caused error, user corrected)                  ║
║  Description: Never hardcode API URLs in production              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 2: Review Patterns (--review flag)

Launch **constructor-context-reviewer** for each pattern:

```
Reviewing Pattern: api-retry-strategy

✅ Evidence quality: HIGH (3 successful uses)
✅ Reproducibility: HIGH (clear steps documented)
✅ Generalizability: MEDIUM (specific to HTTP APIs)
⚠️  Edge cases: Not all covered (what if server is down?)

Reviewer Decision: APPROVE (confidence 91% maintained)
```

### Step 3: Accept Patterns

Launch **constructor-context-accepter** for final approval:

```
╔══════════════════════════════════════════════════════════════════╗
║                  PATTERN ACCEPTANCE                              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Patterns to save:                                               ║
║                                                                  ║
║  ✅ [1] api-retry-strategy (91%) → ACCEPT                        ║
║  ✅ [2] header-format-correction (88%) → ACCEPT                  ║
║  ⚠️  [3] response-validation-order (75%) → NEEDS MORE EVIDENCE   ║
║  ✅ [4] hardcoded-url-antipattern (95%) → ACCEPT                 ║
║                                                                  ║
║  Save approved patterns to learned/patterns.json? [Y/n]          ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 4: Save to Patterns

Only approved patterns saved:

```json
{
  "patterns": [
    {
      "id": "ctx-20260203-001",
      "type": "workflow",
      "name": "api-retry-strategy",
      "description": "Exponential backoff for API failures",
      "confidence": 0.91,
      "reviewed": true,
      "accepted": true,
      "reviewer_notes": "Evidence quality HIGH",
      "source_session": "current",
      "learned_at": "2026-02-03T15:30:00"
    }
  ]
}
```

## Analysis Only Mode

```
/uc:extract analyze
```

Shows analysis without creating anything:

```
╔══════════════════════════════════════════════════════════════════╗
║                  CONVERSATION ANALYSIS                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Session Statistics:                                             ║
║  ├── Total turns: 67                                            ║
║  ├── Tools used: 145                                            ║
║  ├── Successful operations: 128 (88%)                           ║
║  └── Failed operations: 17 (12%)                                ║
║                                                                  ║
║  Domain Analysis:                                                ║
║  ├── Primary topic: API Integration                             ║
║  ├── Secondary topics: Error handling, Authentication           ║
║  └── Complexity: Medium-High                                     ║
║                                                                  ║
║  Extractable Content:                                            ║
║  ├── Skill potential: 87% (enough for full skill)               ║
║  ├── Agent potential: 72% (would need more structure)           ║
║  ├── Hook potential: 45% (not enough validation patterns)       ║
║  └── Learning patterns: 4 high-confidence                        ║
║                                                                  ║
║  Recommendation: Create skill with full organization             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Output Format

```json
{
  "extraction_mode": "component",
  "analysis": {
    "turns_analyzed": 67,
    "domain": "API Testing",
    "complexity": "medium-high"
  },
  "review": {
    "reviewer_decision": "approve",
    "quality_score": 82,
    "notes": ["Missing timeout handling"]
  },
  "acceptance": {
    "accepted": true,
    "final_score": 82,
    "patterns_extracted": 5,
    "antipatterns_extracted": 2
  },
  "component_created": {
    "type": "skill",
    "name": "api-testing-expert",
    "location": "NEW/skills/api-testing-expert/",
    "organization_level": "full"
  }
}
```

## Quality Gates

| Gate | Agent | Criteria |
|------|-------|----------|
| Review | context-reviewer | Evidence quality, reproducibility, coherence |
| Accept | context-accepter | Final quality score ≥70, no critical issues |

If either gate fails:
- Show specific issues
- Ask user to provide more context
- Or proceed with lower-confidence extraction
