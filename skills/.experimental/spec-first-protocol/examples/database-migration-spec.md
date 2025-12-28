# Example Spec: Database Migration - Add User Activity Tracking

## 1. Overview

### Problem Statement
We need to track user activity to understand engagement patterns, identify inactive users, and support analytics. Currently, we have no systematic way to track when users last accessed the platform or what features they use.

### Objectives
- Add database schema to track user activity
- Minimal performance impact on existing queries
- Enable analytics queries for user engagement
- Support retention and churn analysis

### Success Criteria
- [ ] Schema supports tracking last_login, last_activity, activity_count
- [ ] Migration runs successfully on production database (5M users)
- [ ] No downtime during migration
- [ ] Query performance impact < 5%
- [ ] Rollback plan tested and ready

### Non-Goals
- Detailed feature usage tracking (separate event system)
- Historical backfill (will track from migration forward)
- Real-time activity streams (batch updates are sufficient)

---

## 2. Context and Background

### Current State
- Users table exists with ~5M rows
- No activity tracking fields
- Application layer has no hooks for recording activity
- Analytics team queries login logs (slow, incomplete)

### Proposed State
- Users table has activity columns
- Application updates activity on login and key actions
- Analytics can query user segments by activity
- Support team can see last active date

### Stakeholders
- **Primary**: Analytics team, product team
- **Secondary**: Engineering team, support team
- **Reviewers**: Database admin, tech lead, data engineer

---

## 3. Requirements

### Functional Requirements

#### Must Have
1. **Schema Changes**
   - Acceptance criteria:
     - [ ] Add `last_login_at` timestamp column
     - [ ] Add `last_activity_at` timestamp column
     - [ ] Add `activity_count` integer column
     - [ ] Columns nullable for backward compatibility
     - [ ] Default values set appropriately

2. **Indexes**
   - Acceptance criteria:
     - [ ] Index on `last_login_at` for analytics queries
     - [ ] Index on `last_activity_at` for cleanup queries
     - [ ] Composite index for common query patterns

3. **Migration Safety**
   - Acceptance criteria:
     - [ ] Online migration (no locking)
     - [ ] Runs in < 10 minutes on production
     - [ ] Rollback plan documented and tested
     - [ ] Zero downtime

#### Should Have
- Trigger to auto-update `last_activity_at`
- View for active users (active in last 30 days)
- Archive table for deleted users

#### Could Have
- Partitioning by activity date
- Separate activity_log table
- Real-time materialized view

### Non-Functional Requirements

- **Performance**:
  - Migration time < 10 minutes
  - No table locks during migration
  - Read query performance unchanged
  - Write query overhead < 5ms

- **Reliability**:
  - Transactional migration
  - Validated on staging first
  - Rollback tested
  - Monitoring during deployment

- **Data Integrity**:
  - Consistent data types
  - Proper constraints
  - NULL handling clear
  - Timezone-aware timestamps

---

## 4. Technical Design

### Schema Changes

#### Current Schema
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Existing indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

#### Proposed Schema
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- New columns
  last_login_at TIMESTAMP WITH TIME ZONE,
  last_activity_at TIMESTAMP WITH TIME ZONE,
  activity_count INTEGER DEFAULT 0 NOT NULL
);

-- New indexes
CREATE INDEX idx_users_last_login_at ON users(last_login_at)
  WHERE last_login_at IS NOT NULL;
CREATE INDEX idx_users_last_activity_at ON users(last_activity_at)
  WHERE last_activity_at IS NOT NULL;
CREATE INDEX idx_users_activity_lookup ON users(last_activity_at, activity_count)
  WHERE last_activity_at IS NOT NULL;
```

### Migration Strategy

#### Step 1: Add Columns (Online)
```sql
-- Add columns with NULL default (fast, no table rewrite)
ALTER TABLE users 
  ADD COLUMN last_login_at TIMESTAMP WITH TIME ZONE,
  ADD COLUMN last_activity_at TIMESTAMP WITH TIME ZONE,
  ADD COLUMN activity_count INTEGER DEFAULT 0 NOT NULL;

-- Add comment for documentation
COMMENT ON COLUMN users.last_login_at IS 'Last successful login timestamp';
COMMENT ON COLUMN users.last_activity_at IS 'Last recorded activity timestamp';
COMMENT ON COLUMN users.activity_count IS 'Total activity events recorded';
```

#### Step 2: Create Indexes Concurrently
```sql
-- Create indexes without blocking writes
CREATE INDEX CONCURRENTLY idx_users_last_login_at 
  ON users(last_login_at) 
  WHERE last_login_at IS NOT NULL;

