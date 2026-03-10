from flask import Flask, render_template, request, redirect
from deep_translator import GoogleTranslator
from datetime import datetime

app = Flask(__name__)

# In-memory chat history
chat_history = []


@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":
        action = request.form.get("action")

        # Clear chat history
        if action == "clear":
            chat_history = []
            return redirect("/")

        text = request.form.get("text", "").strip()
        target_lang = request.form.get("language", "en")

        if text:
            try:
                # Translate using deep-translator
                translated = GoogleTranslator(
                    source="auto",
                    target=target_lang
                ).translate(text)

                chat_history.append({
                    "original": text,
                    "translated": translated,
                    "detected": "auto",
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

    return render_template("index.html", history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
