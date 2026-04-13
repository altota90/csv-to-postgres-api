from app.db import get_connection
from app.config import DB_CONFIG

print(DB_CONFIG)

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT version();")
    version = cursor.fetchone()

    print("✅ Connection successful!")
    print("📊 PostgreSQL version:", version)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)