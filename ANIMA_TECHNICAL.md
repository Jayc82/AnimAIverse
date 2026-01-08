# ANIMA Technical Documentation

## System Architecture

### Overview

ANIMA integrates a comprehensive token system into the AnimAIverse multi-agent animation platform. The system consists of several interconnected components:

```
┌─────────────────────────────────────────────────────────────┐
│                     ANIMA System Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Token     │  │   Staking    │  │  Governance  │      │
│  │   Manager    │←→│    System    │←→│    System    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                  ↓                  ↓              │
│  ┌──────────────┐  ┌──────────────────────────────┐        │
│  │    Access    │  │   Priority Coordinator       │        │
│  │   Control    │←→│   (Job Scheduling)           │        │
│  └──────────────┘  └──────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              AnimAIverse Core Platform                       │
│  ┌──────────────────────────────────────────────────┐       │
│  │          Workflow Coordinator                     │       │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │       │
│  │  │Writer│ │Direct│ │Animat│ │Editor│ │ ... │  │       │
│  │  │Agent │ │Agent │ │Agent │ │Agent │ │     │  │       │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Style     │  │  Continuous  │  │   Adaptive   │      │
│  │    Memory    │  │   Learning   │  │   Learning   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Token Manager (`token/token_manager.py`)

Handles all token operations, balances, and transactions.

#### Key Features:
- Total supply: 10,000,000 ANM
- 8 decimal places for micro-transactions
- Automatic fee collection and burning
- Transaction history tracking

#### Methods:

```python
class TokenManager:
    def get_balance(user_id: str) -> float
    def transfer(from_user: str, to_user: str, amount: float) -> Dict
    def charge_usage_fee(user_id: str, usage_cost: float) -> Dict
    def mint_tokens(user_id: str, amount: float, reason: str) -> Dict
    def get_token_info() -> Dict
    def get_user_transactions(user_id: str, limit: int) -> List[Dict]
```

#### Fee Structure:

```python
USAGE_FEE = 0.005  # 0.5% of usage cost
BURN_PERCENTAGE = 0.60  # 60% of fees burned
REINVEST_PERCENTAGE = 0.40  # 40% reinvested into treasury
```

---

### 2. Staking System (`token/staking_system.py`)

Manages token staking, rewards, and tier calculations.

#### Tier Thresholds:

| Tier | Min Stake | Max Agents | Resolution | FPS | APY |
|------|-----------|------------|------------|-----|-----|
| Basic | 0 ANM | 2 | 720p | 24 | 5% |
| Advanced | 100 ANM | 5 | 1080p | 30 | 10% |
| Pro | 1,000 ANM | 10 | 4K | 60 | 15% |
| Studio | 10,000 ANM | Unlimited | 8K | 120 | 25% |

#### Priority Multipliers:

```python
PRIORITY_MULTIPLIERS = {
    StakingTier.BASIC: 1.0,
    StakingTier.ADVANCED: 2.0,
    StakingTier.PRO: 5.0,
    StakingTier.STUDIO: 10.0
}
```

#### Reward Calculation:

```python
# Rewards = (staked_amount * APY * time_staked) / year_in_hours
rewards = (stake_amount * apy * hours_staked) / (365.25 * 24)
```

#### Methods:

```python
class StakingSystem:
    def stake_tokens(user_id: str, amount: float) -> Dict
    def unstake_tokens(user_id: str, amount: float) -> Dict
    def claim_rewards(user_id: str) -> Dict
    def calculate_pending_rewards(user_id: str) -> float
    def get_user_tier(user_id: str) -> StakingTier
    def get_tier_features(user_id: str) -> Dict
    def get_priority_score(user_id: str) -> float
