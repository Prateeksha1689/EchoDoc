from gtts import gTTS
from deep_translator import GoogleTranslator
from pydub.utils import mediainfo
import os

def text_to_speech_with_gtts(text, lang="en", filename="temp.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

def get_audio_duration(filepath):
    try:
        info = mediainfo(filepath)
        duration = float(info['duration'])
        return duration
    except:
        return 1.0

def generate_response_audio(english_text, language_choice):
    kannada_text = ""
    en_audio = kn_audio = None

    if language_choice in ["English", "Both"]:
        en_audio = text_to_speech_with_gtts(text=english_text, lang="en", filename="doctor_en.mp3")

    if language_choice in ["Kannada", "Both"]:
        kannada_text = GoogleTranslator(source='auto', target='kn').translate(english_text)
        kn_audio = text_to_speech_with_gtts(text=kannada_text, lang="kn", filename="doctor_kn.mp3")

    return english_text, kannada_text, en_audio, kn_audio

