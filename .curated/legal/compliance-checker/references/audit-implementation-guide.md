# CCPA Audit Implementation Guide

## Overview

This guide provides practical steps for implementing the CCPA compliance audit architecture. It includes setup instructions, configuration examples, and operational procedures.

## Prerequisites

### Technical Requirements

- **Database**: PostgreSQL 13+ or MySQL 8+ for audit logs
- **Time-Series Database**: InfluxDB or TimescaleDB for metrics
- **Message Queue**: RabbitMQ or Apache Kafka for event processing
- **Cache**: Redis 6+ for real-time data
- **Storage**: S3-compatible object storage for log archives
- **Monitoring**: Prometheus + Grafana or similar

### Skills Required

- Privacy/compliance expertise
- Database administration
- Systems integration
- API development
- Security practices

### Resources Needed

- Privacy officer or compliance lead
- Development team (2-3 engineers)
- Security team involvement
- Legal team consultation

## Phase 1: Foundation (Weeks 1-2)

### 1.1 Data Inventory

Create a comprehensive inventory of personal information:

```yaml
# data-inventory.yaml
data_categories:
  - category: identifiers
    examples:
      - name
      - email
      - phone_number
      - ip_address
    sources:
      - web_registration
      - mobile_app
      - crm_system
    purposes:
      - account_creation
      - customer_support
    retention_period: "7 years from last activity"
    
  - category: commercial_information
    examples:
      - purchase_history
      - payment_information
    sources:
      - ecommerce_platform
      - payment_processor
    purposes:
      - order_fulfillment
      - fraud_prevention
    retention_period: "7 years for tax purposes"
    
  - category: internet_activity
    examples:
      - browsing_history
      - search_history
      - interactions
    sources:
      - web_analytics
      - cdn_logs
    purposes:
      - service_improvement
      - personalization
    retention_period: "2 years from collection"
```

### 1.2 Privacy Policy Audit

Review current privacy policy against CCPA requirements:

**Checklist**:
- [ ] Last 12 months of PI categories collected
- [ ] Sources of PI documented
- [ ] Business purposes listed
- [ ] Third-party disclosure categories
- [ ] Selling/sharing practices disclosed
- [ ] Sensitive PI handling described
- [ ] Retention periods specified
- [ ] Consumer rights detailed
- [ ] Request submission instructions
- [ ] Contact information provided
- [ ] Update date within last 12 months

### 1.3 Request Tracking Setup

Implement a system to track consumer requests:

**PostgreSQL Schema:**

```sql
-- Database schema for request tracking (PostgreSQL)
CREATE TABLE consumer_requests (
    request_id UUID PRIMARY KEY,
    consumer_id VARCHAR(255) NOT NULL,
    request_type VARCHAR(50) NOT NULL, -- 'know', 'delete', 'correct', 'opt_out', 'limit_sensitive'
    submission_date TIMESTAMP NOT NULL,
    submission_method VARCHAR(50), -- 'web_form', 'email', 'phone', 'mail'
    status VARCHAR(50) NOT NULL, -- 'received', 'verifying', 'processing', 'completed', 'denied'
    response_date TIMESTAMP,
    response_method VARCHAR(50),
    days_to_respond INTEGER,
    denial_reason TEXT,
    verification_method VARCHAR(100),
    verification_date TIMESTAMP,
    assigned_to VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submission_date ON consumer_requests(submission_date);
CREATE INDEX idx_status ON consumer_requests(status);
CREATE INDEX idx_consumer_id ON consumer_requests(consumer_id);
CREATE INDEX idx_request_type ON consumer_requests(request_type);

-- Trigger for updated_at (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_consumer_requests_updated_at BEFORE UPDATE
    ON consumer_requests FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Audit log for request actions (PostgreSQL)
CREATE TABLE request_audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    request_id UUID NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    action VARCHAR(100) NOT NULL,
    actor VARCHAR(255) NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (request_id) REFERENCES consumer_requests(request_id)
);

CREATE INDEX idx_request_id ON request_audit_log(request_id);
CREATE INDEX idx_timestamp ON request_audit_log(timestamp);
```

