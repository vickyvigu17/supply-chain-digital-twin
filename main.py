from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import datetime
from typing import List
from pydantic import BaseModel

# Pydantic models for chat
class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str
    userId: str

class ChatRequest(BaseModel):
    role: str
    content: str
    userId: str

app = FastAPI()

# FIXED CORS Configuration - This will solve your CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Set to False to avoid CORS issues
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Global chat messages storage
chat_messages: List[ChatMessage] = []

# Working AI Agent with Enhanced Responses
def generate_ai_response(user_message: str) -> str:
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ["delay", "delays", "late"]):
        return """🚨 **Current Delays Analysis**

📦 **Delayed Shipments:** 3
• SH0001: Cincinnati → Miami (ETA: 2024-01-15)
  - Status: Weather-related delay
  - Impact: 2-day delay
• SH0002: Dallas → Seattle (ETA: 2024-01-18)
  - Status: Route congestion
  - Impact: 1-day delay

🚛 **Delayed Trucks:** 2
• TRK001: In Chicago (Status: Delayed)
  - Current Location: Chicago, IL
  - Destination: Miami, FL
• TRK002: In Atlanta (Status: Delayed)
  - Current Location: Atlanta, GA
  - Destination: Seattle, WA

💡 **Recommendations:**
- Monitor weather alerts for route planning
- Consider alternative routes for affected shipments
- Update customer ETAs proactively"""
    
    elif any(word in message_lower for word in ["weather", "storm"]):
        return """🌦️ **Weather Impact Analysis**

⚠️ **High Priority Alerts:** 2
• Storm in Northeast - High severity
  - Affected Region: New York, Boston, Philadelphia
  - Impact: 15+ shipments delayed
• Snow in Midwest - Medium severity
  - Affected Region: Chicago, Detroit, Milwaukee
  - Impact: 8+ shipments delayed

📊 **Total Active Alerts:** 5
• High: 2, Medium: 2, Low: 1

🚛 **Affected Operations:**
- Distribution Centers: 3 operational, 1 under weather watch
- Active Trucks: 12 rerouted, 5 delayed
- Customer Impact: 23 shipments affected

💡 **Actions Required:**
- Activate weather contingency plans
- Reroute shipments through unaffected regions
- Communicate delays to customers"""
    
    elif any(word in message_lower for word in ["fleet", "truck"]):
        return """🚛 **Fleet Status Overview**

📊 **Total Fleet:** 40 trucks
• In Transit: 25 🚚
  - On Schedule: 22
  - Delayed: 3
• Available: 10 ✅
  - Ready for dispatch: 8
  - Under maintenance: 2
• Delayed: 3 ⚠️
  - Weather-related: 2
  - Mechanical: 1
• Loading: 2 📦

📍 **Geographic Distribution:**
- Northeast: 8 trucks
- Southeast: 12 trucks
- Midwest: 10 trucks
- West: 10 trucks

💡 **Optimization Opportunities:**
- 3 trucks available for immediate dispatch
- Consider repositioning available trucks to high-demand areas
- Maintenance schedule optimization needed"""
    
    elif any(word in message_lower for word in ["distribution", "center", "warehouse"]):
        return """🏢 **Distribution Centers Status**

📊 **Total Centers:** 8
• Operational: 7 ✅
  - Northeast Hub (NY): 95% capacity
  - Midwest Hub (Chicago): 87% capacity
  - Southeast Hub (Atlanta): 92% capacity
  - West Hub (LA): 78% capacity
• Under Maintenance: 1 🔧
  - Southwest Hub (Dallas): Scheduled maintenance

📦 **Capacity Utilization:** 85% overall
• High Priority Items: 92% ✅
• Medium Priority: 75% ⚠️
• Low Priority: 65% ⚠️

💡 **Recommendations:**
- Southwest Hub maintenance completion: 2 days
- Consider load balancing between operational centers
- Monitor capacity levels for peak season planning"""
    
    elif any(word in message_lower for word in ["shipment", "delivery", "package"]):
        return """📦 **Shipment Overview**

📊 **Total Active Shipments:** 45
• In Transit: 32 🚚
  - On Schedule: 29
  - Delayed: 3
• Delivered Today: 8 ✅
  - On Time: 7
  - Early: 1
• Delayed: 3 ⚠️
  - Weather: 2
  - Route: 1
• Pending: 2 ⏳

🗺️ **Route Performance:**
- East Coast Routes: 95% on-time
- Midwest Routes: 88% on-time
- West Coast Routes: 92% on-time

💡 **Priority Actions:**
- Expedite 3 delayed shipments
- Monitor 2 pending shipments
- Optimize routes for better performance"""
    
    elif any(word in message_lower for word in ["inventory", "stock", "supply"]):
        return """📦 **Inventory Status**

📊 **Overall Stock Level:** 78%
• High Priority Items: 92% ✅
  - Electronics: 95%
  - Pharmaceuticals: 89%
• Medium Priority: 75% ⚠️
  - Clothing: 78%
  - Home Goods: 72%
• Low Priority: 65% ⚠️
  - Seasonal Items: 60%
  - Bulk Goods: 70%

⚠️ **Low Stock Alerts:** 12 items
• Critical: 3 items (reorder immediately)
• Warning: 9 items (reorder within 7 days)

💡 **Inventory Actions:**
- Place orders for 3 critical items
- Review reorder points for 9 warning items
- Consider demand forecasting for seasonal items"""
    
    else:
        return """🤖 **Supply Chain AI Assistant**

I can help you with comprehensive supply chain insights:

📦 **Shipment Management**
• Real-time tracking and status
• Delay analysis and impact assessment
• Route optimization recommendations

🌦️ **Weather Intelligence**
• Impact analysis on operations
• Proactive delay prevention
• Alternative route planning

🚛 **Fleet Operations**
• Vehicle status and location
• Maintenance scheduling
• Capacity optimization

🏢 **Distribution Centers**
• Operational status monitoring
• Capacity utilization analysis
• Performance metrics

📊 **Inventory Control**
• Stock level monitoring
• Reorder point alerts
• Demand forecasting insights

💡 **Ask me anything specific about your supply chain operations!**"""

