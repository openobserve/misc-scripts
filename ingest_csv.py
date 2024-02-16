import pandas as pd
import requests
import os
from requests.auth import HTTPBasicAuth

# Define the endpoint URL
ENDPOINT_URL = "http://your-http-endpoint.com/data"

# List of CSV file paths
csv_files = ["./csv/1_7feb.csv", "./csv/2_7feb.csv", "./csv/3_7feb.csv", "./csv/4_7feb.csv", "./csv/5_7feb.csv", "./csv/1_7feb.csv", "./csv/6_7feb.csv", "./csv/7_7feb.csv", ]  # Add your file paths here

def send_batch_to_endpoint(batch_data):
    """
    Send a batch of data to the HTTP endpoint.
    
    :param batch_data: List of dictionaries representing the rows to send
    """
    ENDPOINT_URL = "https://api.openobserve.ai/api/trendit1_qT2ghgBwyF7wPKe/atm1/_json"
    USERNAME = "prabhat@openobserve.ai"
    PASSWORD = "21Z7E495SI3G8Ag60pCf"
    try:
        # Include the auth parameter in the post request
        response = requests.post(
            ENDPOINT_URL,
            json=batch_data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        print(f"Batch sent successfully. Response status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def process_csv_files(file_list):
    """
    Process each CSV file and send records in batches of 100 to the endpoint.
    
    :param file_list: List of CSV file paths
    """
    for file in file_list:
        if not os.path.isfile(file):
            print(f"File not found: {file}")
            continue

        print(f"Processing file: {file}")

        # Read CSV file in chunks
        for chunk in pd.read_csv(file, chunksize=50):
            records = chunk.to_dict(orient='records')
            send_batch_to_endpoint(records)

# Run the script to process CSV files and send data to the endpoint
process_csv_files(csv_files)

