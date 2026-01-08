"""
ANIMA System - Complete Token Integration
Main interface for the ANIMA token ecosystem
"""
from typing import Dict, Any, Optional
from .token_manager import TokenManager
from .staking_system import StakingSystem, StakingTier
from .governance import GovernanceSystem, ProposalType
from .access_control import AccessControl
from .priority_coordinator import TokenIntegratedCoordinator


class ANIMASystem:
    """
    Main ANIMA token system interface.
    
    ANIMA - The Bitcoin of Animation
    Decentralized Creativity, Powered by AI
    """
    
    def __init__(self, base_coordinator, data_dir: str = "token"):
        """
        Initialize the complete ANIMA system.
        
        Args:
            base_coordinator: The base WorkflowCoordinator
            data_dir: Directory for token data storage
        """
        print("\n" + "="*60)
        print("🪙  INITIALIZING ANIMA TOKEN SYSTEM")
        print("    The Bitcoin of Animation")
        print("    Decentralized Creativity, Powered by AI")
        print("="*60)
        
        # Initialize core components
        self.token_manager = TokenManager(f"{data_dir}/token_data.json")
        print("✓ Token Manager initialized")
        print(f"   Total Supply: {self.token_manager.TOTAL_SUPPLY:,} ANM")
        
        self.staking_system = StakingSystem(self.token_manager, f"{data_dir}/staking_data.json")
        print("✓ Staking System initialized")
        print(f"   Tiers: {', '.join([t.value for t in StakingTier])}")
        
        self.governance = GovernanceSystem(self.staking_system, f"{data_dir}/governance_data.json")
        print("✓ Governance System initialized")
        print(f"   Voting period: {self.governance.VOTING_PERIOD_DAYS} days")
        
        self.access_control = AccessControl(self.staking_system)
        print("✓ Access Control initialized")
        
        self.coordinator = TokenIntegratedCoordinator(
            base_coordinator,
            self.token_manager,
            self.staking_system,
            self.access_control
        )
        print("✓ Priority Coordinator initialized")
        
        # Display token info
        token_info = self.token_manager.get_token_info()
        print("\n📊 Token Statistics:")
        print(f"   Circulating Supply: {token_info['circulating_supply']:,} ANM")
        print(f"   Burned Supply: {token_info['burned_supply']:,} ANM")
        print(f"   Total Holders: {token_info['total_holders']}")
        
        print("\n" + "="*60)
        print("✅ ANIMA SYSTEM READY")
        print("="*60 + "\n")
    
    # ==================== TOKEN OPERATIONS ====================
    
    def get_balance(self, user_id: str) -> float:
        """Get user's token balance."""
        return self.token_manager.get_balance(user_id)
    
    def transfer_tokens(self, from_user: str, to_user: str, amount: float) -> Dict[str, Any]:
        """Transfer tokens between users."""
        return self.token_manager.transfer(from_user, to_user, amount)
    
    def mint_tokens(self, user_id: str, amount: float, reason: str = "allocation") -> Dict[str, Any]:
        """Mint tokens for a user (admin function)."""
        return self.token_manager.mint_tokens(user_id, amount, reason)
    
    def get_token_info(self) -> Dict[str, Any]:
        """Get token system information."""
        return self.token_manager.get_token_info()
    
    # ==================== STAKING OPERATIONS ====================
    
    def stake(self, user_id: str, amount: float) -> Dict[str, Any]:
        """Stake tokens."""
        return self.staking_system.stake_tokens(user_id, amount)
    
    def unstake(self, user_id: str, amount: float) -> Dict[str, Any]:
        """Unstake tokens."""
        return self.staking_system.unstake_tokens(user_id, amount)
    
    def claim_rewards(self, user_id: str) -> Dict[str, Any]:
        """Claim staking rewards."""
        return self.staking_system.claim_rewards(user_id)
    
    def get_staking_info(self, user_id: str) -> Dict[str, Any]:
        """Get user's staking information."""
        return self.staking_system.get_staking_info(user_id)
    
    def get_user_tier(self, user_id: str) -> StakingTier:
        """Get user's staking tier."""
        return self.staking_system.get_user_tier(user_id)
    
    # ==================== GOVERNANCE OPERATIONS ====================
    
    def create_proposal(
        self,
        user_id: str,
        title: str,
        description: str,
        proposal_type: ProposalType,
        proposal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a governance proposal."""
        return self.governance.create_proposal(
            user_id, title, description, proposal_type, proposal_data
        )
    
    def vote(self, user_id: str, proposal_id: str, vote_for: bool) -> Dict[str, Any]:
        """Vote on a proposal."""
        return self.governance.vote(user_id, proposal_id, vote_for)
    
    def get_proposal_status(self, proposal_id: str) -> Dict[str, Any]:
        """Get proposal status."""
        return self.governance.get_proposal_status(proposal_id)
    
    def get_active_proposals(self) -> list:
        """Get all active proposals."""
        return self.governance.get_active_proposals()
    
    def execute_proposal(self, proposal_id: str, executor_id: str) -> Dict[str, Any]:
        """Execute a passed proposal."""
        return self.governance.execute_proposal(proposal_id, executor_id)
    
    # ==================== ACCESS & PRODUCTION ====================
    
    def check_access(self, user_id: str, feature: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Check if user has access to a feature."""
        return self.access_control.check_access(user_id, feature, params)
    
    def get_feature_access_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's feature access."""
        return self.access_control.get_feature_access_summary(user_id)
    
    def submit_production(self, user_id: str, production_request: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a production request."""
        return self.coordinator.submit_production(user_id, production_request)
    
    def process_next_job(self) -> Optional[Dict[str, Any]]:
        """Process next job in queue."""
        return self.coordinator.process_next_job()
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status."""
        return self.coordinator.get_job_status(job_id)
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return self.coordinator.get_queue_stats()
    
    # ==================== USER DASHBOARD ====================
    
    def get_user_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user dashboard."""
        balance = self.get_balance(user_id)
        staking_info = self.get_staking_info(user_id)
        feature_access = self.get_feature_access_summary(user_id)
        user_jobs = self.coordinator.get_user_jobs(user_id)
        user_votes = self.governance.get_user_votes(user_id)
        
        return {
            "user_id": user_id,
            "wallet": {
                "balance": balance,
                "staked": staking_info["staked"],
                "total_value": balance + staking_info["staked"],
                "pending_rewards": staking_info["pending_rewards"]
            },
            "tier": {
                "current": staking_info["tier"],
                "priority_score": staking_info["priority_score"],
                "next_tier": staking_info.get("next_tier")
            },
            "features": feature_access["features"],
            "activity": {
                "total_productions": len(user_jobs),
                "active_productions": len([j for j in user_jobs if j["status"] in ["queued", "processing"]]),
                "completed_productions": len([j for j in user_jobs if j["status"] == "completed"]),
                "total_votes": len(user_votes)
            },
            "rewards": {
                "total_staking_rewards": staking_info["total_rewards_earned"],
                "apy": staking_info["apy"]
            }
        }
    
    # ==================== PLATFORM STATISTICS ====================
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get overall platform statistics."""
        token_info = self.token_manager.get_token_info()
        staking_stats = self.staking_system.get_global_staking_stats()
        governance_stats = self.governance.get_governance_stats()
        queue_stats = self.coordinator.get_queue_stats()
        
        return {
            "token": {
                "total_supply": token_info["total_supply"],
                "circulating_supply": token_info["circulating_supply"],
                "burned_supply": token_info["total_burned"],
                "deflation_rate": token_info["deflation_rate"],
                "total_holders": token_info["total_holders"],
                "treasury_balance": token_info["treasury_balance"]
            },
            "staking": {
                "total_staked": staking_stats["total_staked"],
                "staking_percentage": (staking_stats["total_staked"] / token_info["circulating_supply"] * 100) if token_info["circulating_supply"] > 0 else 0,
                "total_stakers": staking_stats["total_stakers"],
                "tier_distribution": staking_stats["tier_distribution"]
            },
            "governance": {
                "total_proposals": governance_stats["total_proposals"],
                "executed_proposals": governance_stats["executed_proposals"],
                "active_proposals": len(self.get_active_proposals()),
                "total_votes": governance_stats["total_votes_cast"]
            },
            "production": {
                "queued_jobs": queue_stats["queued_jobs"],
                "active_jobs": queue_stats["active_jobs"],
                "completed_jobs": queue_stats["completed_jobs"],
                "total_jobs": queue_stats["total_jobs_processed"]
            }
        }
    
    def print_platform_overview(self):
        """Print a beautiful overview of the platform."""
        stats = self.get_platform_stats()
        
        print("\n" + "="*70)
        print("🪙  ANIMA PLATFORM OVERVIEW")
        print("="*70)
        
        print("\n💰 TOKEN ECONOMICS:")
        print(f"   Total Supply:       {stats['token']['total_supply']:>15,} ANM")
        print(f"   Circulating:        {stats['token']['circulating_supply']:>15,} ANM")
        print(f"   Burned (Deflationary): {stats['token']['burned_supply']:>12,.2f} ANM ({stats['token']['deflation_rate']:.3f}%)")
        print(f"   Treasury:           {stats['token']['treasury_balance']:>15,.2f} ANM")
        print(f"   Total Holders:      {stats['token']['total_holders']:>15,}")
        
        print("\n📈 STAKING:")
        print(f"   Total Staked:       {stats['staking']['total_staked']:>15,.2f} ANM ({stats['staking']['staking_percentage']:.1f}%)")
        print(f"   Total Stakers:      {stats['staking']['total_stakers']:>15,}")
        print(f"   Tier Distribution:")
        for tier, count in stats['staking']['tier_distribution'].items():
            print(f"      {tier.capitalize():12} {count:>3,} users")
        
        print("\n🗳️  GOVERNANCE:")
        print(f"   Total Proposals:    {stats['governance']['total_proposals']:>15,}")
        print(f"   Executed:           {stats['governance']['executed_proposals']:>15,}")
        print(f"   Active:             {stats['governance']['active_proposals']:>15,}")
        print(f"   Total Votes Cast:   {stats['governance']['total_votes']:>15,}")
        
        print("\n🎬 PRODUCTION QUEUE:")
        print(f"   Queued Jobs:        {stats['production']['queued_jobs']:>15,}")
        print(f"   Active Jobs:        {stats['production']['active_jobs']:>15,}")
        print(f"   Completed:          {stats['production']['completed_jobs']:>15,}")
        print(f"   Total Processed:    {stats['production']['total_jobs']:>15,}")
        
        print("\n" + "="*70 + "\n")
