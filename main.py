from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import random
import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
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

# Add a simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Agent is running"}

# Add a test endpoint for debugging
@app.get("/test")
async def test_endpoint():
    return {"message": "Test endpoint working", "timestamp": datetime.datetime.now().isoformat()}

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
    
    elif any(word in message_lower for word in ["summary", "overview"]):
        return "📊 **Supply Chain Summary:**\n\n🏭 Distribution Centers: 16\n🏪 Stores: 200\n📦 SKUs: 500\n🚛 Trucks: 40\n📋 Purchase Orders: 60\n📦 Shipments: 25"
    
    else:
        return "🤖 **AI Assistant Response:**\n\nI can help you with:\n• 📦 Shipment tracking and delays\n• 🌦️ Weather impact analysis\n• 🚛 Fleet status and routes\n• 📊 Supply chain overview\n\nTry asking about specific areas!"

# API Endpoints
@app.get("/api/chat/messages")
async def get_chat_messages():
    """Get chat messages"""
    try:
        # Convert ChatMessage objects to dictionaries using .dict() method
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
    
    # Store user message
    user_msg = ChatMessage(
        id=str(len(chat_messages) + 1),
        role="user",
        content=user_message,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        userId=user_id
    )
    chat_messages.append(user_msg)
    
    print(f"User message stored. Total messages: {len(chat_messages)}")
    
    # Generate AI response
    ai_response = generate_ai_response(user_message)
    
    print(f"AI response generated: {len(ai_response)} characters")
    
    # Store AI response
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
async def get_supply_chain_summary():
    """Get supply chain summary"""
    return {
        "distribution_centers": 16,
        "stores": 200,
        "skus": 500,
        "trucks": 40,
        "purchase_orders": 60,
        "shipments": 25,
        "inventory_snapshots": 12,
        "returns": 15,
        "weather_alerts": 10,
        "events": 11
    }

@app.get("/api/supply-chain/shipment")
async def get_shipments():
    """Get shipments"""
    return [
        {"shipment_id": "SH0001", "status": "In Transit", "origin": "Cincinnati", "destination": "Miami", "carrier": "FedEx", "eta": "2024-01-15"},
        {"shipment_id": "SH0002", "status": "Delayed", "origin": "Dallas", "destination": "Seattle", "carrier": "UPS", "eta": "2024-01-18"},
        {"shipment_id": "SH0003", "status": "In Transit", "origin": "Chicago", "destination": "Boston", "carrier": "DHL", "eta": "2024-01-12"}
    ]

@app.get("/api/supply-chain/truck")
async def get_trucks():
    """Get trucks"""
    return [
        {"truck_id": "TRK001", "carrier": "FedEx", "status": "Delayed", "current_location": "Chicago", "route_id": "RT001"},
        {"truck_id": "TRK002", "carrier": "UPS", "status": "Delayed", "current_location": "Atlanta", "route_id": "RT002"},
        {"truck_id": "TRK003", "carrier": "DHL", "status": "In Transit", "current_location": "Denver", "route_id": "RT003"}
    ]

@app.get("/api/supply-chain/distributioncenter")
async def get_distribution_centers():
    """Get distribution centers"""
    return [
        {"dc_id": "DC001", "name": "Distribution Center Cincinnati", "location": "Cincinnati, OH", "region": "Midwest"},
        {"dc_id": "DC002", "name": "Distribution Center Dallas", "location": "Dallas, TX", "region": "South"},
        {"dc_id": "DC003", "name": "Distribution Center Atlanta", "location": "Atlanta, GA", "region": "South"}
    ]

@app.get("/api/supply-chain/store")
async def get_stores():
    """Get stores"""
    return [
        {"store_id": "ST001", "name": "Store 1 San Francisco", "location": "San Francisco, CA", "region": "West", "store_type": "urban"},
        {"store_id": "ST002", "name": "Store 2 Miami", "location": "Miami, FL", "region": "South", "store_type": "urban"},
        {"store_id": "ST003", "name": "Store 3 Portland", "location": "Portland, OR", "region": "West", "store_type": "urban"}
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

# Frontend routes
@app.get("/")
async def serve_frontend():
    return {"message": "Supply Chain Digital Twin API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)