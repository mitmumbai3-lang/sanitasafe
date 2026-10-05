from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.seeds.demo_regions import DEMO_REGIONS
from app.data_services import (
    gpm_client,
    smap_client,
    grace_client,
    landsat_modis_client,
    nasadem_client,
    power_client,
    soilgrids_client,
    osm_worldpop_client
)

router = APIRouter(prefix="/hazards", tags=["NASA Hazards"])

@router.get("/gibs-layers")
def get_gibs_layers() -> List[Dict[str, Any]]:
    """
    Returns NASA GIBS (Global Imagery Browse Services) tile configurations for MapLibre GL.
    GIBS provides standard WMTS / EPSG:3857 and EPSG:4326 raster tiles directly from NASA.
    """
    return [
        {
            "id": "gibs_modis_truecolor",
            "name": "MODIS Terra Corrected Reflectance (True Color)",
            "source": "NASA GIBS / Terra MODIS",
            "url": "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/default/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg",
            "resolution": "250 m",
            "opacity": 0.7,
            "category": "optical_imagery",
            "description": "Daily global true-color satellite surface reflectance."
        },
        {
            "id": "gibs_gpm_precipitation",
            "name": "GPM IMERG Precipitation Rate (3-Hour)",
            "source": "NASA GIBS / GPM IMERG",
            "url": "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/IMERG_Precipitation_Rate/default/default/GoogleMapsCompatible_Level6/{z}/{y}/{x}.png",
            "resolution": "0.1° (~10 km)",
            "opacity": 0.65,
            "category": "rainfall",
            "description": "Global precipitation rate from calibrated constellation of satellites."
        },
        {
            "id": "gibs_smap_soil_moisture",
            "name": "SMAP L3 Surface Soil Moisture",
            "source": "NASA GIBS / SMAP",
            "url": "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/SMAP_L3_Passive_Enhanced_Day_Surface_Soil_Moisture/default/default/GoogleMapsCompatible_Level6/{z}/{y}/{x}.png",
            "resolution": "9 km",
            "opacity": 0.65,
            "category": "soil_moisture",
            "description": "Volumetric surface soil moisture indicating runoff and waterlogging vulnerability."
        },
        {
            "id": "gibs_modis_surface_water",
            "name": "MODIS Surface Water Extent (Inundation)",
            "source": "NASA GIBS / MODIS",
            "url": "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_Surface_Water_Daily/default/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.png",
            "resolution": "250 m",
            "opacity": 0.6,
            "category": "flood_water",
            "description": "Daily surface water detection showing standing water and flooded river floodplains."
        }
    ]

@router.get("/point")
def get_point_hazards(lat: float, lon: float) -> Dict[str, Any]:
    """
    Fetch all NASA Earth observation hazard values for any arbitrary lat/lon coordinates.
    """
    return {
        "coordinates": {"lat": lat, "lon": lon},
        "gpm": gpm_client.get_data(lat, lon),
        "smap": smap_client.get_data(lat, lon),
        "grace": grace_client.get_data(lat, lon),
        "landsat_modis": landsat_modis_client.get_data(lat, lon),
        "nasadem": nasadem_client.get_data(lat, lon),
        "power": power_client.get_data(lat, lon),
        "soilgrids": soilgrids_client.get_data(lat, lon),
        "osm_worldpop": osm_worldpop_client.get_data(lat, lon)
    }
