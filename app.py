from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
import os

app = Flask(__name__)
CORS(app)

# Initialize Gradio client for the new space
client = Client("HagarEQAP99/AGRI_AGENT")

@app.route('/handle_analysis', methods=['POST'])
def handle_analysis():
    try:
        data = request.get_json()
        image = data.get("image")

        if not image:
            return jsonify({"error": "Missing image parameter"}), 400

        # Handle image input (assuming URL is provided as per API docs)
        result = client.predict(
            image=handle_file(image),
            api_name="/handle_analysis"
        )

        # Return both outputs as specified in the API documentation
        return jsonify({
            "result": result[0],  # Output for "🔍 النتيجة" Textbox
            "assistant": result[1]  # Output for "🧠 مساعد" Textbox
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/handle_chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        user_input = data.get("user_input")
        current_output = data.get("current_output")

        if not user_input or not current_output:
            return jsonify({"error": "Missing user_input or current_output"}), 400

        result = client.predict(
            user_input=user_input,
            current_output=current_output,
            api_name="/handle_chat"
        )

        # Return the single output as specified in the API documentation
        return jsonify({"assistant": result})  # Output for "🧠 مساعد" Textbox

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)