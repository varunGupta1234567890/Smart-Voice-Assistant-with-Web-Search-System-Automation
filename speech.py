import speech_recognition as sr


def clean_command(command):

    command = command.lower()

    # 🔥 unwanted filler words remove
    fillers = ["please", "jarvis", "hey", "can you", "could you"]
    for word in fillers:
        command = command.replace(word, "")

    # 🔥 common mistakes correction
    corrections = {
        "plane": "play",
        "songg": "song",
        "opne": "open",
        "yotube": "youtube",
        "gogle": "google",
        "musix": "music"
    }

    for wrong, correct in corrections.items():
        if wrong in command:
            command = command.replace(wrong, correct)

    return command.strip()


def take_command():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("🎤 Listening...")

        # 🔥 Noise calibration (better accuracy)
        r.adjust_for_ambient_noise(source, duration=1)

        # 🔥 Sensitivity tuning
        r.energy_threshold = 300      # adjust if needed
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

        # 🔥 CLEAN + FIX TEXT
        command = clean_command(command)

        print("You said:", command)

        # 🔥 Ignore very short noise inputs
        if len(command.split()) < 2:
            return ""

        return command

    except sr.UnknownValueError:
        print("❌ Not understood, speak again")
        return ""

    except sr.RequestError:
        print("❌ Network issue")
        return ""