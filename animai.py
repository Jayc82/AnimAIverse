"""
AnimAIverse - NextGenAI Animation System
Main application interface for creating animated series with AI agents.
Supports multiple languages with English as the primary language.
"""
import sys
import os
import yaml
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.writer_agent import WriterAgent
from agents.director_agent import DirectorAgent
from agents.animator_agent import AnimatorAgent
from agents.scene_composer_agent import SceneComposerAgent
from agents.editor_agent import EditorAgent
from memory.style_memory import StyleMemory
from memory.continuous_learning import ContinuousLearning
from workflows.coordinator import WorkflowCoordinator
from utils.language_manager import LanguageManager


class AnimAIverse:
    """Main application class for AnimAIverse animation system."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the AnimAIverse system."""
        print("🚀 Initializing AnimAIverse - NextGenAI Animation System")
        print("="*60)
        
        # Load configuration
        self.config = self._load_config(config_path)
        print("✓ Configuration loaded")
        
        # Initialize language manager
        self.language_manager = LanguageManager()
        print(f"✓ Language manager initialized (Default: {self.language_manager.get_language_name()})")
        
        # Initialize memory systems
        self.style_memory = StyleMemory(
            self.config.get("memory", {}).get("style_memory_path", "memory/style_memory.json")
        )
        print("✓ Style memory initialized")
        
        self.continuous_learning = ContinuousLearning(
            self.config.get("memory", {}).get("learning_history_path", "memory/learning_history.json")
        )
        print("✓ Continuous learning initialized")
        
        # Initialize workflow coordinator
        self.coordinator = WorkflowCoordinator(
            self.config,
            self.style_memory,
            self.continuous_learning
        )
        print("✓ Workflow coordinator initialized")
        
        # Initialize and register agents
        self._initialize_agents()
        print("✓ All agents initialized and registered")
        
        print("="*60)
        print("✅ AnimAIverse ready for production!")
        print(f"   Supported languages: {', '.join(self.language_manager.get_supported_languages()[:5])}...")
        print()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            print(f"⚠️  Config file not found: {config_path}")
            print("   Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "animation": {
                "resolution": [1920, 1080],
                "fps": 30,
                "style": "cinematic",
                "quality": "high"
            },
            "agents": {
                "writer": {"model": "gpt-4", "temperature": 0.8},
                "director": {"model": "gpt-4", "temperature": 0.7},
                "animator": {"model": "gpt-4", "temperature": 0.6},
                "scene_composer": {"model": "gpt-4", "temperature": 0.5},
                "editor": {"model": "gpt-4", "temperature": 0.5}
            },
            "memory": {
                "style_memory_path": "memory/style_memory.json",
                "learning_history_path": "memory/learning_history.json"
            },
            "workflows": {
                "enable_continuous_learning": True,
                "auto_save_interval": 300
            },
            "output": {
                "base_path": "output",
                "save_intermediate": True,
                "format": "mp4"
            }
        }
    
    def _initialize_agents(self):
        """Initialize all specialized agents."""
        agent_configs = self.config.get("agents", {})
        
        # Create agents
        writer = WriterAgent(agent_configs.get("writer", {}))
        director = DirectorAgent(agent_configs.get("director", {}))
        animator = AnimatorAgent(agent_configs.get("animator", {}))
        composer = SceneComposerAgent(agent_configs.get("scene_composer", {}))
        editor = EditorAgent(agent_configs.get("editor", {}))
        
        # Register with coordinator
        self.coordinator.register_agent("Writer", writer)
        self.coordinator.register_agent("Director", director)
        self.coordinator.register_agent("Animator", animator)
        self.coordinator.register_agent("SceneComposer", composer)
        self.coordinator.register_agent("Editor", editor)
    
    def create_animation(self, 
                        genre: str = "action",
                        theme: str = "",
                        characters: list = None,
                        duration: int = 5,
                        style_preferences: Optional[Dict[str, Any]] = None,
                        language: str = "en") -> Dict[str, Any]:
        """
        Create a full animated series.
        
        Args:
            genre: Animation genre (action, drama, comedy, adventure)
            theme: Central theme or story concept
            characters: List of character names/descriptions
            duration: Target duration in minutes
            style_preferences: Optional style preferences
            language: Target language code (default: 'en' for English)
                     Supported: en, es, fr, de, it, pt, ja, ko, zh, ar, ru, hi
            
        Returns:
            Complete production results
        """
        if characters is None:
            characters = ["Hero", "Companion", "Antagonist"]
        
        # Validate and set language
        if not self.language_manager.is_language_supported(language):
            print(f"⚠️  Language '{language}' not supported. Using English (en)")
            language = "en"
        
        self.language_manager.set_language(language)
        language_name = self.language_manager.get_language_name(language)
        
        print(f"\n🌍 Production Language: {language_name} ({language})")
        
        production_request = {
            "genre": genre,
            "theme": theme if theme else f"An epic {genre} story",
            "characters": characters,
            "duration": duration,
            "style_preferences": style_preferences or {},
            "language": language
        }
        
        # Add language context to production request
        production_request = self.language_manager.format_agent_input(production_request, language)
        
        # Execute production
        result = self.coordinator.execute_production(production_request)
        
        # Save output if requested
        if self.config.get("output", {}).get("save_intermediate", True):
            self._save_production_output(result)
        
        return result
    
    def _save_production_output(self, production: Dict[str, Any]):
        """Save production output to files."""
        output_path = self.config.get("output", {}).get("base_path", "output")
        os.makedirs(output_path, exist_ok=True)
        
        production_id = production.get("start_time", "production").replace(":", "-")
        output_file = os.path.join(output_path, f"production_{production_id}.json")
        
        self.coordinator.export_production(production, output_file)
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get learning system summary."""
        return self.coordinator.get_learning_summary()
    
    def get_style_recommendations(self, genre: str) -> Dict[str, Any]:
        """Get style recommendations for a genre."""
        return self.coordinator.get_style_recommendations(genre)
    
    def get_production_status(self) -> Dict[str, Any]:
        """Get current production status."""
        return self.coordinator.get_production_status()
    
    def set_language(self, language_code: str) -> bool:
        """
        Set the system language for future productions.
        
        Args:
            language_code: ISO 639-1 language code (e.g., 'en', 'es', 'ja')
            
        Returns:
            True if successful, False otherwise
        """
        return self.language_manager.set_language(language_code)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get all supported languages.
        
        Returns:
            Dictionary mapping language codes to display names
        """
        return self.language_manager.list_available_languages()
    
    def get_current_language(self) -> str:
        """Get the currently set language code."""
        return self.language_manager.get_current_language()


