"""Valhalla routing service integration."""
import httpx
from typing import Dict, Any, List, Optional
from ..config import settings


class ValhallaService:
    """Service for interacting with Valhalla routing engine."""

    def __init__(self):
        self.base_url = settings.VALHALLA_URL
        self.timeout = settings.VALHALLA_TIMEOUT

    async def get_route(
        self,
        origin: Dict[str, float],
        destination: Dict[str, float],
        costing: str = "multimodal",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get a route from origin to destination.

        Args:
            origin: Dict with 'lat' and 'lon' keys
            destination: Dict with 'lat' and 'lon' keys
            costing: Routing cost model (auto, bicycle, pedestrian, multimodal, transit, bus)
            options: Additional routing options

        Returns:
            Route response from Valhalla
        """
        request_body = {
            "locations": [
                {"lat": origin["lat"], "lon": origin["lon"]},
                {"lat": destination["lat"], "lon": destination["lon"]}
            ],
            "costing": costing,
            "directions_options": {
                "units": "kilometers",
                "language": "en-US"
            }
        }

        # Add costing options if provided
        if options:
            request_body["costing_options"] = options
        elif costing == "multimodal":
            # Default multimodal options to enable transit
            request_body["costing_options"] = {
                "transit": {
                    "use_bus": 1,
                    "use_rail": 1,
                    "use_transfers": 1
                },
                "pedestrian": {
                    "use_ferry": 0,
                    "use_living_streets": 0.5,
                    "use_tracks": 0
                }
            }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/route",
                    json=request_body
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Valhalla routing error: {str(e)}")

    async def get_isochrone(
        self,
        location: Dict[str, float],
        costing: str = "pedestrian",
        contours: List[int] = [5, 10, 15],
        polygons: bool = True
    ) -> Dict[str, Any]:
        """
        Get isochrone (reachability) from a location.

        Args:
            location: Dict with 'lat' and 'lon' keys
            costing: Travel mode
            contours: Time contours in minutes
            polygons: Return as polygons vs linestrings

        Returns:
            Isochrone response from Valhalla
        """
        request_body = {
            "locations": [{"lat": location["lat"], "lon": location["lon"]}],
            "costing": costing,
            "contours": [{"time": t} for t in contours],
            "polygons": polygons
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/isochrone",
                    json=request_body
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Valhalla isochrone error: {str(e)}")

    async def health_check(self) -> bool:
        """
        Check if Valhalla service is available.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/status")
                return response.status_code == 200
        except:
            return False
