# Jarvis — Voice Assistant aapke PC ke liye

Ek simple Jarvis-style assistant jo aapke **apne computer** ko handle karta hai aur
voice mein status batata hai.

## Kya kar sakta hai

- 📊 **PC status** — CPU, RAM, disk aur battery ka haal voice mein bolta hai
- 🖥️ **Running programs** — kaun se programs sabse zyada chal rahe hain
- 🚀 **App kholna** — "open notepad" / "kholo chrome"
- ⏰ **Time aur date** batata hai
- 🎤 Mic na ho to **keyboard se** bhi command de sakte hain

## Setup

1. Python 3.9+ install karein.
2. Dependencies install karein:

   ```bash
   pip install -r requirements.txt
   ```

   > Agar `PyAudio` install mein dikkat aaye:
   > - **Windows:** `pip install pipwin && pipwin install pyaudio`
   > - **macOS:** `brew install portaudio && pip install pyaudio`
   > - **Linux:** `sudo apt install portaudio19-dev && pip install pyaudio`
   >
   > Voice libraries na milein tab bhi Jarvis **text mode** mein chal jaata hai.

3. Chalayein:

   ```bash
   python jarvis.py
   ```

## Commands (Hindi/Urdu + English dono)

| Aap kahein | Jarvis karega |
|------------|---------------|
| `status` / `haal batao` | CPU, RAM, disk, battery bolega |
| `programs` / `kya chal raha hai` | Top running programs |
| `time` / `kitne baje` / `date` | Time aur date |
| `open notepad` / `kholo chrome` | App kholega |
| `exit` / `band karo` / `bye` | Band ho jaayega |

## Note

- Yeh assistant sirf aapke **apne computer** par chalane ke liye hai.
- Internet sirf speech-to-text (Google) ke liye use hota hai jab aap mic bolte hain.
  Bina internet ke bhi text mode chalta hai.
