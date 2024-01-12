import pyarrow.parquet as pq
import requests
import datetime
import json
import uuid
import os
import sys

# Define the endpoint URL and authorization header
endpoint_url = "http://localhost:5080/api/default/optimized/_multi"
authorization_header = "Basic cm9vdEBleGFtcGxlLmNvbTpDb21wbGV4cGFzcyMxMjM="

# Read each file in logs folder and print its name in python

logs_path = sys.argv[1]
# print(logs_path)
# entries = os.listdir(logs_path)
# print(entries)



for root, dirs, files in os.walk(logs_path):
    for name in files:
        file = os.path.join(root, name)
        print(f'Sending file {file}')

        logs = pq.read_table(file)
        df = logs.to_pandas()

        # Delete _timestamp field from dataframe
        del df['_timestamp']
        df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]

        # Chunk the dataframe
        CHUNK_SIZE = 10000
        num_chunks = len(df) // CHUNK_SIZE + (1 if len(df) % CHUNK_SIZE else 0)

        for chunk_num in range(num_chunks):
            start_index = chunk_num * CHUNK_SIZE
            end_index = start_index + CHUNK_SIZE

            chunk = df.iloc[start_index:end_index]

            # Convert dataframe chunk to JSON and remove unicode characters
            data = chunk.to_json(orient='records', lines=True, force_ascii=False)

            headers = {
                "Authorization": authorization_header,
                "Content-Type": "application/json",
            }

            try:
                # print(f'Sending chunk {chunk_num + 1}...')
                response = requests.post(
                    endpoint_url, headers=headers, data=data.encode('utf-8'), timeout=600
                )
                response.raise_for_status()
                # print('Success')
            except requests.exceptions.HTTPError as errh:
                print("HTTP Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("Something went wrong:", err)
            except Exception as e:
                print(f"Error: {str(e)}")
