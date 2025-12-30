from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
import asyncio

app = FastAPI(title="Quant Oracle API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "oracle_data.db"

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def root():
    return {"message": "Quant Oracle API", "version": "1.0.0"}

@app.get("/api/posts")
async def get_posts(limit: int = 100, offset: int = 0, min_sentiment: Optional[float] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM posts ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params = [limit, offset]
    
    if min_sentiment is not None:
        query = "SELECT * FROM posts WHERE sentiment >= ? ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params = [min_sentiment, limit, offset]
    
    cursor.execute(query, params)
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"posts": posts, "count": len(posts)}

@app.get("/api/metrics")
async def get_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM posts")
    total = cursor.fetchone()['total']
    
    cursor.execute("SELECT AVG(sentiment) as avg_sentiment FROM posts")
    avg_sentiment = cursor.fetchone()['avg_sentiment'] or 0
    
    cursor.execute("SELECT COUNT(*) as bullish FROM posts WHERE sentiment > 0.5")
    bullish = cursor.fetchone()['bullish']
    
    cursor.execute("SELECT COUNT(*) as bearish FROM posts WHERE sentiment < -0.5")
    bearish = cursor.fetchone()['bearish']
    
    cursor.execute("SELECT COUNT(*) as whale_alerts FROM posts WHERE chain_signal = 'WHALE_ALERT'")
    whale_alerts = cursor.fetchone()['whale_alerts']
    
    cursor.execute("SELECT COUNT(*) as low_gas FROM posts WHERE chain_signal = 'LOW_GAS'")
    low_gas = cursor.fetchone()['low_gas']
    
    conn.close()
    
    return {
        "total_posts": total,
        "avg_sentiment": round(avg_sentiment, 4),
        "bullish_count": bullish,
        "bearish_count": bearish,
        "whale_alerts": whale_alerts,
        "low_gas_count": low_gas,
        "bullish_percentage": round((bullish / total * 100) if total > 0 else 0, 2),
        "bearish_percentage": round((bearish / total * 100) if total > 0 else 0, 2)
    }

@app.get("/api/sentiment-timeline")
async def get_sentiment_timeline(limit: int = 50):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, sentiment, chain_signal, title, subreddit 
        FROM posts 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, [limit])
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"timeline": data}

@app.get("/api/subreddit-stats")
async def get_subreddit_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            subreddit,
            COUNT(*) as post_count,
            AVG(sentiment) as avg_sentiment,
            MAX(sentiment) as max_sentiment,
            MIN(sentiment) as min_sentiment
        FROM posts
        GROUP BY subreddit
        ORDER BY post_count DESC
    """)
    
    stats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    for stat in stats:
        stat['avg_sentiment'] = round(stat['avg_sentiment'], 4)
        stat['max_sentiment'] = round(stat['max_sentiment'], 4)
        stat['min_sentiment'] = round(stat['min_sentiment'], 4)
    
    return {"subreddit_stats": stats}

@app.get("/api/signal-distribution")
async def get_signal_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT chain_signal, COUNT(*) as count
        FROM posts
        GROUP BY chain_signal
    """)
    
    distribution = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"distribution": distribution}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send updates every 5 seconds
            await asyncio.sleep(5)
            
            # Get latest metrics
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM posts ORDER BY timestamp DESC LIMIT 1")
            latest = cursor.fetchone()
            
            cursor.execute("SELECT AVG(sentiment) as avg FROM posts")
            avg_sent = cursor.fetchone()['avg'] or 0
            
            conn.close()
            
            update = {
                "type": "metrics_update",
                "data": {
                    "avg_sentiment": round(avg_sent, 4),
                    "latest_post": dict(latest) if latest else None,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            await websocket.send_json(update)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
