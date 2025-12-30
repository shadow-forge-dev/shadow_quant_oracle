import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './SignalDistribution.css';

function SignalDistribution() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/signal-distribution')
            .then(res => res.json())
            .then(result => {
                const formattedData = result.distribution.map(item => ({
                    name: item.chain_signal,
                    value: item.count
                }));
                setData(formattedData);
            })
            .catch(err => console.error('Error fetching signal distribution:', err));
    }, []);

    const COLORS = {
        'LOW_GAS': '#26a69a',
        'NORMAL': '#2962ff',
        'WHALE_ALERT': '#ef5350',
        'N/A': '#787b86'
    };

    return (
        <div className="signal-distribution">
            <h3>Chain Signal Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#787b86'} />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{
                            background: 'var(--bg-tertiary)',
                            border: '1px solid var(--border-color)',
                            borderRadius: '4px',
                            color: 'var(--text-primary)'
                        }}
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}

export default SignalDistribution;
