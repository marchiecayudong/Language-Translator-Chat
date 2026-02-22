from flask import Flask, render_template, request, redirect
from googletrans import Translator
from datetime import datetime

app = Flask(__name__)
translator = Translator()

# In-memory chat history
chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    # Handle POST requests (form submission)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "clear":
            chat_history = []
            return redirect("/")

        text = request.form.get("text", "").strip()
        target_lang = request.form.get("language", "en")
        dark_mode = request.form.get("dark_mode") == "on"

        if text:
            try:
                detected = translator.detect(text)
                translated = translator.translate(text, dest=target_lang)
                chat_history.append({
                    "original": text,
                    "translated": translated.text,
                    "detected": detected.lang,
                    "target": target_lang,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
            except Exception as e:
                chat_history.append({
                    "original": text,
                    "translated": f"Error: {str(e)}",
                    "detected": "Error",
                    "target": target_lang,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
        return redirect("/")

    # GET or HEAD requests just render the page
    return render_template("index.html", history=chat_history)
    
if __name__ == "__main__":
    app.run(debug=True)