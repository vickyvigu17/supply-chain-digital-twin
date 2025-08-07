import React, { useState } from "react";
import { ComposableMap, Geographies, Geography, Marker, Line, ZoomableGroup } from "react-simple-maps";
import { cityCoords } from "./cityCoords";

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

export default function MapView({ dcs, stores, shipments, trucks, highlight, onEntityClick }) {
  const [zoom, setZoom] = useState(1);
  const [center, setCenter] = useState([0, 0]);

  // Helper to get coordinates for a city with small offsets to prevent overlap
  const getCoords = (city, id = '', entityType = '') => {
    if (!city) return [-98, 39]; // fallback if city is null/undefined
    const baseCoords = cityCoords[city] || [-98, 39]; // fallback: center of US
    if (!baseCoords || !Array.isArray(baseCoords) || baseCoords.length < 2) {
      return [-98, 39]; // safe fallback
    }
    
    // Add small offsets based on entity type and ID to prevent overlap
    let offsetX = 0, offsetY = 0;
    if (id) {
      const hash = id.split('').reduce((a, b) => { a = ((a << 5) - a) + b.charCodeAt(0); return a & a; }, 0);
      offsetX = (hash % 20 - 10) * 0.1; // -1 to 1 degree offset
      offsetY = ((hash >> 4) % 20 - 10) * 0.1;
      
      // Different offsets for different entity types
      if (entityType === 'DistributionCenter') {
        offsetX += 0.2;
        offsetY += 0.2;
      } else if (entityType === 'Store') {
        offsetX -= 0.2;
        offsetY -= 0.2;
      } else if (entityType === 'Truck') {
        offsetX += 0.3;
        offsetY -= 0.1;
      }
    }
    
    return [
      (baseCoords[0] || -98) + offsetX, 
      (baseCoords[1] || 39) + offsetY
    ];
  };

  const handleMarkerClick = (entity, entityType) => {
    if (onEntityClick) {
      onEntityClick({ ...entity, entityType });
    }
  };

  const handleShipmentClick = (shipment) => {
    if (onEntityClick) {
      onEntityClick({ ...shipment, entityType: 'Shipment' });
    }
  };

  const renderShipmentRoutes = () => {
    if (!shipments) return null;

    return shipments.map((shipment, i) => {
      const originCoords = getCoords(shipment.origin);
      const routes = [];

      // Handle both old (destination) and new (destinations) data formats
      let destinationsList = [];
      if (shipment.destinations && Array.isArray(shipment.destinations)) {
        destinationsList = shipment.destinations;
      } else if (shipment.destination) {
        destinationsList = [shipment.destination];
      }

      destinationsList.forEach((destination, destIndex) => {
        const destCoords = getCoords(destination);
        
        // Determine color based on status
        let strokeColor = "#10b981"; // default green
        if (shipment.status === "Delayed") strokeColor = "#ef4444"; // red
        else if (shipment.status === "Processing") strokeColor = "#f59e0b"; // yellow
        else if (shipment.status === "Delivered") strokeColor = "#6b7280"; // gray
        
        routes.push(
          <Line
            key={`shipment-${i}-dest-${destIndex}`}
            from={originCoords}
            to={destCoords}
            stroke={highlight?.shipment_id === shipment.shipment_id ? "#f87171" : strokeColor}
            strokeWidth={highlight?.shipment_id === shipment.shipment_id ? 3 : 2}
            strokeDasharray={shipment.status === "Delayed" ? "5,5" : "none"}
            opacity={0.7}
            onClick={() => handleShipmentClick(shipment)}
            style={{ cursor: 'pointer' }}
          />
        );
        
        // Add small circles at destination points for multi-stop routes
        if (shipment.route_type === "multi-stop" || destinationsList.length > 1) {
          routes.push(
            <Marker key={`stop-${i}-${destIndex}`} coordinates={destCoords}>
              <circle
                r={2}
                fill={strokeColor}
                stroke="#fff"
                strokeWidth={1}
                opacity={0.8}
              />
            </Marker>
          );
        }
      });

      return routes;
    });
  };

  const handleZoomIn = () => {
    setZoom(Math.min(zoom * 1.5, 8));
  };

  const handleZoomOut = () => {
    setZoom(Math.max(zoom / 1.5, 1));
  };

  const handleReset = () => {
    setZoom(1);
    setCenter([0, 0]);
  };



  return (
    <div style={{ position: 'relative' }}>
      <ComposableMap projection="geoAlbersUsa" width={900} height={500}>
        <ZoomableGroup zoom={zoom} center={center}>
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
          {renderShipmentRoutes()}

          {/* Distribution Centers */}
          {dcs && dcs.map(dc => (
            <Marker 
              key={dc.dc_id} 
              coordinates={getCoords(dc.location, dc.dc_id, 'DistributionCenter')}
            >
              <g
                onClick={() => handleMarkerClick(dc, 'DistributionCenter')}
                style={{ cursor: 'pointer' }}
              >
                {/* Larger transparent click area */}
                <circle 
                  r={15} 
                  fill="transparent"
                  style={{ cursor: 'pointer' }}
                />
                {/* Visible marker - Square for DCs */}
                <rect
                  x={-6}
                  y={-6}
                  width={12}
                  height={12}
                  fill={highlight?.dc_id === dc.dc_id ? "#f59e0b" : "#2563eb"} 
                  stroke="#fff" 
                  strokeWidth={2}
                  style={{ cursor: 'pointer' }}
                />
              </g>
            </Marker>
          ))}

          {/* Stores */}
          {stores && stores.map(store => (
            <Marker 
              key={store.store_id} 
              coordinates={getCoords(store.location, store.store_id, 'Store')}
            >
              <g
                onClick={() => handleMarkerClick(store, 'Store')}
                style={{ cursor: 'pointer' }}
              >
                {/* Larger transparent click area */}
                <circle 
                  r={12} 
                  fill="transparent"
                  style={{ cursor: 'pointer' }}
                />
                {/* Visible marker - Circle for Stores */}
                <circle 
                  r={5} 
                  fill={highlight?.store_id === store.store_id ? "#10b981" : "#34d399"} 
                  stroke="#fff" 
                  strokeWidth={1.5}
                  style={{ cursor: 'pointer' }}
                />
              </g>
            </Marker>
          ))}

          {/* Trucks */}
          {trucks && trucks.map(truck => (
            <Marker 
              key={truck.truck_id} 
              coordinates={getCoords(truck.current_location, truck.truck_id, 'Truck')}
            >
              <g
                onClick={() => handleMarkerClick(truck, 'Truck')}
                style={{ cursor: 'pointer' }}
              >
                {/* Larger transparent click area */}
                <circle 
                  r={10} 
                  fill="transparent"
                  style={{ cursor: 'pointer' }}
                />
                {/* Visible marker - Diamond for Trucks */}
                <polygon
                  points="0,-4 4,0 0,4 -4,0"
                  fill={getTruckColor(truck.status, highlight?.truck_id === truck.truck_id)} 
                  stroke="#fff" 
                  strokeWidth={1}
                  style={{ cursor: 'pointer' }}
                />
              </g>
            </Marker>
          ))}
        </ZoomableGroup>
      </ComposableMap>

      {/* Zoom Controls */}
      <div style={{
        position: 'absolute',
        top: 10,
        left: 10,
        display: 'flex',
        flexDirection: 'column',
        gap: '5px'
      }}>
        <button 
          onClick={handleZoomIn}
          style={{
            width: '30px',
            height: '30px',
            background: 'rgba(255, 255, 255, 0.9)',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          +
        </button>
        <button 
          onClick={handleZoomOut}
          style={{
            width: '30px',
            height: '30px',
            background: 'rgba(255, 255, 255, 0.9)',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          -
        </button>
        <button 
          onClick={handleReset}
          style={{
            width: '30px',
            height: '30px',
            background: 'rgba(255, 255, 255, 0.9)',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          ⌂
        </button>
      </div>

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
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
          Legend (Zoom: {typeof zoom === 'number' ? zoom.toFixed(1) : '1.0'}x)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '12px', backgroundColor: '#2563eb', marginRight: '8px' }}></div>
          Distribution Centers
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '12px', backgroundColor: '#34d399', borderRadius: '50%', marginRight: '8px' }}></div>
          Stores
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <div style={{ width: '12px', height: '6px', backgroundColor: '#22c55e', transform: 'rotate(45deg)', marginRight: '8px' }}></div>
          Trucks
        </div>
        <div style={{ marginTop: '8px', fontWeight: 'bold', fontSize: '11px' }}>Shipment Routes:</div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2px' }}>
          <div style={{ width: '20px', height: '2px', backgroundColor: '#10b981', marginRight: '8px' }}></div>
          Active ({shipments?.filter(s => s.status === "In Transit").length || 0})
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2px' }}>
          <div style={{ width: '20px', height: '2px', backgroundColor: '#ef4444', borderStyle: 'dashed', borderWidth: '1px 0', marginRight: '8px' }}></div>
          Delayed ({shipments?.filter(s => s.status === "Delayed").length || 0})
        </div>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2px' }}>
          <div style={{ width: '20px', height: '2px', backgroundColor: '#f59e0b', marginRight: '8px' }}></div>
          Processing ({shipments?.filter(s => s.status === "Processing").length || 0})
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ width: '20px', height: '2px', backgroundColor: '#6b7280', marginRight: '8px' }}></div>
          Delivered ({shipments?.filter(s => s.status === "Delivered").length || 0})
        </div>
        <div style={{ marginTop: '6px', fontSize: '10px', color: '#666' }}>
          Total Shipments: {shipments?.length || 0}
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
          maxWidth: '400px'
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
            {highlight.entityType === 'Shipment' && (
              <>
                <div><strong>Carrier:</strong> {highlight.carrier}</div>
                <div><strong>Status:</strong> {highlight.status}</div>
                <div><strong>Mode:</strong> {highlight.mode}</div>
                <div><strong>ETA:</strong> {highlight.eta}</div>
                <div><strong>Origin:</strong> {highlight.origin}</div>
                {highlight.route_type && <div><strong>Route Type:</strong> {highlight.route_type}</div>}
                {highlight.stops_count && <div><strong>Stops:</strong> {highlight.stops_count}</div>}
                {(highlight.destinations || highlight.destination) && (
                  <div style={{ marginTop: '8px' }}>
                    <strong>Destination{highlight.destinations && highlight.destinations.length > 1 ? 's' : ''}:</strong>
                    <div style={{ marginLeft: '8px', fontSize: '11px' }}>
                      {highlight.destinations ? 
                        highlight.destinations.map((dest, i) => (
                          <div key={i}>• {dest}</div>
                        )) :
                        <div>• {highlight.destination}</div>
                      }
                    </div>
                  </div>
                )}
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
