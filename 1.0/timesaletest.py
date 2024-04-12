import requests
import json

# Define the URL of the API endpoint
api_url = "https://api.example.com/your_api_endpoint"

# Define the sample request data
request_data = {
    "requests": [
        {
            "service": "TIMESALE_FUTURES",
            "requestid": "3",
            "command": "SUBS",
            "account": "your_account0",
            "source": "your_source_id",
            "parameters": {
                "keys": "/ES",
                "fields": "0,1,2,3,4"
            }
        },
        {
            "service": "TIMESALE_EQUITY",
            "requestid": "2",
            "command": "SUBS",
            "account": "your_account0",
            "source": "your_source_id",
            "parameters": {
                "keys": "AAPL",
                "fields": "0,1,2,3,4"
            }
        }
    ]
}

# Convert the request data to JSON
json_request_data = json.dumps(request_data)

# Send the POST request to the API
response = requests.post(api_url, data=json_request_data, headers={"Content-Type": "application/json"})

# Check if the request was successful
if response.status_code == 200:
    # Print the API response
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
