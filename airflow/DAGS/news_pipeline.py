from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_PATH = "/opt/airflow/news_project"

with DAG(
    dag_id="news_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False
) as dag:

    scraping = BashOperator(
        task_id="scraping",
        bash_command=f"cd {PROJECT_PATH} && python -m scraper.main_scraper"
    )

    cleaning = BashOperator(
        task_id="cleaning",
        bash_command=f"cd {PROJECT_PATH} && python -m processing.clean"
    )

    analysis = BashOperator(
        task_id="analysis",
        bash_command=f"cd {PROJECT_PATH} && python -m processing.analysis"
    )

    database = BashOperator(
        task_id="database",
        bash_command=f"cd {PROJECT_PATH} && python db/database.py"
    )

    scraping >> cleaning >> analysis >> database