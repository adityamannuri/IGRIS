import json
from urllib.request import Request, urlopen
from pathlib import Path
CONVERSATION_EVENT_URL = "http://127.0.0.1:8765/event"
SLEEP_FLAG = Path(__file__).parent / "_igris_sleep.flag"

def send_conversation_event(role, text):
    """Send a live voice message to the conversation panel."""

    try:
        body = json.dumps(
            {
                "role": role,
                "text": text,
            }
        ).encode("utf-8")

        request = Request(
            CONVERSATION_EVENT_URL,
            data=body,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urlopen(
            request,
            timeout=2
        ):
            pass

    except Exception as error:
        print(
            "Conversation panel update failed:",
            error
        )
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from pathlib import Path



from speech_output import speak
from command_processor import process_command

PROJECT_DIR = Path(__file__).parent

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


def listen_for_command() -> str | None:
    recognizer = sr.Recognizer()

    print("I.G.R.I.S. is listening...")

    try:
        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )

        sd.wait()

        temp_file = PROJECT_DIR / "_command_audio.wav"

        sf.write(
            temp_file,
            recording,
            SAMPLE_RATE,
        )

        with sr.AudioFile(str(temp_file)) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio).lower().strip()

        print("You said:", text)

        return text

    except sr.UnknownValueError:
        print("I.G.R.I.S. couldn't understand that.")
        return None

    except sr.RequestError as error:
        print("Speech recognition error:", error)
        return None

    except Exception as error:
        print("Command listener error:", error)
        return None
def run_command_loop():

    speak("I am listening.")

    while True:

        if SLEEP_FLAG.exists():

            SLEEP_FLAG.unlink()

            speak("Going to sleep.")

            send_conversation_event(
                "igris",
                "Going to sleep."
            )

            send_conversation_event(
                "status",
                "READY"
            )

            return

        command = listen_for_command()

        if not command:
            continue

        send_conversation_event(
            "user",
            command
        )

        response = process_command(command)

        if response == "__SLEEP__":

            send_conversation_event(
                "status",
                "SPEAKING"
            )

            speak("Going to sleep.")

        

            send_conversation_event(
                "status",
                "READY"
            )

            return

        send_conversation_event(
            "status",
            "SPEAKING"
        )

        speak(response)

        send_conversation_event(
            "igris",
            response
        )

        follow_up = "What's now sir?"

        speak(follow_up)

        send_conversation_event(
            "igris",
            follow_up
        )

        send_conversation_event(
            "status",
            "READY"
        )
if __name__ == "__main__":
    run_command_loop()