**MySQL Schema:**

```sql
-- Database schema for request tracking (MySQL)
CREATE TABLE consumer_requests (
    request_id CHAR(36) PRIMARY KEY,
    consumer_id VARCHAR(255) NOT NULL,
    request_type VARCHAR(50) NOT NULL, -- 'know', 'delete', 'correct', 'opt_out', 'limit_sensitive'
    submission_date TIMESTAMP NOT NULL,
    submission_method VARCHAR(50), -- 'web_form', 'email', 'phone', 'mail'
    status VARCHAR(50) NOT NULL, -- 'received', 'verifying', 'processing', 'completed', 'denied'
    response_date TIMESTAMP NULL,
    response_method VARCHAR(50),
    days_to_respond INTEGER,
    denial_reason TEXT,
    verification_method VARCHAR(100),
    verification_date TIMESTAMP NULL,
    assigned_to VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_submission_date (submission_date),
    INDEX idx_status (status),
    INDEX idx_consumer_id (consumer_id),
    INDEX idx_request_type (request_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Audit log for request actions (MySQL)
CREATE TABLE request_audit_log (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    request_id CHAR(36) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    action VARCHAR(100) NOT NULL,
    actor VARCHAR(255) NOT NULL,
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (request_id) REFERENCES consumer_requests(request_id),
    INDEX idx_request_id (request_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Phase 2: Core Audit Infrastructure (Weeks 3-4)

### 2.1 Event Collection Setup

Implement event collectors to capture compliance-relevant events:

```python
# event_collector.py
from datetime import datetime
from typing import Dict, Any
import json

class ComplianceEventCollector:
    def __init__(self, event_bus, audit_log_store):
        self.event_bus = event_bus
        self.audit_log_store = audit_log_store
    
    def _generate_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _get_source_info(self) -> Dict[str, Any]:
        """Get information about the event source"""
        import socket
        return {
            'hostname': socket.gethostname(),
            'service': 'compliance-audit',
            'version': '1.0'
        }
    
    def _hash_identifier(self, identifier: str) -> str:
        """Hash sensitive identifiers for privacy"""
        import hashlib
        return hashlib.sha256(identifier.encode()).hexdigest()
    
    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Log a compliance event with full context"""
        event = {
            'event_id': self._generate_id(),
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details,
            'source': self._get_source_info()
        }
        
        # Publish to event bus for real-time processing
        self.event_bus.publish('compliance.events', event)
        
        # Store in audit log for historical record
        self.audit_log_store.write(event)
        
        return event['event_id']
    
    def log_request_received(self, request_data: Dict[str, Any]):
        """Log consumer request submission"""
        return self.log_event('consumer_request_received', {
            'request_id': request_data['id'],
            'request_type': request_data['type'],
            'consumer_identifier': self._hash_identifier(request_data['consumer']),
            'submission_method': request_data['method']
        })
    
    def log_data_access(self, accessor: str, data_category: str, purpose: str):
        """Log access to personal information"""
        return self.log_event('data_accessed', {
            'accessor': accessor,
            'data_category': data_category,
            'purpose': purpose,
            'access_time': datetime.utcnow().isoformat()
        })
    
    def log_data_deletion(self, consumer_id: str, categories: list):
        """Log data deletion action"""
        return self.log_event('data_deleted', {
            'consumer_id': self._hash_identifier(consumer_id),
            'categories': categories,
            'deletion_time': datetime.utcnow().isoformat()
        })
```

### 2.2 Validation Rules Engine

Create automated compliance validation checks:

```python
# validation_rules.py
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Any

class ValidationRule(ABC):
    def __init__(self, rule_id: str, description: str, severity: str):
        self.rule_id = rule_id
        self.description = description
        self.severity = severity  # 'critical', 'high', 'medium', 'low'
    
    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute validation check and return result"""
        pass

