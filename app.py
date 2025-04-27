from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import time

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Enhanced FAQ Database
faq_db = {
    "admission": {
        "keywords": ["admission", "apply", "requirements", "eligibility", "how to join"],
        "answer": "📌 <b>Admission Requirements:</b><br>1. High school diploma<br>2. Online application form<br>3. $50 application fee<br><br>🔗 <a href='https://university.edu/admissions' class='text-blue-500 hover:underline'>Apply here</a>",
        "quick_reply": ["How to apply?", "Eligibility criteria?"]
    },
    "deadline": {
        "keywords": ["deadline", "last date", "application due", "when to apply"],
        "answer": "⏰ The admission deadline is <b>August 30, 2024</b>. Late applications may not be accepted.",
        "quick_reply": ["Application deadline?", "Last date to apply?"]
    },
    "courses": {
        "keywords": ["courses", "programs", "majors", "degrees"],
        "answer": "🎓 <b>Available Programs:</b><br>- Computer Science<br>- Business Administration<br>- Engineering<br>- Arts<br><br>🔗 <a href='https://university.edu/courses' class='text-blue-500 hover:underline'>Browse all courses</a>",
        "quick_reply": ["List of programs", "What degrees do you offer?"]
    },
    "default": {
        "answer": "❓ I couldn't understand your query. Please contact <b>student support</b> at support@university.edu or try these options:",
        "quick_reply": ["Admission", "Courses", "Fees"]
    }
}

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

def get_response(user_input):
    tokens = preprocess_text(user_input)
    best_match = None
    max_score = 0

    for intent, data in faq_db.items():
        if intent == "default":
            continue
        score = sum(token in data["keywords"] for token in tokens)
        if score > max_score:
            max_score = score
            best_match = intent

    if best_match and max_score > 0:
        return {
            "answer": faq_db[best_match]["answer"],
            "quick_replies": faq_db[best_match].get("quick_reply", [])
        }
    else:
        return {
            "answer": faq_db["default"]["answer"],
            "quick_replies": faq_db["default"]["quick_reply"]
        }

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/get_response", methods=["POST"])
def api_response():
    user_input = request.json["user_input"]
    time.sleep(1)  # Simulate processing delay
    return jsonify(get_response(user_input))

if __name__ == "__main__":
    app.run(debug=True)