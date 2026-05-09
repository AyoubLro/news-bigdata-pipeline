
## 👨‍💻 Auteur

**Ayoub Louraoui **




# 📰 Pipeline de Données News

## 📌 Présentation

Ce projet est un pipeline complet de **Data Engineering** qui collecte des articles d’actualité à partir de plusieurs sources, les traite, puis génère des insights visualisés dans un dashboard.

Le système utilise des outils modernes comme **Kafka, Airflow, MinIO et Streamlit** pour simuler une plateforme de données réelle.

---

## 🏗️ Architecture

```
Scraping → Kafka → Bronze (MinIO) → Cleaning → Silver → Analysis → Gold → Database → Dashboard

```

---

## 🛠️ Technologies utilisées

* **Python**
* **Apache Kafka** (Streaming)
* **Apache Airflow** (Orchestration)
* **MinIO** (Data Lake)
* **Pandas** (Traitement)
* **SQLite** (Stockage)
* **Streamlit** (Visualisation)
* **Docker** (Conteneurisation)

---

## 📊 Sources de données

* Hespress
* Le360
* France24
* The Guardian

---

## 📁 Structure du projet

```
news_project/
│
├── scraper/        # Scripts de scraping
├── streaming/      # Producteur & consommateur Kafka
├── processing/     # Scripts de nettoyage et analyse
├── storage/        # Connexion et upload MinIO
├── db/             # Scripts base de données
├── airflow/        # Pipeline DAG
├── app/            # Dashboard Streamlit
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
```

---

## 🔄 Étapes du pipeline

### 1. Scraping

Collecte des articles depuis plusieurs sites web.

```
python -m scraper.main_scraper

```

---

### 2. Nettoyage (Silver Layer)

Nettoyage et normalisation des données.

```
python -m processing.clean

```

---

### 3. Analyse (Gold Layer)

Génération d’insights comme :

* Mots les plus fréquents
* Articles par source

```
python -m processing.analysis

```

---

### 4. Stockage en base de données

Insertion des données dans SQLite.

```
python db/database.py

```

---

### 5. Dashboard

Visualisation des résultats.

```
streamlit run app/dashboard.py

```

---

## ⚙️ Exécution du projet

### 1. Démarrer les services Docker

```
docker compose up -d

```

---

### 2. Activer l’environnement virtuel

```
venv\Scripts\activate

```

---

### 3. Lancer le pipeline

```
python -m scraper.main_scraper
python -m processing.clean
python -m processing.analysis
python db/database.py
streamlit run app/dashboard.py

```

---

### 4. Accéder aux services

* Airflow: http://localhost:8080
* MinIO: http://localhost:9001
* Dashboard: http://localhost:8501

---

## 🔐 Identifiants par défaut

**Airflow**

* Username: admin
* Password: admin

**MinIO**

* Username: admin
* Password: admin123

---

## 🚀 Fonctionnalités

✔ Streaming de données en temps réel avec Kafka
✔ Architecture Data Lake (Bronze, Silver, Gold)
✔ Orchestration automatisée avec Airflow
✔ Visualisation avec Streamlit
✔ Système scalable et conteneurisé

---
