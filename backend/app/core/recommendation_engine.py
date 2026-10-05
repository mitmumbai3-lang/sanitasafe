"""
SanitaSafe Pure Solution Recommender
Implements:
1. Deterministic Hard Exclusion Rules based on environmental constraints:
   - Water table depth vs minimum safe separation
   - Well/water point proximity buffer
   - Severe water scarcity vs water flush requirements
   - Flood inundation vs flood tolerance
   - Soil permeability vs percolation requirements
2. Multi-Criteria Ranking based on environmental alignment and user priorities:
   - Budget / capital cost sensitivity
   - Maintenance capacity
   - Circular economy & resource recovery (compost, biogas, urine fertilizer)
   - Settlement density and space constraints
3. Plain-language explanations for every excluded and recommended option.
"""

from typing import Dict, Any, List, Optional
import json
import os

def load_sanitation_options() -> List[Dict[str, Any]]:
    path = os.path.join(os.path.dirname(__file__), "..", "seeds", "sanitation_options.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_hard_exclusions(
    option: Dict[str, Any],
    neighborhood: Dict[str, Any],
    subindices: Dict[str, Any]
) -> Optional[str]:
    """
    Checks if a sanitation option violates any physical or hydrogeological hard exclusion rules.
    Returns None if viable, or a plain-language string explaining why it was excluded.
    """
    water_table_depth = float(neighborhood.get("water_table_depth_m", 2.0))
    soil_type = str(neighborhood.get("soil_type", "loam")).lower()
    dist_water = float(neighborhood.get("distance_to_water_source_m", 30.0))
    flood_score = float(subindices.get("flood", {}).get("score", 30.0))
    drought_score = float(subindices.get("drought", {}).get("score", 30.0))

    # Rule 1: Water table depth rule for in-ground leaching systems
    min_wt_required = float(option.get("min_water_table_depth_m", 0.0))
    if min_wt_required > 0.0 and water_table_depth < min_wt_required:
        return (
            f"Excluded: Water table depth ({water_table_depth}m) is shallower than the safe minimum requirement of {min_wt_required}m. "
            f"Fecal pathogens and nitrates will leach directly into the shallow aquifer."
        )

    # Rule 2: Drinking water source proximity buffer (WHO 15m minimum; 30m for coarse sand)
    if option.get("requires_permeable_soil", False) or option["id"] in ["lined_pit_latrine", "twin_pit_pour_flush", "septic_tank_soak_pit"]:
        safe_buffer = 30.0 if "sand" in soil_type else 15.0
        if dist_water < safe_buffer:
            return (
                f"Excluded: Distance to drinking water points ({dist_water}m) is less than the required safe setback "
                f"({safe_buffer}m in {soil_type} soil). High probability of cross-contaminating drinking water."
            )

    # Rule 3: Water scarcity / drought incompatibility
    if option.get("requires_piped_water", False) and drought_score > 60.0:
        return (
            f"Excluded: Requires dependable piped water or pour-flush supply. "
            f"Unviable under severe local water scarcity and drought conditions (Drought Risk: {drought_score}/100)."
        )

    # Rule 4: Flood inundation vulnerability
    if option.get("flood_tolerance") == "low" and flood_score > 55.0:
        return (
            f"Excluded: Vulnerable to flood inundation (Flood Exposure: {flood_score}/100). "
            f"Ground-level unsealed pits will overflow and spread waterborne pathogens during seasonal flooding."
        )

    # Rule 5: Heavy impermeable clay soil prevents soakaway percolation
    if option.get("requires_permeable_soil", False) and soil_type == "clay":
        return (
            f"Excluded: Dense impermeable clay soil cannot absorb soakaway or leaching pit effluent, "
            f"causing surface ponding and rapid system failure."
        )

    return None

