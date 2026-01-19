from textblob import TextBlob

# -------- Grievance Category Detection --------
def classify_grievance(text):
    text = text.lower()
    if "ragging" in text or "harassment" in text:
        return "Discipline"
    elif "hostel" in text:
        return "Hostel"
    elif "exam" in text or "result" in text:
        return "Examination"
    elif "library" in text:
        return "Library"
    elif "fee" in text:
        return "Accounts"
    else:
        return "General"

# -------- Priority Detection --------
def detect_priority(text):
    urgent_words = ["urgent", "immediately", "danger", "harassment", "emergency"]
    if any(word in text.lower() for word in urgent_words):
        return "High"
    elif "not working" in text.lower() or "problem" in text.lower():
        return "Medium"
    else:
        return "Low"

# -------- Sentiment Analysis --------
def sentiment_analysis(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.1:
        return "Negative"
    elif polarity > 0.1:
        return "Positive"
    else:
        return "Neutral"