class RequestDeadlineRule(ValidationRule):
    def __init__(self):
        super().__init__(
            rule_id='CCPA-REQ-001',
            description='Consumer requests must be responded to within 45 days',
            severity='critical'
        )
    
    def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if requests are approaching or past deadline"""
        db = context['database']
        today = datetime.now()
        
        # Query open requests
        open_requests = db.query("""
            SELECT request_id, consumer_id, request_type, submission_date,
                   DATEDIFF(CURDATE(), submission_date) as days_elapsed
            FROM consumer_requests
            WHERE status NOT IN ('completed', 'denied')
        """)
        
        findings = []
        for request in open_requests:
            days = request['days_elapsed']
            
            if days >= 45:
                findings.append({
                    'finding_type': 'deadline_missed',
                    'severity': 'critical',
                    'request_id': request['request_id'],
                    'days_overdue': days - 45,
                    'message': f"Request {request['request_id']} is {days - 45} days overdue"
                })
            elif days >= 40:
                findings.append({
                    'finding_type': 'deadline_imminent',
                    'severity': 'high',
                    'request_id': request['request_id'],
                    'days_remaining': 45 - days,
                    'message': f"Request {request['request_id']} has only {45 - days} days remaining"
                })
            elif days >= 35:
                findings.append({
                    'finding_type': 'deadline_approaching',
                    'severity': 'medium',
                    'request_id': request['request_id'],
                    'days_remaining': 45 - days,
                    'message': f"Request {request['request_id']} approaching deadline"
                })
        
        return {
            'rule_id': self.rule_id,
            'passed': len([f for f in findings if f['severity'] in ['critical', 'high']]) == 0,
            'findings': findings,
            'checked_at': datetime.utcnow().isoformat()
        }

class PrivacyPolicyFreshnessRule(ValidationRule):
    def __init__(self):
        super().__init__(
            rule_id='CCPA-PP-002',
            description='Privacy policy must be updated at least annually',
            severity='high'
        )
    
    def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if privacy policy has been updated in last 12 months"""
        policy_repo = context['policy_repository']
        last_update = policy_repo.get_last_update_date()
        
        twelve_months_ago = datetime.now() - timedelta(days=365)
        is_fresh = last_update > twelve_months_ago
        
        finding = None
        if not is_fresh:
            days_overdue = (datetime.now() - last_update - timedelta(days=365)).days
            finding = {
                'finding_type': 'policy_outdated',
                'severity': 'high',
                'last_update': last_update.isoformat(),
                'days_overdue': days_overdue,
                'message': f"Privacy policy is {days_overdue} days overdue for annual update"
            }
        
        return {
            'rule_id': self.rule_id,
            'passed': is_fresh,
            'findings': [finding] if finding else [],
            'checked_at': datetime.utcnow().isoformat()
        }

