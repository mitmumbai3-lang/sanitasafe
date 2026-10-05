from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import json
import os
from app.seeds.demo_regions import DEMO_REGIONS

router = APIRouter(prefix="/regions", tags=["Regions & Catalog"])

@router.get("")
def list_regions() -> List[Dict[str, Any]]:
    """Return overview list of pre-calibrated demo regions."""
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "country": r["country"],
            "climate_type": r["climate_type"],
            "description": r["description"],
            "center": r["center"],
            "zoom": r["zoom"],
            "neighborhood_count": len(r["neighborhoods"])
        }
        for r in DEMO_REGIONS.values()
    ]

@router.get("/{region_id}")
def get_region_detail(region_id: str) -> Dict[str, Any]:
    """Return full spatial and demographic dataset for a specific region."""
    region = DEMO_REGIONS.get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=f"Region '{region_id}' not found.")
    return region

@router.get("/options/sanitation")
def get_sanitation_options() -> List[Dict[str, Any]]:
    """Return complete database of all 9 sanitation technologies with attributes."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "seeds", "sanitation_options.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed loading sanitation database: {str(e)}")
