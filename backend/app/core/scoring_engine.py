"""
SanitaSafe Pure Risk Scoring Engine
Calculates normalized 0-100 hazard and vulnerability sub-indices and composite risk scores:
1. Flood Exposure (Rainfall extremes, elevation, flow accumulation, historical inundation)
2. Drought & Water Scarcity Exposure (Soil moisture deficit, rainfall deficit, GRACE groundwater depletion)
3. Groundwater Contamination Risk (Water table depth, soil permeability, latrine density, well proximity)
4. Population Vulnerability (Density, sanitation coverage gaps, disease incidence)

Provides plain-language diagnostic explanations, uncertainty tags, and spatial resolution attribution.
"""

from typing import Dict, Any, List, Optional
import math

# Default planning weights (sum = 1.0)
DEFAULT_WEIGHTS = {
    "flood": 0.30,
    "drought": 0.20,
    "groundwater": 0.30,
    "vulnerability": 0.20
}

# Soil permeability ranking table (higher = faster leaching into groundwater = higher contamination risk)
SOIL_PERMEABILITY_SCORES = {
    "sand": 95.0,
    "sandy_loam": 75.0,
    "loam": 50.0,
    "silt": 45.0,
    "clay_loam": 30.0,
    "clay": 15.0,
    "rocky": 25.0,
    "waterlogged": 90.0
}

def clamp(val: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(max_val, val))