```

---

### 3. Access Control (`token/access_control.py`)

Validates user access to features based on staking tier.

#### Feature Checks:

```python
# Check if user can use feature
access_control.check_access(
    user_id="user_alice",
    feature="high_resolution",
    params={"resolution": "4K"}
)
```

#### Validation Process:

1. Get user's staking tier
2. Retrieve tier features
3. Compare requested vs. allowed
4. Return access decision + upgrade recommendations

#### Methods:

```python
class AccessControl:
    def check_access(user_id: str, feature: str, params: Dict) -> Dict
    def validate_production_request(user_id: str, request: Dict) -> Dict
    def get_feature_access_summary(user_id: str) -> Dict
    def calculate_usage_cost(production_request: Dict) -> float
```

#### Cost Calculation:

```python
# Base cost factors
cost = base_cost * res_multiplier * fps_multiplier * 
       duration_multiplier * agent_multiplier

# Resolution multipliers: 720p=1x, 1080p=2x, 4K=5x, 8K=10x
# FPS multiplier: fps/30
# Duration multiplier: minutes/5
# Agent multiplier: agent_count/5
```

---

### 4. Governance System (`token/governance.py`)

Community-driven decision making through proposals and voting.

#### Proposal Types:

```python
class ProposalType(Enum):
    NEW_AGENT = "new_agent"
    AGENT_UPGRADE = "agent_upgrade"
    STYLE_PACK = "style_pack"
    FEATURE = "feature"
    PARAMETER = "parameter"
    TREASURY = "treasury"
    ECOSYSTEM = "ecosystem"
```

#### Governance Parameters:

```python
VOTING_PERIOD_DAYS = 7
QUORUM_PERCENTAGE = 0.10  # 10% must vote
APPROVAL_THRESHOLD = 0.66  # 66% approval needed
MIN_STAKE_TO_PROPOSE = 100  # Min 100 ANM staked
```

#### Proposal Lifecycle:

```
1. DRAFT → Create proposal (requires 100 ANM staked)
2. ACTIVE → Voting period (7 days)
3. PASSED/REJECTED/EXPIRED → Based on quorum & approval
4. EXECUTED → Implementation of passed proposal
```

#### Methods:

```python
class GovernanceSystem:
    def create_proposal(...) -> Dict
    def vote(user_id: str, proposal_id: str, vote_for: bool) -> Dict
    def get_proposal_status(proposal_id: str) -> Dict
    def get_active_proposals() -> List[Dict]
    def execute_proposal(proposal_id: str, executor_id: str) -> Dict
```

---

### 5. Priority Coordinator (`token/priority_coordinator.py`)

Schedules jobs based on staking priority using a priority queue.

#### Priority Score Calculation:

```python
priority_score = tier_multiplier * log(staked_amount + 1)

# Examples:
# Basic tier (0 ANM):        score = 1.0
# Advanced tier (500 ANM):   score ≈ 12.4
# Pro tier (5000 ANM):       score ≈ 42.8
# Studio tier (50000 ANM):   score ≈ 109.3
```

#### Job Submission Flow:

```
1. User submits production request
2. Validate access permissions
3. Calculate and charge cost (with fees)
4. Calculate priority score
5. Add to priority queue
6. Process in priority order
7. Execute production
8. Award completion bonus
```

#### Methods:

```python
class TokenIntegratedCoordinator:
    def submit_production(user_id: str, request: Dict) -> Dict
    def process_next_job() -> Optional[Dict]
    def get_job_status(job_id: str) -> Dict
    def get_user_jobs(user_id: str) -> List[Dict]
    def get_queue_stats() -> Dict
