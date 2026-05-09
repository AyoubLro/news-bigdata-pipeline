from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8")
)

def send_article(article):
    producer.send("news_topic", article)
    producer.flush()