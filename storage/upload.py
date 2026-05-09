import json
from datetime import datetime
from io import BytesIO
from storage.minio_client import client

def upload_to_minio(bucket, data):
    filename = f"{bucket}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")

    client.put_object(
        bucket,
        filename,
        data=BytesIO(json_data),
        length=len(json_data),
        content_type="application/json"
    )

    print(f"☁️ Uploaded to {bucket}: {filename}")