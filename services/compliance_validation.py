"""
Compliance Validation System for AI Act Compliance

This module implements comprehensive compliance validation procedures
for final verification of AI Act compliance before certification.
"""

import json
import datetime
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class ValidationType(Enum):
    """Types of compliance validations"""
    AUTOMATED_VALIDATION = "automated_validation"
    MANUAL_VALIDATION = "manual_validation"
    THIRD_PARTY_VALIDATION = "third_party_validation"
    REGULATORY_VALIDATION = "regulatory_validation"

class ValidationStatus(Enum):
    """Validation status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    REQUIRES_ATTENTION = "requires_attention"

class ValidationSeverity(Enum):
    """Validation severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class ValidationRule:
    """Validation rule data structure"""
    id: str
    name: str
    description: str
    article: str
    requirement: str
    validation_type: ValidationType
    automated: bool
    severity: ValidationSeverity
    weight: float  # 0-1, importance weight

@dataclass
class ValidationResult:
    """Validation result data structure"""
    rule_id: str
    status: ValidationStatus
    score: float  # 0-1
    message: str
    evidence: str
    recommendations: List[str]
    validated_at: str
    validator: str

@dataclass
class ComplianceValidation:
    """Compliance validation data structure"""
    id: str
    validation_type: ValidationType
    validation_date: str
    validator: str
    status: ValidationStatus
    overall_score: Optional[float]
    validation_results: List[ValidationResult]
    findings: List[str]
    recommendations: List[str]
    certification_ready: bool
    next_validation_date: Optional[str]

