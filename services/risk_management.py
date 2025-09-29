"""
Risk Management System for AI Act Compliance (Article 9)

This module implements systematic risk identification, assessment, and mitigation
procedures required under Article 9 of the EU AI Act.
"""

import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskCategory(Enum):
    """Risk categories for AI systems"""
    ACCURACY = "accuracy"
    BIAS = "bias"
    PRIVACY = "privacy"
    SECURITY = "security"
    TRANSPARENCY = "transparency"
    HUMAN_OVERSIGHT = "human_oversight"
    DATA_QUALITY = "data_quality"
    SYSTEM_RELIABILITY = "system_reliability"

@dataclass
class Risk:
    """Risk assessment data structure"""
    id: str
    category: RiskCategory
    level: RiskLevel
    description: str
    impact: str
    likelihood: str
    mitigation_measures: List[str]
    status: str  # "identified", "assessed", "mitigated", "monitored"
    created_date: str
    last_updated: str
    owner: str

@dataclass
class RiskAssessment:
    """Risk assessment result"""
    risk_id: str
    assessment_date: str
    assessor: str
    current_level: RiskLevel
    previous_level: Optional[RiskLevel]
    mitigation_effectiveness: str
    notes: str

class RiskManagementSystem:
    """AI Act compliant risk management system"""
    
    def __init__(self):
        self.risks: Dict[str, Risk] = {}
        self.assessments: List[RiskAssessment] = []
        self.risk_log_file = "data/risk_management_log.json"
        self._load_existing_risks()
        self._initialize_default_risks()
    
    def _load_existing_risks(self):
        """Load existing risk data from file"""
        try:
            with open(self.risk_log_file, 'r') as f:
                data = json.load(f)
                for risk_data in data.get('risks', []):
                    risk = Risk(**risk_data)
                    self.risks[risk.id] = risk
                self.assessments = [RiskAssessment(**assessment) for assessment in data.get('assessments', [])]
        except FileNotFoundError:
            # File doesn't exist yet, will be created on first save
            pass
        except Exception as e:
            print(f"Error loading risk data: {e}")
    
    def _serialize_risk(self, risk: Risk) -> Dict[str, Any]:
        """Serialize risk object for JSON storage"""
        risk_dict = asdict(risk)
        risk_dict['category'] = risk.category.value
        risk_dict['level'] = risk.level.value
        return risk_dict
    
    def _serialize_assessment(self, assessment: RiskAssessment) -> Dict[str, Any]:
        """Serialize assessment object for JSON storage"""
        assessment_dict = asdict(assessment)
        assessment_dict['current_level'] = assessment.current_level.value
        if assessment.previous_level:
            assessment_dict['previous_level'] = assessment.previous_level.value
        return assessment_dict
    
    def _save_risks(self):
        """Save risk data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.risk_log_file), exist_ok=True)
            
            data = {
                'risks': [self._serialize_risk(risk) for risk in self.risks.values()],
                'assessments': [self._serialize_assessment(assessment) for assessment in self.assessments],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.risk_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving risk data: {e}")
    
    def _initialize_default_risks(self):
        """Initialize default risks for AI Resume system"""
        if not self.risks:  # Only initialize if no existing risks
            default_risks = [
                Risk(
                    id="RISK-001",
                    category=RiskCategory.ACCURACY,
                    level=RiskLevel.MEDIUM,
                    description="AI responses may contain inaccuracies about candidate information",
                    impact="Incorrect information could mislead recruiters and affect hiring decisions",
                    likelihood="Medium - AI models may hallucinate or misinterpret data",
                    mitigation_measures=[
                        "Human oversight and response flagging system",
                        "Regular accuracy monitoring and validation",
                        "Clear disclaimers about AI-generated content",
                        "User feedback collection and analysis"
                    ],
                    status="identified",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    owner="Compliance Team"
                ),
                Risk(
                    id="RISK-002",
                    category=RiskCategory.BIAS,
                    level=RiskLevel.MEDIUM,
                    description="AI models may exhibit bias in resume analysis and presentation",
                    impact="Biased responses could lead to unfair hiring practices",
                    likelihood="Medium - AI models trained on potentially biased data",
                    mitigation_measures=[
                        "Diverse training data validation",
                        "Bias detection and monitoring",
                        "Regular model performance audits",
                        "Human review of flagged responses"
                    ],
                    status="identified",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    owner="Compliance Team"
                ),
                Risk(
                    id="RISK-003",
                    category=RiskCategory.PRIVACY,
                    level=RiskLevel.HIGH,
                    description="Personal data processing without proper safeguards",
                    impact="Privacy violations could result in regulatory penalties and user trust loss",
                    likelihood="Low - Data minimization principles applied",
                    mitigation_measures=[
                        "Data minimization and purpose limitation",
                        "Encryption of sensitive data",
                        "Access controls and audit trails",
                        "Privacy impact assessments"
                    ],
                    status="identified",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    owner="Compliance Team"
                ),
                Risk(
                    id="RISK-004",
                    category=RiskCategory.TRANSPARENCY,
                    level=RiskLevel.LOW,
                    description="Users may not understand AI system limitations and capabilities",
                    impact="Misunderstanding could lead to over-reliance on AI responses",
                    likelihood="Low - Transparency notices implemented",
                    mitigation_measures=[
                        "Clear AI transparency notices",
                        "Detailed system information",
                        "User education and guidance",
                        "Regular transparency audits"
                    ],
                    status="mitigated",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    owner="Compliance Team"
                ),
                Risk(
                    id="RISK-005",
                    category=RiskCategory.HUMAN_OVERSIGHT,
                    level=RiskLevel.LOW,
                    description="Insufficient human control over AI system decisions",
                    impact="Lack of human oversight could lead to automated decision-making errors",
                    likelihood="Low - Human oversight mechanisms implemented",
                    mitigation_measures=[
                        "Response flagging and review system",
                        "Human oversight dashboard",
                        "Override mechanisms for AI decisions",
                        "Regular oversight effectiveness monitoring"
                    ],
                    status="mitigated",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    owner="Compliance Team"
                )
            ]
            
            for risk in default_risks:
                self.risks[risk.id] = risk
            
            self._save_risks()
    
    def identify_risk(self, category: RiskCategory, description: str, 
                     impact: str, likelihood: str, mitigation_measures: List[str],
                     owner: str = "Compliance Team") -> str:
        """Identify a new risk"""
        risk_id = f"RISK-{len(self.risks) + 1:03d}"
        
        # Determine risk level based on impact and likelihood
        level = self._calculate_risk_level(impact, likelihood)
        
        risk = Risk(
            id=risk_id,
            category=category,
            level=level,
            description=description,
            impact=impact,
            likelihood=likelihood,
            mitigation_measures=mitigation_measures,
            status="identified",
            created_date=datetime.datetime.now().isoformat(),
            last_updated=datetime.datetime.now().isoformat(),
            owner=owner
        )
        
        self.risks[risk_id] = risk
        self._save_risks()
        
        return risk_id
    
    def _calculate_risk_level(self, impact: str, likelihood: str) -> RiskLevel:
        """Calculate risk level based on impact and likelihood"""
        impact_score = 0
        likelihood_score = 0
        
        # Impact scoring
        if "critical" in impact.lower() or "severe" in impact.lower():
            impact_score = 4
        elif "high" in impact.lower() or "significant" in impact.lower():
            impact_score = 3
        elif "medium" in impact.lower() or "moderate" in impact.lower():
            impact_score = 2
        else:
            impact_score = 1
        
        # Likelihood scoring
        if "high" in likelihood.lower() or "frequent" in likelihood.lower():
            likelihood_score = 4
        elif "medium" in likelihood.lower() or "occasional" in likelihood.lower():
            likelihood_score = 3
        elif "low" in likelihood.lower() or "rare" in likelihood.lower():
            likelihood_score = 2
        else:
            likelihood_score = 1
        
        # Risk level calculation
        total_score = impact_score + likelihood_score
        
        if total_score >= 7:
            return RiskLevel.CRITICAL
        elif total_score >= 5:
            return RiskLevel.HIGH
        elif total_score >= 3:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def assess_risk(self, risk_id: str, assessor: str, 
                   current_level: RiskLevel, mitigation_effectiveness: str,
                   notes: str = "") -> None:
        """Conduct risk assessment"""
        if risk_id not in self.risks:
            raise ValueError(f"Risk {risk_id} not found")
        
        risk = self.risks[risk_id]
        previous_level = risk.level
        
        # Update risk level
        risk.level = current_level
        risk.last_updated = datetime.datetime.now().isoformat()
        
        # Create assessment record
        assessment = RiskAssessment(
            risk_id=risk_id,
            assessment_date=datetime.datetime.now().isoformat(),
            assessor=assessor,
            current_level=current_level,
            previous_level=previous_level,
            mitigation_effectiveness=mitigation_effectiveness,
            notes=notes
        )
        
        self.assessments.append(assessment)
        self._save_risks()
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get risk management summary for compliance reporting"""
        total_risks = len(self.risks)
        risks_by_level = {}
        risks_by_category = {}
        risks_by_status = {}
        
        for risk in self.risks.values():
            # Count by level
            level = risk.level.value
            risks_by_level[level] = risks_by_level.get(level, 0) + 1
            
            # Count by category
            category = risk.category.value
            risks_by_category[category] = risks_by_category.get(category, 0) + 1
            
            # Count by status
            status = risk.status
            risks_by_status[status] = risks_by_status.get(status, 0) + 1
        
        return {
            "total_risks": total_risks,
            "risks_by_level": risks_by_level,
            "risks_by_category": risks_by_category,
            "risks_by_status": risks_by_status,
            "last_assessment": self.assessments[-1].assessment_date if self.assessments else None,
            "total_assessments": len(self.assessments)
        }
    
    def get_high_priority_risks(self) -> List[Risk]:
        """Get high and critical priority risks"""
        high_priority = []
        for risk in self.risks.values():
            if risk.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                high_priority.append(risk)
        return sorted(high_priority, key=lambda x: x.level.value, reverse=True)
    
    def get_risk_by_id(self, risk_id: str) -> Optional[Risk]:
        """Get specific risk by ID"""
        return self.risks.get(risk_id)
    
    def update_risk_status(self, risk_id: str, new_status: str) -> None:
        """Update risk status"""
        if risk_id not in self.risks:
            raise ValueError(f"Risk {risk_id} not found")
        
        self.risks[risk_id].status = new_status
        self.risks[risk_id].last_updated = datetime.datetime.now().isoformat()
        self._save_risks()

# Global risk management system instance
risk_manager = RiskManagementSystem()
