import speech_recognition as sr
import re

def clean_command(command):

    command = command.lower()

    fillers = ["please", "jarvis", "hey", "can you", "could you"]
    for word in fillers:
        command = command.replace(word, "")

    corrections = {
        "plane": "play",
        "songg": "song",
        "opne": "open",
        "yotube": "youtube",
        "gogle": "google",
        "musix": "music",
        "kholo": "open",
        "chalao": "play",
        "gaana": "song"
    }

    for wrong, correct in corrections.items():
        if wrong in command:
            command = command.replace(wrong, correct)
    command = re.sub(r"\s+", " ",command).strip()
    return command


def take_command():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("🎤 Listening...")

        r.adjust_for_ambient_noise(source, duration=1)
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8       # wait before ending sentence

        try:
            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )
        except:
            return ""

    try:
        command = r.recognize_google(audio, language="en-IN")

        command = clean_command(command)

        print("You said:", command)

        if len(command.split()) < 2:
            return ""

        return command

    except sr.UnknownValueError:
        print("❌ Not understood, speak again")
        return ""

    except sr.RequestError:
        print("❌ Network issue")
        return ""