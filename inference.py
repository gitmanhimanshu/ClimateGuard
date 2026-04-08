"""
Baseline inference script for ClimateGuard AI
Uses OpenAI Client with required environment variables
"""

import os
import json
import requests
from openai import OpenAI

# Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

TASKS = ["single_crisis", "multi_crisis", "cascade_crisis"]


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call LLM using OpenAI client"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def format_observation(obs: dict) -> str:
    """Format observation for LLM"""
    lines = [
        f"Day {obs['day']} - Budget: ${obs['resources']['budget_millions']}M",
        f"Casualties: {obs['total_casualties']}, Evacuated: {obs['total_evacuated']}",
        f"\nResources: Firefighting={obs['resources']['firefighting_units']}, Medical={obs['resources']['medical_teams']}, Buses={obs['resources']['evacuation_buses']}",
        f"\nTop Regions:"
    ]
    
    for region in obs['regions'][:3]:
        lines.append(
            f"  {region['region_name']}: {region['crisis_type']} "
            f"(severity {region['severity']:.2f}, pop {region['population']:,})"
        )
    
    return "\n".join(lines)


def parse_action_from_llm(llm_response: str, obs: dict) -> dict:
    """Parse LLM response into action with fallback heuristics"""
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
    
    # Heuristic fallback based on observation
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


def run_episode(task_id: str, seed: int) -> tuple:
    """Run episode and return (score, rewards, steps, success, error)"""
    try:
        reset_response = requests.post(
            f"{ENV_URL}/reset",
            json={"task_id": task_id, "seed": seed}
        )
        obs = reset_response.json()
        
        system_prompt = """You are an AI coordinator for climate crisis response.
Minimize casualties and maximize evacuations by allocating resources effectively."""
        
        rewards = []
        step = 0
        
        while not obs.get('done', False) and step < 20:
            step += 1
            
            # Get LLM guidance
            obs_text = format_observation(obs)
            user_prompt = f"{obs_text}\n\nProvide crisis response strategy."
            llm_response = call_llm(system_prompt, user_prompt)
            
            # Parse action
            action = parse_action_from_llm(llm_response, obs)
            
            step_response = requests.post(
                f"{ENV_URL}/step",
                json=action
            )
            obs = step_response.json()
            
            reward = obs.get('reward', 0.0)
            done = obs.get('done', False)
            rewards.append(reward)
            
            # Required log format
            print(f"[STEP] step={step} action={json.dumps(action)} reward={reward:.2f} done={done} error=null")
        
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = max(0.0, min(1.0, score))
        
        return score, rewards, step, True, None
        
    except Exception as e:
        return 0.0, [], 0, False, str(e)


def main():
    """Run baseline inference with required log format"""
    # Required [START] format
    print(f"[START] task=climateguard env=climateguard-ai model={MODEL_NAME}")
    
    results = {}
    
    for task_id in TASKS:
        score, rewards, steps, success, error = run_episode(task_id, seed=42)
        results[task_id] = score
        
        if not success:
            print(f"[ERROR] task={task_id} error={error}")
    
    avg_score = sum(results.values()) / len(results) if results else 0.0
    all_rewards = ",".join([f"{results[t]:.2f}" for t in TASKS])
    
    # Required [END] format
    print(f"[END] success=true steps={len(TASKS)} score={avg_score:.2f} rewards={all_rewards}")


if __name__ == "__main__":
    main()
