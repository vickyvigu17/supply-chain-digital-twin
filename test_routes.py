#!/usr/bin/env python3

import requests
import time

def test_endpoints():
    base_url = "http://localhost:8000"
    
    # Test basic endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code}")
    except Exception as e:
        print(f"Root endpoint error: {e}")
    
    # Test API endpoint
    try:
        response = requests.get(f"{base_url}/api/chat/messages")
        print(f"Chat messages endpoint: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Chat messages error: {e}")
    
    # Test supply chain endpoint
    try:
        response = requests.get(f"{base_url}/api/supply-chain/summary")
        print(f"Supply chain summary: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Supply chain error: {e}")

if __name__ == "__main__":
    print("Testing endpoints...")
    time.sleep(2)  # Wait for server to start
    test_endpoints()