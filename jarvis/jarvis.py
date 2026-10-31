"""
Jarvis - Ek simple voice assistant aapke apne PC ke liye.

Yeh aapke computer ko handle karta hai aur voice mein status batata hai:
  - CPU, RAM, battery, disk ka status
  - Running programs
  - Apps kholna / band karna
  - Time aur date

Chalane se pehle: pip install -r requirements.txt
Phir:            python jarvis.py

Note: Yeh sirf aapke apne computer par chalane ke liye hai.
"""

import datetime
import os
import platform
import subprocess
import sys

import psutil

try:
    import pyttsx3
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except Exception:  # pragma: no cover - voice libs optional
    VOICE_AVAILABLE = False


# --------------------------------------------------------------------------- #
# Voice engine (bolna aur sunna)
# --------------------------------------------------------------------------- #
class Voice:
    """Text-to-speech aur speech-to-text ka wrapper."""

    def __init__(self):
        self.engine = None
        self.recognizer = None
        if VOICE_AVAILABLE:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 175)
            self.recognizer = sr.Recognizer()

    def say(self, text: str) -> None:
        """Text ko console par likhta hai aur bolta hai."""
        print(f"Jarvis: {text}")
        if self.engine is not None:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self) -> str:
        """Mic se sun kar text return karta hai. Voice na ho to keyboard."""
        if self.recognizer is None:
            return input("Aap: ").strip().lower()

        with sr.Microphone() as source:
            print("Sun raha hoon...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio, language="en-IN")
            print(f"Aap: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.say("Maaf kijiye, samajh nahi aaya.")
            return ""
        except sr.RequestError:
            self.say("Network problem, speech service tak nahi pahunch saka.")
            return ""


# --------------------------------------------------------------------------- #
# PC status helpers
# --------------------------------------------------------------------------- #
def status_report() -> str:
    """Pure PC ka ek line summary banata hai."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/" if os.name != "nt" else "C:\\")

    parts = [
        f"CPU {cpu:.0f} percent use ho raha hai",
        f"RAM {mem.percent:.0f} percent bhari hai",
        f"Disk {disk.percent:.0f} percent full hai",
    ]

    battery = psutil.sensors_battery()
    if battery is not None:
        charging = "charge ho rahi hai" if battery.power_plugged else "battery par chal rahe hain"
        parts.append(f"Battery {battery.percent:.0f} percent hai aur {charging}")

    return ". ".join(parts) + "."


def top_programs(limit: int = 5) -> str:
    """Sabse zyada CPU use karne wale programs."""
    procs = []
    for p in psutil.process_iter(["name", "cpu_percent"]):
        try:
            procs.append((p.info["name"], p.info["cpu_percent"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(key=lambda x: x[1] or 0, reverse=True)
    names = [name for name, _ in procs[:limit] if name]
    if not names:
        return "Abhi koi khaas program nahi chal raha."
    return "Yeh programs chal rahe hain: " + ", ".join(names) + "."


def open_app(name: str) -> str:
    """Naam se app kholne ki koshish karta hai (OS ke hisaab se)."""
    name = name.strip()
    if not name:
        return "Kaunsa app kholna hai, batayein."
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(name)  # type: ignore[attr-defined]
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            subprocess.Popen([name])
        return f"{name} khol raha hoon."
    except Exception:
        return f"Maaf kijiye, {name} nahi khul saka."


def tell_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("Abhi time hai %I:%M %p, %d %B %Y.")


# --------------------------------------------------------------------------- #
# Command router
# --------------------------------------------------------------------------- #
def handle(command: str, voice: Voice) -> bool:
    """Command handle karta hai. False return kare to program band."""
    c = command.lower().strip()
    if not c:
        return True

    if any(w in c for w in ("exit", "quit", "band karo", "bye", "ruk jao")):
        voice.say("Theek hai, main ja raha hoon. Phir milenge!")
        return False

    if "status" in c or "report" in c or "haal" in c:
        voice.say(status_report())
    elif "program" in c or "process" in c or "chal raha" in c:
        voice.say(top_programs())
    elif "time" in c or "samay" in c or "baje" in c or "date" in c or "tareekh" in c:
        voice.say(tell_time())
    elif c.startswith("open ") or c.startswith("kholo ") or "khol do" in c:
        app = c.replace("open", "").replace("kholo", "").replace("khol do", "").strip()
        voice.say(open_app(app))
    elif "hello" in c or "hi" in c or "namaste" in c or "salam" in c:
        voice.say("Namaste! Main Jarvis hoon. Aap PC ka status, programs, ya time pooch sakte hain.")
    else:
        voice.say(
            "Main yeh kaam kar sakta hoon: status batana, running programs, "
            "time, ya koi app kholna. 'exit' kahein to band ho jaunga."
        )
    return True


def main() -> None:
    voice = Voice()
    if not VOICE_AVAILABLE:
        print("(Voice libraries nahi mili — text mode mein chal raha hoon.)")
    voice.say("Jarvis taiyaar hai. Main aapki kya madad karoon?")

    while True:
        try:
            command = voice.listen()
            if not handle(command, voice):
                break
        except KeyboardInterrupt:
            voice.say("Band ho raha hoon.")
            break


if __name__ == "__main__":
    main()
