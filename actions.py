import datetime
import webbrowser
import os
import pyautogui
import time
import shutil
import subprocess
from google_search import google_answer
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_async(text):
    short_text = text[:300]
    threading.Thread(target=speak, args=(short_text,), daemon=True).start()


# 🔹 Logger
def log(msg):
    print(f"[LOG] {msg}")


def take_screenshot(delay=2, open_after=True, region=None):
    """
    Advanced Screenshot Function

    Args:
        delay (int): seconds before capture
        open_after (bool): open image after saving
        region (tuple): (x, y, width, height) for partial screenshot
    """

    try:
        print(f"[LOG] Screenshot will be taken in {delay} seconds...")
        time.sleep(delay)

        # 📂 Create Screenshot Folder
        folder = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        os.makedirs(folder, exist_ok=True)

        # 🕒 Unique Filename (Date + Time)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(folder, filename)

        # 📸 Take Screenshot
        if region:
            img = pyautogui.screenshot(region=region)
        else:
            img = pyautogui.screenshot()

        # 💾 Save Image
        img.save(filepath)

        print(f"[SUCCESS] Screenshot saved at:\n{filepath}")

        # 🔓 Open Screenshot
        if open_after:
            os.startfile(filepath)

        return filepath

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

# 🔹 AI trigger keywords
AI_KEYWORDS = ["explain", "write", "tell", "who", "what", "why", "how","when","define","price","weather","top","list"]


def perform_action(intent, command):

    command = command.lower().strip()

    try:
        log(f"Command: {command} | Intent: {intent}")
        if "date" in command:
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            result = f"Today's date is {current_date}"
            speak_async(result)
            return result
        
        browser_keywords = [
    "buy","price","download","install","near","weather","latest","nearest","link"
]

        if any(word in command for word in browser_keywords):
            webbrowser.open(f"https://www.google.com/search?q={command}")
            speak_async("Opening in browser")
            return "Opening in browser"
        
        
        if any(word in command for word in AI_KEYWORDS) or intent == "search":
            result = google_answer(command)

    # ✅ agar answer mil gaya
            if result and len(result.strip())>120 and "No useful" not in result and "Error" not in result:
                speak_async(result)
                return result

    # ❌ nahi mila → Google open
            webbrowser.open(f"https://www.google.com/search?q={command}")
            speak_async("Opening in browser")
            return "Showing results on Google"
        # =========================================================
        # 🕒 2. TIME
        # =========================================================
        if intent == "get_time":
            current_time = datetime.datetime.now().strftime("%H:%M")
            result = f"The time is {current_time}"
            speak_async(result)
            return result
        
        # =========================================================
