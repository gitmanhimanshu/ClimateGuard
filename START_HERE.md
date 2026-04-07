# 🚀 START HERE - ClimateGuard AI

## Ek Minute Me Start Karo! ⚡

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Demo
```bash
python demo.py
```

Ye dikhayega ki environment kaise kaam karta hai!

---

## Server Start Karo (With UI) 🌐

```bash
# Start server
python -m server.app

# Ya
uvicorn server.app:app --port 7860
```

**Server URL:** http://localhost:7860

**API Docs:** http://localhost:7860/docs

---

## Test Karo ✅

```bash
# Run tests
python test_environment.py

# Run grader
python grader.py
```

---

## Project Structure 📁

```
facebook/
├── models.py              # Data models (RegionData, ClimateAction, etc.)
├── openenv.yaml           # OpenEnv configuration
├── server/
│   ├── __init__.py
│   ├── app.py            # FastAPI server
│   └── environment.py    # Main environment logic
├── demo.py               # Simple demo script
├── test_environment.py   # Test suite
├── grader.py            # Automated grading
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker config
└── README.md            # Full documentation
```

---

## Kaise Kaam Karta Hai? 🤔

### 1. Environment Create Karo
```python
from server.environment import ClimateGuardEnvironment

env = ClimateGuardEnvironment()
```

### 2. Reset Karo (Episode Start)
```python
obs = env.reset(task_id="multi_crisis", seed=42)

print(f"Regions: {len(obs.regions)}")
print(f"Population: {obs.total_population_at_risk}")
```

### 3. Action Lo
```python
from models import ClimateAction

action = ClimateAction(
    firefighting_allocation={"0": 3, "1": 2},  # Region 0 ko 3 units, Region 1 ko 2
    medical_allocation={"0": 2},                # Region 0 ko 2 medical teams
    evacuation_orders=[2, 3],                   # Region 2 aur 3 evacuate karo
    evacuation_allocation={"2": 5, "3": 5}      # 5-5 buses bhejo
)
```

### 4. Step Execute Karo
```python
obs = env.step(action)

print(f"Reward: {obs.reward}")
print(f"Casualties: {obs.total_casualties}")
print(f"Evacuated: {obs.total_evacuated}")
print(f"Done: {obs.done}")
```

---

## 5 Crisis Types 🔥🌊🏜️🌀🌡️

1. **WILDFIRE** - Aag failti hai
2. **FLOOD** - Pani ka crisis
3. **DROUGHT** - Sukha
4. **HURRICANE** - Toofan
5. **HEATWAVE** - Extreme garmi

---

## 3 Tasks (Difficulty Levels)

### Task 1: single_crisis (Easy)
```python
obs = env.reset(task_id="single_crisis")
# 5 regions, sirf wildfire
```

### Task 2: multi_crisis (Medium)
```python
obs = env.reset(task_id="multi_crisis")
# 10 regions, 3 crisis types
```

### Task 3: cascade_crisis (Hard)
```python
obs = env.reset(task_id="cascade_crisis")
# 12 regions, 4 crisis types, cascading effects
```

---

## Actions Kya Kar Sakte Ho? 🎯

```python
ClimateAction(
    # Resources allocate karo
    firefighting_allocation: {"0": 3, "1": 2}
    flood_rescue_allocation: {"2": 2}
    medical_allocation: {"0": 1, "1": 1}
    evacuation_allocation: {"3": 5}
    
    # Infrastructure restore karo
    power_restoration: [0, 1]
    water_supply_restoration: [2]
    
    # Preventive measures
    firebreaks: [0]
    flood_barriers: [2]
    
    # Evacuation orders
    evacuation_orders: [3, 4]
    
    # Supplies distribute karo
    food_distribution: {"0": 10.0, "1": 15.0}
    water_distribution: {"2": 3}
)
```

---

## Observation Me Kya Milta Hai? 📊

```python
obs.regions              # List of all regions with crisis data
obs.resources            # Available resources
obs.day                  # Current day
obs.total_casualties     # Total casualties
obs.total_evacuated      # Total evacuated
obs.reward               # Reward (0-1)
obs.done                 # Episode finished?
obs.co2_ppm              # CO2 concentration
obs.global_temperature_anomaly  # Temperature increase
```

---

## Reward Kaise Calculate Hota Hai? 🏆

```
Reward = 70% lives saved + 30% casualty prevention
```

Higher reward = Better performance!

---

## Docker Se Run Karo 🐳

```bash
# Build
docker build -t climateguard-ai .

# Run
docker run -p 7860:7860 climateguard-ai

# Or use compose
docker-compose up
```

---

## Troubleshooting 🔧

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Change port
uvicorn server.app:app --port 8000
```

### Tests failing
```bash
# Check if models.py and server/environment.py exist
ls models.py server/environment.py
```

---

## Next Steps 🎯

1. ✅ Run `python demo.py` - See it working
2. ✅ Run `python test_environment.py` - Verify tests pass
3. ✅ Run `python grader.py` - Check score
4. ✅ Start server: `python -m server.app`
5. ✅ Deploy to Hugging Face

---

## Quick Commands Cheat Sheet 📝

```bash
# Demo
python demo.py

# Tests
python test_environment.py

# Grader
python grader.py

# Server
python -m server.app

# Docker
docker-compose up
```

---

**Ab shuru karo!** 🚀

Run: `python demo.py`