```

---

## Data Storage

### File Structure:

```
token/
├── token_data.json       # Balances, transactions, supply
├── staking_data.json     # Stakes, rewards, tiers
├── governance_data.json  # Proposals, votes, history
└── ...
```

### Token Data Schema:

```json
{
  "token_info": {
    "name": "ANIMA",
    "symbol": "ANM",
    "total_supply": 10000000,
    "circulating_supply": 5000000,
    "burned_supply": 0,
    "decimals": 8
  },
  "balances": {
    "user_alice": 1000.5,
    "user_bob": 500.25
  },
  "transactions": [
    {
      "timestamp": "2026-01-08T10:00:00",
      "type": "transfer",
      "from": "user_alice",
      "to": "user_bob",
      "amount": 100
    }
  ]
}
```

### Staking Data Schema:

```json
{
  "stakes": {
    "user_alice": {
      "amount": 500,
      "start_time": "2026-01-01T00:00:00",
      "last_reward_claim": "2026-01-07T12:00:00",
      "total_rewards_earned": 25.5
    }
  },
  "total_staked": 50000
}
```

### Governance Data Schema:

```json
{
  "proposals": {
    "PROP-0001": {
      "id": "PROP-0001",
      "proposer": "user_alice",
      "title": "Add Manga Style Pack",
      "type": "style_pack",
      "status": "active",
      "votes_for": 150,
      "votes_against": 50,
      "voting_power_for": 15000,
      "voting_power_against": 3000
    }
  }
}
```

---

## Integration Guide

### Adding ANIMA to Existing AnimAIverse

1. **Install token system**:

```python
from token.anima_system import ANIMASystem
from workflows.coordinator import WorkflowCoordinator

# Initialize base coordinator
base_coordinator = WorkflowCoordinator(config, ...)

# Wrap with ANIMA
anima = ANIMASystem(base_coordinator)
```

2. **Submit token-gated productions**:

```python
# Old way (no tokens)
result = coordinator.execute_production(request)

# New way (with tokens)
result = anima.submit_production(user_id, request)
```

3. **Process jobs with priority**:

```python
# Process next highest-priority job
job = anima.process_next_job()
```

---

## Security Considerations

### Token Security:
- All token operations are logged
- Transaction history is immutable
- Balance checks before transfers
- Fee validation and burning

### Access Control:
- Tier validation on every request
- Feature checks before execution
- Cost calculation and pre-payment
- Automatic access denial with recommendations

### Governance Security:
- Minimum stake requirement for proposals
- Time-locked voting periods
- Quorum and approval thresholds
- Vote weight based on actual stake

---

## Performance Optimization

### Priority Queue:
- O(log n) insertion
- O(log n) extraction
- O(1) size check
- Heap-based implementation

### Reward Calculations:
- Lazy evaluation (only on claim)
- Time-based accrual
- Compound interest model

### Data Persistence:
- Batch writes when possible
- JSON file storage (upgradeable to database)
- Minimal I/O operations

---

## Testing

### Unit Tests:

```python
# Test token operations
def test_transfer():
    manager = TokenManager()
    manager.mint_tokens("alice", 1000, "test")
    result = manager.transfer("alice", "bob", 100)
    assert result["success"] == True
    assert manager.get_balance("bob") == 100

# Test staking
def test_stake_tier_upgrade():
    staking = StakingSystem(token_manager)
    result = staking.stake_tokens("alice", 500)
    assert result["new_tier"] == "advanced"

# Test governance
def test_proposal_voting():
    gov = GovernanceSystem(staking_system)
    proposal = gov.create_proposal(...)
    vote = gov.vote("alice", proposal["id"], True)
    assert vote["success"] == True
```

---

## Future Enhancements

### Phase 1: Blockchain Integration
- Deploy on Ethereum/Polygon
- Smart contract for token
- On-chain governance
- Cross-chain bridges

### Phase 2: Advanced Features
- Liquidity pools
- Token buyback mechanism
- Tiered NFT minting
- Revenue sharing

### Phase 3: Decentralization
- Distributed rendering nodes
- Peer-to-peer agent marketplace
- Community-run infrastructure
- Open-source everything

---

## API Reference

See [ANIMA_README.md](ANIMA_README.md) for complete API documentation.

---

## Support

For technical issues or questions:
- GitHub Issues: [Report Bug]
- Discord: [Tech Support Channel]
- Email: dev@animaverse.ai

---

## License

MIT License - See LICENSE file
