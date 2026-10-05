from typing import Dict, Any, Optional
from app.data_services.base import BaseDataClient
import requests

class SoilGridsClient(BaseDataClient):
    """
    ISRIC SoilGrids 250m Global Gridded Soil Information
    Spatial Resolution: 250 m
    Provides sand, silt, and clay fractions, soil texture classification, and hydraulic conductivity (permeability proxy)
    to determine soakaway, pit leaching, and infiltration viability.
    """
    def __init__(self):
        super().__init__(
            dataset_name="ISRIC SoilGrids v2.0 Global 250m",
            spatial_resolution="250 m grid",
            temporal_resolution="Standardized baseline profile (0-30 cm root-zone depth)",
            uncertainty_note="Machine-learning spatial prediction trained on WoSIS profile data; local fills or urban engineered soils may vary from regional predictions."
        )

    def fetch_live(self, lat: float, lon: float, **kwargs) -> Optional[Dict[str, Any]]:
        # Query ISRIC REST endpoint with short timeout
        url = (
            f"https://rest.isric.org/soilgrids/v2.0/properties/query?"
            f"lon={round(lon, 4)}&lat={round(lat, 4)}&property=clay&property=sand&property=silt&depth=15-30cm&value=mean"
        )
        try:
            resp = requests.get(url, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                layers = {lyr["name"]: lyr for lyr in data.get("properties", {}).get("layers", [])}
                clay_val = layers.get("clay", {}).get("depths", [{}])[0].get("values", {}).get("mean", 250) / 10.0
                sand_val = layers.get("sand", {}).get("depths", [{}])[0].get("values", {}).get("mean", 400) / 10.0
                silt_val = layers.get("silt", {}).get("depths", [{}])[0].get("values", {}).get("mean", 350) / 10.0

                texture = self._classify_texture(sand_val, silt_val, clay_val)
                ksat_proxy = self._estimate_permeability(sand_val, clay_val)

                return {
                    "sand_pct": round(sand_val, 1),
                    "silt_pct": round(silt_val, 1),
                    "clay_pct": round(clay_val, 1),
                    "soil_texture_class": texture,
                    "hydraulic_conductivity_ksat_cm_day": ksat_proxy["ksat_cm_day"],
                    "permeability_rating": ksat_proxy["rating"],
                    "soakaway_suitability": ksat_proxy["suitability"]
                }
        except Exception:
            pass
        return None

    def _classify_texture(self, sand: float, silt: float, clay: float) -> str:
        if sand >= 70:
            return "sand"
        elif clay >= 40:
            return "clay"
        elif silt >= 50:
            return "silt"
        elif sand >= 45 and clay <= 25:
            return "sandy_loam"
        elif clay >= 27:
            return "clay_loam"
        else:
            return "loam"

    def _estimate_permeability(self, sand: float, clay: float) -> Dict[str, Any]:
        if sand > 65:
            return {"ksat_cm_day": 240.0, "rating": "very_high", "suitability": "high_infiltration_high_contamination_risk"}
        elif clay > 38:
            return {"ksat_cm_day": 4.5, "rating": "very_low", "suitability": "unsuitable_for_soakaways_causes_pooling"}
        elif sand > 40:
            return {"ksat_cm_day": 75.0, "rating": "high", "suitability": "suitable_for_soakaways"}
        elif clay > 25:
            return {"ksat_cm_day": 18.0, "rating": "medium_low", "suitability": "marginal_requires_larger_area"}
        else:
            return {"ksat_cm_day": 45.0, "rating": "medium", "suitability": "suitable_for_soakaways"}

    def get_sample_fallback(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        if 20.0 <= lat <= 26.0 and 88.0 <= lon <= 93.0:
            # Dhaka alluvial silt loam
            sand, silt, clay = 20.0, 55.0, 25.0
        elif -5.0 <= lat <= 5.0 and 34.0 <= lon <= 42.0:
            if lat > 2.0:
                # Turkana arid sand
                sand, silt, clay = 78.0, 14.0, 8.0
            else:
                # Nairobi volcanic clay / clay loam
                sand, silt, clay = 22.0, 28.0, 50.0
        elif -27.0 <= lat <= -24.0 and 31.0 <= lon <= 35.0:
            # Maputo coastal sand
            sand, silt, clay = 88.0, 7.0, 5.0
        else:
            sand, silt, clay = 40.0, 40.0, 20.0

        texture = self._classify_texture(sand, silt, clay)
        ksat = self._estimate_permeability(sand, clay)

        return {
            "sand_pct": sand,
            "silt_pct": silt,
            "clay_pct": clay,
            "soil_texture_class": texture,
            "hydraulic_conductivity_ksat_cm_day": ksat["ksat_cm_day"],
            "permeability_rating": ksat["rating"],
            "soakaway_suitability": ksat["suitability"]
        }

soilgrids_client = SoilGridsClient()