class ComplianceValidationSystem:
    """Comprehensive compliance validation system"""
    
    def __init__(self):
        self.validations: List[ComplianceValidation] = []
        self.validation_rules: List[ValidationRule] = []
        self.validation_log_file = "data/compliance_validation.json"
        self._load_existing_data()
        self._initialize_validation_rules()
    
    def _load_existing_data(self):
        """Load existing validation data from file"""
        try:
            with open(self.validation_log_file, 'r') as f:
                data = json.load(f)
                self.validations = [self._deserialize_validation(validation_data) 
                                  for validation_data in data.get('validations', [])]
                self.validation_rules = [self._deserialize_rule(rule_data) 
                                       for rule_data in data.get('rules', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading validation data: {e}")
    
    def _save_data(self):
        """Save validation data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.validation_log_file), exist_ok=True)
            
            data = {
                'validations': [self._serialize_validation(validation) for validation in self.validations],
                'rules': [self._serialize_rule(rule) for rule in self.validation_rules],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.validation_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving validation data: {e}")
    
    def _serialize_validation(self, validation: ComplianceValidation) -> Dict[str, Any]:
        """Serialize validation for JSON storage"""
        validation_dict = asdict(validation)
        validation_dict['validation_type'] = validation.validation_type.value
        validation_dict['status'] = validation.status.value
        return validation_dict
    
    def _deserialize_validation(self, validation_data: Dict[str, Any]) -> ComplianceValidation:
        """Deserialize validation from JSON"""
        validation_data['validation_type'] = ValidationType(validation_data['validation_type'])
        validation_data['status'] = ValidationStatus(validation_data['status'])
        return ComplianceValidation(**validation_data)
    
    def _serialize_rule(self, rule: ValidationRule) -> Dict[str, Any]:
        """Serialize rule for JSON storage"""
        rule_dict = asdict(rule)
        rule_dict['validation_type'] = rule.validation_type.value
        rule_dict['severity'] = rule.severity.value
        return rule_dict
    
    def _deserialize_rule(self, rule_data: Dict[str, Any]) -> ValidationRule:
        """Deserialize rule from JSON"""
        rule_data['validation_type'] = ValidationType(rule_data['validation_type'])
        rule_data['severity'] = ValidationSeverity(rule_data['severity'])
        return ValidationRule(**rule_data)
    
    def _initialize_validation_rules(self):
        """Initialize AI Act validation rules"""
        if not self.validation_rules:  # Only initialize if no existing rules
            rules = [
                # Article 9: Risk Management System
                ValidationRule(
                    id="VAL-ART9-001",
                    name="Risk Management System Exists",
                    description="Verify that a risk management system is implemented and operational",
                    article="Article 9",
                    requirement="Risk Management System",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.CRITICAL,
                    weight=1.0
                ),
                ValidationRule(
                    id="VAL-ART9-002",
                    name="Risk Assessment Procedures",
                    description="Verify that risk assessment procedures are documented and followed",
                    article="Article 9",
                    requirement="Risk Assessment Procedures",
                    validation_type=ValidationType.MANUAL_VALIDATION,
                    automated=False,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                
                # Article 10: Data Governance
                ValidationRule(
                    id="VAL-ART10-001",
                    name="Data Quality Management",
                    description="Verify that data quality management procedures are implemented",
                    article="Article 10",
                    requirement="Data Governance and Quality Management",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                ValidationRule(
                    id="VAL-ART10-002",
                    name="Data Processing Records",
                    description="Verify that data processing activities are properly recorded",
                    article="Article 10",
                    requirement="Data Processing Records",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.MEDIUM,
                    weight=0.7
                ),
                
                # Article 11: Technical Documentation
                ValidationRule(
                    id="VAL-ART11-001",
                    name="Technical Documentation Completeness",
                    description="Verify that technical documentation is complete and up-to-date",
                    article="Article 11",
                    requirement="Technical Documentation",
                    validation_type=ValidationType.MANUAL_VALIDATION,
                    automated=False,
                    severity=ValidationSeverity.CRITICAL,
                    weight=1.0
                ),
                ValidationRule(
                    id="VAL-ART11-002",
                    name="Algorithm Documentation",
                    description="Verify that algorithm documentation is comprehensive",
                    article="Article 11",
                    requirement="Algorithm Documentation",
                    validation_type=ValidationType.MANUAL_VALIDATION,
                    automated=False,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                
                # Article 12: Record Keeping
                ValidationRule(
                    id="VAL-ART12-001",
                    name="System Operation Logs",
                    description="Verify that system operation logs are maintained",
                    article="Article 12",
                    requirement="Record Keeping",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                ValidationRule(
                    id="VAL-ART12-002",
                    name="Audit Trail Integrity",
                    description="Verify that audit trails are complete and tamper-proof",
                    article="Article 12",
                    requirement="Audit Trail Integrity",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.MEDIUM,
                    weight=0.7
                ),
                
                # Article 13: Transparency
                ValidationRule(
                    id="VAL-ART13-001",
                    name="AI Transparency Notices",
                    description="Verify that AI transparency notices are displayed to users",
                    article="Article 13",
                    requirement="Transparency and Provision of Information",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.CRITICAL,
                    weight=1.0
                ),
                ValidationRule(
                    id="VAL-ART13-002",
                    name="User Information Provision",
                    description="Verify that users are provided with adequate information about AI system",
                    article="Article 13",
                    requirement="User Information Provision",
                    validation_type=ValidationType.MANUAL_VALIDATION,
                    automated=False,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                
                # Article 14: Human Oversight
                ValidationRule(
                    id="VAL-ART14-001",
                    name="Human Oversight Mechanisms",
                    description="Verify that human oversight mechanisms are implemented",
                    article="Article 14",
                    requirement="Human Oversight",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.CRITICAL,
                    weight=1.0
                ),
                ValidationRule(
                    id="VAL-ART14-002",
                    name="Override Capabilities",
                    description="Verify that human override capabilities are functional",
                    article="Article 14",
                    requirement="Override Capabilities",
                    validation_type=ValidationType.MANUAL_VALIDATION,
                    automated=False,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                
                # Article 15: Accuracy, Robustness and Cybersecurity
                ValidationRule(
                    id="VAL-ART15-001",
                    name="System Accuracy",
                    description="Verify that system accuracy meets requirements",
                    article="Article 15",
                    requirement="Accuracy, Robustness and Cybersecurity",
                    validation_type=ValidationType.AUTOMATED_VALIDATION,
                    automated=True,
                    severity=ValidationSeverity.HIGH,
                    weight=0.9
                ),
                ValidationRule(
                    id="VAL-ART15-002",
                    name="Cybersecurity Measures",
                    description="Verify that cybersecurity measures are implemented",
                    article="Article 15",
                    requirement="Cybersecurity Measures",
                    validation_type=ValidationType.MANUAL_VALIDATION,
                    automated=False,
                    severity=ValidationSeverity.CRITICAL,
                    weight=1.0
                )
            ]
            
            self.validation_rules.extend(rules)
            self._save_data()
    
    def create_validation(self, validation_type: ValidationType, validator: str) -> str:
        """Create a new compliance validation"""
        validation_id = str(uuid.uuid4())
        
        # Create validation results for all rules
        validation_results = []
        for rule in self.validation_rules:
            result = ValidationResult(
                rule_id=rule.id,
                status=ValidationStatus.PENDING,
                score=0.0,
                message="",
                evidence="",
                recommendations=[],
                validated_at="",
                validator=""
            )
            validation_results.append(result)
        
        validation = ComplianceValidation(
            id=validation_id,
            validation_type=validation_type,
            validation_date=datetime.datetime.now().isoformat(),
            validator=validator,
            status=ValidationStatus.PENDING,
            overall_score=None,
            validation_results=validation_results,
            findings=[],
            recommendations=[],
            certification_ready=False,
            next_validation_date=None
        )
        
        self.validations.append(validation)
        self._save_data()
        
        return validation_id
    
    def start_validation(self, validation_id: str) -> bool:
        """Start a validation"""
        for validation in self.validations:
            if validation.id == validation_id and validation.status == ValidationStatus.PENDING:
                validation.status = ValidationStatus.IN_PROGRESS
                self._save_data()
                return True
        return False
    
    def run_automated_validation(self, validation_id: str) -> bool:
        """Run automated validation rules"""
        validation = next((v for v in self.validations if v.id == validation_id), None)
        if not validation:
            return False
        
        # Run automated validation rules
        for result in validation.validation_results:
            rule = next((r for r in self.validation_rules if r.id == result.rule_id), None)
            if rule and rule.automated:
                # Simulate automated validation
                validation_result = self._simulate_automated_validation(rule)
                result.status = validation_result["status"]
                result.score = validation_result["score"]
                result.message = validation_result["message"]
                result.evidence = validation_result["evidence"]
                result.recommendations = validation_result["recommendations"]
                result.validated_at = datetime.datetime.now().isoformat()
                result.validator = "automated_system"
        
        self._save_data()
        return True
    
    def _simulate_automated_validation(self, rule: ValidationRule) -> Dict[str, Any]:
        """Simulate automated validation result"""
        # This would integrate with actual system checks
        # For now, we'll simulate based on rule type
        
        if "risk_management" in rule.name.lower():
            return {
                "status": ValidationStatus.PASSED,
                "score": 0.95,
                "message": "Risk management system is operational and properly configured",
                "evidence": "Risk management system active, 5 risks identified and managed",
                "recommendations": ["Continue regular risk assessments"]
            }
        elif "data_quality" in rule.name.lower():
            return {
                "status": ValidationStatus.PASSED,
                "score": 0.88,
                "message": "Data quality management procedures are implemented",
                "evidence": "Data quality assessments completed, quality score: 88%",
                "recommendations": ["Improve data validation processes"]
            }
        elif "transparency" in rule.name.lower():
            return {
                "status": ValidationStatus.PASSED,
                "score": 1.0,
                "message": "AI transparency notices are properly displayed",
                "evidence": "Transparency notices found in UI, user information provided",
                "recommendations": []
            }
        elif "human_oversight" in rule.name.lower():
            return {
                "status": ValidationStatus.PASSED,
                "score": 0.92,
                "message": "Human oversight mechanisms are functional",
                "evidence": "Oversight dashboard active, flagging system operational",
                "recommendations": ["Enhance oversight training"]
            }
        elif "record_keeping" in rule.name.lower():
            return {
                "status": ValidationStatus.PASSED,
                "score": 0.90,
                "message": "Record keeping system is operational",
                "evidence": "System logs maintained, audit trails complete",
                "recommendations": ["Implement automated log analysis"]
            }
        else:
            return {
                "status": ValidationStatus.PASSED,
                "score": 0.85,
                "message": "Validation completed successfully",
                "evidence": "System meets basic requirements",
                "recommendations": ["Continue monitoring"]
            }
    
    def update_manual_validation(self, validation_id: str, rule_id: str, 
                                status: ValidationStatus, score: float,
                                message: str, evidence: str, 
                                recommendations: List[str], validator: str) -> bool:
        """Update manual validation result"""
        for validation in self.validations:
            if validation.id == validation_id:
                for result in validation.validation_results:
                    if result.rule_id == rule_id:
                        result.status = status
                        result.score = score
                        result.message = message
                        result.evidence = evidence
                        result.recommendations = recommendations
                        result.validated_at = datetime.datetime.now().isoformat()
                        result.validator = validator
                        
                        self._save_data()
                        return True
        return False
    
    def complete_validation(self, validation_id: str, findings: List[str], 
                           recommendations: List[str]) -> bool:
        """Complete a validation"""
        for validation in self.validations:
            if validation.id == validation_id and validation.status == ValidationStatus.IN_PROGRESS:
                # Calculate overall score
                total_weighted_score = 0.0
                total_weight = 0.0
                
                for result in validation.validation_results:
                    rule = next((r for r in self.validation_rules if r.id == result.rule_id), None)
                    if rule and result.status == ValidationStatus.PASSED:
                        total_weighted_score += result.score * rule.weight
                        total_weight += rule.weight
                
                validation.overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
                
                # Determine certification readiness
                critical_rules = [r for r in self.validation_rules if r.severity == ValidationSeverity.CRITICAL]
                critical_results = [result for result in validation.validation_results 
                                  if any(r.id == result.rule_id for r in critical_rules)]
                
                all_critical_passed = all(result.status == ValidationStatus.PASSED for result in critical_results)
                validation.certification_ready = all_critical_passed and validation.overall_score >= 0.8
                
                validation.findings = findings
                validation.recommendations = recommendations
                validation.status = ValidationStatus.PASSED if validation.certification_ready else ValidationStatus.REQUIRES_ATTENTION
                validation.next_validation_date = (datetime.datetime.now() + datetime.timedelta(days=180)).isoformat()
                
                self._save_data()
                return True
        return False
    
    def get_validation_by_id(self, validation_id: str) -> Optional[ComplianceValidation]:
        """Get validation by ID"""
        for validation in self.validations:
            if validation.id == validation_id:
                return validation
        return None
    
    def get_latest_validation(self) -> Optional[ComplianceValidation]:
        """Get the latest validation"""
        if not self.validations:
            return None
        return max(self.validations, key=lambda x: x.validation_date)
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        total_validations = len(self.validations)
        completed_validations = len([v for v in self.validations if v.status == ValidationStatus.PASSED])
        
        # Count by status
        validation_status = {}
        for validation in self.validations:
            status = validation.status.value
            validation_status[status] = validation_status.get(status, 0) + 1
        
        # Get latest validation
        latest_validation = self.get_latest_validation()
        
        return {
            "total_validations": total_validations,
            "completed_validations": completed_validations,
            "validation_status": validation_status,
            "latest_validation": {
                "id": latest_validation.id,
                "type": latest_validation.validation_type.value,
                "date": latest_validation.validation_date,
                "score": latest_validation.overall_score,
                "certification_ready": latest_validation.certification_ready
            } if latest_validation else None
        }
    
    def get_compliance_validation_status(self) -> Dict[str, Any]:
        """Get overall compliance validation status"""
        latest_validation = self.get_latest_validation()
        
        if not latest_validation or latest_validation.status not in [ValidationStatus.PASSED, ValidationStatus.REQUIRES_ATTENTION]:
            return {
                "status": "no_completed_validation",
                "message": "No completed validation available for compliance status evaluation"
            }
        
        # Get validation results by article
        article_results = {}
        for result in latest_validation.validation_results:
            rule = next((r for r in self.validation_rules if r.id == result.rule_id), None)
            if rule:
                article = rule.article
                if article not in article_results:
                    article_results[article] = []
                article_results[article].append({
                    "rule_name": rule.name,
                    "status": result.status.value,
                    "score": result.score,
                    "severity": rule.severity.value
                })
        
        return {
            "overall_status": latest_validation.status.value,
            "overall_score": latest_validation.overall_score,
            "certification_ready": latest_validation.certification_ready,
            "article_results": article_results,
            "findings": latest_validation.findings,
            "recommendations": latest_validation.recommendations,
            "next_validation_date": latest_validation.next_validation_date
        }

# Global compliance validation system instance
compliance_validator = ComplianceValidationSystem()
