from googleapiclient.discovery import build
from google.oauth2 import service_account

# Replace with your credentials file path
credentials_path = "path/to/your/service-account-file.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Google Sheets configuration
spreadsheet_id = "your_google_sheets_id"
range_name = "Sheet1!A1"

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# Function to update Google Sheets
def update_google_sheets(data):
    values = [
        ["Item ID", "Weight", "Timestamp"],
    ] + data

    body = {
        'values': values
    }

    result = sheet.values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")

# Fetch data from BigQuery and update Google Sheets
query = f"SELECT * FROM `{dataset_id}.{table_id}`"
query_job = bigquery_client.query(query)

data = []
for row in query_job:
    data.append([row["item_id"], row["weight"], row["timestamp"]])

update_google_sheets(data)
