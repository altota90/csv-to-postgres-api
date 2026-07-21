from app.csv_loader import load_csv_to_postgres

if __name__ == "__main__":
    load_csv_to_postgres("data/datos.csv", "mi_tabla")