def main():
    """Main entry point for the application."""
    print("\n" + "="*60)
    print("🎬 Welcome to AnimAIverse - NextGenAI Animation System 🎬")
    print("="*60)
    print("\nAn advanced multi-agent system for creating full animated series")
    print("with precision and creativity.")
    print("Supports multiple languages - Primary language: English\n")
    
    # Initialize system
    animai = AnimAIverse()
    
    # Display supported languages
    print("\n" + "="*60)
    print("🌍 Supported Languages")
    print("="*60)
    languages = animai.get_supported_languages()
    for code, name in list(languages.items())[:6]:
        print(f"  • {name} ({code})")
    print(f"  ... and {len(languages) - 6} more")
    
    # Example production in English
    print("\n" + "="*60)
    print("🎯 Creating Example Animation (English)")
    print("="*60)
    
    result = animai.create_animation(
        genre="action",
        theme="A hero's journey to save the world",
        characters=["Phoenix - The Hero", "Luna - The Guide", "Shadow - The Villain"],
        duration=3,
        style_preferences={
            "visual_style": "cinematic",
            "animation_style": "dynamic",
            "color_grading": "high_contrast"
        },
        language="en"  # English
    )
    
    # Display summary
    if result.get("status") == "completed":
        print("\n" + "="*60)
        print("📊 Production Summary")
        print("="*60)
        
        final_edit = result.get("results", {}).get("final_edit", {})
        quality_report = final_edit.get("quality_report", {})
        
        print(f"Status: ✅ {result.get('status').upper()}")
        print(f"Duration: {result.get('duration_seconds', 0):.2f} seconds")
        print(f"Quality Score: {quality_report.get('metrics', {}).get('overall_score', 0):.2f}/1.0")
        print(f"Scenes: {final_edit.get('metadata', {}).get('scene_count', 0)}")
        print(f"Total Animation Length: {final_edit.get('metadata', {}).get('total_duration', 0)} minutes")
        
        # Learning summary
        print("\n" + "="*60)
        print("🧠 Learning System Summary")
        print("="*60)
        
        learning_summary = animai.get_learning_summary()
        print(f"Total Productions: {learning_summary.get('total_productions', 0)}")
        print(f"Average Quality: {learning_summary.get('average_quality', 0):.2f}")
        print(f"Improvement Trend: {learning_summary.get('improvement_trend', 'N/A')}")
        
        print("\n" + "="*60)
        print("✅ Example completed successfully!")
        print("="*60 + "\n")
    else:
        print(f"\n❌ Production failed: {result.get('error', 'Unknown error')}\n")
    
    # Interactive mode prompt
    print("\n💡 Multi-Language Usage Examples:")
    print("   # English (default)")
    print("   result = animai.create_animation(genre='action', language='en')")
    print()
    print("   # Spanish")
    print("   result = animai.create_animation(genre='drama', language='es')")
    print()
    print("   # Japanese")
    print("   result = animai.create_animation(genre='adventure', language='ja')")
    print()
    print("   # Get supported languages")
    print("   languages = animai.get_supported_languages()")
    print()


if __name__ == "__main__":
    main()
