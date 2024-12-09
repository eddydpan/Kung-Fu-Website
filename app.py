from flask import Flask, request, jsonify
from db import get_db, init_app  # Import database functions

app = Flask(__name__)
app.config['DATABASE'] = "device_fingerprints.db"  # Path to the SQLite database

# Initialize database functionality from db.py
init_app(app)


@app.route("/")
def index():
    """Route to display the number of unique device fingerprints."""
    db = get_db()
    query = "SELECT COUNT(*) AS total FROM runs"
    result = db.execute(query).fetchone()
    row_count = result["total"]  # Use column access with sqlite3.Row
    return f"Number of users who have run KFPM: {row_count}"


@app.route("/log", methods=["POST"])
def log_fingerprint():
    """Route to log a new device fingerprint."""
    data = request.json
    device_fingerprint = data.get("device_fingerprint")

    if not device_fingerprint:
        return jsonify({"status": "error", "message": "No fingerprint provided"}), 400

    db = get_db()
    try:
        db.execute(
            "INSERT INTO runs (device_fingerprint) VALUES (?)", (device_fingerprint,)
        )
        db.commit()
        return jsonify({"status": "success", "message": "Device fingerprint logged"}), 200
    except sqlite3.IntegrityError:  # Prevent duplicate entries
        return jsonify({"status": "duplicate", "message": "Device fingerprint already exists"}), 200


if __name__ == "__main__":
    app.run(debug=True)
