# ⚡ Quick Start - ClimateGuard AI

Get up and running in 5 minutes!

---

## 1️⃣ Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

---

## 2️⃣ Run Tests (1 min)

```bash
python test_environment.py
```

Expected: ✅ ALL TESTS PASSED!

---

## 3️⃣ Check Score (1 min)

```bash
python grader.py
```

Expected: 580+/600 (97%)

---

## 4️⃣ Start Server (1 min)

```bash
uvicorn server.app:app --port 7860
```

Open: http://localhost:7860/docs

---

## 5️⃣ Deploy to HF (1 min)

```bash
huggingface-cli login
python deploy.py YOUR_USERNAME/climateguard-ai
```

---

## ✅ Done!

Your environment is ready for submission! 🎉

---

## 🧪 Quick Test

```python
from server.environment import ClimateGuardEnvironment
from models import ClimateAction

# Create environment
env = ClimateGuardEnvironment()

# Reset
obs = env.reset(task_id="multi_crisis", seed=42)
print(f"Regions: {len(obs.regions)}")
print(f"Crisis types: {set(r.crisis_type for r in obs.regions)}")

# Take action
action = ClimateAction(
    firefighting_allocation={"0": 3, "1": 2},
    medical_allocation={"0": 2},
    evacuation_orders=[2, 3]
)

# Step
obs = env.step(action)
print(f"Reward: {obs.reward:.3f}")
print(f"Casualties: {obs.total_casualties}")
print(f"Evacuated: {obs.total_evacuated}")
```

---

## 🐳 Docker Quick Start

```bash
# Build
docker build -t climateguard-ai .

# Run
docker run -p 7860:7860 climateguard-ai

# Or use compose
docker-compose up
```

---

## 📚 Full Documentation

- **README.md** - Complete overview
- **SETUP_GUIDE.md** - Detailed setup instructions
- **WHY_CLIMATEGUARD_WINS.md** - Why this wins
- **PROJECT_COMPARISON.md** - Comparison with others

---

## 🎯 Submission Checklist

- [ ] Tests pass
- [ ] Grader score 580+
- [ ] Deployed to HF
- [ ] GitHub repo created
- [ ] README complete

---

**You're ready to win!** 🏆🌍
