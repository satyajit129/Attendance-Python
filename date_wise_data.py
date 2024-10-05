from zk import ZK, const
from datetime import datetime

# Replace with your device's IP address and other details
device_ip = '202.5.50.144'
device_port = 50001
password = '8856'

zk = ZK(device_ip, port=device_port, password=password)  # Include password

conn = None  # Initialize `conn` to avoid undefined variable issues

try:
    # Connect to the device
    conn = zk.connect()
    print("Connected to the device successfully")

    # Disable the device to prevent new inputs while fetching attendance data
    conn.disable_device()

    # Retrieve attendance logs
    attendance = conn.get_attendance()

    # Get today's date
    today = datetime.now().date()

    # Process and display only today's attendance records
    print("Today's attendance records:")
    for record in attendance:
        record_date = record.timestamp.date()  # Extract the date part from the timestamp
        if record_date == today:
            print(f"User ID: {record.user_id}, Timestamp: {record.timestamp}, Status: {record.status}")

    # Re-enable the device after data retrieval
    conn.enable_device()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure proper disconnection from the device
    if conn:
        conn.disconnect()
        print("Disconnected from the device")
