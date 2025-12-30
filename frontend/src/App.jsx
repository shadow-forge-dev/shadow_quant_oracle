import { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Chart from './components/Chart';
import MetricsPanel from './components/MetricsPanel';
import PostFeed from './components/PostFeed';
import SignalDistribution from './components/SignalDistribution';
import './App.css';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [posts, setPosts] = useState([]);
  const [timelineData, setTimelineData] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [metricsRes, postsRes, timelineRes] = await Promise.all([
        fetch('http://localhost:8000/api/metrics'),
        fetch('http://localhost:8000/api/posts?limit=50'),
        fetch('http://localhost:8000/api/sentiment-timeline?limit=100')
      ]);

      const metricsData = await metricsRes.json();
      const postsData = await postsRes.json();
      const timelineDataRes = await timelineRes.json();

      setMetrics(metricsData);
      setPosts(postsData.posts);
      setTimelineData(timelineDataRes.timeline);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading Quant Oracle...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Header metrics={metrics} onRefresh={fetchData} />
      <div className="app-content">
        <Sidebar />
        <div className="main-content">
          <MetricsPanel metrics={metrics} />
          <div className="charts-grid">
            <div className="chart-container">
              <Chart data={timelineData} />
            </div>
            <div className="signal-container">
              <SignalDistribution />
            </div>
          </div>
          <PostFeed posts={posts} />
        </div>
      </div>
    </div>
  );
}

export default App;
