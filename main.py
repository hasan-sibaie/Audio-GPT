#make sure FFMPEG IS installed and configured in the PATH environment 
import gradio as gr
import openai
import winsound
from elevenlabslib import *
from pydub import AudioSegment
from pydub.playback import play
import io




#API Keys go here
openai.api_key = 'OPENAI.KEY'
api_key = '11Labs.KEY'
from elevenlabslib import ElevenLabsUser
def new_func(api_key):
    user = ElevenLabsUser(api_key)
    return user

user = new_func(api_key)

messages = ["Assume the role of an an expert advisor.Respond to all input in 50 words or less."]

def transcribe(audio):
    global messages

    if audio is None:
        return "Error: No audio file provided"

    audio_file = open(audio, "rb")
    # rest of the code
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append(f"\nUser: {transcript['text']}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages[-1],
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5,
    )

    system_message = response["choices"][0]["text"]
    messages.append(f"{system_message}")

    #You can choose your own preset voices via ElevenLabs/Voices

    voice = user.get_voices_by_name("MyV")[0]
    audio = voice.generate_audio_bytes(system_message)

    audio = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
    audio.export("output.wav", format="wav")

    winsound.PlaySound("output.wav", winsound.SND_FILENAME)

    chat_transcript = "\n".join(messages)
    return chat_transcript


#Interface is straightforward,make sure to enable MIC access before recording.


interface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="microphone", type="filepath"),
    outputs="text",
    title="Desktop ChatGPT Assistant ",
    description="Please make sure your Microphone is working properly. Ask your question via recording the message and I'll respond to you on the right via audio and text",

)


interface.launch()
