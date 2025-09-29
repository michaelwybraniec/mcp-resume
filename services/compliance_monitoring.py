"""
Advanced Compliance Monitoring System for AI Act Compliance

This module implements advanced monitoring, alerting, and analytics systems
for comprehensive AI Act compliance management.
"""

import json
import datetime
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    """Types of compliance metrics"""
    RISK_LEVEL = "risk_level"
    DATA_QUALITY = "data_quality"
    HUMAN_OVERSIGHT = "human_oversight"
    SYSTEM_PERFORMANCE = "system_performance"
    COMPLIANCE_SCORE = "compliance_score"
    USER_INTERACTION = "user_interaction"

@dataclass
class ComplianceAlert:
    """Compliance alert data structure"""
    id: str
    timestamp: str
    level: AlertLevel
    metric_type: MetricType
    title: str
    description: str
    threshold_value: float
    current_value: float
    status: str  # "active", "acknowledged", "resolved"
    assigned_to: Optional[str]
    resolution_notes: Optional[str]
    resolved_at: Optional[str]

@dataclass
class ComplianceMetric:
    """Compliance metric data structure"""
    id: str
    metric_type: MetricType
    timestamp: str
    value: float
    threshold_warning: float
    threshold_critical: float
    metadata: Dict[str, Any]

@dataclass
class ComplianceReport:
    """Compliance report data structure"""
    id: str
    report_date: str
    period_start: str
    period_end: str
    overall_score: float
    metrics_summary: Dict[str, Any]
    alerts_summary: Dict[str, Any]
    recommendations: List[str]
    compliance_status: str