class DataRetentionRule(ValidationRule):
    def __init__(self):
        super().__init__(
            rule_id='CCPA-RET-001',
            description='Personal information must not be retained beyond stated period',
            severity='medium'
        )
    
    def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check for data exceeding retention period"""
        db = context['database']
        data_inventory = context['data_inventory']
        
        findings = []
        
        for category in data_inventory.get_categories():
            retention_days = category['retention_period_days']
            
            # Query for data exceeding retention
            expired_data = db.query(f"""
                SELECT COUNT(*) as count, MIN(collection_date) as oldest
                FROM {category['table_name']}
                WHERE collection_date < DATE_SUB(CURDATE(), INTERVAL {retention_days} DAY)
                AND deletion_date IS NULL
            """)
            
            if expired_data['count'] > 0:
                findings.append({
                    'finding_type': 'retention_exceeded',
                    'severity': 'medium',
                    'category': category['name'],
                    'count': expired_data['count'],
                    'oldest_date': expired_data['oldest'],
                    'message': f"{expired_data['count']} records in {category['name']} exceed retention period"
                })
        
        return {
            'rule_id': self.rule_id,
            'passed': len(findings) == 0,
            'findings': findings,
            'checked_at': datetime.utcnow().isoformat()
        }
```

### 2.3 Alert Configuration

Set up alerting for critical compliance events:

```yaml
# alerts-config.yaml
alert_rules:
  - name: request_deadline_critical
    condition: "days_until_deadline <= 0"
    severity: critical
    channels:
      - email
      - sms
      - pagerduty
    recipients:
      - privacy-team@company.com
      - compliance-lead@company.com
    template: |
      CRITICAL: Consumer request #{request_id} has exceeded 45-day deadline
      Request Type: {request_type}
      Days Overdue: {days_overdue}
      Action Required: Immediate response and documentation
  
  - name: request_deadline_approaching
    condition: "days_until_deadline <= 5"
    severity: high
    channels:
      - email
      - slack
    recipients:
      - privacy-team@company.com
    template: |
      URGENT: Consumer request #{request_id} deadline approaching
      Request Type: {request_type}
      Days Remaining: {days_remaining}
      Please prioritize processing
  
  - name: security_incident_detected
    condition: "event_type == 'unauthorized_access'"
    severity: critical
    channels:
      - email
      - sms
      - slack
    recipients:
      - security-team@company.com
      - privacy-team@company.com
      - legal-team@company.com
    template: |
      SECURITY INCIDENT: Unauthorized access to personal information
      Category: {data_category}
      Time: {timestamp}
      Affected Records: {record_count}
      Immediate investigation required
  
  - name: policy_update_required
    condition: "days_since_policy_update > 365"
    severity: high
    channels:
      - email
    recipients:
      - privacy-team@company.com
      - legal-team@company.com
    template: |
      Privacy policy requires annual update
      Last Updated: {last_update_date}
      Days Overdue: {days_overdue}
      Please schedule policy review
```

## Phase 3: Reporting & Dashboards (Week 5)

### 3.1 Compliance Metrics

Define and track key compliance metrics:

```python
# metrics.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class ComplianceMetrics:
    """Container for compliance metrics"""
    period_start: datetime
    period_end: datetime
    
    # Request metrics
    total_requests: int
    requests_by_type: dict
    requests_completed: int
    requests_denied: int
    median_response_days: float
    on_time_completion_rate: float
    
    # Compliance metrics
    compliance_score: float
    open_findings: int
    findings_by_severity: dict
    
    # Risk metrics
    high_risk_items: int
    new_risks_this_period: int
    risks_mitigated: int

def calculate_metrics(db, start_date: datetime, end_date: datetime) -> ComplianceMetrics:
    """Calculate compliance metrics for a time period"""
    
    # Request metrics
    requests = db.query("""
        SELECT 
            COUNT(*) as total,
            request_type,
            status,
            days_to_respond
        FROM consumer_requests
        WHERE submission_date BETWEEN %s AND %s
        GROUP BY request_type, status
    """, (start_date, end_date))
    
    total_requests = sum(r['total'] for r in requests)
    requests_by_type = {}
    completed = 0
    denied = 0
    response_times = []
    
    for r in requests:
        requests_by_type[r['request_type']] = requests_by_type.get(r['request_type'], 0) + r['total']
        if r['status'] == 'completed':
            completed += r['total']
            if r['days_to_respond']:
                response_times.append(r['days_to_respond'])
        elif r['status'] == 'denied':
            denied += r['total']
    
    median_response = sorted(response_times)[len(response_times)//2] if response_times else 0
    on_time_rate = len([t for t in response_times if t <= 45]) / len(response_times) if response_times else 1.0
    
    # Compliance findings
    findings = db.query("""
        SELECT severity, COUNT(*) as count
        FROM compliance_findings
        WHERE status = 'open'
        GROUP BY severity
    """)
    
    findings_by_severity = {f['severity']: f['count'] for f in findings}
    open_findings = sum(findings_by_severity.values())
    
    # Calculate compliance score (example formula)
    base_score = 100
    deductions = (
        findings_by_severity.get('critical', 0) * 10 +
        findings_by_severity.get('high', 0) * 5 +
        findings_by_severity.get('medium', 0) * 2 +
        findings_by_severity.get('low', 0) * 1
    )
    compliance_score = max(0, base_score - deductions)
    
    return ComplianceMetrics(
        period_start=start_date,
        period_end=end_date,
        total_requests=total_requests,
        requests_by_type=requests_by_type,
        requests_completed=completed,
        requests_denied=denied,
        median_response_days=median_response,
        on_time_completion_rate=on_time_rate,
        compliance_score=compliance_score,
        open_findings=open_findings,
        findings_by_severity=findings_by_severity,
        high_risk_items=findings_by_severity.get('critical', 0) + findings_by_severity.get('high', 0),
        new_risks_this_period=0,  # Would query risk register
        risks_mitigated=0  # Would query closed risks
    )
```

### 3.2 Report Templates

Create standardized report templates:

```python
# report_generator.py
from jinja2 import Template

MONTHLY_COMPLIANCE_REPORT = Template("""
# CCPA Compliance Report
## Period: {{ metrics.period_start.strftime('%B %Y') }}

