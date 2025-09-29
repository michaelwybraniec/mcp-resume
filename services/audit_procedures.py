"""
Audit Procedures System for AI Act Compliance

This module implements comprehensive audit procedures and protocols
required for AI Act compliance verification and certification.
"""

import json
import datetime
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AuditType(Enum):
    """Types of audits"""
    COMPLIANCE_AUDIT = "compliance_audit"
    RISK_ASSESSMENT = "risk_assessment"
    DATA_QUALITY_AUDIT = "data_quality_audit"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_AUDIT = "performance_audit"
    DOCUMENTATION_AUDIT = "documentation_audit"

class AuditStatus(Enum):
    """Audit status"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AuditResult(Enum):
    """Audit results"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    REQUIRES_ACTION = "requires_action"

@dataclass
class AuditChecklist:
    """Audit checklist item"""
    id: str
    category: str
    description: str
    requirement: str
    evidence_required: str
    status: str  # "pending", "passed", "failed", "not_applicable"
    notes: Optional[str]
    evidence_provided: Optional[str]
    auditor_notes: Optional[str]

@dataclass
class AuditFinding:
    """Audit finding"""
    id: str
    severity: str  # "critical", "major", "minor", "observation"
    category: str
    description: str
    evidence: str
    recommendation: str
    responsible_party: str
    due_date: str
    status: str  # "open", "in_progress", "resolved", "closed"
    resolution_notes: Optional[str]

@dataclass
class AuditReport:
    """Comprehensive audit report"""
    id: str
    audit_type: AuditType
    audit_date: str
    auditor: str
    scope: str
    status: AuditStatus
    result: Optional[AuditResult]
    overall_score: Optional[float]
    checklist_items: List[AuditChecklist]
    findings: List[AuditFinding]
    recommendations: List[str]
    next_audit_date: Optional[str]
    compliance_status: str

