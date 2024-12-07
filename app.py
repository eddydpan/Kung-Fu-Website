from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database (or replace with another storage system)
conn = sqlite3.connect("device_fingerprints.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS runs (device_fingerprint TEXT UNIQUE)")


@app.route("/")
def index():
    table_name = 'runs'
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    
    # cursor.close()
    # conn.close()
    return f"Number of users who have run KFPM: {row_count}"


@app.route("/log", methods=["POST"])
def log_uuid():
    data = request.json
    device_fingerprint = data.get("device_fingerprint")

    # Store the UUID in the database
    try:
        cursor.execute("INSERT INTO runs (device_fingerprint) VALUES (?)", (device_fingerprint,))
        conn.commit()
        return jsonify({"status": "success", "message": "Device fingerprint logged"}), 200
    except sqlite3.IntegrityError:  # Prevent duplicate UUIDs
        return jsonify({"status": "duplicate", "message": "Device fingerprint already exists"}), 200

if __name__ == "__main__":
    app.run(debug=True)
