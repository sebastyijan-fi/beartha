from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Fetch the OpenAI API key from the environment variables
openai_api_key = os.getenv("OPEN_AI_KEY")   

# Initialize the OpenAI API client
openai.api_key = openai_api_key

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")

    # Call OpenAI API here to get the AI response
    try:
        model_engine = "text-davinci-002"  # You can choose other engines
        response = openai.Completion.create(
            engine=model_engine,
            prompt=user_message,
            max_tokens=100
        )
        ai_message = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"ai_message": ai_message})

if __name__ == "__main__":
    app.run(debug=True)
