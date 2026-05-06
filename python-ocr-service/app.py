"""
Smart Library — Python OCR Service  (v5 — FIXED)
─────────────────────────────────────────────────
Routes:
  POST /process-image  ← frontend sends shelf photo
  GET  /health         ← frontend health check

Changes from v4:
  - CORS properly configured (no console errors)
  - Reads from unified `books` table via books.csv (book_number column)
  - Full-image OCR fallback when YOLO finds 0 boxes
  - Tesseract auto-detects OS path
"""

"""
Smart Library — Python OCR Service + RFID (FINAL v6)
"""

import csv
import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import process_image

app = Flask(__name__)

# ✅ FIX: store full object (NOT only UID)
last_rfid = {}

# ── CORS ─────────────────────────────────────────
CORS(app, resources={r"/*": {"origins": "*"}},
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "OPTIONS"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── SUBJECT MAP ──────────────────────────────────
SUBJECT_MAP = {
    "Mathematics": ("Rack-1", "A1"),
    "Physics": ("Rack-2", "A2"),
    "Chemistry (B.Sc)": ("Rack-3", "A3"),
    "Computer Engineering (B.Tech)": ("Rack-5", "B2"),
    "Mechanical Engineering (B.Tech)": ("Rack-6", "B3"),
    "Management (MBA)": ("Rack-9", "C3"),
    "Soft & Technical Skills": ("Rack-10", "D1"),
}

# ── LOAD CSV ─────────────────────────────────────
def load_book_lookup():
    lookup = {}
    here = os.path.dirname(__file__)

    candidates = [
        os.path.join(here, "..", "backend", "books.csv"),
        os.path.join(here, "books.csv"),
    ]

    csv_path = next((p for p in candidates if os.path.exists(p)), None)

    if not csv_path:
        print("❌ books.csv not found")
        return lookup

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if not row or not row[0].strip():
                continue

            uid = row[0].strip().upper()
            book_no = row[1].strip() if len(row) > 1 else ""
            title = row[2].strip() if len(row) > 2 else ""
            author = row[3].strip() if len(row) > 3 else ""
            subject = row[9].strip() if len(row) > 9 else ""

            rack, shelf = SUBJECT_MAP.get(subject, ("Rack-1", "A1"))

            lookup[uid] = {
                "bookNumber": book_no,
                "title": title,
                "author": author,
                "subject": subject,
                "rack": rack,
                "expectedShelf": shelf,
            }

    print(f"✅ Loaded {len(lookup)} books")
    return lookup


BOOK_LOOKUP = load_book_lookup()

# ── OCR ROUTE ────────────────────────────────────
@app.route("/process-image", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error": "No image file"}), 400

    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = process_image(path, BOOK_LOOKUP)
    return jsonify(result)

# ── HEALTH ───────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "books_loaded": len(BOOK_LOOKUP)
    })

# ── RFID MAIN ────────────────────────────────────
@app.route("/rfid", methods=["POST"])
def receive_rfid():
    global last_rfid

    data = request.json
    uid = (data.get("uid") or "").upper()

    print("📡 RFID:", uid)

    if uid in BOOK_LOOKUP:
        book = BOOK_LOOKUP[uid]

        last_rfid = {
            "status": "found",
            "uid": uid,
            "book": book
        }

        print("✅ Found:", book["title"])

        return jsonify(last_rfid)

    else:
        last_rfid = {
            "status": "not_found",
            "uid": uid
        }

        print("❌ Unknown")

        return jsonify(last_rfid)

# ── 🔥 FIXED FRONTEND API ────────────────────────
@app.route("/rfid/latest", methods=["GET"])
def latest():
    return jsonify(last_rfid)

# ── RUN ─────────────────────────────────────────
if __name__ == "__main__":
    print("="*50)
    print("🚀 Smart Library Running")
    print(f"📚 Books: {len(BOOK_LOOKUP)}")
    print("="*50)

    app.run(host="0.0.0.0", port=5001)
