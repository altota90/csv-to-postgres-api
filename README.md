# CSV to PostgreSQL Data Pipeline

An automated data ingestion pipeline built with Python that loads CSV files into PostgreSQL with automatic data cleaning, schema creation, and type inference. The project also includes a Flask API for future extensibility.

---

## 🚀 Features

- 📥 Load CSV files into PostgreSQL automatically
- 🧹 Clean and normalize column names
- 🧠 Automatic data type inference (INTEGER, FLOAT, BOOLEAN, TIMESTAMP, TEXT)
- 🗄️ Dynamic table creation
- ⚡ Fast bulk inserts using PostgreSQL COPY
- 🌐 Flask API structure (extensible for file upload and data access)
- 🔐 Environment-based configuration using `.env`

---

## 🏗️ Tech Stack

- Python 3
- Pandas
- Flask
- PostgreSQL
- psycopg2
- python-dotenv

---

## 📁 Project Structure
H:\New_Project
│
├── app/
│ ├── init.py
│ ├── db.py
│ ├── csv_loader.py
│ └── routes.py
│
├── scripts/
│ └── load_csv.py
│
├── data/
│ └── sample.csv
│
├── run.py
├── requirements.txt
└── .env



---

## ⚙️ Setup & Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/csv-to-postgres-api.git
cd csv-to-postgres-api

2. Create virtual environment

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file:
DB_HOST=localhost
DB_NAME=mi_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

▶️ How to Run

python -m scripts.load_csv

🗄️ Database Output

The system will:

Create table automatically
Infer column types
Insert all CSV data

You can verify results in PostgreSQL:

SELECT * FROM mi_table;

📌 Future Improvements

REST API for CSV upload (POST /upload-csv)
Data validation layer
Duplicate handling
Docker support
Cloud deployment (Render / Railway)

🧠 Key Learning Outcomes

Backend data pipeline design
PostgreSQL integration
Schema inference from CSV
Clean architecture with Python modules
Real-world data ingestion workflow

👨‍💻 Author

Built by Alberto Tobarra
Transitioning into Software Engineering & Data Engineering
