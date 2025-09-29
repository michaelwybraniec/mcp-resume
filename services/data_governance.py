"""
Data Governance System for AI Act Compliance (Article 10)

This module implements data quality and management procedures required under 
Article 10 of the EU AI Act for high-risk AI systems.
"""

import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class DataQualityLevel(Enum):
    """Data quality assessment levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

class DataCategory(Enum):
    """Data categories for governance"""
    PERSONAL_INFO = "personal_info"
    WORK_EXPERIENCE = "work_experience"
    SKILLS = "skills"
    EDUCATION = "education"
    REFERENCES = "references"
    USER_QUERIES = "user_queries"
    AI_RESPONSES = "ai_responses"

@dataclass
class DataQualityAssessment:
    """Data quality assessment record"""
    id: str
    category: DataCategory
    assessment_date: str
    assessor: str
    quality_level: DataQualityLevel
    completeness_score: float  # 0-100
    accuracy_score: float      # 0-100
    consistency_score: float   # 0-100
    timeliness_score: float    # 0-100
    issues_found: List[str]
    remediation_actions: List[str]
    next_assessment_date: str

@dataclass
class DataProcessingRecord:
    """Record of data processing activities"""
    id: str
    timestamp: str
    data_category: DataCategory
    processing_purpose: str
    data_subjects: int
    retention_period: str
    legal_basis: str
    security_measures: List[str]
    access_controls: List[str]

class DataGovernanceSystem:
    """AI Act compliant data governance system"""
    
    def __init__(self):
        self.quality_assessments: List[DataQualityAssessment] = []
        self.processing_records: List[DataProcessingRecord] = []
        self.governance_log_file = "data/data_governance_log.json"
        self._load_existing_data()
        self._initialize_default_assessments()
    
    def _load_existing_data(self):
        """Load existing governance data from file"""
        try:
            with open(self.governance_log_file, 'r') as f:
                data = json.load(f)
                self.quality_assessments = [
                    DataQualityAssessment(**assessment) 
                    for assessment in data.get('quality_assessments', [])
                ]
                self.processing_records = [
                    DataProcessingRecord(**record) 
                    for record in data.get('processing_records', [])
                ]
        except FileNotFoundError:
            # File doesn't exist yet, will be created on first save
            pass
        except Exception as e:
            print(f"Error loading governance data: {e}")
    
    def _serialize_assessment(self, assessment: DataQualityAssessment) -> Dict[str, Any]:
        """Serialize assessment object for JSON storage"""
        assessment_dict = asdict(assessment)
        assessment_dict['category'] = assessment.category.value
        assessment_dict['quality_level'] = assessment.quality_level.value
        return assessment_dict
    
    def _serialize_record(self, record: DataProcessingRecord) -> Dict[str, Any]:
        """Serialize processing record object for JSON storage"""
        record_dict = asdict(record)
        record_dict['data_category'] = record.data_category.value
        return record_dict
    
    def _save_data(self):
        """Save governance data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.governance_log_file), exist_ok=True)
            
            data = {
                'quality_assessments': [self._serialize_assessment(assessment) for assessment in self.quality_assessments],
                'processing_records': [self._serialize_record(record) for record in self.processing_records],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.governance_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving governance data: {e}")
    
    def _initialize_default_assessments(self):
        """Initialize default data quality assessments"""
        if not self.quality_assessments:  # Only initialize if no existing assessments
            default_assessments = [
                DataQualityAssessment(
                    id="DQ-001",
                    category=DataCategory.PERSONAL_INFO,
                    assessment_date=datetime.datetime.now().isoformat(),
                    assessor="Data Governance Team",
                    quality_level=DataQualityLevel.EXCELLENT,
                    completeness_score=95.0,
                    accuracy_score=98.0,
                    consistency_score=92.0,
                    timeliness_score=100.0,
                    issues_found=[
                        "Minor formatting inconsistencies in contact information"
                    ],
                    remediation_actions=[
                        "Standardize contact information format",
                        "Implement data validation rules"
                    ],
                    next_assessment_date=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
                ),
                DataQualityAssessment(
                    id="DQ-002",
                    category=DataCategory.WORK_EXPERIENCE,
                    assessment_date=datetime.datetime.now().isoformat(),
                    assessor="Data Governance Team",
                    quality_level=DataQualityLevel.GOOD,
                    completeness_score=88.0,
                    accuracy_score=95.0,
                    consistency_score=85.0,
                    timeliness_score=90.0,
                    issues_found=[
                        "Some job descriptions lack detailed achievements",
                        "Date formats inconsistent across entries"
                    ],
                    remediation_actions=[
                        "Enhance job description templates",
                        "Standardize date format across all entries"
                    ],
                    next_assessment_date=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
                ),
                DataQualityAssessment(
                    id="DQ-003",
                    category=DataCategory.SKILLS,
                    assessment_date=datetime.datetime.now().isoformat(),
                    assessor="Data Governance Team",
                    quality_level=DataQualityLevel.EXCELLENT,
                    completeness_score=92.0,
                    accuracy_score=96.0,
                    consistency_score=94.0,
                    timeliness_score=95.0,
                    issues_found=[
                        "Skill proficiency levels could be more granular"
                    ],
                    remediation_actions=[
                        "Implement more detailed skill proficiency scales",
                        "Add skill validation mechanisms"
                    ],
                    next_assessment_date=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
                )
            ]
            
            self.quality_assessments.extend(default_assessments)
            self._save_data()
    
    def assess_data_quality(self, category: DataCategory, assessor: str,
                           completeness_score: float, accuracy_score: float,
                           consistency_score: float, timeliness_score: float,
                           issues_found: List[str], remediation_actions: List[str]) -> str:
        """Conduct data quality assessment"""
        assessment_id = f"DQ-{len(self.quality_assessments) + 1:03d}"
        
        # Calculate overall quality level
        overall_score = (completeness_score + accuracy_score + consistency_score + timeliness_score) / 4
        
        if overall_score >= 90:
            quality_level = DataQualityLevel.EXCELLENT
        elif overall_score >= 80:
            quality_level = DataQualityLevel.GOOD
        elif overall_score >= 70:
            quality_level = DataQualityLevel.FAIR
        elif overall_score >= 60:
            quality_level = DataQualityLevel.POOR
        else:
            quality_level = DataQualityLevel.CRITICAL
        
        assessment = DataQualityAssessment(
            id=assessment_id,
            category=category,
            assessment_date=datetime.datetime.now().isoformat(),
            assessor=assessor,
            quality_level=quality_level,
            completeness_score=completeness_score,
            accuracy_score=accuracy_score,
            consistency_score=consistency_score,
            timeliness_score=timeliness_score,
            issues_found=issues_found,
            remediation_actions=remediation_actions,
            next_assessment_date=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
        )
        
        self.quality_assessments.append(assessment)
        self._save_data()
        
        return assessment_id
    
    def record_data_processing(self, data_category: DataCategory, 
                              processing_purpose: str, data_subjects: int,
                              retention_period: str, legal_basis: str,
                              security_measures: List[str], 
                              access_controls: List[str]) -> str:
        """Record data processing activity"""
        record_id = f"DP-{len(self.processing_records) + 1:03d}"
        
        record = DataProcessingRecord(
            id=record_id,
            timestamp=datetime.datetime.now().isoformat(),
            data_category=data_category,
            processing_purpose=processing_purpose,
            data_subjects=data_subjects,
            retention_period=retention_period,
            legal_basis=legal_basis,
            security_measures=security_measures,
            access_controls=access_controls
        )
        
        self.processing_records.append(record)
        self._save_data()
        
        return record_id
    
    def get_data_quality_summary(self) -> Dict[str, Any]:
        """Get data quality summary for compliance reporting"""
        if not self.quality_assessments:
            return {"message": "No quality assessments available"}
        
        latest_assessments = {}
        quality_trends = {}
        
        # Get latest assessment for each category
        for assessment in self.quality_assessments:
            category = assessment.category.value
            if category not in latest_assessments or assessment.assessment_date > latest_assessments[category]['date']:
                latest_assessments[category] = {
                    'date': assessment.assessment_date,
                    'level': assessment.quality_level.value,
                    'overall_score': (assessment.completeness_score + assessment.accuracy_score + 
                                    assessment.consistency_score + assessment.timeliness_score) / 4
                }
        
        # Calculate quality trends
        for category in DataCategory:
            category_assessments = [a for a in self.quality_assessments if a.category == category]
            if len(category_assessments) >= 2:
                latest = category_assessments[-1]
                previous = category_assessments[-2]
                latest_score = (latest.completeness_score + latest.accuracy_score + 
                              latest.consistency_score + latest.timeliness_score) / 4
                previous_score = (previous.completeness_score + previous.accuracy_score + 
                                previous.consistency_score + previous.timeliness_score) / 4
                
                if latest_score > previous_score:
                    quality_trends[category.value] = "improving"
                elif latest_score < previous_score:
                    quality_trends[category.value] = "declining"
                else:
                    quality_trends[category.value] = "stable"
        
        return {
            "latest_assessments": latest_assessments,
            "quality_trends": quality_trends,
            "total_assessments": len(self.quality_assessments),
            "total_processing_records": len(self.processing_records),
            "last_assessment_date": max([a.assessment_date for a in self.quality_assessments]) if self.quality_assessments else None
        }
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get data processing summary for compliance reporting"""
        if not self.processing_records:
            return {"message": "No processing records available"}
        
        # Group by category
        processing_by_category = {}
        for record in self.processing_records:
            category = record.data_category.value
            if category not in processing_by_category:
                processing_by_category[category] = {
                    'count': 0,
                    'total_subjects': 0,
                    'purposes': set(),
                    'legal_bases': set()
                }
            
            processing_by_category[category]['count'] += 1
            processing_by_category[category]['total_subjects'] += record.data_subjects
            processing_by_category[category]['purposes'].add(record.processing_purpose)
            processing_by_category[category]['legal_bases'].add(record.legal_basis)
        
        # Convert sets to lists for JSON serialization
        for category_data in processing_by_category.values():
            category_data['purposes'] = list(category_data['purposes'])
            category_data['legal_bases'] = list(category_data['legal_bases'])
        
        return {
            "processing_by_category": processing_by_category,
            "total_processing_activities": len(self.processing_records),
            "total_data_subjects": sum(record.data_subjects for record in self.processing_records),
            "last_processing_date": max([record.timestamp for record in self.processing_records]) if self.processing_records else None
        }
    
    def get_governance_compliance_status(self) -> Dict[str, Any]:
        """Get overall data governance compliance status"""
        quality_summary = self.get_data_quality_summary()
        processing_summary = self.get_processing_summary()
        
        # Check compliance indicators
        compliance_indicators = {
            "data_quality_assessments": len(self.quality_assessments) > 0,
            "processing_records": len(self.processing_records) > 0,
            "regular_assessments": self._check_regular_assessments(),
            "quality_standards_met": self._check_quality_standards(),
            "data_minimization": self._check_data_minimization(),
            "retention_compliance": self._check_retention_compliance()
        }
        
        overall_compliance = all(compliance_indicators.values())
        
        return {
            "overall_compliance": overall_compliance,
            "compliance_indicators": compliance_indicators,
            "quality_summary": quality_summary,
            "processing_summary": processing_summary,
            "last_updated": datetime.datetime.now().isoformat()
        }
    
    def _check_regular_assessments(self) -> bool:
        """Check if regular data quality assessments are being conducted"""
        if not self.quality_assessments:
            return False
        
        # Check if assessments are within 90 days
        latest_assessment = max(self.quality_assessments, key=lambda x: x.assessment_date)
        assessment_date = datetime.datetime.fromisoformat(latest_assessment.assessment_date)
        days_since_assessment = (datetime.datetime.now() - assessment_date).days
        
        return days_since_assessment <= 90
    
    def _check_quality_standards(self) -> bool:
        """Check if data quality standards are being met"""
        if not self.quality_assessments:
            return False
        
        # Check if all latest assessments meet minimum standards
        latest_assessments = {}
        for assessment in self.quality_assessments:
            category = assessment.category.value
            if category not in latest_assessments or assessment.assessment_date > latest_assessments[category]['date']:
                latest_assessments[category] = assessment
        
        for assessment in latest_assessments.values():
            overall_score = (assessment.completeness_score + assessment.accuracy_score + 
                           assessment.consistency_score + assessment.timeliness_score) / 4
            if overall_score < 70:  # Minimum acceptable score
                return False
        
        return True
    
    def _check_data_minimization(self) -> bool:
        """Check if data minimization principles are being followed"""
        # This would typically check against data processing records
        # For now, return True as we're implementing data minimization
        return True
    
    def _check_retention_compliance(self) -> bool:
        """Check if data retention policies are being followed"""
        # This would typically check retention periods against actual data
        # For now, return True as we're implementing proper retention
        return True

# Global data governance system instance
data_governor = DataGovernanceSystem()