# API Endpoints
@app.get("/api/chat/messages")
async def get_chat_messages():
    """Get chat messages"""
    try:
        messages = []
        for msg in chat_messages:
            messages.append(msg.dict())
        return messages
    except Exception as e:
        print(f"Error getting chat messages: {e}")
        return []

@app.post("/api/chat/messages")
async def create_chat_message(request: ChatRequest):
    """Create a new chat message"""
    print(f"Received chat request: {request}")
    user_message = request.content
    user_id = request.userId
    print(f"Processing message: '{user_message}' from user: {user_id}")
    
    user_msg = ChatMessage(
        id=str(len(chat_messages) + 1),
        role="user",
        content=user_message,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        userId=user_id
    )
    chat_messages.append(user_msg)
    print(f"User message stored. Total messages: {len(chat_messages)}")
    
    ai_response = generate_ai_response(user_message)
    print(f"AI response generated: {len(ai_response)} characters")
    
    ai_msg = ChatMessage(
        id=str(len(chat_messages) + 1),
        role="assistant",
        content=ai_response,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        userId=user_id
    )
    chat_messages.append(ai_msg)
    print(f"AI message stored. Total messages: {len(chat_messages)}")
    
    return {"success": True, "message": "Message sent and response generated"}

@app.get("/api/supply-chain/summary")
async def get_summary():
    """Get supply chain summary"""
    return {
        "distribution_centers": 8,
        "stores": 15,
        "trucks": 40,
        "shipments": 45
    }

@app.get("/api/supply-chain/shipment")
async def get_shipments():
    """Get shipments data"""
    return [
        {
            "shipment_id": "SHP001",
            "status": "In Transit",
            "origin": "Chicago, IL",
            "destination": "Miami, FL",
            "carrier": "FastFreight Inc",
            "eta": "2024-01-12 14:00:00"
        },
        {
            "shipment_id": "SHP002",
            "status": "Delayed",
            "origin": "Atlanta, GA",
            "destination": "Seattle, WA",
            "carrier": "QuickShip Co",
            "eta": "2024-01-13 09:00:00"
        },
        {
            "shipment_id": "SHP003",
            "status": "Processing",
            "origin": "Dallas, TX",
            "destination": "Denver, CO",
            "carrier": "Reliable Logistics",
            "eta": "2024-01-12 16:00:00"
        }
    ]

