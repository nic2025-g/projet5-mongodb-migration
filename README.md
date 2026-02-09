#  Projet de Migration de Données CSV vers MongoDB avec Docker

##  Auteur
Nicolas Nathanael BAMANIA

##  Objectif du projet

Ce projet a pour objectif d’automatiser la migration d’un fichier CSV contenant des données de santé vers une base de données MongoDB, en utilisant Python et Docker.

L’objectif est de garantir :
- Une migration reproductible
- Une bonne gestion des volumes
- Des performances optimisées
- Une traçabilité via des logs

---

##  Technologies utilisées

- Python 3.13
- Pandas
- PyMongo
- MongoDB 7
- Docker
- Docker Compose

---

##  Structure du projet

---

##  Gestion des données

- Le dataset original n’est pas stocké dans le dépôt GitHub pour des raisons de confidentialité et de conformité RGPD.

- Les données sont fournies séparément dans un environnement sécurisé.

---

## Sécurité et confidentialité

- Authentification MongoDB activée

- Rôles utilisateurs définis (admin, analyste, médecin, data engineer)

- Vue anonymisée pour les analystes

- Principe du moindre privilège appliqué

- Fichier .env non versionné

