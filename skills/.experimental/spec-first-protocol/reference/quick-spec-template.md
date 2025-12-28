# Quick Specification Template

Use this lightweight template for small features, bug fixes, or simple changes that don't require a full specification.

---

## Problem
*What issue are we solving?*

[1-2 sentence problem description]

---

## Solution
*What are we building?*

[2-3 sentence solution description]

---

## Scope

**In Scope**:
- [Item 1]
- [Item 2]

**Out of Scope**:
- [Item 1]
- [Item 2]

---

## Technical Approach

### Changes Required
1. **File/Module**: `path/to/file.ts`
   - Change: [What changes]
   - Why: [Reason]

2. **File/Module**: `path/to/other.ts`
   - Change: [What changes]
   - Why: [Reason]

### API Changes (if applicable)
```typescript
// Before
oldFunction(param: string): void

// After
newFunction(param: string, newParam: number): void
```

### Data Changes (if applicable)
- Add column: `new_field` (type, nullable, default)
- Migration: [Brief description]

---

## Testing

**Test Cases**:
1. [Scenario 1]: Expected outcome
2. [Scenario 2]: Expected outcome
3. [Edge case]: Expected outcome

**Manual Testing**:
- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Verify outcome]

---

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] Tests pass
- [ ] No new warnings or errors

---

## Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

---

## Open Questions
1. [Question]? → [Answer or TBD]

---

**Estimated Effort**: [X hours/days]
