from fastapi import APIRouter
from app.vehicle.endpoints import router as vehicle_router

api_router = APIRouter(prefix="/api")
api_router.include_router(vehicle_router)
