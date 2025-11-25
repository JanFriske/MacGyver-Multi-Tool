import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.uplink_service import get_uplink_service

def test_uplink():
    print("Testing MacGyver Uplink Service...")
    service = get_uplink_service()
    
    # Test Data
    data = {
        "message": "Hello MacGyver!",
        "secret": "This is a secret translation.",
        "numbers": [4, 8, 15, 16, 23, 42]
    }
    
    print("\n1. Sending Data...")
    success, result = service.generate_uplink_code(data, expiry="1d")
    
    if success:
        code = result
        print(f"   ✅ Upload Successful!")
        print(f"   🔑 Magic Code: {code}")
    else:
        print(f"   ❌ Upload Failed: {result}")
        return

    print("\n2. Receiving Data...")
    # Simulate receiver
    success, received_data = service.receive_uplink_data(code)
    
    if success:
        print(f"   ✅ Download & Decryption Successful!")
        print(f"   📄 Data: {json.dumps(received_data, indent=2)}")
        
        if received_data == data:
            print("   ✅ Integrity Check Passed: Data matches exactly.")
        else:
            print("   ❌ Integrity Check Failed: Data mismatch.")
    else:
        print(f"   ❌ Receive Failed: {received_data}")

    print("\n3. Testing Invalid Code...")
    success, _ = service.receive_uplink_data("MG-INVALID-CODE")
    if not success:
        print("   ✅ Correctly rejected invalid code.")
    else:
        print("   ❌ Failed to reject invalid code.")

if __name__ == "__main__":
    test_uplink()
