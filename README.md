# MTW Medical Asset Management Platform

Originally developed as a CSV-to-PostgreSQL ingestion platform.

The project has evolved into a medical asset management and image
classification system for my hospital.

---

## 🚀 Features

### Data Management

- Import CSV files into PostgreSQL
- Automatic column cleaning
- Automatic data type detection
- Bulk loading using PostgreSQL COPY

### Asset Classification

- Equipment model matching
- Generic Group assignment
- Generic SubType assignment
- Category generation

### Image Management

- Category-based image library
- Automated image search workflow
- Reusable equipment images
- Reduced image requirements from thousands of models to 370 categories

### Future Functionality

- Flask API
- Equipment search
- Asset dashboard
- Reporting

---

# 🏗️ Tech Stack

- Python 3
- Pandas
- Flask
- PostgreSQL
- psycopg2
- python-dotenv
- RapidFuzz (future matching improvements)
---

# 📊 Current Project Status

MTW Assets           : 51,804
Categorised Assets   : 47,354
Coverage             : 91.4%

Image Categories     : 370
Existing Images      : 127+
``
---

# 🏗️ Architecture

datos.csv
     +
model_list.csv
        ↓
model_mapper.py
        ↓
datos_enriched.csv
        ↓
category_analysis.py
        ↓
category_summary.csv
        ↓
build_image_list.py
        ↓
image_download_list.csv
        ↓
image_helper.py
        ↓
images/category/
---




## 📁 Project Structure
New_Project/

app/
├── __init__.py
├── db.py
├── csv_loader.py
└── routes.py

data/
├── datos.csv
├── model_list.csv
├── datos_enriched.csv
├── category_summary.csv
└── image_download_list.csv

images/
└── category/
    ├── bed_electrical.jpg
    ├── infusion_pump.jpg
    ├── thermomtr_electronic.jpg
    └── ...

scripts/
├── load_csv.py
├── model_mapper.py
├── category_analysis.py
├── build_image_list.py
└── image_helper.py

archive/
└── previous experiments

run.py
requirements.txt
.env
README.md


---

## ⚙️ Setup & Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/csv-to-postgres-api.git
cd csv-to-postgres-api

2. Create virtual environment

python -m venv venv

## Activate
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
    ▶️ Workflow
        Step 1 – Enrich Assets
            python scripts/model_mapper.py
            Creates: datos_enriched.csv
        Step 2 – Build Categories
            python scripts/category_analysis.py
            Creates: category_summary.csv
        Step 3 – Build Image Download List
            python scripts/build_image_list.py
            Creates: image_download_list.csv
        Step 4 – Download Images
            python scripts/image_helper.py
            Process:Open image search
                    Download image
                    Save in images/category/
                    Press ENTER
                    Continue


# 🗄️ Database Output

The system progressively enriches and classifies medical assets.

Stage 1 – Asset Enrichment
    Description:
    BD Alaris VP Plus Infusion Pump

    Generic Group:
    INFUSION

    Generic SubType:
    PUMP

Stage 2 – Category Generation
    INFUSION | PUMP
    BED | ELECTRICAL
    THERMOMTR | ELECTRONIC
    HOIST | PATIENT

Stage 3 – Image Library Generation
    BD Alaris VP Plus Infusion Pump
    → infusion_pump.jpg

    Arjo Enterprise 5000 Bed
    → bed_electrical.jpg

Stage 4 – Category Images
    bed_electrical.jpg
    infusion_pump.jpg
    thermomtr_electronic.jpg
    oxygen_concentrator.jpg



PostgreSQL Roadmap
🗄️ Future PostgreSQL IntegrationShow more lines
Explain:
    CSV Files     
        ↓
    PostgreSQL
        ↓
    Asset Classification
        ↓
    Category Images
        ↓
    Flask Web Application

📌 Future Improvements

- Fuzzy matching improvements
- PostgreSQL asset storage
- Image assignment automation
- Flask dashboard
- Asset search interface
- Reporting
- REST API

🧠 Key Learning Outcomes

- Data Engineering
- PostgreSQL Development
- Python Automation
- Medical Asset Management
- Data Classification and Enrichment
- Software Architecture
- Process Automation

👨‍💻 Author

Built by Alberto Tobarra
Transitioning into Transitioning into Software Engineering, Data Engineering and Healthcare Technology.
