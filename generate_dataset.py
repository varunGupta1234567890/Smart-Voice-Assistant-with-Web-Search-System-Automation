import random
import pandas as pd

# INTENTS + TEMPLATES

intents = {
    "open_app": [
        "open {app}",
        "launch {app}",
        "start {app}",
        "open {app} app",
        "can you open {app}",
    ],
    "play_music": [
        "play {song}",
        "play music",     
        "play song {song}",
        "play {song} song",
        "play some song",
        "start music",
    ],
    "get_time": [
        "what is the time",
        "tell me time",
        "current time",
        "time now",
    ],
    "search": [
        "what is {topic}",
        "tell me about {topic}",
        "who is {topic}",
        "search about {topic}",
    ],
    "greeting": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "how are you",
        "how was your day",
    ]
}

apps = ["youtube", "google", "instagram", "facebook", "whatsapp", "netflix", "spotify","twitter"]
songs = ["kesariya","Raanjhan","shape of you", "believer", "despacito"]
topics = ["AI", "Narendra Modi", "Elon Musk", "cricket", "India", "space", "black hole"]

data = []

# GENERATE DATA
for intent, patterns in intents.items():
    for _ in range(2000):   # 2000 per intent → 10k+ total
        pattern = random.choice(patterns)

        if "{app}" in pattern:
            command = pattern.replace("{app}", random.choice(apps))

        elif "{song}" in pattern:
            command = pattern.replace("{song}", random.choice(songs))

        elif "{topic}" in pattern:
            command = pattern.replace("{topic}", random.choice(topics))

        else:
            command = pattern

        data.append([command, intent])

# SAVE CSV
df = pd.DataFrame(data, columns=["command", "intent"])
df.to_csv("voice_assistant_dataset_10000.csv", index=False)

print("Dataset generated: 10,000+ commands")