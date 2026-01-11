"""Simple test script to verify API setup without Valhalla."""
import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services import GTFSService


async def test_gtfs_service():
    """Test GTFS service functionality."""
    print("Testing GTFS Service...\n")

    service = GTFSService()

    # Test routes
    print("Routes:")
    routes = service.get_routes()
    for route in routes:
        print(f"  - {route['route_short_name']}: {route['route_long_name']} ({route['route_type_name']})")

    print(f"\n  Total routes: {len(routes)}")

    # Test stops
    print("\nStops:")
    stops = service.get_stops()
    for stop in stops:
        print(f"  - {stop['stop_name']} ({stop['stop_lat']}, {stop['stop_lon']})")

    print(f"\n  Total stops: {len(stops)}")

    # Test search
    print("\nSearch for 'Numaish':")
    results = service.search_stops("Numaish")
    for result in results:
        print(f"  - {result['stop_name']}")

    print("\n[OK] GTFS Service test completed successfully!")


def test_imports():
    """Test that all imports work."""
    print("Testing imports...\n")

    try:
        from app.main import app
        print("[OK] FastAPI app imported successfully")

        from app.services import ValhallaService, GTFSService
        print("[OK] Services imported successfully")

        from app.api.routes import router
        print("[OK] API routes imported successfully")

        from app.config import settings
        print(f"[OK] Settings loaded: {settings.API_TITLE}")

        print("\n[OK] All imports successful!")
        return True
    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("TRNSIT Kolachi Backend Test")
    print("=" * 60)
    print()

    # Test imports first
    if not test_imports():
        sys.exit(1)

    print("\n" + "=" * 60)
    print()

    # Test GTFS service
    asyncio.run(test_gtfs_service())

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python run.py")
    print("2. Visit: http://localhost:8000/docs")
    print("3. (Optional) Start Valhalla: docker-compose up valhalla")
