"""
Seed datasets for SanitaSafe demo regions:
1. Dhaka, Bangladesh (Flood-prone delta megacity)
2. Nairobi, Kenya (Informal settlements with steep terrain and acute drought vulnerability)
3. Maputo, Mozambique (Coastal shallow water table with porous sandy soil)
"""

DEMO_REGIONS = {
    "dhaka": {
        "id": "dhaka",
        "name": "Dhaka, Bangladesh",
        "country": "Bangladesh",
        "climate_type": "Tropical Monsoon / Riverine Delta",
        "description": "Low-lying Ganges-Brahmaputra-Meghna delta prone to heavy monsoon rainfall (GPM > 2100mm/yr), extreme riverine waterlogging, and dense informal settlements built on floodplains with shallow groundwater.",
        "center": [90.4125, 23.8103],
        "zoom": 12,
        "neighborhoods": [
            {
                "id": "dhaka_kamrangirchar",
                "name": "Kamrangirchar Island",
                "population": 420000,
                "area_km2": 3.68,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [90.355, 23.715],
                        [90.380, 23.710],
                        [90.385, 23.730],
                        [90.362, 23.735],
                        [90.355, 23.715]
                    ]]
                },
                "water_table_depth_m": 0.8,
                "water_table_is_estimate": True,
                "soil_type": "silt",
                "soil_texture_label": "Silt Loam / Alluvial Mud",
                "permeability_proxy": "medium_low",
                "distance_to_water_source_m": 12,
                "sanitation_coverage": {
                    "pit_latrine": 45,
                    "septic": 25,
                    "sewer": 5,
                    "open_defecation": 10,
                    "shared_public": 15
                },
                "annual_diarrhea_cholera_cases": 840,
                "hazards": {
                    "gpm_rainfall_annual_mm": 2250.0,
                    "gpm_intensity_95th_mm_hr": 38.5,
                    "gpm_extreme_event_days": 24,
                    "smap_soil_moisture": 0.44,
                    "smap_saturation_pct": 88.0,
                    "grace_gw_trend_cm_yr": -0.8,
                    "landsat_lst_celsius": 32.4,
                    "landsat_ndvi": 0.12,
                    "surface_water_inundation_freq_pct": 65.0,
                    "nasadem_elevation_m": 4.2,
                    "nasadem_slope_deg": 0.8,
                    "power_rh_pct": 79.5,
                    "power_heat_index_c": 36.8
                }
            },
            {
                "id": "dhaka_korail",
                "name": "Korail Slum / Gulshan Lake Margin",
                "population": 160000,
                "area_km2": 0.95,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [90.405, 23.775],
                        [90.420, 23.770],
                        [90.425, 23.785],
                        [90.410, 23.788],
                        [90.405, 23.775]
                    ]]
                },
                "water_table_depth_m": 0.6,
                "water_table_is_estimate": True,
                "soil_type": "clay_loam",
                "soil_texture_label": "Alluvial Clay & Mud Fill",
                "permeability_proxy": "low",
                "distance_to_water_source_m": 8,
                "sanitation_coverage": {
                    "pit_latrine": 52,
                    "septic": 18,
                    "sewer": 0,
                    "open_defecation": 8,
                    "shared_public": 22
                },
                "annual_diarrhea_cholera_cases": 620,
                "hazards": {
                    "gpm_rainfall_annual_mm": 2210.0,
                    "gpm_intensity_95th_mm_hr": 36.2,
                    "gpm_extreme_event_days": 22,
                    "smap_soil_moisture": 0.46,
                    "smap_saturation_pct": 92.0,
                    "grace_gw_trend_cm_yr": -0.9,
                    "landsat_lst_celsius": 33.1,
                    "landsat_ndvi": 0.09,
                    "surface_water_inundation_freq_pct": 72.0,
                    "nasadem_elevation_m": 3.5,
                    "nasadem_slope_deg": 0.5,
                    "power_rh_pct": 80.2,
                    "power_heat_index_c": 37.4
                }
            },
            {
                "id": "dhaka_hazaribagh",
                "name": "Hazaribagh Embankment Zone",
                "population": 210000,
                "area_km2": 2.40,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [90.358, 23.732],
                        [90.375, 23.730],
                        [90.378, 23.748],
                        [90.360, 23.750],
                        [90.358, 23.732]
                    ]]
                },
                "water_table_depth_m": 1.2,
                "water_table_is_estimate": True,
                "soil_type": "loam",
                "soil_texture_label": "Silty Clay Loam",
                "permeability_proxy": "medium",
                "distance_to_water_source_m": 25,
                "sanitation_coverage": {
                    "pit_latrine": 38,
                    "septic": 35,
                    "sewer": 12,
                    "open_defecation": 3,
                    "shared_public": 12
                },
                "annual_diarrhea_cholera_cases": 410,
                "hazards": {
                    "gpm_rainfall_annual_mm": 2180.0,
                    "gpm_intensity_95th_mm_hr": 35.0,
                    "gpm_extreme_event_days": 20,
                    "smap_soil_moisture": 0.38,
                    "smap_saturation_pct": 76.0,
                    "grace_gw_trend_cm_yr": -1.1,
                    "landsat_lst_celsius": 34.5,
                    "landsat_ndvi": 0.14,
                    "surface_water_inundation_freq_pct": 48.0,
                    "nasadem_elevation_m": 5.8,
                    "nasadem_slope_deg": 1.1,
                    "power_rh_pct": 78.0,
                    "power_heat_index_c": 38.0
                }
            },
            {
                "id": "dhaka_mirpur",
                "name": "Mirpur Sector 11 & Lowland Pockets",
                "population": 380000,
                "area_km2": 4.10,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [90.350, 23.810],
                        [90.380, 23.805],
                        [90.385, 23.830],
                        [90.355, 23.832],
                        [90.350, 23.810]
                    ]]
                },
                "water_table_depth_m": 2.2,
                "water_table_is_estimate": True,
                "soil_type": "clay_loam",
                "soil_texture_label": "Madhupur Clay Subsoil",
                "permeability_proxy": "low",
                "distance_to_water_source_m": 60,
                "sanitation_coverage": {
                    "pit_latrine": 25,
                    "septic": 48,
                    "sewer": 18,
                    "open_defecation": 1,
                    "shared_public": 8
                },
                "annual_diarrhea_cholera_cases": 280,
                "hazards": {
                    "gpm_rainfall_annual_mm": 2150.0,
                    "gpm_intensity_95th_mm_hr": 33.5,
                    "gpm_extreme_event_days": 18,
                    "smap_soil_moisture": 0.32,
                    "smap_saturation_pct": 64.0,
                    "grace_gw_trend_cm_yr": -1.4,
                    "landsat_lst_celsius": 33.8,
                    "landsat_ndvi": 0.18,
                    "surface_water_inundation_freq_pct": 28.0,
                    "nasadem_elevation_m": 9.2,
                    "nasadem_slope_deg": 2.4,
                    "power_rh_pct": 77.0,
                    "power_heat_index_c": 36.5
                }
            }
        ]
    },
    "nairobi": {
        "id": "nairobi",
        "name": "Nairobi & Turkana, Kenya",
        "country": "Kenya",
        "climate_type": "Semi-Arid Highland & Dryland Fringe",
        "description": "Informal valley settlements with steep drainage ravines (Kibera, Mukuru, Mathare) combined with dryland zones (Lodwar/Turkana). Experiences severe water shortages, dry spells, low soil moisture, and flash floods that flush pit waste into water points.",
        "center": [36.785, -1.315],
        "zoom": 13,
        "neighborhoods": [
            {
                "id": "nairobi_kibera_soweto",
                "name": "Kibera - Soweto East & Gatwekera",
                "population": 125000,
                "area_km2": 0.72,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [36.780, -1.318],
                        [36.798, -1.314],
                        [36.802, -1.325],
                        [36.784, -1.328],
                        [36.780, -1.318]
                    ]]
                },
                "water_table_depth_m": 3.8,
                "water_table_is_estimate": True,
                "soil_type": "clay",
                "soil_texture_label": "Black Cotton Clay / Deep Volcanic",
                "permeability_proxy": "very_low",
                "distance_to_water_source_m": 15,
                "sanitation_coverage": {
                    "pit_latrine": 48,
                    "septic": 5,
                    "sewer": 4,
                    "open_defecation": 15,
                    "shared_public": 28
                },
                "annual_diarrhea_cholera_cases": 780,
                "hazards": {
                    "gpm_rainfall_annual_mm": 860.0,
                    "gpm_intensity_95th_mm_hr": 28.0,
                    "gpm_extreme_event_days": 11,
                    "smap_soil_moisture": 0.14,
                    "smap_saturation_pct": 28.0,
                    "grace_gw_trend_cm_yr": -1.8,
                    "landsat_lst_celsius": 29.8,
                    "landsat_ndvi": 0.15,
                    "surface_water_inundation_freq_pct": 32.0,
                    "nasadem_elevation_m": 1675.0,
                    "nasadem_slope_deg": 8.5,
                    "power_rh_pct": 54.0,
                    "power_heat_index_c": 31.0
                }
            },
            {
                "id": "nairobi_mukuru",
                "name": "Mukuru kwa Njenga (Ngong River Lowlands)",
                "population": 190000,
                "area_km2": 1.45,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [36.870, -1.315],
                        [36.892, -1.310],
                        [36.896, -1.325],
                        [36.874, -1.328],
                        [36.870, -1.315]
                    ]]
                },
                "water_table_depth_m": 1.4,
                "water_table_is_estimate": True,
                "soil_type": "clay_loam",
                "soil_texture_label": "Alluvial Valley Clay",
                "permeability_proxy": "low",
                "distance_to_water_source_m": 10,
                "sanitation_coverage": {
                    "pit_latrine": 55,
                    "septic": 10,
                    "sewer": 2,
                    "open_defecation": 12,
                    "shared_public": 21
                },
                "annual_diarrhea_cholera_cases": 910,
                "hazards": {
                    "gpm_rainfall_annual_mm": 840.0,
                    "gpm_intensity_95th_mm_hr": 29.5,
                    "gpm_extreme_event_days": 13,
                    "smap_soil_moisture": 0.22,
                    "smap_saturation_pct": 44.0,
                    "grace_gw_trend_cm_yr": -1.6,
                    "landsat_lst_celsius": 31.2,
                    "landsat_ndvi": 0.11,
                    "surface_water_inundation_freq_pct": 58.0,
                    "nasadem_elevation_m": 1620.0,
                    "nasadem_slope_deg": 3.8,
                    "power_rh_pct": 52.0,
                    "power_heat_index_c": 32.5
                }
            },
            {
                "id": "nairobi_mathare",
                "name": "Mathare Valley (Upper & Lower)",
                "population": 140000,
                "area_km2": 0.88,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [36.852, -1.258],
                        [36.870, -1.252],
                        [36.874, -1.268],
                        [36.856, -1.272],
                        [36.852, -1.258]
                    ]]
                },
                "water_table_depth_m": 2.1,
                "water_table_is_estimate": True,
                "soil_type": "loam",
                "soil_texture_label": "Volcanic Loam with Outcrops",
                "permeability_proxy": "medium",
                "distance_to_water_source_m": 18,
                "sanitation_coverage": {
                    "pit_latrine": 50,
                    "septic": 8,
                    "sewer": 8,
                    "open_defecation": 9,
                    "shared_public": 25
                },
                "annual_diarrhea_cholera_cases": 580,
                "hazards": {
                    "gpm_rainfall_annual_mm": 880.0,
                    "gpm_intensity_95th_mm_hr": 26.5,
                    "gpm_extreme_event_days": 10,
                    "smap_soil_moisture": 0.18,
                    "smap_saturation_pct": 36.0,
                    "grace_gw_trend_cm_yr": -1.7,
                    "landsat_lst_celsius": 30.5,
                    "landsat_ndvi": 0.16,
                    "surface_water_inundation_freq_pct": 38.0,
                    "nasadem_elevation_m": 1640.0,
                    "nasadem_slope_deg": 7.2,
                    "power_rh_pct": 53.0,
                    "power_heat_index_c": 31.8
                }
            },
            {
                "id": "turkana_lodwar",
                "name": "Lodwar Central (Turkana Dryland Peri-Urban)",
                "population": 65000,
                "area_km2": 5.20,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [35.580, 3.100],
                        [35.620, 3.090],
                        [35.625, 3.130],
                        [35.585, 3.140],
                        [35.580, 3.100]
                    ]]
                },
                "water_table_depth_m": 6.5,
                "water_table_is_estimate": True,
                "soil_type": "sand",
                "soil_texture_label": "Arid Sand & Gravel",
                "permeability_proxy": "high",
                "distance_to_water_source_m": 120,
                "sanitation_coverage": {
                    "pit_latrine": 32,
                    "septic": 6,
                    "sewer": 0,
                    "open_defecation": 48,
                    "shared_public": 14
                },
                "annual_diarrhea_cholera_cases": 320,
                "hazards": {
                    "gpm_rainfall_annual_mm": 210.0,
                    "gpm_intensity_95th_mm_hr": 19.0,
                    "gpm_extreme_event_days": 4,
                    "smap_soil_moisture": 0.06,
                    "smap_saturation_pct": 12.0,
                    "grace_gw_trend_cm_yr": -2.4,
                    "landsat_lst_celsius": 41.2,
                    "landsat_ndvi": 0.05,
                    "surface_water_inundation_freq_pct": 8.0,
                    "nasadem_elevation_m": 477.0,
                    "nasadem_slope_deg": 1.2,
                    "power_rh_pct": 28.0,
                    "power_heat_index_c": 44.5
                }
            }
        ]
    },
    "maputo": {
        "id": "maputo",
        "name": "Maputo, Mozambique",
        "country": "Mozambique",
        "climate_type": "Tropical Coastal & Cyclone Exposed",
        "description": "Coastal zone characterized by extremely shallow water table (<1.2m), deep porous quartz sands with rapid pathogen transmission into shallow domestic boreholes, and high cyclone/storm-surge flooding susceptibility.",
        "center": [32.585, -25.955],
        "zoom": 12,
        "neighborhoods": [
            {
                "id": "maputo_chamanculo",
                "name": "Chamanculo A & B",
                "population": 110000,
                "area_km2": 1.85,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [32.545, -25.955],
                        [32.568, -25.945],
                        [32.572, -25.962],
                        [32.548, -25.968],
                        [32.545, -25.955]
                    ]]
                },
                "water_table_depth_m": 0.9,
                "water_table_is_estimate": True,
                "soil_type": "sand",
                "soil_texture_label": "Coastal Quartz Dune Sand",
                "permeability_proxy": "very_high",
                "distance_to_water_source_m": 9,
                "sanitation_coverage": {
                    "pit_latrine": 68,
                    "septic": 18,
                    "sewer": 2,
                    "open_defecation": 4,
                    "shared_public": 8
                },
                "annual_diarrhea_cholera_cases": 710,
                "hazards": {
                    "gpm_rainfall_annual_mm": 980.0,
                    "gpm_intensity_95th_mm_hr": 42.0,
                    "gpm_extreme_event_days": 14,
                    "smap_soil_moisture": 0.36,
                    "smap_saturation_pct": 72.0,
                    "grace_gw_trend_cm_yr": -0.4,
                    "landsat_lst_celsius": 30.8,
                    "landsat_ndvi": 0.22,
                    "surface_water_inundation_freq_pct": 52.0,
                    "nasadem_elevation_m": 12.0,
                    "nasadem_slope_deg": 1.4,
                    "power_rh_pct": 76.0,
                    "power_heat_index_c": 35.2
                }
            },
            {
                "id": "maputo_polana_canico",
                "name": "Polana Caniço A & B",
                "population": 95000,
                "area_km2": 2.10,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [32.580, -25.935],
                        [32.605, -25.928],
                        [32.610, -25.945],
                        [32.585, -25.950],
                        [32.580, -25.935]
                    ]]
                },
                "water_table_depth_m": 1.1,
                "water_table_is_estimate": True,
                "soil_type": "sandy_loam",
                "soil_texture_label": "Sandy Coastal Loam",
                "permeability_proxy": "high",
                "distance_to_water_source_m": 14,
                "sanitation_coverage": {
                    "pit_latrine": 58,
                    "septic": 28,
                    "sewer": 4,
                    "open_defecation": 2,
                    "shared_public": 8
                },
                "annual_diarrhea_cholera_cases": 490,
                "hazards": {
                    "gpm_rainfall_annual_mm": 970.0,
                    "gpm_intensity_95th_mm_hr": 39.0,
                    "gpm_extreme_event_days": 13,
                    "smap_soil_moisture": 0.32,
                    "smap_saturation_pct": 64.0,
                    "grace_gw_trend_cm_yr": -0.5,
                    "landsat_lst_celsius": 29.5,
                    "landsat_ndvi": 0.28,
                    "surface_water_inundation_freq_pct": 44.0,
                    "nasadem_elevation_m": 24.0,
                    "nasadem_slope_deg": 3.2,
                    "power_rh_pct": 75.0,
                    "power_heat_index_c": 34.0
                }
            },
            {
                "id": "maputo_maxaquene",
                "name": "Maxaquene & Mafalala",
                "population": 120000,
                "area_km2": 1.60,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [32.560, -25.940],
                        [32.580, -25.935],
                        [32.584, -25.952],
                        [32.564, -25.956],
                        [32.560, -25.940]
                    ]]
                },
                "water_table_depth_m": 0.8,
                "water_table_is_estimate": True,
                "soil_type": "sand",
                "soil_texture_label": "Fine White Dune Sand",
                "permeability_proxy": "very_high",
                "distance_to_water_source_m": 11,
                "sanitation_coverage": {
                    "pit_latrine": 62,
                    "septic": 22,
                    "sewer": 3,
                    "open_defecation": 3,
                    "shared_public": 10
                },
                "annual_diarrhea_cholera_cases": 560,
                "hazards": {
                    "gpm_rainfall_annual_mm": 975.0,
                    "gpm_intensity_95th_mm_hr": 40.5,
                    "gpm_extreme_event_days": 14,
                    "smap_soil_moisture": 0.38,
                    "smap_saturation_pct": 76.0,
                    "grace_gw_trend_cm_yr": -0.4,
                    "landsat_lst_celsius": 30.2,
                    "landsat_ndvi": 0.20,
                    "surface_water_inundation_freq_pct": 61.0,
                    "nasadem_elevation_m": 10.5,
                    "nasadem_slope_deg": 1.1,
                    "power_rh_pct": 77.0,
                    "power_heat_index_c": 35.0
                }
            },
            {
                "id": "maputo_costa_do_sol",
                "name": "Costa do Sol Beachfront & Estuary",
                "population": 48000,
                "area_km2": 3.80,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [32.610, -25.910],
                        [32.640, -25.890],
                        [32.650, -25.920],
                        [32.620, -25.935],
                        [32.610, -25.910]
                    ]]
                },
                "water_table_depth_m": 0.5,
                "water_table_is_estimate": True,
                "soil_type": "sand",
                "soil_texture_label": "Tidal Sand & Mangrove Silt",
                "permeability_proxy": "high",
                "distance_to_water_source_m": 15,
                "sanitation_coverage": {
                    "pit_latrine": 24,
                    "septic": 52,
                    "sewer": 12,
                    "open_defecation": 2,
                    "shared_public": 10
                },
                "annual_diarrhea_cholera_cases": 180,
                "hazards": {
                    "gpm_rainfall_annual_mm": 990.0,
                    "gpm_intensity_95th_mm_hr": 44.0,
                    "gpm_extreme_event_days": 16,
                    "smap_soil_moisture": 0.42,
                    "smap_saturation_pct": 84.0,
                    "grace_gw_trend_cm_yr": -0.3,
                    "landsat_lst_celsius": 28.5,
                    "landsat_ndvi": 0.35,
                    "surface_water_inundation_freq_pct": 78.0,
                    "nasadem_elevation_m": 2.1,
                    "nasadem_slope_deg": 0.4,
                    "power_rh_pct": 81.0,
                    "power_heat_index_c": 33.8
                }
            }
        ]
    }
}
