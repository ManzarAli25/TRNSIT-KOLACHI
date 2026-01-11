# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TRNSIT Kolachi** is a transit application for Karachi's public transport system. The project consists of:
- **Mobile App** (React Native/Expo): User-facing mobile application with journey planning
- **Backend** (Maps): Routing infrastructure with Valhalla tiles and GTFS data for Karachi

## Development Commands

### Mobile App (mobile-app/)

Start the development server:
```bash
cd mobile-app
npx expo start
```

Platform-specific commands:
```bash
npm run android    # Start on Android
npm run ios        # Start on iOS
npm run web        # Start on web
```

Install dependencies:
```bash
cd mobile-app
npm install
```

### Backend API (backend/)

Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Run the FastAPI server:
```bash
cd backend
python run.py
# Or: uvicorn app.main:app --reload
```

Run with Docker (API + Valhalla):
```bash
cd backend
docker-compose up -d
```

API documentation available at: http://localhost:8000/docs

## Code Architecture

### Mobile App Structure

The app follows a **3-screen architecture** reflecting the user journey:

1. **SearchScreen** - "Where to?" entry point with popular hubs and recent searches
2. **ResultsScreen** - Route comparison showing different transport options (Green Line BRT, Red Bus, coaches)
3. **JourneyScreen** - Step-by-step vertical timeline visualization of the selected route

**Key directories:**
- `screens/` - Three main screens implementing the core user flow
- `components/` - Reusable UI components (Button, RouteCard, Timeline)
- `data/mockRoutes.ts` - Mock data defining routes with steps (walk, bus, brt, transfer types)
- `constants/theme.ts` - Design system with colors, fonts, spacing, and radius values

**Navigation:** React Navigation with native stack navigator. All screens use headerShown: false for custom headers.

**Data Model:**
- `Route`: Contains serviceName, serviceType, totalFare, duration, tags, steps, and color
- `Step`: Represents journey segments with type (walk/bus/brt/transfer), instruction, and optional detail

### Design System (constants/theme.ts)

**Color Palette** inspired by the logo's "Kolachi vibe":
- `backgroundDark: '#0A0A0A'` - Primary background
- `neonLime: '#CBFF00'` - Primary accent (replaces transitYellow in legacy code)
- `asphaltBlack: '#1A1A1B'` - Surface color
- `pbsRed: '#E63946'` - People's Bus Service indicator
- `greenLine: '#2A9D8F'` - BRT-specific color

**Fonts:** Inter family loaded via @expo-google-fonts/inter (400, 500, 700 weights)

**Spacing/Radius:** Token-based system (xs to xxl) for consistent layouts

### Backend API Structure

The backend is a **FastAPI application** providing routing and transit data services:

```
backend/
├── app/                         # FastAPI application
│   ├── api/routes.py           # API endpoints
│   ├── services/
│   │   ├── valhalla_service.py # Valhalla routing client
│   │   └── gtfs_service.py     # GTFS data parser
│   ├── config.py               # Settings management
│   └── main.py                 # App initialization
├── data/gtfs/                  # Transit data
│   ├── routes.txt              # Route definitions (Green Line BRT)
│   └── stops.txt               # Stop locations
└── valhalla/                   # Routing engine data
    ├── valhalla.json           # Configuration
    ├── valhalla_tiles/         # Pre-built routing graph (551MB)
    └── pakistan-251227.osm.pbf # OSM data (140MB)
```

**API Endpoints:**
- `GET /api/v1/health` - Service health check
- `POST /api/v1/route` - Calculate routes with multimodal support
- `POST /api/v1/isochrone` - Reachability analysis
- `GET /api/v1/routes` - List transit routes
- `GET /api/v1/stops` - Get/search transit stops

**Services:**
- **ValhallaService**: Async HTTP client for Valhalla routing engine (runs on port 8002)
- **GTFSService**: Parses GTFS CSV files and provides in-memory querying

**Configuration:** Uses Pydantic Settings with .env support. Key settings: VALHALLA_URL, PORT, CORS_ORIGINS.

## Key Development Notes

### POC Scope
The current implementation is a proof-of-concept focusing on the **Gulshan-e-Iqbal to Tower** journey. Search functionality is hardcoded to demonstrate the Journey Screen's step-by-step timeline, which is the core feature of the app.

### Font Loading
The app uses expo-splash-screen to prevent auto-hide until Inter fonts are loaded. The splash screen shows until fonts are ready, preventing FOUT (Flash of Unstyled Text).

### TypeScript
All source files use TypeScript. The project has a minimal tsconfig.json extending Expo's base configuration.

### Styling Pattern
All screens use StyleSheet.create with inline styles. Components import theme constants for consistency. The design prioritizes high contrast and large tap targets for mobile usability in crowded environments.

### Backend Integration Strategy

The backend provides REST API endpoints that the mobile app can consume:

**Current State:**
- Mobile app uses `mockRoutes.ts` with hardcoded data
- Backend API is ready but not yet integrated with the app
- Valhalla requires Docker container to run (tiles pre-built)

**Integration Steps:**
1. **Replace mock data**: Create API client in mobile app to call `/api/v1/routes` and `/api/v1/stops`
2. **Route calculation**: Use `/api/v1/route` endpoint for real-time journey planning
3. **Parse responses**: Transform Valhalla route response into Step[] format for Timeline component
4. **Handle multimodal**: Valhalla supports transit+pedestrian routing when configured

**Architecture Pattern:**
- Backend: FastAPI async services → Valhalla HTTP API
- Mobile: React Native → Backend REST API → Valhalla routing
- Data flow: GTFS CSV → GTFSService (in-memory) → JSON API → Mobile app

**Deployment:**
- Run Valhalla in Docker (uses pre-built tiles from valhalla_tiles/)
- Run FastAPI server (connects to Valhalla via HTTP)
- Mobile app connects to FastAPI (not directly to Valhalla)
