import os
from flask import Flask, render_template, request, session
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")  # Required for sessions

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        if prompt:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.choices[0].message.content.strip()
                session["history"].append({"prompt": prompt, "response": response_text})
                session.modified = True
            except Exception as e:
                response_text = f"Error: {e}"

    return render_template("index.html", response=response_text, history=session["history"])

if __name__ == "__main__":
    app.run(debug=True)