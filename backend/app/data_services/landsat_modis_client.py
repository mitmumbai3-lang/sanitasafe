from typing import Dict, Any, Optional
from app.data_services.base import BaseDataClient
from app.config import settings

class LandsatMODISClient(BaseDataClient):
    """
    NASA Landsat 8/9 OLI/TIRS and MODIS/VIIRS Land Surface & Water Dynamics
    Spatial Resolution: 30 m (Landsat OLI/TIRS) to 250 m (MODIS Terra/Aqua / VIIRS)
    Provides Land Surface Temperature (LST °C), NDVI vegetation proxy, NDWI surface water extent, and historical flood inundation frequency.
    """
    def __init__(self):
        super().__init__(
            dataset_name="NASA Landsat 8/9 & MODIS/VIIRS Combined Land Surface Suite",
            spatial_resolution="30 m (Landsat) to 250 m (MODIS/VIIRS)",
            temporal_resolution="16-day Landsat repeat cycle; Daily MODIS/VIIRS composite",
            uncertainty_note="LST accuracy ±1.5°C; cloud masking can interpolate overcast rainy season weeks."
        )

    def fetch_live(self, lat: float, lon: float, **kwargs) -> Optional[Dict[str, Any]]:
        if not settings.EARTHDATA_USERNAME or not settings.EARTHDATA_PASSWORD:
            return None
        return None

    def get_sample_fallback(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        if 20.0 <= lat <= 26.0 and 88.0 <= lon <= 93.0:
            # Dhaka: dense built urban heat island, low NDVI, high inundation frequency
            lst = 33.5
            ndvi = 0.12
            ndwi_water_pct = 22.0
            historical_flood_inundation_pct = 62.0
            monthly_flood_freq = [5, 4, 8, 18, 35, 68, 76, 70, 52, 28, 10, 6]
            monthly_lst = [22, 26, 31, 34, 33, 31, 31, 31, 32, 31, 28, 23]
        elif -5.0 <= lat <= 5.0 and 34.0 <= lon <= 42.0:
            if lat > 2.0:
                # Turkana arid: extreme LST, minimal NDVI, rare flash inundation
                lst = 41.5
                ndvi = 0.05
                ndwi_water_pct = 1.5
                historical_flood_inundation_pct = 7.0
                monthly_flood_freq = [2, 1, 3, 12, 8, 2, 1, 2, 1, 3, 9, 3]
                monthly_lst = [39, 41, 42, 40, 39, 38, 37, 38, 39, 40, 39, 38]
            else:
                # Nairobi informal settlements: high urban density, valley stream inundation
                lst = 30.5
                ndvi = 0.14
                ndwi_water_pct = 8.0
                historical_flood_inundation_pct = 42.0
                monthly_flood_freq = [6, 4, 15, 45, 32, 8, 4, 5, 8, 14, 38, 22]
                monthly_lst = [29, 31, 31, 28, 27, 25, 24, 25, 27, 29, 28, 28]
        elif -27.0 <= lat <= -24.0 and 31.0 <= lon <= 35.0:
            # Maputo: coastal humidity, moderate LST, high storm surge / flood frequency
            lst = 30.2
            ndvi = 0.24
            ndwi_water_pct = 18.0
            historical_flood_inundation_pct = 58.0
            monthly_flood_freq = [38, 45, 34, 18, 8, 4, 3, 4, 6, 12, 26, 35]
            monthly_lst = [32, 32, 30, 28, 26, 24, 23, 24, 26, 28, 30, 31]
        else:
            lst = 31.0
            ndvi = 0.20
            ndwi_water_pct = 10.0
            historical_flood_inundation_pct = 30.0
            monthly_flood_freq = [10, 10, 12, 15, 25, 35, 40, 38, 25, 18, 12, 10]
            monthly_lst = [27, 28, 29, 30, 31, 30, 29, 29, 29, 29, 28, 27]

        return {
            "land_surface_temperature_celsius": lst,
            "ndvi_vegetation_index": ndvi,
            "surface_water_extent_pct": ndwi_water_pct,
            "historical_flood_inundation_frequency_pct": historical_flood_inundation_pct,
            "monthly_flood_frequency_pct": monthly_flood_freq,
            "monthly_lst_trend_celsius": monthly_lst,
            "months_labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        }

landsat_modis_client = LandsatMODISClient()
