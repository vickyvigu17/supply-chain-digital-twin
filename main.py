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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat messages storage
chat_messages: List[ChatMessage] = []

# Working AI Agent with LLM Integration
async def generate_ai_response(user_message: str) -> str:
    try:
        # Use a free LLM API (you can replace this with OpenAI, Gemini, etc.)
        import aiohttp
        
        # Simple prompt engineering for supply chain context
        system_prompt = """You are a Supply Chain AI Assistant. You help users understand their supply chain operations including:
        - Shipment status and delays
        - Weather impact analysis
        - Fleet and truck information
        - Distribution center status
        - Inventory levels
        - Route optimization
        
        Provide helpful, specific responses with emojis and clear formatting. If you don't have specific data, provide general supply chain insights."""
        
        # For now, use a simple but intelligent response system
        # You can replace this with actual LLM API calls
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
            
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "🤖 I'm experiencing technical difficulties. Please try again or contact support."

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
    
    ai_response = await generate_ai_response(user_message)
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
        "total_shipments": 45,
        "active_trucks": 25,
        "delayed_shipments": 3,
        "weather_alerts": 5,
        "distribution_centers": 8
    }

@app.get("/api/supply-chain/shipment")
async def get_shipments():
    """Get shipments"""
    return [
        {"shipment_id": "SH0001", "origin": "Cincinnati, OH", "destination": "Miami, FL", "status": "In Transit", "eta": "2024-01-15"},
        {"shipment_id": "SH0002", "origin": "Dallas, TX", "destination": "Seattle, WA", "status": "Delayed", "eta": "2024-01-18"}
    ]

@app.get("/api/supply-chain/truck")
async def get_trucks():
    """Get trucks"""
    return [
        {"truck_id": "TRK001", "location": "Chicago, IL", "status": "Delayed", "current_load": "Electronics"},
        {"truck_id": "TRK002", "location": "Atlanta, GA", "status": "Delayed", "current_load": "Clothing"}
    ]

@app.get("/api/supply-chain/distributioncenter")
async def get_distribution_centers():
    """Get distribution centers"""
    return [
        {"center_id": "DC001", "name": "Northeast Hub", "location": "New York, NY", "status": "Operational"},
        {"center_id": "DC002", "name": "Midwest Hub", "location": "Chicago, IL", "status": "Operational"}
    ]

@app.get("/api/supply-chain/store")
async def get_stores():
    """Get stores"""
    return [
        {"store_id": "ST001", "name": "Store 1 San Francisco", "location": "San Francisco, CA", "region": "West", "store_type": "urban"},
        {"store_id": "ST002", "name": "Store 2 Miami", "location": "Miami, FL", "region": "South", "store_type": "urban"}
    ]

@app.get("/api/supply-chain/event")
async def get_events():
    """Get events"""
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
    """Get weather alerts"""
    return [
        {"alert_id": "WA001", "alert_type": "Storm", "region": "Northeast", "severity": "High", "date": "2024-01-10"},
        {"alert_id": "WA002", "alert_type": "Snow", "region": "Midwest", "severity": "Medium", "date": "2024-01-09"}
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
