import { TrendingUp, TrendingDown, AlertCircle, Activity } from 'lucide-react';
import './MetricsPanel.css';

function MetricsPanel({ metrics }) {
    if (!metrics) return null;

    const metricCards = [
        {
            label: 'Total Posts',
            value: metrics.total_posts,
            icon: Activity,
            color: 'blue'
        },
        {
            label: 'Bullish Signals',
            value: metrics.bullish_count,
            percentage: metrics.bullish_percentage,
            icon: TrendingUp,
            color: 'green'
        },
        {
            label: 'Bearish Signals',
            value: metrics.bearish_count,
            percentage: metrics.bearish_percentage,
            icon: TrendingDown,
            color: 'red'
        },
        {
            label: 'Whale Alerts',
            value: metrics.whale_alerts,
            icon: AlertCircle,
            color: 'yellow'
        }
    ];

    return (
        <div className="metrics-panel">
            {metricCards.map((metric, index) => (
                <div key={index} className={`metric-card ${metric.color}`}>
                    <div className="metric-header">
                        <span className="metric-label">{metric.label}</span>
                        <metric.icon size={18} className="metric-icon" />
                    </div>
                    <div className="metric-value">{metric.value}</div>
                    {metric.percentage !== undefined && (
                        <div className="metric-percentage">
                            {metric.percentage.toFixed(1)}%
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}

export default MetricsPanel;
