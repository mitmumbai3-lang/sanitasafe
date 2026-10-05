import pytest
from app.core.scenario_engine import (
    apply_climate_perturbations,
    simulate_region_scenarios
)
from app.seeds.demo_regions import DEMO_REGIONS

def test_heavier_rain_perturbation():
    base_n = DEMO_REGIONS["dhaka"]["neighborhoods"][0]
    perturbed = apply_climate_perturbations(base_n, "heavier_rain")
    assert perturbed["hazards"]["gpm_intensity_95th_mm_hr"] > base_n["hazards"]["gpm_intensity_95th_mm_hr"]
    assert perturbed["water_table_depth_m"] <= base_n["water_table_depth_m"]

def test_prolonged_drought_perturbation():
    base_n = DEMO_REGIONS["nairobi"]["neighborhoods"][0]
    perturbed = apply_climate_perturbations(base_n, "prolonged_drought")
    assert perturbed["hazards"]["gpm_rainfall_annual_mm"] < base_n["hazards"]["gpm_rainfall_annual_mm"]
    assert perturbed["hazards"]["smap_soil_moisture"] < base_n["hazards"]["smap_soil_moisture"]
    assert perturbed["water_table_depth_m"] > base_n["water_table_depth_m"]

def test_simulate_region_scenarios_dhaka():
    dhaka_data = DEMO_REGIONS["dhaka"]
    sim = simulate_region_scenarios(dhaka_data, selected_scenario="heavier_rain")
    assert sim["scenario"] == "heavier_rain"
    assert len(sim["baseline_neighborhoods"]) == len(dhaka_data["neighborhoods"])
    assert len(sim["scenario_neighborhoods"]) == len(dhaka_data["neighborhoods"])
    assert len(sim["most_changed_neighborhoods"]) == len(dhaka_data["neighborhoods"])
    # First in most changed has a delta
    first_shift = sim["most_changed_neighborhoods"][0]
    assert "score_delta" in first_shift
    assert "baseline_score" in first_shift
    assert "scenario_score" in first_shift
