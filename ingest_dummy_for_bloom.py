import requests
import json
import uuid
import time
import random

# Define the endpoint URL and authorization header
endpoint_url = "http://localhost:5080/api/default/bloom_search/_json"
authorization_header = "Basic cm9vdEBleGFtcGxlLmNvbTpDb21wbGV4cGFzcyMxMjM="

# Function to generate a single data entry

def generate_data_entry():
    operation_list = ["operation_1", "operation_2", "operation_3"]
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    parent_id = str(uuid.uuid4())
    operation_name = random.choice(operation_list)
    start_time = int(time.time())
    duration = random.randint(1, 100)  # Adjust the range as needed

    data_entry = {
        "trace_id": trace_id,
        "span_id": span_id,
        "parent_id": parent_id,
        "operation_name": operation_name,
        "start_time": start_time,
        "duration": duration,
    }

    return data_entry

# Function to send all data entries in a single request


def send_data(data_entries):
    headers = {
        "Authorization": authorization_header,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            endpoint_url, headers=headers, data=json.dumps(data_entries))
        if response.status_code == 200:
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")

# Main function


def main():
    
    start_time = int(time.time())
    
    for i in range(2500):
        # Generate 1000 data entries
        data_entries = [generate_data_entry() for _ in range(10000)]

        # Send all data entries in a single request
        send_data(data_entries)

        print(f"Sent {i+1} requests")

    end_time = int(time.time())
    print(f"Total time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
