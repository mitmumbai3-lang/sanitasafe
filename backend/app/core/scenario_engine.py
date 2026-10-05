"""
SanitaSafe Climate Scenario Simulation Engine
Perturbs environmental hazard baselines under 4 scenario modes:
1. baseline: Default NASA observations and climatological means.
2. heavier_rain: +20% precipitation intensity, +25% extreme events, higher soil saturation, rising water table (+0.3m shallower).
3. prolonged_drought: -25% rainfall, longer dry spells, dropping soil moisture, regional groundwater depletion, lower water table (+0.8m deeper).
4. compound: Compound climate extremes (alternating prolonged dry spells interrupted by extreme convective storms).

Re-evaluates risk scoring and sanitation option feasibility across all neighborhoods,
generating delta comparisons and 'most changed neighborhoods' shift tracking.
"""

from typing import Dict, Any, List
import copy
from app.core.scoring_engine import score_neighborhood, clamp
from app.core.recommendation_engine import recommend_sanitation_solutions

SCENARIO_DESCRIPTIONS = {
    "baseline": {
        "name": "Current Baseline Climatology",
        "description": "Historical 10-year NASA observations and current regional monitoring."
    },
    "heavier_rain": {
        "name": "Heavier Rainfall (+20% Intensity)",
        "description": "IPCC SSP2-4.5 wet extreme: +20% convective rainfall intensity, +25% flood extent, saturated topsoil, and rising seasonal water table."
    },
    "prolonged_drought": {
        "name": "Prolonged Drought (-25% Rainfall)",
        "description": "Extended meteorological and hydrological drought: -25% rainfall, drop in soil moisture, water table drawdown, and acute municipal water scarcity."
    },
    "compound": {
        "name": "Compound Extremes (Drought + Heavy Storms)",
        "description": "Compound shocks: long severe dry spells interspersed with sudden extreme cloudbursts over baked, impermeable soils."
    }
}

def apply_climate_perturbations(neighborhood: Dict[str, Any], scenario: str) -> Dict[str, Any]:
    """Applies climate scenario delta parameters to neighborhood hazards and hydrogeology."""
    cloned = copy.deepcopy(neighborhood)
    h = cloned.setdefault("hazards", {})

    if scenario == "heavier_rain":
        h["gpm_intensity_95th_mm_hr"] = round(h.get("gpm_intensity_95th_mm_hr", 25.0) * 1.20, 1)
        h["gpm_extreme_event_days"] = int(h.get("gpm_extreme_event_days", 10) * 1.25)
        h["smap_saturation_pct"] = clamp(h.get("smap_saturation_pct", 50.0) * 1.15)
        h["surface_water_inundation_freq_pct"] = clamp(h.get("surface_water_inundation_freq_pct", 20.0) * 1.25)
        # Rising shallow water table (becomes shallower by 0.3m)
        current_wt = cloned.get("water_table_depth_m", 2.0)
        cloned["water_table_depth_m"] = round(max(0.1, current_wt - 0.3), 1)

    elif scenario == "prolonged_drought":
        h["gpm_rainfall_annual_mm"] = round(h.get("gpm_rainfall_annual_mm", 1000.0) * 0.75, 1)
        h["smap_soil_moisture"] = round(max(0.02, h.get("smap_soil_moisture", 0.25) * 0.65), 3)
        h["smap_saturation_pct"] = clamp(h.get("smap_saturation_pct", 50.0) * 0.60)
        h["grace_gw_trend_cm_yr"] = round(h.get("grace_gw_trend_cm_yr", -0.5) - 0.6, 2)
        h["power_heat_index_c"] = round(h.get("power_heat_index_c", 32.0) + 2.5, 1)
        # Water table drops deeper
        current_wt = cloned.get("water_table_depth_m", 2.0)
        cloned["water_table_depth_m"] = round(current_wt + 0.8, 1)

    elif scenario == "compound":
        # Intense storm spikes combined with lower average rainfall and lower baseline water table
        h["gpm_intensity_95th_mm_hr"] = round(h.get("gpm_intensity_95th_mm_hr", 25.0) * 1.25, 1)
        h["gpm_rainfall_annual_mm"] = round(h.get("gpm_rainfall_annual_mm", 1000.0) * 0.80, 1)
        h["smap_soil_moisture"] = round(max(0.04, h.get("smap_soil_moisture", 0.25) * 0.75), 3)
        h["surface_water_inundation_freq_pct"] = clamp(h.get("surface_water_inundation_freq_pct", 20.0) * 1.30)
        h["power_heat_index_c"] = round(h.get("power_heat_index_c", 32.0) + 2.0, 1)

    return cloned

def simulate_region_scenarios(
    region_data: Dict[str, Any],
    selected_scenario: str = "baseline",
    custom_weights: Optional[Dict[str, float]] = None,
    user_priorities: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Simulates baseline and selected scenario, computing deltas and identifying the most changed neighborhoods.
    """
    neighborhoods = region_data.get("neighborhoods", [])
    baseline_results = []
    scenario_results = []
    shifts = []

    for n in neighborhoods:
        # 1. Baseline scoring
        base_score = score_neighborhood(n, custom_weights)
        base_recs = recommend_sanitation_solutions(n, base_score["subindices"], user_priorities)
        base_item = {
            **n,
            "scoring": base_score,
            "recommendations": base_recs
        }
        baseline_results.append(base_item)

        # 2. Perturbed scenario scoring
        perturbed_n = apply_climate_perturbations(n, selected_scenario)
        scen_score = score_neighborhood(perturbed_n, custom_weights)
        scen_recs = recommend_sanitation_solutions(perturbed_n, scen_score["subindices"], user_priorities)
        scen_item = {
            **perturbed_n,
            "scoring": scen_score,
            "recommendations": scen_recs
        }
        scenario_results.append(scen_item)

        # 3. Delta shift calculation
        score_diff = round(scen_score["composite_score"] - base_score["composite_score"], 1)
        tier_shifted = scen_score["risk_tier"] != base_score["risk_tier"]
        base_top_opt = base_recs["recommended_options"][0]["option"]["name"] if base_recs["recommended_options"] else "None"
        scen_top_opt = scen_recs["recommended_options"][0]["option"]["name"] if scen_recs["recommended_options"] else "None"
        opt_changed = base_top_opt != scen_top_opt

        shifts.append({
            "neighborhood_id": n["id"],
            "neighborhood_name": n["name"],
            "baseline_score": base_score["composite_score"],
            "scenario_score": scen_score["composite_score"],
            "score_delta": score_diff,
            "baseline_tier": base_score["risk_tier"],
            "scenario_tier": scen_score["risk_tier"],
            "tier_changed": tier_shifted,
            "baseline_top_recommendation": base_top_opt,
            "scenario_top_recommendation": scen_top_opt,
            "recommendation_shifted": opt_changed
        })

    # Sort shifts by absolute score change descending to identify most impacted areas
    shifts.sort(key=lambda x: abs(x["score_delta"]), reverse=True)

    return {
        "region_id": region_data.get("id"),
        "region_name": region_data.get("name"),
        "scenario": selected_scenario,
        "scenario_metadata": SCENARIO_DESCRIPTIONS.get(selected_scenario, SCENARIO_DESCRIPTIONS["baseline"]),
        "baseline_neighborhoods": baseline_results,
        "scenario_neighborhoods": scenario_results,
        "most_changed_neighborhoods": shifts
    }
