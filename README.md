# News BigData Pipeline

Ce projet est une pipeline Big Data développée en Python pour collecter, nettoyer, stocker et analyser des articles d’actualité provenant de plusieurs sources comme Hespress, Le360, France24 et The Guardian.

## Objectif

L’objectif du projet est de mettre en place une architecture de traitement de données basée sur le modèle Medallion Architecture :

- Bronze : données brutes collectées depuis les sites web
- Silver : données nettoyées et normalisées
- Gold : données analysées et prêtes pour la visualisation

## Technologies utilisées

- Python
- BeautifulSoup
- SQLite
- Apache Airflow
- MinIO
- Streamlit
- Docker Compose

## Structure du projet

```text
news_project/
│
├── scraper/        # Scripts de scraping
├── processing/     # Nettoyage et analyse des données
├── data/           # Données Bronze, Silver et Gold
├── db/             # Base de données SQLite
├── airflow/        # DAG Airflow
├── app/            # Dashboard Streamlit
├── storage/        # Intégration MinIO
├── streaming/      # Producer / Consumer
└── README.md
Exécution

Installer les dépendances :

pip install -r requirements.txt

Lancer le scraping :

python -m scraper.main_scraper

Lancer le nettoyage :

python -m processing.clean

Lancer l’analyse :

python -m processing.analysis

Lancer le dashboard :

streamlit run app/dashboard.py
Auteur

Ayoub Louraoui
