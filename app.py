from flask import Flask, request, jsonify
import json
import subprocess
import os

# Initialize Flask app
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_script():
    # Extract JSON data from request
    data = request.get_json()
    
    # Validate the presence of 'script' in the data
    if not data or 'script' not in data:
        return jsonify({"error": "No script provided"}), 400

    script = data['script']

    # Check if script contains a main() function
    if "def main():" not in script:
        return jsonify({"error": "The script must contain a main() function"}), 400

    script_path = "/app/script.py"

    # Template for the script to execute in a secure environment
    wrapped_script = f"""
import json
import os
import pandas
import numpy

{script}

def run():
    try:
        # Execute the main function and ensure it returns a dictionary
        result = main()
        if not isinstance(result, dict):
            raise ValueError("Execution did not return valid JSON")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({{"error": str(e)}})

if __name__ == "__main__":
    print(run())
"""

    # Write the wrapped script to a file
    with open(script_path, 'w') as f:
        f.write(wrapped_script)

    try:
        # Execute the script in a sandboxed environment
        result = subprocess.run([
            'nsjail',
            '--config', 'nsjail.cfg',
            '--', 'python3', script_path
        ], capture_output=True, text=True, timeout=10)

        # Cleanup by removing the script file
        os.remove(script_path)

        # Handle errors in script execution
        if result.returncode != 0:
            return jsonify({"error": 'Execution failed'}), 400

        if 'Execution did not return valid JSON' in result.stdout:
            return jsonify({"error": "Execution did not return valid JSON"}), 400
        
        # Parse and return output assuming the main() function returns a JSON string
        output = result.stdout.strip()
        return jsonify({"result": json.loads(output)})

    # Handle errors in JSON parsing
    except json.JSONDecodeError:
        return jsonify({"error": "Execution did not return valid JSON"}), 400
    # Handle general exceptions
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask application on specified host and port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
