import base64
import json
import requests
from google.cloud import bigquery
from google.oauth2 import service_account

# Replace with your credentials file path
credentials_path = "path/to/your/service-account-file.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# BigQuery configuration
bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
dataset_id = "your_bigquery_dataset_id"
table_id = "your_bigquery_table_id"
table_ref = bigquery_client.dataset(dataset_id).table(table_id)

# Instakart API endpoint
instakart_api_url = "https://api.instakart.com/order"

# Item threshold weights (example data)
threshold_weights = {
    "item1": 10.0,
    "item2": 5.0,
    "item3": 7.5,
}

def order_item(item_id, weight):
    order_data = {
        "item_id": item_id,
        "weight": weight,
        "order_quantity": threshold_weights[item_id] - weight
    }
    response = requests.post(instakart_api_url, json=order_data)
    if response.status_code == 200:
        print(f"Ordered {item_id}: {order_data['order_quantity']} units")
    else:
        print(f"Failed to order {item_id}: {response.content}")

def process_weight_data(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)

    item_id = message_data["item_id"]
    weight = message_data["weight"]

    # Store data in BigQuery
    rows_to_insert = [
        {u"item_id": item_id, u"weight": weight, u"timestamp": context.timestamp}
    ]
    errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
    if errors:
        print(f"Error inserting into BigQuery: {errors}")

    # Check weight against threshold and order if needed
    if weight < threshold_weights[item_id]:
        order_item(item_id, weight)
