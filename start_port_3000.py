#!/usr/bin/env python3
import uvicorn
from datetime import datetime

print("="*60)
print(f"🚀 STARTING ON PORT 3000 - {datetime.now()}")
print("="*60)

# Verify data before starting
from main import supply_chain_data
shipments = supply_chain_data['shipments']
print(f"✅ DATA VERIFICATION:")
print(f"   📦 Total Shipments: {len(shipments)}")
print(f"   🛑 Max Stops per Route: {max(s.stops_count for s in shipments)}")
print(f"   🚫 Milk Runs (>5 stops): {len([s for s in shipments if s.stops_count > 5])}")
print(f"   🛣️  Route Types: {list(set(s.route_type for s in shipments))}")

print("="*60)
print("🌟 NEW CODESPACES URL:")
print("🌟 https://super-memory-9gq79x7w9f99jq-3000.app.github.dev/")
print("🌟 Test endpoint: /test123")
print("="*60)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)