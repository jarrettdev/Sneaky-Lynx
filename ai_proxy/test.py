import requests
import json

def test_openai_endpoint(prompt):
    # URL of the endpoint
    url = 'http://localhost:5000/api/openai'

    # Data to be sent in JSON format
    data = {
        'prompt': prompt
    }

    # Headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Sending POST request to the endpoint
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # If request is successful, print the result
    if response.status_code == 200:
        print("Response from server:", response.json())
    else:
        print("Error:", response.status_code)


# Example usage
test_prompt = '{"test":"test"}'
test_openai_endpoint(test_prompt)
