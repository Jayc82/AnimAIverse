"""
ANIMA Token Manager
Handles token operations, balances, and transactions
"""
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal


class TokenManager:
    """Manages ANIMA (ANM) token operations."""
    
    # Token configuration
    TOKEN_NAME = "ANIMA"
    TOKEN_SYMBOL = "ANM"
    TOTAL_SUPPLY = 10_000_000  # 10 million ANM
    DECIMALS = 8  # For micro-transactions
    
    # Distribution (percentages)
    COMMUNITY_ALLOCATION = 0.50  # 50% - 5,000,000 ANM
    TEAM_ALLOCATION = 0.20       # 20% - 2,000,000 ANM
    ECOSYSTEM_ALLOCATION = 0.15  # 15% - 1,500,000 ANM
    RESERVE_ALLOCATION = 0.10    # 10% - 1,000,000 ANM
    MARKETING_ALLOCATION = 0.05  # 5%  - 500,000 ANM
    
    # Transaction fees
    USAGE_FEE = 0.005  # 0.5% fee on AI usage
    BURN_PERCENTAGE = 0.60  # 60% of fees burned
    REINVEST_PERCENTAGE = 0.40  # 40% of fees reinvested
    
    def __init__(self, data_path: str = "token/token_data.json"):
        """Initialize the token manager."""
        self.data_path = data_path
        self.token_data = self._load_or_initialize_data()
        
    def _load_or_initialize_data(self) -> Dict[str, Any]:
        """Load existing token data or initialize new system."""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)
        else:
            # Initialize new token system
            initial_data = {
                "token_info": {
                    "name": self.TOKEN_NAME,
                    "symbol": self.TOKEN_SYMBOL,
                    "total_supply": self.TOTAL_SUPPLY,
                    "circulating_supply": int(self.TOTAL_SUPPLY * self.COMMUNITY_ALLOCATION),
                    "burned_supply": 0,
                    "decimals": self.DECIMALS,
                    "launch_date": datetime.now().isoformat()
                },
                "allocations": {
                    "community": int(self.TOTAL_SUPPLY * self.COMMUNITY_ALLOCATION),
                    "team": int(self.TOTAL_SUPPLY * self.TEAM_ALLOCATION),
                    "ecosystem": int(self.TOTAL_SUPPLY * self.ECOSYSTEM_ALLOCATION),
                    "reserve": int(self.TOTAL_SUPPLY * self.RESERVE_ALLOCATION),
                    "marketing": int(self.TOTAL_SUPPLY * self.MARKETING_ALLOCATION)
                },
                "balances": {},  # user_id: balance
                "transactions": [],
                "total_fees_collected": 0,
                "total_burned": 0,
                "total_reinvested": 0,
                "treasury": int(self.TOTAL_SUPPLY * self.RESERVE_ALLOCATION)
            }
            self._save_data(initial_data)
            return initial_data
    
    def _save_data(self, data: Optional[Dict[str, Any]] = None):
        """Save token data to file."""
        if data is None:
            data = self.token_data
        
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_balance(self, user_id: str) -> float:
        """Get user's token balance."""
        return self.token_data["balances"].get(user_id, 0.0)
    
    def transfer(self, from_user: str, to_user: str, amount: float) -> Dict[str, Any]:
        """
        Transfer tokens between users.
        
        Args:
            from_user: Sender's user ID
            to_user: Recipient's user ID
            amount: Amount to transfer
            
        Returns:
            Transaction result
        """
        # Validate balance
        from_balance = self.get_balance(from_user)
        if from_balance < amount:
            return {
                "success": False,
                "error": "Insufficient balance",
                "balance": from_balance
            }
        
        # Execute transfer
        self.token_data["balances"][from_user] = from_balance - amount
        self.token_data["balances"][to_user] = self.get_balance(to_user) + amount
        
        # Record transaction
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "type": "transfer",
            "from": from_user,
            "to": to_user,
            "amount": amount
        }
        self.token_data["transactions"].append(transaction)
        self._save_data()
        
        return {
            "success": True,
            "transaction": transaction,
            "new_balance": self.get_balance(from_user)
        }
    
    def charge_usage_fee(self, user_id: str, usage_cost: float) -> Dict[str, Any]:
        """
        Charge usage fee for AI operations.
        
        Args:
            user_id: User's ID
            usage_cost: Base cost of the operation
            
        Returns:
            Fee charging result with burn/reinvest breakdown
        """
        # Calculate fee
        fee = usage_cost * self.USAGE_FEE
        total_cost = usage_cost + fee
        
        # Check balance
        balance = self.get_balance(user_id)
        if balance < total_cost:
            return {
                "success": False,
                "error": "Insufficient balance",
                "required": total_cost,
                "balance": balance
            }
        
        # Deduct total cost
        self.token_data["balances"][user_id] = balance - total_cost
        
        # Calculate burn and reinvest amounts
        burn_amount = fee * self.BURN_PERCENTAGE
        reinvest_amount = fee * self.REINVEST_PERCENTAGE
        
        # Update totals
        self.token_data["total_fees_collected"] += fee
        self.token_data["total_burned"] += burn_amount
        self.token_data["total_reinvested"] += reinvest_amount
        self.token_data["token_info"]["burned_supply"] += burn_amount
        self.token_data["token_info"]["circulating_supply"] -= burn_amount
        self.token_data["treasury"] += reinvest_amount
        
        # Record transaction
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "type": "usage_fee",
            "user": user_id,
            "usage_cost": usage_cost,
            "fee": fee,
            "burned": burn_amount,
            "reinvested": reinvest_amount,
            "total_charged": total_cost
        }
        self.token_data["transactions"].append(transaction)
        self._save_data()
        
        return {
            "success": True,
            "transaction": transaction,
            "new_balance": self.get_balance(user_id),
            "deflationary_impact": {
                "burned": burn_amount,
                "reinvested": reinvest_amount
            }
        }
    
    def mint_tokens(self, user_id: str, amount: float, reason: str = "allocation") -> Dict[str, Any]:
        """
        Mint tokens for a user (only for initial distributions/rewards).
        
        Args:
            user_id: User's ID
            amount: Amount to mint
            reason: Reason for minting
            
        Returns:
            Minting result
        """
        self.token_data["balances"][user_id] = self.get_balance(user_id) + amount
        
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "type": "mint",
            "user": user_id,
            "amount": amount,
            "reason": reason
        }
        self.token_data["transactions"].append(transaction)
        self._save_data()
        
        return {
            "success": True,
            "transaction": transaction,
            "new_balance": self.get_balance(user_id)
        }
    
    def get_token_info(self) -> Dict[str, Any]:
        """Get current token information and statistics."""
        info = self.token_data["token_info"].copy()
        info.update({
            "total_fees_collected": self.token_data["total_fees_collected"],
            "total_burned": self.token_data["total_burned"],
            "total_reinvested": self.token_data["total_reinvested"],
            "treasury_balance": self.token_data["treasury"],
            "deflation_rate": (self.token_data["total_burned"] / self.TOTAL_SUPPLY) * 100,
            "total_holders": len(self.token_data["balances"])
        })
        return info
    
    def get_user_transactions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's transaction history."""
        user_txs = [
            tx for tx in self.token_data["transactions"]
            if tx.get("user") == user_id or 
               tx.get("from") == user_id or 
               tx.get("to") == user_id
        ]
        return user_txs[-limit:]
    
    def get_allocation_info(self) -> Dict[str, Any]:
        """Get token allocation information."""
        return {
            "allocations": self.token_data["allocations"],
            "percentages": {
                "community": f"{self.COMMUNITY_ALLOCATION * 100}%",
                "team": f"{self.TEAM_ALLOCATION * 100}%",
                "ecosystem": f"{self.ECOSYSTEM_ALLOCATION * 100}%",
                "reserve": f"{self.RESERVE_ALLOCATION * 100}%",
                "marketing": f"{self.MARKETING_ALLOCATION * 100}%"
            }
        }
