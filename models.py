"""
Pydantic models for ClimateGuard AI Environment
"""

from typing import List, Optional, Dict, Literal
from pydantic import Field, BaseModel

try:
    from openenv.core.env_server import Action, Observation, State
except ImportError:
    class Action(BaseModel):
        pass
    class Observation(BaseModel):
        done: bool = False
        reward: Optional[float] = None
    class State(BaseModel):
        episode_id: Optional[str] = None
        step_count: int = 0


class RegionData(BaseModel):
    """Data for each geographic region"""
    region_id: int
    region_name: str
    crisis_type: Literal["WILDFIRE", "FLOOD", "DROUGHT", "HURRICANE", "HEATWAVE"]
    severity: float = Field(ge=0.0, le=1.0)
    population: int = Field(gt=0)
    evacuated: int = Field(ge=0)
    casualties: int = Field(ge=0)
    infrastructure_damage: float = Field(ge=0.0, le=1.0)
    water_supply: float = Field(ge=0.0, le=1.0)
    power_grid: float = Field(ge=0.0, le=1.0)
    hospital_capacity: float = Field(ge=0.0, le=1.0)
    food_supply_days: float = Field(ge=0.0)
    temperature_celsius: float
    air_quality_index: int = Field(ge=0, le=500)
    wind_speed_kmh: float = Field(ge=0.0)
    precipitation_mm: float = Field(ge=0.0)
    fire_spread_risk: float = Field(ge=0.0, le=1.0)
    flood_risk: float = Field(ge=0.0, le=1.0)
    neighboring_regions: List[int] = Field(default_factory=list)
    climate_trend: Literal["WORSENING", "STABLE", "IMPROVING"] = "STABLE"


class GlobalResources(BaseModel):
    """Available global resources"""
    firefighting_units: int = Field(default=0, ge=0)
    flood_rescue_boats: int = Field(default=0, ge=0)
    medical_teams: int = Field(default=0, ge=0)
    evacuation_buses: int = Field(default=0, ge=0)
    helicopters: int = Field(default=0, ge=0)
    water_tankers: int = Field(default=0, ge=0)
    food_supplies_tons: float = Field(default=0.0, ge=0.0)
    emergency_shelters: int = Field(default=0, ge=0)
    power_generators: int = Field(default=0, ge=0)
    communication_satellites: int = Field(default=0, ge=0)
    budget_millions: float = Field(default=0.0, ge=0.0)


class ClimateAction(Action):
    """Agent actions for climate crisis response"""
    firefighting_allocation: Dict[str, int] = Field(default_factory=dict)
    flood_rescue_allocation: Dict[str, int] = Field(default_factory=dict)
    medical_allocation: Dict[str, int] = Field(default_factory=dict)
    evacuation_allocation: Dict[str, int] = Field(default_factory=dict)
    power_restoration: List[int] = Field(default_factory=list)
    water_supply_restoration: List[int] = Field(default_factory=list)
    firebreaks: List[int] = Field(default_factory=list)
    flood_barriers: List[int] = Field(default_factory=list)
    evacuation_orders: List[int] = Field(default_factory=list)
    food_distribution: Dict[str, float] = Field(default_factory=dict)
    water_distribution: Dict[str, int] = Field(default_factory=dict)
    satellite_coverage: List[int] = Field(default_factory=list)
    priority_regions: List[int] = Field(default_factory=list)


class ClimateObservation(Observation):
    """Observation returned after each step"""
    regions: List[RegionData] = Field(default_factory=list)
    resources: GlobalResources = Field(default_factory=GlobalResources)
    day: int = Field(ge=0)
    total_casualties: int = Field(ge=0)
    total_evacuated: int = Field(ge=0)
    total_population_at_risk: int = Field(ge=0)
    global_temperature_anomaly: float = 0.0
    co2_ppm: float = 420.0
    new_crises: List[str] = Field(default_factory=list)
    resolved_crises: List[int] = Field(default_factory=list)
    cascade_events: List[str] = Field(default_factory=list)
    response_efficiency: float = Field(ge=0.0, le=1.0, default=0.0)
    resource_utilization: float = Field(ge=0.0, le=1.0, default=0.0)
    equity_score: float = Field(ge=0.0, le=1.0, default=1.0)
    outcome_summary: str = ""
    task_description: str = ""


class ClimateEpisodeState(State):
    """Episode state information"""
    scenario_type: Literal["SINGLE_CRISIS", "MULTI_CRISIS", "CASCADE", "EXTREME"] = "MULTI_CRISIS"
    difficulty: Literal["EASY", "MEDIUM", "HARD", "EXPERT", "NIGHTMARE"] = "MEDIUM"
    num_regions: int = 10
    max_days: int = 15
    initial_budget_millions: float = 500.0
    climate_scenario: str = "RCP4.5"
    baseline_human_score: float = 0.65
    task_id: str = "multi_crisis_response"
