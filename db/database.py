import sqlite3
import pandas as pd
import glob
import json


# =========================
# DB CONNECTION
# =========================
def create_connection():
    return sqlite3.connect("news.db")


# =========================
# CREATE TABLE
# =========================
def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        url TEXT,
        source TEXT,
        date TEXT
    )
    """)

    conn.commit()


# =========================
# LOAD DATA FROM BRONZE
# =========================
def load_data():
    files = glob.glob("data/bronze/*.json")

    all_data = []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            all_data.extend(json.load(f))

    return pd.DataFrame(all_data)


# =========================
# CLEAN DATA
# =========================
def clean_data(df):

    df.columns = [c.lower() for c in df.columns]

    # fix date column
    if "scraped_at" in df.columns and "date" not in df.columns:
        df["date"] = df["scraped_at"]

    # fill missing values
    df["url"] = df["url"].fillna("unknown")
    df["date"] = df["date"].fillna(pd.Timestamp.now().isoformat())

    # remove invalid rows
    df = df.dropna(subset=["title"])
    df = df[df["title"] != ""]

    # remove duplicates
    df = df.drop_duplicates(subset=["title"])

    # keep needed columns
    df = df[["title", "url", "source", "date"]]

    return df


# =========================
# INSERT INTO SQLITE
# =========================
def insert_data(conn, df):

    cursor = conn.cursor()
    inserted = 0

    for _, row in df.iterrows():

        cursor.execute(
            "SELECT 1 FROM articles WHERE title = ?",
            (row["title"],)
        )

        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                "INSERT INTO articles (title, url, source, date) VALUES (?, ?, ?, ?)",
                (row["title"], row["url"], row["source"], row["date"])
            )
            inserted += 1

    conn.commit()

    print(f"✅ Inserted {inserted} new rows into SQLite")


# =========================
# SHOW SAMPLE DATA
# =========================
def show_data(conn):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, source, date FROM articles ORDER BY id DESC LIMIT 5"
    )

    rows = cursor.fetchall()

    print("\n📊 SAMPLE DATA:")
    print("-" * 50)

    for row in rows:
        print(row)


# =========================
# MAIN PIPELINE
# =========================
if __name__ == "__main__":

    conn = create_connection()

    create_table(conn)

    df = load_data()
    df = clean_data(df)

    insert_data(conn, df)

    show_data(conn)

    conn.close()