import React from "react";
import { ComposableMap, Geographies, Geography, Marker, Line } from "react-simple-maps";
import { cityCoords } from "./cityCoords";

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

export default function MapView({ dcs, stores, shipments, trucks, highlight, onEntityClick }) {
  // Helper to get coordinates for a city
  const getCoords = (city) => cityCoords[city] || [-98, 39]; // fallback: center of US

  const handleMarkerClick = (entity, entityType) => {
    if (onEntityClick) {
      onEntityClick({ ...entity, entityType });
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      <ComposableMap projection="geoAlbersUsa" width={900} height={500}>
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map(geo => (
              <Geography 
                key={geo.rsmKey} 
                geography={geo} 
                fill="#EAEAEC" 
                stroke="#D6D6DA" 
                strokeWidth={0.5}
              />
            ))
          }
        </Geographies>

        {/* Shipment Routes (draw first so they appear behind markers) */}
        {shipments && shipments.map((shipment, i) => {
          const originCoords = getCoords(shipment.origin);
          const destCoords = getCoords(shipment.destination);
          
          return (
            <Line
              key={`shipment-${i}`}
              from={originCoords}
              to={destCoords}
              stroke={highlight?.shipment_id === shipment.shipment_id ? "#f87171" : "#10b981"}
              strokeWidth={highlight?.shipment_id === shipment.shipment_id ? 3 : 2}
              strokeDasharray={shipment.status === "Delayed" ? "5,5" : "none"}
              opacity={0.7}
            />
          );
        })}

        {/* Distribution Centers */}
        {dcs && dcs.map(dc => (
          <Marker 
            key={dc.dc_id} 
            coordinates={getCoords(dc.location)}
            onClick={() => handleMarkerClick(dc, 'DistributionCenter')}
            style={{ cursor: 'pointer' }}
          >
            <circle 
              r={highlight?.dc_id === dc.dc_id ? 10 : 8} 
              fill={highlight?.dc_id === dc.dc_id ? "#f59e0b" : "#2563eb"} 
              stroke="#fff" 
              strokeWidth={2}
              style={{ cursor: 'pointer' }}
            />
            <text 
              textAnchor="middle" 
              y={-15} 
              style={{ 
                fontSize: highlight?.dc_id === dc.dc_id ? 12 : 10, 
                fontWeight: 600,
                fill: '#333',
                pointerEvents: 'none'
              }}
            >
              {dc.name.replace('Distribution Center ', 'DC ')}
            </text>
          </Marker>
        ))}

        {/* Stores */}
        {stores && stores.map(store => (
          <Marker 
            key={store.store_id} 
            coordinates={getCoords(store.location)}
            onClick={() => handleMarkerClick(store, 'Store')}
            style={{ cursor: 'pointer' }}
          >
            <circle 
              r={highlight?.store_id === store.store_id ? 7 : 5} 
              fill={highlight?.store_id === store.store_id ? "#10b981" : "#34d399"} 
              stroke="#fff" 
              strokeWidth={1.5}
              style={{ cursor: 'pointer' }}
            />
            <text 
              textAnchor="middle" 
              y={-12} 
              style={{ 
                fontSize: highlight?.store_id === store.store_id ? 9 : 8,
                fill: '#333',
                pointerEvents: 'none'
              }}
            >
              {store.store_type === 'urban' ? '🏪' : '🏬'}
            </text>
          </Marker>
        ))}

        {/* Trucks */}
        {trucks && trucks.map(truck => (
          <Marker 
            key={truck.truck_id} 
            coordinates={getCoords(truck.current_location)}
            onClick={() => handleMarkerClick(truck, 'Truck')}
            style={{ cursor: 'pointer' }}
          >
            <g>
              <circle 
                r={highlight?.truck_id === truck.truck_id ? 6 : 4} 
                fill={getTruckColor(truck.status, highlight?.truck_id === truck.truck_id)} 
                stroke="#fff" 
                strokeWidth={1}
                style={{ cursor: 'pointer' }}
              />
              <text 
                textAnchor="middle" 
                y={2} 
                style={{ 
                  fontSize: highlight?.truck_id === truck.truck_id ? 10 : 8,
                  fill: '#fff',
                  fontWeight: 'bold',
                  pointerEvents: 'none'
                }}
              >
                🚛
              </text>
            </g>
          </Marker>
        ))}
      </ComposableMap>

      {/* Legend */}
      <div style={{
        position: 'absolute',
        top: 10,
        right: 10,
        background: 'rgba(255, 255, 255, 0.95)',
        padding: '12px',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        fontSize: '12px',
        minWidth: '200px'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>Legend</div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '12px', backgroundColor: '#2563eb', borderRadius: '50%', marginRight: '8px' }}></div>
          Distribution Centers
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '12px', backgroundColor: '#34d399', borderRadius: '50%', marginRight: '8px' }}></div>
          Stores
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '12px', backgroundColor: '#22c55e', borderRadius: '50%', marginRight: '8px' }}></div>
          Trucks (Active)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '12px', backgroundColor: '#ef4444', borderRadius: '50%', marginRight: '8px' }}></div>
          Trucks (Delayed)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '20px', height: '2px', backgroundColor: '#10b981', marginRight: '8px' }}></div>
          Active Shipments
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ width: '20px', height: '2px', backgroundColor: '#10b981', backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 2px, white 2px, white 4px)', marginRight: '8px' }}></div>
          Delayed Shipments
        </div>
      </div>

      {/* Entity Info Panel */}
      {highlight && (
        <div style={{
          position: 'absolute',
          bottom: 10,
          left: 10,
          background: 'rgba(255, 255, 255, 0.95)',
          padding: '16px',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          minWidth: '250px',
          maxWidth: '350px'
        }}>
          <div style={{ fontWeight: 'bold', fontSize: '14px', marginBottom: '8px' }}>
            {highlight.entityType}: {highlight.name || highlight.truck_id || highlight.shipment_id}
          </div>
          <div style={{ fontSize: '12px', lineHeight: '1.4' }}>
            {highlight.entityType === 'DistributionCenter' && (
              <>
                <div><strong>Location:</strong> {highlight.location}</div>
                <div><strong>Region:</strong> {highlight.region}</div>
                <div><strong>ID:</strong> {highlight.dc_id}</div>
              </>
            )}
            {highlight.entityType === 'Store' && (
              <>
                <div><strong>Location:</strong> {highlight.location}</div>
                <div><strong>Region:</strong> {highlight.region}</div>
                <div><strong>Type:</strong> {highlight.store_type}</div>
                <div><strong>ID:</strong> {highlight.store_id}</div>
              </>
            )}
            {highlight.entityType === 'Truck' && (
              <>
                <div><strong>Carrier:</strong> {highlight.carrier}</div>
                <div><strong>Status:</strong> {highlight.status}</div>
                <div><strong>Location:</strong> {highlight.current_location}</div>
                <div><strong>Route:</strong> {highlight.route_id}</div>
              </>
            )}
          </div>
          <button 
            onClick={() => onEntityClick && onEntityClick(null)}
            style={{
              position: 'absolute',
              top: '8px',
              right: '8px',
              background: 'none',
              border: 'none',
              fontSize: '16px',
              cursor: 'pointer',
              color: '#666'
            }}
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
}

function getTruckColor(status, isHighlighted) {
  if (isHighlighted) return "#f59e0b";
  
  switch (status) {
    case "Delayed":
      return "#ef4444";
    case "In Transit":
      return "#22c55e";
    case "Loading":
      return "#3b82f6";
    case "Delivered":
      return "#6b7280";
    default:
      return "#22c55e";
  }
}