### Executive Summary
- **Overall Compliance Score**: {{ "%.1f"|format(metrics.compliance_score) }}%
- **Consumer Requests Processed**: {{ metrics.total_requests }}
- **Median Response Time**: {{ metrics.median_response_days }} days
- **On-Time Completion Rate**: {{ "%.1f"|format(metrics.on_time_completion_rate * 100) }}%

### Consumer Requests
| Request Type | Count |
|--------------|-------|
{% for type, count in metrics.requests_by_type.items() %}
| {{ type }} | {{ count }} |
{% endfor %}
| **Total** | **{{ metrics.total_requests }}** |

**Status Breakdown**:
- Completed: {{ metrics.requests_completed }}
- Denied: {{ metrics.requests_denied }}
- In Progress: {{ metrics.total_requests - metrics.requests_completed - metrics.requests_denied }}

### Compliance Findings
**Open Findings**: {{ metrics.open_findings }}

| Severity | Count |
|----------|-------|
{% for severity, count in metrics.findings_by_severity.items() %}
| {{ severity }} | {{ count }} |
{% endfor %}

### Risk Status
- **High-Risk Items**: {{ metrics.high_risk_items }}
- **New Risks Identified**: {{ metrics.new_risks_this_period }}
- **Risks Mitigated**: {{ metrics.risks_mitigated }}

### Recommendations
{% if metrics.high_risk_items > 0 %}
1. Address {{ metrics.high_risk_items }} high-risk compliance findings immediately
{% endif %}
{% if metrics.on_time_completion_rate < 0.95 %}
2. Improve request processing time to meet 45-day deadline consistently
{% endif %}
{% if metrics.compliance_score < 90 %}
3. Conduct focused audit on areas with open findings
{% endif %}

