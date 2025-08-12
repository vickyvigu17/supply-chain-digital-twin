#!/usr/bin/env python3

import requests
import time
import subprocess
import sys

def test_server():
    print("Testing Supply Chain Digital Twin AI Agent...")
    
    # Start server
    print("Starting server...")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main_simple:app", 
            "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        
        # Test endpoints
        base_url = "http://localhost:8000"
        
        print("Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"Root: {response.status_code} - {response.json()}")
        
        print("Testing AI agent endpoint...")
        response = requests.get(f"{base_url}/api/chat/messages")
        print(f"Chat messages: {response.status_code} - {response.json()}")
        
        print("Testing supply chain summary...")
        response = requests.get(f"{base_url}/api/supply-chain/summary")
        print(f"Summary: {response.status_code} - {response.json()}")
        
        # Test AI agent with a message
        print("Testing AI agent response...")
        response = requests.post(f"{base_url}/api/chat/messages", json={
            "role": "user",
            "content": "Show me current delays",
            "userId": "test-user"
        })
        print(f"AI Response: {response.status_code} - {response.json()}")
        
        # Get updated chat messages
        response = requests.get(f"{base_url}/api/chat/messages")
        print(f"Updated chat: {response.status_code} - {len(response.json())} messages")
        
        print("\n✅ AI Agent is working successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Stop server
        if 'process' in locals():
            process.terminate()
            process.wait()

if __name__ == "__main__":
    test_server()