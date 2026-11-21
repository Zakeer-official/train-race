# 🚆 Train Race — Indian Railway Head-to-Head Comparison Platform

> **Don't just track trains. Predict which train will reach the destination first.**

[![Backend Tests](https://img.shields.io/badge/tests-10%20passed-brightgreen.svg)]()
[![FastAPI](https://img.shields.io/badge/backend-FastAPI%201.0-009688.svg)]()
[![Next.js](https://img.shields.io/badge/frontend-Next.js%2014-black.svg)]()
[![TypeScript](https://img.shields.io/badge/typescript-strict-blue.svg)]()
[![Tailwind CSS](https://img.shields.io/badge/styles-TailwindCSS-38bdf8.svg)]()

---

## Overview

Existing Indian Railway tracking applications focus on monitoring individual trains in isolation. Passengers, relatives, or railway enthusiasts traveling on different trains towards a common destination (e.g., Mahbubabad, New Delhi, Vijayawada) are forced to switch between multiple tabs and mentally calculate arrival gaps.

**Train Race** solves this by providing a unified head-to-head comparison platform that:
1. Concurrently tracks two trains racing towards a common destination.
2. Evaluates arrival times using a multi-level ETA framework (live telemetry speed, intermediate halt durations, and delay propagation).
3. Prominently identifies the predicted leader and exact time margin.
4. Visualizes dual-route convergence via an interactive OpenStreetMap Leaflet map and linear track tracker.
5. Enables zero-friction race sharing via WhatsApp and unguessable public URLs requiring no user login.

---

## Key Features

- **Side-by-Side Dual Telemetry:** Desktop side-by-side and mobile-optimized stacked views showing real-time speeds, remaining route distances, and current reported stations.
- **Multi-Level Prediction Hierarchy:**
  - **Level 1 (Live Telemetry):** GPS coordinates & live cruising speed.
  - **Level 2 (Sequence Engine):** Track sequence distance calculation incorporating intermediate halt durations.
  - **Level 3 (Timetable Blend):** Official timetable blended with latest observed departure delay.
  - **Level 4 (Stale Warning):** Transparent warnings when data freshness exceeds thresholds.
- **Dynamic Common Destination Validation:** Automatically scans routes of both trains to identify common upcoming stations.
- **Lead-Change Tracking:** Captures and logs every change of lead with timestamps and margin evolution.
- **Live Auto-Refresh & SSE:** Server-Sent Events stream with client-side countdown timer and pause/resume controls.
- **One-Click Sharing:** WhatsApp prefilled sharing and clipboard copy for public race sessions.

---

## Technology Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS with custom dark navy railway theme
- **Icons:** Lucide React
- **Charts:** Recharts
- **Maps:** Leaflet & OpenStreetMap

### Backend
- **Framework:** Python 3.12 + FastAPI
- **Validation:** Pydantic V2 + Pydantic Settings
- **ORM & Database:** SQLAlchemy (async) with SQLite for local development and PostgreSQL support for production
- **Testing:** Pytest & pytest-asyncio
- **HTTP Client:** HTTPX

---

## Architecture

```
train-race/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app & lifespan configuration
│   │   ├── config.py            # Environment settings
│   │   ├── database.py          # Async SQLAlchemy engine
│   │   ├── models/              # Train, Station, RaceSession, Snapshots
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── providers/           # Base provider, RapidAPI, Demo provider
│   │   ├── engine/              # ETACalculator & TrainComparisonEngine
│   │   ├── api/                 # Trains, Stations, Races, Health endpoints
│   │   └── services/            # Cache service & Race service
│   ├── tests/                   # 10 automated unit and integration tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router (Landing, Create, Race, About)
│   │   ├── components/          # TrainCard, RaceLeaderBanner, ProgressTracker, Map
│   │   └── lib/                 # API client & TypeScript interfaces
│   └── package.json
├── docker-compose.yml
├── PROJECT_STATUS.md
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Clone & Setup Repository
```bash
git clone https://github.com/your-username/train-race.git
cd train-race
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt greenlet
```

Run tests:
```bash
$env:PYTHONPATH = "."
pytest -v
```

Start backend API:
```bash
uvicorn app.main:app --reload --port 8000
```
API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Docker Deployment

Run both backend and frontend via Docker Compose:
```bash
docker-compose up --build
```

---

## Environment Variables

Copy `.env.example` to `.env`:
```ini
ENVIRONMENT=development
DATABASE_URL=sqlite+aiosqlite:///./train_race.db
RAILWAY_API_PROVIDER=demo # or "rapidapi"
RAPIDAPI_KEY=your_key_here
REFRESH_INTERVAL_SECONDS=15
```

---

## Data Disclosure & Disclaimer

Train Race is an independent analytical application. For official reservation and ticketing, refer to [IRCTC](https://www.irctc.co.in).
