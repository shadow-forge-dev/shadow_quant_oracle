import sqlite3
import random
from datetime import datetime, timedelta

db_path = "oracle_data.db"

# Create database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA journal_mode=WAL;")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        subreddit TEXT,
        title TEXT,
        score INTEGER,
        sentiment REAL,
        chain_signal TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON posts(sentiment);")
conn.commit()

# Generate test data
titles = [
    "Ethereum merge complete - bullish outlook",
    "Bitcoin dips below 30k, hodl strong",
    "New L2 solution launches on ETH",
    "SEC announces crypto investigation",
    "Vitalik speaks at conference about scaling",
    "Major exchange lists new altcoin",
    "DeFi protocol hacked for 10M",
    "Institutional investors buying ETH",
    "Gas fees drop to lowest in months",
    "Whale moves 50k BTC to exchange",
    "Community excited about upcoming fork",
    "Staking rewards increase significantly",
    "FUD spreads about regulation",
    "Development team ships major update",
    "Price prediction: ETH to moon"
]

test_data = []
for i, title in enumerate(titles):
    sentiment = random.uniform(-0.8, 0.9)
    chain_signal = random.choice(['LOW_GAS', 'NORMAL', 'WHALE_ALERT', 'N/A'])
    timestamp = (datetime.now() - timedelta(hours=i)).isoformat()
    
    test_data.append((
        f'test_{i}',
        random.choice(['ethereum', 'bitcoin']),
        title,
        random.randint(10, 500),
        round(sentiment, 4),
        chain_signal
    ))

cursor.executemany('''
    INSERT OR REPLACE INTO posts (id, subreddit, title, score, sentiment, chain_signal)
    VALUES (?, ?, ?, ?, ?, ?)
''', test_data)

conn.commit()
conn.close()

print(f"Created test database with {len(test_data)} posts")
print("Run: streamlit run streamlit_dashboard.py")