CREATE INDEX CONCURRENTLY idx_users_last_activity_at 
  ON users(last_activity_at) 
  WHERE last_activity_at IS NOT NULL;

CREATE INDEX CONCURRENTLY idx_users_activity_lookup 
  ON users(last_activity_at, activity_count) 
  WHERE last_activity_at IS NOT NULL;
```

#### Step 3: Verify
```sql
-- Check columns exist
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' 
  AND column_name IN ('last_login_at', 'last_activity_at', 'activity_count');

-- Check indexes exist
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'users' 
  AND indexname LIKE '%activity%';

-- Verify no locks
SELECT * FROM pg_locks WHERE relation = 'users'::regclass;
```

### Rollback Strategy

#### If migration fails mid-flight:
```sql
-- Drop indexes (fast)
DROP INDEX CONCURRENTLY IF EXISTS idx_users_last_login_at;
DROP INDEX CONCURRENTLY IF EXISTS idx_users_last_activity_at;
DROP INDEX CONCURRENTLY IF EXISTS idx_users_activity_lookup;

-- Drop columns (requires ACCESS EXCLUSIVE lock, but table is small after cleanup)
ALTER TABLE users 
  DROP COLUMN IF EXISTS last_login_at,
  DROP COLUMN IF EXISTS last_activity_at,
  DROP COLUMN IF EXISTS activity_count;
```

#### Note on Rollback
- Column drops require brief lock (< 1s on our table size)
- Should only rollback if migration fails
- After successful migration, no rollback planned (columns harmless if unused)

### Application Integration

#### Update on Login
```typescript
async function recordLogin(userId: string): Promise<void> {
  await db.query(
    `UPDATE users 
     SET last_login_at = NOW(),
         last_activity_at = NOW(),
         activity_count = activity_count + 1
     WHERE id = $1`,
    [userId]
  );
}
```

#### Update on Activity
```typescript
async function recordActivity(userId: string): Promise<void> {
  await db.query(
    `UPDATE users 
     SET last_activity_at = NOW(),
         activity_count = activity_count + 1
     WHERE id = $1`,
    [userId]
  );
}
```

#### Batch Update (Optional Performance Optimization)
```typescript
// Buffer updates and flush every 5 minutes
class ActivityTracker {
  private buffer: Map<string, Date> = new Map();
  
  recordActivity(userId: string): void {
    this.buffer.set(userId, new Date());
  }
  
  async flush(): Promise<void> {
    const entries = Array.from(this.buffer.entries());
    if (entries.length === 0) return;
    
    await db.query(
      `UPDATE users 
       SET last_activity_at = v.timestamp,
           activity_count = activity_count + 1
       FROM (VALUES ${entries.map((_, i) => `($${i*2+1}, $${i*2+2})`).join(',')}) 
         AS v(user_id, timestamp)
       WHERE users.id = v.user_id::uuid`,
      entries.flatMap(([id, ts]) => [id, ts])
    );
    
    this.buffer.clear();
  }
}
```

---

## 5. Analytics Queries

### Active Users (Last 30 Days)
```sql
SELECT COUNT(*) 
FROM users 
WHERE last_activity_at >= NOW() - INTERVAL '30 days';
```

### User Segments by Activity
```sql
-- Very active: > 100 activities
-- Active: 10-100 activities
-- Occasional: 1-10 activities
-- Inactive: 0 activities

SELECT 
  CASE 
    WHEN activity_count > 100 THEN 'very_active'
    WHEN activity_count >= 10 THEN 'active'
    WHEN activity_count > 0 THEN 'occasional'
    ELSE 'inactive'
  END AS segment,
  COUNT(*) as user_count,
  AVG(EXTRACT(EPOCH FROM (NOW() - last_activity_at))/86400) as avg_days_since_activity
FROM users
GROUP BY segment;
```

### Churn Risk (No Activity in 60 Days)
```sql
SELECT 
  id, 
  email, 
  username,
  last_activity_at,
  EXTRACT(EPOCH FROM (NOW() - last_activity_at))/86400 AS days_inactive
FROM users
WHERE last_activity_at < NOW() - INTERVAL '60 days'
  OR last_activity_at IS NULL
