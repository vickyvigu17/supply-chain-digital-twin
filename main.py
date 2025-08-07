from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import random
import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data generation for supply chain digital twin
@dataclass
class DistributionCenter:
    dc_id: str
    name: str
    location: str
    region: str
    type: str = "DistributionCenter"

@dataclass
class Store:
    store_id: str
    name: str
    location: str
    region: str
    store_type: str  # urban/rural
    type: str = "Store"

@dataclass
class SKU:
    sku_id: str
    name: str
    category: str
    unit: str
    temperature_zone: str
    type: str = "SKU"

@dataclass
class Truck:
    truck_id: str
    carrier: str
    route_id: str
    status: str
    current_location: str
    type: str = "Truck"

@dataclass
class PurchaseOrder:
    po_id: str
    date: str
    status: str
    delivery_window_start: str
    delivery_window_end: str
    store_id: str
    type: str = "PurchaseOrder"

@dataclass
class Shipment:
    shipment_id: str
    carrier: str
    mode: str
    status: str
    eta: str
    origin: str
    destinations: List[str]
    route_type: str
    stops_count: int
    type: str = "Shipment"

@dataclass
class InventorySnapshot:
    snapshot_id: str
    sku_id: str
    quantity_on_hand: int
    store_id: str
    timestamp: str
    type: str = "InventorySnapshot"

@dataclass
class Return:
    return_id: str
    reason: str
    date: str
    condition: str
    quantity: int
    store_id: str
    sku_id: str
    type: str = "Return"

@dataclass
class WeatherAlert:
    alert_id: str
    alert_type: str
    region: str
    severity: str
    date: str
    type: str = "WeatherAlert"

@dataclass
class Event:
    event_id: str
    event_type: str
    impacted_entity: str
    timestamp: str
    resolution_status: str
    type: str = "Event"

