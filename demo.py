"""
Simple Demo Script for ClimateGuard AI
Shows how to use the environment
"""

from server.environment import ClimateGuardEnvironment
from models import ClimateAction

def demo():
    print("\n" + "="*60)
    print("🌍 ClimateGuard AI - Demo")
    print("="*60 + "\n")
    
    # Create environment
    env = ClimateGuardEnvironment()
    
    # Reset for multi-crisis task
    print("📍 Starting multi-crisis scenario...")
    obs = env.reset(task_id="multi_crisis", seed=42)
    
    print(f"\n✅ Environment initialized!")
    print(f"   Regions: {len(obs.regions)}")
    print(f"   Population at risk: {obs.total_population_at_risk:,}")
    print(f"   Budget: ${obs.resources.budget_millions}M")
    print(f"   CO2: {obs.co2_ppm} ppm")
    
    print(f"\n🔥 Crisis Types:")
    for region in obs.regions:
        print(f"   Region {region.region_id} ({region.region_name}): {region.crisis_type} - Severity: {region.severity:.2f}")
    
    # Run 3 steps
    print(f"\n🎮 Running simulation for 3 days...\n")
    
    for day in range(3):
        # Create action
        action = ClimateAction(
            firefighting_allocation={"0": 3, "1": 2},
            medical_allocation={"0": 2, "1": 1},
            evacuation_orders=[2, 3],
            evacuation_allocation={"2": 5, "3": 5}
        )
        
        # Step
        obs = env.step(action)
        
        print(f"Day {obs.day}:")
        print(f"  Reward: {obs.reward:.3f}")
        print(f"  Casualties: {obs.total_casualties}")
        print(f"  Evacuated: {obs.total_evacuated}")
        print(f"  Budget remaining: ${obs.resources.budget_millions:.1f}M")
        print(f"  {obs.outcome_summary}")
        print()
        
        if obs.done:
            print("✅ Episode completed!")
            break
    
    print("="*60)
    print("Demo complete! Environment is working correctly.")
    print("="*60 + "\n")


if __name__ == '__main__':
    demo()