# 📅 DATE
# =========================================================
        if intent == "get_date":
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            result = f"Today's date is {current_date}"
            speak_async(result)
            return result

        # =========================================================
        # 📸 3. SCREENSHOT
        # =========================================================
        # if "screenshot" in command or "screen shot" in command:
        #     log("Taking screenshot...")
        #     time.sleep(2)

        #     desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        #     filename = f"screenshot_{int(time.time())}.png"
        #     filepath = os.path.join(desktop, filename)

        #     img = pyautogui.screenshot(region=(x,y, width ,height))
        #     img.save(filepath)

        #     result = "Screenshot saved on Desktop"
        #     speak_async(result)
        #     return result
        take_screenshot(delay=4,open_after=False,region=(100,200,500,400))

        # =========================================================
        # 🔊 4. VOLUME
        # =========================================================
        if "volume" in command:
            if "up" in command or "increase" in command:
                pyautogui.press("volumeup")
                speak_async("Volume increased")
                return "Volume increased"

            elif "down" in command or "decrease" in command:
                pyautogui.press("volumedown")
                speak_async("Volume decreased")
                return "Volume decreased"

            elif "mute" in command:
                pyautogui.press("volumemute")
                speak_async("Volume muted")
                return "Volume muted"

        # =========================================================
        # 🗺️ 5. MAP
        # =========================================================
        if any(word in command for word in ["map", "location", "near", "direction", "distance"]):

            place = command

    # Clean keywords
            for word in ["map", "location", "show", "find", "near", "direction", "distance"]:
                place = place.replace(word, "")

            place = place.strip()

    # 🧭 Distance / direction handling
            if "from" in command and "to" in command:
                try:
                    parts = command.split("to")
                    source = parts[0].replace("distance", "").replace("from", "").strip()
                    destination = parts[1].strip()

                    url = f"https://www.google.com/maps/dir/{source}/{destination}"
                    webbrowser.open(url)

                    speak_async(f"Showing route from {source} to {destination}")
                    return f"Route from {source} to {destination}"

                except:
                        pass

    # 📍 Normal place search
            if place:
                url = f"https://www.google.com/maps/search/{place}"
            else:
                url = "https://www.google.com/maps"

            webbrowser.open(url)
            speak_async("Opening location on map")
            return "Opening location on map"

        # =========================================================
        # 📷 6. CAMERA
        # =========================================================
        if "camera" in command:
            os.system("start microsoft.windows.camera:")
            speak_async("Starting Camera")
            return "Opening Camera"

        # =========================================================
        # 🌦️ 7. WEATHER
        # =========================================================
        if "weather" in command:
            place = command.replace("weather", "").strip()

            if place:
                url = f"https://www.google.com/search?q=weather {place}"
            else:
                url = "https://www.google.com/search?q=weather"

            webbrowser.open(url)
            speak_async(f"Showing weather {place}" if place else "Showing weather")
            return "Showing weather"
        # =========================================================
        # 🧮 8. CALCULATE
        # =========================================================
        if "calculate" in command:
            query = command.replace("calculate", "").strip()

            if not query:
                speak_async("What should I calculate?")
                return "Please tell me what to calculate"

    # Basic word → symbol conversion
            query = query.replace("plus", "+").replace("minus", "-")
            query = query.replace("into", "*").replace("multiply", "*")
            query = query.replace("divide", "/")

            webbrowser.open(f"https://www.google.com/search?q={query}")

            result = f"Calculating {query}"
            speak_async(result)
            return result

        # =========================================================
        # 📂 9. OPEN FOLDER
        # =========================================================
        if "open folder" in command:
            os.system("explorer .")
            return "Opening folder"

        # =========================================================
        # 🔄 10. SYSTEM UPDATE
        # =========================================================
        if any(word in command for word in ["update", "windows update", "check updates"]):
            os.system("start ms-settings:windowsupdate")
            speak_async("Opening Windows Update")
            return "Opening Windows Update"

        # =========================================================
        # 🌐 11. OPEN APP / WEBSITE
        # =========================================================
        if intent == "open_app":
            if any(word in command for word in ["who","what","why","how","define","explain","best","when","best","price","weather","top","list"]):
                result = google_answer(command)
                if result and len(result.strip())>120 and "No useful" not in result and "Error" not in result:
                    speak_async(result)
                    return result
                else:
                    webbrowser.open(f"https://www.google.com/search?q={command}")
                    return "Showing results on Google"
            app_name = command.replace("open", "").replace("app", "").strip()

            # 🌐 websites
            web_apps = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "instagram": "https://www.instagram.com",
                "netflix": "https://www.netflix.com",
                "amazon": "https://www.amazon.in",
                "flipkart": "https://www.flipkart.com",
                "spotify": "https://open.spotify.com",
                "twitter": "https://twitter.com",
                "facebook": "https://facebook.com"
                
            }

            for app, url in web_apps.items():
                if app in command:
                    webbrowser.open(url)
                    speak_async(f"Opening {app}")
                    return f"Opening {app}"

            # 💻 local apps
            local_apps = {    

    # 📝 Basic
            "notepad": "notepad",
            "calculator": "calc",
            "paint": "mspaint",

    # 🌐 Browser
            "chrome": "start chrome",
            "edge": "start msedge",
            "firefox": "start firefox",

    # 💻 Dev Tools
            "vs code": "code",
            "code": "code",
            "pycharm": "start pycharm64",
            "jupyter": "jupyter notebook",

    # 📂 System
            "cmd": "start cmd",
            "powershell": "start powershell",
            "task manager": "taskmgr",
            "control panel": "control",
            "settings": "start ms-settings:",   

    # 🎵 Media
            "vlc": "start vlc",
            "windows media player": "wmplayer",


    # 📊 MS Office
            "word": "start winword",
            "excel": "start excel",
            "powerpoint": "start powerpnt",
            "outlook": "start outlook",

    # 🎮 Fun / Others
            "camera": "start microsoft.windows.camera:",
            "snipping tool": "snippingtool",
            "calculator app": "calc"
}
            
            for app, cmd in local_apps.items():
                if app in command:
                    os.system(cmd)
                    speak_async(f"Opening {app}")
                    return f"Opening {app}"
            
            if "downloads" in command:
                path = os.path.join(os.path.expanduser("~"), "Downloads")
                subprocess.Popen(f'explorer "{path}"')
                speak_async("Opening Downloads")
                return "Opening Downloads"
            if "documents" in command:
                path = os.path.join(os.path.expanduser("~"), "Documents")
                subprocess.Popen(f'explorer "{path}"')
                speak_async("Opening Documents")
                return "Opening Documents"
            if "desktop" in command:
                path = os.path.join(os.path.expanduser("~"), "Desktop")
                subprocess.Popen(f'explorer "{path}"')
                speak_async("Opening Desktop")
                return "Opening Desktop" 
            if "whatsapp" in command and any(word in command for word in ["open", "start"]):
    
                try:
        # Try opening desktop app
                    os.system("start whatsapp")
                    speak_async("Opening WhatsApp")
                    return "Opening WhatsApp"

                except:
        # Fallback to web
                    webbrowser.open("https://web.whatsapp.com")
                    speak_async("Opening WhatsApp Web")
                    return "Opening WhatsApp Web"

            if "telegram" in command:
                webbrowser.open("https://web.telegram.org")
                speak_async("Opening Telegram")
                return "Opening Telegram"

            if "zoom" in command:
                webbrowser.open("https://zoom.us")
                speak_async("Opening Zoom")
                return "Opening Zoom"
            
            if "code" in command or "vs code" in command:
                os.system("code")
                speak_async("Opening Vs Code")
                return "Opening VS Code"

            # 🧠 safety (random text → browser)
            # if len(app_name.split()) > 2:
            #     webbrowser.open(f"https://www.google.com/search?q={app_name}")
            #     return "Opening in browser"

            # 🔥 final fallback (NO popup)
            try:
                subprocess.Popen(app_name, shell=True)
                return f"Opening {app_name}"
            except:
                webbrowser.open(f"https://www.google.com/search?q={app_name}")
                return f"{app_name} not found, opening in browser"

        # =========================================================
        # 🎵 12. MUSIC
        # =========================================================
        if intent == "play_music":

            song = command.replace("play", "").replace("song", "").strip()

            if not song:
                song = "latest songs"
            query = song.replace(" ", "+")

            log("Opening YouTube...")    

            webbrowser.open(
                f"https://www.youtube.com/results?search_query={query}"
            )
                # Step 2: wait for page load
            time.sleep(3)
            # Step 3: auto play first video
            pyautogui.click(500,400)
            time.sleep(3)
            pyautogui.press("f")

            return f"Playing {song}"

        # =========================================================
        # 💻 13. SYSTEM CONTROL
        # =========================================================
        if intent == "system_control":

            if "shutdown" in command:
                os.system("shutdown /s /t 5")
                return "Shutting down system"

            elif "restart" in command:
                os.system("shutdown /r /t 5")
                return "Restarting system"

            elif "lock" in command:
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "Locking system"

            return "System command not recognized"

        if len(command.split()) >= 5 and intent not in ["open_app", "play_music", "system_control", "volume"]:
            result = google_answer(command)
            if result and len(result.strip())>120 and "No useful" not in result and "Error" not in result:
                speak_async(result)
                return result
            else:
                webbrowser.open(f"https://www.google.com/search?q={command}")
                speak_async("Opening in browser")
                return "Showing results on Google"

        # =========================================================
        log("Fallback AI")
        result = google_answer(command)
        if result and len(result.strip())>120 and "No useful" not in result and "Error" not in result:
            speak_async(result)
            return result
        else:
            webbrowser.open(f"https://www.google.com/search?q={command}")
            speak_async("Opening in browser")
            return "Showing results on Google"

    except Exception as e:
        log(f"Error: {str(e)}")
        return "Something went wrong"