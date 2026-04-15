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

    # 📌 Filters (asset system)
    site = request.args.get("site")
    team = request.args.get("team")
    department = request.args.get("department")
    manufacturer = request.args.get("manufacturer")
    model = request.args.get("model")
    asset_id = request.args.get("asset_id")
    available = request.args.get("available_for_work_orders")

# 📌 Build query dynamically
    # =========================
    query = "SELECT * FROM mi_tabla"
    conditions = []
    params = []

    if site:
        conditions.append("site = %s")
        params.append(site)

    if team:
        conditions.append("team = %s")
        params.append(team)

    if department:
        conditions.append("department = %s")
        params.append(department)

    if manufacturer:
        conditions.append("manufacturer = %s")
        params.append(manufacturer)

    if model:
        conditions.append("model = %s")
        params.append(model)

    if asset_id:
        conditions.append("asset_id = %s")
        params.append(asset_id)

    if available:
        conditions.append("available_for_work_orders = %s")
        params.append(available)

    # =========================
    # 📌 WHERE clause
    # =========================
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # =========================
    # 📌 Pagination
    # =========================
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    # 📌 Execute query
    cursor.execute(query, params)

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    # 📌 Response
    return jsonify({
        "page": page,
        "limit": limit,
        "filters": {
            "site": site,
            "team": team,
            "department": department,
            "manufacturer": manufacturer,
            "model": model,
            "asset_id": asset_id,
            "available_for_work_orders": available
        },
        "count": len(data),
        "data": data
    })