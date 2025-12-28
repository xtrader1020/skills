---
name: spec-first-protocol
description: Implement a spec-first protocol for agentic coding workflows where agents create detailed specifications before implementation.
metadata:
  short-description: Spec-first protocol for agentic workflows
---

# Spec-First Protocol

## Goal

Guide AI agents through a specification-first development workflow that emphasizes planning, documentation, and clear requirements before implementation. This protocol ensures better code quality, fewer iterations, and clearer communication between agents and humans.

## Overview

The Spec-First Protocol is a structured approach for agentic coding workflows that requires creating comprehensive specifications before writing code. This approach reduces ambiguity, improves collaboration, and ensures alignment between intent and implementation.

## When to Use

Use this skill when:
- Starting a new feature or component
- Refactoring complex systems
- Working on projects requiring clear documentation
- Collaborating with multiple agents or team members
- Building systems that need maintainability and clarity

## Core Principles

1. **Specify Before Implementing**: Always create a specification document before writing code
2. **Iterate on Specs**: Refine specifications through review cycles before implementation
3. **Validate Assumptions**: Make implicit assumptions explicit in specifications
4. **Track Decisions**: Document key decisions and their rationale
5. **Maintain Alignment**: Keep specifications and code in sync

## Workflow

### Phase 1: Specification Creation

1. **Gather Requirements**
   - Read existing documentation, code, and context
   - Identify stakeholders and their needs
   - List functional and non-functional requirements
   - Document constraints (technical, time, resources)

2. **Draft Initial Spec**
   - Use `reference/spec-template.md` as a starting point
   - Include: objectives, scope, architecture, interfaces, data models
   - Add acceptance criteria and success metrics
   - Note open questions and assumptions

3. **Review and Refine**
   - Share spec for feedback (with humans or other agents)
   - Address ambiguities and gaps
   - Update based on clarifications
   - Get approval before proceeding

### Phase 2: Implementation Planning

4. **Create Implementation Plan**
   - Break down spec into tasks using `reference/task-breakdown.md`
   - Identify dependencies and ordering
   - Estimate effort and timeline
   - Plan for testing and validation

5. **Set Up Tracking**
   - Create tasks in tracking system (Linear, GitHub Issues, etc.)
   - Link tasks to specification
   - Establish checkpoints and milestones

### Phase 3: Implementation

6. **Implement Against Spec**
   - Follow the specification closely
   - Document deviations with rationale
   - Keep implementation aligned with design decisions
   - Write tests based on acceptance criteria

7. **Validate Continuously**
   - Check implementation against spec requirements
   - Run tests frequently
   - Update documentation as needed
   - Mark spec sections as implemented

### Phase 4: Review and Iteration

8. **Conduct Reviews**
   - Code review against specification
   - Verify all requirements are met
   - Check for edge cases and error handling
   - Validate performance and quality criteria

9. **Update Artifacts**
   - Update spec with lessons learned
   - Document any spec deviations in implementation
   - Add notes for future maintainers
   - Archive decision records

## Key Artifacts

### Specification Document
- Problem statement and context
- Objectives and success criteria
- Scope (in/out of scope)
- Architecture and design decisions
- API/interface definitions
- Data models and schemas
- Security and performance considerations
- Testing approach
- Deployment and rollout plan
- Open questions and assumptions

### Implementation Plan
- Task breakdown with dependencies
- Timeline and milestones
- Resource allocation
- Risk assessment
- Testing and validation strategy

### Decision Records
- Key technical decisions
- Alternatives considered
- Rationale and trade-offs
- Context and constraints

## Best Practices

### For Specifications
- **Be Specific**: Avoid vague terms; use concrete examples
- **Use Diagrams**: Include architecture diagrams, flowcharts, sequence diagrams
- **Define Interfaces**: Clearly specify APIs, function signatures, data formats
- **Include Examples**: Show expected inputs/outputs, use cases
- **Document Non-Goals**: Explicitly state what's out of scope
- **Version Control**: Track spec changes with git

### For Implementation
- **Reference the Spec**: Link code comments to spec sections
- **Test Against Criteria**: Use spec's acceptance criteria for tests
- **Flag Deviations**: Document when implementation differs from spec
- **Keep It Current**: Update spec when requirements change
- **Use Type Systems**: Encode spec constraints in types when possible

### For Collaboration
- **Async-First**: Write specs that enable async review and feedback
- **Clear Questions**: Make open questions obvious and trackable
- **Track Decisions**: Use ADRs (Architecture Decision Records)
- **Share Early**: Get feedback on specs before investing in code
- **Iterate Cheaply**: Spec changes are cheaper than code changes

## Tools and Templates

- `reference/spec-template.md` - Comprehensive specification template
- `reference/quick-spec-template.md` - Lightweight spec for small changes
- `reference/task-breakdown.md` - Guide for breaking specs into tasks
- `reference/decision-record-template.md` - ADR template
- `reference/validation-checklist.md` - Checklist for spec completeness

## Examples

- `examples/api-feature-spec.md` - REST API endpoint specification
- `examples/ui-component-spec.md` - React component specification
- `examples/database-migration-spec.md` - Database schema change spec
- `examples/refactoring-spec.md` - Code refactoring specification

## Evaluation

- `evaluations/spec-quality.json` - Criteria for evaluating specification quality
- `evaluations/implementation-alignment.json` - Checking code-spec alignment

## Common Pitfalls to Avoid

1. **Over-Specification**: Don't specify implementation details that should be flexible
2. **Under-Specification**: Don't leave critical decisions undocumented
3. **Spec Drift**: Keep specs updated as implementation evolves
4. **Skipping Review**: Always get spec feedback before implementing
5. **Ignoring the Spec**: Don't deviate from spec without updating it first

## Integration with Other Skills

- **create-plan**: Use for initial task planning from spec
- **notion-spec-to-implementation**: Use for managing specs in Notion
- **gh-fix-ci**: Use after implementation for validation
- **notion-knowledge-capture**: Use for documenting decisions and learnings

## Success Metrics

A successful spec-first workflow should:
- Reduce implementation rework by 40-60%
- Increase code review speed by providing clear reference
- Improve maintainability through better documentation
- Enable better async collaboration
- Reduce misalignment between intent and implementation
