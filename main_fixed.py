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
from pydantic import BaseModel

# Pydantic models for chat
class ChatMessage(BaseModel):
    id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    userId: str

class ChatRequest(BaseModel):
    role: str
    content: str
    userId: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat messages storage (in production, use a database)
chat_messages: List[ChatMessage] = []

# AI Agent Logic
class SupplyChainAI:
    def __init__(self, supply_chain_data):
        self.data = supply_chain_data
    
    def generate_response(self, user_message: str) -> str:
        """Generate AI response based on user message and supply chain data"""
        message_lower = user_message.lower()
        
        # Check for specific query types
        if any(word in message_lower for word in ["delay", "delays", "late", "slow"]):
            return self._analyze_delays()
        elif any(word in message_lower for word in ["weather", "storm", "rain", "snow"]):
            return self._analyze_weather_impact()
        elif any(word in message_lower for word in ["fleet", "truck", "trucks", "vehicle"]):
            return self._analyze_fleet_status()
        elif any(word in message_lower for word in ["distribution", "dc", "warehouse"]):
            return self._analyze_distribution_centers()
        elif any(word in message_lower for word in ["shipment", "shipments", "delivery"]):
            return self._analyze_shipments()
        elif any(word in message_lower for word in ["inventory", "stock", "quantity"]):
            return self._analyze_inventory()
        elif any(word in message_lower for word in ["summary", "overview", "status"]):
            return self._generate_summary()
        else:
            return self._generate_general_response(user_message)
    
    def _analyze_delays(self) -> str:
        """Analyze current delays in the supply chain"""
        delayed_shipments = [s for s in self.data["shipments"] if s.status == "Delayed"]
        delayed_trucks = [t for t in self.data["trucks"] if t.status == "Delayed"]
        
        response = "🚨 **Current Delays Analysis:**\n\n"
        
        if delayed_shipments:
            response += f"📦 **Delayed Shipments:** {len(delayed_shipments)}\n"
            for shipment in delayed_shipments[:3]:  # Show top 3
                response += f"• {shipment.shipment_id}: {shipment.origin} → {shipment.destination} (ETA: {shipment.eta})\n"
        else:
            response += "✅ No delayed shipments currently\n"
        
        if delayed_trucks:
            response += f"\n🚛 **Delayed Trucks:** {len(delayed_trucks)}\n"
            for truck in delayed_trucks[:3]:  # Show top 3
                response += f"• {truck.truck_id}: {truck.current_location} (Status: {truck.status})\n"
        else:
            response += "\n✅ No delayed trucks currently\n"
        
        return response
    
    def _analyze_weather_impact(self) -> str:
        """Analyze weather impact on supply chain"""
        weather_alerts = self.data["weather_alerts"]
        high_severity = [w for w in weather_alerts if w.severity in ["High", "Critical"]]
        
        response = "🌦️ **Weather Impact Analysis:**\n\n"
        
        if high_severity:
            response += f"⚠️ **High Priority Alerts:** {len(high_severity)}\n"
            for alert in high_severity:
                response += f"• {alert.alert_type} in {alert.region} - {alert.severity} severity\n"
        else:
            response += "✅ No high-priority weather alerts\n"
        
        response += f"\n📊 **Total Active Alerts:** {len(weather_alerts)}\n"
        response += f"• Low: {len([w for w in weather_alerts if w.severity == 'Low'])}\n"
        response += f"• Medium: {len([w for w in weather_alerts if w.severity == 'Medium'])}\n"
        response += f"• High: {len([w for w in weather_alerts if w.severity == 'High'])}\n"
        response += f"• Critical: {len([w for w in weather_alerts if w.severity == 'Critical'])}\n"
        
        return response
    
    def _analyze_fleet_status(self) -> str:
        """Analyze fleet status"""
        trucks = self.data["trucks"]
        in_transit = [t for t in trucks if t.status == "In Transit"]
        available = [t for t in trucks if t.status == "Available"]
        delayed = [t for t in trucks if t.status == "Delayed"]
        
        response = "🚛 **Fleet Status Overview:**\n\n"
        response += f"📊 **Total Fleet:** {len(trucks)} trucks\n"
        response += f"• In Transit: {len(in_transit)} 🚚\n"
        response += f"• Available: {len(available)} ✅\n"
        response += f"• Delayed: {len(delayed)} ⚠️\n"
        response += f"• Loading: {len([t for t in trucks if t.status == 'Loading'])} 📦\n"
        response += f"• Delivered: {len([t for t in trucks if t.status == 'Delivered'])} 🎯\n"
        
        # Show some active routes
        if in_transit:
            response += f"\n🛣️ **Active Routes:**\n"
            for truck in in_transit[:3]:
                response += f"• {truck.truck_id} on {truck.route_id} (Location: {truck.current_location})\n"
        
        return response
    
    def _analyze_distribution_centers(self) -> str:
        """Analyze distribution center status"""
        dcs = self.data["distribution_centers"]
        
        response = "🏭 **Distribution Centers Status:**\n\n"
        response += f"📊 **Total DCs:** {len(dcs)}\n"
        
        # Group by region
        regions = {}
        for dc in dcs:
            if dc.region not in regions:
                regions[dc.region] = []
            regions[dc.region].append(dc)
        
        response += f"🌍 **Regional Distribution:**\n"
        for region, dc_list in regions.items():
            response += f"• {region}: {len(dc_list)} DCs\n"
        
        response += f"\n📍 **Sample Locations:**\n"
        for dc in dcs[:5]:
            response += f"• {dc.name} in {dc.location}\n"
        
        return response
    
    def _analyze_shipments(self) -> str:
        """Analyze shipment status"""
        shipments = self.data["shipments"]
        in_transit = [s for s in shipments if s.status == "In Transit"]
        delayed = [s for s in shipments if s.status == "Delayed"]
        delivered = [s for s in shipments if s.status == "Delivered"]
        
        response = "📦 **Shipment Status Overview:**\n\n"
        response += f"📊 **Total Shipments:** {len(shipments)}\n"
        response += f"• In Transit: {len(in_transit)} 🚚\n"
        response += f"• Delayed: {len(delayed)} ⚠️\n"
        response += f"• Delivered: {len(delivered)} ✅\n"
        response += f"• Processing: {len([s for s in shipments if s.status == 'Processing'])} ⏳\n"
        
        if in_transit:
            response += f"\n🚚 **Active Shipments:**\n"
            for shipment in in_transit[:3]:
                response += f"• {shipment.shipment_id}: {shipment.origin} → {shipment.destination}\n"
                response += f"  ETA: {shipment.eta}, Mode: {shipment.mode}\n"
        
        return response
    
    def _analyze_inventory(self) -> str:
        """Analyze inventory status"""
        inventory = self.data["inventory"]
        low_stock = [inv for inv in inventory if inv.quantity_on_hand < 100]
        
        response = "📦 **Inventory Status:**\n\n"
        response += f"📊 **Total SKUs Tracked:** {len(inventory)}\n"
        response += f"• Low Stock Items (<100): {len(low_stock)} ⚠️\n"
        response += f"• Well Stocked Items: {len(inventory) - len(low_stock)} ✅\n"
        
        if low_stock:
            response += f"\n⚠️ **Low Stock Alerts:**\n"
            for inv in low_stock[:3]:
                response += f"• {inv.sku_id}: {inv.quantity_on_hand} units at Store {inv.store_id}\n"
        
        return response
    
    def _generate_summary(self) -> str:
        """Generate overall supply chain summary"""
        response = "📊 **Supply Chain Digital Twin Summary:**\n\n"
        response += f"🏭 **Distribution Centers:** {len(self.data['distribution_centers'])}\n"
        response += f"🏪 **Stores:** {len(self.data['stores'])}\n"
        response += f"📦 **SKUs:** {len(self.data['skus'])}\n"
        response += f"🚛 **Trucks:** {len(self.data['trucks'])}\n"
        response += f"📋 **Purchase Orders:** {len(self.data['purchase_orders'])}\n"
        response += f"📦 **Shipments:** {len(self.data['shipments'])}\n"
        response += f"📊 **Inventory Snapshots:** {len(self.data['inventory'])}\n"
        response += f"🔄 **Returns:** {len(self.data['returns'])}\n"
        response += f"🌦️ **Weather Alerts:** {len(self.data['weather_alerts'])}\n"
        response += f"⚠️ **Events:** {len(self.data['events'])}\n"
        
        # Add some insights
        delayed_shipments = len([s for s in self.data['shipments'] if s.status == 'Delayed'])
        open_events = len([e for e in self.data['events'] if e.resolution_status == 'Open'])
        
        response += f"\n🔍 **Key Insights:**\n"
        response += f"• Delayed Shipments: {delayed_shipments}\n"
        response += f"• Open Issues: {open_events}\n"
        
        return response
    
    def _generate_general_response(self, user_message: str) -> str:
        """Generate a general helpful response"""
        response = "🤖 **AI Assistant Response:**\n\n"
        response += f"I understand you're asking about: '{user_message}'\n\n"
        response += "I can help you with:\n"
        response += "• 📦 Shipment tracking and delays\n"
        response += "• 🌦️ Weather impact analysis\n"
        response += "• 🚛 Fleet status and routes\n"
        response += "• 🏭 Distribution center operations\n"
        response += "• 📊 Inventory levels\n"
        response += "• ⚠️ Issue tracking and resolution\n\n"
        response += "Try asking about specific areas like 'Show me current delays' or 'Weather impact summary'"
        
        return response

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
    destination: str
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
    # Separate cities for DCs and Stores to avoid overlap
    dc_cities = [
        ("Cincinnati, OH", "Midwest"), ("Dallas, TX", "South"), ("Atlanta, GA", "South"),
        ("Denver, CO", "West"), ("Chicago, IL", "Midwest"), ("Phoenix, AZ", "West"),
        ("Seattle, WA", "West"), ("Orlando, FL", "South"), ("Nashville, TN", "South"),
        ("Salt Lake City, UT", "West"), ("Boston, MA", "Northeast"), ("Detroit, MI", "Midwest"),
        ("Houston, TX", "South"), ("Los Angeles, CA", "West"), ("New York, NY", "Northeast"),
        ("Philadelphia, PA", "Northeast")
    ]
    
    store_cities = [
        ("San Francisco, CA", "West"), ("Miami, FL", "South"), ("Portland, OR", "West"), 
        ("Minneapolis, MN", "Midwest"), ("Baltimore, MD", "Northeast"), ("Richmond, VA", "South"),
        ("Kansas City, MO", "Midwest"), ("San Antonio, TX", "South"), ("Las Vegas, NV", "West"),
        ("Charlotte, NC", "South"), ("Cleveland, OH", "Midwest"), ("Pittsburgh, PA", "Northeast"),
        ("Buffalo, NY", "Northeast"), ("Birmingham, AL", "South"), ("Oklahoma City, OK", "South"),
        ("Memphis, TN", "South"), ("Louisville, KY", "South"), ("Milwaukee, WI", "Midwest"),
        ("Albuquerque, NM", "West"), ("Tucson, AZ", "West")
    ]
    
    # Generate Distribution Centers (16)
    dcs = []
    for i in range(16):
        city, region = dc_cities[i]
        dcs.append(DistributionCenter(
            dc_id=f"DC{i+1:03d}",
            name=f"Distribution Center {city.split(',')[0]}",
            location=city,
            region=region
        ))
    
    # Generate Stores (200) - use different cities than DCs
    stores = []
    store_types = ["urban", "rural"]
    for i in range(200):
        # Cycle through store cities and add some random ones
        if i < len(store_cities):
            city, region = store_cities[i % len(store_cities)]
        else:
            # Add some stores in same cities as DCs but they'll be positioned differently
            city, region = random.choice(dc_cities + store_cities)
        
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
        truck_city, _ = random.choice(dc_cities + store_cities)
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
    
    # Generate Shipments (25) - More shipments with varied statuses
    shipments = []
    modes = ["FTL", "LTL", "Parcel", "Express"]
    shipment_statuses = ["In Transit", "Delivered", "Delayed", "Processing"]
    
    for i in range(25):
        origin_dc = random.choice(dcs)
        dest_store = random.choice(stores)
        eta = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 5))
        
        # Ensure we have some of each status
        if i < 8:
            status = "In Transit"
        elif i < 12:
            status = "Delayed" 
        elif i < 16:
            status = "Processing"
        else:
            status = random.choice(shipment_statuses)
        
        shipments.append(Shipment(
            shipment_id=f"SH{i+1:04d}",
            carrier=random.choice(carriers),
            mode=random.choice(modes),
            status=status,
            eta=eta.strftime("%Y-%m-%d"),
            origin=origin_dc.location,
            destination=dest_store.location
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
    regions = ["Northeast", "South", "Midwest", "West"]
    
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

# Initialize AI agent
ai_agent = SupplyChainAI(supply_chain_data)

# ===== API ENDPOINTS - MUST BE DEFINED FIRST =====

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

# Frontend-specific endpoints
@app.get("/api/supply-chain/summary")
async def get_supply_chain_summary():
    """Get supply chain summary (frontend endpoint)"""
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

@app.get("/api/supply-chain/shipment")
async def get_shipments():
    """Get all shipments"""
    return [asdict(shipment) for shipment in supply_chain_data["shipments"]]

@app.get("/api/supply-chain/truck")
async def get_trucks():
    """Get all trucks"""
    return [asdict(truck) for truck in supply_chain_data["trucks"]]

@app.get("/api/supply-chain/distributioncenter")
async def get_distribution_centers():
    """Get all distribution centers"""
    return [asdict(dc) for dc in supply_chain_data["distribution_centers"]]

@app.get("/api/supply-chain/store")
async def get_stores():
    """Get all stores"""
    return [asdict(store) for store in supply_chain_data["stores"]]

@app.get("/api/supply-chain/event")
async def get_events():
    """Get all events"""
    return [asdict(event) for event in supply_chain_data["events"]]

@app.get("/api/supply-chain/weatheralert")
async def get_weather_alerts():
    """Get all weather alerts"""
    return [asdict(alert) for alert in supply_chain_data["weather_alerts"]]

# ===== AI AGENT CHAT ENDPOINTS =====

@app.get("/api/chat/history")
async def get_chat_history():
    """Endpoint to retrieve chat history"""
    return [asdict(msg) for msg in chat_messages]

@app.get("/api/chat/messages")
async def get_chat_messages():
    """Endpoint to retrieve chat messages (alias for history)"""
    return [asdict(msg) for msg in chat_messages]

@app.post("/api/chat/messages")
async def create_chat_message(request: ChatRequest):
    """Endpoint to create a new chat message"""
    user_message = request.content
    user_id = request.userId
    
    # Store the user message
    user_msg = ChatMessage(
        id=str(len(chat_messages) + 1),
        role="user",
        content=user_message,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        userId=user_id
    )
    chat_messages.append(user_msg)
    
    # Generate AI response
    ai_response = ai_agent.generate_response(user_message)
    
    # Store the AI response
    ai_msg = ChatMessage(
        id=str(len(chat_messages) + 1),
        role="assistant",
        content=ai_response,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        userId=user_id
    )
    chat_messages.append(ai_msg)
    
    return {"success": True, "message": "Message sent and response generated"}

# ===== FRONTEND ROUTES - DEFINED LAST =====

@app.get("/")
async def serve_frontend():
    if not os.path.exists("static/index.html"):
        return {"error": "static/index.html not found", "message": "Run build.sh to build the frontend"}
    return FileResponse("static/index.html")

@app.get("/debug/static")
async def debug_static():
    try:
        return {"static_files": os.listdir("static")}
    except Exception as e:
        return {"error": str(e)}

# Frontend route for React Router - must be last
@app.get("/{full_path:path}")
async def serve_frontend_catch_all(full_path: str):
    # Skip API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Serve frontend for all other routes
    if not os.path.exists("static/index.html"):
        return {"error": "static/index.html not found", "message": "Run build.sh to build the frontend"}
    return FileResponse("static/index.html")

# Serve static files (React build) - moved to end to avoid route conflicts
app.mount("/static", StaticFiles(directory="static/static", check_dir=False), name="static")

# For Render deployment
if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)