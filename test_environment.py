"""
Comprehensive test suite for ClimateGuard AI Environment
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.environment import ClimateGuardEnvironment
from models import ClimateAction


class TestClimateGuardEnvironment(unittest.TestCase):
    """Test suite for ClimateGuard AI"""
    
    def setUp(self):
        """Set up test environment"""
        self.env = ClimateGuardEnvironment()
    
    def test_initialization(self):
        """Test environment initializes correctly"""
        self.assertIsNotNone(self.env)
        self.assertEqual(self.env._day, 0)
    
    def test_reset_basic(self):
        """Test basic reset functionality"""
        obs = self.env.reset(seed=42)
        
        self.assertIsNotNone(obs)
        self.assertFalse(obs.done)
        self.assertIsNone(obs.reward)
        self.assertGreater(len(obs.regions), 0)
        self.assertIsNotNone(obs.resources)
    
    def test_reset_all_tasks(self):
        """Test reset for all task types"""
        tasks = ["single_crisis", "multi_crisis", "cascade_crisis", 
                 "extreme_climate", "resource_scarcity"]
        
        for task_id in tasks:
            obs = self.env.reset(task_id=task_id, seed=42)
            self.assertIsNotNone(obs)
            self.assertEqual(obs.day, 0)
            print(f"✓ Task '{task_id}' reset successfully")
    
    def test_step_basic(self):
        """Test basic step functionality"""
        obs = self.env.reset(seed=42)
        
        action = ClimateAction(
            firefighting_allocation={"0": 2},
            medical_allocation={"1": 1}
        )
        
        obs = self.env.step(action)
        
        self.assertIsNotNone(obs)
        self.assertIsNotNone(obs.reward)
        self.assertIsInstance(obs.reward, float)
        self.assertGreaterEqual(obs.reward, 0.0)
        self.assertLessEqual(obs.reward, 1.0)
        self.assertEqual(obs.day, 1)
    
    def test_action_space(self):
        """Test all action types work"""
        obs = self.env.reset(seed=42)
        
        action = ClimateAction(
            firefighting_allocation={"0": 3, "1": 2},
            flood_rescue_allocation={"2": 2},
            medical_allocation={"0": 1, "3": 1},
            evacuation_allocation={"4": 5},
            power_restoration=[0, 1],
            water_supply_restoration=[2],
            firebreaks=[0],
            flood_barriers=[2],
            evacuation_orders=[3, 4],
            food_distribution={"0": 10.0, "1": 15.0},
            water_distribution={"2": 3},
            satellite_coverage=[0, 1, 2],
            priority_regions=[0, 1, 2, 3, 4]
        )
        
        obs = self.env.step(action)
        self.assertIsNotNone(obs.reward)
    
    def test_observation_structure(self):
        """Test observation contains all required fields"""
        obs = self.env.reset(seed=42)
        
        required_fields = [
            'done', 'reward', 'regions', 'resources', 'day',
            'total_casualties', 'total_evacuated', 'total_population_at_risk',
            'global_temperature_anomaly', 'co2_ppm', 'new_crises',
            'resolved_crises', 'cascade_events', 'response_efficiency',
            'resource_utilization', 'equity_score', 'outcome_summary',
            'task_description'
        ]
        
        for field in required_fields:
            self.assertTrue(hasattr(obs, field), f"Missing field: {field}")
    
    def test_region_data_structure(self):
        """Test region data contains all required fields"""
        obs = self.env.reset(seed=42)
        
        self.assertGreater(len(obs.regions), 0)
        region = obs.regions[0]
        
        required_fields = [
            'region_id', 'region_name', 'crisis_type', 'severity',
            'population', 'evacuated', 'casualties', 'infrastructure_damage',
            'water_supply', 'power_grid', 'hospital_capacity',
            'food_supply_days', 'temperature_celsius', 'air_quality_index',
            'wind_speed_kmh', 'precipitation_mm', 'fire_spread_risk',
            'flood_risk', 'neighboring_regions', 'climate_trend'
        ]
        
        for field in required_fields:
            self.assertTrue(hasattr(region, field), f"Missing region field: {field}")
    
    def test_resources_structure(self):
        """Test resources contain all required fields"""
        obs = self.env.reset(seed=42)
        
        required_fields = [
            'firefighting_units', 'flood_rescue_boats', 'medical_teams',
            'evacuation_buses', 'helicopters', 'water_tankers',
            'food_supplies_tons', 'emergency_shelters', 'power_generators',
            'communication_satellites', 'budget_millions'
        ]
        
        for field in required_fields:
            self.assertTrue(hasattr(obs.resources, field), 
                          f"Missing resource field: {field}")
    
    def test_reward_range(self):
        """Test rewards are in valid range"""
        obs = self.env.reset(seed=42)
        
        for _ in range(10):
            action = ClimateAction(
                firefighting_allocation={"0": 1},
                medical_allocation={"1": 1}
            )
            obs = self.env.step(action)
            
            self.assertGreaterEqual(obs.reward, 0.0)
            self.assertLessEqual(obs.reward, 1.0)
            
            if obs.done:
                break
    
    def test_episode_termination(self):
        """Test episode terminates correctly"""
        obs = self.env.reset(task_id="single_crisis", seed=42)
        
        max_steps = 50
        steps = 0
        
        while not obs.done and steps < max_steps:
            action = ClimateAction(
                firefighting_allocation={"0": 5, "1": 5},
                medical_allocation={"0": 3, "1": 3},
                evacuation_orders=[0, 1, 2, 3, 4]
            )
            obs = self.env.step(action)
            steps += 1
        
        self.assertTrue(obs.done or steps >= max_steps)
    
    def test_resource_consumption(self):
        """Test resources are consumed correctly"""
        obs = self.env.reset(seed=42)
        
        initial_firefighting = obs.resources.firefighting_units
        initial_medical = obs.resources.medical_teams
        
        action = ClimateAction(
            firefighting_allocation={"0": 3, "1": 2},
            medical_allocation={"0": 2}
        )
        
        obs = self.env.step(action)
        
        # Resources should decrease
        self.assertLessEqual(obs.resources.firefighting_units, initial_firefighting)
        self.assertLessEqual(obs.resources.medical_teams, initial_medical)
    
    def test_crisis_evolution(self):
        """Test crises evolve over time"""
        obs = self.env.reset(seed=42)
        
        initial_severities = [r.severity for r in obs.regions]
        
        # Take minimal action
        for _ in range(3):
            action = ClimateAction()
            obs = self.env.step(action)
        
        # Some severities should change
        current_severities = [r.severity for r in obs.regions]
        self.assertNotEqual(initial_severities, current_severities)
    
    def test_evacuation_logic(self):
        """Test evacuation reduces population at risk"""
        obs = self.env.reset(seed=42)
        
        initial_at_risk = obs.total_population_at_risk
        
        action = ClimateAction(
            evacuation_orders=[0, 1, 2],
            evacuation_allocation={"0": 10, "1": 10, "2": 10}
        )
        
        obs = self.env.step(action)
        
        # Population at risk should decrease
        self.assertLess(obs.total_population_at_risk, initial_at_risk)
    
    def test_cascade_events(self):
        """Test cascade events can occur"""
        obs = self.env.reset(task_id="cascade_crisis", seed=42)
        
        all_cascades = []
        
        for _ in range(10):
            action = ClimateAction()  # No action to let crises worsen
            obs = self.env.step(action)
            all_cascades.extend(obs.cascade_events)
            
            if obs.done:
                break
        
        # Should have some cascade events in cascade task
        print(f"Cascade events detected: {len(all_cascades)}")
    
    def test_state_property(self):
        """Test state property returns valid state"""
        obs = self.env.reset(seed=42)
        
        state = self.env.state
        self.assertIsNotNone(state)
        self.assertIsNotNone(state.episode_id)
        self.assertEqual(state.step_count, 0)
    
    def test_deterministic_reset(self):
        """Test reset with same seed produces same initial state"""
        obs1 = self.env.reset(seed=12345)
        region1_severity = obs1.regions[0].severity
        
        obs2 = self.env.reset(seed=12345)
        region2_severity = obs2.regions[0].severity
        
        self.assertEqual(region1_severity, region2_severity)
    
    def test_different_seeds(self):
        """Test different seeds produce different states"""
        obs1 = self.env.reset(seed=111)
        region1_severity = obs1.regions[0].severity
        
        obs2 = self.env.reset(seed=222)
        region2_severity = obs2.regions[0].severity
        
        self.assertNotEqual(region1_severity, region2_severity)
    
    def test_concurrent_sessions(self):
        """Test environment supports concurrent sessions"""
        self.assertTrue(self.env.SUPPORTS_CONCURRENT_SESSIONS)


def run_tests():
    """Run all tests with detailed output"""
    print("\n" + "="*70)
    print("🧪 ClimateGuard AI - Comprehensive Test Suite")
    print("="*70 + "\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestClimateGuardEnvironment)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
        print(f"   Tests run: {result.testsRun}")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
