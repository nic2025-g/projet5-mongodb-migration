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
- L'optimisation par index et les rôles personnalisés sont en fait des améliorations prévues.

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

### Justification du modèle

Chaque document représente une ligne du CSV, correspondant à un
enregistrement d’hospitalisation. Un même patient peut donc apparaître
dans plusieurs documents.

Les informations sont regroupées dans quatre sous-documents :

- `personal_info` : informations personnelles ;
- `medical_info` : condition médicale, médecin et traitement ;
- `administrative_info` : établissement, admission, sortie et facturation ;
- `metadata` : fichier source et date d’import.

Cette organisation permet de consulter les informations d’une
hospitalisation dans un même document, sans jointure.

###  Fonctionnement du programme
Le script migrate_to_mongo.py:
- Se connecte à MongoDB
- Charge le fichier CSV avec Pandas
- Transforme les lignes en documents JSON
- refuse le chargement si la collection contient déjà des documents
- Insère les données par batch(1000 documents)
- vérifie le nombre de documents après insertion
- Génère des logs de migration

---

## Sécurité

- Authentification MongoDB configurée au démarrage.
- Identifiants fournis par des variables d’environnement.
- Fichier `.env` exclu du suivi Git.
- Aucun port MongoDB publié sur Windows.
- CSV monté en lecture seule dans le conteneur de migration.

### Limites

La migration utilise actuellement un compte administrateur.
Un compte limité à la base cible constitue une amélioration prévue.

La création de rôles personnalisés et d’une vue anonymisée
n’est pas automatisée dans cette version.

## Installation et exécution

### Prérequis

- Git
- Docker Desktop avec Docker Compose
- Le fichier `healthcare_dataset_clean.csv`

### 1. Cloner le dépôt

```bash
git clone https://github.com/nic2025-g/projet5-mongodb-migration.git
cd projet5-mongodb-migration
```

Les améliorations décrites ici sont actuellement sur la branche :

```bash
git switch feature/portfolio-improvements
```

### 2. Préparer les données

Placer le CSV nettoyé à cet emplacement :

```text
data/healthcare_dataset_clean.csv
```

### 3. Configurer les identifiants

Créer un fichier `.env` à la racine du projet :

```dotenv
MONGO_USER=migration_admin
MONGO_PASS=REMPLACER_PAR_UN_MOT_DE_PASSE
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=healthcare_portfolio_test
MONGO_COLLECTION=patients
```

Remplacer le mot de passe avant le lancement.
Ne jamais publier le fichier `.env`.

Le script utilise actuellement la collection `patients`
directement dans le code.

### 4. Vérifier la configuration

```bash
docker compose config --quiet
```

### 5. Démarrer MongoDB

```bash
docker compose up -d mongo
docker compose ps
```

Attendre que MongoDB affiche le statut `healthy`.

### 6. Exécuter la migration

```bash
docker compose run --rm --build migration
```

La migration refuse de démarrer si la collection contient déjà
des documents.

### 7. Consulter les journaux sous PowerShell

```powershell
Get-Content .\logs\migration.log -Tail 20 -Encoding UTF8
```

### 8. Arrêter les services

```bash
docker compose down
```

Les données restent conservées dans le volume Docker.
La commande `docker compose down -v` supprime ce volume
et ses données : elle ne doit pas être utilisée pour un arrêt courant.

### Identifiants et volume persistant

Les variables `MONGO_INITDB_ROOT_USERNAME` et
`MONGO_INITDB_ROOT_PASSWORD` servent à initialiser le compte
sur un volume neuf. Modifier ensuite le fichier `.env`
ne change pas le mot de passe du compte déjà créé.

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

## Résultats et vérifications

Tests réalisés le 19 octobre 2026 dans une base de test dédiée.

| Vérification | Résultat |
|---|---|
| Lignes du CSV nettoyé | 54 897 |
| Documents insérés dans MongoDB | 54 897 |
| Taille des lots d’insertion | 1 000 documents |
| Code de sortie après migration réussie | 0 |
| Relance sur une collection déjà remplie | Refus avant insertion, code 1 |

Le script vérifie que le nombre de documents insérés et le nombre
final de documents correspondent au nombre de lignes du CSV.

Il refuse de charger une collection non vide afin de préserver
les données existantes. Il ne réalise pas de déduplication métier.

Les journaux sont conservés localement dans `logs/migration.log`
et ne sont pas versionnés.

### Limites actuelles

- Le CSV et les documents transformés sont chargés entièrement en mémoire.
- Les dates provenant du CSV sont conservées sous forme de chaînes.
- Une erreur pendant le chargement peut laisser une insertion partielle.
- Aucun index métier n’est créé par le script actuel.
- Les performances des requêtes n’ont pas été mesurées.


---

## Conclusion

Ce projet met en œuvre une migration CSV vers MongoDB avec Python
et Docker Compose : transformation en documents imbriqués,
insertion par lots, journalisation et contrôle du nombre de documents.

Les tests ont confirmé l’import de 54 897 documents et le refus
d’un second chargement sur une collection déjà remplie.

Les prochaines améliorations envisagées sont la création d’index
adaptés aux requêtes, un compte de migration aux droits limités,
la validation des données et la lecture du CSV par morceaux.



