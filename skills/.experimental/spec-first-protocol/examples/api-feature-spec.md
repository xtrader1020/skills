# Example Spec: REST API Feature - User Profile Management

## 1. Overview

### Problem Statement
Users need the ability to view and update their profile information. Currently, user data can only be modified through admin tools, creating friction and requiring support tickets for simple profile updates.

### Objectives
- Primary objective: Enable users to self-manage their profile information
- Secondary objectives:
  - Reduce support ticket volume for profile updates
  - Improve user engagement through customization
  - Establish pattern for future user-facing APIs

### Success Criteria
- [ ] Users can view their full profile via API
- [ ] Users can update allowed fields (name, bio, preferences)
- [ ] Profile updates are validated and persisted correctly
- [ ] API response time < 200ms at p95
- [ ] Support tickets for profile updates reduced by 80%

### Non-Goals
- Avatar/image upload (future enhancement)
- Profile visibility settings (future enhancement)
- Admin profile management (separate spec)
- Profile deletion (requires legal review)

---

## 2. Context and Background

### Current State
- User profiles exist in the database with 15+ fields
- Only admins can modify profiles via internal tool
- Users submit support tickets to change name, bio, etc.
- Profile data is read-only via legacy `/api/users/me` endpoint

### Proposed State
- Users access profile via new `/api/v2/profile` endpoints
- Users can update name, bio, location, website, preferences
- Changes are validated and immediately reflected
- Audit log tracks all profile modifications

### Stakeholders
- **Primary**: All registered users (~50K active)
- **Secondary**: Support team, product team
- **Reviewers**: Tech lead, security team, product manager

---

## 3. Requirements

### Functional Requirements

#### Must Have
1. **View Profile**
   - Acceptance criteria:
     - [ ] GET /api/v2/profile returns authenticated user's profile
     - [ ] Response includes all profile fields
     - [ ] Sensitive fields (email) are masked appropriately

2. **Update Profile**
   - Acceptance criteria:
     - [ ] PATCH /api/v2/profile updates allowed fields
     - [ ] Only changed fields are updated
     - [ ] Invalid updates return 400 with clear error messages
     - [ ] Concurrent updates are handled correctly

3. **Validation**
   - Acceptance criteria:
     - [ ] Name: 1-100 chars, alphanumeric + spaces
     - [ ] Bio: 0-500 chars
     - [ ] Website: Valid URL or empty
     - [ ] Location: 0-100 chars

#### Should Have
- Profile update history (last 10 changes)
- Email notification on profile change
- Rate limiting (5 updates per hour)

#### Could Have
- Bulk validation endpoint
- Profile completeness percentage
- Suggested fields to complete

### Non-Functional Requirements

- **Performance**: 
  - GET response time < 100ms (p95)
  - PATCH response time < 200ms (p95)
  - Database queries optimized with proper indexes

- **Scalability**: 
  - Support 500 concurrent users
  - Handle 1000 requests/minute per instance

- **Reliability**: 
  - 99.9% uptime
  - Graceful degradation if audit log fails
  - Retry logic for transient failures

- **Security**: 
  - JWT authentication required
  - Users can only access their own profile
  - Input validation and sanitization
  - Rate limiting to prevent abuse

- **Maintainability**: 
  - Clear error messages
  - Comprehensive logging
  - API versioned (v2)
  - Backward compatible with v1 reads

---

## 4. Technical Design

### Architecture Overview

```
┌──────────┐      ┌──────────────┐      ┌──────────┐      ┌───────────┐
│  Client  │─────▶│ API Gateway  │─────▶│ Profile  │─────▶│ Database  │
│          │◀─────│ + Auth       │◀─────│ Service  │◀─────│           │
└──────────┘      └──────────────┘      └──────────┘      └───────────┘
                                              │
                                              ├─────▶ Audit Log
                                              └─────▶ Email Service
```

### Component Specifications

#### Profile Service
- **Purpose**: Handle profile CRUD operations
- **Responsibilities**: 
  - Retrieve user profile
  - Validate and apply updates
  - Trigger audit logging
  - Emit events for downstream services
- **Dependencies**: Database, AuditService, EventBus

### Data Models

#### UserProfile
```typescript
interface UserProfile {
  id: string;                    // UUID, primary key
  userId: string;                // FK to users table
  name: string;                  // 1-100 chars
  bio: string | null;            // 0-500 chars
  location: string | null;       // 0-100 chars
  website: string | null;        // Valid URL
  preferences: ProfilePreferences;
  createdAt: Date;
  updatedAt: Date;
}

interface ProfilePreferences {
  emailNotifications: boolean;
  theme: 'light' | 'dark' | 'auto';
  language: string;              // ISO 639-1 code
}
```

**Validation Rules**:
- `name`: Required, 1-100 characters, matches `/^[a-zA-Z0-9\s'-]+$/`
- `bio`: Optional, max 500 characters
- `website`: Optional, valid URL format
- `location`: Optional, max 100 characters
- `preferences.language`: Must be supported language code

### API Specifications

