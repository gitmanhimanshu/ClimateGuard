"""
Baseline inference script for ClimateGuard AI
Tests the environment with OpenAI GPT-4 agent
"""

import os
import sys
import json
import requests
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Environment endpoint
ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")

# Tasks to test
TASKS = ["single_crisis", "multi_crisis", "cascade_crisis"]


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI API"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content


def format_observation(obs: dict) -> str:
    """Format observation for LLM"""
    lines = [
        f"Day {obs['day']}",
        f"Total Casualties: {obs['total_casualties']}",
        f"Total Evacuated: {obs['total_evacuated']}",
        f"Budget: ${obs['resources']['budget_millions']}M",
        f"\nResources Available:",
        f"  Firefighting Units: {obs['resources']['firefighting_units']}",
        f"  Medical Teams: {obs['resources']['medical_teams']}",
        f"  Evacuation Buses: {obs['resources']['evacuation_buses']}",
        f"\nRegions:"
    ]
    
    for region in obs['regions'][:5]:  # Show first 5 regions
        lines.append(
            f"  {region['region_name']}: {region['crisis_type']} "
            f"(severity {region['severity']:.2f}, pop {region['population']:,})"
        )
    
    return "\n".join(lines)


def parse_action(llm_response: str, obs: dict) -> dict:
    """Parse LLM response into action"""
    # Simple heuristic-based action
    action = {
        "firefighting_allocation": {},
        "flood_rescue_allocation": {},
        "medical_allocation": {},
        "evacuation_allocation": {},
        "power_restoration": [],
        "water_supply_restoration": [],
        "firebreaks": [],
        "flood_barriers": [],
        "evacuation_orders": [],
        "food_distribution": {},
        "water_distribution": {},
        "satellite_coverage": [],
        "priority_regions": []
    }
    
    # Allocate resources based on crisis severity
    for region in obs['regions']:
        rid = str(region['region_id'])
        severity = region['severity']
        
        if region['crisis_type'] == 'WILDFIRE' and severity > 0.5:
            action['firefighting_allocation'][rid] = min(5, int(severity * 10))
            action['firebreaks'].append(region['region_id'])
        
        if region['crisis_type'] == 'FLOOD' and severity > 0.5:
            action['flood_rescue_allocation'][rid] = min(3, int(severity * 6))
            action['flood_barriers'].append(region['region_id'])
        
        if severity > 0.6:
            action['medical_allocation'][rid] = min(3, int(severity * 5))
            action['evacuation_allocation'][rid] = min(5, int(severity * 8))
            action['evacuation_orders'].append(region['region_id'])
        
        if region['power_grid'] < 0.5:
            action['power_restoration'].append(region['region_id'])
        
        if region['water_supply'] < 0.5:
            action['water_supply_restoration'].append(region['region_id'])
    
    return action


def run_episode(task_id: str, seed: int) -> float:
    """Run one episode"""
    # Reset environment
    reset_response = requests.post(
        f"{ENV_URL}/reset",
        json={"task_id": task_id, "seed": seed}
    )
    obs = reset_response.json()
    
    system_prompt = """You are an AI coordinator for global climate crisis response.
Your goal is to minimize casualties and maximize evacuations by allocating resources
effectively across multiple regions facing wildfires, floods, droughts, and extreme weather."""
    
    total_reward = 0.0
    step = 0
    
    while not obs.get('done', False):
        step += 1
        
        # Format observation
        obs_text = format_observation(obs)
        
        # Get LLM decision
        user_prompt = f"{obs_text}\n\nWhat actions should we take?"
        llm_response = call_llm(system_prompt, user_prompt)
        
        # Parse action
        action = parse_action(llm_response, obs)
        
        # Take step
        step_response = requests.post(
            f"{ENV_URL}/step",
            json=action
        )
        obs = step_response.json()
        
        reward = obs.get('reward', 0.0)
        total_reward += reward
        
        print(f"[STEP] task={task_id} step={step} reward={reward:.3f} "
              f"casualties={obs['total_casualties']} evacuated={obs['total_evacuated']}")
    
    return total_reward


def main():
    """Run baseline inference"""
    print("[START] ClimateGuard AI Baseline Inference")
    print(f"Environment: {ENV_URL}")
    print(f"Model: gpt-4")
    print()
    
    results = {}
    
    for task_id in TASKS:
        print(f"\n{'='*60}")
        print(f"Running task: {task_id}")
        print('='*60)
        
        total_reward = run_episode(task_id, seed=42)
        score = max(0.0, min(1.0, total_reward))
        
        results[task_id] = score
        print(f"[END] task={task_id} score={score:.2f}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for task_id, score in results.items():
        print(f"{task_id}: {score:.2f}")
    
    avg_score = sum(results.values()) / len(results)
    print(f"\nAverage Score: {avg_score:.2f}")


if __name__ == "__main__":
    main()
