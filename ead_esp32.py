import serial
import time

try:
    print("⚡ Initializing Hardware Loopback Test on /dev/ttyACM0...")
    # Initialize port matching your S3 native handshake configuration
    esp32 = serial.Serial('/dev/ttyACM0', 115200, timeout=1, rtscts=True, dsrdtr=True)
    time.sleep(2)
    
    test_message = "Hello ESP32-S3 Hardware"
    print(f"🚀 Sending text out via TX line: '{test_message}'")
    
    # Write data out the port
    esp32.write(f"{test_message}\n".encode('utf-8'))
    time.sleep(0.5)
    
    # Check if anything came right back into the RX buffer
    if esp32.in_waiting > 0:
        incoming_data = esp32.readline().decode('utf-8').strip()
        print(f"✅ SUCCESS! Received back on RX line: '{incoming_data}'")
        print("🎉 Your USB data connection is 100% working perfectly!")
    else:
        print("❌ FAILURE: Sent data but nothing returned on the RX line.")
        print("Check if your jumper wire securely connects TX directly to RX.")
        
except Exception as e:
    print(f"⚠️ Error opening port: {e}")
finally:
    if 'esp32' in locals() and esp32.is_open:
        esp32.close()