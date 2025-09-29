"""
Performance Analytics System for AI Act Compliance

This module implements advanced performance metrics, analytics, and reporting
for comprehensive AI Act compliance monitoring and optimization.
"""

import json
import datetime
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class MetricCategory(Enum):
    """Performance metric categories"""
    SYSTEM_PERFORMANCE = "system_performance"
    USER_EXPERIENCE = "user_experience"
    COMPLIANCE_METRICS = "compliance_metrics"
    RISK_METRICS = "risk_metrics"
    DATA_QUALITY = "data_quality"
    HUMAN_OVERSIGHT = "human_oversight"

class TimeRange(Enum):
    """Time range options for analytics"""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    id: str
    category: MetricCategory
    name: str
    value: float
    unit: str
    timestamp: str
    metadata: Dict[str, Any]

@dataclass
class AnalyticsReport:
    """Analytics report data structure"""
    id: str
    report_type: str
    period_start: str
    period_end: str
    metrics_summary: Dict[str, Any]
    trends: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    generated_at: str

@dataclass
class TrendAnalysis:
    """Trend analysis data structure"""
    metric_name: str
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0-1
    change_percentage: float
    significance: str  # "high", "medium", "low"

class PerformanceAnalytics:
    """Advanced performance analytics system"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.reports: List[AnalyticsReport] = []
        self.analytics_log_file = "data/performance_analytics.json"
        self._load_existing_data()
        self._initialize_default_metrics()
    
    def _load_existing_data(self):
        """Load existing analytics data from file"""
        try:
            with open(self.analytics_log_file, 'r') as f:
                data = json.load(f)
                self.metrics = [self._deserialize_metric(metric_data) for metric_data in data.get('metrics', [])]
                self.reports = [self._deserialize_report(report_data) for report_data in data.get('reports', [])]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading analytics data: {e}")
    
    def _save_data(self):
        """Save analytics data to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.analytics_log_file), exist_ok=True)
            
            data = {
                'metrics': [self._serialize_metric(metric) for metric in self.metrics],
                'reports': [self._serialize_report(report) for report in self.reports],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.analytics_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics data: {e}")
    
    def _serialize_metric(self, metric: PerformanceMetric) -> Dict[str, Any]:
        """Serialize metric for JSON storage"""
        metric_dict = asdict(metric)
        metric_dict['category'] = metric.category.value
        return metric_dict
    
    def _deserialize_metric(self, metric_data: Dict[str, Any]) -> PerformanceMetric:
        """Deserialize metric from JSON"""
        metric_data['category'] = MetricCategory(metric_data['category'])
        return PerformanceMetric(**metric_data)
    
    def _serialize_report(self, report: AnalyticsReport) -> Dict[str, Any]:
        """Serialize report for JSON storage"""
        return asdict(report)
    
    def _deserialize_report(self, report_data: Dict[str, Any]) -> AnalyticsReport:
        """Deserialize report from JSON"""
        return AnalyticsReport(**report_data)
    
    def _initialize_default_metrics(self):
        """Initialize default performance metrics"""
        # This would typically load from configuration or database
        # For now, we'll create some sample metrics
        pass
    
    def record_metric(self, category: MetricCategory, name: str, value: float, 
                     unit: str, metadata: Dict[str, Any] = None) -> str:
        """Record a performance metric"""
        import uuid
        metric_id = str(uuid.uuid4())
        
        metric = PerformanceMetric(
            id=metric_id,
            category=category,
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.datetime.now().isoformat(),
            metadata=metadata or {}
        )
        
        self.metrics.append(metric)
        self._save_data()
        
        return metric_id
    
    def get_metrics_by_category(self, category: MetricCategory, 
                               time_range: TimeRange = TimeRange.DAY) -> List[PerformanceMetric]:
        """Get metrics by category and time range"""
        cutoff_time = self._get_cutoff_time(time_range)
        cutoff_str = cutoff_time.isoformat()
        
        return [m for m in self.metrics 
                if m.category == category and m.timestamp >= cutoff_str]
    
    def get_metrics_by_name(self, name: str, time_range: TimeRange = TimeRange.DAY) -> List[PerformanceMetric]:
        """Get metrics by name and time range"""
        cutoff_time = self._get_cutoff_time(time_range)
        cutoff_str = cutoff_time.isoformat()
        
        return [m for m in self.metrics 
                if m.name == name and m.timestamp >= cutoff_str]
    
    def _get_cutoff_time(self, time_range: TimeRange) -> datetime.datetime:
        """Get cutoff time for time range"""
        now = datetime.datetime.now()
        
        if time_range == TimeRange.HOUR:
            return now - datetime.timedelta(hours=1)
        elif time_range == TimeRange.DAY:
            return now - datetime.timedelta(days=1)
        elif time_range == TimeRange.WEEK:
            return now - datetime.timedelta(weeks=1)
        elif time_range == TimeRange.MONTH:
            return now - datetime.timedelta(days=30)
        elif time_range == TimeRange.QUARTER:
            return now - datetime.timedelta(days=90)
        elif time_range == TimeRange.YEAR:
            return now - datetime.timedelta(days=365)
        else:
            return now - datetime.timedelta(days=1)
    
    def calculate_metric_statistics(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Calculate statistics for a list of metrics"""
        if not metrics:
            return {"error": "No metrics provided"}
        
        values = [m.value for m in metrics]
        
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "mode": statistics.mode(values) if len(set(values)) < len(values) else None,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "variance": statistics.variance(values) if len(values) > 1 else 0
        }
    
    def analyze_trends(self, metric_name: str, time_range: TimeRange = TimeRange.WEEK) -> TrendAnalysis:
        """Analyze trends for a specific metric"""
        metrics = self.get_metrics_by_name(metric_name, time_range)
        
        if len(metrics) < 2:
            return TrendAnalysis(
                metric_name=metric_name,
                trend_direction="insufficient_data",
                trend_strength=0.0,
                change_percentage=0.0,
                significance="low"
            )
        
        # Sort metrics by timestamp
        metrics.sort(key=lambda x: x.timestamp)
        
        # Calculate trend using linear regression
        x_values = list(range(len(metrics)))
        y_values = [m.value for m in metrics]
        
        # Simple linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine trend direction
        if slope > 0.01:
            trend_direction = "increasing"
        elif slope < -0.01:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"
        
        # Calculate trend strength (R-squared)
        y_mean = sum_y / n
        ss_tot = sum((y - y_mean) ** 2 for y in y_values)
        ss_res = sum((y - (slope * x + (sum_y - slope * sum_x) / n)) ** 2 
                    for x, y in zip(x_values, y_values))
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        trend_strength = abs(r_squared)
        
        # Calculate change percentage
        first_value = y_values[0]
        last_value = y_values[-1]
        change_percentage = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
        
        # Determine significance
        if trend_strength > 0.7:
            significance = "high"
        elif trend_strength > 0.4:
            significance = "medium"
        else:
            significance = "low"
        
        return TrendAnalysis(
            metric_name=metric_name,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            change_percentage=change_percentage,
            significance=significance
        )
    
    def generate_performance_report(self, time_range: TimeRange = TimeRange.WEEK) -> str:
        """Generate comprehensive performance report"""
        import uuid
        report_id = str(uuid.uuid4())
        
        end_date = datetime.datetime.now()
        start_date = self._get_cutoff_time(time_range)
        
        # Get metrics for the period
        period_metrics = [m for m in self.metrics 
                         if start_date.isoformat() <= m.timestamp <= end_date.isoformat()]
        
        # Calculate metrics summary
        metrics_summary = {}
        for category in MetricCategory:
            category_metrics = [m for m in period_metrics if m.category == category]
            if category_metrics:
                metrics_summary[category.value] = self.calculate_metric_statistics(category_metrics)
        
        # Analyze trends
        trends = {}
        unique_metric_names = list(set(m.name for m in period_metrics))
        for metric_name in unique_metric_names:
            trends[metric_name] = self.analyze_trends(metric_name, time_range)
        
        # Generate insights
        insights = self._generate_insights(metrics_summary, trends)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics_summary, trends)
        
        # Create report
        report = AnalyticsReport(
            id=report_id,
            report_type=f"performance_report_{time_range.value}",
            period_start=start_date.isoformat(),
            period_end=end_date.isoformat(),
            metrics_summary=metrics_summary,
            trends=trends,
            insights=insights,
            recommendations=recommendations,
            generated_at=datetime.datetime.now().isoformat()
        )
        
        self.reports.append(report)
        self._save_data()
        
        return report_id
    
    def _generate_insights(self, metrics_summary: Dict[str, Any], 
                          trends: Dict[str, TrendAnalysis]) -> List[str]:
        """Generate insights from metrics and trends"""
        insights = []
        
        # Analyze system performance
        if MetricCategory.SYSTEM_PERFORMANCE.value in metrics_summary:
            perf_stats = metrics_summary[MetricCategory.SYSTEM_PERFORMANCE.value]
            if perf_stats.get('mean', 0) > 0.9:
                insights.append("System performance is excellent with high reliability")
            elif perf_stats.get('mean', 0) > 0.8:
                insights.append("System performance is good with room for optimization")
            else:
                insights.append("System performance needs attention and improvement")
        
        # Analyze compliance metrics
        if MetricCategory.COMPLIANCE_METRICS.value in metrics_summary:
            comp_stats = metrics_summary[MetricCategory.COMPLIANCE_METRICS.value]
            if comp_stats.get('mean', 0) > 0.9:
                insights.append("Compliance metrics show excellent adherence to AI Act requirements")
            elif comp_stats.get('mean', 0) > 0.8:
                insights.append("Compliance metrics show good adherence with minor improvements needed")
            else:
                insights.append("Compliance metrics indicate areas requiring immediate attention")
        
        # Analyze trends
        for metric_name, trend in trends.items():
            if trend.significance == "high":
                if trend.trend_direction == "increasing" and "performance" in metric_name.lower():
                    insights.append(f"Strong positive trend in {metric_name} indicates system improvement")
                elif trend.trend_direction == "decreasing" and "risk" in metric_name.lower():
                    insights.append(f"Strong decreasing trend in {metric_name} shows effective risk mitigation")
                elif trend.trend_direction == "decreasing" and "performance" in metric_name.lower():
                    insights.append(f"Concerning decreasing trend in {metric_name} requires investigation")
        
        if not insights:
            insights.append("System performance is stable with no significant trends detected")
        
        return insights
    
    def _generate_recommendations(self, metrics_summary: Dict[str, Any], 
                                 trends: Dict[str, TrendAnalysis]) -> List[str]:
        """Generate recommendations based on metrics and trends"""
        recommendations = []
        
        # Performance recommendations
        if MetricCategory.SYSTEM_PERFORMANCE.value in metrics_summary:
            perf_stats = metrics_summary[MetricCategory.SYSTEM_PERFORMANCE.value]
            if perf_stats.get('mean', 0) < 0.8:
                recommendations.append("Implement system performance optimization measures")
        
        # Compliance recommendations
        if MetricCategory.COMPLIANCE_METRICS.value in metrics_summary:
            comp_stats = metrics_summary[MetricCategory.COMPLIANCE_METRICS.value]
            if comp_stats.get('mean', 0) < 0.8:
                recommendations.append("Review and strengthen compliance procedures")
        
        # Risk recommendations
        if MetricCategory.RISK_METRICS.value in metrics_summary:
            risk_stats = metrics_summary[MetricCategory.RISK_METRICS.value]
            if risk_stats.get('mean', 0) > 0.7:
                recommendations.append("Enhance risk mitigation strategies")
        
        # Data quality recommendations
        if MetricCategory.DATA_QUALITY.value in metrics_summary:
            quality_stats = metrics_summary[MetricCategory.DATA_QUALITY.value]
            if quality_stats.get('mean', 0) < 0.8:
                recommendations.append("Improve data quality validation processes")
        
        # Trend-based recommendations
        for metric_name, trend in trends.items():
            if trend.significance == "high" and trend.trend_direction == "decreasing":
                if "performance" in metric_name.lower():
                    recommendations.append(f"Investigate and address declining {metric_name}")
                elif "compliance" in metric_name.lower():
                    recommendations.append(f"Take corrective action for declining {metric_name}")
        
        if not recommendations:
            recommendations.append("Continue current performance monitoring and optimization efforts")
        
        return recommendations
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get key metrics for dashboard display"""
        # Get recent metrics (last 24 hours)
        recent_metrics = [m for m in self.metrics 
                         if datetime.datetime.fromisoformat(m.timestamp) >= 
                         datetime.datetime.now() - datetime.timedelta(hours=24)]
        
        if not recent_metrics:
            return {"message": "No recent metrics available"}
        
        # Calculate key performance indicators
        kpis = {}
        for category in MetricCategory:
            category_metrics = [m for m in recent_metrics if m.category == category]
            if category_metrics:
                stats = self.calculate_metric_statistics(category_metrics)
                kpis[category.value] = {
                    "current_value": stats.get('mean', 0),
                    "trend": self.analyze_trends(category_metrics[0].name, TimeRange.DAY).trend_direction,
                    "count": stats.get('count', 0)
                }
        
        return {
            "kpis": kpis,
            "total_metrics": len(recent_metrics),
            "last_updated": max(m.timestamp for m in recent_metrics) if recent_metrics else None
        }
    
    def get_report_by_id(self, report_id: str) -> Optional[AnalyticsReport]:
        """Get analytics report by ID"""
        for report in self.reports:
            if report.id == report_id:
                return report
        return None
    
    def get_latest_report(self) -> Optional[AnalyticsReport]:
        """Get the latest analytics report"""
        if not self.reports:
            return None
        return max(self.reports, key=lambda x: x.generated_at)

# Global performance analytics instance
performance_analytics = PerformanceAnalytics()
