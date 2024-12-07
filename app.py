from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database (or replace with another storage system)
conn = sqlite3.connect("uuids.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS runs (uuid TEXT UNIQUE)")


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
    unique_id = data.get("unique_id")

    # Store the UUID in the database
    try:
        cursor.execute("INSERT INTO runs (uuid) VALUES (?)", (unique_id,))
        conn.commit()
        return jsonify({"status": "success", "message": "UUID logged"}), 200
    except sqlite3.IntegrityError:  # Prevent duplicate UUIDs
        return jsonify({"status": "duplicate", "message": "UUID already exists"}), 200

if __name__ == "__main__":
    app.run(debug=True)
