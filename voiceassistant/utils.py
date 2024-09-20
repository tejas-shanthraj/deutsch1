import sounddevice as sd
import wave
import whisper
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
from .models import LlmPrompt

# Load environment variables from .env file
load_dotenv()

def record_audio_chunk(duration=5, sample_rate=16000, channels=1):
    try:
        """Record audio for a given duration and save to a file."""
        print("Aufnahme...")
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, device=1, dtype='int16')
        sd.wait()
        print("Recording completed!", audio_data)

        # Check the recorded data
        if audio_data is not None:
            print("Audio recorded successfully!")
        else:
            print("Failed to record audio.")

        temp_file_path = './temp_audio_chunk.wav'
        with wave.open(temp_file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())

        return temp_file_path
    except Exception as e:
        print(f"Error during recording: {e}")
        return None

def transcribe_audio(model, file_path):
    """Transcribe audio file to text using Whisper model."""
    print("Transkribieren...")
    if os.path.isfile(file_path):
        print(file_path)
        print("asdlkfj...")
        results = model.transcribe(file_path, language='de')
        print(f"Results - {results['text']}")
        return results['text']
    else:
        print("Audio file not found")
        return None

def load_whisper():
    """Load and return Whisper model."""
    model = whisper.load_model("base")
    return model

def load_llm(groq_api_key=None):
    """Load and return the ChatGroq model."""
    if groq_api_key is None:
        groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("GROQ_API_KEY muss angegeben werden")

    chat_groq = ChatGroq(
        temperature=0,
        model_name="llama3-8b-8192",
        groq_api_key=groq_api_key
    )
    return chat_groq

def get_response_llm(user_question, memory, groq_api_key, prompt_type):
    """Generate a response from the LLM model based on the prompt type."""

    if prompt_type != "":
        pt = LlmPrompt.objects.filter(prompt_type=prompt_type).values('input_prompt')
        input_prompt = pt[0]['input_prompt']
    else:
        raise ValueError("Unbekannter Prompt-Typ")

    chat_groq = load_llm(groq_api_key)
    prompt = PromptTemplate.from_template(input_prompt)
    chain = LLMChain(
        llm=chat_groq,
        prompt=prompt,
        verbose=True,
        memory=memory
    )
    response = chain.invoke({"question": user_question})
    return response['text']

def play_text_to_speech(text, language='de', slow=False):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang=language, slow=slow)
    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    # os.remove(temp_audio_file)
