import os
from flask import Flask, request, jsonify, send_from_directory
from google import genai

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

# Gemini API client
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    prompt = f"""
You are WomenSahay, a simple Tamil-language assistant for women
who have little or no digital experience.

The current demo focuses on PM Ujjwala Yojana.

User message:
{user_message}

Answer in very simple Tamil.
Do not use complicated technical words.
Give practical step-by-step guidance.
Do not claim that WomenSahay itself is a government service.

If the user asks about eligibility, documents, or applying,
tell them to verify the latest requirements on the official
government website.

Keep the answer short, clear and useful.
"""

    # Try Gemini first
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    # If Gemini is temporarily unavailable,
    # provide a working fallback response
    except Exception:
        fallback = """
வணக்கம்! 😊

பிரதான் மந்திரி உஜ்வாலா யோஜனா மூலம் எல்பிஜி(LPG) கேஸ் இணைப்பைப்
பெறுவதற்கான வழிகாட்டுதல்:

1. விண்ணப்பதாரர் 18 வயது அல்லது அதற்கு மேற்பட்ட பெண்ணாக இருக்க வேண்டும்.
2. குடும்பத்தில் ஏற்கனவே LPG இணைப்பு இருக்கக்கூடாது.
3. தேவையான ஆவணங்களைத் தயாராக வைத்திருக்க வேண்டும்.
4. தற்போதைய தகுதி மற்றும் தேவையான ஆவணங்களை அதிகாரப்பூர்வ
   அரசு இணையதளத்தில் சரிபார்க்கவும்.

அதிகாரப்பூர்வ இணையதளம்:
https://www.pmuy.gov.in/

மேலும் உதவி வேண்டுமென்றால்:
"ஆவணங்கள்" அல்லது "எப்படி விண்ணப்பிப்பது?" என்று கேளுங்கள். 😊
"""

        return jsonify({
            "reply": fallback
        })


if __name__ == "__main__":
    app.run(debug=True)
    