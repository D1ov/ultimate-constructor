# Quality Criteria

Scoring criteria for component quality assessment.

## Overview

Components are scored 0-100 based on weighted criteria.
Pass threshold: 80/100

## Criteria Breakdown

### 1. Trigger Specificity (20%)

How well the description defines when to activate.

| Score | Criteria |
|-------|----------|
| 20 | 5+ specific trigger phrases with context |
| 15 | 3-4 specific phrases |
| 10 | 1-2 vague triggers |
| 5 | Implied triggers only |
| 0 | No clear triggers |

**Examples:**

**20 points:**
```yaml
description: |
  Create API tests. Use when user mentions "test API", "endpoint test",
  "integration test", "REST test", "API validation".
```

**10 points:**
```yaml
description: |
  Help with testing.
```

### 2. Progressive Disclosure (15%)

Content layering and organization.

| Score | Criteria |
|-------|----------|
| 15 | Main file < 300 lines, details in references/ |
| 12 | Main file 300-400 lines with references |
| 8 | Main file 400-500 lines |
| 4 | Main file > 500 lines with some references |
| 0 | Monolithic > 500 lines, no references |

### 3. Boundaries Clarity (15%)

How clearly scope limits are defined.

| Score | Criteria |
|-------|----------|
| 15 | Explicit DO/DON'T sections + description boundaries |
| 12 | "NOT for:" in description + body boundaries |
| 8 | Only "NOT for:" in description |
| 4 | Implied boundaries |
| 0 | No boundaries defined |

**Example of 15 points:**
```markdown
## When to Use
- API endpoint testing
- Integration tests
- Request/response validation

## When NOT to Use
- Unit tests (use unit-testing skill)
- UI tests (use e2e-testing skill)
- Load testing (use performance skill)
```

### 4. Antipattern Awareness (15%)

Documentation of what NOT to do.

| Score | Criteria |
|-------|----------|
| 15 | Dedicated "Common Mistakes" section with 3+ items |
| 10 | Scattered warnings throughout |
| 5 | Single "avoid" or "don't" mention |
| 0 | No antipattern guidance |

**Example of 15 points:**
```markdown
## Common Mistakes

### ❌ Testing Implementation Details
Don't test internal methods directly.
**Instead:** Test public API behavior.

### ❌ Hardcoded Test Data
Don't use production credentials in tests.
**Instead:** Use environment variables or fixtures.
```

### 5. Resource Organization (10%)

Structure of supporting files.

| Score | Criteria |
|-------|----------|
| 10 | Logical scripts/ and references/ with clear purposes |
| 7 | Has scripts/ or references/ with good organization |
| 4 | Flat structure with named files |
| 0 | Disorganized or missing resources |

### 6. Writing Style (10%)

Adherence to style guidelines.

| Score | Criteria |
|-------|----------|
| 10 | Imperative voice, third person, concise |
| 7 | Mostly correct with minor issues |
| 4 | Mixed styles |
| 0 | First/second person throughout |

**Correct style:**
- "Create a new test file" ✓
- "Run the validation script" ✓
- "Check output for errors" ✓

**Incorrect style:**
- "You should create a file" ✗
- "I recommend running tests" ✗
- "We need to check errors" ✗

### 7. Examples Quality (10%)

Working code examples.

| Score | Criteria |
|-------|----------|
| 10 | 3+ complete, working examples |
| 7 | 2 examples with context |
| 4 | 1 example or pseudocode |
| 0 | No examples |

**Good example (10 points):**
```javascript
// Complete with imports and context
import { test, expect } from 'vitest';
import { createUser } from './api';

test('creates user with valid data', async () => {
  const user = await createUser({ name: 'Test', email: 'test@example.com' });
  expect(user.id).toBeDefined();
  expect(user.name).toBe('Test');
});
```

### 8. Documentation (5%)

Overall documentation quality.

| Score | Criteria |
|-------|----------|
| 5 | README, clear sections, well-commented |
| 3 | Basic documentation |
| 0 | Minimal or missing docs |

## Score Calculation

```
Total = Σ(criterion_score)
Percentage = Total / 100 * 100

Example:
Triggers: 15/20
Disclosure: 12/15
Boundaries: 15/15
Antipatterns: 10/15
Organization: 7/10
Style: 10/10
Examples: 7/10
Documentation: 3/5

Total: 79/100 = 79%
```

## Recommendations

| Score | Recommendation |
|-------|----------------|
| 90-100 | Excellent - approve |
| 80-89 | Good - approve with minor suggestions |
| 70-79 | Fair - refactor recommended |
| 60-69 | Needs work - refactor required |
| < 60 | Poor - redesign needed |

## Quick Checklist

### Must Have (Errors if missing)
- [ ] Valid YAML/JSON frontmatter
- [ ] Name field (lowercase, hyphens)
- [ ] Description field (< 1024 chars)
- [ ] All referenced files exist

### Should Have (Warnings if missing)
- [ ] Trigger phrases in description
- [ ] Boundaries (NOT for)
- [ ] Examples section
- [ ] Third-person writing

### Nice to Have (Info if missing)
- [ ] references/ directory
- [ ] scripts/ directory
- [ ] Common mistakes section
- [ ] README file
