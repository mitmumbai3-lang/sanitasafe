from typing import Dict, Any, Optional
from app.data_services.base import BaseDataClient
import requests

class OSMWorldPopClient(BaseDataClient):
    """
    WorldPop (100m High Resolution Population Density) & OpenStreetMap (OSM Overpass API)
    Provides neighborhood population densities, proximity to drinking water points (boreholes, shallow wells, taps),
    and distance to surface rivers/canals.
    """
    def __init__(self):
        super().__init__(
            dataset_name="WorldPop 100m & OpenStreetMap Water Infrastructure",
            spatial_resolution="100 m (WorldPop) / Vector POI (OSM)",
            temporal_resolution="Annual population projection / Continual OSM updates",
            uncertainty_note="Informal settlements often have dynamic transient populations undercounted by static censuses."
        )

    def fetch_live(self, lat: float, lon: float, **kwargs) -> Optional[Dict[str, Any]]:
        # Optional live Overpass API query for water points near coordinate
        overpass_query = f"""
        [out:json][timeout:4];
        (
          node["man_made"="water_well"](around:500, {lat}, {lon});
          node["amenity"="drinking_water"](around:500, {lat}, {lon});
          way["waterway"](around:500, {lat}, {lon});
        );
        out count;
        """
        try:
            resp = requests.post("https://overpass-api.de/api/interpreter", data=overpass_query, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                count = int(data.get("elements", [{}])[0].get("tags", {}).get("total", 0))
                dist_proxy = max(10, 200 - min(180, count * 20))
                return {
                    "estimated_distance_to_water_source_m": dist_proxy,
                    "water_infrastructure_count_500m": count,
                    "data_source": "live_openstreetmap"
                }
        except Exception:
            pass
        return None

    def get_sample_fallback(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        if 20.0 <= lat <= 26.0 and 88.0 <= lon <= 93.0:
            # Dhaka: dense canals, hand-pumps adjacent to latrines
            dist = 12
            density_km2 = 48000
        elif -5.0 <= lat <= 5.0 and 34.0 <= lon <= 42.0:
            if lat > 2.0:
                dist = 140
                density_km2 = 3200
            else:
                dist = 15
                density_km2 = 55000
        elif -27.0 <= lat <= -24.0 and 31.0 <= lon <= 35.0:
            dist = 10
            density_km2 = 28000
        else:
            dist = 30
            density_km2 = 12000

        return {
            "estimated_distance_to_water_source_m": dist,
            "population_density_per_km2": density_km2,
            "osm_water_features": ["shallow_boreholes", "drainage_canal", "standpipe"]
        }

osm_worldpop_client = OSMWorldPopClient()
