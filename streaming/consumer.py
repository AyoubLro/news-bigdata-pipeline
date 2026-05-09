from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "news_topic",
    bootstrap_servers="localhost:29092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("📡 Waiting for articles...")

for msg in consumer:
    print("📰 New article:", msg.value.get("title"))