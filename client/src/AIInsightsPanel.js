import React, { useState, useEffect } from 'react';
import './AIComponents.css';

const AIInsightsPanel = () => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/ai/insights');
      const data = await response.json();
      
      setInsights({
        content: data.insights || data.error || 'No insights available',
        provider: data.provider,
        model: data.model,
        success: data.success,
        timestamp: data.timestamp
      });
      setLastUpdated(new Date().toLocaleTimeString());
      
    } catch (error) {
      setInsights({
        content: `Error loading insights: ${error.message}`,
        provider: 'Error',
        model: 'Error',
        success: false,
        timestamp: new Date().toISOString()
      });
    }
    setLoading(false);
  };

  useEffect(() => {
    // Load insights on component mount
    fetchInsights();
    
    // Auto-refresh every 5 minutes if enabled
    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchInsights, 5 * 60 * 1000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const formatInsights = (content) => {
    if (!content) return [];
    
    // Split by lines and filter out empty ones
    const lines = content.split('\n').filter(line => line.trim());
    
    return lines.map((line, index) => {
      // Detect insight type by emoji or content
      let type = 'neutral';
      if (line.includes('⚠️') || line.includes('🔴') || line.toLowerCase().includes('delayed') || line.toLowerCase().includes('issue')) {
        type = 'warning';
      } else if (line.includes('✅') || line.includes('📊') || line.toLowerCase().includes('stable') || line.toLowerCase().includes('excellent')) {
        type = 'success';
      } else if (line.includes('🌦️') || line.includes('🚛')) {
        type = 'info';
      }
      
      return {
        id: index,
        content: line,
        type: type
      };
    });
  };

  const insightsList = insights ? formatInsights(insights.content) : [];

  return (
    <div className="ai-insights-panel">
      <div className="insights-header">
        <div className="header-left">
          <h3>🧠 AI Insights & Analytics</h3>
          <p>Smart recommendations from your supply chain data</p>
        </div>
        <div className="header-controls">
          <button
            onClick={fetchInsights}
            className="refresh-btn"
            disabled={loading}
          >
            {loading ? '🔄' : '↻'}
          </button>
          <label className="auto-refresh-toggle">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh
          </label>
        </div>
      </div>

      {loading && !insights && (
        <div className="loading-state">
          <div className="loading-spinner">🔍</div>
          <p>Analyzing supply chain data...</p>
        </div>
      )}

      {insights && (
        <div className="insights-content">
          <div className="insights-meta">
            <span className="provider-tag">{insights.provider}</span>
            {lastUpdated && <span className="last-updated">Updated: {lastUpdated}</span>}
          </div>

          {insightsList.length > 0 ? (
            <div className="insights-list">
              {insightsList.map((insight) => (
                <div key={insight.id} className={`insight-item ${insight.type}`}>
                  <div className="insight-content">{insight.content}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-insights">
              <p>No specific insights available at the moment.</p>
              <button onClick={fetchInsights} className="retry-btn">
                Try Again
              </button>
            </div>
          )}

          {!insights.success && (
            <div className="insights-error">
              <p>⚠️ Could not generate AI insights. Showing fallback analysis.</p>
            </div>
          )}
        </div>
      )}

      <div className="insights-actions">
        <button 
          onClick={() => window.open('/analytics', '_blank')}
          className="detailed-analytics-btn"
        >
          📊 View Detailed Analytics
        </button>
        <button 
          onClick={fetchInsights}
          className="generate-report-btn"
          disabled={loading}
        >
          📋 Refresh Insights
        </button>
      </div>
    </div>
  );
};

export default AIInsightsPanel;