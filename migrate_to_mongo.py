import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import logging
import os


# ============================
# CONFIG LOG
# ============================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/migration.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("===== DÉBUT MIGRATION =====")


# ============================
# ENV VARIABLES
# ============================

MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "admin123")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_DB   = os.getenv("MONGO_DB", "healthcare_db")



#MONGO_USER = os.getenv("MONGO_USER")
#MONGO_PASS = os.getenv("MONGO_PASS")
#MONGO_HOST = os.getenv("MONGO_HOST")
#MONGO_DB = os.getenv("MONGO_DB")

CSV_FILE = "data/healthcare_dataset_clean.csv"


# ============================
# CONNEXION MONGO
# ============================

uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/?authSource=admin"

client = MongoClient(uri)

db = client[MONGO_DB]
collection = db["patients"]

logging.info("Connexion MongoDB OK")


# ============================
# LECTURE CSV
# ============================

df = pd.read_csv(CSV_FILE)

logging.info(f"CSV chargé : {len(df)} lignes")


# ============================
# TRANSFORMATION
# ============================

documents = []

for _, row in df.iterrows():

    doc = {
        "personal_info": {
            "name": row["Name"],
            "age": row["Age"],
            "gender": row["Gender"],
            "blood_type": row["Blood Type"]
        },

        "medical_info": {
            "condition": row["Medical Condition"],
            "doctor": row["Doctor"],
            "medication": row["Medication"],
            "test_results": row["Test Results"]
        },

        "administrative_info": {
            "hospital": row["Hospital"],
            "room_number": row["Room Number"],

            "admission": {
                "type": row["Admission Type"],
                "date": row["Date of Admission"]
            },

            "discharge": {
                "date": row["Discharge Date"],
                "stay_duration_days": row.get("Stay Duration (Days)", None)
            },

            "insurance_provider": row["Insurance Provider"],
            "billing_amount": row["Billing Amount"]
        },

        "metadata": {
            "source": CSV_FILE,
            "import_date": datetime.now()
        }
    }

    documents.append(doc)


# ============================
# INSERTION PAR LOTS
# ============================

try:

    collection.delete_many({})
    logging.info("Collection vidée")

    BATCH = 1000
    total = len(documents)

    for i in range(0, total, BATCH):

        batch = documents[i:i+BATCH]

        collection.insert_many(batch)

        logging.info(f"Insertion : {i+len(batch)} / {total}")

    logging.info("Migration terminée")

except Exception as e:

    logging.error(f"ERREUR : {e}")

print("Migration terminée ✅")
