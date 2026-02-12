#  Projet de Migration de Données médicales vers MongoDB avec Docker

##  Auteur

Nicolas Nathanael BAMANIA

##  Contexte de la mission

Un client possède un dataset médical volumineux au format CSV.
Avec l'augmentation des données, les performances et la scalabilité deviennent problematiques.

L'objectif de cette mission est de:

- Migrer les données vers MongoDB;
- Automatiser le processus;
- conteneuriser la soltion avec Docker;
- Garantir la sécurité et la reproductibilité;
- Preparer un futur déploiement cloud(AWS).

---

##  Objectif du projet

- Automatiser la migration CSV → MongoDB
- Optimiser les performances (index, batch insert)
- Mettre en place un système sécurisé (authentification + rôles)
- Conteneuriser la base et le script
- Documenter entièrement la solution

---

##  Technologies utilisées

- Python 3.13
- Pandas
- PyMongo
- MongoDB 7
- Docker
- Docker Compose
- Git/GitHub

---

##  Structure du projet

###  data_project_mongo/
####    data/
#####      healthcare_dataset_clean.csv      # Données nettoyées
####    logs/
#####      migration.log                     # Logs de migration
####    migrate_to_mongo.py                  # Script de migration
####    Dockerfile                           # Image du script
####    docker-compose.yml                   # Orchestration des services
####    requirements.txt                     # Dépendances Python
####    .gitignore                           # Fichiers ignorés
####    README.md                            # Documentation
####    venv/                                # Environnement virtuel (local)

---

##  Schéma de la base de données

###  Base de données : 
- healthcare_db

###  Collection principale :
- patients

###  Exemple de document MongoDB :

 {
  "personal_info": {
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "blood_type": "O+"
  },
  "medical_info": {
    "condition": "Diabetes",
    "medication": "Metformin",
    "test_results": "Stable"
  },
  "administrative_info": {
    "hospital": "Central Hospital",
    "doctor": "Dr Smith",
    "admission": {
      "date": "2024-01-12",
      "type": "Emergency"
    },
    "discharge_date": "2024-01-20",
    "billing_amount": 3200
  },
  "metadata": {
    "source": "CSV migration",
    "migration_date": "2026-02-04"
  }
}

###  Justification du modele :
- Un document = un patient
- Structure imbriquée adaptée à MongoDB
- Pas de jointures necessaires
- Meilleures performances en lecture
- Une seule collection principale pour simplifier l'architechture

###  Fonctionnement du programme
Le script migrate_to_mongo.py:
- Se connecte à MongoDB
- Charge le fichier CSV avec Pandas
- Transforme les lignes en documents JSON
- supprime le contenu existant de la collection
- Insère les données par batch(1000 documents)
- Créé les index necessaires
- Génère des logs de migration

---

##  Securité confidentielle

###  Authentification MongoDB activée 
###  Rôles définis :
- admin
- data engineer
- analyste
- médecin 
###  Vue anonymisée pour les analystes
###  Principe du moindre privilège appliqué
###  Fichier .env non versionné

---

##  Déploiement du projet 

###  Clonage du repository

- Dans bash:
git clone https://github.com/ton_repo.git
cd projet

###  Configuration du fichier .env

####  Création du fichier .env:

MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
MONGO_DB=healthcare_db
MONGO_COLLECTION=patients

###  Lancement la migration

- Dans bash: docker compose up --build

###  Verification la migration

- Dans bash : mongosh -u admin -p admin123 --authenticationDatabase admin
- Puis :      use healthcare_db
              db.patients.countDocuments()

---

##  Performances

###  Insertion par batch(1000 documents)

###  Index créé sur :

- nom
- condition médicale
- hôpital 
- date d'admission

###  Amelioration des temps de requête avec index

---

##  Perspective Cloud(AWS)

###  Possibilité de déploiement via :

- MongoDB Atlas
- Amazon DocumentDB
- Amazon ECS
- Sauvegarde via S3

---

##  Conclusion

###  Ce projet demontre :

- La maitrise de MongoDB
- L'automatisation d'un pipeline de migration
- La conteneurisation via Docker
- la mise en place d'une architechture sécurisée 

###  Il génère une documentation complète et reproductible








