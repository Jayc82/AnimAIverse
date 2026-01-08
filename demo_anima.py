"""
ANIMA Demo Script
Demonstrates all key features of the ANIMA token system
"""
from anima_app import AnimAIverseANIMA
from token.governance import ProposalType
import time


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def demo_user_onboarding(app: AnimAIverseANIMA):
    """Demonstrate user onboarding."""
    print_section("DEMO 1: USER ONBOARDING")
    
    # Onboard multiple users
    users = [
        ("alice", 1000.0),
        ("bob", 500.0),
        ("charlie", 10000.0)
    ]
    
    for username, tokens in users:
        result = app.onboard_user(username, tokens)
        print(f"✓ Onboarded {username} with {tokens} ANM")
    
    print("\n✅ Onboarding complete!")


def demo_staking(app: AnimAIverseANIMA):
    """Demonstrate staking mechanics."""
    print_section("DEMO 2: STAKING & TIER UPGRADES")
    
    # Alice stakes to reach Advanced tier
    print("📍 Alice stakes 200 ANM to reach Advanced tier...")
    result = app.stake_tokens("alice", 200.0)
    print(f"   Staked: {result['amount_staked']} ANM")
    print(f"   Tier: {result['old_tier']} → {result['new_tier']}")
    print(f"   APY: {result['apy']}%")
    print(f"   Priority: {result['priority_multiplier']}x")
    
    # Bob stakes to reach Advanced tier
    print("\n📍 Bob stakes 300 ANM to reach Advanced tier...")
    result = app.stake_tokens("bob", 300.0)
    print(f"   Staked: {result['amount_staked']} ANM")
    print(f"   Tier: {result['old_tier']} → {result['new_tier']}")
    
    # Charlie stakes to reach Studio tier
    print("\n📍 Charlie stakes 5000 ANM to reach Studio tier...")
    result = app.stake_tokens("charlie", 5000.0)
    print(f"   Staked: {result['amount_staked']} ANM")
    print(f"   Tier: {result['old_tier']} → {result['new_tier']}")
    print(f"   APY: {result['apy']}%")
    print(f"   Priority: {result['priority_multiplier']}x")
    
    print("\n✅ Staking demonstration complete!")


def demo_feature_access(app: AnimAIverseANIMA):
    """Demonstrate tiered feature access."""
    print_section("DEMO 3: TIERED FEATURE ACCESS")
    
    users = ["alice", "bob", "charlie"]
    
    for user in users:
        print(f"📊 {user.upper()}'s Access:")
        access = app.anima.get_feature_access_summary(user)
        
        tier = access['tier']
        print(f"   Tier: {tier}")
        print(f"   Priority Score: {access['priority_score']:.2f}")
        print(f"   Max Agents: {access['features']['agents']['max_simultaneous']}")
        print(f"   Max Resolution: {access['features']['video']['max_resolution']}")
        print(f"   Max FPS: {access['features']['video']['max_fps']}")
        print(f"   Style Packs: {', '.join(access['features']['styles']['available_packs'])}")
        print()
    
    print("✅ Feature access demonstration complete!")


def demo_production_workflow(app: AnimAIverseANIMA):
    """Demonstrate production creation with priority."""
    print_section("DEMO 4: PRODUCTION WORKFLOW WITH PRIORITY")
    
    # Multiple users submit productions
    productions = [
        ("alice", "sci-fi", "Space odyssey", "1080p", 30),
        ("bob", "action", "Epic battle", "720p", 24),
        ("charlie", "fantasy", "Magic realm", "4K", 60)
    ]
    
    print("📍 Submitting productions from different tier users...")
    for user, genre, theme, resolution, fps in productions:
        print(f"\n{user.upper()} submitting {genre} animation...")
        
        result = app.create_animation(
            user_id=user,
            genre=genre,
            theme=theme,
            duration=3,
            resolution=resolution,
            fps=fps,
            style="cinematic"
        )
        
        if result["success"]:
            print(f"   ✓ Job ID: {result['job_id']}")
            print(f"   ✓ Status: Production completed")
        else:
            print(f"   ✗ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Production workflow complete!")


def demo_rewards_claiming(app: AnimAIverseANIMA):
    """Demonstrate reward claiming."""
    print_section("DEMO 5: STAKING REWARDS")
    
    print("⏳ Simulating time passage for reward accrual...")
    print("   (In production, rewards accrue over time)")
    
    users = ["alice", "bob", "charlie"]
    
    for user in users:
        print(f"\n📍 {user.upper()} claiming rewards...")
        
        # Check pending rewards
        staking_info = app.anima.get_staking_info(user)
        pending = staking_info.get("pending_rewards", 0)
        
        print(f"   Pending rewards: {pending:.6f} ANM")
        
        # Claim rewards
        if pending > 0:
            result = app.claim_rewards(user)
            if result["success"]:
                print(f"   ✓ Claimed: {result['rewards']:.6f} ANM")
                print(f"   ✓ Total earned: {result['total_earned']:.6f} ANM")
        else:
            print("   No rewards to claim yet (stake for longer)")
    
    print("\n✅ Rewards demonstration complete!")


