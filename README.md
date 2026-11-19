# L'Observatoire Météo

Application Python permettant de collecter les données météorologiques actuelles via l'API externe Open-Meteo, de valider leur structure avec Pydantic, de les stocker durablement dans une base de données SQLite grâce à l'ORM SQLModel, et de les exposer à travers une API REST FastAPI documentée avec Swagger.

## Fonctionnalités

* **Initialisation automatique** : Création automatique de la base SQLite et insertion par défaut de la ville de Saint-Quentin (latitude `49.8489`, longitude `3.2876`) au démarrage.
* **Collecte et Validation** : Interrogation de l'API Open-Meteo à partir des coordonnées stockées en base, avec gestion des erreurs et validation stricte via Pydantic.
* **Persistance ORM** : Enregistrement relationnel des villes et de leurs relevés météorologiques dans SQLite avec SQLModel.
* **API REST & Swagger** : Exposition des relevés, de l'historique et des statistiques avec une interface interactive générée automatiquement.

## Arborescence du projet

```text
observatoire_meteo/
├── db/
│   └── meteo.db         # Base de données SQLite (générée automatiquement)
├── database.py          # Connexion SQLite, création des tables et initialisation de Saint-Quentin
├── models.py            # Modèles ORM SQLModel (tables) et schémas de validation Pydantic
├── pipeline.py          # Script d'ingestion des données météo vers la base
├── main.py              # Application FastAPI et définition des routes
└── README.md            # Documentation du projet
```

## Installation

### 1. Créer et activer un environnement virtuel

Sur Windows :
```bash
python -m venv .venv
.venv\Scripts\activate
```

Sur macOS et Linux :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installer les dépendances

Une fois l'environnement virtuel activé, installez l'ensemble des bibliothèques requises via le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

## Utilisation

### Lancer une collecte depuis le terminal

Exécutez le pipeline pour récupérer la météo actuelle de Saint-Quentin et l'enregistrer en base :

```bash
python pipeline.py
```

### Démarrer le serveur API

Lancez le serveur local Uvicorn :

```bash
uvicorn main:app --reload
```

Ouvrez ensuite votre navigateur sur `http://127.0.0.1:8000` (en HTTP simple) pour explorer et tester l'API via Swagger UI.

## Routes de l'API

| Méthode | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/collecter/{nom}` | Lit les coordonnées de la ville en base, interroge Open-Meteo et enregistre un nouveau relevé. |
| `GET` | `/meteo/{nom}` | Retourne le dernier relevé météorologique enregistré pour la ville demandée. |
| `GET` | `/historique/{nom}` | Retourne la liste complète de tous les relevés enregistrés en base pour la ville. |
| `GET` | `/stats/{nom}` | Calcule le nombre de relevés ainsi que les températures moyenne, minimale et maximale. |

## Route vers Swagger

`/docs`