"""
Record Keeping System for AI Act Compliance (Article 12)

This module implements comprehensive record keeping procedures required under 
Article 12 of the EU AI Act for high-risk AI systems.
"""

import json
import datetime
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class RecordType(Enum):
    """Types of records to be kept"""
    SYSTEM_OPERATION = "system_operation"
    USER_INTERACTION = "user_interaction"
    AI_DECISION = "ai_decision"
    HUMAN_OVERSIGHT = "human_oversight"
    RISK_ASSESSMENT = "risk_assessment"
    DATA_PROCESSING = "data_processing"
    INCIDENT = "incident"
    COMPLIANCE_AUDIT = "compliance_audit"

class RecordStatus(Enum):
    """Record status"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

@dataclass
class SystemRecord:
    """System operation record"""
    id: str
    record_type: RecordType
    timestamp: str
    user_id: Optional[str]
    session_id: Optional[str]
    action: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    processing_time_ms: int
    ai_model_used: str
    confidence_score: Optional[float]
    human_reviewed: bool
    status: RecordStatus
    metadata: Dict[str, Any]

@dataclass
class AuditTrail:
    """Audit trail entry"""
    id: str
    timestamp: str
    user_id: Optional[str]
    action: str
    resource: str
    old_value: Optional[Any]
    new_value: Optional[Any]
    reason: str
    ip_address: Optional[str]
    user_agent: Optional[str]

class RecordKeepingSystem:
    """AI Act compliant record keeping system"""
    
    def __init__(self):
        self.records: List[SystemRecord] = []
        self.audit_trails: List[AuditTrail] = []
        self.records_file = "data/system_records.json"
        self.audit_file = "data/audit_trails.json"
        self._load_existing_records()
    
    def _load_existing_records(self):
        """Load existing records from files"""
        try:
            # Load system records
            with open(self.records_file, 'r') as f:
                data = json.load(f)
                # Convert string values back to enums
                records = []
                for record in data.get('records', []):
                    if isinstance(record.get('record_type'), str):
                        record['record_type'] = RecordType(record['record_type'])
                    if isinstance(record.get('status'), str):
                        record['status'] = RecordStatus(record['status'])
                    records.append(SystemRecord(**record))
                self.records = records
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading system records: {e}")
        
        try:
            # Load audit trails
            with open(self.audit_file, 'r') as f:
                data = json.load(f)
                self.audit_trails = [AuditTrail(**trail) for trail in data.get('audit_trails', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading audit trails: {e}")
    
    def _serialize_record(self, record: SystemRecord) -> Dict[str, Any]:
        """Serialize record object for JSON storage"""
        record_dict = asdict(record)
        record_dict['record_type'] = record.record_type.value
        record_dict['status'] = record.status.value
        return record_dict
    
    def _save_records(self):
        """Save system records to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.records_file), exist_ok=True)
            
            data = {
                'records': [self._serialize_record(record) for record in self.records],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.records_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving system records: {e}")
    
    def _save_audit_trails(self):
        """Save audit trails to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.audit_file), exist_ok=True)
            
            data = {
                'audit_trails': [asdict(trail) for trail in self.audit_trails],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.audit_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving audit trails: {e}")
    
    def log_system_operation(self, record_type: RecordType, user_id: Optional[str],
                           session_id: Optional[str], action: str, input_data: Dict[str, Any],
                           output_data: Dict[str, Any], processing_time_ms: int,
                           ai_model_used: str, confidence_score: Optional[float] = None,
                           human_reviewed: bool = False, metadata: Dict[str, Any] = None) -> str:
        """Log a system operation"""
        record_id = str(uuid.uuid4())
        
        record = SystemRecord(
            id=record_id,
            record_type=record_type,
            timestamp=datetime.datetime.now().isoformat(),
            user_id=user_id,
            session_id=session_id,
            action=action,
            input_data=input_data,
            output_data=output_data,
            processing_time_ms=processing_time_ms,
            ai_model_used=ai_model_used,
            confidence_score=confidence_score,
            human_reviewed=human_reviewed,
            status=RecordStatus.ACTIVE,
            metadata=metadata or {}
        )
        
        self.records.append(record)
        self._save_records()
        
        # Create audit trail entry
        self.create_audit_trail(
            user_id=user_id,
            action=f"system_operation_{action}",
            resource=f"record_{record_id}",
            old_value=None,
            new_value=action,
            reason=f"System operation logged: {action}"
        )
        
        return record_id
    
    def create_audit_trail(self, user_id: Optional[str], action: str, resource: str,
                          old_value: Optional[Any], new_value: Optional[Any], reason: str,
                          ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> str:
        """Create an audit trail entry"""
        trail_id = str(uuid.uuid4())
        
        trail = AuditTrail(
            id=trail_id,
            timestamp=datetime.datetime.now().isoformat(),
            user_id=user_id,
            action=action,
            resource=resource,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.audit_trails.append(trail)
        self._save_audit_trails()
        
        return trail_id
    
    def log_user_interaction(self, user_id: str, session_id: str, query: str,
                           response: str, ai_model: str, processing_time_ms: int,
                           confidence_score: Optional[float] = None) -> str:
        """Log user interaction with AI system"""
        return self.log_system_operation(
            record_type=RecordType.USER_INTERACTION,
            user_id=user_id,
            session_id=session_id,
            action="user_query_processed",
            input_data={"query": query},
            output_data={"response": response},
            processing_time_ms=processing_time_ms,
            ai_model_used=ai_model,
            confidence_score=confidence_score,
            metadata={"interaction_type": "chat"}
        )
    
    def log_human_oversight(self, user_id: str, record_id: str, action: str,
                          review_result: str, notes: str = "") -> str:
        """Log human oversight activity"""
        return self.log_system_operation(
            record_type=RecordType.HUMAN_OVERSIGHT,
            user_id=user_id,
            session_id=None,
            action=f"human_review_{action}",
            input_data={"reviewed_record_id": record_id},
            output_data={"review_result": review_result, "notes": notes},
            processing_time_ms=0,
            ai_model_used="human_reviewer",
            human_reviewed=True,
            metadata={"oversight_type": action}
        )
    
    def log_incident(self, incident_type: str, description: str, severity: str,
                    user_id: Optional[str] = None, affected_records: List[str] = None) -> str:
        """Log a system incident"""
        return self.log_system_operation(
            record_type=RecordType.INCIDENT,
            user_id=user_id,
            session_id=None,
            action="incident_logged",
            input_data={"incident_type": incident_type, "description": description},
            output_data={"severity": severity, "affected_records": affected_records or []},
            processing_time_ms=0,
            ai_model_used="system",
            metadata={"incident_severity": severity}
        )
    
    def get_records_by_type(self, record_type: RecordType, 
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> List[SystemRecord]:
        """Get records filtered by type and date range"""
        filtered_records = [r for r in self.records if r.record_type == record_type]
        
        if start_date:
            filtered_records = [r for r in filtered_records if r.timestamp >= start_date]
        
        if end_date:
            filtered_records = [r for r in filtered_records if r.timestamp <= end_date]
        
        return sorted(filtered_records, key=lambda x: x.timestamp, reverse=True)
    
    def get_user_interaction_history(self, user_id: str, limit: int = 100) -> List[SystemRecord]:
        """Get user interaction history"""
        user_records = [r for r in self.records if r.user_id == user_id and r.record_type == RecordType.USER_INTERACTION]
        return sorted(user_records, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_audit_trail(self, resource: Optional[str] = None, 
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> List[AuditTrail]:
        """Get audit trail entries"""
        filtered_trails = self.audit_trails
        
        if resource:
            filtered_trails = [t for t in filtered_trails if t.resource == resource]
        
        if start_date:
            filtered_trails = [t for t in filtered_trails if t.timestamp >= start_date]
        
        if end_date:
            filtered_trails = [t for t in filtered_trails if t.timestamp <= end_date]
        
        return sorted(filtered_trails, key=lambda x: x.timestamp, reverse=True)
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get record keeping compliance summary"""
        # Count records by type
        records_by_type = {}
        for record in self.records:
            record_type = record.record_type.value
            records_by_type[record_type] = records_by_type.get(record_type, 0) + 1
        
        # Count audit trails
        total_audit_trails = len(self.audit_trails)
        
        # Calculate retention compliance
        retention_compliance = self._check_retention_compliance()
        
        # Get recent activity
        recent_records = [r for r in self.records if self._is_recent(r.timestamp, days=7)]
        recent_audit_trails = [t for t in self.audit_trails if self._is_recent(t.timestamp, days=7)]
        
        return {
            "total_records": len(self.records),
            "records_by_type": records_by_type,
            "total_audit_trails": total_audit_trails,
            "retention_compliance": retention_compliance,
            "recent_activity": {
                "records_last_7_days": len(recent_records),
                "audit_trails_last_7_days": len(recent_audit_trails)
            },
            "last_record_date": max([r.timestamp for r in self.records]) if self.records else None,
            "last_audit_date": max([t.timestamp for t in self.audit_trails]) if self.audit_trails else None
        }
    
    def _check_retention_compliance(self) -> Dict[str, Any]:
        """Check if records are being retained according to policy"""
        # AI Act requires records to be kept for at least 10 years for high-risk systems
        retention_period_days = 3650  # 10 years
        
        current_date = datetime.datetime.now()
        compliance_status = {
            "retention_period_days": retention_period_days,
            "records_within_retention": 0,
            "records_outside_retention": 0,
            "compliance_percentage": 0.0
        }
        
        for record in self.records:
            record_date = datetime.datetime.fromisoformat(record.timestamp)
            days_old = (current_date - record_date).days
            
            if days_old <= retention_period_days:
                compliance_status["records_within_retention"] += 1
            else:
                compliance_status["records_outside_retention"] += 1
        
        total_records = len(self.records)
        if total_records > 0:
            compliance_status["compliance_percentage"] = (
                compliance_status["records_within_retention"] / total_records * 100
            )
        
        return compliance_status
    
    def _is_recent(self, timestamp: str, days: int = 7) -> bool:
        """Check if timestamp is within specified days"""
        try:
            record_date = datetime.datetime.fromisoformat(timestamp)
            days_old = (datetime.datetime.now() - record_date).days
            return days_old <= days
        except:
            return False
    
    def archive_old_records(self, days_old: int = 3650) -> int:
        """Archive records older than specified days"""
        archived_count = 0
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
        
        for record in self.records:
            if record.status == RecordStatus.ACTIVE:
                record_date = datetime.datetime.fromisoformat(record.timestamp)
                if record_date < cutoff_date:
                    record.status = RecordStatus.ARCHIVED
                    archived_count += 1
        
        if archived_count > 0:
            self._save_records()
        
        return archived_count
    
    def get_record_by_id(self, record_id: str) -> Optional[SystemRecord]:
        """Get specific record by ID"""
        for record in self.records:
            if record.id == record_id:
                return record
        return None

# Global record keeping system instance
record_keeper = RecordKeepingSystem()
