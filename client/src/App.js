import React, { useEffect, useState } from "react";
import axios from "axios";
import MapView from "./MapView";
import "./index.css";

function App() {
  const [supplyChainData, setSupplyChainData] = useState({
    distribution_centers: [],
    stores: [],
    trucks: [],
    purchase_orders: [],
    shipments: [],
    events: [],
    weather_alerts: [],
    inventory: [],
    returns: [],
    skus: []
  });
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [highlightedEntity, setHighlightedEntity] = useState(null);
  const [activeTab, setActiveTab] = useState("map");

  // Use your deployed backend URL or environment variable
  const apiUrl = process.env.REACT_APP_API_URL || "";

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch all node types
        const nodeTypes = [
          'distribution_centers', 'stores', 'trucks', 'purchase_orders', 
          'shipments', 'events', 'weather_alerts', 'inventory', 'returns', 'skus'
        ];
        
        const responses = await Promise.all([
          ...nodeTypes.map(type => axios.get(`${apiUrl}/api/nodes/${type}`)),
          axios.get(`${apiUrl}/api/summary`)
        ]);
        
        const data = {};
        nodeTypes.forEach((type, index) => {
          data[type] = responses[index].data;
        });
        
        setSupplyChainData(data);
        setSummary(responses[responses.length - 1].data);
      } catch (err) {
        console.error("Error fetching data:", err);
        // Set empty data on error
      }
      setLoading(false);
    };
    fetchData();
  }, [apiUrl]);

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
          )
        };
      case "active_shipments":
        return {
          stores: supplyChainData.stores,
          distribution_centers: supplyChainData.distribution_centers,
          shipments: supplyChainData.shipments.filter(sh => sh.status === "In Transit")
        };
      case "weather_impacted":
        return {
          stores: supplyChainData.stores.filter(store => 
            supplyChainData.weather_alerts.some(alert => alert.region === store.region)
          ),
          distribution_centers: supplyChainData.distribution_centers.filter(dc => 
            supplyChainData.weather_alerts.some(alert => alert.region === dc.region)
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

  const renderSummaryCards = () => (
    <div className="summary-grid">
      <div className="summary-card">
        <h3>Distribution Centers</h3>
        <div className="summary-number">{summary.distribution_centers || 0}</div>
      </div>
      <div className="summary-card">
        <h3>Stores</h3>
        <div className="summary-number">{summary.stores || 0}</div>
      </div>
      <div className="summary-card">
        <h3>Active Trucks</h3>
        <div className="summary-number">{summary.trucks || 0}</div>
      </div>
      <div className="summary-card">
        <h3>Purchase Orders</h3>
        <div className="summary-number">{summary.purchase_orders || 0}</div>
      </div>
      <div className="summary-card">
        <h3>Shipments</h3>
        <div className="summary-number">{summary.shipments || 0}</div>
      </div>
      <div className="summary-card">
        <h3>Active Events</h3>
        <div className="summary-number">{summary.events || 0}</div>
      </div>
    </div>
  );

  const renderDataTable = (data, title) => (
    <div className="data-table-container">
      <h3>{title}</h3>
      <div className="data-table">
        <table>
          <thead>
            <tr>
              {data.length > 0 && Object.keys(data[0]).map(key => (
                <th key={key}>{key.replace('_', ' ').toUpperCase()}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 10).map((item, index) => (
              <tr key={index}>
                {Object.values(item).map((value, i) => (
                  <td key={i}>{typeof value === 'object' ? JSON.stringify(value) : value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {data.length > 10 && (
          <div className="table-footer">
            Showing 10 of {data.length} records
          </div>
        )}
      </div>
    </div>
  );

  const renderEventsPanel = () => (
    <div className="events-panel">
      <h3>Recent Events</h3>
      <div className="events-list">
        {supplyChainData.events.slice(0, 8).map(event => (
          <div key={event.event_id} className={`event-item ${event.resolution_status.toLowerCase().replace(' ', '-')}`}>
            <div className="event-header">
              <span className="event-type">{event.event_type}</span>
              <span className={`event-status ${event.resolution_status.toLowerCase().replace(' ', '-')}`}>
                {event.resolution_status}
              </span>
            </div>
            <div className="event-details">
              <div>Entity: {event.impacted_entity}</div>
              <div>Time: {new Date(event.timestamp).toLocaleString()}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderWeatherPanel = () => (
    <div className="weather-panel">
      <h3>Weather Alerts</h3>
      <div className="weather-list">
        {supplyChainData.weather_alerts.slice(0, 5).map(alert => (
          <div key={alert.alert_id} className={`weather-item severity-${alert.severity.toLowerCase()}`}>
            <div className="weather-header">
              <span className="weather-type">{alert.alert_type}</span>
              <span className={`weather-severity severity-${alert.severity.toLowerCase()}`}>
                {alert.severity}
              </span>
            </div>
            <div className="weather-details">
              <div>Region: {alert.region}</div>
              <div>Date: {alert.date}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <div>Loading Supply Chain Digital Twin...</div>
      </div>
    );
  }

  const filteredData = getFilteredData();

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏭 Supply Chain Digital Twin</h1>
        <p>Ontology-Based Graph Model for Retail Supply Chain Management</p>
      </header>

      <nav className="app-nav">
        <button 
          className={activeTab === "map" ? "nav-button active" : "nav-button"}
          onClick={() => setActiveTab("map")}
        >
          Map View
        </button>
        <button 
          className={activeTab === "data" ? "nav-button active" : "nav-button"}
          onClick={() => setActiveTab("data")}
        >
          Data Tables
        </button>
        <button 
          className={activeTab === "analytics" ? "nav-button active" : "nav-button"}
          onClick={() => setActiveTab("analytics")}
        >
          Analytics
        </button>
      </nav>

      {activeTab === "map" && (
        <div className="map-container">
          <div className="controls-panel">
            <div className="filter-controls">
              <label htmlFor="filter-select">Filter View:</label>
              <select 
                id="filter-select"
                value={selectedFilter} 
                onChange={(e) => setSelectedFilter(e.target.value)}
                className="filter-select"
              >
                <option value="all">All Entities</option>
                <option value="issues">Issues & Delays</option>
                <option value="active_shipments">Active Shipments</option>
                <option value="weather_impacted">Weather Impacted</option>
              </select>
            </div>
          </div>

          <div className="map-and-panels">
            <div className="map-section">
              <MapView 
                dcs={filteredData.distribution_centers || []}
                stores={filteredData.stores || []}
                shipments={filteredData.shipments || []}
                trucks={filteredData.trucks || []}
                highlight={highlightedEntity}
                onEntityClick={setHighlightedEntity}
              />
            </div>
            
            <div className="side-panels">
              {renderEventsPanel()}
              {renderWeatherPanel()}
            </div>
          </div>
        </div>
      )}

      {activeTab === "data" && (
        <div className="data-view">
          {renderSummaryCards()}
          <div className="tables-container">
            {renderDataTable(supplyChainData.distribution_centers, "Distribution Centers")}
            {renderDataTable(supplyChainData.stores, "Stores")}
            {renderDataTable(supplyChainData.trucks, "Trucks")}
            {renderDataTable(supplyChainData.purchase_orders, "Purchase Orders")}
            {renderDataTable(supplyChainData.shipments, "Shipments")}
          </div>
        </div>
      )}

      {activeTab === "analytics" && (
        <div className="analytics-view">
          {renderSummaryCards()}
          <div className="analytics-panels">
            <div className="analytics-section">
              <h3>Supply Chain Health</h3>
              <div className="health-metrics">
                <div className="metric">
                  <label>On-Time Delivery Rate</label>
                  <div className="metric-value">
                    {(100 - (supplyChainData.events.filter(e => e.event_type === "Delay").length / supplyChainData.shipments.length * 100)).toFixed(1)}%
                  </div>
                </div>
                <div className="metric">
                  <label>Active Issues</label>
                  <div className="metric-value">
                    {supplyChainData.events.filter(e => e.resolution_status !== "Resolved").length}
                  </div>
                </div>
                <div className="metric">
                  <label>Weather Alerts</label>
                  <div className="metric-value">
                    {supplyChainData.weather_alerts.filter(w => w.severity === "High" || w.severity === "Critical").length}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="analytics-section">
              <h3>Regional Distribution</h3>
              <div className="regional-stats">
                {["Northeast", "South", "Midwest", "West"].map(region => {
                  const regionStores = supplyChainData.stores.filter(s => s.region === region).length;
                  const regionDCs = supplyChainData.distribution_centers.filter(dc => dc.region === region).length;
                  return (
                    <div key={region} className="region-stat">
                      <div className="region-name">{region}</div>
                      <div className="region-data">
                        <span>{regionDCs} DCs</span>
                        <span>{regionStores} Stores</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
