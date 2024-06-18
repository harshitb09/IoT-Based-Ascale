import time
import random
import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account

# Replace with your credentials file path
credentials_path = "path/to/your/service-account-file.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Pub/Sub configuration
project_id = "your-google-cloud-project-id"
topic_id = "your-pubsub-topic-id"

publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_id)

# Item threshold weights (example data)
threshold_weights = {
    "item1": 10.0,
    "item2": 5.0,
    "item3": 7.5,
}

def publish_weight_data(item_id, weight):
    message_data = {
        "item_id": item_id,
        "weight": weight,
    }
    message_json = json.dumps(message_data)
    message_bytes = message_json.encode("utf-8")
    publisher.publish(topic_path, data=message_bytes)
    print(f"Published data: {message_json}")

def simulate_device():
    while True:
        for item_id in threshold_weights:
            weight = random.uniform(0, threshold_weights[item_id] + 5)  # Simulating weight measurement
            publish_weight_data(item_id, weight)
        time.sleep(10)  # Delay between measurements

if __name__ == "__main__":
    simulate_device()
