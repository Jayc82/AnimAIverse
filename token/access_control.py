"""
ANIMA Access Control System
Manages tiered access to platform features based on token holdings and staking
"""
from typing import Dict, Any, Optional, List
from datetime import datetime


class AccessControl:
    """Controls access to platform features based on token staking."""
    
    def __init__(self, staking_system):
        """Initialize access control with staking system."""
        self.staking_system = staking_system
        self.access_logs = []
    
    def check_access(self, user_id: str, feature: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Check if user has access to a feature.
        
        Args:
            user_id: User's ID
            feature: Feature to check access for
            params: Optional parameters (e.g., resolution, agents count)
            
        Returns:
            Access result with granted status and details
        """
        tier_features = self.staking_system.get_tier_features(user_id)
        tier = self.staking_system.get_user_tier(user_id)
        
        access_result = {
            "granted": False,
            "user_id": user_id,
            "feature": feature,
            "tier": tier.value,
            "timestamp": datetime.now().isoformat()
        }
        
        # Feature-specific access checks
        if feature == "multi_agent_orchestration":
            requested_agents = params.get("agent_count", 1) if params else 1
            max_agents = tier_features["max_agents_simultaneous"]
            
            if max_agents == -1 or requested_agents <= max_agents:
                access_result["granted"] = True
                access_result["details"] = {
                    "requested_agents": requested_agents,
                    "max_allowed": max_agents
                }
            else:
                access_result["reason"] = f"Tier allows max {max_agents} agents, requested {requested_agents}"
                access_result["upgrade_required"] = True
        
        elif feature == "high_resolution":
            requested_res = params.get("resolution", "720p") if params else "720p"
            max_res = tier_features["max_resolution"]
            
            res_hierarchy = ["720p", "1080p", "4K", "8K"]
            if res_hierarchy.index(requested_res) <= res_hierarchy.index(max_res):
                access_result["granted"] = True
                access_result["details"] = {
                    "requested_resolution": requested_res,
                    "max_allowed": max_res
                }
            else:
                access_result["reason"] = f"Tier supports up to {max_res}, requested {requested_res}"
                access_result["upgrade_required"] = True
        
        elif feature == "sequence_length":
            requested_length = params.get("length", 30) if params else 30
            max_length = tier_features["max_sequence_length"]
            
            if max_length == -1 or requested_length <= max_length:
                access_result["granted"] = True
                access_result["details"] = {
                    "requested_length": requested_length,
                    "max_allowed": max_length
                }
            else:
                access_result["reason"] = f"Tier allows max {max_length}s sequences, requested {requested_length}s"
                access_result["upgrade_required"] = True
        
        elif feature == "frame_rate":
            requested_fps = params.get("fps", 24) if params else 24
            max_fps = tier_features["max_fps"]
            
            if requested_fps <= max_fps:
                access_result["granted"] = True
                access_result["details"] = {
                    "requested_fps": requested_fps,
                    "max_allowed": max_fps
                }
            else:
                access_result["reason"] = f"Tier supports up to {max_fps} FPS, requested {requested_fps}"
                access_result["upgrade_required"] = True
        
        elif feature == "style_pack":
            requested_style = params.get("style", "basic") if params else "basic"
            available_packs = tier_features["style_packs"]
            
            if "all" in available_packs or requested_style in available_packs:
                access_result["granted"] = True
                access_result["details"] = {
                    "requested_style": requested_style,
                    "available_packs": available_packs
                }
            else:
                access_result["reason"] = f"Style '{requested_style}' not available in tier"
                access_result["upgrade_required"] = True
                access_result["available_styles"] = available_packs
        
        elif feature == "priority_rendering":
            has_priority = tier_features.get("priority_rendering", False)
            access_result["granted"] = has_priority
            if not has_priority:
                access_result["reason"] = "Priority rendering requires Advanced tier or higher"
                access_result["upgrade_required"] = True
        
        elif feature == "custom_agents":
            has_custom = tier_features.get("custom_agents", False)
            access_result["granted"] = has_custom
            if not has_custom:
                access_result["reason"] = "Custom agents require Studio tier"
                access_result["upgrade_required"] = True
        
        else:
            # Default: grant access to basic features
            access_result["granted"] = True
            access_result["details"] = {"message": "Basic feature access"}
        
        # Log access attempt
        self.access_logs.append(access_result)
        
        return access_result
    
    def validate_production_request(self, user_id: str, production_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a complete production request against user's access level.
        
        Args:
            user_id: User's ID
            production_request: Full production request parameters
            
        Returns:
            Validation result with all access checks
        """
        tier = self.staking_system.get_user_tier(user_id)
        tier_features = self.staking_system.get_tier_features(user_id)
        
        validations = {
            "user_id": user_id,
            "tier": tier.value,
            "valid": True,
            "checks": [],
            "violations": [],
            "recommendations": []
        }
        
        # Check resolution
        resolution = production_request.get("resolution", "1080p")
        res_check = self.check_access(user_id, "high_resolution", {"resolution": resolution})
        validations["checks"].append(res_check)
        if not res_check["granted"]:
            validations["valid"] = False
            validations["violations"].append(f"Resolution {resolution} not available")
        
        # Check FPS
        fps = production_request.get("fps", 30)
        fps_check = self.check_access(user_id, "frame_rate", {"fps": fps})
        validations["checks"].append(fps_check)
        if not fps_check["granted"]:
            validations["valid"] = False
            validations["violations"].append(f"FPS {fps} not available")
        
        # Check duration/sequence length
        duration = production_request.get("duration", 5) * 60  # convert minutes to seconds
        length_check = self.check_access(user_id, "sequence_length", {"length": duration})
        validations["checks"].append(length_check)
        if not length_check["granted"]:
            validations["valid"] = False
            validations["violations"].append(f"Duration {duration}s exceeds limit")
        
        # Check style pack
        style = production_request.get("style", "basic")
        style_check = self.check_access(user_id, "style_pack", {"style": style})
        validations["checks"].append(style_check)
        if not style_check["granted"]:
            validations["valid"] = False
            validations["violations"].append(f"Style '{style}' not available")
        
        # Check agent count (estimate based on production complexity)
        agent_count = self._estimate_agent_count(production_request)
        agent_check = self.check_access(user_id, "multi_agent_orchestration", {"agent_count": agent_count})
        validations["checks"].append(agent_check)
        if not agent_check["granted"]:
            validations["valid"] = False
            validations["violations"].append(f"Requires {agent_count} agents, tier allows {tier_features['max_agents_simultaneous']}")
        
        # Add upgrade recommendations if needed
        if not validations["valid"]:
            next_tier_info = self.staking_system._get_next_tier_info(
                self.staking_system.staking_data["stakes"].get(user_id, {}).get("amount", 0)
            )
            if next_tier_info:
                validations["recommendations"].append({
                    "action": "stake_more",
                    "tier": next_tier_info["tier"],
                    "additional_stake_needed": next_tier_info["additional_needed"],
                    "benefits": next_tier_info["benefits"]
                })
        
        return validations
    
    def _estimate_agent_count(self, production_request: Dict[str, Any]) -> int:
        """Estimate number of agents needed for a production."""
        # Base agents: Writer, Director, Animator, Editor
        agent_count = 4
        
        # Additional agents based on features
        if production_request.get("characters"):
            agent_count += 1  # Character Generator
        
        if production_request.get("style_preferences"):
            agent_count += 1  # Graphics Agent
        
        if production_request.get("voice_generation", True):
            agent_count += 1  # Voice Agent
        
        if production_request.get("special_effects", False):
            agent_count += 1  # Special Effects Agent
        
        if production_request.get("scenes"):
            agent_count += 1  # Scene Composer
        
        return agent_count
    
    def get_feature_access_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of all features accessible to user."""
        tier = self.staking_system.get_user_tier(user_id)
        tier_features = self.staking_system.get_tier_features(user_id)
        staking_info = self.staking_system.get_staking_info(user_id)
        
        return {
            "user_id": user_id,
            "tier": tier.value,
            "staked_amount": staking_info["staked"],
            "priority_score": staking_info["priority_score"],
            "features": {
                "agents": {
                    "max_simultaneous": tier_features["max_agents_simultaneous"],
                    "description": "Unlimited" if tier_features["max_agents_simultaneous"] == -1 else f"Up to {tier_features['max_agents_simultaneous']} agents"
                },
                "video": {
                    "max_resolution": tier_features["max_resolution"],
                    "max_fps": tier_features["max_fps"],
                    "max_sequence_length": tier_features["max_sequence_length"],
                    "description": f"{tier_features['max_resolution']} @ {tier_features['max_fps']} FPS"
                },
                "styles": {
                    "available_packs": tier_features["style_packs"],
                    "description": "All styles" if "all" in tier_features["style_packs"] else f"{len(tier_features['style_packs'])} style packs"
                },
                "rendering": {
                    "priority": tier_features["priority_rendering"],
                    "priority_multiplier": self.staking_system.PRIORITY_MULTIPLIERS[tier]
                },
                "advanced": {
                    "custom_agents": tier_features.get("custom_agents", False)
                }
            },
            "next_tier": staking_info.get("next_tier")
        }
    
    def calculate_usage_cost(self, production_request: Dict[str, Any]) -> float:
        """
        Calculate the token cost for a production request.
        
        Args:
            production_request: Production request parameters
            
        Returns:
            Estimated cost in ANM tokens
        """
        # Base cost factors
        base_cost = 10.0  # Base cost in ANM
        
        # Resolution multiplier
        res_multipliers = {
            "720p": 1.0,
            "1080p": 2.0,
            "4K": 5.0,
            "8K": 10.0
        }
        resolution = production_request.get("resolution", "1080p")
        res_multiplier = res_multipliers.get(resolution, 2.0)
        
        # FPS multiplier
        fps = production_request.get("fps", 30)
        fps_multiplier = fps / 30.0
        
        # Duration multiplier
        duration = production_request.get("duration", 5)  # in minutes
        duration_multiplier = duration / 5.0
        
        # Agent count multiplier
        agent_count = self._estimate_agent_count(production_request)
        agent_multiplier = agent_count / 5.0
        
        # Calculate total cost
        total_cost = (
            base_cost * 
            res_multiplier * 
            fps_multiplier * 
            duration_multiplier * 
            agent_multiplier
        )
        
        return round(total_cost, 2)
    
    def get_access_logs(self, user_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get access logs, optionally filtered by user."""
        if user_id:
            logs = [log for log in self.access_logs if log["user_id"] == user_id]
        else:
            logs = self.access_logs
        
        return logs[-limit:]
