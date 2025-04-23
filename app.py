import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load your OpenAI API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        if prompt:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                response_text = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                response_text = f"Error: {e}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)