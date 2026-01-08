"""
ANIMA Governance System
Community voting and platform evolution management
"""
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum


class ProposalType(Enum):
    """Types of governance proposals."""
    NEW_AGENT = "new_agent"
    AGENT_UPGRADE = "agent_upgrade"
    STYLE_PACK = "style_pack"
    FEATURE = "feature"
    PARAMETER = "parameter"
    TREASURY = "treasury"
    ECOSYSTEM = "ecosystem"


class ProposalStatus(Enum):
    """Status of proposals."""
    DRAFT = "draft"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    EXPIRED = "expired"


class GovernanceSystem:
    """Manages community governance and voting."""
    
    # Voting configuration
    VOTING_PERIOD_DAYS = 7
    QUORUM_PERCENTAGE = 0.10  # 10% of staked tokens must vote
    APPROVAL_THRESHOLD = 0.66  # 66% approval needed
    MIN_STAKE_TO_PROPOSE = 100  # Minimum ANM staked to create proposal
    
    def __init__(self, staking_system, data_path: str = "token/governance_data.json"):
        """Initialize the governance system."""
        self.staking_system = staking_system
        self.data_path = data_path
        self.governance_data = self._load_or_initialize_data()
    
    def _load_or_initialize_data(self) -> Dict[str, Any]:
        """Load existing governance data or initialize new system."""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)
        else:
            initial_data = {
                "proposals": {},  # proposal_id: proposal_data
                "votes": {},      # proposal_id: {user_id: vote_data}
                "executed_proposals": [],
                "proposal_counter": 0
            }
            self._save_data(initial_data)
            return initial_data
    
    def _save_data(self, data: Optional[Dict[str, Any]] = None):
        """Save governance data to file."""
        if data is None:
            data = self.governance_data
        
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_proposal(
        self,
        user_id: str,
        title: str,
        description: str,
        proposal_type: ProposalType,
        proposal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new governance proposal.
        
        Args:
            user_id: Proposer's user ID
            title: Proposal title
            description: Detailed description
            proposal_type: Type of proposal
            proposal_data: Specific data for the proposal type
            
        Returns:
            Created proposal information
        """
        # Check if user has enough stake to propose
        staking_info = self.staking_system.get_staking_info(user_id)
        if staking_info["staked"] < self.MIN_STAKE_TO_PROPOSE:
            return {
                "success": False,
                "error": f"Minimum {self.MIN_STAKE_TO_PROPOSE} ANM stake required to propose",
                "current_stake": staking_info["staked"]
            }
        
        # Generate proposal ID
        self.governance_data["proposal_counter"] += 1
        proposal_id = f"PROP-{self.governance_data['proposal_counter']:04d}"
        
        # Create proposal
        proposal = {
            "id": proposal_id,
            "proposer": user_id,
            "title": title,
            "description": description,
            "type": proposal_type.value,
            "data": proposal_data,
            "status": ProposalStatus.ACTIVE.value,
            "created_at": datetime.now().isoformat(),
            "voting_ends": (datetime.now() + timedelta(days=self.VOTING_PERIOD_DAYS)).isoformat(),
            "votes_for": 0,
            "votes_against": 0,
            "voting_power_for": 0,
            "voting_power_against": 0,
            "total_voters": 0
        }
        
        self.governance_data["proposals"][proposal_id] = proposal
        self.governance_data["votes"][proposal_id] = {}
        self._save_data()
        
        return {
            "success": True,
            "proposal": proposal,
            "message": f"Proposal {proposal_id} created successfully"
        }
    
    def vote(self, user_id: str, proposal_id: str, vote_for: bool) -> Dict[str, Any]:
        """
        Vote on a proposal.
        
        Args:
            user_id: Voter's user ID
            proposal_id: Proposal to vote on
            vote_for: True to vote for, False to vote against
            
        Returns:
            Voting result
        """
        # Check if proposal exists
        if proposal_id not in self.governance_data["proposals"]:
            return {
                "success": False,
                "error": "Proposal not found"
            }
        
        proposal = self.governance_data["proposals"][proposal_id]
        
        # Check if voting is still active
        if proposal["status"] != ProposalStatus.ACTIVE.value:
            return {
                "success": False,
                "error": f"Voting is closed. Proposal status: {proposal['status']}"
            }
        
        # Check if voting period has ended
        if datetime.now() > datetime.fromisoformat(proposal["voting_ends"]):
            self._finalize_proposal(proposal_id)
            return {
                "success": False,
                "error": "Voting period has ended"
            }
        
        # Get user's voting power (based on staked amount)
        staking_info = self.staking_system.get_staking_info(user_id)
        voting_power = staking_info["staked"]
        
        if voting_power <= 0:
            return {
                "success": False,
                "error": "No staked tokens. Stake ANM to vote."
            }
        
        # Check if user has already voted
        proposal_votes = self.governance_data["votes"][proposal_id]
        if user_id in proposal_votes:
            # Update existing vote
            old_vote = proposal_votes[user_id]
            old_vote_for = old_vote["vote_for"]
            old_power = old_vote["voting_power"]
            
            # Remove old vote
            if old_vote_for:
                proposal["votes_for"] -= 1
                proposal["voting_power_for"] -= old_power
            else:
                proposal["votes_against"] -= 1
                proposal["voting_power_against"] -= old_power
            
            message = "Vote updated"
        else:
            message = "Vote recorded"
            proposal["total_voters"] += 1
        
        # Record new vote
        vote_data = {
            "user": user_id,
            "vote_for": vote_for,
            "voting_power": voting_power,
            "timestamp": datetime.now().isoformat()
        }
        proposal_votes[user_id] = vote_data
        
        # Update proposal vote counts
        if vote_for:
            proposal["votes_for"] += 1
            proposal["voting_power_for"] += voting_power
        else:
            proposal["votes_against"] += 1
            proposal["voting_power_against"] += voting_power
        
        self._save_data()
        
        return {
            "success": True,
            "message": message,
            "vote": vote_data,
            "proposal_status": self.get_proposal_status(proposal_id)
        }
    
    def _finalize_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """Finalize a proposal after voting period ends."""
        proposal = self.governance_data["proposals"][proposal_id]
        
        # Calculate results
        total_voting_power = proposal["voting_power_for"] + proposal["voting_power_against"]
        total_staked = self.staking_system.staking_data["total_staked"]
        
        # Check quorum
        quorum_reached = (total_voting_power / total_staked) >= self.QUORUM_PERCENTAGE if total_staked > 0 else False
        
        # Check approval threshold
        approval_rate = (proposal["voting_power_for"] / total_voting_power) if total_voting_power > 0 else 0
        approved = approval_rate >= self.APPROVAL_THRESHOLD
        
        # Update proposal status
        if quorum_reached and approved:
            proposal["status"] = ProposalStatus.PASSED.value
        elif not quorum_reached:
            proposal["status"] = ProposalStatus.EXPIRED.value
        else:
            proposal["status"] = ProposalStatus.REJECTED.value
        
        proposal["finalized_at"] = datetime.now().isoformat()
        proposal["results"] = {
            "quorum_reached": quorum_reached,
            "approval_rate": approval_rate,
            "total_voting_power": total_voting_power,
            "quorum_percentage": (total_voting_power / total_staked) * 100 if total_staked > 0 else 0
        }
        
        self._save_data()
        
        return {
            "proposal_id": proposal_id,
            "status": proposal["status"],
            "results": proposal["results"]
        }
    
    def execute_proposal(self, proposal_id: str, executor_id: str) -> Dict[str, Any]:
        """
        Execute a passed proposal.
        
        Args:
            proposal_id: Proposal to execute
            executor_id: User executing the proposal
            
        Returns:
            Execution result
        """
        if proposal_id not in self.governance_data["proposals"]:
            return {
                "success": False,
                "error": "Proposal not found"
            }
        
        proposal = self.governance_data["proposals"][proposal_id]
        
        # Check if proposal passed
        if proposal["status"] != ProposalStatus.PASSED.value:
            return {
                "success": False,
                "error": f"Cannot execute proposal with status: {proposal['status']}"
            }
        
        # Execute based on proposal type
        execution_result = self._execute_proposal_action(proposal)
        
        # Update proposal status
        proposal["status"] = ProposalStatus.EXECUTED.value
        proposal["executed_at"] = datetime.now().isoformat()
        proposal["executed_by"] = executor_id
        proposal["execution_result"] = execution_result
        
        # Add to executed proposals
        self.governance_data["executed_proposals"].append({
            "proposal_id": proposal_id,
            "executed_at": proposal["executed_at"],
            "type": proposal["type"],
            "title": proposal["title"]
        })
        
        self._save_data()
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "execution_result": execution_result,
            "message": f"Proposal {proposal_id} executed successfully"
        }
    
    def _execute_proposal_action(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual proposal action."""
        proposal_type = ProposalType(proposal["type"])
        proposal_data = proposal["data"]
        
        # Placeholder execution logic - to be implemented based on specific needs
        if proposal_type == ProposalType.NEW_AGENT:
            return {
                "action": "new_agent_added",
                "agent_name": proposal_data.get("agent_name"),
                "agent_type": proposal_data.get("agent_type"),
                "status": "pending_implementation"
            }
        
        elif proposal_type == ProposalType.STYLE_PACK:
            return {
                "action": "style_pack_added",
                "pack_name": proposal_data.get("pack_name"),
                "styles": proposal_data.get("styles", []),
                "status": "pending_implementation"
            }
        
        elif proposal_type == ProposalType.PARAMETER:
            return {
                "action": "parameter_updated",
                "parameter": proposal_data.get("parameter"),
                "old_value": proposal_data.get("old_value"),
                "new_value": proposal_data.get("new_value"),
                "status": "updated"
            }
        
        elif proposal_type == ProposalType.TREASURY:
            return {
                "action": "treasury_allocation",
                "amount": proposal_data.get("amount"),
                "recipient": proposal_data.get("recipient"),
                "purpose": proposal_data.get("purpose"),
                "status": "pending_transfer"
            }
        
        else:
            return {
                "action": "generic_execution",
                "status": "pending_implementation"
            }
    
    def get_proposal_status(self, proposal_id: str) -> Dict[str, Any]:
        """Get detailed status of a proposal."""
        if proposal_id not in self.governance_data["proposals"]:
            return {"error": "Proposal not found"}
        
        proposal = self.governance_data["proposals"][proposal_id]
        
        # Check if voting period has ended but not finalized
        if (proposal["status"] == ProposalStatus.ACTIVE.value and 
            datetime.now() > datetime.fromisoformat(proposal["voting_ends"])):
            self._finalize_proposal(proposal_id)
            proposal = self.governance_data["proposals"][proposal_id]
        
        total_voting_power = proposal["voting_power_for"] + proposal["voting_power_against"]
        total_staked = self.staking_system.staking_data["total_staked"]
        
        return {
            "proposal": proposal,
            "voting_stats": {
                "votes_for": proposal["votes_for"],
                "votes_against": proposal["votes_against"],
                "voting_power_for": proposal["voting_power_for"],
                "voting_power_against": proposal["voting_power_against"],
                "total_voters": proposal["total_voters"],
                "total_voting_power": total_voting_power,
                "approval_rate": (proposal["voting_power_for"] / total_voting_power * 100) if total_voting_power > 0 else 0,
                "quorum_progress": (total_voting_power / total_staked * 100) if total_staked > 0 else 0,
                "quorum_required": self.QUORUM_PERCENTAGE * 100,
                "approval_required": self.APPROVAL_THRESHOLD * 100
            },
            "time_remaining": self._calculate_time_remaining(proposal["voting_ends"]) if proposal["status"] == ProposalStatus.ACTIVE.value else None
        }
    
    def _calculate_time_remaining(self, voting_ends: str) -> str:
        """Calculate time remaining for voting."""
        end_time = datetime.fromisoformat(voting_ends)
        remaining = end_time - datetime.now()
        
        if remaining.total_seconds() < 0:
            return "Ended"
        
        days = remaining.days
        hours = remaining.seconds // 3600
        
        if days > 0:
            return f"{days} day{'s' if days != 1 else ''} {hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''}"
    
    def get_active_proposals(self) -> List[Dict[str, Any]]:
        """Get all active proposals."""
        active = []
        for proposal_id, proposal in self.governance_data["proposals"].items():
            if proposal["status"] == ProposalStatus.ACTIVE.value:
                # Check if still active
                if datetime.now() <= datetime.fromisoformat(proposal["voting_ends"]):
                    active.append(self.get_proposal_status(proposal_id))
                else:
                    self._finalize_proposal(proposal_id)
        
        return active
    
    def get_user_votes(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all votes cast by a user."""
        user_votes = []
        
        for proposal_id, votes in self.governance_data["votes"].items():
            if user_id in votes:
                vote_data = votes[user_id]
                proposal = self.governance_data["proposals"][proposal_id]
                
                user_votes.append({
                    "proposal_id": proposal_id,
                    "proposal_title": proposal["title"],
                    "proposal_type": proposal["type"],
                    "vote_for": vote_data["vote_for"],
                    "voting_power": vote_data["voting_power"],
                    "timestamp": vote_data["timestamp"],
                    "proposal_status": proposal["status"]
                })
        
        return user_votes
    
    def get_governance_stats(self) -> Dict[str, Any]:
        """Get overall governance statistics."""
        proposals = self.governance_data["proposals"]
        
        status_counts = {}
        for status in ProposalStatus:
            status_counts[status.value] = sum(
                1 for p in proposals.values() if p["status"] == status.value
            )
        
        type_counts = {}
        for ptype in ProposalType:
            type_counts[ptype.value] = sum(
                1 for p in proposals.values() if p["type"] == ptype.value
            )
        
        return {
            "total_proposals": len(proposals),
            "executed_proposals": len(self.governance_data["executed_proposals"]),
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "total_votes_cast": sum(
                len(votes) for votes in self.governance_data["votes"].values()
            ),
            "governance_config": {
                "voting_period_days": self.VOTING_PERIOD_DAYS,
                "quorum_percentage": f"{self.QUORUM_PERCENTAGE * 100}%",
                "approval_threshold": f"{self.APPROVAL_THRESHOLD * 100}%",
                "min_stake_to_propose": self.MIN_STAKE_TO_PROPOSE
            }
        }
