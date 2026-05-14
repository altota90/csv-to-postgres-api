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

    try:
        # 📌 Pagination parameters
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        # Prevent invalid values
        page = max(page, 1)
        limit = max(min(limit, 100), 1)  # limit between 1 and 100

        offset = (page - 1) * limit

        # 📌 Available filters
        filters = {
            "site": request.args.get("site"),
            "team": request.args.get("team"),
            "department": request.args.get("department"),
            "manufacturer": request.args.get("manufacturer"),
            "model": request.args.get("model"),
            "asset_id": request.args.get("asset_id"),
            "available_for_work_orders": request.args.get(
                "available_for_work_orders"
            ),
        }

        # 📌 Build query dynamically
        query = "SELECT * FROM mi_tabla"
        conditions = []
        params = []

        for column, value in filters.items():
            if value:
                conditions.append(f"{column} = %s")
                params.append(value)

        # 📌 Add WHERE clause if filters exist
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # 📌 Pagination
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        # 📌 Execute query
        cursor.execute(query, params)

        # Convert rows to list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        # 📌 Count total rows matching filters (for frontend pagination)
        count_query = "SELECT COUNT(*) FROM mi_tabla"
        count_params = params[:-2]  # remove LIMIT and OFFSET

        if conditions:
            count_query += " WHERE " + " AND ".join(conditions)

        cursor.execute(count_query, count_params)
        total_records = cursor.fetchone()[0]

        total_pages = (total_records + limit - 1) // limit

        # Remove empty filters from response
        applied_filters = {
            key: value
            for key, value in filters.items()
            if value is not None and value != ""
        }

        # 📌 JSON response
        return jsonify({
            "success": True,
            "page": page,
            "limit": limit,
            "count": len(data),
            "total_records": total_records,
            "total_pages": total_pages,
            "filters": applied_filters,
            "data": data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# 🔍 Search assets
@routes.route("/search", methods=["GET"])
def search_assets():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 📌 Search query
        q = request.args.get("q")

        if not q:
            return jsonify({
                "success": False,
                "error": "Missing search query parameter 'q'"
            }), 400

        # 📌 Pagination parameters
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=20, type=int)

        # Prevent invalid values
        page = max(page, 1)
        limit = max(min(limit, 100), 1)

        offset = (page - 1) * limit

        # 📌 Search pattern
        pattern = f"%{q}%"

        # Columns to search with ILIKE
        search_columns = [
            "description",
            "model",
            "manufacturer",
            "serial_number",
            "site",
        ]

        # Build WHERE clause dynamically
        conditions = [f"{column} ILIKE %s" for column in search_columns]
        where_clause = " OR ".join(conditions)

        # 📌 Main query
        query = f"""
            SELECT *
            FROM mi_tabla
            WHERE {where_clause}
            LIMIT %s OFFSET %s
        """

        params = [pattern] * len(search_columns)
        params.extend([limit, offset])

        cursor.execute(query, params)

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        # 📌 Count total matches
        count_query = f"""
            SELECT COUNT(*)
            FROM mi_tabla
            WHERE {where_clause}
        """

        count_params = [pattern] * len(search_columns)

        cursor.execute(count_query, count_params)
        total_records = cursor.fetchone()[0]

        total_pages = (total_records + limit - 1) // limit

        # 📌 Response
        return jsonify({
            "success": True,
            "query": q,
            "page": page,
            "limit": limit,
            "count": len(data),
            "total_records": total_records,
            "total_pages": total_pages,
            "data": data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()