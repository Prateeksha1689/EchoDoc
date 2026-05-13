from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
import subprocess
import platform

def convert_mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

def play_audio(wav_file):
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', wav_file])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', wav_file])
    except Exception as e:
        print(f"Error playing audio: {e}")

def doctor_response_to_kannada_speech(input_text, output_filepath="doctor_kannada.mp3", autoplay=False):
    """Translate English doctor response to Kannada and convert to speech."""
    try:
        translated_text = GoogleTranslator(source='en', target='kn').translate(input_text)
        print(f"Translated to Kannada: {translated_text}")
        tts = gTTS(text=translated_text, lang="kn", slow=False)
        tts.save(output_filepath)

        wav_file = output_filepath.replace(".mp3", ".wav")
        convert_mp3_to_wav(output_filepath, wav_file)

        if autoplay:
            play_audio(wav_file)

        return output_filepath
    except Exception as e:
        print(f"Translation or speech error: {e}")
        return None