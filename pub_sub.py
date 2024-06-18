from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json

# Replace with your credentials file path
credentials_path = "path/to/your/service-account-file.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Pub/Sub configuration
project_id = "your-google-cloud-project-id"
topic_id = "your-pubsub-topic-id"

publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_id)

message_data = {
    "item_id": "item1",
    "weight": 4.5
}
message_json = json.dumps(message_data)
message_bytes = message_json.encode("utf-8")
publisher.publish(topic_path, data=message_bytes)
print(f"Published data: {message_json}")