ORDER BY last_activity_at ASC NULLS FIRST
LIMIT 1000;
```

---

## 6. Performance Considerations

### Migration Performance

**Table Size**: 5M rows, ~2GB
**Expected Duration**: 
- Add columns: < 1 second (metadata only)
- Create indexes: 5-8 minutes (concurrent, non-blocking)
- Total: < 10 minutes

**Testing on Staging**: 
- Staging has 1M rows, similar schema
- Test migration took 2 minutes
- Extrapolated to production: ~10 minutes

### Query Performance Impact

**Before Migration**:
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE id = '...';
-- Planning Time: 0.05 ms
-- Execution Time: 0.08 ms
```

**After Migration** (Expected):
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE id = '...';
-- Planning Time: 0.06 ms (+0.01ms)
-- Execution Time: 0.09 ms (+0.01ms)
```

**Impact**: < 1% on primary key lookups

### Write Performance

**Current**: ~1000 inserts/sec
**After Migration**: ~950 inserts/sec (estimated -5%)
**Mitigation**: Use batch updates for activity tracking

---

## 7. Testing Strategy

### Pre-Migration Tests
1. **Staging Migration**
   - Run full migration on staging
   - Verify schema matches expected
   - Check all indexes created
   - Measure migration time

2. **Performance Baseline**
   - Measure current query performance
   - Document baseline metrics
   - Identify slow queries

### During Migration
1. **Monitoring**
   - Watch database CPU/memory
   - Monitor active connections
   - Check for blocked queries
   - Track migration progress

### Post-Migration Tests
1. **Schema Verification**
   - Columns exist with correct types
   - Indexes exist and valid
   - Constraints applied correctly

2. **Performance Verification**
   - Run baseline queries
   - Compare performance
   - Verify < 5% impact

3. **Functional Tests**
   - Application can update fields
   - Analytics queries work
   - NULL values handled correctly

4. **Rollback Test**
   - Test rollback on staging
   - Verify clean removal
   - Document rollback time

---

## 8. Deployment Plan

### Pre-Deployment
- [ ] Review migration on staging
- [ ] Get DBA approval
- [ ] Schedule maintenance window (optional, not required)
- [ ] Notify team of migration
- [ ] Prepare monitoring dashboard

### Deployment Steps
1. **Take Backup** (10 minutes)
   ```bash
   pg_dump -Fc -f users_backup_$(date +%Y%m%d).dump production_db
   ```

2. **Run Migration** (10 minutes)
   ```bash
   psql production_db -f migrations/add_activity_tracking.sql
   ```

3. **Verify** (5 minutes)
   - Check schema
   - Test queries
   - Monitor performance

4. **Deploy Application Changes** (15 minutes)
   - Deploy code to record activity
   - Enable feature flag
   - Monitor errors

### Post-Deployment
- [ ] Monitor for 1 hour
- [ ] Check error rates
- [ ] Verify data being populated
- [ ] Document any issues

### Rollback Triggers
- Migration takes > 20 minutes
- Database CPU > 90% sustained
- Blocked queries > 1 minute
- Application errors spike

---

## 9. Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Migration timeout | Low | High | Use CONCURRENTLY, test on staging |
| Index creation fails | Low | Medium | Retry with different parameters |
| Performance degradation | Low | Medium | Monitor closely, prepared to disable tracking |
| Application errors | Medium | Medium | Feature flag for easy disable |
| Disk space exhaustion | Low | High | Verify free space before migration (need ~500MB) |

---

## 10. Timeline

- **Day 1**: Test migration on staging, measure performance
- **Day 2**: Review with DBA, get approval
- **Day 3**: Deploy to production during low-traffic window
- **Day 4**: Monitor and adjust
- **Day 5**: Enable application tracking

**Total**: 5 days

---

## 11. Open Questions

1. Should we backfill historical data from logs?
   - **Status**: Resolved
   - **Decision**: No, start tracking from migration forward
   - **Rationale**: Complex, error-prone, diminishing value

2. Partition table by activity date?
   - **Status**: Deferred
   - **Decision**: Not now, revisit if table grows > 50M rows

---

## 12. Decisions

### Decision 1: Column Names
- **Date**: 2024-03-16
- **Decision**: Use `last_login_at` and `last_activity_at` (not `last_seen`)
- **Rationale**: More specific, distinguishes between login and general activity

### Decision 2: Batch vs. Real-time Updates
- **Date**: 2024-03-17
- **Decision**: Start with real-time, optimize to batch if needed
- **Rationale**: Simpler to implement, optimize later if performance issue

### Decision 3: Partial Indexes
- **Date**: 2024-03-17
- **Decision**: Use `WHERE column IS NOT NULL` on indexes
- **Rationale**: Reduces index size, most queries filter out NULL anyway
