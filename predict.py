import pickle
import re

# load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


# 🔥 CLEAN TEXT
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return text


# 🔥 HINGLISH NORMALIZATION
def normalize_text(text):
    text = text.lower()

    replacements = {
        "khol": "open",
        "kholo": "open",
        "chala": "open",
        "jaldi": "open",
        "khol do": "open",
        "chalao": "play",
        "bajao": "play",
        "chala do": "play",
        "samay": "time",
        "time kya hai": "time",
        "kitna": "time",
        "gaana": "music",
        "gana": "music",
        "app": "",
        "please": "",
        "bhai": "",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


# 🔥 FINAL PREDICT FUNCTION
def predict_intent(text):
    text = normalize_text(text)   # 👈 NEW
    text = clean_text(text)

    vec = vectorizer.transform([text])
    return model.predict(vec)[0]