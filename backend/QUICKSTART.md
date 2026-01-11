# Quick Start Guide

## Option 1: API Only (Without Routing)

If you just want to test the GTFS data endpoints without Valhalla routing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

Visit http://localhost:8000/docs to explore the API.

**Available endpoints:**
- `GET /api/v1/routes` - Get Green Line BRT route
- `GET /api/v1/stops` - Get 5 BRT stops
- `GET /api/v1/stops?search=Numaish` - Search stops

## Option 2: Full Stack (API + Valhalla Routing)

For complete routing functionality with multimodal support:

```bash
# Start both services with Docker
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
docker-compose logs -f valhalla
```

The Valhalla service takes a few minutes to start (loading 551MB of tiles).

**Test routing:**
```bash
curl -X POST "http://localhost:8000/api/v1/route" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": {"lat": 24.9, "lon": 67.1},
    "destination": {"lat": 24.87, "lon": 67.03},
    "costing": "multimodal"
  }'
```

## Option 3: Development Mode

For active development with auto-reload:

```bash
# Terminal 1: Start Valhalla
docker-compose up valhalla

# Terminal 2: Run API in dev mode
python run.py
# Changes to app/ files will auto-reload
```

## Testing

Run the test script to verify everything works:

```bash
python test_api.py
```

Expected output:
- All imports successful
- 1 route loaded (Green Line BRT)
- 5 stops loaded
- Search working

## Common Issues

### Port 8000 already in use
```bash
# Change port in .env
PORT=8001

# Or kill existing process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Valhalla not responding
```bash
# Check if container is running
docker ps

# Restart Valhalla
docker-compose restart valhalla

# Check logs
docker-compose logs valhalla
```

### GTFS data not found
Ensure `data/gtfs/` contains:
- routes.txt
- stops.txt

Check file paths in config.py if files are elsewhere.

## Next Steps

1. Explore API docs: http://localhost:8000/docs
2. Test health check: http://localhost:8000/api/v1/health
3. Add more GTFS data to `data/gtfs/`
4. Integrate with mobile app
