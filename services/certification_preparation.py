"""
Certification Preparation System for AI Act Compliance

This module implements comprehensive certification preparation procedures
for AI Act compliance certification and regulatory submission.
"""

import json
import datetime
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class CertificationType(Enum):
    """Types of certifications"""
    CE_MARKING = "ce_marking"
    CONFORMITY_ASSESSMENT = "conformity_assessment"
    THIRD_PARTY_CERTIFICATION = "third_party_certification"
    SELF_DECLARATION = "self_declaration"

class CertificationStatus(Enum):
    """Certification status"""
    PREPARING = "preparing"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class DocumentType(Enum):
    """Types of certification documents"""
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    CONFORMITY_ASSESSMENT = "conformity_assessment"
    RISK_ASSESSMENT = "risk_assessment"
    DATA_GOVERNANCE = "data_governance"
    AUDIT_REPORTS = "audit_reports"
    COMPLIANCE_EVIDENCE = "compliance_evidence"
    USER_MANUAL = "user_manual"
    DECLARATION_OF_CONFORMITY = "declaration_of_conformity"

@dataclass
class CertificationDocument:
    """Certification document data structure"""
    id: str
    document_type: DocumentType
    title: str
    description: str
    file_path: Optional[str]
    content: Optional[str]
    version: str
    created_date: str
    last_updated: str
    status: str  # "draft", "review", "approved", "submitted"
    required: bool
    evidence_type: str

@dataclass
class CertificationApplication:
    """Certification application data structure"""
    id: str
    certification_type: CertificationType
    application_date: str
    applicant: str
    status: CertificationStatus
    documents: List[CertificationDocument]
    review_notes: List[str]
    approval_date: Optional[str]
    expiry_date: Optional[str]
    certificate_number: Optional[str]
    regulatory_body: str
    contact_information: Dict[str, str]

