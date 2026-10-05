from typing import Dict, Any, Optional
from app.data_services.base import BaseDataClient
from app.config import settings

class GRACEClient(BaseDataClient):
    """
    NASA GRACE / GRACE-FO (Gravity Recovery and Climate Experiment Follow-On)
    Spatial Resolution: ~300 km (Coarse Gravimetric Mascon)
    IMPORTANT: GRACE-FO measures total terrestrial water storage (TWS) anomalies over large regional basins.
    It does NOT provide neighborhood-scale water table depth and should strictly be interpreted as a regional macro-outlook.
    """
    def __init__(self):
        super().__init__(
            dataset_name="NASA GRACE-FO JPL RL06 Mascon v02",
            spatial_resolution="~300 km (coarse gravimetric mascon footprint)",
            temporal_resolution="Monthly gravity field solutions",
            uncertainty_note="Coarse resolution (~300 km). Mascon filtering separates regional TWS into groundwater, surface water, and soil moisture components with ±1.5-2.0 cm equivalent water height uncertainty."
        )

    def fetch_live(self, lat: float, lon: float, **kwargs) -> Optional[Dict[str, Any]]:
        if not settings.EARTHDATA_USERNAME or not settings.EARTHDATA_PASSWORD:
            return None
        return None

    def get_sample_fallback(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        # Regional basin trends (cm of water per year depletion or recharge)
        if 20.0 <= lat <= 26.0 and 88.0 <= lon <= 93.0:
            # Bengal Basin (Dhaka region): Severe deep aquifer over-abstraction (-1.1 cm/yr TWS equivalent)
            gw_trend = -1.1
            regional_basin = "Ganges-Brahmaputra Basin"
            status = "Declining due to municipal and irrigation deep pumping"
            multi_year_trend = [-0.2, -0.4, -0.6, -0.8, -1.0, -1.2, -1.3, -1.5, -1.7, -1.9]
        elif -5.0 <= lat <= 5.0 and 34.0 <= lon <= 42.0:
            # East African Rift / Athi-Turkana Basins
            gw_trend = -1.7
            regional_basin = "Athi-Rift Valley Basin"
            status = "Regional multi-year drought depletion"
            multi_year_trend = [-0.5, -0.8, -1.1, -1.3, -1.6, -1.9, -2.2, -2.5, -2.7, -3.0]
        elif -27.0 <= lat <= -24.0 and 31.0 <= lon <= 35.0:
            # Limpopo / Southern Mozambique Coastal Basin
            gw_trend = -0.4
            regional_basin = "Limpopo-Maputo Coastal Basin"
            status = "Slight multi-year drawdown, high cyclone recharge variability"
            multi_year_trend = [-0.1, -0.2, +0.3, -0.1, -0.3, -0.5, +0.2, -0.2, -0.4, -0.5]
        else:
            gw_trend = -0.5
            regional_basin = "Regional Hydrological Basin"
            status = "Moderate baseline change"
            multi_year_trend = [-0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0, -1.1]

        return {
            "regional_basin_name": regional_basin,
            "groundwater_trend_cm_year": gw_trend,
            "regional_storage_status": status,
            "resolution_caveat": "Coarse ~300 km footprint. Represents regional basin groundwater storage trends, not individual neighborhood boreholes.",
            "five_year_anomaly_series": multi_year_trend,
            "years_labels": ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]
        }

grace_client = GRACEClient()
