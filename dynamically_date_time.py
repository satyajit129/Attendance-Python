from zk import ZK, const
from datetime import datetime

# Replace with your device's IP address and other details
device_ip = '202.5.50.144'
device_port = 50001
password = '8856'

zk = ZK(device_ip, port=device_port, password=password)  # Include password

conn = None

try:
    # Get dynamic input from the user for start and end date/time
    start_date_str = input("Enter the start date and time (YYYY-MM-DD HH:MM:SS): ")
    end_date_str = input("Enter the end date and time (YYYY-MM-DD HH:MM:SS): ")

    # Convert input strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')

    # Connect to the device
    conn = zk.connect()
    print("Connected to the device successfully")

    # Disable the device to prevent new inputs while fetching attendance data
    conn.disable_device()

    # Retrieve attendance logs
    attendance = conn.get_attendance()

    # Process and display attendance records within the specified date/time range
    print(f"Attendance records between {start_date} and {end_date}:")
    for record in attendance:
        record_time = record.timestamp  # Get the full timestamp (date and time)
        if start_date <= record_time <= end_date:
            print(f"User ID: {record.user_id}, Timestamp: {record.timestamp}, Status: {record.status}")
    conn.enable_device()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure proper disconnection from the device
    if conn:
        conn.disconnect()
        print("Disconnected from the device")
