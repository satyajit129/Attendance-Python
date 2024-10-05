from flask import Flask, request, jsonify
from zk import ZK, const
from datetime import datetime

# Flask app instance
app = Flask(__name__)

# List of devices with IP, port, and password
devices = [
    {'ip': '202.5.50.144', 'port': 50001, 'password': '8856'},
    {'ip': '202.5.50.144', 'port': 50004, 'password': '8856'},
]

# Function to fetch attendance data
def get_attendance_data(start_date, end_date, user_id=None):
    attendance_data = []

    for device in devices:
        zk = ZK(device['ip'], port=device['port'], password=device['password'])
        conn = None  # Initialize `conn`

        try:
            # Connect to the device
            conn = zk.connect()

            # Disable the device to prevent new inputs while fetching attendance data
            conn.disable_device()

            # Retrieve attendance logs
            attendance = conn.get_attendance()

            # Process and collect attendance records within the specified date/time range
            for record in attendance:
                # Apply user_id filter if provided
                if user_id is None or record.user_id == user_id:
                    record_time = record.timestamp
                    if start_date <= record_time <= end_date:
                        attendance_data.append({
                            "device_ip": device['ip'],  # Include device IP
                            "user_id": record.user_id,
                            "timestamp": record_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "status": record.status
                        })

            # Re-enable the device after data retrieval
            conn.enable_device()

        except Exception as e:
            return {"error": f"Error with device {device['ip']}: {str(e)}"}

        finally:
            if conn:
                conn.disconnect()

    return attendance_data


# API endpoint for attendance data
@app.route('/attendance', methods=['GET'])
def attendance():
    # Get query parameters for start_date, end_date, and user_id
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    user_id_str = request.args.get('user_id')

    # Log the incoming parameters for testing
    print(f"Received Parameters - Start Date: {start_date_str}, End Date: {end_date_str}, User ID: {user_id_str}")

    # Check for missing parameters
    if not start_date_str or not end_date_str:
        return jsonify({"error": "Please provide both 'start_date' and 'end_date' query parameters."}), 400

    # Convert input strings to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

    attendance_records = get_attendance_data(start_date, end_date, user_id_str)

    if "error" in attendance_records:
        return jsonify({"error": attendance_records["error"]}), 500

    return jsonify({"attendance_records": attendance_records})


if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
