import pytest
from app.core.scoring_engine import (
    calculate_flood_subindex,
    calculate_drought_subindex,
    calculate_groundwater_contamination_subindex,
    calculate_vulnerability_subindex,
    score_neighborhood,
    clamp
)

def test_clamp_utility():
    assert clamp(150, 0, 100) == 100.0
    assert clamp(-20, 0, 100) == 0.0
    assert clamp(55.5, 0, 100) == 55.5

def test_flood_subindex_high_hazard():
    extreme_hazards = {
        "gpm_intensity_95th_mm_hr": 45.0,
        "gpm_extreme_event_days": 25,
        "nasadem_elevation_m": 2.0,
        "nasadem_slope_deg": 0.5,
        "surface_water_inundation_freq_pct": 80.0,
        "smap_saturation_pct": 95.0
    }
    result = calculate_flood_subindex(extreme_hazards)
    assert 0 <= result["score"] <= 100
    assert result["score"] >= 80.0, f"Expected high flood score, got {result['score']}"
    assert "intense rainfall" in result["driver_summary"]
    assert "low-lying topography" in result["driver_summary"]

def test_flood_subindex_dry_highland():
    arid_hazards = {
        "gpm_intensity_95th_mm_hr": 15.0,
        "gpm_extreme_event_days": 2,
        "nasadem_elevation_m": 1800.0,
        "nasadem_slope_deg": 8.0,
        "surface_water_inundation_freq_pct": 2.0,
        "smap_saturation_pct": 10.0
    }
    result = calculate_flood_subindex(arid_hazards)
    assert result["score"] <= 20.0

def test_drought_subindex_arid_extremes():
    arid_hazards = {
        "gpm_rainfall_annual_mm": 180.0,
        "smap_soil_moisture": 0.05,
        "grace_gw_trend_cm_yr": -2.5,
        "power_heat_index_c": 44.0
    }
    result = calculate_drought_subindex(arid_hazards)
    assert result["score"] >= 80.0
    assert "low soil moisture" in result["driver_summary"]
    assert "annual rainfall deficit" in result["driver_summary"]

def test_groundwater_contamination_shallow_water_table_sandy_soil():
    # Maputo-style coastal high water table + sandy soil + pits near wells
    result = calculate_groundwater_contamination_subindex(
        water_table_depth_m=0.7,
        soil_type="sand",
        distance_to_water_m=10.0,
        sanitation_coverage={"pit_latrine": 70, "open_defecation": 5}
    )
    assert result["score"] >= 80.0
    assert "shallow water table" in result["driver_summary"]
    assert "highly permeable sand soil" in result["driver_summary"]

def test_groundwater_contamination_deep_water_table_clay():
    # Deep water table (5m), clay soil, far from wells (80m)
    result = calculate_groundwater_contamination_subindex(
        water_table_depth_m=5.5,
        soil_type="clay",
        distance_to_water_m=80.0,
        sanitation_coverage={"pit_latrine": 20, "open_defecation": 0}
    )
    assert result["score"] <= 30.0

def test_vulnerability_subindex():
    result = calculate_vulnerability_subindex(
        population=120000,
        area_km2=1.0,
        sanitation_coverage={"pit_latrine": 50, "open_defecation": 20, "shared_public": 20},
        annual_diarrhea_cholera_cases=800
    )
    assert result["score"] >= 70.0
    assert result["population_density_per_km2"] == 120000

def test_score_neighborhood_composite():
    mock_neighborhood = {
        "id": "test_ward",
        "name": "Test Ward",
        "population": 100000,
        "area_km2": 1.5,
        "water_table_depth_m": 0.9,
        "soil_type": "sand",
        "distance_to_water_source_m": 12.0,
        "sanitation_coverage": {"pit_latrine": 65, "open_defecation": 10, "shared_public": 15},
        "annual_diarrhea_cholera_cases": 650,
        "hazards": {
            "gpm_intensity_95th_mm_hr": 42.0,
            "gpm_extreme_event_days": 20,
            "nasadem_elevation_m": 3.0,
            "nasadem_slope_deg": 0.7,
            "surface_water_inundation_freq_pct": 70.0,
            "smap_saturation_pct": 90.0,
            "gpm_rainfall_annual_mm": 2100.0,
            "smap_soil_moisture": 0.42,
            "grace_gw_trend_cm_yr": -0.8,
            "power_heat_index_c": 36.0
        }
    }
    scored = score_neighborhood(mock_neighborhood)
    assert scored["composite_score"] >= 68.0
    assert scored["risk_tier"] in ["Critical Hotspot", "High Risk"]
    assert "Overall risk is" in scored["plain_explanation"]
    assert "subindices" in scored
    assert all(k in scored["subindices"] for k in ["flood", "drought", "groundwater", "vulnerability"])
