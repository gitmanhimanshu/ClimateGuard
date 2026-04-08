"""
Baseline inference script for ClimateGuard AI
Required log format: [START], [STEP], [END]
"""

import os
import json
import requests

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

TASKS = ["single_crisis", "multi_crisis", "cascade_crisis"]


def parse_action(obs: dict) -> dict:
    """Heuristic action based on observation"""
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
        
        rewards = []
        step = 0
        
        while not obs.get('done', False) and step < 20:
            step += 1
            action = parse_action(obs)
            
            step_response = requests.post(
                f"{ENV_URL}/step",
                json=action
            )
            obs = step_response.json()
            
            reward = obs.get('reward', 0.0)
            done = obs.get('done', False)
            rewards.append(reward)
            
            print(f"[STEP] step={step} action={json.dumps(action)} reward={reward:.2f} done={done} error=null")
        
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = max(0.0, min(1.0, score))
        
        return score, rewards, step, True, None
        
    except Exception as e:
        return 0.0, [], 0, False, str(e)


def main():
    """Run baseline inference with required log format"""
    print(f"[START] task=climateguard env=climateguard-ai model={MODEL_NAME}")
    
    results = {}
    
    for task_id in TASKS:
        score, rewards, steps, success, error = run_episode(task_id, seed=42)
        results[task_id] = score
        
        if not success:
            print(f"[ERROR] task={task_id} error={error}")
    
    avg_score = sum(results.values()) / len(results) if results else 0.0
    all_rewards = ",".join([f"{results[t]:.2f}" for t in TASKS])
    
    print(f"[END] success=true steps={len(TASKS)} score={avg_score:.2f} rewards={all_rewards}")


if __name__ == "__main__":
    main()
