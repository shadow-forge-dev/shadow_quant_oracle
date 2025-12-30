import { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';
import './Chart.css';

function Chart({ data }) {
    const chartContainerRef = useRef();
    const chartRef = useRef();

    useEffect(() => {
        if (!chartContainerRef.current || !data || data.length === 0) return;

        const chart = createChart(chartContainerRef.current, {
            layout: {
                background: { color: '#1e222d' },
                textColor: '#d1d4dc',
            },
            grid: {
                vertLines: { color: '#2b2f3a' },
                horzLines: { color: '#2b2f3a' },
            },
            width: chartContainerRef.current.clientWidth,
            height: 400,
            timeScale: {
                timeVisible: true,
                secondsVisible: false,
            },
        });

        const lineSeries = chart.addLineSeries({
            color: '#2962ff',
            lineWidth: 2,
        });

        const chartData = data
            .map(item => ({
                time: new Date(item.timestamp).getTime() / 1000,
                value: item.sentiment
            }))
            .sort((a, b) => a.time - b.time);

        lineSeries.setData(chartData);

        const handleResize = () => {
            chart.applyOptions({ width: chartContainerRef.current.clientWidth });
        };

        window.addEventListener('resize', handleResize);
        chartRef.current = chart;

        return () => {
            window.removeEventListener('resize', handleResize);
            chart.remove();
        };
    }, [data]);

    return (
        <div className="chart-wrapper">
            <div className="chart-header">
                <h3>Sentiment Timeline</h3>
                <div className="chart-legend">
                    <span className="legend-item">
                        <span className="legend-dot blue"></span>
                        Sentiment Score
                    </span>
                </div>
            </div>
            <div ref={chartContainerRef} className="chart" />
        </div>
    );
}

export default Chart;
