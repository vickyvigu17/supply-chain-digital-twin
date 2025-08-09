import React, { useState } from 'react';
import './AIComponents.css';

const AIQueryInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const sampleQueries = [
    "How many shipments are delayed?",
    "Show me trucks in the West region",
    "What stores have issues?", 
    "Which areas have weather alerts?",
    "Show shipments going to Chicago"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/ai/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim() })
      });

      const data = await response.json();
      
      const newEntry = {
        query: query.trim(),
        response: data.response || data.error || 'No response received',
        success: data.success,
        provider: data.provider,
        timestamp: new Date().toLocaleTimeString()
      };

      setResponse(newEntry);
      setHistory(prev => [newEntry, ...prev.slice(0, 4)]); // Keep last 5
      setQuery('');
      
    } catch (error) {
      const errorEntry = {
        query: query.trim(),
        response: `Error: ${error.message}`,
        success: false,
        provider: 'Error',
        timestamp: new Date().toLocaleTimeString()
      };
      setResponse(errorEntry);
      setHistory(prev => [errorEntry, ...prev.slice(0, 4)]);
    }
    
    setLoading(false);
  };

  const handleSampleQuery = (sampleQuery) => {
    setQuery(sampleQuery);
  };

  return (
    <div className="ai-query-interface">
      <div className="ai-header">
        <h3>🤖 AI Supply Chain Assistant</h3>
        <p>Ask natural language questions about your supply chain data</p>
      </div>

      <form onSubmit={handleSubmit} className="query-form">
        <div className="query-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask me anything about your supply chain..."
            className="query-input"
            disabled={loading}
          />
          <button 
            type="submit" 
            className="query-button"
            disabled={loading || !query.trim()}
          >
            {loading ? '🔍' : '🚀'}
          </button>
        </div>
      </form>

      <div className="sample-queries">
        <span className="sample-label">Try these:</span>
        {sampleQueries.map((sample, index) => (
          <button
            key={index}
            onClick={() => handleSampleQuery(sample)}
            className="sample-query-btn"
            disabled={loading}
          >
            {sample}
          </button>
        ))}
      </div>

      {response && (
        <div className={`ai-response ${response.success ? 'success' : 'error'}`}>
          <div className="response-header">
            <strong>Q:</strong> {response.query}
            <span className="response-meta">
              {response.provider} • {response.timestamp}
            </span>
          </div>
          <div className="response-content">
            <strong>A:</strong> {response.response}
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div className="query-history">
          <h4>Recent Queries</h4>
          {history.map((entry, index) => (
            <div key={index} className={`history-item ${entry.success ? 'success' : 'error'}`}>
              <div className="history-query">{entry.query}</div>
              <div className="history-response">{entry.response}</div>
              <div className="history-meta">{entry.provider} • {entry.timestamp}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AIQueryInterface;