def demo_governance(app: AnimAIverseANIMA):
    """Demonstrate governance system."""
    print_section("DEMO 6: COMMUNITY GOVERNANCE")
    
    # Alice creates a proposal
    print("📍 Alice creates a proposal for a new style pack...")
    proposal_result = app.create_proposal(
        user_id="alice",
        title="Add Cyberpunk Style Pack",
        description="High-quality cyberpunk aesthetic with neon lighting, futuristic cityscapes, and tech-noir atmosphere",
        proposal_type="style_pack",
        proposal_data={
            "pack_name": "cyberpunk_2077",
            "styles": ["neon_city", "tech_noir", "dystopian_future"],
            "tier_access": "advanced"
        }
    )
    
    if proposal_result["success"]:
        proposal_id = proposal_result["proposal"]["id"]
        print(f"   ✓ Proposal created: {proposal_id}")
        print(f"   ✓ Title: {proposal_result['proposal']['title']}")
        print(f"   ✓ Voting ends: {proposal_result['proposal']['voting_ends']}")
        
        # Users vote
        print("\n📍 Community members vote on the proposal...")
        
        votes = [
            ("alice", True, "Creator votes FOR"),
            ("bob", True, "Bob votes FOR"),
            ("charlie", True, "Charlie votes FOR (high voting power)")
        ]
        
        for user, vote_for, description in votes:
            print(f"   {description}...")
            vote_result = app.vote_on_proposal(user, proposal_id, vote_for)
            if vote_result["success"]:
                print(f"      ✓ Vote recorded")
        
        # Check proposal status
        print("\n📍 Checking proposal status...")
        status = app.anima.get_proposal_status(proposal_id)
        voting_stats = status["voting_stats"]
        
        print(f"   Votes FOR: {voting_stats['votes_for']}")
        print(f"   Votes AGAINST: {voting_stats['votes_against']}")
        print(f"   Approval rate: {voting_stats['approval_rate']:.1f}%")
        print(f"   Quorum progress: {voting_stats['quorum_progress']:.1f}%")
        
        if voting_stats['approval_rate'] >= voting_stats['approval_required']:
            print(f"   ✓ Proposal is passing! (>{voting_stats['approval_required']}% approval)")
        
    else:
        print(f"   ✗ Failed to create proposal: {proposal_result.get('error')}")
    
    print("\n✅ Governance demonstration complete!")


def demo_dashboards(app: AnimAIverseANIMA):
    """Demonstrate user dashboards."""
    print_section("DEMO 7: USER DASHBOARDS")
    
    users = ["alice", "bob", "charlie"]
    
    for user in users:
        print(f"📊 {user.upper()}'S DASHBOARD:")
        dashboard = app.get_dashboard(user)
        
        wallet = dashboard["wallet"]
        tier = dashboard["tier"]
        activity = dashboard["activity"]
        
        print(f"   💰 Wallet:")
        print(f"      Balance: {wallet['balance']:.2f} ANM")
        print(f"      Staked: {wallet['staked']:.2f} ANM")
        print(f"      Total Value: {wallet['total_value']:.2f} ANM")
        print(f"      Pending Rewards: {wallet['pending_rewards']:.6f} ANM")
        
        print(f"   🎯 Tier:")
        print(f"      Current: {tier['current']}")
        print(f"      Priority Score: {tier['priority_score']:.2f}")
        
        print(f"   📈 Activity:")
        print(f"      Total Productions: {activity['total_productions']}")
        print(f"      Completed: {activity['completed_productions']}")
        print(f"      Votes Cast: {activity['total_votes']}")
        
        print()
    
    print("✅ Dashboard demonstration complete!")


def demo_platform_stats(app: AnimAIverseANIMA):
    """Display platform statistics."""
    print_section("DEMO 8: PLATFORM STATISTICS")
    
    app.show_platform_stats()
    
    print("✅ Platform statistics displayed!")


def main():
    """Run complete ANIMA demonstration."""
    print("\n" + "🌟"*35)
    print(" "*20 + "ANIMA COMPLETE DEMO")
    print(" "*15 + "The Bitcoin of Animation")
    print("🌟"*35 + "\n")
    
    # Initialize ANIMA system
    print("🚀 Initializing ANIMA system...")
    app = AnimAIverseANIMA()
    
    # Run all demos
    demo_user_onboarding(app)
    time.sleep(1)
    
    demo_staking(app)
    time.sleep(1)
    
    demo_feature_access(app)
    time.sleep(1)
    
    demo_production_workflow(app)
    time.sleep(1)
    
    demo_rewards_claiming(app)
    time.sleep(1)
    
    demo_governance(app)
    time.sleep(1)
    
    demo_dashboards(app)
    time.sleep(1)
    
    demo_platform_stats(app)
    
    # Final summary
    print("\n" + "="*70)
    print("  🎉 DEMO COMPLETE!")
    print("="*70)
    print("\n✅ All ANIMA features demonstrated successfully!")
    print("\n📚 Key Features Showcased:")
    print("   • Token management and distribution")
    print("   • Multi-tier staking system")
    print("   • Priority-based job scheduling")
    print("   • Tiered feature access control")
    print("   • Automated reward distribution")
    print("   • Community governance system")
    print("   • Deflationary tokenomics")
    print("   • Comprehensive user dashboards")
    print("\n🚀 ANIMA - Democratizing Animation Creation!\n")


if __name__ == "__main__":
    main()
