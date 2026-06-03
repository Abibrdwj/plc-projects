from opcua import Client

# Try anonymous
print("Trying anonymous connection...")
try:
    client = Client("opc.tcp://localhost:4840")
    client.connect()
    print("Anonymous connection SUCCESS!")
    client.disconnect()
except Exception as e:
    print(f"Anonymous failed: {e}")

# Try with credentials
print("\nTrying username/password connection...")
try:
    client = Client("opc.tcp://localhost:4840")
    client.set_user("admin")
    client.set_password("Plc@2026")
    client.connect()
    print("Username/password connection SUCCESS!")
    client.disconnect()
except Exception as e:
    print(f"Username/password failed: {e}")