# Compatibility-Patch für Pillow ≥10
from PIL import Image
Image.ANTIALIAS = Image.Resampling.LANCZOS

# zusätzliche Pillow-Imports
from PIL import ImageDraw, ImageFont

# nun die restlichen Imports
from moviepy.editor import (
    VideoFileClip, AudioFileClip,
    concatenate_videoclips, CompositeVideoClip,
    ImageClip
)
from tts import synthesize_speech
from pexels_client import fetch_clips
import numpy as np
import os


def make_text_image(text: str, font_path: str = None, font_size: int = 40, line_spacing: int = 5):
    """
    Erzeugt ein RGBA-Bild mit transparentem Hintergrund und beschriftetem Text via Pillow.
    """
    # Standard-Schrift (Arial) oder angegebener Pfad
    font = ImageFont.truetype(font_path or "arial.ttf", font_size)
    # Zeilen splitten
    lines = text.split("\n") or [text]

    # temporäres Bild zum Messen anlegen
    temp_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(temp_img)

    # Maße jeder Zeile ermitteln
    widths = []
    heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])

    max_width = max(widths)
    total_height = sum(heights) + (len(lines) - 1) * line_spacing

    # Bild erstellen
    img = Image.new("RGBA", (max_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Text zeichnen
    y = 0
    for line, h in zip(lines, heights):
        draw.text((0, y), line, font=font, fill=(255, 255, 255, 255))
        y += h + line_spacing

    # Rückgabe als NumPy-Array
    return np.array(img)


def build_video(script: str, output_path="output.mp4"):
    # 1) TTS-Audio erzeugen
    audio_path = "voice.mp3"
    synthesize_speech(script, audio_path)
    audio = AudioFileClip(audio_path)

    # 2) Stock-Clips laden
    clips = []
    for url in fetch_clips("hibiscus tea", per_page=3):
        clip = VideoFileClip(url).subclip(0, 5).resize(width=720)
        clips.append(clip)

    # 3) Text-Hook als Bildclip
    hook = script.split(".")[0]
    text_img = make_text_image(hook, font_size=40)
    txt_clip = (ImageClip(text_img)
                .set_duration(5)
                .set_position("center"))

    # 4) Erstes Segment: Clip + Textbild
    first = CompositeVideoClip([clips[0], txt_clip])

    # 5) Sequenz zusammensetzen & Audio setzen
    sequence = [first] + clips[1:]
    final = (concatenate_videoclips(sequence)
             .set_audio(audio)
             .set_duration(audio.duration))

    # 6) Export
    final.write_videofile(output_path, fps=24, codec="libx264")
    return output_path


if __name__ == "__main__":
    build_video(
        "VENTY – Refresh & Chill. Unser Hibiskustee bringt Farbe in deinen Tag!",
        "test_output.mp4"
    )