class CertificationPreparationSystem:
    """Comprehensive certification preparation system"""
    
    def __init__(self):
        self.applications: List[CertificationApplication] = []
        self.documents: List[CertificationDocument] = []
        self.certification_log_file = "data/certification_preparation.json"
        self._load_existing_data()
        self._initialize_required_documents()
    
    def _load_existing_data(self):
        """Load existing certification data from file"""
        try:
            with open(self.certification_log_file, 'r') as f:
                data = json.load(f)
                self.applications = [self._deserialize_application(app_data) 
                                   for app_data in data.get('applications', [])]
                self.documents = [self._deserialize_document(doc_data) 
                                for doc_data in data.get('documents', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading certification data: {e}")
    
    def _save_data(self):
        """Save certification data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.certification_log_file), exist_ok=True)
            
            data = {
                'applications': [self._serialize_application(app) for app in self.applications],
                'documents': [self._serialize_document(doc) for doc in self.documents],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.certification_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving certification data: {e}")
    
    def _serialize_application(self, application: CertificationApplication) -> Dict[str, Any]:
        """Serialize application for JSON storage"""
        app_dict = asdict(application)
        app_dict['certification_type'] = application.certification_type.value
        app_dict['status'] = application.status.value
        return app_dict
    
    def _deserialize_application(self, app_data: Dict[str, Any]) -> CertificationApplication:
        """Deserialize application from JSON"""
        app_data['certification_type'] = CertificationType(app_data['certification_type'])
        app_data['status'] = CertificationStatus(app_data['status'])
        return CertificationApplication(**app_data)
    
    def _serialize_document(self, document: CertificationDocument) -> Dict[str, Any]:
        """Serialize document for JSON storage"""
        doc_dict = asdict(document)
        doc_dict['document_type'] = document.document_type.value
        return doc_dict
    
    def _deserialize_document(self, doc_data: Dict[str, Any]) -> CertificationDocument:
        """Deserialize document from JSON"""
        doc_data['document_type'] = DocumentType(doc_data['document_type'])
        return CertificationDocument(**doc_data)
    
    def _initialize_required_documents(self):
        """Initialize required certification documents"""
        if not self.documents:  # Only initialize if no existing documents
            required_docs = [
                CertificationDocument(
                    id="DOC-001",
                    document_type=DocumentType.TECHNICAL_DOCUMENTATION,
                    title="Technical Documentation",
                    description="Complete technical documentation of the AI system including architecture, algorithms, and training data",
                    file_path=None,
                    content=None,
                    version="1.0",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    status="draft",
                    required=True,
                    evidence_type="technical_specification"
                ),
                CertificationDocument(
                    id="DOC-002",
                    document_type=DocumentType.CONFORMITY_ASSESSMENT,
                    title="Conformity Assessment Report",
                    description="Comprehensive conformity assessment report demonstrating compliance with AI Act requirements",
                    file_path=None,
                    content=None,
                    version="1.0",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    status="draft",
                    required=True,
                    evidence_type="assessment_report"
                ),
                CertificationDocument(
                    id="DOC-003",
                    document_type=DocumentType.RISK_ASSESSMENT,
                    title="Risk Assessment Report",
                    description="Detailed risk assessment report including identified risks and mitigation measures",
                    file_path=None,
                    content=None,
                    version="1.0",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    status="draft",
                    required=True,
                    evidence_type="risk_analysis"
                ),
                CertificationDocument(
                    id="DOC-004",
                    document_type=DocumentType.DATA_GOVERNANCE,
                    title="Data Governance Documentation",
                    description="Data governance procedures and quality management documentation",
                    file_path=None,
                    content=None,
                    version="1.0",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    status="draft",
                    required=True,
                    evidence_type="governance_procedures"
                ),
                CertificationDocument(
                    id="DOC-005",
                    document_type=DocumentType.AUDIT_REPORTS,
                    title="Audit Reports",
                    description="Comprehensive audit reports demonstrating ongoing compliance monitoring",
                    file_path=None,
                    content=None,
                    version="1.0",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    status="draft",
                    required=True,
                    evidence_type="audit_evidence"
                ),
                CertificationDocument(
                    id="DOC-006",
                    document_type=DocumentType.DECLARATION_OF_CONFORMITY,
                    title="Declaration of Conformity",
                    description="Official declaration of conformity with EU AI Act requirements",
                    file_path=None,
                    content=None,
                    version="1.0",
                    created_date=datetime.datetime.now().isoformat(),
                    last_updated=datetime.datetime.now().isoformat(),
                    status="draft",
                    required=True,
                    evidence_type="legal_declaration"
                )
            ]
            
            self.documents.extend(required_docs)
            self._save_data()
    
    def create_certification_application(self, certification_type: CertificationType, 
                                       applicant: str, regulatory_body: str,
                                       contact_information: Dict[str, str]) -> str:
        """Create a new certification application"""
        application_id = str(uuid.uuid4())
        
        # Get required documents for this certification type
        required_docs = [doc for doc in self.documents if doc.required]
        
        application = CertificationApplication(
            id=application_id,
            certification_type=certification_type,
            application_date=datetime.datetime.now().isoformat(),
            applicant=applicant,
            status=CertificationStatus.PREPARING,
            documents=required_docs,
            review_notes=[],
            approval_date=None,
            expiry_date=None,
            certificate_number=None,
            regulatory_body=regulatory_body,
            contact_information=contact_information
        )
        
        self.applications.append(application)
        self._save_data()
        
        return application_id
    
    def update_document(self, document_id: str, content: str, version: str = None) -> bool:
        """Update a certification document"""
        for doc in self.documents:
            if doc.id == document_id:
                doc.content = content
                doc.last_updated = datetime.datetime.now().isoformat()
                if version:
                    doc.version = version
                else:
                    # Auto-increment version
                    try:
                        current_version = float(doc.version)
                        doc.version = str(current_version + 0.1)
                    except:
                        doc.version = "1.1"
                
                self._save_data()
                return True
        return False
    
    def submit_document_for_review(self, document_id: str) -> bool:
        """Submit document for review"""
        for doc in self.documents:
            if doc.id == document_id:
                doc.status = "review"
                doc.last_updated = datetime.datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def approve_document(self, document_id: str) -> bool:
        """Approve a document"""
        for doc in self.documents:
            if doc.id == document_id:
                doc.status = "approved"
                doc.last_updated = datetime.datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def submit_application(self, application_id: str) -> bool:
        """Submit certification application"""
        for app in self.applications:
            if app.id == application_id and app.status == CertificationStatus.PREPARING:
                # Check if all required documents are approved
                all_docs_approved = all(doc.status == "approved" for doc in app.documents if doc.required)
                
                if all_docs_approved:
                    app.status = CertificationStatus.SUBMITTED
                    self._save_data()
                    return True
                else:
                    return False  # Cannot submit without all required documents approved
        return False
    
    def get_application_by_id(self, application_id: str) -> Optional[CertificationApplication]:
        """Get application by ID"""
        for app in self.applications:
            if app.id == application_id:
                return app
        return None
    
    def get_document_by_id(self, document_id: str) -> Optional[CertificationDocument]:
        """Get document by ID"""
        for doc in self.documents:
            if doc.id == document_id:
                return doc
        return None
    
    def get_certification_readiness(self) -> Dict[str, Any]:
        """Get certification readiness status"""
        required_docs = [doc for doc in self.documents if doc.required]
        
        doc_status = {}
        for doc in required_docs:
            doc_status[doc.document_type.value] = {
                "status": doc.status,
                "version": doc.version,
                "last_updated": doc.last_updated,
                "has_content": bool(doc.content)
            }
        
        # Calculate readiness percentage
        approved_docs = len([doc for doc in required_docs if doc.status == "approved"])
        total_required = len(required_docs)
        readiness_percentage = (approved_docs / total_required * 100) if total_required > 0 else 0
        
        # Check if ready for submission
        ready_for_submission = all(doc.status == "approved" for doc in required_docs)
        
        return {
            "readiness_percentage": readiness_percentage,
            "ready_for_submission": ready_for_submission,
            "total_required_documents": total_required,
            "approved_documents": approved_docs,
            "document_status": doc_status,
            "missing_documents": [doc.document_type.value for doc in required_docs if doc.status != "approved"]
        }
    
    def generate_certification_package(self, application_id: str) -> Dict[str, Any]:
        """Generate complete certification package"""
        application = self.get_application_by_id(application_id)
        if not application:
            return {"error": "Application not found"}
        
        # Get all documents for the application
        package_documents = []
        for doc in application.documents:
            package_documents.append({
                "id": doc.id,
                "type": doc.document_type.value,
                "title": doc.title,
                "description": doc.description,
                "version": doc.version,
                "status": doc.status,
                "content": doc.content,
                "evidence_type": doc.evidence_type
            })
        
        return {
            "application_info": {
                "id": application.id,
                "type": application.certification_type.value,
                "applicant": application.applicant,
                "regulatory_body": application.regulatory_body,
                "application_date": application.application_date,
                "status": application.status.value
            },
            "documents": package_documents,
            "contact_information": application.contact_information,
            "generated_at": datetime.datetime.now().isoformat()
        }
    
    def get_certification_summary(self) -> Dict[str, Any]:
        """Get certification summary"""
        total_applications = len(self.applications)
        total_documents = len(self.documents)
        
        # Count applications by status
        app_status = {}
        for app in self.applications:
            status = app.status.value
            app_status[status] = app_status.get(status, 0) + 1
        
        # Count documents by status
        doc_status = {}
        for doc in self.documents:
            status = doc.status
            doc_status[status] = doc_status.get(status, 0) + 1
        
        # Get latest application
        latest_app = max(self.applications, key=lambda x: x.application_date) if self.applications else None
        
        return {
            "total_applications": total_applications,
            "total_documents": total_documents,
            "applications_by_status": app_status,
            "documents_by_status": doc_status,
            "latest_application": {
                "id": latest_app.id,
                "type": latest_app.certification_type.value,
                "date": latest_app.application_date,
                "status": latest_app.status.value
            } if latest_app else None,
            "certification_readiness": self.get_certification_readiness()
        }

# Global certification preparation system instance
certification_preparer = CertificationPreparationSystem()