class ComplianceMonitor:
    """Advanced compliance monitoring system"""
    
    def __init__(self):
        self.alerts: List[ComplianceAlert] = []
        self.metrics: List[ComplianceMetric] = []
        self.reports: List[ComplianceReport] = []
        self.monitoring_log_file = "data/compliance_monitoring.json"
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alert_callbacks: List[Callable] = []
        self._load_existing_data()
        self._initialize_default_thresholds()
    
    def _load_existing_data(self):
        """Load existing monitoring data from file"""
        try:
            with open(self.monitoring_log_file, 'r') as f:
                data = json.load(f)
                self.alerts = [self._deserialize_alert(alert_data) for alert_data in data.get('alerts', [])]
                self.metrics = [self._deserialize_metric(metric_data) for metric_data in data.get('metrics', [])]
                self.reports = [self._deserialize_report(report_data) for report_data in data.get('reports', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading monitoring data: {e}")
    
    def _save_data(self):
        """Save monitoring data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.monitoring_log_file), exist_ok=True)
            
            data = {
                'alerts': [self._serialize_alert(alert) for alert in self.alerts],
                'metrics': [self._serialize_metric(metric) for metric in self.metrics],
                'reports': [self._serialize_report(report) for report in self.reports],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.monitoring_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving monitoring data: {e}")
    
    def _serialize_alert(self, alert: ComplianceAlert) -> Dict[str, Any]:
        """Serialize alert for JSON storage"""
        alert_dict = asdict(alert)
        alert_dict['level'] = alert.level.value
        alert_dict['metric_type'] = alert.metric_type.value
        return alert_dict
    
    def _deserialize_alert(self, alert_data: Dict[str, Any]) -> ComplianceAlert:
        """Deserialize alert from JSON"""
        alert_data['level'] = AlertLevel(alert_data['level'])
        alert_data['metric_type'] = MetricType(alert_data['metric_type'])
        return ComplianceAlert(**alert_data)
    
    def _serialize_metric(self, metric: ComplianceMetric) -> Dict[str, Any]:
        """Serialize metric for JSON storage"""
        metric_dict = asdict(metric)
        metric_dict['metric_type'] = metric.metric_type.value
        return metric_dict
    
    def _deserialize_metric(self, metric_data: Dict[str, Any]) -> ComplianceMetric:
        """Deserialize metric from JSON"""
        metric_data['metric_type'] = MetricType(metric_data['metric_type'])
        return ComplianceMetric(**metric_data)
    
    def _serialize_report(self, report: ComplianceReport) -> Dict[str, Any]:
        """Serialize report for JSON storage"""
        return asdict(report)
    
    def _deserialize_report(self, report_data: Dict[str, Any]) -> ComplianceReport:
        """Deserialize report from JSON"""
        return ComplianceReport(**report_data)
    
    def _initialize_default_thresholds(self):
        """Initialize default monitoring thresholds"""
        self.thresholds = {
            MetricType.RISK_LEVEL: {"warning": 0.7, "critical": 0.9},
            MetricType.DATA_QUALITY: {"warning": 0.8, "critical": 0.6},
            MetricType.HUMAN_OVERSIGHT: {"warning": 0.1, "critical": 0.05},
            MetricType.SYSTEM_PERFORMANCE: {"warning": 0.9, "critical": 0.95},
            MetricType.COMPLIANCE_SCORE: {"warning": 0.8, "critical": 0.7},
            MetricType.USER_INTERACTION: {"warning": 100, "critical": 50}
        }
    
    def record_metric(self, metric_type: MetricType, value: float, metadata: Dict[str, Any] = None) -> str:
        """Record a compliance metric"""
        import uuid
        metric_id = str(uuid.uuid4())
        
        thresholds = self.thresholds.get(metric_type, {"warning": 0.8, "critical": 0.6})
        
        metric = ComplianceMetric(
            id=metric_id,
            metric_type=metric_type,
            timestamp=datetime.datetime.now().isoformat(),
            value=value,
            threshold_warning=thresholds["warning"],
            threshold_critical=thresholds["critical"],
            metadata=metadata or {}
        )
        
        self.metrics.append(metric)
        self._save_data()
        
        # Check for alerts
        self._check_metric_thresholds(metric)
        
        return metric_id
    
    def _check_metric_thresholds(self, metric: ComplianceMetric):
        """Check if metric exceeds thresholds and create alerts"""
        current_value = metric.value
        warning_threshold = metric.threshold_warning
        critical_threshold = metric.threshold_critical
        
        alert_level = None
        threshold_value = None
        
        # Determine alert level based on metric type and thresholds
        if metric.metric_type in [MetricType.RISK_LEVEL, MetricType.SYSTEM_PERFORMANCE]:
            # Higher values are worse for these metrics
            if current_value >= critical_threshold:
                alert_level = AlertLevel.CRITICAL
                threshold_value = critical_threshold
            elif current_value >= warning_threshold:
                alert_level = AlertLevel.WARNING
                threshold_value = warning_threshold
        else:
            # Lower values are worse for these metrics
            if current_value <= critical_threshold:
                alert_level = AlertLevel.CRITICAL
                threshold_value = critical_threshold
            elif current_value <= warning_threshold:
                alert_level = AlertLevel.WARNING
                threshold_value = warning_threshold
        
        if alert_level:
            self.create_alert(
                level=alert_level,
                metric_type=metric.metric_type,
                title=f"{metric.metric_type.value.replace('_', ' ').title()} Threshold Exceeded",
                description=f"Current value {current_value:.2f} {'exceeds' if metric.metric_type in [MetricType.RISK_LEVEL, MetricType.SYSTEM_PERFORMANCE] else 'falls below'} threshold of {threshold_value:.2f}",
                threshold_value=threshold_value,
                current_value=current_value
            )
    
    def create_alert(self, level: AlertLevel, metric_type: MetricType, title: str,
                    description: str, threshold_value: float, current_value: float,
                    assigned_to: Optional[str] = None) -> str:
        """Create a compliance alert"""
        import uuid
        alert_id = str(uuid.uuid4())
        
        alert = ComplianceAlert(
            id=alert_id,
            timestamp=datetime.datetime.now().isoformat(),
            level=level,
            metric_type=metric_type,
            title=title,
            description=description,
            threshold_value=threshold_value,
            current_value=current_value,
            status="active",
            assigned_to=assigned_to,
            resolution_notes=None,
            resolved_at=None
        )
        
        self.alerts.append(alert)
        self._save_data()
        
        # Trigger alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Error in alert callback: {e}")
        
        return alert_id
    
    def acknowledge_alert(self, alert_id: str, assigned_to: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert.id == alert_id and alert.status == "active":
                alert.status = "acknowledged"
                alert.assigned_to = assigned_to
                self._save_data()
                return True
        return False
    
    def resolve_alert(self, alert_id: str, resolution_notes: str) -> bool:
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id and alert.status in ["active", "acknowledged"]:
                alert.status = "resolved"
                alert.resolution_notes = resolution_notes
                alert.resolved_at = datetime.datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def get_active_alerts(self) -> List[ComplianceAlert]:
        """Get all active alerts"""
        return [alert for alert in self.alerts if alert.status == "active"]
    
    def get_alerts_by_level(self, level: AlertLevel) -> List[ComplianceAlert]:
        """Get alerts by severity level"""
        return [alert for alert in self.alerts if alert.level == level]
    
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for specified time period"""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        cutoff_str = cutoff_time.isoformat()
        
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_str]
        
        if not recent_metrics:
            return {"message": "No metrics available for the specified period"}
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in recent_metrics:
            metric_type = metric.metric_type.value
            if metric_type not in metrics_by_type:
                metrics_by_type[metric_type] = []
            metrics_by_type[metric_type].append(metric.value)
        
        # Calculate statistics
        summary = {}
        for metric_type, values in metrics_by_type.items():
            summary[metric_type] = {
                "count": len(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "latest": values[-1] if values else None
            }
        
        return summary
    
    def generate_compliance_report(self, period_days: int = 30) -> str:
        """Generate comprehensive compliance report"""
        import uuid
        report_id = str(uuid.uuid4())
        
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=period_days)
        
        # Get metrics for the period
        period_metrics = [m for m in self.metrics if start_date.isoformat() <= m.timestamp <= end_date.isoformat()]
        period_alerts = [a for a in self.alerts if start_date.isoformat() <= a.timestamp <= end_date.isoformat()]
        
        # Calculate overall compliance score
        overall_score = self._calculate_compliance_score(period_metrics, period_alerts)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(period_metrics, period_alerts)
        
        # Create report
        report = ComplianceReport(
            id=report_id,
            report_date=end_date.isoformat(),
            period_start=start_date.isoformat(),
            period_end=end_date.isoformat(),
            overall_score=overall_score,
            metrics_summary=self.get_metrics_summary(hours=period_days * 24),
            alerts_summary=self._get_alerts_summary(period_alerts),
            recommendations=recommendations,
            compliance_status="compliant" if overall_score >= 0.8 else "non_compliant"
        )
        
        self.reports.append(report)
        self._save_data()
        
        return report_id
    
    def _calculate_compliance_score(self, metrics: List[ComplianceMetric], alerts: List[ComplianceAlert]) -> float:
        """Calculate overall compliance score"""
        if not metrics:
            return 0.0
        
        # Base score from metrics
        metric_scores = []
        for metric in metrics:
            if metric.metric_type in [MetricType.RISK_LEVEL, MetricType.SYSTEM_PERFORMANCE]:
                # Higher values are worse
                score = max(0, 1 - metric.value)
            else:
                # Lower values are worse
                score = metric.value
            metric_scores.append(score)
        
        base_score = sum(metric_scores) / len(metric_scores) if metric_scores else 0.0
        
        # Penalty for alerts
        alert_penalty = 0.0
        for alert in alerts:
            if alert.status == "active":
                if alert.level == AlertLevel.CRITICAL:
                    alert_penalty += 0.1
                elif alert.level == AlertLevel.ERROR:
                    alert_penalty += 0.05
                elif alert.level == AlertLevel.WARNING:
                    alert_penalty += 0.02
        
        final_score = max(0.0, base_score - alert_penalty)
        return min(1.0, final_score)
    
    def _get_alerts_summary(self, alerts: List[ComplianceAlert]) -> Dict[str, Any]:
        """Get alerts summary"""
        summary = {
            "total_alerts": len(alerts),
            "active_alerts": len([a for a in alerts if a.status == "active"]),
            "resolved_alerts": len([a for a in alerts if a.status == "resolved"]),
            "alerts_by_level": {},
            "alerts_by_type": {}
        }
        
        for alert in alerts:
            level = alert.level.value
            metric_type = alert.metric_type.value
            
            summary["alerts_by_level"][level] = summary["alerts_by_level"].get(level, 0) + 1
            summary["alerts_by_type"][metric_type] = summary["alerts_by_type"].get(metric_type, 0) + 1
        
        return summary
    
    def _generate_recommendations(self, metrics: List[ComplianceMetric], alerts: List[ComplianceAlert]) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # Analyze metrics
        if metrics:
            risk_metrics = [m for m in metrics if m.metric_type == MetricType.RISK_LEVEL]
            if risk_metrics and any(m.value > 0.7 for m in risk_metrics):
                recommendations.append("Review and update risk mitigation strategies for high-risk areas")
            
            quality_metrics = [m for m in metrics if m.metric_type == MetricType.DATA_QUALITY]
            if quality_metrics and any(m.value < 0.8 for m in quality_metrics):
                recommendations.append("Improve data quality procedures and validation processes")
        
        # Analyze alerts
        active_alerts = [a for a in alerts if a.status == "active"]
        if len(active_alerts) > 5:
            recommendations.append("Address high number of active alerts to improve compliance status")
        
        critical_alerts = [a for a in active_alerts if a.level == AlertLevel.CRITICAL]
        if critical_alerts:
            recommendations.append("Immediately address critical alerts to prevent compliance violations")
        
        if not recommendations:
            recommendations.append("Continue current compliance practices and monitoring")
        
        return recommendations
    
    def start_monitoring(self, interval_seconds: int = 300):
        """Start continuous monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, args=(interval_seconds,))
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
    
    def _monitoring_loop(self, interval_seconds: int):
        """Continuous monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                time.sleep(interval_seconds)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(interval_seconds)
    
    def _collect_system_metrics(self):
        """Collect system metrics for monitoring"""
        # This would integrate with the existing compliance systems
        # For now, we'll create some sample metrics
        
        # Risk level metric (simulated)
        risk_level = 0.3  # Low risk
        self.record_metric(MetricType.RISK_LEVEL, risk_level, {"source": "risk_assessment"})
        
        # Data quality metric (simulated)
        data_quality = 0.85  # Good quality
        self.record_metric(MetricType.DATA_QUALITY, data_quality, {"source": "quality_assessment"})
        
        # System performance metric (simulated)
        system_performance = 0.95  # Excellent performance
        self.record_metric(MetricType.SYSTEM_PERFORMANCE, system_performance, {"source": "performance_monitor"})
    
    def add_alert_callback(self, callback: Callable):
        """Add alert callback function"""
        self.alert_callbacks.append(callback)
    
    def get_compliance_dashboard_data(self) -> Dict[str, Any]:
        """Get data for compliance dashboard"""
        return {
            "active_alerts": len(self.get_active_alerts()),
            "critical_alerts": len(self.get_alerts_by_level(AlertLevel.CRITICAL)),
            "metrics_summary": self.get_metrics_summary(hours=24),
            "latest_report": self.reports[-1] if self.reports else None,
            "monitoring_status": "active" if self.monitoring_active else "inactive"
        }

# Global compliance monitor instance
compliance_monitor = ComplianceMonitor()