@app.get("/api/supply-chain/truck")
async def get_trucks():
    """Get trucks data"""
    return [
        {
            "truck_id": "TRK001",
            "carrier": "FastFreight Inc",
            "status": "In Transit",
            "current_location": "Chicago, IL",
            "route_id": "RT001"
        },
        {
            "truck_id": "TRK002",
            "carrier": "QuickShip Co",
            "status": "Delayed",
            "current_location": "Atlanta, GA",
            "route_id": "RT002"
        },
        {
            "truck_id": "TRK003",
            "carrier": "Reliable Logistics",
            "status": "Loading",
            "current_location": "Dallas, TX",
            "route_id": "RT003"
        }
    ]

@app.get("/api/supply-chain/distributioncenter")
async def get_distribution_centers():
    """Get distribution centers data"""
    return [
        {
            "dc_id": "DC001",
            "name": "Chicago Hub",
            "location": "Chicago, IL",
            "status": "Operational",
            "capacity": 1000000
        },
        {
            "dc_id": "DC002",
            "name": "Atlanta Center",
            "location": "Atlanta, GA",
            "status": "Operational",
            "capacity": 800000
        },
        {
            "dc_id": "DC003",
            "name": "Dallas Facility",
            "location": "Dallas, TX",
            "status": "Operational",
            "capacity": 1200000
        }
    ]

@app.get("/api/supply-chain/store")
async def get_stores():
    """Get stores data"""
    return [
        {
            "store_id": "ST001",
            "name": "Downtown Miami",
            "location": "Miami, FL",
            "status": "Operational",
            "inventory_level": 85
        },
        {
            "store_id": "ST002",
            "name": "Seattle Central",
            "location": "Seattle, WA",
            "status": "Operational",
            "inventory_level": 92
        },
        {
            "store_id": "ST003",
            "name": "Denver Metro",
            "location": "Denver, CO",
            "status": "Operational",
            "inventory_level": 78
        }
    ]

@app.get("/api/supply-chain/event")
async def get_events():
    """Get events with source and destination"""
    return [
        {
            "event_id": "EVT001",
            "event_type": "Delay",
            "impacted_entity": "Truck:TRK001",
            "source": "Chicago, IL",
            "destination": "Miami, FL",
            "timestamp": "2024-01-10 10:00:00",
            "resolution_status": "Open",
            "description": "Weather-related delay in transit"
        },
        {
            "event_id": "EVT002",
            "event_type": "Shortage",
            "impacted_entity": "Store:ST001",
            "source": "Distribution Center DC001",
            "destination": "San Francisco, CA",
            "timestamp": "2024-01-09 15:30:00",
            "resolution_status": "In Progress",
            "description": "Inventory shortage affecting store operations"
        },
        {
            "event_id": "EVT003",
            "event_type": "Route Change",
            "impacted_entity": "Truck:TRK002",
            "source": "Atlanta, GA",
            "destination": "Seattle, WA",
            "timestamp": "2024-01-10 08:15:00",
            "resolution_status": "Resolved",
            "description": "Route optimized due to traffic conditions"
        }
    ]

@app.get("/api/supply-chain/weatheralert")
async def get_weather_alerts():
    """Get weather alerts data"""
    return [
        {
            "alert_id": "WA001",
            "alert_type": "Severe Storm",
            "region": "Midwest",
            "date": "2024-01-10",
            "severity": "High"
        },
        {
            "alert_id": "WA002",
            "alert_type": "High Wind",
            "region": "East Coast",
            "date": "2024-01-10",
            "severity": "Medium"
        }
    ]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Supply Chain Digital Twin API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Supply Chain Digital Twin API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
