# tts.py
import os
import pyttsx3

def synthesize_speech(text: str, out_path: str):
    # 1) Engine initialisieren
    engine = pyttsx3.init()
    # 2) Stimme wählen (optional)
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)  # z.B. deutsch: voices[1]
    # 3) Geschwindigkeit einstellen (optional)
    engine.setProperty('rate', 150)

    # 4) Audio in Datei speichern
    engine.save_to_file(text, out_path)
    engine.runAndWait()
    print(f"Audio gespeichert unter: {out_path}")
    return out_path

if __name__ == "__main__":
    synthesize_speech("VENTY – Refresh & Chill. Bald verfügbar!", "voice.mp3")
