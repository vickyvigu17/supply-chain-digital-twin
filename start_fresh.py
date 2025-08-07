#!/usr/bin/env python3
import uvicorn
import os
from datetime import datetime

print("="*50)
print(f"🚀 STARTING FRESH SERVER - {datetime.now()}")
print("="*50)

# Verify data before starting
from main import supply_chain_data
shipments = supply_chain_data['shipments']
print(f"✅ DATA VERIFIED:")
print(f"   - Shipments: {len(shipments)}")
print(f"   - Max stops: {max(s.stops_count for s in shipments)}")
print(f"   - Milk runs (>5): {len([s for s in shipments if s.stops_count > 5])}")
print(f"   - Route types: {set(s.route_type for s in shipments)}")
print("="*50)

# Start server
port = int(os.environ.get("PORT", 8000))
print(f"🌟 Server starting on port {port}")
print(f"🌟 Codespaces URL should be available at your GitHub URL")
print("="*50)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)