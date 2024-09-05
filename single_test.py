import requests

# Define the URL for the endpoint
url = 'http://localhost:4000/execute'

# Define the script to be sent
data = {
    "script": """
import pandas
def main():
    return {"message": "Hello, World!"}
"""
}

# Make the POST request
response = requests.post(url, json=data)

# Print the status code and response data
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
