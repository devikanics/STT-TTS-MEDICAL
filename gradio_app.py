# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr
import requests

LANGUAGE_MAP = {
    "Hindi":        "hi-IN",
    "English":      "en-IN",
    "Marathi":      "mr-IN",
    "Bengali":      "bn-IN",
    "Tamil":        "ta-IN",
    "Kannada":      "kn-IN",
    "Malayalam":    "ml-IN",
    "Gujrati":      "gu-IN",
    "Odia":         "od-IN",
    "Punjabi":      "pa-IN",
}

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq,transcribe_with_sarvam
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs,text_to_speech_with_sarvam

#load_dotenv()
GROQ_API_KEY="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"

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should only be in one paragraph in two sentences. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see''
            DONT RESPOND AS AN AI in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise."""





def process_inputs(audio_filepath, image_filepath,language_name):
    language_code = LANGUAGE_MAP.get(language_name, "hi‑IN")
    speech_to_text_output = transcribe_with_groq( 
                                                 audio_filepath=audio_filepath,stt_model="whisper-large-v3",GROQ_API_KEY=GROQ_API_KEY
                                                 )

    # Handle the image input
    if image_filepath:
        enc = encode_image(image_filepath)
    else:
        enc = None

    doctor_response = analyze_image_with_query(
        query=system_prompt + speech_to_text_output,
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        encoded_image=enc
    )

    wav_output_path = text_to_speech_with_sarvam(input_text=doctor_response, output_filepath_wav="final.wav",language_code=language_code) 
    return speech_to_text_output, doctor_response, wav_output_path


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath"),
        gr.Dropdown(
            label="Select Output Language",
            choices=list(LANGUAGE_MAP.keys()),     # show full names
            value="Hindi", 
        )
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice", type="filepath")
    ],
    title="Major Project XAI"
)


iface.launch(debug=True)

#http://127.0.0.1:7860