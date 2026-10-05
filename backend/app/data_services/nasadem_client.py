from typing import Dict, Any, Optional
from app.data_services.base import BaseDataClient
from app.config import settings

class NASADEMClient(BaseDataClient):
    """
    NASA NASADEM / SRTM (Shuttle Radar Topography Mission) v001
    Spatial Resolution: 1 arc-second (~30 m)
    Provides elevation, topographic slope, flow accumulation proxies, and low-lying depression indices.
    """
    def __init__(self):
        super().__init__(
            dataset_name="NASA NASADEM Global 1 Arc-Second (~30 m)",
            spatial_resolution="1 arc-second (~30 m grid cell)",
            temporal_resolution="Static Digital Elevation Model (reprocessed with ICESat/GLAS calibration)",
            uncertainty_note="Vertical accuracy ±3-5 meters in flat urban delta areas; radar elevation can reflect dense building rooftops or tree crowns."
        )

    def fetch_live(self, lat: float, lon: float, **kwargs) -> Optional[Dict[str, Any]]:
        if not settings.EARTHDATA_USERNAME or not settings.EARTHDATA_PASSWORD:
            return None
        return None

    def get_sample_fallback(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        if 20.0 <= lat <= 26.0 and 88.0 <= lon <= 93.0:
            # Dhaka: flat, low delta floodplain
            elevation = 5.2
            slope_deg = 0.8
            flow_acc_index = 8.8  # high flow accumulation (valley/waterway)
            depression_risk = "critical"  # waterlogging depression
            twi_index = 11.4  # Topographic wetness index
        elif -5.0 <= lat <= 5.0 and 34.0 <= lon <= 42.0:
            if lat > 2.0:
                # Turkana: gently sloping desert plain
                elevation = 480.0
                slope_deg = 1.4
                flow_acc_index = 3.2
                depression_risk = "low"
                twi_index = 6.2
            else:
                # Nairobi informal settlements (Kibera/Mukuru/Mathare): steep ravines
                elevation = 1640.0
                slope_deg = 7.5
                flow_acc_index = 6.5
                depression_risk = "moderate_valley_bottom"
                twi_index = 8.5
        elif -27.0 <= lat <= -24.0 and 31.0 <= lon <= 35.0:
            # Maputo: low coastal plain and dunes
            elevation = 11.5
            slope_deg = 1.2
            flow_acc_index = 7.1
            depression_risk = "high_coastal_depression"
            twi_index = 9.8
        else:
            elevation = 50.0
            slope_deg = 3.0
            flow_acc_index = 5.0
            depression_risk = "moderate"
            twi_index = 7.5

        return {
            "elevation_meters": elevation,
            "slope_degrees": slope_deg,
            "slope_pct": round(slope_deg * 1.75, 1),
            "flow_accumulation_proxy": flow_acc_index,
            "topographic_wetness_index_twi": twi_index,
            "low_lying_depression_status": depression_risk,
            "elevation_profile_bins": [
                {"range": "0-5m", "pct_area": 45 if elevation < 10 else 5},
                {"range": "5-15m", "pct_area": 40 if elevation < 20 else 15},
                {"range": "15-30m", "pct_area": 15 if elevation < 50 else 30},
                {"range": ">30m", "pct_area": 0 if elevation < 50 else 50}
            ]
        }

nasadem_client = NASADEMClient()
