from zk import ZK, const

# List of devices with IP, port, and password
devices = [
    {'ip': '202.5.50.144', 'port': 50001, 'password': '8856'},
    {'ip': '202.5.50.144', 'port': 50004, 'password': '8856'},
]

for device in devices:
    conn = None

    try:
        # Create a ZK instance for each device
        zk = ZK(device['ip'], port=device['port'], password=device['password'])  # Include password

        # Connect to the device
        conn = zk.connect()
        print(f"Connected to the device at IP {device['ip']} on port {device['port']}")

        # Disable the device to prevent new inputs while fetching attendance data
        conn.disable_device()

        # Retrieve attendance logs
        attendance = conn.get_attendance()

        # Process and display attendance records
        for record in attendance:
            print(f"User ID: {record.user_id}, Timestamp: {record.timestamp}, Status: {record.status}")
            # Uncomment this to print all attributes of the attendance record
            # for attr, value in vars(record).items():
            #     print(f"{attr}: {value}")

        # Re-enable the device after data retrieval
        conn.enable_device()

    except Exception as e:
        print(f"An error occurred with device {device['ip']} on port {device['port']}: {e}")

    finally:
        # Ensure proper disconnection from the device
        if conn:
            conn.disconnect()
            print(f"Disconnected from the device at IP {device['ip']} on port {device['port']}")
