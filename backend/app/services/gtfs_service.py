"""GTFS data service for transit information."""
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..config import settings


class GTFSService:
    """Service for reading and serving GTFS transit data."""

    def __init__(self):
        self.gtfs_dir = settings.GTFS_DIR
        self._routes_cache: Optional[List[Dict[str, Any]]] = None
        self._stops_cache: Optional[List[Dict[str, Any]]] = None

    def _read_csv(self, filename: str) -> List[Dict[str, str]]:
        """Read a GTFS CSV file and return list of dicts."""
        file_path = self.gtfs_dir / filename
        if not file_path.exists():
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def get_routes(self) -> List[Dict[str, Any]]:
        """
        Get all transit routes from GTFS data.

        Returns:
            List of route dictionaries with route information
        """
        if self._routes_cache is not None:
            return self._routes_cache

        routes_data = self._read_csv('routes.txt')
        routes = []

        for route in routes_data:
            routes.append({
                "route_id": route.get('route_id'),
                "route_short_name": route.get('route_short_name'),
                "route_long_name": route.get('route_long_name'),
                "route_type": int(route.get('route_type', 3)),  # 3 = Bus
                "route_type_name": self._get_route_type_name(int(route.get('route_type', 3))),
                "route_color": route.get('route_color', 'FFFFFF')
            })

        self._routes_cache = routes
        return routes

    def get_route_by_id(self, route_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific route by ID.

        Args:
            route_id: The route identifier

        Returns:
            Route dictionary or None if not found
        """
        routes = self.get_routes()
        for route in routes:
            if route['route_id'] == route_id:
                return route
        return None

    def get_stops(self, route_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all transit stops from GTFS data.

        Args:
            route_id: Optional route ID to filter stops by route

        Returns:
            List of stop dictionaries with stop information
        """
        if self._stops_cache is None:
            stops_data = self._read_csv('stops.txt')
            stops = []

            for stop in stops_data:
                stops.append({
                    "stop_id": stop.get('stop_id'),
                    "stop_name": stop.get('stop_name'),
                    "stop_lat": float(stop.get('stop_lat', 0)),
                    "stop_lon": float(stop.get('stop_lon', 0)),
                    "stop_desc": stop.get('stop_desc', '')
                })

            self._stops_cache = stops

        if route_id:
            return self._filter_stops_by_route(route_id)

        return self._stops_cache

    def get_stop_by_id(self, stop_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific stop by ID.

        Args:
            stop_id: The stop identifier

        Returns:
            Stop dictionary or None if not found
        """
        stops = self.get_stops()
        for stop in stops:
            if stop['stop_id'] == stop_id:
                return stop
        return None

    def search_stops(self, query: str) -> List[Dict[str, Any]]:
        """
        Search stops by name.

        Args:
            query: Search query string

        Returns:
            List of matching stops
        """
        stops = self.get_stops()
        query_lower = query.lower()
        return [
            stop for stop in stops
            if query_lower in stop['stop_name'].lower()
        ]

    def _filter_stops_by_route(self, route_id: str) -> List[Dict[str, Any]]:
        """Filter stops by route using stop_times and trips."""
        trips_data = self._read_csv('trips.txt')
        stop_times_data = self._read_csv('stop_times.txt')

        # Get trip IDs for this route
        trip_ids = [trip['trip_id'] for trip in trips_data if trip.get('route_id') == route_id]

        # Get stop IDs for these trips
        stop_ids = set()
        for stop_time in stop_times_data:
            if stop_time.get('trip_id') in trip_ids:
                stop_ids.add(stop_time.get('stop_id'))

        # Filter stops
        return [stop for stop in self._stops_cache if stop['stop_id'] in stop_ids]

    def get_trips(self, route_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get trips, optionally filtered by route."""
        trips_data = self._read_csv('trips.txt')

        if route_id:
            return [trip for trip in trips_data if trip.get('route_id') == route_id]

        return trips_data

    def get_stop_times(self, trip_id: str) -> List[Dict[str, Any]]:
        """Get stop times for a specific trip."""
        stop_times_data = self._read_csv('stop_times.txt')

        times = [st for st in stop_times_data if st.get('trip_id') == trip_id]

        # Sort by stop sequence
        times.sort(key=lambda x: int(x.get('stop_sequence', 0)))

        return times

    @staticmethod
    def _get_route_type_name(route_type: int) -> str:
        """Convert GTFS route_type code to readable name."""
        route_types = {
            0: "Tram",
            1: "Subway",
            2: "Rail",
            3: "Bus",
            4: "Ferry",
            5: "Cable Car",
            6: "Gondola",
            7: "Funicular"
        }
        return route_types.get(route_type, "Unknown")