### Next Period Priorities
1. Close all critical and high-severity findings
2. Maintain on-time request completion above 95%
3. Conduct quarterly comprehensive audit
""")

def generate_monthly_report(metrics: ComplianceMetrics) -> str:
    """Generate monthly compliance report"""
    return MONTHLY_COMPLIANCE_REPORT.render(metrics=metrics)
```

## Phase 4: Operational Procedures (Week 6)

### 4.1 Daily Operations Checklist

```markdown
## Daily Audit Operations Checklist

### Morning Review (9:00 AM)
- [ ] Check dashboard for critical alerts (target: 0)
- [ ] Review requests approaching deadline (40+ days)
- [ ] Verify audit system health and availability
- [ ] Check overnight batch job completion

### Request Monitoring
- [ ] Review new requests received in last 24 hours
- [ ] Verify assignment of unassigned requests
- [ ] Check verification status of pending requests
- [ ] Follow up on requests requiring additional information

### Alert Management
- [ ] Acknowledge and triage new alerts
- [ ] Escalate critical issues to appropriate teams
- [ ] Update status of in-progress investigations
- [ ] Document resolution of closed alerts

### End of Day Review (5:00 PM)
- [ ] Update request processing status
- [ ] Document any compliance incidents
- [ ] Prepare summary for next day handoff
- [ ] Verify all critical alerts addressed
```

### 4.2 Weekly Tasks

```markdown
## Weekly Audit Tasks

### Monday
- [ ] Generate previous week's metrics report
- [ ] Review risk register for new items
- [ ] Schedule follow-ups for open findings
- [ ] Team sync meeting on priorities

### Wednesday
- [ ] Mid-week compliance check
- [ ] Review service provider compliance status
- [ ] Update remediation tracking
- [ ] Test alert mechanisms

### Friday
- [ ] Week-end compliance summary
- [ ] Review and update documentation
- [ ] Prepare weekend escalation procedures
- [ ] Backup verification
```

### 4.3 Monthly Procedures

```markdown
## Monthly Audit Procedures

### Week 1
- [ ] Generate previous month's compliance report
- [ ] Calculate and publish consumer request metrics
- [ ] Review and update privacy policy if needed
- [ ] Conduct internal compliance review

### Week 2
- [ ] Risk assessment update
- [ ] Service provider audit review
- [ ] Training completion verification
- [ ] Control effectiveness testing

### Week 3
- [ ] Comprehensive validation audit
- [ ] Update compliance documentation
- [ ] Review and refine validation rules
- [ ] Stakeholder report distribution

### Week 4
- [ ] Remediation progress review
- [ ] Next month planning
- [ ] Tool and process improvements
- [ ] Team retrospective
```

## Phase 5: Integration & Automation (Weeks 7-8)

### 5.1 API Integration Examples

```python
# api_integration.py
import requests
from typing import Dict, Any

class ComplianceAuditAPI:
    """Client for integrating with compliance audit system"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def submit_consumer_request(self, request_data: Dict[str, Any]) -> str:
        """Submit a new consumer request to audit system"""
        response = requests.post(
            f'{self.base_url}/api/v1/requests',
            headers=self.headers,
            json=request_data
        )
        response.raise_for_status()
        return response.json()['request_id']
    
    def log_data_access(self, access_event: Dict[str, Any]):
        """Log access to personal information"""
        response = requests.post(
            f'{self.base_url}/api/v1/audit/access',
            headers=self.headers,
            json=access_event
        )
        response.raise_for_status()
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get current compliance status"""
        response = requests.get(
            f'{self.base_url}/api/v1/compliance/status',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Example usage in application code
audit_api = ComplianceAuditAPI(
    base_url='https://audit.company.com',
    api_key='your-api-key'
)

# Log when user data is accessed
audit_api.log_data_access({
    'accessor': 'user-service',
    'consumer_id': 'hashed-id-123',
    'data_category': 'identifiers',
    'purpose': 'account_login',
    'timestamp': datetime.utcnow().isoformat()
})
```

### 5.2 Automated Testing

```python
# test_compliance_rules.py
import pytest
from datetime import datetime, timedelta
from validation_rules import RequestDeadlineRule
from typing import List, Dict, Any

class MockDatabase:
    """Mock database for testing validation rules"""
    def __init__(self, mock_data: List[Dict[str, Any]]):
        self.mock_data = mock_data
    
    def query(self, sql: str, params: tuple = None):
        """Return mock data for queries"""
        return self.mock_data

class TestRequestDeadlineRule:
    def test_critical_finding_past_deadline(self):
        """Test that requests past 45 days generate critical finding"""
        rule = RequestDeadlineRule()
        
        # Mock database with overdue request
        mock_db = MockDatabase([{
            'request_id': 'req-123',
            'consumer_id': 'consumer-456',
            'request_type': 'delete',
            'submission_date': datetime.now() - timedelta(days=50),
            'days_elapsed': 50
        }])
        
        result = rule.validate({'database': mock_db})
        
        assert not result['passed']
        assert len(result['findings']) == 1
        assert result['findings'][0]['severity'] == 'critical'
        assert result['findings'][0]['days_overdue'] == 5
    
    def test_high_severity_imminent_deadline(self):
        """Test that requests within 5 days of deadline generate high severity"""
        rule = RequestDeadlineRule()
        
        mock_db = MockDatabase([{
            'request_id': 'req-789',
            'consumer_id': 'consumer-101',
            'request_type': 'know',
            'submission_date': datetime.now() - timedelta(days=42),
            'days_elapsed': 42
        }])
        
        result = rule.validate({'database': mock_db})
        
        assert not result['passed']
        assert result['findings'][0]['severity'] == 'high'
        assert result['findings'][0]['days_remaining'] == 3
    
    def test_no_findings_for_recent_requests(self):
        """Test that recent requests generate no findings"""
        rule = RequestDeadlineRule()
        
        mock_db = MockDatabase([{
            'request_id': 'req-999',
            'consumer_id': 'consumer-888',
            'request_type': 'know',
            'submission_date': datetime.now() - timedelta(days=20),
            'days_elapsed': 20
        }])
        
        result = rule.validate({'database': mock_db})
        
        assert result['passed']
        assert len(result['findings']) == 0
```

## Troubleshooting Guide

### Common Issues

#### Issue: High False Positive Rate in Validation Checks
**Symptoms**: Many alerts for non-violations
**Solutions**:
1. Review validation rule logic
2. Adjust severity thresholds
3. Add exclusion criteria for known edge cases
4. Implement feedback loop from alert handlers

#### Issue: Slow Audit Processing
**Symptoms**: Audits taking too long to complete
**Solutions**:
1. Add database indexes on frequently queried columns
2. Implement incremental validation for large datasets
3. Use parallel processing for independent checks
4. Cache intermediate results

#### Issue: Alert Fatigue
**Symptoms**: Team ignoring alerts due to volume
**Solutions**:
1. Increase severity thresholds for alerts
2. Implement alert aggregation and batching
3. Add snooze capability for known issues
4. Create escalation tiers

## Security Considerations

### Access Control
- Implement role-based access (viewer, analyst, administrator)
- Require multi-factor authentication
- Log all access to audit system
- Separate production and test environments

### Data Protection
- Encrypt personal identifiers in audit logs
- Use secure connections (TLS 1.3+)
- Implement data retention for audit logs (minimum 24 months)
- Regular security assessments

### Incident Response
- Document procedure for audit system compromise
- Maintain offline backup of critical audit data
- Test disaster recovery procedures quarterly
- Maintain chain of custody for audit evidence

## Next Steps

After implementing the basic audit architecture:

1. **Expand Coverage**: Add validation rules for additional CCPA requirements
2. **Enhance Automation**: Implement auto-remediation for low-risk findings
3. **Integration**: Connect with additional enterprise systems
4. **Machine Learning**: Add predictive analytics for risk assessment
5. **Certification**: Pursue third-party audit certification

## Support & Resources

### Internal Resources
- Privacy Team: privacy-team@company.com
- Security Team: security-team@company.com
- IT Support: it-support@company.com

### External Resources
- CCPA Official Site: https://oag.ca.gov/privacy/ccpa
- IAPP (Privacy Professional Association): https://iapp.org
- NIST Privacy Framework: https://www.nist.gov/privacy-framework

### Training
- CCPA Compliance Training (monthly)
- Audit System User Training (quarterly)
- Technical Implementation Workshops (as needed)
