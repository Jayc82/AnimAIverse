"""
Continuous Learning System - Improves agent performance over time.
Tracks performance, identifies patterns, and optimizes workflows.
"""
import json
import os
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict


class ContinuousLearning:
    """Manages continuous learning for the multi-agent system."""
    
    def __init__(self, history_path: str = "memory/learning_history.json"):
        self.history_path = history_path
        self.learning_history = self._load_history()
        
    def _load_history(self) -> Dict[str, Any]:
        """Load learning history from disk."""
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._initialize_history()
        return self._initialize_history()
    
    def _initialize_history(self) -> Dict[str, Any]:
        """Initialize empty learning history."""
        return {
            "productions": [],
            "agent_performance": {
                "Writer": [],
                "Director": [],
                "Animator": [],
                "SceneComposer": [],
                "Editor": []
            },
            "workflow_metrics": [],
            "improvement_insights": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_productions": 0
            }
        }
    
    def save_history(self):
        """Save learning history to disk."""
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        self.learning_history["metadata"]["last_updated"] = datetime.now().isoformat()
        
        with open(self.history_path, 'w') as f:
            json.dump(self.learning_history, f, indent=2)
    
    def record_production(self, production_data: Dict[str, Any]):
        """Record a completed production for learning."""
        production_entry = {
            "timestamp": datetime.now().isoformat(),
            "production_id": f"prod_{len(self.learning_history['productions']) + 1}",
            "data": production_data,
            "quality_score": production_data.get("quality_report", {}).get("metrics", {}).get("overall_score", 0.0)
        }
        
        self.learning_history["productions"].append(production_entry)
        self.learning_history["metadata"]["total_productions"] += 1
        
        # Keep only the last 100 productions
        if len(self.learning_history["productions"]) > 100:
            self.learning_history["productions"] = self.learning_history["productions"][-100:]
        
        self.save_history()
    
    def record_agent_performance(self, agent_name: str, performance_data: Dict[str, Any]):
        """Record individual agent performance."""
        if agent_name not in self.learning_history["agent_performance"]:
            self.learning_history["agent_performance"][agent_name] = []
        
        performance_entry = {
            "timestamp": datetime.now().isoformat(),
            "metrics": performance_data
        }
        
        self.learning_history["agent_performance"][agent_name].append(performance_entry)
        
        # Keep only the last 50 entries per agent
        if len(self.learning_history["agent_performance"][agent_name]) > 50:
            self.learning_history["agent_performance"][agent_name] = \
                self.learning_history["agent_performance"][agent_name][-50:]
        
        self.save_history()
    
    def analyze_performance_trends(self, agent_name: str = None) -> Dict[str, Any]:
        """Analyze performance trends for agents."""
        if agent_name:
            agent_history = self.learning_history["agent_performance"].get(agent_name, [])
            return self._analyze_single_agent(agent_name, agent_history)
        else:
            # Analyze all agents
            trends = {}
            for agent, history in self.learning_history["agent_performance"].items():
                trends[agent] = self._analyze_single_agent(agent, history)
            return trends
    
    def _analyze_single_agent(self, agent_name: str, history: List[Dict]) -> Dict[str, Any]:
        """Analyze single agent's performance."""
        if not history:
            return {
                "agent": agent_name,
                "trend": "no_data",
                "average_quality": 0.0,
                "improvement_rate": 0.0
            }
        
        # Calculate average quality
        qualities = [
            entry.get("metrics", {}).get("quality", 0.8)
            for entry in history
        ]
        avg_quality = sum(qualities) / len(qualities) if qualities else 0.0
        
        # Calculate improvement rate
        if len(qualities) >= 2:
            first_half_avg = sum(qualities[:len(qualities)//2]) / (len(qualities)//2)
            second_half_avg = sum(qualities[len(qualities)//2:]) / (len(qualities) - len(qualities)//2)
            improvement_rate = second_half_avg - first_half_avg
        else:
            improvement_rate = 0.0
        
        return {
            "agent": agent_name,
            "trend": "improving" if improvement_rate > 0 else "stable" if improvement_rate == 0 else "declining",
            "average_quality": avg_quality,
            "improvement_rate": improvement_rate,
            "total_tasks": len(history)
        }
    
    def identify_success_patterns(self) -> List[Dict[str, Any]]:
        """Identify patterns in successful productions."""
        successful_productions = [
            prod for prod in self.learning_history["productions"]
            if prod.get("quality_score", 0) >= 0.85
        ]
        
        if not successful_productions:
            return []
        
        patterns = []
        
        # Analyze genre patterns
        genre_scores = defaultdict(list)
        for prod in successful_productions:
            genre = prod.get("data", {}).get("script", {}).get("genre", "unknown")
            genre_scores[genre].append(prod.get("quality_score", 0))
        
        for genre, scores in genre_scores.items():
            patterns.append({
                "type": "genre",
                "value": genre,
                "average_score": sum(scores) / len(scores),
                "frequency": len(scores),
                "confidence": min(len(scores) / 10, 1.0)  # Higher confidence with more data
            })
        
        return sorted(patterns, key=lambda x: x["average_score"], reverse=True)
    
    def generate_improvement_insights(self) -> List[Dict[str, Any]]:
        """Generate insights for improvement."""
        insights = []
        
        # Analyze recent productions
        recent_productions = self.learning_history["productions"][-10:]
        if recent_productions:
            avg_recent_quality = sum(
                p.get("quality_score", 0) for p in recent_productions
            ) / len(recent_productions)
            
            if avg_recent_quality < 0.8:
                insights.append({
                    "type": "quality_alert",
                    "severity": "medium",
                    "message": "Recent production quality below target (0.8)",
                    "recommendation": "Review workflow parameters and agent configurations"
                })
        
        # Analyze agent performance
        agent_trends = self.analyze_performance_trends()
        for agent_name, trend_data in agent_trends.items():
            if trend_data.get("trend") == "declining":
                insights.append({
                    "type": "agent_performance",
                    "severity": "high",
                    "agent": agent_name,
                    "message": f"{agent_name} showing declining performance",
                    "recommendation": f"Review {agent_name} configuration and recent outputs"
                })
        
        # Store insights
        for insight in insights:
            insight["timestamp"] = datetime.now().isoformat()
            self.learning_history["improvement_insights"].append(insight)
        
        # Keep only the last 50 insights
        if len(self.learning_history["improvement_insights"]) > 50:
            self.learning_history["improvement_insights"] = \
                self.learning_history["improvement_insights"][-50:]
        
        self.save_history()
        
        return insights
    
    def get_optimization_suggestions(self) -> Dict[str, Any]:
        """Get suggestions for workflow optimization."""
        suggestions = {
            "workflow": [],
            "agent_config": [],
            "resource_allocation": []
        }
        
        # Analyze workflow metrics
        if self.learning_history["workflow_metrics"]:
            avg_duration = sum(
                m.get("duration", 0) for m in self.learning_history["workflow_metrics"]
            ) / len(self.learning_history["workflow_metrics"])
            
            if avg_duration > 300:  # More than 5 minutes
                suggestions["workflow"].append({
                    "type": "performance",
                    "message": "Average workflow duration is high",
                    "suggestion": "Consider parallel agent execution where possible"
                })
        
        # Analyze success patterns
        patterns = self.identify_success_patterns()
        if patterns:
            best_pattern = patterns[0]
            suggestions["workflow"].append({
                "type": "pattern",
                "message": f"Genre '{best_pattern['value']}' shows highest quality",
                "suggestion": f"Apply similar patterns to other genres"
            })
        
        return suggestions
    
    def record_workflow_metrics(self, metrics: Dict[str, Any]):
        """Record workflow execution metrics."""
        metric_entry = {
            "timestamp": datetime.now().isoformat(),
            "duration": metrics.get("duration", 0),
            "agent_count": metrics.get("agent_count", 0),
            "quality_score": metrics.get("quality_score", 0),
            "resource_usage": metrics.get("resource_usage", {})
        }
        
        self.learning_history["workflow_metrics"].append(metric_entry)
        
        # Keep only the last 100 metrics
        if len(self.learning_history["workflow_metrics"]) > 100:
            self.learning_history["workflow_metrics"] = \
                self.learning_history["workflow_metrics"][-100:]
        
        self.save_history()
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get a summary of learning progress."""
        total_productions = len(self.learning_history["productions"])
        
        if total_productions == 0:
            return {
                "total_productions": 0,
                "average_quality": 0.0,
                "improvement_trend": "no_data",
                "top_patterns": []
            }
        
        # Calculate average quality
        avg_quality = sum(
            p.get("quality_score", 0) for p in self.learning_history["productions"]
        ) / total_productions
        
        # Determine improvement trend
        if total_productions >= 10:
            early_quality = sum(
                p.get("quality_score", 0) 
                for p in self.learning_history["productions"][:5]
            ) / 5
            recent_quality = sum(
                p.get("quality_score", 0) 
                for p in self.learning_history["productions"][-5:]
            ) / 5
            
            improvement = recent_quality - early_quality
            trend = "improving" if improvement > 0.05 else "stable" if abs(improvement) <= 0.05 else "needs_attention"
        else:
            trend = "insufficient_data"
        
        return {
            "total_productions": total_productions,
            "average_quality": avg_quality,
            "improvement_trend": trend,
            "top_patterns": self.identify_success_patterns()[:3],
            "recent_insights": self.learning_history["improvement_insights"][-5:]
        }
    
    def export_learning_data(self, export_path: str):
        """Export learning data for analysis."""
        with open(export_path, 'w') as f:
            json.dump(self.learning_history, f, indent=2)
    
    def reset_learning_history(self):
        """Reset learning history (use with caution)."""
        self.learning_history = self._initialize_history()
        self.save_history()
