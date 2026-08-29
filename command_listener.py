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
import numpy as np
import speech_recognition as sr
from pathlib import Path



from speech_output import speak
from command_processor import process_command

PROJECT_DIR = Path(__file__).parent

SAMPLE_RATE = 16000

MAX_RECORD_SECONDS = 8
SILENCE_SECONDS = 0.8
CALIBRATION_SECONDS = 0.5
BLOCK_SECONDS = 0.1
PRE_ROLL_SECONDS = 0.3


def listen_for_command() -> str | None:
    recognizer = sr.Recognizer()

    print("I.G.R.I.S. is listening...")

    try:
        block_size = int(
            SAMPLE_RATE * BLOCK_SECONDS
        )

        calibration_blocks = int(
            CALIBRATION_SECONDS / BLOCK_SECONDS
        )

        pre_roll_blocks = int(
            PRE_ROLL_SECONDS / BLOCK_SECONDS
        )

        max_blocks = int(
            MAX_RECORD_SECONDS / BLOCK_SECONDS
        )

        # ---------------------------------
        # CALIBRATE BACKGROUND NOISE
        # ---------------------------------
        print("Calibrating...")

        calibration_data = []

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=block_size
        ) as stream:

            for _ in range(calibration_blocks):

                block, _ = stream.read(
                    block_size
                )

                calibration_data.append(
                    block.copy()
                )

            calibration_audio = np.concatenate(
                calibration_data
            )

            noise_level = float(
                np.sqrt(
                    np.mean(
                        calibration_audio ** 2
                    )
                )
            )

            threshold = max(
                0.01,
                noise_level * 3.0
            )

            print(
                f"Noise level: {noise_level:.4f}"
            )

            print(
                f"Voice threshold: {threshold:.4f}"
            )

            # ---------------------------------
            # WAIT FOR SPEECH
            # ---------------------------------
            print("Waiting for speech...")

            recorded_blocks = []
            pre_roll = []

            speech_started = False
            silent_time = 0.0
            elapsed_time = 0.0

            while elapsed_time < MAX_RECORD_SECONDS:

                block, _ = stream.read(
                    block_size
                )

                block = block.copy()

                volume = float(
                    np.sqrt(
                        np.mean(
                            block ** 2
                        )
                    )
                )

                elapsed_time += BLOCK_SECONDS

                # Keep a small amount before speech starts.
                pre_roll.append(block)

                if len(pre_roll) > pre_roll_blocks:
                    pre_roll.pop(0)

                # ---------------------------------
                # SPEECH STARTED
                # ---------------------------------
                if not speech_started:

                    if volume > threshold:

                        speech_started = True

                        print("Speech detected.")

                        recorded_blocks.extend(
                            pre_roll
                        )

                    continue

                # ---------------------------------
                # RECORD SPEECH
                # ---------------------------------
                recorded_blocks.append(
                    block
                )

                if volume < threshold:

                    silent_time += BLOCK_SECONDS

                else:

                    silent_time = 0.0

                # ---------------------------------
                # END AFTER SILENCE
                # ---------------------------------
                if silent_time >= SILENCE_SECONDS:

                    print(
                        "Speech finished."
                    )

                    break

        if not speech_started:

            print(
                "No speech detected."
            )

            return None

        # ---------------------------------
        # SAVE AUDIO
        # ---------------------------------
        recording = np.concatenate(
            recorded_blocks,
            axis=0
        )

        temp_file = (
            PROJECT_DIR /
            "_command_audio.wav"
        )

        sf.write(
            temp_file,
            recording,
            SAMPLE_RATE
        )

        # ---------------------------------
        # SPEECH RECOGNITION
        # ---------------------------------
        with sr.AudioFile(
            str(temp_file)
        ) as source:

            audio = recognizer.record(
                source
            )

        text = recognizer.recognize_google(
            audio
        ).lower().strip()

        print(
            "You said:",
            text
        )

        return text

    except sr.UnknownValueError:

        print(
            "I.G.R.I.S. couldn't understand that."
        )

        return None

    except sr.RequestError as error:

        print(
            "Speech recognition error:",
            error
        )

        return None

    except Exception as error:

        print(
            "Command listener error:",
            error
        )

        return None
def run_command_loop():

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
            "igris",
            response
        )

        speak(response)



        send_conversation_event(
            "status",
            "READY"
        )
if __name__ == "__main__":
    run_command_loop()