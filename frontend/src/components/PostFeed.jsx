import { MessageSquare } from 'lucide-react';
import './PostFeed.css';

function PostFeed({ posts }) {
    const getSentimentColor = (sentiment) => {
        if (sentiment > 0.5) return 'positive';
        if (sentiment < -0.5) return 'negative';
        return 'neutral';
    };

    const getSignalBadge = (signal) => {
        const badges = {
            'LOW_GAS': { text: 'Low Gas', color: 'green' },
            'NORMAL': { text: 'Normal', color: 'blue' },
            'WHALE_ALERT': { text: 'Whale', color: 'red' },
            'N/A': { text: 'N/A', color: 'gray' }
        };
        return badges[signal] || badges['N/A'];
    };

    return (
        <div className="post-feed">
            <div className="feed-header">
                <h3>
                    <MessageSquare size={18} />
                    Live Feed
                </h3>
                <span className="post-count">{posts.length} posts</span>
            </div>
            <div className="feed-list">
                {posts.map((post, index) => {
                    const badge = getSignalBadge(post.chain_signal);
                    return (
                        <div key={post.id || index} className="post-item">
                            <div className="post-header">
                                <span className="post-subreddit">r/{post.subreddit}</span>
                                <span className={`signal-badge ${badge.color}`}>{badge.text}</span>
                            </div>
                            <div className="post-title">{post.title}</div>
                            <div className="post-footer">
                                <span className="post-score">↑ {post.score}</span>
                                <span className={`post-sentiment ${getSentimentColor(post.sentiment)}`}>
                                    Sentiment: {post.sentiment?.toFixed(3)}
                                </span>
                                <span className="post-time">
                                    {new Date(post.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default PostFeed;
