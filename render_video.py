import os
import sys
import json
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, AudioFileClip

def create_video(title_text, audio_path, output_path="output.mp4"):
    # 1. Wczytanie ścieżki dźwiękowej od OpenAI
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 2. Tło (Czarny ekran 1080x1920, dopasowany do długości audio)
    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=duration)

    # 3. Stylizacja tekstu (Biały tekst, wysoki kontrast, wyśrodkowany z cieniem)
    shadow = TextClip(
        title_text.upper(),
        fontsize=60,
        color='black',
        font='Arial-Bold',
        method='caption',
        size=(850, None)
    ).set_position(('center', 805)).set_duration(duration)

    text = TextClip(
        title_text.upper(),
        fontsize=60,
        color='white',
        font='Arial-Bold',
        method='caption',
        size=(850, None)
    ).set_position(('center', 800)).set_duration(duration)

    # 4. Połączenie warstw
    video = CompositeVideoClip([bg, shadow, text]).set_audio(audio)

    # 5. Renderowanie pliku MP4 z wykorzystaniem FFmpeg
    video.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast'
    )

if __name__ == "__main__":
    title = os.getenv("VIDEO_TITLE", "DEFAULT TITLE")
    audio_file = os.getenv("AUDIO_FILE_PATH", "input_audio.mp3")
    
    create_video(title, audio_file)
