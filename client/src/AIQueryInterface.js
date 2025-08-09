import React, { useState } from 'react';

const AIQueryInterface = ({ onClose }) => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentProvider, setCurrentProvider] = useState('huggingface');

  const handleQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/ai/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      
      const data = await response.json();
      
      if (data.error) {
        setResponse(`❌ Error: ${data.error}`);
      } else {
        setResponse(data.response);
      }
    } catch (error) {
      setResponse(`❌ Network error: ${error.message}`);
    }
    setLoading(false);
  };

  const switchProvider = async (provider) => {
    try {
      const response = await fetch('/api/ai/switch-provider', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider })
      });
      
      const data = await response.json();
      if (!data.error) {
        setCurrentProvider(provider);
        setResponse(`🔄 Switched to ${provider.toUpperCase()}`);
      }
    } catch (error) {
      setResponse(`❌ Provider switch failed: ${error.message}`);
    }
  };

  const exampleQueries = [
    "What are the main issues with our shipments?",
    "Which routes are causing the most delays?",
    "How can we optimize our supply chain?",
    "What regions have the most problems?",
    "Show me performance insights"
  ];

  return (
    <div className="ai-query-interface">
      <div className="ai-header">
        <h3>🤖 AI Supply Chain Assistant</h3>
        <button onClick={onClose} className="close-btn">×</button>
      </div>
      
      <div className="ai-provider-switch">
        <label>AI Provider:</label>
        <div className="provider-buttons">
          {['huggingface', 'openai', 'gemini'].map(provider => (
            <button
              key={provider}
              className={`provider-btn ${currentProvider === provider ? 'active' : ''}`}
              onClick={() => switchProvider(provider)}
            >
              {provider.toUpperCase()}
              {provider === 'huggingface' && ' (FREE)'}
            </button>
          ))}
        </div>
      </div>

      <div className="query-section">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything about your supply chain..."
          className="query-input"
          rows={3}
        />
        
        <button 
          onClick={handleQuery} 
          disabled={loading || !query.trim()}
          className="query-btn"
        >
          {loading ? '🔍 Thinking...' : '🔍 Ask AI'}
        </button>
      </div>

      <div className="example-queries">
        <p>💡 Try these examples:</p>
        {exampleQueries.map((example, index) => (
          <button
            key={index}
            className="example-btn"
            onClick={() => setQuery(example)}
          >
            {example}
          </button>
        ))}
      </div>

      {response && (
        <div className="ai-response">
          <h4>🤖 AI Response:</h4>
          <div className="response-content">
            {response}
          </div>
        </div>
      )}
    </div>
  );
};

export default AIQueryInterface;