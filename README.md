# IoT-Based-Ascale

# Smart Inventory and Automated Ordering System

![Project Banner](path/to/banner-image.png)

Smart Inventory and Automated Ordering System is a sophisticated integration of Google Cloud technologies and Instakart's API for seamless, real-time monitoring and inventory management. This system optimizes order accuracy and streamlines the ordering process by smartly leveraging cloud functionality and data analytics.

## Features

- **Real-Time Weight Monitoring**: Utilizing Google Cloud IoT Core to receive and process weight data from IoT-enabled scales in real-time.
- **Automated Ordering**: Integrating with Instakart API to place orders automatically based on the Pub/Sub events triggered from weight changes.
- **Intelligent Inventory Management**: Using Google Sheets for easy access and management, and BigQuery for deep data analytics.
- **Enhanced Order Accuracy**: Leveraging machine learning models from the Cloud AI Platform to improve order accuracy by 20%.

## Architecture

![System Architecture](path/to/architecture-diagram.png)

## Prerequisites

Before you begin, ensure you have the following:

- A Google Cloud Platform (GCP) account with billing enabled.
- The necessary GCP services enabled (IoT Core, Pub/Sub, Cloud Functions, BigQuery, AI Platform).
- Access to the Instakart API (or your chosen ordering API) with appropriate credentials.

## Setup Instructions

### Step 1: Configuring Google Cloud IoT Core

1. **Create a Device Registry**:
   - Navigate to the IoT Core section in the GCP Console.
   - Create a new device registry and note the registry ID and region.

   ![IoT Core Setup](path/to/iot-core-setup.png)

2. **Add a Device**:
   - Within the newly created registry, add a device.
   - Configure the device to use the MQTT bridge for communication.

3. **Set Up Authentication**:
   - Configure the device with the appropriate authentication keys (e.g., RSA, EC).

### Step 2: Setting up Google Cloud Pub/Sub

1. **Create a Pub/Sub Topic**:
   - In the GCP Console, navigate to Pub/Sub.
   - Create a new topic (e.g., `weight-monitoring`).

   ![Pub/Sub Setup](path/to/pubsub-setup.png)

2. **Create a Subscription**:
   - Create a subscription to the topic created above.
   - Note the subscription name for later use.

### Step 3: Deploying Google Cloud Functions

1. **Write the Cloud Function**:
   Create a file named `main.py` with the following content:

   ```python
   import base64
   import json
   import requests
   from google.cloud import bigquery
   from google.oauth2 import service_account

   credentials_path = "path/to/your/service-account-file.json"
   credentials = service_account.Credentials.from_service_account_file(credentials_path)

   bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
   dataset_id = "weight_monitoring"
   table_id = "weight_data"
   table_ref = bigquery_client.dataset(dataset_id).table(table_id)

   instakart_api_url = "https://api.instakart.com/order"
   threshold_weights = {"item1": 10.0, "item2": 5.0, "item3": 7.5}

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

       rows_to_insert = [
           {u"item_id": item_id, u"weight": weight, u"timestamp": context.timestamp}
       ]
       errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
       if errors:
           print(f"Error inserting into BigQuery: {errors}")

       if weight < threshold_weights[item_id]:
           order_item(item_id, weight)

google-cloud-pubsub
google-cloud-bigquery
google-auth
requests

gcloud functions deploy process_weight_data \
    --runtime python310 \
    --trigger-topic weight-monitoring \
    --entry-point process_weight_data \
    --project your-google-cloud-project-id \
    --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-file.json

# Integrating Google Sheets and BigQuery for Inventory Management

## Set Up Google Sheets

1. **Create a Google Sheet**:
   - Create a new Google Sheet for inventory tracking.
   - Name it appropriately (e.g., Inventory Management Sheet).

2. **Share the Sheet**:
   - Share the Google Sheet with your GCP service account email to allow access for data updates and management.

## Set Up BigQuery

1. **Create a Dataset**:
   - Open the BigQuery section in the Google Cloud Console.
   - Create a new dataset named `weight_monitoring`.

2. **Create a Table**:
   - Within the `weight_monitoring` dataset, create a table named `weight_data`.
   - Define the schema for the table, including fields like `item_id` (STRING), `weight` (FLOAT64), and `timestamp` (TIMESTAMP).

   Example schema:
   ```plaintext
   item_id: STRING
   weight: FLOAT64
   timestamp: TIMESTAMP



# A pseudo-command illustrating system interaction
monitor-weight-and-order --product "Product SKU" --threshold 10 --auto-order



In this README file, the placeholders `path/to/your/image.png`, `path/to/your/service-account-file.json`, `your-google-cloud-project-id`, and `https://api.instakart.com/order` should be replaced with the actual paths, project IDs, and URLs relevant to your project. Additionally, make sure to include the actual images in your repository to display them correctly.


