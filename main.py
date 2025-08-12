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

# Simple AI Agent
def generate_ai_response(user_message: str) -> str:
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ["delay", "delays", "late"]):
        return "🚨 **Current Delays Analysis:**\n\n📦 **Delayed Shipments:** 3\n• SH0001: Cincinnati → Miami (ETA: 2024-01-15)\n• SH0002: Dallas → Seattle (ETA: 2024-01-18)\n\n🚛 **Delayed Trucks:** 2\n• TRK001: In Chicago (Status: Delayed)\n• TRK002: In Atlanta (Status: Delayed)"
    
    elif any(word in message_lower for word in ["weather", "storm"]):
        return "🌦️ **Weather Impact Analysis:**\n\n⚠️ **High Priority Alerts:** 2\n• Storm in Northeast - High severity\n• Snow in Midwest - Medium severity\n\n📊 **Total Active Alerts:** 5"
   
    elif any(word in message_lower for word in ["fleet", "truck"]):
        return "🚛 **Fleet Status Overview:**\n\n📊 **Total Fleet:** 40 trucks\n• In Transit: 25 🚚\n• Available: 10 ✅\n• Delayed: 3 ⚠️\n• Loading: 2 📦"
    
    elif any(word in message_lower for word in ["distribution", "center", "warehouse"]):
        return "🏢 **Distribution Centers Status:**\n\n📊 **Total Centers:** 8\n• Operational: 7 ✅\n• Under Maintenance: 1 🔧\n• Capacity Utilization: 85%"
    
    elif any(word in message_lower for word in ["shipment", "delivery", "package"]):
        return "📦 **Shipment Overview:**\n\n📊 **Total Active Shipments:** 45\n• In Transit: 32 🚚\n• Delivered Today: 8 ✅\n• Delayed: 3 ⚠️\n• Pending: 2 ⏳"
    
    elif any(word in message_lower for word in ["inventory", "stock", "supply"]):
        return "📦 **Inventory Status:**\n\n📊 **Overall Stock Level:** 78%\n• High Priority Items: 92% ✅\n• Medium Priority: 75% ⚠️\n• Low Priority: 65% ⚠️"
    
    else:
        return "🤖 **Supply Chain AI Assistant**\n\nI can help you with:\n• 📦 Shipment status and delays\n• 🌦️ Weather impact analysis\n• 🚛 Fleet and truck information\n• 🏢 Distribution center status\n• 📊 Inventory levels\n\nAsk me anything about your supply chain!"

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
        {"event_id": "EVT001", "event_type": "Delay", "impacted_entity": "Truck:TRK001", "timestamp": "2024-01-10 10:00:00", "resolution_status": "Open"},
        {"event_id": "EVT002", "event_type": "Shortage", "impacted_entity": "Store:ST001", "timestamp": "2024-01-09 15:30:00", "resolution_status": "In Progress"}
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
