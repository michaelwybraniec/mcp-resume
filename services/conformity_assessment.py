"""
Conformity Assessment System for AI Act Compliance

This module implements comprehensive conformity assessment procedures
required for AI Act compliance certification and regulatory submission.
"""

import json
import datetime
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AssessmentType(Enum):
    """Types of conformity assessments"""
    SELF_ASSESSMENT = "self_assessment"
    THIRD_PARTY_ASSESSMENT = "third_party_assessment"
    REGULATORY_ASSESSMENT = "regulatory_assessment"
    CERTIFICATION_ASSESSMENT = "certification_assessment"

class AssessmentStatus(Enum):
    """Assessment status"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CERTIFIED = "certified"

class ComplianceLevel(Enum):
    """Compliance levels"""
    FULLY_COMPLIANT = "fully_compliant"
    SUBSTANTIALLY_COMPLIANT = "substantially_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"

@dataclass
class AssessmentCriteria:
    """Assessment criteria data structure"""
    id: str
    article: str
    requirement: str
    description: str
    evidence_required: str
    assessment_method: str
    weight: float  # 0-1, importance weight
    mandatory: bool

@dataclass
class AssessmentResult:
    """Assessment result data structure"""
    criteria_id: str
    score: float  # 0-1
    evidence_provided: str
    assessor_notes: str
    compliance_status: str  # "compliant", "non_compliant", "partially_compliant"
    recommendations: List[str]

@dataclass
class ConformityAssessment:
    """Conformity assessment data structure"""
    id: str
    assessment_type: AssessmentType
    assessment_date: str
    assessor: str
    status: AssessmentStatus
    overall_score: Optional[float]
    compliance_level: Optional[ComplianceLevel]
    criteria_results: List[AssessmentResult]
    findings: List[str]
    recommendations: List[str]
    certification_ready: bool
    next_assessment_date: Optional[str]

class ConformityAssessmentSystem:
    """Comprehensive conformity assessment system"""
    
    def __init__(self):
        self.assessments: List[ConformityAssessment] = []
        self.assessment_criteria: List[AssessmentCriteria] = []
        self.assessment_log_file = "data/conformity_assessment.json"
        self._load_existing_data()
        self._initialize_assessment_criteria()
    
    def _load_existing_data(self):
        """Load existing assessment data from file"""
        try:
            with open(self.assessment_log_file, 'r') as f:
                data = json.load(f)
                self.assessments = [self._deserialize_assessment(assessment_data) 
                                  for assessment_data in data.get('assessments', [])]
                self.assessment_criteria = [self._deserialize_criteria(criteria_data) 
                                          for criteria_data in data.get('criteria', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading assessment data: {e}")
    
    def _save_data(self):
        """Save assessment data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.assessment_log_file), exist_ok=True)
            
            data = {
                'assessments': [self._serialize_assessment(assessment) for assessment in self.assessments],
                'criteria': [self._serialize_criteria(criteria) for criteria in self.assessment_criteria],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.assessment_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving assessment data: {e}")
    
    def _serialize_assessment(self, assessment: ConformityAssessment) -> Dict[str, Any]:
        """Serialize assessment for JSON storage"""
        assessment_dict = asdict(assessment)
        assessment_dict['assessment_type'] = assessment.assessment_type.value
        assessment_dict['status'] = assessment.status.value
        if assessment.compliance_level:
            assessment_dict['compliance_level'] = assessment.compliance_level.value
        return assessment_dict
    
    def _deserialize_assessment(self, assessment_data: Dict[str, Any]) -> ConformityAssessment:
        """Deserialize assessment from JSON"""
        assessment_data['assessment_type'] = AssessmentType(assessment_data['assessment_type'])
        assessment_data['status'] = AssessmentStatus(assessment_data['status'])
        if assessment_data.get('compliance_level'):
            assessment_data['compliance_level'] = ComplianceLevel(assessment_data['compliance_level'])
        return ConformityAssessment(**assessment_data)
    
    def _serialize_criteria(self, criteria: AssessmentCriteria) -> Dict[str, Any]:
        """Serialize criteria for JSON storage"""
        return asdict(criteria)
    
    def _deserialize_criteria(self, criteria_data: Dict[str, Any]) -> AssessmentCriteria:
        """Deserialize criteria from JSON"""
        return AssessmentCriteria(**criteria_data)
    
    def _initialize_assessment_criteria(self):
        """Initialize AI Act assessment criteria"""
        if not self.assessment_criteria:  # Only initialize if no existing criteria
            criteria = [
                # Article 9: Risk Management System
                AssessmentCriteria(
                    id="ART9-001",
                    article="Article 9",
                    requirement="Risk Management System",
                    description="Establishment and maintenance of a risk management system",
                    evidence_required="Risk management procedures, risk register, mitigation plans",
                    assessment_method="Document review, system testing, risk assessment validation",
                    weight=1.0,
                    mandatory=True
                ),
                
                # Article 10: Data Governance and Quality Management
                AssessmentCriteria(
                    id="ART10-001",
                    article="Article 10",
                    requirement="Data Governance and Quality Management",
                    description="Data governance and quality management procedures",
                    evidence_required="Data quality procedures, processing records, quality assessments",
                    assessment_method="Data quality review, governance documentation analysis",
                    weight=1.0,
                    mandatory=True
                ),
                
                # Article 11: Technical Documentation
                AssessmentCriteria(
                    id="ART11-001",
                    article="Article 11",
                    requirement="Technical Documentation",
                    description="Technical documentation of the AI system",
                    evidence_required="System architecture, algorithm documentation, training data info",
                    assessment_method="Documentation review, technical validation",
                    weight=1.0,
                    mandatory=True
                ),
                
                # Article 12: Record Keeping
                AssessmentCriteria(
                    id="ART12-001",
                    article="Article 12",
                    requirement="Record Keeping",
                    description="Record keeping of the AI system",
                    evidence_required="System operation logs, audit trails, decision records",
                    assessment_method="Log analysis, record validation, audit trail review",
                    weight=1.0,
                    mandatory=True
                ),
                
                # Article 13: Transparency and Provision of Information
                AssessmentCriteria(
                    id="ART13-001",
                    article="Article 13",
                    requirement="Transparency and Provision of Information",
                    description="Transparency and provision of information to users",
                    evidence_required="User notices, transparency documentation, user interface",
                    assessment_method="User interface review, transparency notice validation",
                    weight=1.0,
                    mandatory=True
                ),
                
                # Article 14: Human Oversight
                AssessmentCriteria(
                    id="ART14-001",
                    article="Article 14",
                    requirement="Human Oversight",
                    description="Human oversight of the AI system",
                    evidence_required="Oversight procedures, human review mechanisms, override capabilities",
                    assessment_method="Oversight mechanism testing, procedure validation",
                    weight=1.0,
                    mandatory=True
                ),
                
                # Article 15: Accuracy, Robustness and Cybersecurity
                AssessmentCriteria(
                    id="ART15-001",
                    article="Article 15",
                    requirement="Accuracy, Robustness and Cybersecurity",
                    description="Accuracy, robustness and cybersecurity measures",
                    evidence_required="Performance testing, security measures, robustness validation",
                    assessment_method="Performance testing, security assessment, robustness validation",
                    weight=1.0,
                    mandatory=True
                )
            ]
            
            self.assessment_criteria.extend(criteria)
            self._save_data()
    
    def create_assessment(self, assessment_type: AssessmentType, assessor: str) -> str:
        """Create a new conformity assessment"""
        assessment_id = str(uuid.uuid4())
        
        # Create assessment results for all criteria
        criteria_results = []
        for criteria in self.assessment_criteria:
            result = AssessmentResult(
                criteria_id=criteria.id,
                score=0.0,
                evidence_provided="",
                assessor_notes="",
                compliance_status="pending",
                recommendations=[]
            )
            criteria_results.append(result)
        
        assessment = ConformityAssessment(
            id=assessment_id,
            assessment_type=assessment_type,
            assessment_date=datetime.datetime.now().isoformat(),
            assessor=assessor,
            status=AssessmentStatus.PLANNED,
            overall_score=None,
            compliance_level=None,
            criteria_results=criteria_results,
            findings=[],
            recommendations=[],
            certification_ready=False,
            next_assessment_date=None
        )
        
        self.assessments.append(assessment)
        self._save_data()
        
        return assessment_id
    
    def start_assessment(self, assessment_id: str) -> bool:
        """Start an assessment"""
        for assessment in self.assessments:
            if assessment.id == assessment_id and assessment.status == AssessmentStatus.PLANNED:
                assessment.status = AssessmentStatus.IN_PROGRESS
                self._save_data()
                return True
        return False
    
    def update_criteria_result(self, assessment_id: str, criteria_id: str, 
                              score: float, evidence_provided: str, 
                              assessor_notes: str, recommendations: List[str]) -> bool:
        """Update assessment result for specific criteria"""
        for assessment in self.assessments:
            if assessment.id == assessment_id:
                for result in assessment.criteria_results:
                    if result.criteria_id == criteria_id:
                        result.score = score
                        result.evidence_provided = evidence_provided
                        result.assessor_notes = assessor_notes
                        result.recommendations = recommendations
                        
                        # Determine compliance status based on score
                        if score >= 0.9:
                            result.compliance_status = "compliant"
                        elif score >= 0.7:
                            result.compliance_status = "partially_compliant"
                        else:
                            result.compliance_status = "non_compliant"
                        
                        self._save_data()
                        return True
        return False
    
    def complete_assessment(self, assessment_id: str, findings: List[str], 
                           recommendations: List[str]) -> bool:
        """Complete an assessment"""
        for assessment in self.assessments:
            if assessment.id == assessment_id and assessment.status == AssessmentStatus.IN_PROGRESS:
                # Calculate overall score
                total_weighted_score = 0.0
                total_weight = 0.0
                
                for result in assessment.criteria_results:
                    criteria = next((c for c in self.assessment_criteria if c.id == result.criteria_id), None)
                    if criteria:
                        total_weighted_score += result.score * criteria.weight
                        total_weight += criteria.weight
                
                assessment.overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
                
                # Determine compliance level
                if assessment.overall_score >= 0.9:
                    assessment.compliance_level = ComplianceLevel.FULLY_COMPLIANT
                elif assessment.overall_score >= 0.8:
                    assessment.compliance_level = ComplianceLevel.SUBSTANTIALLY_COMPLIANT
                elif assessment.overall_score >= 0.6:
                    assessment.compliance_level = ComplianceLevel.PARTIALLY_COMPLIANT
                else:
                    assessment.compliance_level = ComplianceLevel.NON_COMPLIANT
                
                # Determine certification readiness
                assessment.certification_ready = (
                    assessment.compliance_level in [ComplianceLevel.FULLY_COMPLIANT, 
                                                   ComplianceLevel.SUBSTANTIALLY_COMPLIANT] and
                    all(result.compliance_status in ["compliant", "partially_compliant"] 
                        for result in assessment.criteria_results)
                )
                
                assessment.findings = findings
                assessment.recommendations = recommendations
                assessment.status = AssessmentStatus.COMPLETED
                assessment.next_assessment_date = (datetime.datetime.now() + datetime.timedelta(days=365)).isoformat()
                
                self._save_data()
                return True
        return False
    
    def get_assessment_by_id(self, assessment_id: str) -> Optional[ConformityAssessment]:
        """Get assessment by ID"""
        for assessment in self.assessments:
            if assessment.id == assessment_id:
                return assessment
        return None
    
    def get_latest_assessment(self) -> Optional[ConformityAssessment]:
        """Get the latest assessment"""
        if not self.assessments:
            return None
        return max(self.assessments, key=lambda x: x.assessment_date)
    
    def get_assessment_summary(self) -> Dict[str, Any]:
        """Get assessment summary"""
        total_assessments = len(self.assessments)
        completed_assessments = len([a for a in self.assessments if a.status == AssessmentStatus.COMPLETED])
        
        # Count by compliance level
        compliance_levels = {}
        for assessment in self.assessments:
            if assessment.compliance_level:
                level = assessment.compliance_level.value
                compliance_levels[level] = compliance_levels.get(level, 0) + 1
        
        # Count by type
        assessment_types = {}
        for assessment in self.assessments:
            assessment_type = assessment.assessment_type.value
            assessment_types[assessment_type] = assessment_types.get(assessment_type, 0) + 1
        
        # Get latest assessment
        latest_assessment = self.get_latest_assessment()
        
        return {
            "total_assessments": total_assessments,
            "completed_assessments": completed_assessments,
            "compliance_levels": compliance_levels,
            "assessment_types": assessment_types,
            "latest_assessment": {
                "id": latest_assessment.id,
                "type": latest_assessment.assessment_type.value,
                "date": latest_assessment.assessment_date,
                "score": latest_assessment.overall_score,
                "compliance_level": latest_assessment.compliance_level.value if latest_assessment.compliance_level else None,
                "certification_ready": latest_assessment.certification_ready
            } if latest_assessment else None
        }
    
    def get_certification_readiness(self) -> Dict[str, Any]:
        """Get certification readiness status"""
        latest_assessment = self.get_latest_assessment()
        
        if not latest_assessment or latest_assessment.status != AssessmentStatus.COMPLETED:
            return {
                "status": "no_completed_assessment",
                "message": "No completed assessment available for certification readiness evaluation"
            }
        
        # Check mandatory criteria compliance
        mandatory_criteria = [c for c in self.assessment_criteria if c.mandatory]
        mandatory_results = []
        
        for criteria in mandatory_criteria:
            result = next((r for r in latest_assessment.criteria_results if r.criteria_id == criteria.id), None)
            if result:
                mandatory_results.append({
                    "criteria_id": criteria.id,
                    "article": criteria.article,
                    "requirement": criteria.requirement,
                    "score": result.score,
                    "compliance_status": result.compliance_status
                })
        
        # Calculate certification readiness
        all_mandatory_compliant = all(
            result["compliance_status"] in ["compliant", "partially_compliant"] 
            for result in mandatory_results
        )
        
        return {
            "overall_readiness": latest_assessment.certification_ready,
            "compliance_level": latest_assessment.compliance_level.value if latest_assessment.compliance_level else None,
            "overall_score": latest_assessment.overall_score,
            "mandatory_criteria_compliance": all_mandatory_compliant,
            "mandatory_criteria_details": mandatory_results,
            "recommendations": latest_assessment.recommendations,
            "next_assessment_date": latest_assessment.next_assessment_date
        }
    
    def generate_certification_report(self, assessment_id: str) -> Dict[str, Any]:
        """Generate certification report"""
        assessment = self.get_assessment_by_id(assessment_id)
        if not assessment:
            return {"error": "Assessment not found"}
        
        # Get criteria details
        criteria_details = []
        for result in assessment.criteria_results:
            criteria = next((c for c in self.assessment_criteria if c.id == result.criteria_id), None)
            if criteria:
                criteria_details.append({
                    "criteria": criteria,
                    "result": result
                })
        
        return {
            "assessment_info": {
                "id": assessment.id,
                "type": assessment.assessment_type.value,
                "date": assessment.assessment_date,
                "assessor": assessment.assessor,
                "status": assessment.status.value,
                "overall_score": assessment.overall_score,
                "compliance_level": assessment.compliance_level.value if assessment.compliance_level else None,
                "certification_ready": assessment.certification_ready
            },
            "criteria_results": criteria_details,
            "findings": assessment.findings,
            "recommendations": assessment.recommendations,
            "next_assessment_date": assessment.next_assessment_date
        }

# Global conformity assessment system instance
conformity_assessor = ConformityAssessmentSystem()
