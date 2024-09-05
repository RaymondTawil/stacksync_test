# Secure Python Execution Service

This Flask application provides an API endpoint to securely execute Python scripts provided by users. It checks that the provided script contains a `main()` function, wraps it in a secure execution environment using `nsjail`, and returns the JSON output of the script.

## Features

- **Script Validation:** Ensures that all scripts contain a `main()` function.
- **Secure Execution:** Uses `nsjail` to sandbox script execution, limiting potential security risks.
- **JSON Output:** Expects the `main()` function to return a JSON-compatible dictionary and handles JSON serialization.

## Requirements

- Python 3
- Flask
- nsjail

## Usage
To execute a script, send a POST request to the /execute endpoint with the Python script in the request body. The script must define a main() function that returns a JSON object.

### Example cURL Request
curl -X POST http://0.0.0.0:4000/execute -d '{"script":"def main(): return {\"hello\": \"world\"}"}' -H "Content-Type: application/json"

### Example cURL Request via Python
Or you can use the `single_test.py` to do the request directly via Python

## Responses
- **200 OK:** The script executed successfully. The response body contains the result.
- **400 Bad Request:** The script could not be executed due to missing main() function or other errors.
- **500 Internal Server Error:** Server error during script execution or JSON parsing.

## Run
sudo docker build -t flask_app .

sudo docker run -p 4000:8080 --privileged --rm -it flask_app

once the container in up and running you can run localy `test.py` to run predefined unit tests



