# Quant Oracle - TradingView-Style Dashboard

A professional full-stack cryptocurrency sentiment analysis dashboard inspired by TradingView, featuring real-time data updates, advanced charting, and a modern dark theme UI.

##  Features

- **Real-time Sentiment Analysis** - Live sentiment tracking from Reddit crypto communities
- **TradingView-Style Charts** - Professional candlestick charts using Lightweight Charts library
- **WebSocket Updates** - Real-time data streaming for instant updates
- **Modern Dark Theme** - Sleek, professional UI matching TradingView aesthetics
- **Interactive Visualizations** - Pie charts, line charts, and data tables
- **REST API** - Full-featured FastAPI backend with comprehensive endpoints

##  Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────┐
│  React Frontend │ ◄─────► │  FastAPI Backend │ ◄─────► │   SQLite DB  │
│   (Port 5173)   │         │   (Port 8000)    │         │              │
└─────────────────┘         └──────────────────┘         └──────────────┘
        │                            │
        │                            │
        └────── WebSocket ───────────┘
```

##  Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database
- **WebSockets** - Real-time communication
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Lightweight Charts** - TradingView charting library
- **Recharts** - Additional visualizations
- **Lucide React** - Icon library

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Generate test data (optional):
```bash
python3 test_backend.py
```

3. Start the FastAPI server:
```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 📡 API Endpoints

### REST Endpoints

- `GET /` - API health check
- `GET /api/posts` - Fetch posts with pagination
  - Query params: `limit`, `offset`, `min_sentiment`
- `GET /api/metrics` - Get aggregated metrics
- `GET /api/sentiment-timeline` - Time-series sentiment data
- `GET /api/subreddit-stats` - Per-subreddit statistics
- `GET /api/signal-distribution` - Chain signal distribution

### WebSocket

- `WS /ws` - Real-time metrics updates (broadcasts every 5 seconds)

##  Components

### Frontend Components

- **Header** - Top navigation with live ticker
- **Sidebar** - Navigation menu
- **MetricsPanel** - Key metrics cards
- **Chart** - TradingView-style sentiment timeline
- **SignalDistribution** - Pie chart for chain signals
- **PostFeed** - Live feed of Reddit posts

## 🔧 Configuration

### Reddit API Credentials

Update `oracle_backend.py` with your Reddit API credentials:

```python
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
```

Get credentials at: https://www.reddit.com/prefs/apps

### Backend Scraper

Run the scraper to collect real data:

```bash
python3 oracle_backend.py --subs ethereum,bitcoin --limit 20 --sentiment --chain
```

##  Usage

1. Start the backend API server (port 8000)
2. Start the frontend dev server (port 5173)
3. Open `http://localhost:5173` in your browser
4. View real-time sentiment data and charts

## Features Breakdown

### Metrics Dashboard
- Average sentiment score
- Bullish/bearish post counts
- Whale alert tracking
- Total posts monitored

### Sentiment Timeline
- Interactive line chart
- Zoom and pan capabilities
- Hover tooltips with post details
- Real-time updates

### Post Feed
- Live Reddit posts
- Sentiment scores
- Chain signal badges
- Subreddit filtering

##  Production Build

Build the frontend for production:

```bash
cd frontend
npm run build
```

The production files will be in `frontend/dist/`

## License

MIT License

##  Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

Built with ❤️ using FastAPI, React, and TradingView Lightweight Charts
