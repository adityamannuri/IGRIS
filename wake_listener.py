import subprocess
import webbrowser
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

from speech_output import speak
from command_listener import run_command_loop

WAKE_PHRASES = (
    "daddy is home buddy"
    "daddy is home igris"
    "don't leave me buddy"
    "boss is back"
    "wake up igris"
    "okiro irs"
)

PROJECT_DIR = Path(__file__).parent



SAMPLE_RATE = 16000
RECORD_SECONDS = 4


def listen_for_wake_phrase():

    recognizer = sr.Recognizer()

    print("I.G.R.I.S. wake listener started.")
    print('Say "Wakeup IGRIS"...')

    while True:

        try:
            print("Listening...")

            recording = sd.rec(
                int(RECORD_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32"
            )

            sd.wait()

            temp_file = PROJECT_DIR / "_wake_audio.wav"

            sf.write(
                temp_file,
                recording,
                SAMPLE_RATE
            )

            with sr.AudioFile(str(temp_file)) as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(
                audio
            ).lower().strip()

            print("Heard:", text)

            if any(phrase in text for phrase in WAKE_PHRASES):

                print("I.G.R.I.S. ACTIVATED!")
            from pathlib import Path

            HOLOGRAM_FILE = PROJECT_DIR / "hologram" / "index.html"
            
            EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

            hologram_process = subprocess.Popen(
                [
                    EDGE_PATH,
                    "--app=" + HOLOGRAM_FILE.resolve().as_uri()
                ]
            )

            run_command_loop()

            subprocess.run(
                [
                    "taskkill",
                    "/FI",
                    "WINDOWTITLE eq I.G.R.I.S.*",
                    "/T",
                    "/F"
                ],
                capture_output=True,
                text=True
            )

            return

        except sr.UnknownValueError:
         print("Couldn't understand that.")

        except sr.RequestError as error:
            print("Speech recognition error:", error)

        except Exception as error:
            print("Listener error:", error)


if __name__ == "__main__":
    listen_for_wake_phrase()