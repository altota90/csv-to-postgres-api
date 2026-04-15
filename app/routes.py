from flask import Blueprint, request, jsonify
import os
from app.csv_loader import load_csv_to_postgres
from app.db import get_connection

routes = Blueprint("routes", __name__)

UPLOAD_FOLDER = "data"

# 📥 Upload CSV
@routes.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        load_csv_to_postgres(file_path, "mi_tabla")
        return jsonify({"message": "CSV uploaded and loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📊 Get data
@routes.route("/data", methods=["GET"])
def get_data():
    conn = get_connection()
    cursor = conn.cursor()

     # 📌 Get query params (defaults if not provided)
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)

    # 📌 Calculate OFFSET
    offset = (page - 1) * limit

    # 📌 Query with pagination
    query = f"""
        SELECT * FROM mi_tabla
        LIMIT {limit} OFFSET {offset};
    """

    cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "data": data
    })