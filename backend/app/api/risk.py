from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.seeds.demo_regions import DEMO_REGIONS
from app.core.scoring_engine import score_neighborhood, DEFAULT_WEIGHTS
from app.core.recommendation_engine import recommend_sanitation_solutions
from app.core.scenario_engine import simulate_region_scenarios

router = APIRouter(prefix="/risk", tags=["Risk Scoring & Recommender"])

class CustomEvaluationRequest(BaseModel):
    neighborhood: Dict[str, Any]
    custom_weights: Optional[Dict[str, float]] = None
    user_priorities: Optional[Dict[str, float]] = None

@router.get("/region/{region_id}")
def get_region_risk_and_recommendations(
    region_id: str,
    scenario: str = Query("baseline", description="baseline | heavier_rain | prolonged_drought | compound"),
    flood_weight: float = Query(0.30, ge=0.0, le=1.0),
    drought_weight: float = Query(0.20, ge=0.0, le=1.0),
    groundwater_weight: float = Query(0.30, ge=0.0, le=1.0),
    vulnerability_weight: float = Query(0.20, ge=0.0, le=1.0),
    budget_priority: float = Query(0.35, ge=0.0, le=1.0),
    maintenance_priority: float = Query(0.25, ge=0.0, le=1.0),
    circular_reuse_priority: float = Query(0.20, ge=0.0, le=1.0),
    climate_resilience_priority: float = Query(0.20, ge=0.0, le=1.0)
) -> Dict[str, Any]:
    """
    Evaluates risk and sanitation recommendations across all neighborhoods in a region
    under the selected climate scenario with customizable weights and priorities.
    """
    region = DEMO_REGIONS.get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=f"Region '{region_id}' not found.")

    custom_weights = {
        "flood": flood_weight,
        "drought": drought_weight,
        "groundwater": groundwater_weight,
        "vulnerability": vulnerability_weight
    }
    user_priorities = {
        "budget_sensitivity": budget_priority,
        "low_maintenance": maintenance_priority,
        "circular_reuse": circular_reuse_priority,
        "climate_resilience": climate_resilience_priority
    }

    sim_result = simulate_region_scenarios(
        region_data=region,
        selected_scenario=scenario,
        custom_weights=custom_weights,
        user_priorities=user_priorities
    )
    return sim_result

@router.post("/evaluate")
def evaluate_custom_neighborhood(req: CustomEvaluationRequest) -> Dict[str, Any]:
    """
    Evaluates an ad-hoc or user-drawn/uploaded neighborhood polygon with custom parameters.
    """
    score_res = score_neighborhood(req.neighborhood, req.custom_weights)
    rec_res = recommend_sanitation_solutions(req.neighborhood, score_res["subindices"], req.user_priorities)

    return {
        "neighborhood": req.neighborhood,
        "scoring": score_res,
        "recommendations": rec_res
    }