def score_viable_option(
    option: Dict[str, Any],
    neighborhood: Dict[str, Any],
    subindices: Dict[str, Any],
    user_priorities: Dict[str, float]
) -> Dict[str, Any]:
    """
    Ranks viable options using a multi-criteria model incorporating environmental fit and community priorities.
    """
    flood_score = float(subindices.get("flood", {}).get("score", 30.0))
    drought_score = float(subindices.get("drought", {}).get("score", 30.0))
    gw_score = float(subindices.get("groundwater", {}).get("score", 30.0))

    # Priority weights
    w_budget = user_priorities.get("budget_sensitivity", 0.35)
    w_maint = user_priorities.get("low_maintenance", 0.25)
    w_reuse = user_priorities.get("circular_reuse", 0.20)
    w_env = user_priorities.get("climate_resilience", 0.20)

    # 1. Climate Resilience Match (0-100)
    cr_score = 60.0
    if flood_score > 60.0 and option.get("flood_tolerance") == "high":
        cr_score += 25.0
    if drought_score > 60.0 and option.get("water_requirement") == "none":
        cr_score += 25.0
    if gw_score > 60.0 and option.get("health_protection_level") == "safely_managed":
        cr_score += 20.0
    cr_score = min(100.0, cr_score)

    # 2. Cost / Budget Score (0-100)
    capex_map = {"$": 100.0, "$$": 75.0, "$$$": 45.0, "$$$$": 20.0}
    opex_map = {"$": 100.0, "$$": 75.0, "$$$": 45.0, "$$$$": 20.0}
    capex_score = capex_map.get(option.get("relative_capex", "$$"), 70.0)
    opex_score = opex_map.get(option.get("relative_opex", "$$"), 70.0)
    budget_score = 0.6 * capex_score + 0.4 * opex_score

    # 3. Maintenance Simplicity (0-100)
    maint_map = {"low": 100.0, "medium": 65.0, "high": 30.0}
    maint_score = maint_map.get(option.get("maintenance_complexity", "medium"), 65.0)

    # 4. Circular Reuse & Resource Recovery (0-100)
    reuse_items = option.get("reuse_potential", [])
    has_reuse = len(reuse_items) > 0 and "none" not in reuse_items
    reuse_score = 100.0 if has_reuse else 25.0

    # Composite Match Score
    match_score = (
        w_env * cr_score +
        w_budget * budget_score +
        w_maint * maint_score +
        w_reuse * reuse_score
    )
    match_score = round(min(100.0, max(0.0, match_score)), 1)

    # Plain language recommendation rationale
    highlights = []
    if option.get("flood_tolerance") == "high" and flood_score > 50:
        highlights.append("high flood immunity")
    if option.get("water_requirement") == "none" and drought_score > 50:
        highlights.append("zero water consumption in drought")
    if has_reuse:
        highlights.append(f"resource recovery ({', '.join(reuse_items)})")
    if option.get("relative_capex") == "$":
        highlights.append("minimal capital investment")
    if option.get("maintenance_complexity") == "low":
        highlights.append("simple community-led maintenance")

    why_text = (
        f"Strong candidate ({match_score}/100 match): " +
        (", ".join(highlights) if highlights else "balanced cost and operational fit") + "."
    )

    return {
        "match_score": match_score,
        "climate_resilience_score": round(cr_score, 1),
        "budget_score": round(budget_score, 1),
        "maintenance_score": round(maint_score, 1),
        "circular_reuse_score": round(reuse_score, 1),
        "recommendation_rationale": why_text
    }

def recommend_sanitation_solutions(
    neighborhood: Dict[str, Any],
    subindices: Dict[str, Any],
    user_priorities: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Evaluates all sanitation options for a neighborhood:
    - Segregates options into 'recommended' and 'excluded'
    - Annotates every excluded option with transparent physical reasons
    - Ranks viable options by multi-criteria match score
    """
    priorities = user_priorities or {
        "budget_sensitivity": 0.35,
        "low_maintenance": 0.25,
        "circular_reuse": 0.20,
        "climate_resilience": 0.20
    }

    all_options = load_sanitation_options()
    viable_list = []
    excluded_list = []

    for opt in all_options:
        exclusion_reason = evaluate_hard_exclusions(opt, neighborhood, subindices)
        if exclusion_reason:
            excluded_list.append({
                "option": opt,
                "is_viable": False,
                "exclusion_reason": exclusion_reason
            })
        else:
            scoring_res = score_viable_option(opt, neighborhood, subindices, priorities)
            viable_list.append({
                "option": opt,
                "is_viable": True,
                **scoring_res
            })

    # Sort viable options by match score descending
    viable_list.sort(key=lambda x: x["match_score"], reverse=True)

    # Top recommendation summary in plain language
    if viable_list:
        top_name = viable_list[0]["option"]["name"]
        top_reason = viable_list[0]["recommendation_rationale"]
        summary = f"Top recommended solution is {top_name} ({viable_list[0]['match_score']}/100). {top_reason}"
    else:
        summary = "No standard on-site options meet all physical safety criteria; customized elevated or container systems required."

    return {
        "neighborhood_id": neighborhood.get("id"),
        "neighborhood_name": neighborhood.get("name"),
        "viable_count": len(viable_list),
        "excluded_count": len(excluded_list),
        "recommended_options": viable_list,
        "excluded_options": excluded_list,
        "summary": summary
    }
