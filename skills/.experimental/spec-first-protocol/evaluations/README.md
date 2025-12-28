# Evaluation Guide

This directory contains evaluation frameworks for assessing specification quality and implementation alignment.

## Files

### spec-quality.json
Evaluation criteria for assessing the quality of a specification before implementation begins.

**When to use**: After completing a specification, before starting implementation

**Scoring**:
- 90-100: Excellent - Ready for implementation
- 75-89: Good - Minor gaps to address
- 60-74: Fair - Needs work before implementation
- 0-59: Poor - Major revision required

**Categories evaluated**:
1. **Clarity** (20%): How clear and understandable is the spec?
2. **Completeness** (25%): Does it contain all necessary information?
3. **Technical Detail** (20%): Is the design sufficiently detailed?
4. **Testability** (15%): Can requirements be validated through testing?
5. **Security** (10%): Are security considerations addressed?
6. **Operations** (10%): Are operational concerns covered?

### implementation-alignment.json
Evaluation criteria for checking if implementation matches the specification.

**When to use**: During code review or after implementation is complete

**Scoring**:
- 95-100: Perfect Alignment - Implementation exactly matches spec
- 85-94: Strong Alignment - Minor acceptable deviations
- 70-84: Moderate Alignment - Some gaps to address
- 0-69: Weak Alignment - Significant misalignment

**Categories evaluated**:
1. **Requirements Coverage** (30%): Are all requirements implemented?
2. **API Contract Compliance** (20%): Do interfaces match the spec?
3. **Data Model Alignment** (15%): Does the data layer match?
4. **Security Compliance** (15%): Are security requirements met?
5. **Performance Compliance** (10%): Are performance targets achieved?
6. **Testing Alignment** (10%): Does testing match the strategy?

## How to Use

### Evaluating a Specification

1. Complete your specification using the appropriate template
2. Go through each check in `spec-quality.json`
3. Award points for each satisfied criterion
4. Calculate your total score
5. Review recommendations based on your score
6. Address gaps before proceeding to implementation

**Example**:
```
Clarity: 18/20
Completeness: 23/25
Technical Detail: 18/20
Testability: 14/15
Security: 9/10
Operations: 8/10
---
Total: 90/100 (Excellent)
```

### Evaluating Implementation Alignment

1. Complete your implementation
2. Review the specification
3. Go through each check in `implementation-alignment.json`
4. Award points for each satisfied criterion
5. Document any deviations from the spec
6. For each deviation, classify it as:
   - **Justified**: Good reason, documented
   - **Improvement**: Adds value not in spec
   - **Unjustified**: Needs correction or spec update

**Example**:
```
Requirements Coverage: 28/30
API Contract Compliance: 20/20
Data Model Alignment: 15/15
Security Compliance: 13/15
Performance Compliance: 10/10
Testing Alignment: 8/10
---
Total: 94/100 (Strong Alignment)

Deviations:
- Changed error response format (justified: better error handling)
- Added caching layer (improvement: better performance)
```

## Best Practices

### For Specification Evaluation

1. **Be Honest**: Don't give yourself points if a criterion isn't truly met
2. **Use Examples**: If examples are missing, add them before claiming completeness
3. **Get Feedback**: Have someone else review your spec and scoring
4. **Iterate**: If you score below 75, revise the spec before implementing
5. **Document Gaps**: Note what's missing even if you choose to proceed

### For Implementation Evaluation

1. **Compare Directly**: Have the spec open while reviewing implementation
2. **Test Everything**: Run all acceptance criteria as tests
3. **Document Deviations**: Every difference from spec should be documented
4. **Justify Changes**: If implementation differs, explain why in code or ADR
5. **Update Spec**: If implementation revealed better approaches, update the spec

## Common Issues

### Specifications
- ❌ Vague requirements: "Should be fast"
- ✅ Specific requirements: "Response time < 200ms for p95"

- ❌ Missing acceptance criteria
- ✅ Each requirement has testable criteria

- ❌ No technical design
- ✅ Architecture diagrams, data models, APIs specified

### Implementation
- ❌ Undocumented deviations from spec
- ✅ All deviations documented with rationale

- ❌ Missing required features
- ✅ All must-have requirements implemented

- ❌ Different API than specified
- ✅ API matches spec or spec updated to reflect changes

## Integration with Workflow

### Spec-First Workflow

```
1. Write Specification
   ↓
2. Evaluate with spec-quality.json
   ↓
3. Score < 75? → Revise spec → Go to step 2
   ↓
4. Score ≥ 75? → Get approval → Proceed
   ↓
5. Implement against spec
   ↓
6. Evaluate with implementation-alignment.json
   ↓
7. Score < 85? → Fix misalignments → Go to step 6
   ↓
8. Score ≥ 85? → Ship!
```

### Quick Spec Workflow

For small changes, you can use a lighter process:

```
1. Write Quick Spec
   ↓
2. Quick evaluation (< 5 min)
   ↓
3. Implement
   ↓
4. Quick alignment check
   ↓
5. Ship!
```

## Automation

These evaluation files can be used programmatically:

```typescript
import specQuality from './spec-quality.json';

function evaluateSpec(spec: Specification): EvaluationResult {
  const scores: Record<string, number> = {};
  
  for (const [category, criteria] of Object.entries(specQuality.criteria)) {
    scores[category] = evaluateCategory(spec, criteria);
  }
  
  const totalScore = calculateWeightedScore(scores, specQuality.criteria);
  const rating = getRating(totalScore, specQuality.scoring);
  const recommendations = getRecommendations(totalScore, specQuality.recommendations);
  
  return { scores, totalScore, rating, recommendations };
}
```

## Feedback

These evaluation frameworks are living documents. If you find:
- Criteria that aren't useful
- Missing important checks
- Unclear descriptions
- Better scoring approaches

Please update these files to improve them for everyone.
