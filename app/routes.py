from flask import Blueprint, request, jsonify
from app.csv_loader import load_csv_to_postgres

bp = Blueprint("main", __name__)

@bp.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    file_path = f"data/{file.filename}"
    file.save(file_path)

    load_csv_to_postgres(file_path, "mi_tabla")

    return jsonify({"message": "CSV cargado correctamente"})