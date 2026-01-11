# TRNSIT Kolachi Backend

FastAPI backend server for TRNSIT Kolachi transit routing application.

## Architecture

```
backend/
├── app/                    # FastAPI application
│   ├── api/               # API routes
│   │   └── routes.py      # Endpoint definitions
│   ├── services/          # Business logic
│   │   ├── valhalla_service.py  # Valhalla routing integration
│   │   └── gtfs_service.py      # GTFS data service
│   ├── config.py          # Configuration settings
│   └── main.py           # FastAPI app initialization
├── data/                  # Application data
│   └── gtfs/             # GTFS transit data
│       ├── routes.txt    # Transit routes
│       └── stops.txt     # Transit stops
├── valhalla/             # Valhalla routing engine data
│   ├── valhalla.json     # Valhalla configuration
│   ├── valhalla_tiles/   # Pre-built routing tiles
│   ├── valhalla_tiles.tar
│   └── *.osm.pbf        # OpenStreetMap data
└── requirements.txt      # Python dependencies
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and adjust settings:

```bash
cp .env.example .env
```

Key settings:
- `VALHALLA_URL`: URL to Valhalla routing service (default: http://localhost:8002)
- `PORT`: API server port (default: 8000)

### 3. Start Valhalla (Optional)

If you want to use actual routing (not just GTFS data), start Valhalla with Docker:

```bash
docker run -d \
  --name valhalla \
  -p 8002:8002 \
  -v "$(pwd)/valhalla:/custom_files" \
  ghcr.io/gis-ops/docker-valhalla/valhalla:latest
```

**Note:** The Valhalla tiles are already pre-built in `valhalla/valhalla_tiles/`. The container should detect and use them automatically.

### 4. Run the API Server

```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API and Valhalla service health

### Routing
- `POST /api/v1/route` - Calculate route between two points
- `POST /api/v1/isochrone` - Get reachability isochrone from a location

### GTFS Data
- `GET /api/v1/routes` - Get all transit routes
- `GET /api/v1/routes/{route_id}` - Get specific route
- `GET /api/v1/stops` - Get all transit stops
- `GET /api/v1/stops?search={query}` - Search stops by name
- `GET /api/v1/stops/{stop_id}` - Get specific stop

## Example Usage

### Get a Route

```bash
curl -X POST "http://localhost:8000/api/v1/route" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": {"lat": 24.9, "lon": 67.1},
    "destination": {"lat": 24.87, "lon": 67.03},
    "costing": "multimodal"
  }'
```

### Get Transit Stops

```bash
curl "http://localhost:8000/api/v1/stops"
```

### Search Stops

```bash
curl "http://localhost:8000/api/v1/stops?search=Numaish"
```

## Development

### Project Structure

- **app/api/routes.py**: API endpoint definitions with request/response models
- **app/services/valhalla_service.py**: Async HTTP client for Valhalla routing
- **app/services/gtfs_service.py**: GTFS data parser and query service
- **app/config.py**: Centralized configuration using Pydantic settings
- **app/main.py**: FastAPI application setup with CORS and lifecycle

### Adding New Endpoints

1. Define request/response models in `app/api/routes.py`
2. Add route handler with `@router.get/post/etc`
3. Implement business logic in appropriate service
4. Document with docstrings (auto-generates OpenAPI docs)

### Extending GTFS Data

The current GTFS data is minimal. To add more transit data:

1. Add GTFS files to `data/gtfs/`:
   - `trips.txt` - Trip definitions
   - `stop_times.txt` - Stop sequences and times
   - `calendar.txt` - Service schedules
   - `shapes.txt` - Route geometries

2. Extend `GTFSService` to parse new files

3. Add new endpoints in `routes.py` for trip planning, schedules, etc.

## Valhalla Configuration

The `valhalla/valhalla.json` file contains Valhalla routing engine configuration. Key settings:

- **Multimodal routing**: Enabled with transit support
- **Service limits**: Configured for Karachi's scale
- **Tile directory**: Points to pre-built tiles in `valhalla_tiles/`

Modify this file to adjust routing behavior, cost models, or service limits.

## Production Deployment

For production:

1. Set `RELOAD=false` in `.env`
2. Use a production ASGI server (uvicorn with workers or gunicorn)
3. Set up proper CORS origins instead of `*`
4. Run Valhalla in a separate container/service
5. Consider adding authentication/rate limiting
6. Set up logging and monitoring

Example production command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### Valhalla service unavailable

If `/api/v1/health` shows Valhalla as unavailable:
1. Verify Valhalla container is running: `docker ps`
2. Check Valhalla logs: `docker logs valhalla`
3. Verify `VALHALLA_URL` in `.env` matches container port
4. Test Valhalla directly: `curl http://localhost:8002/status`

### GTFS data not loading

1. Verify files exist in `data/gtfs/`
2. Check file permissions
3. Ensure CSV format is correct (comma-separated, UTF-8)
4. Check API logs for parsing errors
