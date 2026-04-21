## AI Voice Assistant (ML + NLP Based)
An intelligent voice-controlled assistant built using Python, Machine Learning, and Speech Recognition.
It can understand user commands, predict intent using an ML model, and perform real-world actions like opening apps, searching the web, playing music, and more.

---

# Features

- Voice Input using Speech Recognition
- Intent Classification using Machine Learning (TF-IDF + Naive Bayes / Logistic Regression)
- Text-to-Speech (TTS) response
- Open websites & apps (YouTube, Chrome, VS Code, etc.)
- Play music via YouTube
- Open maps & directions
- Take screenshots
- Control system volume
- Check weather
- Perform calculations
- Smart fallback (Google search if intent not found)

---

# Tech Stack

- Python
- Scikit-learn (ML Model)
- Pandas (Data Handling)
- SpeechRecognition (Voice Input)
- PyAudio (Microphone Access)
- pyttsx3 (Text-to-Speech)
- Webbrowser, OS, Subprocess

---

# Project Structure

ML_voice_assistant/
│
├── app.py                # Main app (UI / Streamlit)
├── speech.py            # Voice input (speech → text)
├── tts.py               # Text-to-speech (text → voice)
├── actions.py           # Perform actions based on intent
├── predict.py           # ML model prediction
├── generate_dataset.py  # Dataset generator
├── google_search.py     # Smart search fallback
│
├── model.pkl            # Trained ML model
├── vectorizer.pkl       # TF-IDF vectorizer
│
├── final_dataset.csv    # Final merged dataset
├── voice.ipynb          # Model training notebook
│
└── README.md

---

# Installation

# 1️. Clone the repository

git clone https://github.com/your-username/AI-Voice-Assistant.git
cd AI-Voice-Assistant

# 2️. Install dependencies

pip install -r requirements.txt

# 3️. Install PyAudio (Important for mic)

pip install pipwin
pipwin install pyaudio

---

# ▶ Run the Project

python app.py

OR (if using Streamlit):

streamlit run app.py

---

# Model Training

Run the notebook:

voice.ipynb

Steps:

1. Load dataset
2. Clean text
3. Train model (TF-IDF + ML)
4. Save model ("model.pkl")
5. Save vectorizer ("vectorizer.pkl")


---

# How it Works

User Voice 
   ↓
speech.py (Speech → Text)
   ↓
predict.py (Intent Classification)
   ↓
actions.py (Execute Task)
   ↓
tts.py (Text → Speech)

---

# Future Improvements

- Wake word detection ("Hey Jarvis")
- Offline speech recognition
- Deep learning model (LSTM / BERT)
- Multi-language support (Hindi + Hinglish)
- GUI improvements

---

# Author

Varun Gupta
Aspiring Data Scientist & AI Developer

---
