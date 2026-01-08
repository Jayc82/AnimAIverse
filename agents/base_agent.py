"""
Base Agent class for AnimAIverse multi-agent system.
Provides common functionality for all specialized agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name/identifier
            config: Configuration dictionary for the agent
        """
        self.name = name
        self.config = config
        self.history = []
        self.learning_data = []
        
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input and produce output.
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Processed output data
        """
        pass
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log an action for tracking and learning."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "action": action,
            "details": details
        }
        self.history.append(log_entry)
        
    def learn_from_feedback(self, feedback: Dict[str, Any]):
        """Store feedback for continuous learning."""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "feedback": feedback
        }
        self.learning_data.append(learning_entry)
        
    def get_history(self) -> list:
        """Return agent's action history."""
        return self.history
    
    def get_learning_data(self) -> list:
        """Return agent's learning data."""
        return self.learning_data
    
    def reset(self):
        """Reset agent state."""
        self.history = []
        self.learning_data = []
