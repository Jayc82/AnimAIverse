"""
ANIMA - The Bitcoin of Animation
Decentralized Creativity, Powered by AI

Main application interface with full token integration
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
from agents.graphics_agent import GraphicsAgent
from agents.character_generator_agent import CharacterGeneratorAgent
from agents.voice_agent import VoiceAgent
from agents.special_effects_agent import SpecialEffectsAgent
from memory.style_memory import StyleMemory
from memory.continuous_learning import ContinuousLearning
from workflows.coordinator import WorkflowCoordinator
from utils.language_manager import LanguageManager
from token.anima_system import ANIMASystem


class AnimAIverseANIMA:
    """
    ANIMA-integrated AnimAIverse system.
    
    The Bitcoin of Animation - Decentralized, Token-Gated, Community-Governed
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the ANIMA-integrated AnimAIverse system."""
        print("\n" + "🌟"*30)
        print("🎬 ANIMA - THE BITCOIN OF ANIMATION")
        print("   Decentralized Creativity, Powered by AI")
        print("🌟"*30 + "\n")
        
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
        
        # Initialize adaptive learning system
        from memory.adaptive_learning_system import AdaptiveLearningSystem
        self.adaptive_learning = AdaptiveLearningSystem(
            self.config.get("memory", {}).get("adaptive_learning_path", "memory/adaptive_learning.json")
        )
        print("✓ Adaptive learning system initialized")
        
        # Initialize workflow coordinator (base, non-token version)
        self.base_coordinator = WorkflowCoordinator(
            self.config,
            self.style_memory,
            self.continuous_learning
        )
        print("✓ Base workflow coordinator initialized")
        
        # Initialize and register agents
        self._initialize_agents()
        print("✓ All agents initialized and registered")
        
        # Initialize ANIMA token system
        self.anima = ANIMASystem(self.base_coordinator)
        
        print("\n" + "="*60)
        print("✅ ANIMA SYSTEM FULLY OPERATIONAL")
        print(f"   Supported languages: {', '.join(self.language_manager.get_supported_languages()[:5])}...")
        print(f"   🧠 Adaptive Learning: Generation {self.adaptive_learning.adaptive_data['evolution_generation']}")
        print(f"   🪙  Token System: LIVE")
        print("="*60 + "\n")
    
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
                "writer": {"enabled": True},
                "director": {"enabled": True},
                "animator": {"enabled": True},
                "character_generator": {"enabled": True},
                "graphics": {"enabled": True},
                "voice": {"enabled": True},
                "special_effects": {"enabled": True},
                "scene_composer": {"enabled": True},
                "editor": {"enabled": True}
            },
            "memory": {
                "style_memory_path": "memory/style_memory.json",
                "learning_history_path": "memory/learning_history.json",
                "adaptive_learning_path": "memory/adaptive_learning.json"
            }
        }
    
    def _initialize_agents(self):
        """Initialize and register all agents."""
        agents_config = self.config.get("agents", {})
        
        # Character Generator Agent
        if agents_config.get("character_generator", {}).get("enabled", True):
            char_gen_agent = CharacterGeneratorAgent(self.config)
            self.base_coordinator.register_agent("CharacterGenerator", char_gen_agent)
        
        # Graphics Agent
        if agents_config.get("graphics", {}).get("enabled", True):
            graphics_agent = GraphicsAgent(self.config)
            self.base_coordinator.register_agent("Graphics", graphics_agent)
        
        # Writer Agent
        if agents_config.get("writer", {}).get("enabled", True):
            writer_agent = WriterAgent(self.config)
            self.base_coordinator.register_agent("Writer", writer_agent)
        
        # Director Agent
        if agents_config.get("director", {}).get("enabled", True):
            director_agent = DirectorAgent(self.config)
            self.base_coordinator.register_agent("Director", director_agent)
        
        # Animator Agent
        if agents_config.get("animator", {}).get("enabled", True):
            animator_agent = AnimatorAgent(self.config)
            self.base_coordinator.register_agent("Animator", animator_agent)
        
        # Voice Agent
        if agents_config.get("voice", {}).get("enabled", True):
            voice_agent = VoiceAgent(self.config)
            self.base_coordinator.register_agent("Voice", voice_agent)
        
        # Special Effects Agent
        if agents_config.get("special_effects", {}).get("enabled", True):
            vfx_agent = SpecialEffectsAgent(self.config)
            self.base_coordinator.register_agent("SpecialEffects", vfx_agent)
        
        # Scene Composer Agent
        if agents_config.get("scene_composer", {}).get("enabled", True):
            composer_agent = SceneComposerAgent(self.config)
            self.base_coordinator.register_agent("SceneComposer", composer_agent)
        
        # Editor Agent
        if agents_config.get("editor", {}).get("enabled", True):
            editor_agent = EditorAgent(self.config)
            self.base_coordinator.register_agent("Editor", editor_agent)
    
    # ==================== USER ONBOARDING ====================
    
    def onboard_user(self, user_id: str, initial_tokens: float = 100.0) -> Dict[str, Any]:
        """
        Onboard a new user with initial token allocation.
        
        Args:
            user_id: User's identifier
            initial_tokens: Initial token grant (default 100 ANM)
            
        Returns:
            Onboarding result with wallet and tier info
        """
        print(f"\n{'='*60}")
        print(f"👤 ONBOARDING USER: {user_id}")
        print(f"{'='*60}")
        
        # Mint initial tokens
        mint_result = self.anima.mint_tokens(user_id, initial_tokens, "user_onboarding")
        
        if not mint_result["success"]:
            return {
                "success": False,
                "error": "Failed to mint tokens"
            }
        
        print(f"✓ Minted {initial_tokens} ANM")
        
        # Get user dashboard
        dashboard = self.anima.get_user_dashboard(user_id)
        
        print(f"✓ Balance: {dashboard['wallet']['balance']} ANM")
        print(f"✓ Tier: {dashboard['tier']['current']}")
        print(f"\n{'='*60}\n")
        
        return {
            "success": True,
            "user_id": user_id,
            "initial_balance": initial_tokens,
            "dashboard": dashboard
        }
    
    # ==================== PRODUCTION WORKFLOW ====================
    
    def create_animation(
        self,
        user_id: str,
        genre: str = "action",
        theme: str = "Epic adventure",
        characters: list = None,
        duration: int = 5,
        resolution: str = "1080p",
        fps: int = 30,
        style: str = "cinematic"
    ) -> Dict[str, Any]:
        """
        Create an animation with token-gated access.
        
        Args:
            user_id: User's ID
            genre: Animation genre
            theme: Story theme
            characters: Character list
            duration: Duration in minutes
            resolution: Video resolution
            fps: Frames per second
            style: Animation style
            
        Returns:
            Production result
        """
        if characters is None:
            characters = ["Hero", "Companion", "Antagonist"]
        
        production_request = {
            "genre": genre,
            "theme": theme,
            "characters": characters,
            "duration": duration,
            "resolution": resolution,
            "fps": fps,
            "style": style
        }
        
        # Submit to token-integrated coordinator
        submission = self.anima.submit_production(user_id, production_request)
        
        if not submission["success"]:
            return submission
        
        # Process immediately (in production, this would be queued)
        result = self.anima.process_next_job()
        
        return {
            "success": True,
            "job_id": submission["job_id"],
            "production_result": result
        }
    
    # ==================== TOKEN OPERATIONS ====================
    
    def stake_tokens(self, user_id: str, amount: float) -> Dict[str, Any]:
        """Stake tokens to unlock features and earn rewards."""
        return self.anima.stake(user_id, amount)
    
    def unstake_tokens(self, user_id: str, amount: float) -> Dict[str, Any]:
        """Unstake tokens."""
        return self.anima.unstake(user_id, amount)
    
    def claim_rewards(self, user_id: str) -> Dict[str, Any]:
        """Claim staking rewards."""
        return self.anima.claim_rewards(user_id)
    
    def get_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get user's complete dashboard."""
        return self.anima.get_user_dashboard(user_id)
    
    # ==================== GOVERNANCE ====================
    
    def create_proposal(
        self,
        user_id: str,
        title: str,
        description: str,
        proposal_type: str,
        proposal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a governance proposal."""
        from token.governance import ProposalType
        ptype = ProposalType(proposal_type)
        return self.anima.create_proposal(user_id, title, description, ptype, proposal_data)
    
    def vote_on_proposal(self, user_id: str, proposal_id: str, vote_for: bool) -> Dict[str, Any]:
        """Vote on a governance proposal."""
        return self.anima.vote(user_id, proposal_id, vote_for)
    
    def get_active_proposals(self) -> list:
        """Get all active proposals."""
        return self.anima.get_active_proposals()
    
    # ==================== PLATFORM INFO ====================
    
    def show_platform_stats(self):
        """Display beautiful platform statistics."""
        self.anima.print_platform_overview()
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return self.anima.get_platform_stats()


def main():
    """Main entry point demonstrating ANIMA system."""
    # Initialize ANIMA system
    app = AnimAIverseANIMA()
    
    # Show platform stats
    app.show_platform_stats()
    
    # Example: Onboard a user
    print("\n📝 DEMO: User Onboarding")
    user1_result = app.onboard_user("user_alice", initial_tokens=1000.0)
    
    # Example: Stake tokens
    print("\n📝 DEMO: Staking Tokens")
    stake_result = app.stake_tokens("user_alice", 500.0)
    print(f"Staked: {stake_result['amount_staked']} ANM")
    print(f"New Tier: {stake_result['new_tier']}")
    print(f"APY: {stake_result['apy']}%")
    
    # Example: Check dashboard
    print("\n📝 DEMO: User Dashboard")
    dashboard = app.get_dashboard("user_alice")
    print(f"Balance: {dashboard['wallet']['balance']} ANM")
    print(f"Staked: {dashboard['wallet']['staked']} ANM")
    print(f"Tier: {dashboard['tier']['current']}")
    print(f"Priority Score: {dashboard['tier']['priority_score']:.2f}")
    
    # Example: Create animation
    print("\n📝 DEMO: Creating Animation")
    animation = app.create_animation(
        "user_alice",
        genre="sci-fi",
        theme="Space exploration",
        characters=["Captain", "Engineer", "Alien"],
        duration=5,
        resolution="1080p",
        fps=30,
        style="cinematic"
    )
    
    if animation["success"]:
        print(f"✅ Animation created successfully!")
        print(f"Job ID: {animation['job_id']}")
    
    # Show final stats
    print("\n" + "="*60)
    print("FINAL PLATFORM STATE")
    print("="*60)
    app.show_platform_stats()


if __name__ == "__main__":
    main()
