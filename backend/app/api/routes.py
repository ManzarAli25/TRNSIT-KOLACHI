"""API route handlers for TRNSIT Kolachi."""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from ..services import ValhallaService, GTFSService


router = APIRouter()
valhalla_service = ValhallaService()
gtfs_service = GTFSService()


# Request/Response Models
class Location(BaseModel):
    """Geographic location."""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")


class RouteRequest(BaseModel):
    """Route request parameters."""
    origin: Location
    destination: Location
    costing: str = Field(
        default="multimodal",
        description="Routing mode: auto, bicycle, pedestrian, multimodal, transit, bus"
    )
    options: Optional[Dict[str, Any]] = None


class IsochroneRequest(BaseModel):
    """Isochrone request parameters."""
    location: Location
    costing: str = Field(default="pedestrian", description="Travel mode")
    contours: List[int] = Field(default=[5, 10, 15], description="Time contours in minutes")
    polygons: bool = Field(default=True, description="Return as polygons")


# Health Check
@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Check API and Valhalla service health.

    Returns:
        Health status of the API and routing service
    """
    valhalla_healthy = await valhalla_service.health_check()

    return {
        "status": "healthy" if valhalla_healthy else "degraded",
        "api": "healthy",
        "valhalla": "healthy" if valhalla_healthy else "unavailable",
        "message": "All services operational" if valhalla_healthy else "Valhalla service unavailable"
    }


# Routing Endpoints
@router.post("/route")
async def get_route(request: RouteRequest) -> Dict[str, Any]:
    """
    Calculate a route between origin and destination.

    Args:
        request: Route request with origin, destination, and options

    Returns:
        Route information including directions and geometry
    """
    try:
        route = await valhalla_service.get_route(
            origin=request.origin.model_dump(),
            destination=request.destination.model_dump(),
            costing=request.costing,
            options=request.options
        )
        return route
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/isochrone")
async def get_isochrone(request: IsochroneRequest) -> Dict[str, Any]:
    """
    Calculate reachability isochrone from a location.

    Args:
        request: Isochrone request with location and parameters

    Returns:
        Isochrone polygons or linestrings
    """
    try:
        isochrone = await valhalla_service.get_isochrone(
            location=request.location.model_dump(),
            costing=request.costing,
            contours=request.contours,
            polygons=request.polygons
        )
        return isochrone
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GTFS Data Endpoints
@router.get("/routes")
async def get_routes() -> List[Dict[str, Any]]:
    """
    Get all available transit routes.

    Returns:
        List of transit routes from GTFS data
    """
    try:
        routes = gtfs_service.get_routes()
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/routes/{route_id}")
async def get_route_by_id(route_id: str) -> Dict[str, Any]:
    """
    Get a specific transit route by ID.

    Args:
        route_id: Route identifier

    Returns:
        Route information
    """
    route = gtfs_service.get_route_by_id(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.get("/stops")
async def get_stops(
    route_id: Optional[str] = Query(None, description="Filter stops by route ID"),
    search: Optional[str] = Query(None, description="Search stops by name")
) -> List[Dict[str, Any]]:
    """
    Get transit stops, optionally filtered by route or search query.

    Args:
        route_id: Optional route ID to filter stops
        search: Optional search query for stop names

    Returns:
        List of transit stops
    """
    try:
        if search:
            stops = gtfs_service.search_stops(search)
        else:
            stops = gtfs_service.get_stops(route_id)
        return stops
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stops/{stop_id}")
async def get_stop_by_id(stop_id: str) -> Dict[str, Any]:
    """
    Get a specific transit stop by ID.

    Args:
        stop_id: Stop identifier

    Returns:
        Stop information
    """
    stop = gtfs_service.get_stop_by_id(stop_id)
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    return stop
