"""
ANIMA Staking System
Enables users to stake tokens for rewards and priority access
"""
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum


class StakingTier(Enum):
    """Staking tiers with different benefits."""
    BASIC = "basic"           # 0-100 ANM staked
    ADVANCED = "advanced"     # 100-1,000 ANM staked
    PRO = "pro"              # 1,000-10,000 ANM staked
    STUDIO = "studio"        # 10,000+ ANM staked


class StakingSystem:
    """Manages token staking and rewards."""
    
    # Staking tier thresholds
    TIER_THRESHOLDS = {
        StakingTier.BASIC: 0,
        StakingTier.ADVANCED: 100,
        StakingTier.PRO: 1_000,
        StakingTier.STUDIO: 10_000
    }
    
    # Annual percentage yields by tier
    APY_RATES = {
        StakingTier.BASIC: 0.05,      # 5% APY
        StakingTier.ADVANCED: 0.10,    # 10% APY
        StakingTier.PRO: 0.15,         # 15% APY
        StakingTier.STUDIO: 0.25       # 25% APY
    }
    
    # Priority multipliers for job execution
    PRIORITY_MULTIPLIERS = {
        StakingTier.BASIC: 1.0,
        StakingTier.ADVANCED: 2.0,
        StakingTier.PRO: 5.0,
        StakingTier.STUDIO: 10.0
    }
    
    # Feature access by tier
    TIER_FEATURES = {
        StakingTier.BASIC: {
            "max_agents_simultaneous": 2,
            "max_sequence_length": 30,  # seconds
            "max_resolution": "720p",
            "max_fps": 24,
            "style_packs": ["basic"],
            "priority_rendering": False
        },
        StakingTier.ADVANCED: {
            "max_agents_simultaneous": 5,
            "max_sequence_length": 120,  # seconds
            "max_resolution": "1080p",
            "max_fps": 30,
            "style_packs": ["basic", "cinematic", "anime"],
            "priority_rendering": True
        },
        StakingTier.PRO: {
            "max_agents_simultaneous": 10,
            "max_sequence_length": 600,  # seconds
            "max_resolution": "4K",
            "max_fps": 60,
            "style_packs": ["all"],
            "priority_rendering": True
        },
        StakingTier.STUDIO: {
            "max_agents_simultaneous": -1,  # unlimited
            "max_sequence_length": -1,      # unlimited
            "max_resolution": "8K",
            "max_fps": 120,
            "style_packs": ["all", "custom"],
            "priority_rendering": True,
            "custom_agents": True
        }
    }
    
    def __init__(self, token_manager, data_path: str = "token/staking_data.json"):
        """Initialize the staking system."""
        self.token_manager = token_manager
        self.data_path = data_path
        self.staking_data = self._load_or_initialize_data()
    
    def _load_or_initialize_data(self) -> Dict[str, Any]:
        """Load existing staking data or initialize new system."""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)
        else:
            initial_data = {
                "stakes": {},  # user_id: stake_info
                "total_staked": 0,
                "staking_pool_rewards": 0,
                "reward_history": []
            }
            self._save_data(initial_data)
            return initial_data
    
    def _save_data(self, data: Optional[Dict[str, Any]] = None):
        """Save staking data to file."""
        if data is None:
            data = self.staking_data
        
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def stake_tokens(self, user_id: str, amount: float) -> Dict[str, Any]:
        """
        Stake tokens for a user.
        
        Args:
            user_id: User's ID
            amount: Amount to stake
            
        Returns:
            Staking result
        """
        # Check balance
        balance = self.token_manager.get_balance(user_id)
        if balance < amount:
            return {
                "success": False,
                "error": "Insufficient balance",
                "balance": balance
            }
        
        # Get or create stake
        if user_id not in self.staking_data["stakes"]:
            self.staking_data["stakes"][user_id] = {
                "amount": 0,
                "start_time": datetime.now().isoformat(),
                "last_reward_claim": datetime.now().isoformat(),
                "total_rewards_earned": 0,
                "staking_history": []
            }
        
        stake = self.staking_data["stakes"][user_id]
        
        # Transfer tokens from balance to stake
        transfer_result = self.token_manager.transfer(
            user_id, 
            "staking_pool", 
            amount
        )
        
        if not transfer_result["success"]:
            return transfer_result
        
        # Update stake
        old_amount = stake["amount"]
        stake["amount"] += amount
        stake["staking_history"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "stake",
            "amount": amount,
            "total_staked": stake["amount"]
        })
        
        # Update totals
        self.staking_data["total_staked"] += amount
        self._save_data()
        
        # Calculate new tier
        new_tier = self.get_user_tier(user_id)
        old_tier = self._calculate_tier(old_amount)
        
        return {
            "success": True,
            "amount_staked": amount,
            "total_staked": stake["amount"],
            "old_tier": old_tier.value,
            "new_tier": new_tier.value,
            "tier_upgraded": new_tier.value != old_tier.value,
            "apy": self.APY_RATES[new_tier] * 100,
            "priority_multiplier": self.PRIORITY_MULTIPLIERS[new_tier]
        }
    
    def unstake_tokens(self, user_id: str, amount: float) -> Dict[str, Any]:
        """
        Unstake tokens for a user.
        
        Args:
            user_id: User's ID
            amount: Amount to unstake
            
        Returns:
            Unstaking result
        """
        if user_id not in self.staking_data["stakes"]:
            return {
                "success": False,
                "error": "No stake found"
            }
        
        stake = self.staking_data["stakes"][user_id]
        
        if stake["amount"] < amount:
            return {
                "success": False,
                "error": "Insufficient staked amount",
                "staked": stake["amount"]
            }
        
        # Claim pending rewards first
        self.claim_rewards(user_id)
        
        # Update stake
        old_amount = stake["amount"]
        stake["amount"] -= amount
        stake["staking_history"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "unstake",
            "amount": amount,
            "total_staked": stake["amount"]
        })
        
        # Transfer tokens back
        self.token_manager.transfer("staking_pool", user_id, amount)
        
        # Update totals
        self.staking_data["total_staked"] -= amount
        self._save_data()
        
        # Calculate tier change
        new_tier = self.get_user_tier(user_id)
        old_tier = self._calculate_tier(old_amount)
        
        return {
            "success": True,
            "amount_unstaked": amount,
            "remaining_staked": stake["amount"],
            "old_tier": old_tier.value,
            "new_tier": new_tier.value,
            "tier_downgraded": new_tier.value != old_tier.value
        }
    
    def claim_rewards(self, user_id: str) -> Dict[str, Any]:
        """
        Claim accumulated staking rewards.
        
        Args:
            user_id: User's ID
            
        Returns:
            Reward claim result
        """
        if user_id not in self.staking_data["stakes"]:
            return {
                "success": False,
                "error": "No stake found"
            }
        
        stake = self.staking_data["stakes"][user_id]
        rewards = self.calculate_pending_rewards(user_id)
        
        if rewards <= 0:
            return {
                "success": True,
                "rewards": 0,
                "message": "No rewards to claim"
            }
        
        # Mint rewards
        self.token_manager.mint_tokens(user_id, rewards, "staking_rewards")
        
        # Update stake
        stake["last_reward_claim"] = datetime.now().isoformat()
        stake["total_rewards_earned"] += rewards
        
        # Record reward
        reward_record = {
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "amount": rewards,
            "staked_amount": stake["amount"]
        }
        self.staking_data["reward_history"].append(reward_record)
        self._save_data()
        
        return {
            "success": True,
            "rewards": rewards,
            "total_earned": stake["total_rewards_earned"],
            "new_balance": self.token_manager.get_balance(user_id)
        }
    
    def calculate_pending_rewards(self, user_id: str) -> float:
        """Calculate pending rewards for a user."""
        if user_id not in self.staking_data["stakes"]:
            return 0.0
        
        stake = self.staking_data["stakes"][user_id]
        
        # Calculate time staked since last claim
        last_claim = datetime.fromisoformat(stake["last_reward_claim"])
        now = datetime.now()
        time_delta = now - last_claim
        hours_staked = time_delta.total_seconds() / 3600
        
        # Calculate rewards based on APY
        tier = self.get_user_tier(user_id)
        apy = self.APY_RATES[tier]
        
        # Rewards = (staked_amount * APY * time_period) / year_in_hours
        rewards = (stake["amount"] * apy * hours_staked) / (365.25 * 24)
        
        return round(rewards, self.token_manager.DECIMALS)
    
    def get_user_tier(self, user_id: str) -> StakingTier:
        """Get user's current staking tier."""
        if user_id not in self.staking_data["stakes"]:
            return StakingTier.BASIC
        
        staked_amount = self.staking_data["stakes"][user_id]["amount"]
        return self._calculate_tier(staked_amount)
    
    def _calculate_tier(self, staked_amount: float) -> StakingTier:
        """Calculate tier based on staked amount."""
        if staked_amount >= self.TIER_THRESHOLDS[StakingTier.STUDIO]:
            return StakingTier.STUDIO
        elif staked_amount >= self.TIER_THRESHOLDS[StakingTier.PRO]:
            return StakingTier.PRO
        elif staked_amount >= self.TIER_THRESHOLDS[StakingTier.ADVANCED]:
            return StakingTier.ADVANCED
        else:
            return StakingTier.BASIC
    
    def get_tier_features(self, user_id: str) -> Dict[str, Any]:
        """Get features available to user based on their tier."""
        tier = self.get_user_tier(user_id)
        return self.TIER_FEATURES[tier].copy()
    
    def get_priority_score(self, user_id: str) -> float:
        """Get user's priority score for job scheduling."""
        tier = self.get_user_tier(user_id)
        multiplier = self.PRIORITY_MULTIPLIERS[tier]
        
        if user_id not in self.staking_data["stakes"]:
            return multiplier
        
        # Priority score = base_multiplier * log(staked_amount + 1)
        staked = self.staking_data["stakes"][user_id]["amount"]
        import math
        priority_score = multiplier * math.log(staked + 1)
        
        return priority_score
    
    def get_staking_info(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive staking information for a user."""
        if user_id not in self.staking_data["stakes"]:
            return {
                "staked": 0,
                "tier": StakingTier.BASIC.value,
                "pending_rewards": 0,
                "apy": self.APY_RATES[StakingTier.BASIC] * 100,
                "features": self.TIER_FEATURES[StakingTier.BASIC],
                "priority_score": 1.0
            }
        
        tier = self.get_user_tier(user_id)
        stake = self.staking_data["stakes"][user_id]
        
        return {
            "staked": stake["amount"],
            "tier": tier.value,
            "pending_rewards": self.calculate_pending_rewards(user_id),
            "total_rewards_earned": stake["total_rewards_earned"],
            "apy": self.APY_RATES[tier] * 100,
            "start_time": stake["start_time"],
            "features": self.TIER_FEATURES[tier],
            "priority_score": self.get_priority_score(user_id),
            "next_tier": self._get_next_tier_info(stake["amount"])
        }
    
    def _get_next_tier_info(self, current_stake: float) -> Optional[Dict[str, Any]]:
        """Get information about the next tier."""
        current_tier = self._calculate_tier(current_stake)
        
        tier_order = [StakingTier.BASIC, StakingTier.ADVANCED, StakingTier.PRO, StakingTier.STUDIO]
        current_index = tier_order.index(current_tier)
        
        if current_index == len(tier_order) - 1:
            return None  # Already at highest tier
        
        next_tier = tier_order[current_index + 1]
        required = self.TIER_THRESHOLDS[next_tier]
        
        return {
            "tier": next_tier.value,
            "required_stake": required,
            "additional_needed": required - current_stake,
            "benefits": self.TIER_FEATURES[next_tier]
        }
    
    def get_global_staking_stats(self) -> Dict[str, Any]:
        """Get global staking statistics."""
        return {
            "total_staked": self.staking_data["total_staked"],
            "total_stakers": len(self.staking_data["stakes"]),
            "total_rewards_distributed": sum(
                stake["total_rewards_earned"] 
                for stake in self.staking_data["stakes"].values()
            ),
            "tier_distribution": self._get_tier_distribution()
        }
    
    def _get_tier_distribution(self) -> Dict[str, int]:
        """Get distribution of users across tiers."""
        distribution = {tier.value: 0 for tier in StakingTier}
        
        for user_id in self.staking_data["stakes"]:
            tier = self.get_user_tier(user_id)
            distribution[tier.value] += 1
        
        return distribution
