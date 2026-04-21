from speech import take_command
from predict import predict_intent
from actions import perform_action
from tts import speak
import datetime
import random

def greet_user():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good morning! I am ready to use")
    elif hour < 18:
        speak("Good afternoon! How can I help?")
    else:
        speak("Good evening! I'm listening.")


FILLERS = [
    "Okay",
    "Sure",
    "Got it",
    "Alright",
    "Working on it"
]


print("🤖 AI Voice Assistant Started...")
greet_user()

while True:

    # Voice input
    command = take_command()

    if not command:
        continue

    command = command.lower().strip()
    print("You said:", command)

    if "exit" in command or "stop" in command or "bye" in command:
        speak("Goodbye! Have a nice day.")
        break

    # small human response
    filler = random.choice(FILLERS)
    print("Assistant:", filler)
    speak(filler)

    intent = predict_intent(command)
    print("Intent:", intent)

    response = perform_action(intent, command)
    print("Assistant:", response)

    speak(response)