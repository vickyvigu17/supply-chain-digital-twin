from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import datetime
from typing import List
from pydantic import BaseModel
import os

# Pydantic models
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

# CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Mount static files for production
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Global chat storage
chat_messages: List[ChatMessage] = []

# Simple AI Agent using free API
def get_ai_response(user_message: str) -> str:
    """Get AI response using a free API"""
    try:
        # Using a free AI API (you can replace this with any working API)
        api_url = "https://api.freeai.org/chat"  # This is a placeholder
        
        # For now, let's use a smart rule-based system that works immediately
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["delay", "delays", "late", "problem"]):
            return """🚨 **Supply Chain Delays Report**

📦 **Current Delays:** 3 shipments
• **Shipment SHP001**: Chicago → Miami (2-day delay)
  - Cause: Weather conditions
  - Impact: Customer delivery delayed
  - Action: Route optimization in progress

• **Shipment SHP002**: Atlanta → Seattle (1-day delay)  
  - Cause: Route congestion
  - Impact: Minor delay
  - Action: Alternative route activated

• **Truck TRK001**: In Chicago area
  - Status: Delayed due to weather
  - ETA: 2 hours behind schedule

💡 **Recommendations:**
- Monitor weather alerts for route planning
- Activate backup carriers for critical shipments
- Update customer ETAs proactively
- Consider air freight for urgent deliveries"""

        elif any(word in message_lower for word in ["weather", "storm", "rain", "snow"]):
            return """🌦️ **Weather Impact Analysis**

⚠️ **Active Weather Alerts:**
• **Northeast Region**: Severe storm warning
  - Affected areas: NY, Boston, Philadelphia
  - Impact: 15+ shipments delayed
  - Action: Route diversions activated

• **Midwest Region**: Snow storm alert
  - Affected areas: Chicago, Detroit, Milwaukee
  - Impact: 8+ shipments delayed
  - Action: Winter weather protocols

• **Southeast Region**: High wind warning
  - Affected areas: Atlanta, Miami, Charlotte
  - Impact: 5+ shipments affected
  - Action: Wind-resistant packaging required

📊 **Total Impact:**
- Distribution Centers: 4 operational, 2 under weather watch
- Active Trucks: 18 rerouted, 7 delayed
- Customer Impact: 28 shipments affected

💡 **Immediate Actions:**
- Activate weather contingency plans
- Reroute shipments through unaffected regions
- Communicate delays to customers
- Prepare backup delivery options"""

        elif any(word in message_lower for word in ["fleet", "truck", "vehicle", "driver"]):
            return """🚛 **Fleet Operations Status**

📊 **Fleet Overview:**
• **Total Vehicles**: 40 trucks
• **In Transit**: 25 trucks 🚚
• **Available**: 10 trucks ✅
• **Maintenance**: 3 trucks 🔧
• **Delayed**: 2 trucks ⚠️

📍 **Geographic Distribution:**
- **Northeast**: 8 trucks (6 operational, 2 delayed)
- **Southeast**: 12 trucks (10 operational, 2 maintenance)
- **Midwest**: 10 trucks (8 operational, 2 delayed)
- **West Coast**: 10 trucks (9 operational, 1 maintenance)

🚚 **Active Routes:**
- **Route RT001**: Chicago → Miami (TRK001)
- **Route RT002**: Atlanta → Seattle (TRK002)
- **Route RT003**: Dallas → Denver (TRK003)

💡 **Optimization Opportunities:**
- 3 trucks available for immediate dispatch
- Consider repositioning available trucks to high-demand areas
- Maintenance schedule optimization needed
- Driver training program for weather conditions"""

        elif any(word in message_lower for word in ["inventory", "stock", "supply", "warehouse"]):
            return """📦 **Inventory & Warehouse Status**

🏢 **Distribution Centers:**
• **DC001 - Chicago Hub**: 95% capacity ✅
  - High priority items: 98%
  - Medium priority: 92%
  - Low priority: 85%

• **DC002 - Atlanta Center**: 87% capacity ⚠️
  - High priority items: 95%
  - Medium priority: 78%
  - Low priority: 70%

• **DC003 - Dallas Facility**: 78% capacity ⚠️
  - High priority items: 89%
  - Medium priority: 72%
  - Low priority: 65%

⚠️ **Low Stock Alerts:**
- **Critical (reorder immediately)**: 5 items
- **Warning (reorder within 7 days)**: 12 items
- **Monitor (reorder within 14 days)**: 8 items

💡 **Inventory Actions:**
- Place orders for 5 critical items
- Review reorder points for 12 warning items
- Consider demand forecasting for seasonal items
- Optimize storage space allocation"""

        elif any(word in message_lower for word in ["shipment", "delivery", "package", "order"]):
            return """📦 **Shipment & Delivery Status**

📊 **Active Shipments: 45**
• **In Transit**: 32 shipments 🚚
  - On Schedule: 29 shipments ✅
  - Delayed: 3 shipments ⚠️

• **Delivered Today**: 8 shipments ✅
  - On Time: 7 shipments
  - Early: 1 shipment

• **Pending**: 5 shipments ⏳
  - Ready for pickup: 3
  - Processing: 2

🗺️ **Route Performance:**
- **East Coast Routes**: 95% on-time delivery
- **Midwest Routes**: 88% on-time delivery  
- **West Coast Routes**: 92% on-time delivery
- **Southeast Routes**: 89% on-time delivery

🚚 **Current Active Routes:**
- Chicago → Miami (ETA: 2 days)
- Atlanta → Seattle (ETA: 3 days)
- Dallas → Denver (ETA: 1 day)

💡 **Priority Actions:**
- Expedite 3 delayed shipments
- Monitor 5 pending shipments
- Optimize routes for better performance
- Update customer ETAs"""

        else:
            return """🤖 **Supply Chain AI Assistant**

I'm here to help you with your supply chain operations! Here's what I can help with:

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

💡 **Just ask me about:**
- "Show me current delays"
- "What's the weather impact?"
- "How's our fleet doing?"
- "Check inventory levels"
- "Shipment status"

I'm ready to help you optimize your supply chain! 🚀"""

    except Exception as e:
        return f"🤖 **AI Assistant**\n\nI'm here to help with your supply chain questions! Ask me about delays, weather, fleet status, inventory, or shipments.\n\n💡 **Try asking:**\n- 'Show me current delays'\n- 'What's the weather impact?'\n- 'How's our fleet doing?'"

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
    try:
        user_message = request.content
        user_id = request.userId
        
        # Store user message
        user_msg = ChatMessage(
            id=str(len(chat_messages) + 1),
            role="user",
            content=user_message,
            timestamp=datetime.datetime.now().isoformat(),
            userId=user_id
        )
        chat_messages.append(user_msg)
        
        # Get AI response
        ai_response = get_ai_response(user_message)
        
        # Store AI response
        ai_msg = ChatMessage(
            id=str(len(chat_messages) + 1),
            role="assistant",
            content=ai_response,
            timestamp=datetime.datetime.now().isoformat(),
            userId=user_id
        )
        chat_messages.append(ai_msg)
        
        return {"success": True, "message": "Message sent and response generated"}
    except Exception as e:
        print(f"Error creating chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
    """Root endpoint - serve frontend"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Supply Chain Digital Twin API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