# Generate sample data
def generate_sample_data():
    # Cities and regions for realistic locations
    cities = [
        ("Cincinnati, OH", "Midwest"), ("Dallas, TX", "South"), ("Atlanta, GA", "South"),
        ("Denver, CO", "West"), ("Chicago, IL", "Midwest"), ("Phoenix, AZ", "West"),
        ("Seattle, WA", "West"), ("Orlando, FL", "South"), ("Nashville, TN", "South"),
        ("Salt Lake City, UT", "West"), ("Boston, MA", "Northeast"), ("Detroit, MI", "Midwest"),
        ("Houston, TX", "South"), ("Los Angeles, CA", "West"), ("New York, NY", "Northeast"),
        ("Philadelphia, PA", "Northeast"), ("San Francisco, CA", "West"), ("Miami, FL", "South"),
        ("Portland, OR", "West"), ("Minneapolis, MN", "Midwest")
    ]
    
    # Generate Distribution Centers (16)
    dcs = []
    for i in range(16):
        city, region = random.choice(cities)
        dcs.append(DistributionCenter(
            dc_id=f"DC{i+1:03d}",
            name=f"Distribution Center {city.split(',')[0]}",
            location=city,
            region=region
        ))
    
    # Generate Stores (200)
    stores = []
    store_types = ["urban", "rural"]
    for i in range(200):
        city, region = random.choice(cities)
        stores.append(Store(
            store_id=f"ST{i+1:03d}",
            name=f"Store {i+1} {city.split(',')[0]}",
            location=city,
            region=region,
            store_type=random.choice(store_types)
        ))
    
    # Generate SKUs (500)
    skus = []
    categories = ["Electronics", "Groceries", "Clothing", "Home & Garden", "Automotive", "Health & Beauty"]
    units = ["each", "lb", "oz", "gallon", "pack", "case"]
    temp_zones = ["Frozen", "Ambient", "Fragile", "Refrigerated"]
    
    for i in range(500):
        category = random.choice(categories)
        skus.append(SKU(
            sku_id=f"SKU{i+1:04d}",
            name=f"{category} Item {i+1}",
            category=category,
            unit=random.choice(units),
            temperature_zone=random.choice(temp_zones)
        ))
    
    # Generate Trucks (40)
    trucks = []
    carriers = ["FedEx", "UPS", "DHL", "USPS", "Kroger Logistics", "Tractor Supply Fleet"]
    statuses = ["In Transit", "Delayed", "Loading", "Delivered", "Available"]
    
    for i in range(40):
        truck_city, _ = random.choice(cities)
        trucks.append(Truck(
            truck_id=f"TRK{i+1:03d}",
            carrier=random.choice(carriers),
            route_id=f"RT{i+1:03d}",
            status=random.choice(statuses),
            current_location=truck_city
        ))
    
    # Generate Purchase Orders (60)
    pos = []
    po_statuses = ["Open", "In Progress", "Delivered", "Cancelled"]
    
    for i in range(60):
        start_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(-30, 30))
        end_date = start_date + datetime.timedelta(days=random.randint(1, 7))
        
        pos.append(PurchaseOrder(
            po_id=f"PO{i+1:04d}",
            date=start_date.strftime("%Y-%m-%d"),
            status=random.choice(po_statuses),
            delivery_window_start=start_date.strftime("%Y-%m-%d"),
            delivery_window_end=end_date.strftime("%Y-%m-%d"),
            store_id=random.choice(stores).store_id
        ))
    
    # Generate Shipments (45) - Multi-stop deliveries (no milk runs)
    shipments = []
    modes = ["FTL", "LTL", "Parcel", "Express"]
    shipment_statuses = ["In Transit", "Delivered", "Delayed", "Processing"]
    route_types = ["single", "multi-stop"]
    
    for i in range(45):
        origin_dc = random.choice(dcs)
        
        route_type = random.choices(
            route_types, 
            weights=[40, 60],
            k=1
        )[0]
        
        if route_type == "single":
            stops_count = 1
            # Choose stores from same region to be more realistic
            region_stores = [s for s in stores if s.region == origin_dc.region]
            if region_stores:
                destinations = [random.choice(region_stores).location]
            else:
                destinations = [random.choice(stores).location]
        else:  # multi-stop (2-3 stops max to reduce congestion)
            stops_count = random.randint(2, 3)
            region_stores = [s for s in stores if s.region == origin_dc.region]
            if len(region_stores) >= stops_count:
                selected_stores = random.sample(region_stores, stops_count)
            else:
                selected_stores = random.sample(stores, min(stops_count, len(stores)))
            destinations = [s.location for s in selected_stores]
        
        # Better status distribution
        if i < 15:
            status = "In Transit"
        elif i < 25:
            status = "Delayed" 
        elif i < 32:
            status = "Processing"
        else:
            status = "Delivered"
            
        eta = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 5))
        
        shipments.append(Shipment(
            shipment_id=f"SH{i+1:04d}",
            carrier=random.choice(carriers),
            mode=random.choice(modes),
            status=status,
            eta=eta.strftime("%Y-%m-%d"),
            origin=origin_dc.location,
            destinations=destinations,
            route_type=route_type,
            stops_count=stops_count
        ))
    
    # Generate Inventory Snapshots (12)
    inventory = []
    for i in range(12):
        inventory.append(InventorySnapshot(
            snapshot_id=f"INV{i+1:03d}",
            sku_id=random.choice(skus).sku_id,
            quantity_on_hand=random.randint(0, 1000),
            store_id=random.choice(stores).store_id,
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    # Generate Returns (15)
    returns = []
    return_reasons = ["Damaged", "Wrong Item", "Customer Return", "Expired", "Quality Issue"]
    conditions = ["Damaged", "Good", "Resellable", "Dispose"]
    
    for i in range(15):
        returns.append(Return(
            return_id=f"RET{i+1:03d}",
            reason=random.choice(return_reasons),
            date=(datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            condition=random.choice(conditions),
            quantity=random.randint(1, 50),
            store_id=random.choice(stores).store_id,
            sku_id=random.choice(skus).sku_id
        ))
    
    # Generate Weather Alerts (10)
    weather_alerts = []
    alert_types = ["Storm", "Heatwave", "Flood", "Snow", "Hurricane"]
    severities = ["Low", "Medium", "High", "Critical"]
    regions = list(set([region for _, region in cities]))
    
    for i in range(10):
        weather_alerts.append(WeatherAlert(
            alert_id=f"WA{i+1:03d}",
            alert_type=random.choice(alert_types),
            region=random.choice(regions),
            severity=random.choice(severities),
            date=(datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        ))
    
    # Generate Events (11)
    events = []
    event_types = ["Delay", "Shortage", "Rejection", "Route Change", "Equipment Failure"]
    resolution_statuses = ["Open", "In Progress", "Resolved", "Escalated"]
    
    for i in range(11):
        entity_type = random.choice(["Truck", "PurchaseOrder", "Store", "DistributionCenter"])
        if entity_type == "Truck":
            entity_id = random.choice(trucks).truck_id
        elif entity_type == "PurchaseOrder":
            entity_id = random.choice(pos).po_id
        elif entity_type == "Store":
            entity_id = random.choice(stores).store_id
        else:
            entity_id = random.choice(dcs).dc_id
            
        events.append(Event(
            event_id=f"EVT{i+1:03d}",
            event_type=random.choice(event_types),
            impacted_entity=f"{entity_type}:{entity_id}",
            timestamp=(datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 168))).strftime("%Y-%m-%d %H:%M:%S"),
            resolution_status=random.choice(resolution_statuses)
        ))
    
    return {
        "distribution_centers": dcs,
        "stores": stores,
        "skus": skus,
        "trucks": trucks,
        "purchase_orders": pos,
        "shipments": shipments,
        "inventory": inventory,
        "returns": returns,
        "weather_alerts": weather_alerts,
        "events": events
    }

# Global data storage
supply_chain_data = generate_sample_data()

# API Endpoints
@app.get("/api/nodes")
async def get_all_nodes():
    """Get all supply chain nodes"""
    all_nodes = []
    for category, items in supply_chain_data.items():
        for item in items:
            all_nodes.append(asdict(item))
    return all_nodes

@app.get("/api/nodes/{node_type}")
async def get_nodes_by_type(node_type: str):
    """Get nodes by type"""
    node_type_map = {
        "distribution_centers": "distribution_centers",
        "stores": "stores",
        "skus": "skus",
        "trucks": "trucks",
        "purchase_orders": "purchase_orders",
        "shipments": "shipments",
        "inventory": "inventory",
        "returns": "returns",
        "weather_alerts": "weather_alerts",
        "events": "events"
    }
    
    if node_type not in node_type_map:
        raise HTTPException(status_code=404, detail="Node type not found")
    
    items = supply_chain_data[node_type_map[node_type]]
    return [asdict(item) for item in items]

@app.get("/api/relationships")
async def get_relationships():
    """Generate relationships between nodes"""
    relationships = []
    
    # (DistributionCenter)-[:SUPPLIES]->(Store)
    for dc in supply_chain_data["distribution_centers"]:
        # Each DC supplies multiple stores in the same region
        region_stores = [s for s in supply_chain_data["stores"] if s.region == dc.region]
        for store in random.sample(region_stores, min(15, len(region_stores))):
            relationships.append({
                "source": dc.dc_id,
                "target": store.store_id,
                "relationship": "SUPPLIES",
                "source_type": "DistributionCenter",
                "target_type": "Store"
            })
    
    # Add more relationships as needed...
    # This is a simplified version for demo purposes
    
    return relationships

@app.get("/api/summary")
async def get_summary():
    """Get summary statistics"""
    return {
        "distribution_centers": len(supply_chain_data["distribution_centers"]),
        "stores": len(supply_chain_data["stores"]),
        "skus": len(supply_chain_data["skus"]),
        "trucks": len(supply_chain_data["trucks"]),
        "purchase_orders": len(supply_chain_data["purchase_orders"]),
        "shipments": len(supply_chain_data["shipments"]),
        "inventory_snapshots": len(supply_chain_data["inventory"]),
        "returns": len(supply_chain_data["returns"]),
        "weather_alerts": len(supply_chain_data["weather_alerts"]),
        "events": len(supply_chain_data["events"])
    }

# Serve static files (React build)
app.mount("/static", StaticFiles(directory="static/static", check_dir=False), name="static")

@app.get("/")
async def serve_frontend():
    if not os.path.exists("static/index.html"):
        return {"error": "static/index.html not found", "message": "Run build.sh to build the frontend"}
    return FileResponse("static/index.html")

# Debug endpoint to check static folder
@app.get("/debug/static")
async def debug_static():
    try:
        return {"static_files": os.listdir("static")}
    except Exception as e:
        return {"error": str(e)}

# Catch-all for React Router
@app.get("/{full_path:path}")
async def serve_frontend_catch_all(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoints not found")
    if not os.path.exists("static/index.html"):
        return {"error": "static/index.html not found", "message": "Run build.sh to build the frontend"}
    return FileResponse("static/index.html")
