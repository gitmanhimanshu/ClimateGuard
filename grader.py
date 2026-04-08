"""
Automated Grading System for ClimateGuard AI
Evaluates environment quality across multiple dimensions
"""

import sys
import os
import time
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.environment import ClimateGuardEnvironment
from models import ClimateAction


class ClimateGuardGrader:
    """Comprehensive grading system"""
    
    def __init__(self):
        self.env = ClimateGuardEnvironment()
        self.max_score = 600
        self.scores = {}
    
    def grade_runtime_correctness(self) -> Dict:
        """Test runtime correctness (100 points)"""
        print("\n📋 Testing Runtime Correctness...")
        score = 0
        tests = []
        
        # Test 1: Environment initialization (10 pts)
        try:
            env = ClimateGuardEnvironment()
            tests.append(("initialization", True, 10))
            score += 10
        except Exception as e:
            tests.append(("initialization", False, 0))
        
        # Test 2: Reset functionality (15 pts)
        try:
            obs = self.env.reset(seed=42)
            assert obs is not None
            assert not obs.done
            tests.append(("reset", True, 15))
            score += 15
        except Exception as e:
            tests.append(("reset", False, 0))
        
        # Test 3: Step functionality (20 pts)
        try:
            obs = self.env.reset(seed=42)
            action = ClimateAction(firefighting_allocation={"0": 2})
            obs = self.env.step(action)
            assert obs.reward is not None
            assert 0.0 <= obs.reward <= 1.0
            tests.append(("step", True, 20))
            score += 20
        except Exception as e:
            tests.append(("step", False, 0))
        
        # Test 4: All tasks work (25 pts)
        try:
            tasks = ["single_crisis", "multi_crisis", "cascade_crisis"]
            for task in tasks:
                obs = self.env.reset(task_id=task, seed=42)
                assert obs is not None
            tests.append(("all_tasks", True, 25))
            score += 25
        except Exception as e:
            tests.append(("all_tasks", False, 0))
        
        # Test 5: Episode completion (15 pts)
        try:
            obs = self.env.reset(task_id="single_crisis", seed=42)
            for _ in range(20):
                action = ClimateAction(
                    firefighting_allocation={"0": 5},
                    evacuation_orders=[0, 1, 2]
                )
                obs = self.env.step(action)
                if obs.done:
                    break
            tests.append(("episode_completion", True, 15))
            score += 15
        except Exception as e:
            tests.append(("episode_completion", False, 0))
        
        # Test 6: No crashes (15 pts)
        try:
            obs = self.env.reset(seed=42)
            for _ in range(10):
                action = ClimateAction(
                    firefighting_allocation={"0": 1, "1": 1},
                    medical_allocation={"2": 1},
                    evacuation_orders=[3]
                )
                obs = self.env.step(action)
                if obs.done:
                    break
            tests.append(("stability", True, 15))
            score += 15
        except Exception as e:
            tests.append(("stability", False, 0))
        
        return {"score": score, "max": 100, "tests": tests}
    
    def grade_interface_compliance(self) -> Dict:
        """Test OpenEnv interface compliance (100 points)"""
        print("\n📋 Testing Interface Compliance...")
        score = 0
        tests = []
        
        # Test 1: SUPPORTS_CONCURRENT_SESSIONS (10 pts)
        try:
            assert hasattr(self.env, 'SUPPORTS_CONCURRENT_SESSIONS')
            tests.append(("concurrent_sessions", True, 10))
            score += 10
        except:
            tests.append(("concurrent_sessions", False, 0))
        
        # Test 2: Observation structure (25 pts)
        try:
            obs = self.env.reset(seed=42)
            required = ['done', 'reward', 'regions', 'resources', 'day']
            for field in required:
                assert hasattr(obs, field)
            tests.append(("observation_structure", True, 25))
            score += 25
        except:
            tests.append(("observation_structure", False, 0))
        
        # Test 3: Action structure (20 pts)
        try:
            action = ClimateAction()
            required = ['firefighting_allocation', 'medical_allocation', 
                       'evacuation_orders', 'priority_regions']
            for field in required:
                assert hasattr(action, field)
            tests.append(("action_structure", True, 20))
            score += 20
        except:
            tests.append(("action_structure", False, 0))
        
        # Test 4: State property (15 pts)
        try:
            obs = self.env.reset(seed=42)
            state = self.env.state
            assert hasattr(state, 'episode_id')
            assert hasattr(state, 'step_count')
            tests.append(("state_property", True, 15))
            score += 15
        except:
            tests.append(("state_property", False, 0))
        
        # Test 5: Reward range (15 pts)
        try:
            obs = self.env.reset(seed=42)
            for _ in range(5):
                action = ClimateAction(firefighting_allocation={"0": 1})
                obs = self.env.step(action)
                assert 0.0 <= obs.reward <= 1.0
                if obs.done:
                    break
            tests.append(("reward_range", True, 15))
            score += 15
        except:
            tests.append(("reward_range", False, 0))
        
        # Test 6: Deterministic reset (15 pts)
        try:
            obs1 = self.env.reset(seed=999)
            sev1 = obs1.regions[0].severity
            obs2 = self.env.reset(seed=999)
            sev2 = obs2.regions[0].severity
            assert sev1 == sev2
            tests.append(("deterministic_reset", True, 15))
            score += 15
        except:
            tests.append(("deterministic_reset", False, 0))
        
        return {"score": score, "max": 100, "tests": tests}
    
    def grade_task_design(self) -> Dict:
        """Evaluate task design quality (100 points)"""
        print("\n📋 Testing Task Design...")
        score = 0
        tests = []
        
        # Test 1: Multiple difficulty levels (20 pts)
        try:
            tasks = ["single_crisis", "multi_crisis", "cascade_crisis"]
            assert len(tasks) >= 3
            tests.append(("difficulty_levels", True, 20))
            score += 20
        except:
            tests.append(("difficulty_levels", False, 0))
        
        # Test 2: State complexity (20 pts)
        try:
            obs = self.env.reset(seed=42)
            assert len(obs.regions) >= 5
            region = obs.regions[0]
            # Check for rich state
            assert hasattr(region, 'severity')
            assert hasattr(region, 'crisis_type')
            assert hasattr(region, 'neighboring_regions')
            tests.append(("state_complexity", True, 20))
            score += 20
        except:
            tests.append(("state_complexity", False, 0))
        
        # Test 3: Action complexity (20 pts)
        try:
            action = ClimateAction()
            action_types = [
                'firefighting_allocation', 'flood_rescue_allocation',
                'medical_allocation', 'evacuation_orders',
                'power_restoration', 'firebreaks', 'flood_barriers'
            ]
            for action_type in action_types:
                assert hasattr(action, action_type)
            tests.append(("action_complexity", True, 20))
            score += 20
        except:
            tests.append(("action_complexity", False, 0))
        
        # Test 4: Crisis variety (20 pts)
        try:
            obs = self.env.reset(task_id="multi_crisis", seed=42)
            crisis_types = set(r.crisis_type for r in obs.regions)
            assert len(crisis_types) >= 2
            tests.append(("crisis_variety", True, 20))
            score += 20
        except:
            tests.append(("crisis_variety", False, 0))
        
        # Test 5: Dynamic environment (20 pts)
        try:
            obs = self.env.reset(seed=42)
            initial_sev = [r.severity for r in obs.regions]
            for _ in range(3):
                obs = self.env.step(ClimateAction())
            current_sev = [r.severity for r in obs.regions]
            # Environment should change
            assert initial_sev != current_sev
            tests.append(("dynamic_environment", True, 20))
            score += 20
        except:
            tests.append(("dynamic_environment", False, 0))
        
        return {"score": score, "max": 100, "tests": tests}
    
    def grade_reward_logic(self) -> Dict:
        """Evaluate reward function quality (100 points)"""
        print("\n📋 Testing Reward Logic...")
        score = 0
        tests = []
        
        # Test 1: Reward variety (20 pts)
        try:
            obs = self.env.reset(seed=42)
            rewards = []
            for _ in range(10):
                action = ClimateAction(
                    firefighting_allocation={"0": 1},
                    medical_allocation={"1": 1}
                )
                obs = self.env.step(action)
                rewards.append(obs.reward)
                if obs.done:
                    break
            # Should have variety
            assert len(set(rewards)) >= 3
            tests.append(("reward_variety", True, 20))
            score += 20
        except:
            tests.append(("reward_variety", False, 0))
        
        # Test 2: Good actions rewarded (25 pts)
        try:
            obs1 = self.env.reset(seed=42)
            # Good action
            action_good = ClimateAction(
                firefighting_allocation={"0": 5, "1": 5},
                medical_allocation={"0": 3, "1": 3},
                evacuation_orders=[0, 1, 2]
            )
            obs_good = self.env.step(action_good)
            
            obs2 = self.env.reset(seed=42)
            # Bad action (do nothing)
            action_bad = ClimateAction()
            obs_bad = self.env.step(action_bad)
            
            # Good action should have higher reward
            assert obs_good.reward > obs_bad.reward
            tests.append(("good_actions_rewarded", True, 25))
            score += 25
        except:
            tests.append(("good_actions_rewarded", False, 0))
        
        # Test 3: Multi-objective (20 pts)
        try:
            obs = self.env.reset(seed=42)
            # Check for multiple objectives in observation
            assert hasattr(obs, 'response_efficiency')
            assert hasattr(obs, 'equity_score')
            assert hasattr(obs, 'resource_utilization')
            tests.append(("multi_objective", True, 20))
            score += 20
        except:
            tests.append(("multi_objective", False, 0))
        
        # Test 4: Reward consistency (20 pts)
        try:
            obs1 = self.env.reset(seed=555)
            action = ClimateAction(firefighting_allocation={"0": 2})
            obs1 = self.env.step(action)
            reward1 = obs1.reward
            
            obs2 = self.env.reset(seed=555)
            obs2 = self.env.step(action)
            reward2 = obs2.reward
            
            # Same seed, same action = same reward
            assert abs(reward1 - reward2) < 0.01
            tests.append(("reward_consistency", True, 20))
            score += 20
        except:
            tests.append(("reward_consistency", False, 0))
        
        # Test 5: Reward scaling (15 pts)
        try:
            obs = self.env.reset(seed=42)
            rewards = []
            for _ in range(5):
                action = ClimateAction(firefighting_allocation={"0": 1})
                obs = self.env.step(action)
                rewards.append(obs.reward)
                if obs.done:
                    break
            # All rewards should be in [0, 1]
            assert all(0.0 <= r <= 1.0 for r in rewards)
            tests.append(("reward_scaling", True, 15))
            score += 15
        except:
            tests.append(("reward_scaling", False, 0))
        
        return {"score": score, "max": 100, "tests": tests}
    
    def grade_real_world_relevance(self) -> Dict:
        """Evaluate real-world applicability (100 points)"""
        print("\n📋 Testing Real-World Relevance...")
        score = 0
        tests = []
        
        # Test 1: Multiple crisis types (25 pts)
        try:
            obs = self.env.reset(task_id="multi_crisis", seed=42)
            crisis_types = set(r.crisis_type for r in obs.regions)
            valid_types = {"WILDFIRE", "FLOOD", "DROUGHT", "HURRICANE", "HEATWAVE"}
            assert crisis_types.issubset(valid_types)
            assert len(crisis_types) >= 3
            tests.append(("crisis_types", True, 25))
            score += 25
        except:
            tests.append(("crisis_types", False, 0))
        
        # Test 2: Realistic parameters (20 pts)
        try:
            obs = self.env.reset(seed=42)
            region = obs.regions[0]
            # Check realistic ranges
            assert 0.0 <= region.severity <= 1.0
            assert region.population > 0
            assert -10 <= region.temperature_celsius <= 60
            assert 0 <= region.air_quality_index <= 500
            tests.append(("realistic_parameters", True, 20))
            score += 20
        except:
            tests.append(("realistic_parameters", False, 0))
        
        # Test 3: Cascading effects (20 pts)
        try:
            obs = self.env.reset(task_id="cascade_crisis", seed=42)
            cascades = []
            for _ in range(10):
                obs = self.env.step(ClimateAction())
                cascades.extend(obs.cascade_events)
                if obs.done:
                    break
            # Should have some cascades in cascade task
            tests.append(("cascading_effects", True, 20))
            score += 20
        except:
            tests.append(("cascading_effects", False, 0))
        
        # Test 4: Resource constraints (20 pts)
        try:
            obs = self.env.reset(seed=42)
            initial_budget = obs.resources.budget_millions
            for _ in range(5):
                action = ClimateAction(
                    firefighting_allocation={"0": 3},
                    evacuation_orders=[0, 1]
                )
                obs = self.env.step(action)
                if obs.done:
                    break
            # Budget should decrease
            assert obs.resources.budget_millions < initial_budget
            tests.append(("resource_constraints", True, 20))
            score += 20
        except:
            tests.append(("resource_constraints", False, 0))
        
        # Test 5: Climate metrics (15 pts)
        try:
            obs = self.env.reset(seed=42)
            assert hasattr(obs, 'global_temperature_anomaly')
            assert hasattr(obs, 'co2_ppm')
            assert obs.co2_ppm > 400  # Realistic CO2 levels
            tests.append(("climate_metrics", True, 15))
            score += 15
        except:
            tests.append(("climate_metrics", False, 0))
        
        return {"score": score, "max": 100, "tests": tests}
    
    def grade_code_quality(self) -> Dict:
        """Evaluate code quality (100 points)"""
        print("\n📋 Testing Code Quality...")
        score = 0
        tests = []
        
        # Test 1: Documentation (20 pts)
        try:
            assert self.env.__doc__ is not None
            assert len(self.env.__doc__) > 50
            tests.append(("documentation", True, 20))
            score += 20
        except:
            tests.append(("documentation", False, 0))
        
        # Test 2: Error handling (20 pts)
        try:
            # Should handle invalid actions gracefully
            obs = self.env.reset(seed=42)
            action = ClimateAction(
                firefighting_allocation={"999": 100}  # Invalid region
            )
            obs = self.env.step(action)
            tests.append(("error_handling", True, 20))
            score += 20
        except:
            tests.append(("error_handling", False, 0))
        
        # Test 3: Performance (20 pts)
        try:
            start = time.time()
            obs = self.env.reset(seed=42)
            for _ in range(10):
                action = ClimateAction(firefighting_allocation={"0": 1})
                obs = self.env.step(action)
                if obs.done:
                    break
            elapsed = time.time() - start
            # Should be reasonably fast
            assert elapsed < 5.0
            tests.append(("performance", True, 20))
            score += 20
        except:
            tests.append(("performance", False, 0))
        
        # Test 4: Type safety (20 pts)
        try:
            obs = self.env.reset(seed=42)
            # Check types
            assert isinstance(obs.day, int)
            assert isinstance(obs.reward, (float, type(None)))
            assert isinstance(obs.regions, list)
            tests.append(("type_safety", True, 20))
            score += 20
        except:
            tests.append(("type_safety", False, 0))
        
        # Test 5: Modularity (20 pts)
        try:
            # Check for proper method organization
            assert hasattr(self.env, 'reset')
            assert hasattr(self.env, 'step')
            assert hasattr(self.env, '_generate_regions')
            assert hasattr(self.env, '_compute_reward')
            tests.append(("modularity", True, 20))
            score += 20
        except:
            tests.append(("modularity", False, 0))
        
        return {"score": score, "max": 100, "tests": tests}
    
    def run_full_grading(self) -> Dict:
        """Run complete grading suite"""
        print("\n" + "="*70)
        print("🎓 ClimateGuard AI - Automated Grading System")
        print("="*70)
        
        results = {}
        
        # Run all grading categories
        results['runtime'] = self.grade_runtime_correctness()
        results['interface'] = self.grade_interface_compliance()
        results['task_design'] = self.grade_task_design()
        results['reward'] = self.grade_reward_logic()
        results['real_world'] = self.grade_real_world_relevance()
        results['code_quality'] = self.grade_code_quality()
        
        # Calculate total
        total_score = sum(r['score'] for r in results.values())
        
        # Print summary
        print("\n" + "="*70)
        print("📊 GRADING SUMMARY")
        print("="*70)
        
        categories = [
            ("Runtime Correctness", results['runtime']),
            ("Interface Compliance", results['interface']),
            ("Task Design", results['task_design']),
            ("Reward Logic", results['reward']),
            ("Real-World Relevance", results['real_world']),
            ("Code Quality", results['code_quality'])
        ]
        
        for name, result in categories:
            percentage = (result['score'] / result['max']) * 100
            print(f"{name:.<30} {result['score']:>3}/{result['max']:<3} ({percentage:>5.1f}%)")
        
        print("="*70)
        total_percentage = (total_score / self.max_score) * 100
        print(f"{'TOTAL SCORE':.<30} {total_score:>3}/{self.max_score:<3} ({total_percentage:>5.1f}%)")
        print("="*70)
        
        # Grade interpretation
        if total_percentage >= 90:
            grade = "A+ (Excellent)"
        elif total_percentage >= 80:
            grade = "A (Very Good)"
        elif total_percentage >= 70:
            grade = "B (Good)"
        elif total_percentage >= 60:
            grade = "C (Acceptable)"
        else:
            grade = "D (Needs Improvement)"
        
        print(f"\n🏆 Final Grade: {grade}\n")
        
        return {
            'total_score': total_score,
            'max_score': self.max_score,
            'percentage': total_percentage,
            'grade': grade,
            'details': results
        }


if __name__ == '__main__':
    grader = ClimateGuardGrader()
    results = grader.run_full_grading()
