# Architecture Decision Record (ADR) Template

Use this template to document important technical decisions made during specification and implementation.

---

# ADR-[NUMBER]: [Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded]

**Date**: YYYY-MM-DD

**Deciders**: [List people involved in decision]

**Technical Story**: [Link to spec, issue, or context]

---

## Context

*What is the issue or problem we're facing? What factors are influencing this decision?*

[2-4 paragraphs describing the context, including:]
- Current situation
- Forces at play (technical, organizational, deadline)
- Why this decision is needed now
- Constraints and requirements

---

## Decision

*What decision have we made?*

[1-2 paragraphs clearly stating the decision]

We will [action/approach], because [primary reason].

---

## Alternatives Considered

### Option 1: [Name]

**Description**: [How this would work]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]
- [Disadvantage 3]

**Why not chosen**: [Primary reason for rejection]

---

### Option 2: [Name]

**Description**: [How this would work]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Why not chosen**: [Primary reason for rejection]

---

### Option 3: [Name] (Chosen)

**Description**: [How this will work]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Why chosen**: [Primary reasons for selection]

---

## Consequences

### Positive
- [Good consequence 1]
- [Good consequence 2]
- [Good consequence 3]

### Negative
- [Trade-off or cost 1]
- [Trade-off or cost 2]

### Neutral
- [Side effect 1]
- [Side effect 2]

---

## Implementation

*What needs to be done to implement this decision?*

- [ ] [Implementation step 1]
- [ ] [Implementation step 2]
- [ ] [Implementation step 3]

**Estimated Effort**: [X days/weeks]

---

## Validation

*How will we know if this decision is working?*

**Success Metrics**:
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]

**Validation Plan**:
- [Validation approach 1]
- [Validation approach 2]

**Review Date**: [When to reassess this decision]

---

## Related Decisions

- ADR-[X]: [Related decision]
- ADR-[Y]: [Another related decision]

---

## References

- [Link to research 1]
- [Link to documentation 2]
- [Link to discussion 3]

---

## Notes

*Additional context, discussion points, or future considerations*

[Any additional notes that don't fit above]

---

**Revision History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | YYYY-MM-DD | [Name] | Initial draft |
| 1.0 | YYYY-MM-DD | [Name] | Accepted |

---

## Example ADRs

### ADR-001: Use PostgreSQL for Primary Database

**Status**: Accepted

**Date**: 2024-01-15

**Context**: We need to select a database for our new application that will store user data, transactions, and analytics. Requirements include ACID compliance, support for complex queries, scalability to millions of users, and strong community support.

**Decision**: We will use PostgreSQL as our primary database.

**Alternatives Considered**:
1. **MySQL**: Good performance, but weaker support for complex queries and JSON
2. **MongoDB**: Great for flexibility, but ACID compliance concerns for financial data
3. **PostgreSQL** (Chosen): Best balance of features, performance, and reliability

**Consequences**:
- Positive: Strong ACID guarantees, excellent JSON support, powerful query capabilities
- Negative: Slightly more complex setup than MySQL, steeper learning curve
- Neutral: Will need connection pooling and read replicas for scale

**Implementation**:
- Set up PostgreSQL 15
- Configure connection pooling with PgBouncer
- Implement migration framework with db-migrate

---

### ADR-002: Adopt Monorepo Structure

**Status**: Accepted

**Date**: 2024-01-20

**Context**: As our codebase grows with multiple services and shared libraries, we need to decide on repository structure. We have 3 backend services, 2 frontend apps, and 5 shared libraries.

**Decision**: We will adopt a monorepo structure using pnpm workspaces.

**Alternatives Considered**:
1. **Multi-repo**: Each service/app in its own repo
2. **Monorepo with npm workspaces**: Limited cross-repo scripting
3. **Monorepo with pnpm** (Chosen): Better workspace support, faster installs

**Consequences**:
- Positive: Easier code sharing, atomic cross-service changes, unified CI/CD
- Negative: Larger repo size, need for proper tooling
- Neutral: CI needs to be smart about what to build/test

**Implementation**:
- Migrate repos into monorepo structure
- Set up pnpm workspaces
- Configure Turborepo for build orchestration
- Update CI/CD pipelines
