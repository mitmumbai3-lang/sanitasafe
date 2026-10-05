# SanitaSafe 🌍🚽🛰️

**SanitaSafe** is a responsive, climate-resilient sanitation decision support application designed for community health workers and NGO field teams (phone-optimized, offline-resilient, plain-language) as well as municipal and district planners (desktop GIS console, multi-criteria weight tuning, scenario models, and exportable investment reports).

SanitaSafe integrates NASA Earth Observation (EO) satellite products to detect environmental risk hotspots and recommend viable sanitation infrastructure based on deterministic physical and hydrogeological exclusion rules.

---

## 🚀 Live Services & Ports

| Service | Port & URL | Description |
| :--- | :--- | :--- |
| **Frontend Web App & PWA** | [http://localhost:3000](http://localhost:3000) | Next.js 16 + TypeScript + Tailwind CSS + MapLibre GL |
| **Analytical Engine API** | [http://localhost:8000](http://localhost:8000) | Python FastAPI Backend |
| **Interactive API Documentation** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger OpenAPI UI |
| **Methodology & Limitations** | [http://localhost:3000/methodology](http://localhost:3000/methodology) | Scientific formulas, normalization & engineering disclaimer |
| **About the Data** | [http://localhost:3000/about](http://localhost:3000/about) | NASA dataset credits, spatial resolutions & extension guide |

---

## 🛰️ NASA Earth Observation Datasets Integrated

All dataset values are sourced from verified Earth observation products and attributed with explicit spatial footprint notes in the UI:

| Dataset | Sensor / Platform | Spatial Resolution | Extracted Hazard Parameter |
| :--- | :--- | :--- | :--- |
| **GPM IMERG v07B** | GPM Constellation | **0.1° (~10 km)** | Cumulative rainfall, 95th percentile storm intensity (mm/hr), extreme storm days |
| **NASA SMAP L3** | Radiometer | **9 km – 36 km** | Top 5cm volumetric soil moisture ($m^3/m^3$), soil saturation ratio (%) |
| **NASA GRACE-FO RL06** | Dual Satellite Gravimetry | **~300 km (Coarse)** | Regional river basin groundwater storage anomaly & depletion trend (cm/yr) |
| **Landsat 8/9 & MODIS/VIIRS** | OLI/TIRS & Terra/Aqua | **30 m – 250 m** | Land surface temperature (LST °C), NDVI greenness, surface water extent & flood frequency |
| **NASADEM / SRTM** | Radar Interferometry | **1 Arc-Sec (~30 m)** | Elevation (m), topographic slope (°), low-lying depression risk |
| **NASA POWER** | MERRA-2 Assimilation | **0.5° (~50 km)** | 30-year climatological temperature, relative humidity, heat index |
| **ISRIC SoilGrids** | WoSIS Machine Learning | **250 m** | Sand, silt, clay fractions, hydraulic conductivity ($K_{sat}$) permeability proxy |
| **WorldPop & OSM** | Gridded Census & Overpass | **100 m / Vector** | High-resolution population density, proximity to drinking water points and wells |
| **NASA GIBS WMTS** | Direct EPSG:3857 Tiles | **250m – 10km** | Real-time map overlays: MODIS True Color, GPM Precipitation, SMAP Soil Moisture, Surface Inundation |

> ⚠️ **Coarse Resolution Disclosure**: GRACE-FO operates at a regional ~300 km footprint representing river basin storage trends, not neighborhood boreholes. SMAP operates at 9–36 km.

---

## 🏙️ Pre-Calibrated Demo Regions

1. **Dhaka, Bangladesh** *(Delta & Flood Prone)*:
   - Wards: Kamrangirchar Island, Korail Slum, Hazaribagh Embankment, Mirpur Sector 11.
   - Low elevation (3–6m), monsoon rainfall (GPM > 2200mm/yr), high soil saturation (SMAP > 85%), high waterlogging frequency.
2. **Nairobi & Turkana, Kenya** *(Informal Settlements & Semi-Arid Drought)*:
   - Settlements: Kibera (Soweto East), Mukuru kwa Njenga, Mathare Valley, Lodwar Central (Turkana).
   - Acute water scarcity, soil moisture deficits (SMAP < 0.14), steep ravine slopes, flash floods over crusted soils.
3. **Maputo, Mozambique** *(Coastal Shallow Water Table & Sandy Soil)*:
   - Bairros: Chamanculo, Polana Caniço, Maxaquene & Mafalala, Costa do Sol.
   - Shallow water table (< 1.2m), coastal quartz sand (rapid pathogen leaching into shallow domestic wells), cyclone storm surges.

---

## ⚙️ Core Analytical Capabilities

### 1. Risk Scoring Engine (0–100)
Pure, unit-tested engine computing four normalized sub-indices:
- **Flood Exposure**: Rain extremes + elevation + slope + historical inundation + soil saturation.
- **Drought & Scarcity**: Soil moisture deficit + rainfall deficit + GRACE-FO depletion + thermal heat stress.
- **Groundwater Contamination Risk**: Water table depth + soil permeability + latrine density + drinking well setback.
- **Population Vulnerability**: Demographic density + sanitation coverage gap + waterborne disease incidence.
- **Composite Score**: Transparent weighted score with plain-language driver summaries.

### 2. Solution Recommender & Exclusion Rules
Curated database of 9 verified technologies:
- Raised / Elevated Latrines
- Sealed / Lined Pits (VIP)
- Urine-Diverting Dry Toilets (UDDT)
- Composting Toilets / Arborloo
- Septic Tanks with Soak Pits
- Twin-Pit Pour-Flush Latrines
- Container-Based Sanitation (CBS)
- Decentralized Wastewater Treatment (DEWATS) & Constructed Wetlands
- Off-Site Sewered Connections

**Hard Exclusion Rules**:
- **Shallow Water Table**: Leaching pits/septic tanks excluded where water table $< 1.5$m – $2.5$m.
- **Drinking Well Buffer**: Ground infiltration excluded if distance to well $< 15$m (or $< 30$m in coarse sands).
- **Water Scarcity**: Pour-flush and conventional sewers excluded if drought score $> 60/100$.
- **Flood Inundation**: Low-flood-tolerance pits excluded in frequent flood zones.
- **Impermeable Clay**: Soak pits excluded in heavy clay soils ($K_{sat}$ low).

Remaining options are ranked using multi-criteria alignment and user priority weights (Budget, Maintenance, Circular Reuse, Climate Resilience).

### 3. Climate Scenario Simulation & Swipe Map
- **Baseline**: Current NASA 10-year climatology.
- **Heavier Rain (+20%)**: +20% rainfall intensity, +25% flood extent, saturated topsoil, shallower water table.
- **Prolonged Drought (-25%)**: -25% rainfall, severe soil moisture drop, water table drawdown.
- **Compound Extremes**: Severe drought alternating with sudden convective cloudbursts.
- **Swipe Map**: Interactive side-by-side split screen with draggable divider slider comparing Baseline vs Scenario.
- **Most Changed Neighborhoods**: Delta tracking table flagging communities that shift into critical risk.

### 4. Reporting & Exports
- **PDF Investment Brief**: Formatted 2-page brief for district planners and municipal leadership with prioritized investments and geotechnical disclaimers.
- **CSV Export**: Tabular dataset of all hazard scores and recommendations.
- **GeoJSON Export**: Spatial GIS polygons with embedded risk attributes.

---

## 🛠️ Local Development & Setup

### Prerequisites
- Node.js >= 20 (Tested on Node v24.21.0)
- Python >= 3.10 (Tested on Python 3.14.6)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run unit tests (17 tests covering scoring, exclusions, and scenarios)
pytest -o pythonpath=. app/tests

# Start FastAPI server on port 8000
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup
```bash
cd frontend

# Install npm dependencies
npm install

# Run TypeScript build verification
npm run build

# Start Next.js development server on port 3000
npm run dev
```

### 3. NASA Earthdata Credentials (Optional)
SanitaSafe functions completely offline out of the box using calibrated high-fidelity seed datasets. To connect to live NASA Earthdata CMR and OPeNDAP services, create `backend/.env`:
```env
EARTHDATA_USERNAME=your_nasa_username
EARTHDATA_PASSWORD=your_nasa_password
ENABLE_LIVE_FETCH=true
```
Register for a free Earthdata account at [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov).

---

## 🌐 Multilingual Support (i18n)
SanitaSafe includes complete localized UI dictionaries for:
- 🇬🇧 English (`en`)
- 🇪🇸 Spanish (`es`)
- 🇫🇷 French (`fr`)
- 🇮🇳 Hindi (`hi`)
- 🇰🇪 Swahili (`sw`)

---

## 🧩 Extending SanitaSafe

- **Add a Sanitation Option**: Add an entry to `backend/app/seeds/sanitation_options.json` and `frontend/src/lib/clientSeeds.ts`.
- **Add a New City/District**: Add a region block to `backend/app/seeds/demo_regions.py` and `frontend/src/lib/clientSeeds.ts`.
- **Add an Earth Observation Layer**: Implement a subclass of `BaseDataClient` in `backend/app/data_services/`.

---

## 📜 Ethical & Accessibility Standards
- **WCAG AA Compliant**: 4.5:1 text contrast ratio, keyboard navigable, accessible dialogs.
- **Colorblind-Safe Palettes**: ColorBrewer / Viridis ramps paired with distinct geometric symbols (■ Critical, ◆ High, ▲ Moderate, ● Low).
- **Privacy by Design**: Zero accounts required, no private household coordinates stored or transmitted.
- **Disclaimer**: Tool supports planning and preliminary screening; it does not replace site assessments by professional civil engineers.
