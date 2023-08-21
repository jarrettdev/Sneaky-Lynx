from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')


# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains
CORS(app)


# Initialize OpenAI API
openai.api_key = openai_api_key

meta_to_json_prompt = None
system_prompt = None

with open('system-prompt.txt', 'r') as f:
    system_prompt_input = f.read()

with open('meta-to-json.txt', 'r') as f:
    meta_to_json_prompt = f.read()


def gpt_request(prompt, max_retries=5, model='gpt-3.5-turbo'):
    # system_prompt = {"role": "system", "content": f"{system_prompt_input}"}
    chat_prompt = {"role": "user", "content": f"{prompt}"}
    print(f'Processing request: {prompt}')
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                        chat_prompt,
                    ]
            )
            return response.choices[0].message.content.strip()
        except Exception:
            print(f"Rate limit error while processing request")
            retries += 1
            time.sleep(2 ** retries)  # exponential backoff
    print(f"Max retries exceeded while processing request")
    return ""

# Define the OpenAI endpoint
@app.route('/api/openai', methods=['POST'])
def openai_endpoint():
    # Get the prompt from the request body
    prompt = request.json['prompt']
    prompt = f'{meta_to_json_prompt}\n\n{prompt}'

    response = gpt_request(prompt)

    return jsonify({"result": response})


if __name__ == '__main__':
    app.run(port=5000)
