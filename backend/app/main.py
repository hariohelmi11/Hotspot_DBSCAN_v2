import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import dashboard, hotspots, incidents, geojson, jobs
from app.jobs.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title="Web GIS Hotspot Kerawanan Ketertiban Umum DKI Jakarta",
    description=(
        "REST API untuk analisis hotspot kerawanan ketertiban umum "
        "DKI Jakarta berbasis DBSCAN."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(hotspots.router, prefix="/api/v1/hotspots", tags=["Hotspots"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["Incidents"])
app.include_router(geojson.router, prefix="/api/v1/geojson", tags=["GeoJSON"])
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.get("/", tags=["Root"])
def root():
    return {"message": "Web GIS Hotspot API", "docs": "/docs", "version": "1.0.0"}
