import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from datetime import datetime

DB_PATH = "oracle_data.db"

st.set_page_config(
    page_title="Quant Oracle",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        color: #ffffff;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #e0e6ed;
        font-weight: 600;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .stMetric label {
        color: #a0aec0 !important;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #cbd5e0;
    }
    
    .subtitle {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM posts ORDER BY timestamp DESC", conn)
        conn.close()
        
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    except Exception as err:
        st.error(f"Database error: {err}")
        return pd.DataFrame()

def create_sentiment_chart(df):
    if df.empty:
        return None
    
    color_map = {
        'LOW_GAS': '#10b981',
        'NORMAL': '#3b82f6', 
        'WHALE_ALERT': '#ef4444',
        'N/A': '#6b7280'
    }
    
    colors = df['chain_signal'].map(color_map).fillna('#6b7280')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['sentiment'],
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            line=dict(width=1, color='rgba(255,255,255,0.3)'),
            opacity=0.8
        ),
        text=df['title'],
        hovertemplate='<b>%{text}</b><br>Sentiment: %{y:.3f}<br>Time: %{x}<extra></extra>',
        showlegend=False
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)", line_width=1)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e6ed', family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            title='Time',
            title_font=dict(size=14, color='#a0aec0')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            title='Sentiment Score',
            title_font=dict(size=14, color='#a0aec0'),
            range=[-1.1, 1.1]
        ),
        height=400,
        margin=dict(l=60, r=40, t=40, b=60),
        hovermode='closest'
    )
    
    return fig

def main():
    st.markdown("<h1>📊 Quant Oracle</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Real-time sentiment analysis from crypto communities</p>", unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    with col_btn1:
        if st.button("🔄 Refresh"):
            st.rerun()

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data available. Run the backend to collect data.")
        st.code("python3 oracle_backend.py --subs ethereum,bitcoin --limit 20 --sentiment --chain", language="bash")
        st.info("💡 Make sure to set your Reddit API credentials in oracle_backend.py")
        return

    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_sentiment = df['sentiment'].mean()
    bull_count = df[df['sentiment'] > 0.5].shape[0]
    bear_count = df[df['sentiment'] < -0.5].shape[0]
    whale_count = df[df['chain_signal'] == 'WHALE_ALERT'].shape[0]

    with col1:
        delta_color = "normal" if avg_sentiment > 0 else "inverse"
        st.metric(
            "Avg Sentiment", 
            f"{avg_sentiment:.3f}",
            delta="Bullish" if avg_sentiment > 0 else "Bearish",
            delta_color=delta_color
        )
    
    with col2:
        st.metric("Bullish Posts", bull_count, delta=f"{(bull_count/len(df)*100):.1f}%")
    
    with col3:
        st.metric("Bearish Posts", bear_count, delta=f"{(bear_count/len(df)*100):.1f}%", delta_color="inverse")
    
    with col4:
        st.metric("Whale Alerts", whale_count, delta="High Activity" if whale_count > 3 else "Normal")

    st.markdown("---")
    st.markdown("### 📊 Sentiment Timeline")
    
    fig = create_sentiment_chart(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    col_legend1, col_legend2, col_legend3, col_legend4 = st.columns(4)
    with col_legend1:
        st.markdown("🟢 **Low Gas**")
    with col_legend2:
        st.markdown("🔵 **Normal**")
    with col_legend3:
        st.markdown("🔴 **Whale Alert**")
    with col_legend4:
        st.markdown("⚫ **N/A**")

    st.markdown("---")
    st.markdown("### 📋 Post Feed")
    
    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        min_score = st.slider("Minimum Sentiment Score", -1.0, 1.0, -1.0, 0.1)
    with col_filter2:
        signal_filter = st.selectbox("Chain Signal", ["All", "LOW_GAS", "NORMAL", "WHALE_ALERT", "N/A"])
    
    filtered_df = df[df['sentiment'] >= min_score].copy()
    if signal_filter != "All":
        filtered_df = filtered_df[filtered_df['chain_signal'] == signal_filter]
    
    if not filtered_df.empty:
        display_df = filtered_df[['subreddit', 'title', 'score', 'sentiment', 'chain_signal', 'timestamp']].copy()
        display_df['sentiment'] = display_df['sentiment'].round(3)
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "subreddit": st.column_config.TextColumn("Subreddit", width="small"),
                "title": st.column_config.TextColumn("Title", width="large"),
                "score": st.column_config.NumberColumn("Score", width="small"),
                "sentiment": st.column_config.NumberColumn("Sentiment", width="small"),
                "chain_signal": st.column_config.TextColumn("Signal", width="small"),
                "timestamp": st.column_config.TextColumn("Time", width="medium")
            }
        )
        st.caption(f"Showing {len(filtered_df)} of {len(df)} posts")
    else:
        st.info("No posts match the current filters")

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #718096;'>Built with Streamlit • Data updates in real-time</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