def calculate_flood_subindex(hazards: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flood exposure sub-index (0-100) combining GPM extremes, NASADEM depression, MODIS inundation, and SMAP saturation.
    """
    gpm_intensity = hazards.get("gpm_intensity_95th_mm_hr", 25.0)
    gpm_extreme_days = hazards.get("gpm_extreme_event_days", 10.0)
    nasadem_elevation = hazards.get("nasadem_elevation_m", 20.0)
    nasadem_slope = hazards.get("nasadem_slope_deg", 2.0)
    inundation_freq = hazards.get("surface_water_inundation_freq_pct", 20.0)
    smap_saturation = hazards.get("smap_saturation_pct", 50.0)

    # 1. Rain extremes component (0-100)
    rain_score = clamp(((gpm_intensity - 15.0) / 30.0) * 60.0 + (gpm_extreme_days / 24.0) * 40.0)

    # 2. Elevation & topographic depression component
    # Elevation < 15m in coastal/delta settings represents severe flood risk; flat slopes (<2 deg) prevent runoff drain
    elev_score = clamp((15.0 - min(15.0, nasadem_elevation)) / 15.0 * 70.0 + (5.0 - min(5.0, nasadem_slope)) / 5.0 * 30.0)

    # 3. Direct surface water inundation from satellite
    inund_score = clamp(inundation_freq)

    # 4. Topsoil pre-saturation
    sat_score = clamp(smap_saturation)

    subindex = 0.35 * rain_score + 0.25 * elev_score + 0.25 * inund_score + 0.15 * sat_score
    score = round(clamp(subindex), 1)

    # Determine driving factor
    drivers = []
    if rain_score > 60:
        drivers.append(f"intense rainfall ({gpm_intensity} mm/hr 95th pct)")
    if elev_score > 65:
        drivers.append(f"low-lying topography ({nasadem_elevation}m elevation, {nasadem_slope}° slope)")
    if inund_score > 50:
        drivers.append(f"frequent historical surface water inundation ({inundation_freq}%)")
    if sat_score > 75:
        drivers.append(f"high soil saturation ({smap_saturation}%)")

    return {
        "score": score,
        "components": {
            "rainfall_extremes": round(rain_score, 1),
            "topographic_depression": round(elev_score, 1),
            "historical_inundation": round(inund_score, 1),
            "soil_saturation": round(sat_score, 1)
        },
        "driver_summary": ", ".join(drivers) if drivers else "moderate baseline hydrology",
        "data_sources": "GPM IMERG (10km), NASADEM (30m), MODIS (250m), SMAP (9km)"
    }

def calculate_drought_subindex(hazards: Dict[str, Any]) -> Dict[str, Any]:
    """
    Drought and water scarcity sub-index (0-100) combining SMAP moisture deficit, GPM rain deficit, and GRACE-FO depletion.
    """
    annual_rain = hazards.get("gpm_rainfall_annual_mm", 1000.0)
    soil_moisture = hazards.get("smap_soil_moisture", 0.25)
    grace_trend = hazards.get("grace_gw_trend_cm_yr", -0.5)
    heat_index = hazards.get("power_heat_index_c", 32.0)

    # 1. Soil moisture deficit (0-100): <0.10 m3/m3 is severe arid dryland
    sm_deficit = clamp((0.35 - soil_moisture) / 0.28 * 100.0)

    # 2. Rainfall deficit: <400mm is severe arid
    rain_deficit = clamp((1200.0 - min(1200.0, annual_rain)) / 1000.0 * 100.0)

    # 3. GRACE-FO regional drawdown: <-1.5 cm/yr is rapid aquifer depletion
    grace_score = clamp((-grace_trend - 0.2) / 2.0 * 100.0)

    # 4. Thermal evaporative stress
    heat_score = clamp((heat_index - 28.0) / 14.0 * 100.0)

    subindex = 0.35 * sm_deficit + 0.30 * rain_deficit + 0.25 * grace_score + 0.10 * heat_score
    score = round(clamp(subindex), 1)

    drivers = []
    if sm_deficit > 65:
        drivers.append(f"low soil moisture ({soil_moisture} m³/m³)")
    if rain_deficit > 65:
        drivers.append(f"annual rainfall deficit ({annual_rain} mm/yr)")
    if grace_score > 60:
        drivers.append(f"regional groundwater storage decline ({grace_trend} cm/yr)")
    if heat_score > 60:
        drivers.append(f"high thermal evaporative demand ({heat_index}°C)")

    return {
        "score": score,
        "components": {
            "soil_moisture_deficit": round(sm_deficit, 1),
            "rainfall_deficit": round(rain_deficit, 1),
            "grace_regional_drawdown": round(grace_score, 1),
            "evaporative_heat_stress": round(heat_score, 1)
        },
        "driver_summary": ", ".join(drivers) if drivers else "adequate moisture and water availability",
        "data_sources": "SMAP (9-36km), GPM IMERG (10km), GRACE-FO (~300km regional), NASA POWER (50km)"
    }

def calculate_groundwater_contamination_subindex(
    water_table_depth_m: float,
    soil_type: str,
    distance_to_water_m: float,
    sanitation_coverage: Dict[str, float]
) -> Dict[str, Any]:
    """
    Groundwater contamination sub-index (0-100) evaluating the risk of fecal pathogen transmission into drinking aquifers.
    Key factors:
    - Shallow water table (<1.5m is critical hazard)
    - High soil permeability (sand allows fast pathogen plume movement without filtration)
    - High density of unlined pit latrines
    - Close proximity to drinking water extraction points (<15m)
    """
    # 1. Water table depth hazard (0-100): <=0.5m = 100; >=4.5m = 10
    depth_hazard = clamp((4.5 - min(4.5, max(0.2, water_table_depth_m))) / 4.0 * 100.0)

    # 2. Soil permeability score
    soil_hazard = SOIL_PERMEABILITY_SCORES.get(soil_type.lower(), 50.0)

    # 3. Unlined latrine density
    pit_pct = sanitation_coverage.get("pit_latrine", 30.0)
    od_pct = sanitation_coverage.get("open_defecation", 5.0)
    latrine_hazard = clamp(pit_pct * 1.0 + od_pct * 0.8)

    # 4. Proximity to water points: <=10m = 100; >=60m = 10
    prox_hazard = clamp((60.0 - min(60.0, max(5.0, distance_to_water_m))) / 55.0 * 100.0)

    # Composite: Depth and proximity are the most direct hydrogeological transmission pathways
    subindex = 0.35 * depth_hazard + 0.25 * soil_hazard + 0.20 * latrine_hazard + 0.20 * prox_hazard
    score = round(clamp(subindex), 1)

    drivers = []
    if depth_hazard > 65:
        drivers.append(f"shallow water table ({water_table_depth_m}m depth)")
    if soil_hazard > 65:
        drivers.append(f"highly permeable {soil_type} soil")
    if latrine_hazard > 50:
        drivers.append(f"high unlined pit latrine density ({pit_pct}%)")
    if prox_hazard > 60:
        drivers.append(f"close proximity to drinking water points ({distance_to_water_m}m)")

    return {
        "score": score,
        "components": {
            "water_table_hazard": round(depth_hazard, 1),
            "soil_permeability_hazard": round(soil_hazard, 1),
            "unlined_latrine_density": round(latrine_hazard, 1),
            "water_source_proximity": round(prox_hazard, 1)
        },
        "driver_summary": ", ".join(drivers) if drivers else "safe separation between pits and groundwater",
        "data_sources": "Hydrogeological depth estimates, ISRIC SoilGrids (250m), OSM & community survey"
    }

def calculate_vulnerability_subindex(
    population: int,
    area_km2: float,
    sanitation_coverage: Dict[str, float],
    annual_diarrhea_cholera_cases: int
) -> Dict[str, Any]:
    """
    Population vulnerability sub-index (0-100) assessing exposure density, infrastructure deficit, and health burden.
    """
    density_km2 = population / max(0.1, area_km2)

    # 1. Density score: 5,000 to 50,000+ people/km2
    density_score = clamp(((density_km2 - 5000.0) / 45000.0) * 100.0)

    # 2. Coverage gap (% unimproved: pit_latrine + open_defecation)
    pit_pct = sanitation_coverage.get("pit_latrine", 30.0)
    od_pct = sanitation_coverage.get("open_defecation", 5.0)
    shared_pct = sanitation_coverage.get("shared_public", 15.0)
    gap_score = clamp(od_pct * 1.5 + pit_pct * 0.5 + shared_pct * 0.4)

    # 3. Disease incidence per 1,000 residents: 1 to 8 cases/1000
    rate_per_1k = (annual_diarrhea_cholera_cases / max(100, population)) * 1000.0
    disease_score = clamp((rate_per_1k / 7.0) * 100.0)

    subindex = 0.35 * density_score + 0.35 * gap_score + 0.30 * disease_score
    score = round(clamp(subindex), 1)

    drivers = []
    if density_score > 60:
        drivers.append(f"dense informal settlement ({int(density_km2):,} people/km²)")
    if gap_score > 55:
        drivers.append(f"high unimproved sanitation gap ({od_pct}% OD, {pit_pct}% unlined pits)")
    if disease_score > 55:
        drivers.append(f"recurrent waterborne outbreak burden ({rate_per_1k:.1f} cases/1,000)")

    return {
        "score": score,
        "components": {
            "population_density": round(density_score, 1),
            "sanitation_coverage_gap": round(gap_score, 1),
            "disease_incidence_burden": round(disease_score, 1)
        },
        "population_density_per_km2": int(density_km2),
        "disease_rate_per_1000": round(rate_per_1k, 1),
        "driver_summary": ", ".join(drivers) if drivers else "moderate demographic vulnerability",
        "data_sources": "WorldPop (100m) & Municipal Public Health Registry"
    }

def score_neighborhood(
    neighborhood: Dict[str, Any],
    custom_weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Computes complete composite risk score and 4 sub-indices for a given neighborhood unit.
    Returns composite score (0-100), risk tier, sub-indices, and plain-language driver explanation.
    """
    weights = custom_weights or DEFAULT_WEIGHTS
    # Normalize weights so they always sum to 1.0
    w_sum = sum(weights.values()) or 1.0
    norm_w = {k: v / w_sum for k, v in weights.items()}

    hazards = neighborhood.get("hazards", {})
    flood = calculate_flood_subindex(hazards)
    drought = calculate_drought_subindex(hazards)
    groundwater = calculate_groundwater_contamination_subindex(
        water_table_depth_m=neighborhood.get("water_table_depth_m", 2.0),
        soil_type=neighborhood.get("soil_type", "loam"),
        distance_to_water_m=neighborhood.get("distance_to_water_source_m", 25.0),
        sanitation_coverage=neighborhood.get("sanitation_coverage", {})
    )
    vulnerability = calculate_vulnerability_subindex(
        population=neighborhood.get("population", 50000),
        area_km2=neighborhood.get("area_km2", 1.0),
        sanitation_coverage=neighborhood.get("sanitation_coverage", {}),
        annual_diarrhea_cholera_cases=neighborhood.get("annual_diarrhea_cholera_cases", 200)
    )

    composite = (
        norm_w["flood"] * flood["score"] +
        norm_w["drought"] * drought["score"] +
        norm_w["groundwater"] * groundwater["score"] +
        norm_w["vulnerability"] * vulnerability["score"]
    )
    composite_score = round(clamp(composite), 1)

    # Classify Risk Tier
    if composite_score >= 75.0:
        tier = "Critical Hotspot"
        tier_code = "critical"
        color = "#b91c1c"  # deep red / accessible
    elif composite_score >= 55.0:
        tier = "High Risk"
        tier_code = "high"
        color = "#c2410c"  # orange-red
    elif composite_score >= 35.0:
        tier = "Moderate Risk"
        tier_code = "moderate"
        color = "#d97706"  # amber
    else:
        tier = "Low Risk"
        tier_code = "low"
        color = "#15803d"  # emerald green

    # Identify primary driving subindex
    subindex_map = {
        "Flood Exposure": (flood["score"], flood["driver_summary"]),
        "Groundwater Contamination": (groundwater["score"], groundwater["driver_summary"]),
        "Drought & Scarcity": (drought["score"], drought["driver_summary"]),
        "Population Vulnerability": (vulnerability["score"], vulnerability["driver_summary"])
    }
    sorted_drivers = sorted(subindex_map.items(), key=lambda x: x[1][0], reverse=True)
    primary_name, (primary_val, primary_detail) = sorted_drivers[0]

    plain_explanation = (
        f"Overall risk is {tier.lower()} ({composite_score}/100), primarily driven by {primary_name} ({primary_val}/100) "
        f"due to {primary_detail}."
    )

    return {
        "neighborhood_id": neighborhood.get("id"),
        "neighborhood_name": neighborhood.get("name"),
        "composite_score": composite_score,
        "risk_tier": tier,
        "risk_tier_code": tier_code,
        "color_code": color,
        "subindices": {
            "flood": flood,
            "drought": drought,
            "groundwater": groundwater,
            "vulnerability": vulnerability
        },
        "weights_used": norm_w,
        "primary_driver": primary_name,
        "plain_explanation": plain_explanation,
        "water_table_is_estimate": neighborhood.get("water_table_is_estimate", True)
    }
