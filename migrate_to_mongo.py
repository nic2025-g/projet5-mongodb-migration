import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import logging
import os
import sys


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

client = MongoClient(
    host=MONGO_HOST,
    port=int(os.getenv("MONGO_PORT", "27017")),
    username=MONGO_USER,
    password=MONGO_PASS,
    authSource="admin",
    serverSelectionTimeoutMS=10000
)

db = client[MONGO_DB]
collection = db["patients"]


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
    client.admin.command("ping")
    logging.info("Connexion MongoDB vérifiée")

    existing_count = collection.count_documents({})

    if existing_count > 0:
        raise RuntimeError(
            f"La collection contient déjà {existing_count} documents. "
            "Migration annulée pour préserver les données existantes."
        )

    if not documents:
        raise ValueError("Aucun document à importer.")

    BATCH = 1000
    total = len(documents)
    inserted_count = 0

    for i in range(0, total, BATCH):
        batch = documents[i:i + BATCH]
        result = collection.insert_many(batch)
        inserted_count += len(result.inserted_ids)

        logging.info("Insertion : %s / %s", inserted_count, total)

    final_count = collection.count_documents({})

    if inserted_count != total or final_count != total:
        raise RuntimeError(
            f"Comptage incorrect : {total} attendus, "
            f"{inserted_count} insérés, {final_count} présents."
        )

    logging.info("Migration réussie : %s documents", final_count)
    print(f"Migration réussie : {final_count} documents ✅")

except Exception:
    logging.exception("Échec de la migration")
    print(
        "Migration interrompue. Consultez logs/migration.log. "
        "Une insertion partielle peut avoir eu lieu.",
        file=sys.stderr
    )
    sys.exit(1)

finally:
    client.close()