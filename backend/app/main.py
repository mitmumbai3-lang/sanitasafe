from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.regions import router as regions_router
from app.api.hazards import router as hazards_router
from app.api.risk import router as risk_router

app = FastAPI(
    title="SanitaSafe Analytical Engine API",
    description="Climate-resilient sanitation decision support powered by NASA Earth observations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(regions_router, prefix=settings.API_PREFIX)
app.include_router(hazards_router, prefix=settings.API_PREFIX)
app.include_router(risk_router, prefix=settings.API_PREFIX)

@app.get("/")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SanitaSafe Analytical Engine",
        "nasa_datasets_integrated": [
            "GPM IMERG Final Run v07B",
            "SMAP L3/L4 Radiometer Soil Moisture",
            "GRACE-FO JPL RL06 Mascon",
            "Landsat 8/9 & MODIS/VIIRS LST & Surface Water",
            "NASADEM 1 Arc-Second Global DEM",
            "NASA POWER Climatology API"
        ],
        "auxiliary_datasets": [
            "ISRIC SoilGrids 250m",
            "WorldPop High Resolution Population",
            "OpenStreetMap Water Infrastructure"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
