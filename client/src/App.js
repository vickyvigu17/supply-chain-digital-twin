import React, { useState, useEffect } from "react";
import axios from "axios";
import MapView from "./MapView";
import "./index.css";

function App() {
  const [supplyChainData, setSupplyChainData] = useState({
    distribution_centers: [],
    stores: [],
    trucks: [],
    shipments: [],
    events: [],
    weather_alerts: []
  });
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [highlightedEntity, setHighlightedEntity] = useState(null);
  const [activeTab, setActiveTab] = useState("map");
  
  // AI Chat state
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");

  // Use production URL for deployment
  const apiUrl = window.location.hostname === "localhost" 
    ? "http://localhost:8000" 
    : "https://supply-chain-digital-twin-1.onrender.com";

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [summaryRes, eventsRes, shipmentsRes, trucksRes, dcsRes, storesRes, weatherRes] = await Promise.all([
          axios.get(`${apiUrl}/api/supply-chain/summary`),
          axios.get(`${apiUrl}/api/supply-chain/event`),
          axios.get(`${apiUrl}/api/supply-chain/shipment`),
          axios.get(`${apiUrl}/api/supply-chain/truck`),
          axios.get(`${apiUrl}/api/supply-chain/distributioncenter`),
          axios.get(`${apiUrl}/api/supply-chain/store`),
          axios.get(`${apiUrl}/api/supply-chain/weatheralert`)
        ]);
        
        setSummary(summaryRes.data);
        setSupplyChainData({
          events: eventsRes.data,
          shipments: shipmentsRes.data,
          trucks: trucksRes.data,
          distribution_centers: dcsRes.data,
          stores: storesRes.data,
          weather_alerts: weatherRes.data
        });
      } catch (err) {
        console.error("Error fetching data:", err);
      }
      setLoading(false);
    };
    fetchData();
  }, [apiUrl]);

  // AI Chat functions
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    try {
      const response = await axios.post(`${apiUrl}/api/chat/messages`, {
        role: "user",
        content: inputMessage,
        userId: "user123"
      });
      
      if (response.data.success) {
        // Fetch updated messages
        const messagesResponse = await axios.get(`${apiUrl}/api/chat/messages`);
        setChatMessages(messagesResponse.data);
        setInputMessage("");
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const getFilteredData = () => {
    switch (selectedFilter) {
      case "issues":
        return {
          stores: supplyChainData.stores.filter(store => 
            supplyChainData.events.some(event => event.impacted_entity.includes(store.store_id))
          ),
          distribution_centers: supplyChainData.distribution_centers.filter(dc => 
            supplyChainData.events.some(event => event.impacted_entity.includes(dc.dc_id))
          ),
          trucks: supplyChainData.trucks.filter(truck => 
            truck.status === "Delayed" || 
            supplyChainData.events.some(event => event.impacted_entity.includes(truck.truck_id))
          ),
          shipments: supplyChainData.shipments.filter(sh => 
            sh.status === "Delayed" || sh.status === "Processing"
          )
        };
      case "active_shipments":
        const activeShipments = supplyChainData.shipments.filter(sh => 
          sh.status === "In Transit" || sh.status === "Processing"
        );
        return {
          stores: supplyChainData.stores,
          distribution_centers: supplyChainData.distribution_centers,
          trucks: supplyChainData.trucks.filter(truck => 
            truck.status === "In Transit" || truck.status === "Loading"
          ),
          shipments: activeShipments
        };
      case "weather_impacted":
        const weatherRegions = supplyChainData.weather_alerts.map(alert => alert.region);
        return {
          stores: supplyChainData.stores.filter(store => 
            weatherRegions.includes(store.region)
          ),
          distribution_centers: supplyChainData.distribution_centers.filter(dc => 
            weatherRegions.includes(dc.region)
          ),
          trucks: supplyChainData.trucks.filter(truck => 
            weatherRegions.includes(truck.current_location)
          ),
          shipments: supplyChainData.shipments.filter(sh => 
            weatherRegions.includes(sh.origin) || weatherRegions.includes(sh.destination)
          )
        };
      default:
        return {
          stores: supplyChainData.stores,
          distribution_centers: supplyChainData.distribution_centers,
          trucks: supplyChainData.trucks,
          shipments: supplyChainData.shipments
        };
    }
  };

  const handleEntityClick = (entity) => {
    setHighlightedEntity(entity);
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading Supply Chain Data...</p>
        </div>
      </div>
    );
  }

  const filteredData = getFilteredData();

  return (
    <div className="container">
      <div className="header">
        <h1>🏭 Supply Chain Digital Twin</h1>
        <p>Ontology-Based Graph Model for Retail Supply Chain Management</p>
      </div>

      <div className="summary-cards">
        <div className="summary-card">
          <div className="icon blue">
            <i className="fas fa-warehouse"></i>
          </div>
          <div className="number">{summary.distribution_centers || 0}</div>
          <div className="label">Distribution Centers</div>
        </div>
        <div className="summary-card">
          <div className="icon green">
            <i className="fas fa-store"></i>
          </div>
          <div className="number">{summary.stores || 0}</div>
          <div className="label">Active Stores</div>
        </div>
        <div className="summary-card">
          <div className="icon orange">
            <i className="fas fa-truck"></i>
          </div>
          <div className="number">{summary.trucks || 0}</div>
          <div className="label">Active Trucks</div>
        </div>
        <div className="summary-card">
          <div className="icon red">
            <i className="fas fa-exclamation-triangle"></i>
          </div>
          <div className="number">{supplyChainData.events.filter(e => e.resolution_status === "Open").length}</div>
          <div className="label">Active Issues</div>
        </div>
      </div>

      <div className="controls">
        <select 
          className="filter-select"
          value={selectedFilter} 
          onChange={(e) => setSelectedFilter(e.target.value)}
        >
          <option value="all">All Entities</option>
          <option value="issues">Issues & Delays</option>
          <option value="active_shipments">Active Shipments</option>
          <option value="weather_impacted">Weather Impacted</option>
        </select>
        <button className="refresh-btn" onClick={() => window.location.reload()}>
          <i className="fas fa-sync-alt"></i>
          Refresh
        </button>
      </div>

      <div className="main-content">
        <div className="map-section">
          <h3>🏭 Supply Chain Network Map</h3>
          <div className="map-container">
            <MapView 
              dcs={filteredData.distribution_centers}
              stores={filteredData.stores}
              shipments={filteredData.shipments}
              trucks={filteredData.trucks}
              highlight={highlightedEntity}
              onEntityClick={handleEntityClick}
            />
          </div>
        </div>

        <div className="data-section">
          <h3>📊 Data Tables</h3>
          <div className="tabs">
            <button 
              className={`tab ${activeTab === 'map' ? 'active' : ''}`}
              onClick={() => handleTabChange('map')}
            >
              Map View
            </button>
            <button 
              className={`tab ${activeTab === 'shipments' ? 'active' : ''}`}
              onClick={() => handleTabChange('shipments')}
            >
              Shipments
            </button>
            <button 
              className={`tab ${activeTab === 'trucks' ? 'active' : ''}`}
              onClick={() => handleTabChange('trucks')}
            >
              Fleet
            </button>
            <button 
              className={`tab ${activeTab === 'events' ? 'active' : ''}`}
              onClick={() => handleTabChange('events')}
            >
              Events
            </button>
            <button 
              className={`tab ${activeTab === 'weather' ? 'active' : ''}`}
              onClick={() => handleTabChange('weather')}
            >
              Weather
            </button>
          </div>

          <div className={`tab-content ${activeTab === 'shipments' ? 'active' : ''}`}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Shipment ID</th>
                  <th>Status</th>
                  <th>Route</th>
                  <th>Carrier</th>
                  <th>ETA</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.shipments.map((shipment) => (
                  <tr key={shipment.shipment_id}>
                    <td>{shipment.shipment_id}</td>
                    <td>
                      <span className={`status-badge status-${shipment.status.toLowerCase().replace(' ', '-')}`}>
                        {shipment.status}
                      </span>
                    </td>
                    <td>{shipment.origin} → {shipment.destination}</td>
                    <td>{shipment.carrier}</td>
                    <td>{shipment.eta}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={`tab-content ${activeTab === 'trucks' ? 'active' : ''}`}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Truck ID</th>
                  <th>Carrier</th>
                  <th>Status</th>
                  <th>Current Location</th>
                  <th>Route</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.trucks.map((truck) => (
                  <tr key={truck.truck_id}>
                    <td>{truck.truck_id}</td>
                    <td>{truck.carrier}</td>
                    <td>
                      <span className={`status-badge status-${truck.status.toLowerCase().replace(' ', '-')}`}>
                        {truck.status}
                      </span>
                    </td>
                    <td>{truck.current_location}</td>
                    <td>{truck.route_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={`tab-content ${activeTab === 'events' ? 'active' : ''}`}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Event Type</th>
                  <th>Impacted Entity</th>
                  <th>Route</th>
                  <th>Status</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {supplyChainData.events.map((event) => (
                  <tr key={event.event_id}>
                    <td>{event.event_type}</td>
                    <td>{event.impacted_entity}</td>
                    <td>{event.source} → {event.destination}</td>
                    <td>
                      <span className={`status-badge ${event.resolution_status === 'Open' ? 'status-delayed' : 'status-operational'}`}>
                        {event.resolution_status}
                      </span>
                    </td>
                    <td>{event.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={`tab-content ${activeTab === 'weather' ? 'active' : ''}`}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Alert Type</th>
                  <th>Region</th>
                  <th>Severity</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {supplyChainData.weather_alerts.map((alert) => (
                  <tr key={alert.alert_id}>
                    <td>{alert.alert_type}</td>
                    <td>{alert.region}</td>
                    <td>
                      <span className={`status-badge severity-${alert.severity.toLowerCase()}`}>
                        {alert.severity}
                      </span>
                    </td>
                    <td>{alert.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {highlightedEntity && (
        <div className="entity-details">
          <h4>Entity Details</h4>
          <div className="detail-row">
            <span className="detail-label">Type:</span>
            <span className="detail-value">{highlightedEntity.entityType}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">ID:</span>
            <span className="detail-value">{highlightedEntity[Object.keys(highlightedEntity)[0]]}</span>
          </div>
          {highlightedEntity.status && (
            <div className="detail-row">
              <span className="detail-label">Status:</span>
              <span className="detail-value">{highlightedEntity.status}</span>
            </div>
          )}
          {highlightedEntity.location && (
            <div className="detail-row">
              <span className="detail-label">Location:</span>
              <span className="detail-value">{highlightedEntity.location}</span>
            </div>
          )}
        </div>
      )}

      {/* AI Chat Widget */}
      <div className="ai-chat-widget">
        <button 
          className="chat-toggle-btn"
          onClick={() => setIsChatOpen(!isChatOpen)}
        >
          🤖 AI Assistant
        </button>
        
        {isChatOpen && (
          <div className="chat-container">
            <div className="chat-header">
              <h3>AI Supply Chain Assistant</h3>
              <button onClick={() => setIsChatOpen(false)}>✕</button>
            </div>
            
            <div className="chat-messages">
              {chatMessages.map((msg) => (
                <div key={msg.id} className={`message ${msg.role}`}>
                  <div className="message-content">{msg.content}</div>
                </div>
              ))}
            </div>
            
            <div className="chat-input">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask about delays, weather, fleet..."
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              />
              <button onClick={sendMessage}>Send</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
