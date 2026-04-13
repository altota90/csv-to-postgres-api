import pandas as pd
from io import StringIO
from app.db import get_connection
import re

def clean_column(col):
    col = col.strip().lower()
    col = col.replace(" ", "_")
    col = re.sub(r'[^a-z0-9_]', '', col)
    return col

def map_dtype(dtype):
    if "int" in str(dtype):
        return "INTEGER"
    elif "float" in str (dtype):
        return "FLOAT"
    elif "bool" in str (dtype):
        return "BOOLEAN"
    elif "datetime" in str (dtype):
        return "TIMESTAMP"
    else:
        return "TEXT"

def load_csv_to_postgres(file_path, table_name):
    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(file_path)
    df.columns = [clean_column(col) for col in df.columns]

    # intentar convertir fechas automáticamente
    for col in df.columns:
        if "date" in col or "time" in col:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                pass
    
    # BORRAR tabla
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    # crear tabla con tipos correctos
    columns = ", ".join([
        f'"{col}" {map_dtype(df[col].dtype)}'
        for col in df.columns
    ])

    cursor.execute(f"""
        CREATE TABLE {table_name} (
            {columns}
        );
    """)

    # COPY
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, na_rep='')
    buffer.seek(0)

    cursor.copy_expert(
        f"COPY {table_name} FROM STDIN WITH CSV",
        buffer
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ CSV cargado correctamente")