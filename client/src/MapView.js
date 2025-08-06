import React from "react";
import { ComposableMap, Geographies, Geography, Marker, Line } from "react-simple-maps";
import { cityCoords } from "./cityCoords";

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

export default function MapView({ dcs, stores, shipments, trucks, highlight, onEntityClick }) {
  const getCoords = (city) => cityCoords[city] || [-98, 39];

  const handleMarkerClick = (entity, entityType, event) => {
    event.stopPropagation();
    if (onEntityClick) {
      onEntityClick({ ...entity, entityType });
    }
  };

  const handleShipmentClick = (shipment, event) => {
    event.stopPropagation();
    if (onEntityClick) {
      onEntityClick({ ...shipment, entityType: 'Shipment' });
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

        {/* Shipment Routes - Clickable */}
        {shipments && shipments.map((shipment, i) => {
          const originCoords = getCoords(shipment.origin);
          const destCoords = getCoords(shipment.destination);
          
          return (
            <Line
              key={`shipment-${i}`}
              from={originCoords}
              to={destCoords}
              stroke={highlight?.shipment_id === shipment.shipment_id ? "#f87171" : "#10b981"}
              strokeWidth={highlight?.shipment_id === shipment.shipment_id ? 5 : 4}
              strokeDasharray={shipment.status === "Delayed" ? "10,5" : "none"}
              opacity={0.8}
              style={{ cursor: 'pointer' }}
              onClick={(event) => handleShipmentClick(shipment, event)}
            />
          );
        })}

        {/* Distribution Centers - NO TEXT, just clean markers */}
        {dcs && dcs.map((dc, index) => (
          <Marker 
            key={dc.dc_id} 
            coordinates={getCoords(dc.location)}
            onClick={(event) => handleMarkerClick(dc, 'DistributionCenter', event)}
            style={{ cursor: 'pointer' }}
          >
            <g style={{ pointerEvents: 'all' }}>
              <circle 
                r={20} 
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              <rect
                x={-12}
                y={-12}
                width={24}
                height={24}
                fill={highlight?.dc_id === dc.dc_id ? "#f59e0b" : "#2563eb"}
                stroke="#fff"
                strokeWidth={3}
                style={{ cursor: 'pointer' }}
              />
              <text 
                textAnchor="middle" 
                y={4} 
                style={{ 
                  fontSize: 10, 
                  fontWeight: 'bold',
                  fill: '#ffffff',
                  pointerEvents: 'none'
                }}
              >
                DC
              </text>
            </g>
          </Marker>
        ))}

        {/* Stores - NO TEXT, just clean markers */}
        {stores && stores.map((store, index) => (
          <Marker 
            key={store.store_id} 
            coordinates={getCoords(store.location)}
            onClick={(event) => handleMarkerClick(store, 'Store', event)}
            style={{ cursor: 'pointer' }}
          >
            <g style={{ pointerEvents: 'all' }}>
              <circle 
                r={15} 
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              <circle 
                r={10} 
                fill={highlight?.store_id === store.store_id ? "#10b981" : "#34d399"} 
                stroke="#fff" 
                strokeWidth={2}
                style={{ cursor: 'pointer' }}
              />
              <text 
                textAnchor="middle" 
                y={3} 
                style={{ 
                  fontSize: 12,
                  pointerEvents: 'none'
                }}
              >
                {store.store_type === 'urban' ? '🏪' : '🏬'}
              </text>
            </g>
          </Marker>
        ))}

        {/* Trucks - Clean markers */}
        {trucks && trucks.map((truck, index) => (
          <Marker 
            key={truck.truck_id} 
            coordinates={getCoords(truck.current_location)}
            onClick={(event) => handleMarkerClick(truck, 'Truck', event)}
            style={{ cursor: 'pointer' }}
          >
            <g style={{ pointerEvents: 'all' }}>
              <circle 
                r={12} 
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              <polygon
                points="0,-10 10,0 0,10 -10,0"
                fill={getTruckColor(truck.status, highlight?.truck_id === truck.truck_id)}
                stroke="#fff"
                strokeWidth={2}
                style={{ cursor: 'pointer' }}
              />
              <text 
                textAnchor="middle" 
                y={3} 
                style={{ 
                  fontSize: 8,
                  fill: '#fff',
                  fontWeight: 'bold',
                  pointerEvents: 'none'
                }}
              >
                T
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
        fontSize: '11px',
        minWidth: '240px'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>Supply Chain Entities</div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '20px', height: '20px', backgroundColor: '#2563eb', marginRight: '8px' }}></div>
          Distribution Centers (Click for Details)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '16px', height: '16px', backgroundColor: '#34d399', borderRadius: '50%', marginRight: '8px' }}></div>
          Stores (Click for Details)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '16px', height: '16px', backgroundColor: '#22c55e', transform: 'rotate(45deg)', marginRight: '8px' }}></div>
          Trucks (Click for Details)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '28px', height: '4px', backgroundColor: '#10b981', marginRight: '8px' }}></div>
          Shipments (Click Lines for Details)
        </div>
        <div style={{ fontSize: '10px', color: '#666', marginTop: '8px' }}>
          Total: {(dcs?.length || 0)} DCs, {(stores?.length || 0)} Stores, {(trucks?.length || 0)} Trucks
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
          minWidth: '280px',
          maxWidth: '400px'
        }}>
          <div style={{ fontWeight: 'bold', fontSize: '16px', marginBottom: '8px', color: '#2563eb' }}>
            {highlight.entityType}: {highlight.name || highlight.truck_id || highlight.shipment_id}
          </div>
          <div style={{ fontSize: '13px', lineHeight: '1.4' }}>
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
                <div><strong>ID:</strong> {highlight.truck_id}</div>
              </>
            )}
            {highlight.entityType === 'Shipment' && (
              <>
                <div><strong>Carrier:</strong> {highlight.carrier}</div>
                <div><strong>Mode:</strong> {highlight.mode}</div>
                <div><strong>Status:</strong> {highlight.status}</div>
                <div><strong>Origin:</strong> {highlight.origin}</div>
                <div><strong>Destination:</strong> {highlight.destination}</div>
                <div><strong>ETA:</strong> {highlight.eta}</div>
                <div><strong>ID:</strong> {highlight.shipment_id}</div>
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
              fontSize: '18px',
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