class AuditProcedures:
    """Comprehensive audit procedures system"""
    
    def __init__(self):
        self.audit_reports: List[AuditReport] = []
        self.audit_log_file = "data/audit_procedures.json"
        self._load_existing_data()
        self._initialize_default_checklists()
    
    def _load_existing_data(self):
        """Load existing audit data from file"""
        try:
            with open(self.audit_log_file, 'r') as f:
                data = json.load(f)
                self.audit_reports = [self._deserialize_report(report_data) for report_data in data.get('audit_reports', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading audit data: {e}")
    
    def _save_data(self):
        """Save audit data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.audit_log_file), exist_ok=True)
            
            data = {
                'audit_reports': [self._serialize_report(report) for report in self.audit_reports],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.audit_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving audit data: {e}")
    
    def _serialize_report(self, report: AuditReport) -> Dict[str, Any]:
        """Serialize audit report for JSON storage"""
        report_dict = asdict(report)
        report_dict['audit_type'] = report.audit_type.value
        report_dict['status'] = report.status.value
        if report.result:
            report_dict['result'] = report.result.value
        return report_dict
    
    def _deserialize_report(self, report_data: Dict[str, Any]) -> AuditReport:
        """Deserialize audit report from JSON"""
        report_data['audit_type'] = AuditType(report_data['audit_type'])
        report_data['status'] = AuditStatus(report_data['status'])
        if report_data.get('result'):
            report_data['result'] = AuditResult(report_data['result'])
        return AuditReport(**report_data)
    
    def _initialize_default_checklists(self):
        """Initialize default audit checklists"""
        self.checklists = {
            AuditType.COMPLIANCE_AUDIT: [
                AuditChecklist(
                    id="COMP-001",
                    category="AI Transparency",
                    description="AI transparency notices are displayed to users",
                    requirement="Article 13 - Transparency and provision of information to users",
                    evidence_required="Screenshots of transparency notices in application",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="COMP-002",
                    category="Human Oversight",
                    description="Human oversight mechanisms are implemented",
                    requirement="Article 14 - Human oversight",
                    evidence_required="Documentation of oversight procedures and user interface",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="COMP-003",
                    category="Risk Management",
                    description="Risk management system is operational",
                    requirement="Article 9 - Risk management system",
                    evidence_required="Risk assessment reports and mitigation procedures",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="COMP-004",
                    category="Data Governance",
                    description="Data governance procedures are implemented",
                    requirement="Article 10 - Data governance and quality management",
                    evidence_required="Data quality assessments and processing records",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="COMP-005",
                    category="Technical Documentation",
                    description="Technical documentation is complete and up-to-date",
                    requirement="Article 11 - Technical documentation",
                    evidence_required="System architecture and algorithm documentation",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="COMP-006",
                    category="Record Keeping",
                    description="Record keeping system is operational",
                    requirement="Article 12 - Record keeping",
                    evidence_required="System operation logs and audit trails",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                )
            ],
            AuditType.RISK_ASSESSMENT: [
                AuditChecklist(
                    id="RISK-001",
                    category="Risk Identification",
                    description="All system risks have been identified and documented",
                    requirement="Comprehensive risk identification",
                    evidence_required="Risk register and assessment reports",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="RISK-002",
                    category="Risk Mitigation",
                    description="Risk mitigation measures are implemented and effective",
                    requirement="Effective risk mitigation",
                    evidence_required="Mitigation action plans and effectiveness assessments",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                )
            ],
            AuditType.DATA_QUALITY_AUDIT: [
                AuditChecklist(
                    id="DATA-001",
                    category="Data Quality",
                    description="Data quality standards are met",
                    requirement="High-quality training and validation data",
                    evidence_required="Data quality assessment reports",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                ),
                AuditChecklist(
                    id="DATA-002",
                    category="Data Processing",
                    description="Data processing procedures are compliant",
                    requirement="Compliant data processing",
                    evidence_required="Data processing records and procedures",
                    status="pending",
                    notes=None,
                    evidence_provided=None,
                    auditor_notes=None
                )
            ]
        }
    
    def create_audit(self, audit_type: AuditType, auditor: str, scope: str) -> str:
        """Create a new audit"""
        audit_id = str(uuid.uuid4())
        
        # Get checklist for audit type
        checklist_items = self.checklists.get(audit_type, [])
        
        # Create audit report
        audit_report = AuditReport(
            id=audit_id,
            audit_type=audit_type,
            audit_date=datetime.datetime.now().isoformat(),
            auditor=auditor,
            scope=scope,
            status=AuditStatus.PLANNED,
            result=None,
            overall_score=None,
            checklist_items=checklist_items,
            findings=[],
            recommendations=[],
            next_audit_date=None,
            compliance_status="pending"
        )
        
        self.audit_reports.append(audit_report)
        self._save_data()
        
        return audit_id
    
    def start_audit(self, audit_id: str) -> bool:
        """Start an audit"""
        for report in self.audit_reports:
            if report.id == audit_id and report.status == AuditStatus.PLANNED:
                report.status = AuditStatus.IN_PROGRESS
                self._save_data()
                return True
        return False
    
    def complete_checklist_item(self, audit_id: str, checklist_id: str, 
                               status: str, evidence_provided: str, 
                               auditor_notes: str = "") -> bool:
        """Complete a checklist item"""
        for report in self.audit_reports:
            if report.id == audit_id:
                for item in report.checklist_items:
                    if item.id == checklist_id:
                        item.status = status
                        item.evidence_provided = evidence_provided
                        item.auditor_notes = auditor_notes
                        self._save_data()
                        return True
        return False
    
    def add_audit_finding(self, audit_id: str, severity: str, category: str,
                         description: str, evidence: str, recommendation: str,
                         responsible_party: str, due_date: str) -> str:
        """Add an audit finding"""
        finding_id = str(uuid.uuid4())
        
        finding = AuditFinding(
            id=finding_id,
            severity=severity,
            category=category,
            description=description,
            evidence=evidence,
            recommendation=recommendation,
            responsible_party=responsible_party,
            due_date=due_date,
            status="open",
            resolution_notes=None
        )
        
        for report in self.audit_reports:
            if report.id == audit_id:
                report.findings.append(finding)
                self._save_data()
                return finding_id
        return ""
    
    def complete_audit(self, audit_id: str, recommendations: List[str]) -> bool:
        """Complete an audit"""
        for report in self.audit_reports:
            if report.id == audit_id and report.status == AuditStatus.IN_PROGRESS:
                # Calculate overall score
                total_items = len(report.checklist_items)
                passed_items = len([item for item in report.checklist_items if item.status == "passed"])
                report.overall_score = (passed_items / total_items) if total_items > 0 else 0.0
                
                # Determine result
                if report.overall_score >= 0.9:
                    report.result = AuditResult.COMPLIANT
                elif report.overall_score >= 0.7:
                    report.result = AuditResult.PARTIALLY_COMPLIANT
                else:
                    report.result = AuditResult.NON_COMPLIANT
                
                # Set compliance status
                if report.result == AuditResult.COMPLIANT:
                    report.compliance_status = "compliant"
                elif report.result == AuditResult.PARTIALLY_COMPLIANT:
                    report.compliance_status = "partially_compliant"
                else:
                    report.compliance_status = "non_compliant"
                
                report.recommendations = recommendations
                report.status = AuditStatus.COMPLETED
                report.next_audit_date = (datetime.datetime.now() + datetime.timedelta(days=365)).isoformat()
                
                self._save_data()
                return True
        return False
    
    def get_audit_by_id(self, audit_id: str) -> Optional[AuditReport]:
        """Get audit report by ID"""
        for report in self.audit_reports:
            if report.id == audit_id:
                return report
        return None
    
    def get_audits_by_type(self, audit_type: AuditType) -> List[AuditReport]:
        """Get audits by type"""
        return [report for report in self.audit_reports if report.audit_type == audit_type]
    
    def get_audit_summary(self) -> Dict[str, Any]:
        """Get audit summary"""
        total_audits = len(self.audit_reports)
        completed_audits = len([r for r in self.audit_reports if r.status == AuditStatus.COMPLETED])
        
        # Count by result
        results = {}
        for report in self.audit_reports:
            if report.result:
                result = report.result.value
                results[result] = results.get(result, 0) + 1
        
        # Count by type
        types = {}
        for report in self.audit_reports:
            audit_type = report.audit_type.value
            types[audit_type] = types.get(audit_type, 0) + 1
        
        # Get latest audit
        latest_audit = max(self.audit_reports, key=lambda x: x.audit_date) if self.audit_reports else None
        
        return {
            "total_audits": total_audits,
            "completed_audits": completed_audits,
            "audits_by_result": results,
            "audits_by_type": types,
            "latest_audit": {
                "id": latest_audit.id,
                "type": latest_audit.audit_type.value,
                "date": latest_audit.audit_date,
                "result": latest_audit.result.value if latest_audit.result else None,
                "score": latest_audit.overall_score
            } if latest_audit else None
        }
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get overall compliance status"""
        if not self.audit_reports:
            return {"status": "no_audits", "message": "No audits have been conducted"}
        
        # Get latest compliance audit
        compliance_audits = self.get_audits_by_type(AuditType.COMPLIANCE_AUDIT)
        if not compliance_audits:
            return {"status": "no_compliance_audit", "message": "No compliance audits have been conducted"}
        
        latest_compliance_audit = max(compliance_audits, key=lambda x: x.audit_date)
        
        return {
            "status": latest_compliance_audit.compliance_status,
            "last_audit_date": latest_compliance_audit.audit_date,
            "audit_score": latest_compliance_audit.overall_score,
            "audit_result": latest_compliance_audit.result.value if latest_compliance_audit.result else None,
            "next_audit_date": latest_compliance_audit.next_audit_date,
            "open_findings": len([f for f in latest_compliance_audit.findings if f.status == "open"]),
            "total_findings": len(latest_compliance_audit.findings)
        }
    
    def generate_audit_report(self, audit_id: str) -> Dict[str, Any]:
        """Generate detailed audit report"""
        audit = self.get_audit_by_id(audit_id)
        if not audit:
            return {"error": "Audit not found"}
        
        # Calculate statistics
        checklist_stats = {
            "total_items": len(audit.checklist_items),
            "passed": len([item for item in audit.checklist_items if item.status == "passed"]),
            "failed": len([item for item in audit.checklist_items if item.status == "failed"]),
            "pending": len([item for item in audit.checklist_items if item.status == "pending"]),
            "not_applicable": len([item for item in audit.checklist_items if item.status == "not_applicable"])
        }
        
        findings_stats = {
            "total_findings": len(audit.findings),
            "critical": len([f for f in audit.findings if f.severity == "critical"]),
            "major": len([f for f in audit.findings if f.severity == "major"]),
            "minor": len([f for f in audit.findings if f.severity == "minor"]),
            "observation": len([f for f in audit.findings if f.severity == "observation"]),
            "open": len([f for f in audit.findings if f.status == "open"]),
            "resolved": len([f for f in audit.findings if f.status == "resolved"])
        }
        
        return {
            "audit_info": {
                "id": audit.id,
                "type": audit.audit_type.value,
                "date": audit.audit_date,
                "auditor": audit.auditor,
                "scope": audit.scope,
                "status": audit.status.value,
                "result": audit.result.value if audit.result else None,
                "overall_score": audit.overall_score,
                "compliance_status": audit.compliance_status
            },
            "checklist_summary": checklist_stats,
            "findings_summary": findings_stats,
            "recommendations": audit.recommendations,
            "next_audit_date": audit.next_audit_date
        }

# Global audit procedures instance
audit_procedures = AuditProcedures()
