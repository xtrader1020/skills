# Task Breakdown Guide

This guide helps you break down a specification into implementable tasks.

## Principles

1. **Single Responsibility**: Each task should have one clear objective
2. **Right-Sized**: Tasks should take 0.5-2 days (4-16 hours)
3. **Testable**: Each task should have clear completion criteria
4. **Ordered**: Tasks should have minimal dependencies
5. **Independent**: Tasks should be parallelizable when possible

## Breakdown Process

### Step 1: Identify Major Components

Read through the spec and list the major components or work streams:

- [ ] Data models and database schema
- [ ] API endpoints and business logic
- [ ] Frontend components and UI
- [ ] Testing infrastructure
- [ ] Documentation
- [ ] Deployment and configuration

### Step 2: Break Down by Layer

For each component, create tasks by architectural layer:

#### Backend Tasks
- Data model definition
- Database migrations
- Repository/DAO implementation
- Service layer logic
- API controllers/handlers
- Input validation
- Error handling
- Integration with external services

#### Frontend Tasks
- Component structure
- State management
- API integration
- Form handling and validation
- UI/UX implementation
- Responsive design
- Accessibility

#### Infrastructure Tasks
- Configuration management
- Environment setup
- CI/CD pipeline updates
- Monitoring and alerting
- Feature flags

### Step 3: Add Supporting Tasks

Don't forget these often-overlooked tasks:

- [ ] Unit test setup
- [ ] Integration test setup
- [ ] E2E test implementation
- [ ] Documentation updates
- [ ] Code review preparation
- [ ] Performance testing
- [ ] Security review

### Step 4: Order by Dependencies

Create a dependency graph:

```
[Setup DB Schema] → [Create Models] → [Implement API] → [Build UI]
                          ↓
                    [Unit Tests]
                          ↓
                   [Integration Tests]
```

## Task Template

For each task, define:

### Task: [Clear, Action-Oriented Title]

**Description**:
[2-3 sentences describing what needs to be done]

**Acceptance Criteria**:
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

**Dependencies**:
- Depends on: [Task A, Task B]
- Blocks: [Task C, Task D]

**Files to Change**:
- `path/to/file1.ts`: [What changes]
- `path/to/file2.ts`: [What changes]

**Testing**:
- Unit tests: [What to test]
- Integration tests: [What to test]

**Estimated Effort**: [X hours]

**Reference**: [Link to relevant spec section]

## Example Breakdown

### Spec: User Authentication System

#### Phase 1: Foundation (Day 1)
1. **Task 1.1**: Design and create database schema
   - Tables: users, sessions, passwords
   - Indexes and constraints
   - Migration scripts
   - Est: 4 hours

2. **Task 1.2**: Set up authentication middleware
   - JWT token validation
   - Session management
   - Error handling
   - Est: 4 hours

#### Phase 2: Core Features (Days 2-3)
3. **Task 2.1**: Implement user registration
   - POST /api/auth/register endpoint
   - Password hashing
   - Email validation
   - Est: 6 hours

4. **Task 2.2**: Implement login functionality
   - POST /api/auth/login endpoint
   - Credential verification
   - Token generation
   - Est: 4 hours

5. **Task 2.3**: Implement logout
   - POST /api/auth/logout endpoint
   - Session cleanup
   - Token invalidation
   - Est: 2 hours

#### Phase 3: Security & Edge Cases (Day 4)
6. **Task 3.1**: Add rate limiting
   - Implement rate limiter middleware
   - Configure limits per endpoint
   - Add error responses
   - Est: 4 hours

7. **Task 3.2**: Add password reset flow
   - Generate reset tokens
   - Email integration
   - Token validation
   - Est: 6 hours

#### Phase 4: Testing (Day 5)
8. **Task 4.1**: Unit tests for auth logic
   - Test password hashing
   - Test token generation
   - Test validation logic
   - Est: 4 hours

9. **Task 4.2**: Integration tests
   - Test full registration flow
   - Test login/logout flow
   - Test password reset flow
   - Est: 4 hours

#### Phase 5: Documentation & Deployment (Day 6)
10. **Task 5.1**: Update API documentation
    - Document all endpoints
    - Add example requests/responses
    - Update authentication guide
    - Est: 2 hours

11. **Task 5.2**: Configure deployment
    - Set up environment variables
    - Configure feature flags
    - Update monitoring
    - Est: 2 hours

## Task Sizing Guidelines

### Extra Small (XS): 1-2 hours
- Update documentation
- Fix simple bug
- Add validation rule
- Write unit test

### Small (S): 2-4 hours
- Implement simple endpoint
- Create basic component
- Add simple feature
- Write integration test

### Medium (M): 4-8 hours
- Implement complex endpoint
- Create complex component
- Refactor module
- Multiple related features

### Large (L): 8-16 hours
- Design and implement subsystem
- Complex refactoring
- Multiple endpoints with logic
- Full feature implementation

### Extra Large (XL): 16+ hours
- **Break this down further!**
- Tasks this large should be split

## Red Flags

Watch out for these signs that tasks need refinement:

❌ **Too Vague**: "Work on the backend"
✅ **Better**: "Implement POST /api/users endpoint with validation"

❌ **Too Large**: "Build entire authentication system"
✅ **Better**: Break into 8-12 smaller tasks

❌ **Unclear Success**: "Improve performance"
✅ **Better**: "Reduce API response time to < 200ms for /api/users"

❌ **Multiple Concerns**: "Add endpoint, write tests, update docs, deploy"
✅ **Better**: Split into separate tasks

## Checklist for Good Task Breakdown

- [ ] Each task has a clear, action-oriented title
- [ ] Each task has specific acceptance criteria
- [ ] Tasks are right-sized (0.5-2 days)
- [ ] Dependencies are identified
- [ ] Tasks are ordered logically
- [ ] Testing tasks are included
- [ ] Documentation tasks are included
- [ ] Each task references the relevant spec section
- [ ] Effort estimates are reasonable
- [ ] Edge cases are covered

## Integration with Tools

### Linear
```
Title: [Task title]
Description: [From template]
Labels: backend, api, high-priority
Estimate: 4 (hours/points)
```

### GitHub Issues
```markdown
## Description
[Task description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## References
- Spec: [link]
- Related: #123
```

### Jira
```
Summary: [Task title]
Story Points: 3
Sprint: Sprint 5
Epic: [Epic link]
```
