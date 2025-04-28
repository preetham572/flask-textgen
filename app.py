import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
print("Loaded OpenAI Key:", os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        if prompt:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                response_text = response.choices[0].message.content.strip()
            except Exception as e:
                response_text = f"Error: {e}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)