#### Endpoint: GET /api/v2/profile
**Purpose**: Retrieve authenticated user's profile

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response** (200 OK):
```json
{
  "id": "uuid-here",
  "userId": "user-uuid",
  "name": "John Doe",
  "bio": "Software engineer passionate about open source",
  "location": "San Francisco, CA",
  "website": "https://johndoe.com",
  "preferences": {
    "emailNotifications": true,
    "theme": "dark",
    "language": "en"
  },
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-03-20T14:30:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Profile doesn't exist
- 500 Internal Server Error: Server error

---

#### Endpoint: PATCH /api/v2/profile
**Purpose**: Update user's profile

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Jane Doe",
  "bio": "Updated bio text",
  "preferences": {
    "theme": "light"
  }
}
```

**Response** (200 OK):
```json
{
  "id": "uuid-here",
  "userId": "user-uuid",
  "name": "Jane Doe",
  "bio": "Updated bio text",
  "location": "San Francisco, CA",
  "website": "https://johndoe.com",
  "preferences": {
    "emailNotifications": true,
    "theme": "light",
    "language": "en"
  },
  "updatedAt": "2024-03-21T09:15:00Z"
}
```

**Error Responses**:
- 400 Bad Request: Invalid input
  ```json
  {
    "error": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "name",
        "message": "Name must be between 1 and 100 characters"
      }
    ]
  }
  ```
- 401 Unauthorized: Missing or invalid token
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Server error

**Validation**:
- At least one field must be provided
- Only allowed fields can be updated
- Each field follows its validation rules
- Partial updates supported (only send changed fields)

### Database Schema

#### Table: user_profiles
```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  bio VARCHAR(500),
  location VARCHAR(100),
  website VARCHAR(500),
  preferences JSONB NOT NULL DEFAULT '{"emailNotifications": true, "theme": "auto", "language": "en"}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_updated_at ON user_profiles(updated_at);
```

**Migrations**:
```sql
-- Up
CREATE TABLE user_profiles (...);
INSERT INTO user_profiles (user_id, name)
  SELECT id, COALESCE(full_name, username) FROM users;

-- Down
DROP TABLE user_profiles;
```

---

## 5. Security Considerations

### Authentication & Authorization
- **Who can access**: Authenticated users only
- **Authentication method**: JWT token in Authorization header
- **Authorization checks**: User can only access their own profile (userId from token must match profile)

### Data Protection
- **Sensitive data**: Email, phone (not included in this API)
- **Validation**: All inputs sanitized against XSS, SQL injection
- **Rate Limiting**: 5 updates per hour per user

### Input Validation
- `name`: HTML stripped, length checked, pattern validated
- `bio`: HTML stripped, length checked
- `website`: URL format validated, protocol must be http(s)
- `location`: HTML stripped, length checked

---

## 6. Testing Strategy

### Unit Tests
- ProfileService.getProfile() - various user states
- ProfileService.updateProfile() - valid/invalid inputs
- Validation logic for each field
- Error handling for database failures

### Integration Tests
- GET /api/v2/profile with valid token
- GET /api/v2/profile with invalid token (401)
- PATCH /api/v2/profile with valid data
- PATCH /api/v2/profile with invalid data (400)
- PATCH /api/v2/profile rate limiting (429)
- Concurrent PATCH requests (optimistic locking)

### Performance Tests
- Load test: 100 concurrent users reading profiles
- Stress test: 500 requests/minute profile updates
- Response time verification (< 200ms p95)

---

## 7. Deployment

### Rollout Plan
1. Deploy to dev environment, run integration tests
2. Deploy to staging, run smoke tests with test users
3. Deploy to production with feature flag disabled
4. Enable for internal employees (10 users)
5. Gradual rollout: 10% → 50% → 100% over 1 week
6. Monitor error rates, response times, user feedback

### Rollback Plan
- Disable feature flag if error rate > 1%
- Roll back deployment if critical issues
- Database migrations are backward compatible

### Monitoring
- **Metrics**: Request count, error rate, response time, validation errors
- **Alerts**: Error rate > 1%, response time > 500ms
- **Dashboard**: Real-time metrics, user activity

---

## 8. Timeline

- Specification: 1 day ✓
- Implementation: 3 days
  - Backend API: 2 days
  - Tests: 1 day
- Review & QA: 1 day
- Deployment: 1 day
- **Total**: 6 days

---

## 9. Open Questions

1. Should we allow clearing/removing optional fields (set to null)?
   - **Status**: Resolved
   - **Decision**: Yes, sending `null` will clear the field

2. What happens to profiles if a user is deleted?
   - **Status**: Resolved
   - **Decision**: CASCADE delete in database

---

## 10. Decisions

### Decision 1: Use PATCH instead of PUT
- **Date**: 2024-03-15
- **Rationale**: PATCH allows partial updates, reducing payload size and complexity
- **Alternative**: PUT would require sending all fields every time

### Decision 2: Store preferences as JSONB
- **Date**: 2024-03-15
- **Rationale**: Flexible schema for future preference additions without migrations
- **Alternative**: Separate columns would be more structured but less flexible
