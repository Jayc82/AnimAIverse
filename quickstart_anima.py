"""
Quick Start Script for ANIMA
Run this for a fast demonstration of key features
"""
from anima_app import AnimAIverseANIMA


def quick_demo():
    """Quick 2-minute demo of ANIMA."""
    print("\n" + "🌟"*30)
    print("     ANIMA QUICK START DEMO")
    print("     2-Minute Overview")
    print("🌟"*30 + "\n")
    
    # Initialize
    print("🚀 Initializing ANIMA...")
    app = AnimAIverseANIMA()
    
    # Create user
    print("\n👤 Creating user with 1000 ANM...")
    app.onboard_user("demo_user", initial_tokens=1000.0)
    
    # Stake
    print("\n💎 Staking 500 ANM...")
    stake_result = app.stake_tokens("demo_user", 500.0)
    print(f"✓ Tier: {stake_result['new_tier']}")
    print(f"✓ APY: {stake_result['apy']}%")
    
    # Show features
    print("\n🎯 Your Features:")
    access = app.anima.get_feature_access_summary("demo_user")
    print(f"✓ Max Resolution: {access['features']['video']['max_resolution']}")
    print(f"✓ Max FPS: {access['features']['video']['max_fps']}")
    print(f"✓ Max Agents: {access['features']['agents']['max_simultaneous']}")
    
    # Create animation
    print("\n🎬 Creating Animation...")
    result = app.create_animation(
        user_id="demo_user",
        genre="action",
        theme="Epic adventure",
        duration=3,
        resolution="1080p",
        fps=30
    )
    
    if result["success"]:
        print("✓ Animation created successfully!")
    
    # Final dashboard
    print("\n📊 Your Dashboard:")
    dashboard = app.get_dashboard("demo_user")
    print(f"✓ Balance: {dashboard['wallet']['balance']:.2f} ANM")
    print(f"✓ Staked: {dashboard['wallet']['staked']:.2f} ANM")
    print(f"✓ Tier: {dashboard['tier']['current']}")
    print(f"✓ Productions: {dashboard['activity']['total_productions']}")
    
    print("\n" + "="*60)
    print("✅ QUICK DEMO COMPLETE!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   • Run full demo: python demo_anima.py")
    print("   • Read docs: ANIMA_README.md")
    print("   • Explore code: token/")
    print("\n🌟 Welcome to ANIMA!\n")


if __name__ == "__main__":
    quick_demo()
