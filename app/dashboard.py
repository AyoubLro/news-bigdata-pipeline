import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="News Dashboard", layout="wide")

st.title("📰 News Trends Analyzer")


# =========================
# LOAD DATA
# =========================
def load_articles():
    conn = sqlite3.connect("news.db")
    df = pd.read_sql_query(
        "SELECT title, url, source, date FROM articles",
        conn
    )
    conn.close()
    return df


def load_json(path):
    if os.path.exists(path):
        return pd.read_json(path)
    return pd.DataFrame()


articles = load_articles()
top_words = load_json("data/gold/top_words.json")
by_source = load_json("data/gold/articles_by_source.json")


# =========================
# FORMAT DATE (🔥 هنا درنا fix)
# =========================
if not articles.empty:
    articles["date"] = pd.to_datetime(
        articles["date"], errors="coerce"
    ).dt.strftime("%d-%m-%Y %H:%M")


# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(articles))
col2.metric("Sources", articles["source"].nunique())
col3.metric("Top Keywords", len(top_words))


# =========================
# CHARTS
# =========================
st.subheader("📊 Articles par source")

if not by_source.empty:
    st.bar_chart(by_source.set_index("source")["count"])


st.subheader("🔥 Top Keywords")

if not top_words.empty:
    st.bar_chart(top_words.set_index("word")["count"])


# =========================
# FILTER
# =========================
st.subheader("📰 Articles")

source_filter = st.selectbox(
    "Filtrer par source",
    ["All"] + sorted(articles["source"].dropna().unique().tolist())
)

if source_filter != "All":
    articles = articles[articles["source"] == source_filter]


# =========================
# TABLE (URL clickable)
# =========================
articles["url"] = articles["url"].fillna("unknown")

st.dataframe(
    articles,
    use_container_width=True,
    column_config={
        "url": st.column_config.LinkColumn("Article URL"),
        "title": "Title",
        "source": "Source",
        "date": "Date"
    }
)