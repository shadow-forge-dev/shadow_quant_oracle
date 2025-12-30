import { TrendingUp, RefreshCw } from 'lucide-react';
import './Header.css';

function Header({ metrics, onRefresh }) {
    return (
        <header className="header">
            <div className="header-left">
                <div className="logo">
                    <TrendingUp size={24} />
                    <span className="logo-text">Quant Oracle</span>
                </div>
                <div className="header-ticker">
                    <div className="ticker-item">
                        <span className="ticker-label">Avg Sentiment</span>
                        <span className={`ticker-value ${metrics?.avg_sentiment > 0 ? 'positive' : 'negative'}`}>
                            {metrics?.avg_sentiment?.toFixed(4) || '0.0000'}
                        </span>
                    </div>
                    <div className="ticker-item">
                        <span className="ticker-label">Posts</span>
                        <span className="ticker-value">{metrics?.total_posts || 0}</span>
                    </div>
                    <div className="ticker-item">
                        <span className="ticker-label">Bullish</span>
                        <span className="ticker-value positive">{metrics?.bullish_percentage?.toFixed(1)}%</span>
                    </div>
                </div>
            </div>
            <div className="header-right">
                <button className="refresh-btn" onClick={onRefresh}>
                    <RefreshCw size={18} />
                    Refresh
                </button>
            </div>
        </header>
    );
}

export default Header;
