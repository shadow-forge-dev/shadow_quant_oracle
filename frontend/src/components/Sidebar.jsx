import { BarChart3, Activity, Flame, Zap } from 'lucide-react';
import './Sidebar.css';

function Sidebar() {
    return (
        <aside className="sidebar">
            <nav className="sidebar-nav">
                <button className="nav-item active">
                    <BarChart3 size={20} />
                    <span>Overview</span>
                </button>
                <button className="nav-item">
                    <Activity size={20} />
                    <span>Sentiment</span>
                </button>
                <button className="nav-item">
                    <Flame size={20} />
                    <span>Trending</span>
                </button>
                <button className="nav-item">
                    <Zap size={20} />
                    <span>Signals</span>
                </button>
            </nav>
        </aside>
    );
}

export default Sidebar;
