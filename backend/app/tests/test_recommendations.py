import pytest
from app.core.recommendation_engine import (
    load_sanitation_options,
    evaluate_hard_exclusions,
    recommend_sanitation_solutions
)

def test_load_sanitation_options():
    options = load_sanitation_options()
    assert len(options) == 9
    ids = [o["id"] for o in options]
    assert "raised_latrine" in ids
    assert "lined_pit_latrine" in ids
    assert "uddt" in ids
    assert "composting_toilet" in ids
    assert "septic_tank_soak_pit" in ids
    assert "twin_pit_pour_flush" in ids
    assert "cbs_container_sanitation" in ids
    assert "dewats_constructed_wetlands" in ids
    assert "sewered_connection" in ids

def test_exclusion_shallow_water_table():
    # Shallow water table: 0.8m (like Dhaka delta or Maputo coast)
    neighborhood = {
        "water_table_depth_m": 0.8,
        "soil_type": "sand",
        "distance_to_water_source_m": 35.0
    }
    subindices = {"flood": {"score": 30.0}, "drought": {"score": 20.0}}

    options = load_sanitation_options()
    septic_opt = next(o for o in options if o["id"] == "septic_tank_soak_pit")
    pit_opt = next(o for o in options if o["id"] == "lined_pit_latrine")
    cbs_opt = next(o for o in options if o["id"] == "cbs_container_sanitation")
    uddt_opt = next(o for o in options if o["id"] == "uddt")

    # Septic requires 2.5m, Pit requires 1.5m -> both should be excluded
    assert evaluate_hard_exclusions(septic_opt, neighborhood, subindices) is not None
    assert "shallower than the safe minimum" in evaluate_hard_exclusions(septic_opt, neighborhood, subindices)

    assert evaluate_hard_exclusions(pit_opt, neighborhood, subindices) is not None
    assert "shallower than the safe minimum" in evaluate_hard_exclusions(pit_opt, neighborhood, subindices)

    # CBS and UDDT are completely sealed above ground -> should NOT be excluded
    assert evaluate_hard_exclusions(cbs_opt, neighborhood, subindices) is None
    assert evaluate_hard_exclusions(uddt_opt, neighborhood, subindices) is None

def test_exclusion_well_proximity():
    # Pit latrine too close to drinking water well (10m away in sandy soil)
    neighborhood = {
        "water_table_depth_m": 3.0,
        "soil_type": "sand",
        "distance_to_water_source_m": 10.0
    }
    subindices = {"flood": {"score": 30.0}, "drought": {"score": 20.0}}

    options = load_sanitation_options()
    pit_opt = next(o for o in options if o["id"] == "lined_pit_latrine")
    reason = evaluate_hard_exclusions(pit_opt, neighborhood, subindices)
    assert reason is not None
    assert "safe setback" in reason

def test_exclusion_severe_drought():
    # Severe water scarcity: drought subindex 75/100
    neighborhood = {
        "water_table_depth_m": 4.0,
        "soil_type": "loam",
        "distance_to_water_source_m": 40.0
    }
    subindices = {"flood": {"score": 20.0}, "drought": {"score": 75.0}}

    options = load_sanitation_options()
    sewer_opt = next(o for o in options if o["id"] == "sewered_connection")
    uddt_opt = next(o for o in options if o["id"] == "uddt")

    # Sewers require copious water -> excluded
    assert evaluate_hard_exclusions(sewer_opt, neighborhood, subindices) is not None
    assert "piped water" in evaluate_hard_exclusions(sewer_opt, neighborhood, subindices)

    # UDDT uses zero water -> viable
    assert evaluate_hard_exclusions(uddt_opt, neighborhood, subindices) is None

def test_exclusion_impermeable_clay():
    neighborhood = {
        "water_table_depth_m": 4.0,
        "soil_type": "clay",
        "distance_to_water_source_m": 40.0
    }
    subindices = {"flood": {"score": 20.0}, "drought": {"score": 20.0}}

    options = load_sanitation_options()
    septic_opt = next(o for o in options if o["id"] == "septic_tank_soak_pit")
    assert evaluate_hard_exclusions(septic_opt, neighborhood, subindices) is not None
    assert "clay" in evaluate_hard_exclusions(septic_opt, neighborhood, subindices).lower()

def test_full_recommender_output():
    neighborhood = {
        "id": "kamrangirchar",
        "name": "Kamrangirchar Island",
        "water_table_depth_m": 0.8,
        "soil_type": "silt",
        "distance_to_water_source_m": 12.0
    }
    subindices = {
        "flood": {"score": 72.0},
        "drought": {"score": 20.0},
        "groundwater": {"score": 85.0},
        "vulnerability": {"score": 78.0}
    }
    rec_result = recommend_sanitation_solutions(neighborhood, subindices)
    assert rec_result["viable_count"] > 0
    assert rec_result["excluded_count"] > 0
    assert len(rec_result["recommended_options"]) == rec_result["viable_count"]
    # Check that highest viable option is elevated or container based
    top_opt_id = rec_result["recommended_options"][0]["option"]["id"]
    assert top_opt_id in ["raised_latrine", "cbs_container_sanitation", "uddt"]
    assert "Top recommended solution is" in rec_result["summary"]
