# #Step1a: Setup Text to Speech–TTS–model with gTTS
# import os
# from gtts import gTTS

# def text_to_speech_with_gtts_old(input_text, output_filepath):
#     language="en"

#     audioobj= gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)


# input_text="Hi this is AI with Ashfaq!"
# # text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

# #Step1b: Setup Text to Speech–TTS–model with ElevenLabs
# import elevenlabs
# from elevenlabs.client import ElevenLabs

# ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.generate(
#         text= input_text,
#         voice= "Clyde",
#         output_format= "mp3_22050_32",
#         model= "eleven_turbo_v2"
#     )
#     elevenlabs.save(audio, output_filepath)

# # text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 



# #Step2: Use Model for Text output to Voice

# import subprocess
# import platform
# from pydub import AudioSegment
# from playsound import playsound




# def convert_mp3_to_wav(mp3_file, wav_file):
#     sound = AudioSegment.from_mp3(mp3_file)
#     sound.export(wav_file, format="wav")


# def text_to_speech_with_gtts(input_text, output_filepath):
#     language="kn"

#     audioobj= gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
    
#     wav_file = output_filepath.replace(".mp3", ".wav")
#     convert_mp3_to_wav(output_filepath, wav_file)
    


#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])
#             # playsound(output_filepath)
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")


# input_text="ನನ್ನ ಮುಖದಲ್ಲಿ ಇದೇನಿದೆ?"
# # text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


# def text_to_speech_with_elevenlabs(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.generate(
#         text= input_text,
#         voice= "Aria",
#         output_format= "mp3_22050_32",
#         model= "eleven_turbo_v2"
#     )
#     elevenlabs.save(audio, output_filepath)

#     wav_file = output_filepath.replace(".mp3", ".wav")
#     convert_mp3_to_wav(output_filepath, wav_file)

#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")

# # text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")



# voice_of_the_doctor.py

from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
import os

def convert_mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

def text_to_speech(text, lang, output_path):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    wav_path = output_path.replace(".mp3", ".wav")
    convert_mp3_to_wav(output_path, wav_path)
    return output_path

def generate_response_audio(english_text, language_choice):
    english_audio = None
    kannada_audio = None
    kannada_text = None

    if language_choice in ["English", "Both"]:
        english_audio = text_to_speech(english_text, "en", "doctor_en.mp3")

    if language_choice in ["Kannada", "Both"]:
        kannada_text = GoogleTranslator(source='en', target='kn').translate(english_text)
        kannada_audio = text_to_speech(kannada_text, "kn", "doctor_kn.mp3")

    return english_text, kannada_text, english_audio, kannada_audio


import os
from groq import Groq

def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model="whisper-large-v3"):
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="kn"
        )
    return transcription.text