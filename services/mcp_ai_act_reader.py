"""
MCP AI Act Report Reader

This module reads and parses compliance reports from the mcp-ai-act directory
to provide real compliance data to the dashboard.
"""

import json
import os
import glob
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

class MCPAIActReader:
    """Reads and parses MCP AI Act compliance reports"""
    
    def __init__(self, base_path: str = "mcp-ai-act"):
        # Get absolute path relative to project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        self.base_path = os.path.join(project_root, base_path)
        self.latest_report = None
        self.latest_report_path = None
        self._load_latest_report()
    
    def _load_latest_report(self) -> None:
        """Find and load the most recent compliance report"""
        try:
            # Find all report JSON files
            pattern = os.path.join(self.base_path, "session-*/report-analysis/report-*.json")
            report_files = glob.glob(pattern)
            
            if not report_files:
                return
            
            # Sort by modification time to get the latest
            report_files.sort(key=os.path.getmtime, reverse=True)
            latest_file = report_files[0]
            
            # Load the report
            with open(latest_file, 'r') as f:
                self.latest_report = json.load(f)
                self.latest_report_path = latest_file
                
        except Exception as e:
            print(f"Error loading MCP AI Act report: {e}")
            self.latest_report = None
            self.latest_report_path = None
    
    def get_latest_report(self) -> Optional[Dict[str, Any]]:
        """Get the latest compliance report"""
        return self.latest_report
    
    def get_report_metadata(self) -> Dict[str, Any]:
        """Get metadata about the latest report"""
        if not self.latest_report:
            return {
                "available": False,
                "message": "No compliance report found"
            }
        
        # Extract session ID from path
        session_id = None
        if self.latest_report_path:
            parts = self.latest_report_path.split(os.sep)
            for part in parts:
                if part.startswith("session-"):
                    session_id = part
                    break
        
        metadata = self.latest_report.get("assessment_metadata", {})
        
        return {
            "available": True,
            "session_id": session_id,
            "report_path": self.latest_report_path,
            "analysis_timestamp": metadata.get("analysis_timestamp"),
            "total_articles_analyzed": metadata.get("total_articles_analyzed", 0),
            "total_categories_checked": metadata.get("total_categories_checked", 0),
            "data_version": metadata.get("data_version")
        }
    
    def get_risk_level(self) -> str:
        """Get the risk level from the report"""
        if not self.latest_report:
            return "unknown"
        return self.latest_report.get("risk_level", "unknown")
    
    def get_compliance_score(self) -> float:
        """Get the compliance score (0-1)"""
        if not self.latest_report:
            return 0.0
        return self.latest_report.get("compliance_score", 0.0)
    
    def get_applicable_articles(self) -> list:
        """Get list of applicable articles"""
        if not self.latest_report:
            return []
        return self.latest_report.get("applicable_articles", [])
    
    def get_compliance_categories(self) -> Dict[str, Any]:
        """Get compliance categories and their status"""
        if not self.latest_report:
            return {}
        return self.latest_report.get("compliance_categories", {})
    
    def get_requirements(self) -> list:
        """Get list of requirements"""
        if not self.latest_report:
            return []
        return self.latest_report.get("requirements", [])
    
    def get_recommendations(self) -> list:
        """Get list of recommendations"""
        if not self.latest_report:
            return []
        return self.latest_report.get("recommendations", [])
    
    def get_risk_breakdown(self) -> Dict[str, int]:
        """Get risk breakdown percentages"""
        if not self.latest_report:
            return {}
        return self.latest_report.get("risk_breakdown", {})
    
    def is_high_risk(self) -> bool:
        """Check if system is classified as high-risk"""
        if not self.latest_report:
            return False
        risk_level = self.latest_report.get("risk_level", "").lower()
        return "high" in risk_level or risk_level == "high_risk"
    
    def get_detailed_analysis(self) -> str:
        """Get the detailed analysis text"""
        if not self.latest_report:
            return ""
        return self.latest_report.get("detailed_analysis", "")
    
    def get_simple_summary(self) -> str:
        """Get the simple summary text"""
        if not self.latest_report:
            return ""
        return self.latest_report.get("simple_summary", "")

# Global instance
mcp_ai_act_reader = MCPAIActReader()
