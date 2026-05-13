import os
import gradio as gr
import logging
import time
from pydub import AudioSegment
from brain_of_the_doctor import encode_image, analyse_image_with_query
from voice_of_the_patient import transcribe_with_groq
from text_to_speech import generate_response_audio, get_audio_duration

logging.basicConfig(level=logging.INFO)

system_prompt = """
You have to act as a professional doctor, I know you are not but this is for learning purpose.
What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them.
Do not add any numbers or special characters in your response.
Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see, I think you have ....'
Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot.
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please.
"""

def combine_audios(audio1_path, audio2_path, output_path="combined_output.wav"):
    audio1 = AudioSegment.from_file(audio1_path)
    audio2 = AudioSegment.from_file(audio2_path)
    combined = audio1 + AudioSegment.silent(duration=500) + audio2
    combined.export(output_path, format="wav")
    return output_path

def process_inputs(audio_filepath, image_filepath, language_choice):
    if not audio_filepath:
        yield "No audio provided", "", "", None, ""
        return

    try:
        stt_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        yield f"Speech transcription failed: {str(e)}", "", "", None, ""
        return

    try:
        if image_filepath:
            doctor_response = analyse_image_with_query(
                query=system_prompt + stt_output,
                encoded_image=encode_image(image_filepath),
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
            doctor_text = doctor_response[0].message.content.strip()
        else:
            doctor_text = "No image provided for me to analyze."
    except Exception as e:
        yield stt_output, f"Image analysis failed: {str(e)}", "", None, ""
        return

    try:
        english_text, kannada_text, en_audio, kn_audio = generate_response_audio(
            english_text=doctor_text,
            language_choice=language_choice
        )
    except Exception as e:
        yield stt_output, f"Audio generation failed: {str(e)}", "", None, ""
        return

    if language_choice == "Both":
        combined_audio = combine_audios(en_audio, kn_audio)
        combined_text = english_text + "\n\n" + kannada_text
        audio_duration = get_audio_duration(combined_audio)
    elif language_choice == "English":
        combined_audio = en_audio
        combined_text = english_text
        audio_duration = get_audio_duration(en_audio)
    elif language_choice == "Kannada":
        combined_audio = kn_audio
        combined_text = kannada_text
        audio_duration = get_audio_duration(kn_audio)
    else:
        combined_audio = None
        combined_text = ""
        audio_duration = 3.0

    # Adjust typing delay — English slightly faster
    total_chars = max(len(combined_text), 1)
    delay_factor = 0.4 if language_choice == "English" else 0.6
    char_delay = max(min(audio_duration / total_chars * delay_factor, 0.035), 0.003)

    typed_output = ""
    for char in combined_text:
        typed_output += char
        time.sleep(char_delay)
        yield stt_output, english_text, kannada_text, combined_audio, typed_output

def clear_all():
    return "", "", "", None, ""

# Gradio UI
# with gr.Blocks() as iface:
#     gr.Markdown("## 🩺 EchoDoc – Multilingual AI Doctor")

#     with gr.Row():
#         audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Patient Voice")
#         image_input = gr.Image(type="filepath", label="🖼️ Upload Image ")

#     language_choice = gr.Radio(
#         choices=["English", "Kannada", "Both"],
#         label="🌐 Preferred Output Language",
#         value="Both"
#     )

#     with gr.Row():
#         submit_btn = gr.Button("🟢 Submit for Diagnosis")
#         clear_btn = gr.Button("🧹 Clear All")

#     stt_output = gr.Textbox(label="🗣️ Transcribed Patient Speech")
#     doctor_en_text = gr.Textbox(label="👨‍⚕️ Doctor's Response (English)", show_copy_button=True)
#     doctor_kn_text = gr.Textbox(label="👨‍⚕️ Doctor's Response (Kannada)", show_copy_button=True)

#     combined_audio_output = gr.Audio(label="🔊 Doctor's Voice Output", autoplay=True)
#     typing_textbox = gr.Textbox(label="💬 Doctor Typing (Sync with Voice)", lines=10)

#     submit_btn.click(
#         fn=process_inputs,
#         inputs=[audio_input, image_input, language_choice],
#         outputs=[stt_output, doctor_en_text, doctor_kn_text, combined_audio_output, typing_textbox]
#     )

#     clear_btn.click(
#         fn=clear_all,
#         outputs=[stt_output, doctor_en_text, doctor_kn_text, combined_audio_output, typing_textbox]
#     )







# --------------------new UI changed
# with gr.Blocks() as iface:
#     gr.Markdown("<h1 style='text-align: center;'>🩺 EchoDoc – Multilingual AI Doctor</h1>")

#     with gr.Row():
#         # LEFT COLUMN: Inputs
#         with gr.Column(scale=1):
#             audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Patient Voice")
#             image_input = gr.Image(type="filepath", label="🖼️ Upload Image")
            
#             language_choice = gr.Radio(
#                 choices=["English", "Kannada", "Both"],
#                 label="🌐 Preferred Output Language",
#                 value="Both"
#             )

#             submit_btn = gr.Button(" Submit ")
#             clear_btn = gr.Button(" Clear All")

#         # RIGHT COLUMN: Outputs
#         with gr.Column(scale=1):
#             stt_output = gr.Textbox(label="🗣️ Transcribed Patient Speech", lines=2)
#             doctor_en_text = gr.Textbox(label="👨‍⚕️ Doctor's Response (English)", show_copy_button=True, lines=3)
#             doctor_kn_text = gr.Textbox(label="👨‍⚕️ Doctor's Response (Kannada)", show_copy_button=True, lines=3)
#             combined_audio_output = gr.Audio(label="🔊 Doctor's Voice Output", autoplay=True)
#             typing_textbox = gr.Textbox(label="💬 Doctor Response ", lines=6)

#     submit_btn.click(
#         fn=process_inputs,
#         inputs=[audio_input, image_input, language_choice],
#         outputs=[stt_output, doctor_en_text, doctor_kn_text, combined_audio_output, typing_textbox]
#     )

#     clear_btn.click(
#         fn=clear_all,
#         outputs=[stt_output, doctor_en_text, doctor_kn_text, combined_audio_output, typing_textbox]
#     )



# iface.launch(debug=True)




# ---------------------------test-------------
with gr.Blocks() as iface:
    gr.HTML("""
<div id="echodoc-header" style="
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: var(--block-background-fill);
  border-bottom: 1px solid var(--border-color-primary);
">
  <h2 style="
    margin: 0;
    color: var(--body-text-color);
    font-weight: 600;
    font-size: 1.3rem;
  ">EchoDoc</h2>
  <a href='http://localhost:3000' style="
    padding: 8px 16px;
    background-color: var(--button-primary-background, #4F46E5);
    color: var(--button-primary-text-color, #ffffff);
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
  ">
    Logout
  </a>
</div>
""")


    gr.Markdown("<h1 style='text-align: center;'>Healthcare at your voice and vision <br />—Anytime, Anywhere</h1>")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Patient Voice")
            image_input = gr.Image(type="filepath", label="🖼️ Upload Image ")
            language_choice = gr.Radio(
                choices=["English", "Kannada", "Both"],
                label="🌐 Preferred Output Language",
                value="Both"
            )
            with gr.Row():
                submit_btn = gr.Button(" Submit ")
                clear_btn = gr.Button(" Clear ")
        with gr.Column():
            stt_output = gr.Textbox(label="🗣️ Transcribed Patient Speech")
            typing_textbox_en = gr.Textbox(label="👨‍⚕️ Doctor Typing (English)", lines=6, visible=False)
            typing_textbox_kn = gr.Textbox(label="👨‍⚕️ Doctor Typing (Kannada)", lines=6, visible=False)
            combined_audio_output = gr.Audio(label="🔊 Doctor's Voice Output", autoplay=True)

    def update_visibility(language_choice):
        return {
            typing_textbox_en: gr.update(visible=(language_choice in ["English", "Both"])),
            typing_textbox_kn: gr.update(visible=(language_choice in ["Kannada", "Both"]))
        }

    language_choice.change(fn=update_visibility, inputs=language_choice, outputs=[typing_textbox_en, typing_textbox_kn])

    def process_inputs(audio_filepath, image_filepath, language_choice):
        if not audio_filepath:
            yield "No audio provided", "", "", None, ""
            return

        try:
            stt_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )
        except Exception as e:
            yield f"Speech transcription failed: {str(e)}", "", "", None, ""
            return

        try:
            if image_filepath:
                doctor_response = analyse_image_with_query(
                    query=system_prompt + stt_output,
                    encoded_image=encode_image(image_filepath),
                    model="meta-llama/llama-4-scout-17b-16e-instruct"
                )
                doctor_text = doctor_response[0].message.content.strip()
            else:
                doctor_text = "No image provided for me to analyze."
        except Exception as e:
            yield stt_output, f"Image analysis failed: {str(e)}", "", None, ""
            return

        try:
            english_text, kannada_text, en_audio, kn_audio = generate_response_audio(
                english_text=doctor_text,
                language_choice=language_choice
            )
        except Exception as e:
            yield stt_output, f"Audio generation failed: {str(e)}", "", None, ""
            return

        if language_choice == "Both":
            combined_audio = combine_audios(en_audio, kn_audio)
            audio_duration = get_audio_duration(combined_audio)
        elif language_choice == "English":
            combined_audio = en_audio
            audio_duration = get_audio_duration(en_audio)
        elif language_choice == "Kannada":
            combined_audio = kn_audio
            audio_duration = get_audio_duration(kn_audio)
        else:
            combined_audio = None
            audio_duration = 3.0

        delay_factor = 0.4
        typed_output_en, typed_output_kn = "", ""

        max_len = max(len(english_text), len(kannada_text), 1)
        char_delay = max(min(audio_duration / max_len * delay_factor, 0.035), 0.003)

        for i in range(max_len):
            if language_choice in ["English", "Both"] and i < len(english_text):
                typed_output_en += english_text[i]
            if language_choice in ["Kannada", "Both"] and i < len(kannada_text):
                typed_output_kn += kannada_text[i]
            time.sleep(char_delay)
            yield stt_output, typed_output_en, typed_output_kn, combined_audio

    def clear_all():
        return "", "", "", None

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input, language_choice],
        outputs=[stt_output, typing_textbox_en, typing_textbox_kn, combined_audio_output]
    )

    clear_btn.click(
        fn=clear_all,
        outputs=[stt_output, typing_textbox_en, typing_textbox_kn, combined_audio_output]
    )

iface.launch(debug=True)
