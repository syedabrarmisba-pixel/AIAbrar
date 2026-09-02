import os
import tempfile
import wave

import numpy as np
import sounddevice as sd
import pyttsx3
from faster_whisper import WhisperModel
from ollama import chat

MODEL_NAME = "tinyllama:latest"
WHISPER_PATH = "whisper-model"

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

user_name = "Abrar"

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    print("AbrarAI:", text)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Voice error:", e)


print("Loading Whisper...")

whisper = WhisperModel(
    WHISPER_PATH,
    device="cpu",
    compute_type="int8"
)

print("Whisper loaded successfully!")


def record_voice():
    print()
    print("🎤 Listening... Speak now!")

    audio = sd.rec(
        int(SAMPLE_RATE * RECORD_SECONDS),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    print("✅ Recording complete!")

    return audio


def save_audio(audio):
    audio_int16 = (audio * 32767).astype(np.int16)

    file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    filename = file.name
    file.close()

    with wave.open(filename, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(audio_int16.tobytes())

    return filename


def listen():
    audio = record_voice()
    filename = save_audio(audio)

    print("🧠 Understanding...")

    try:
        segments, info = whisper.transcribe(
            filename,
            language="en",
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    finally:
        try:
            os.remove(filename)
        except:
            pass


def ask_ai(user_text):
    system_prompt = f"""
You are AbrarAI, Abrar's personal AI assistant.

Rules:
- Always answer in clear, simple English.
- Be friendly and helpful.
- The user's name is {user_name}.
- You may call him Abrar or sir.
- Do not randomly change languages.
- Give direct and useful answers.
- Keep answers reasonably short because you speak your answers aloud.
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response.message.content


print()
print("================================")
print("          ABRAR AI")
print("================================")
print("Voice AI - Local")
print("Say 'exit' to stop.")
print()

speak("Hello Abrar. AbrarAI is ready.")


while True:

    try:
        user_text = listen()

        if not user_text:
            print("I didn't hear anything.")
            speak("I didn't hear anything.")
            continue

        print("You:", user_text)

        if user_text.lower().strip() in [
            "exit",
            "quit",
            "stop",
            "goodbye"
        ]:
            speak("Allah Hafiz, Abrar!")
            break

        if "my name is" in user_text.lower():

            name = user_text.lower().split(
                "my name is",
                1
            )[1].strip()

            if name:
                user_name = name.title()

                answer = (
                    f"Nice to meet you, {user_name}. "
                    "I will remember your name."
                )

                speak(answer)
                continue

        if "what is my name" in user_text.lower():

            answer = f"Your name is {user_name}, sir."

            speak(answer)
            continue

        answer = ask_ai(user_text)

        speak(answer)

    except KeyboardInterrupt:

        print()
        speak("Goodbye, Abrar!")
        break

    except Exception as e:

        print("Error:", e)
        speak("Sorry Abrar, something went wrong.")