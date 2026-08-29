import multiprocessing
from pathlib import Path


PROJECT_DIR = Path(__file__).parent
SPEECH_PID_FILE = PROJECT_DIR / "_igris_speech.pid"

speech_process = None


def wait_for_speech() -> None:
    """Wait until the current speech process finishes."""

    global speech_process

    if speech_process is not None:

        speech_process.join()

        speech_process = None

def _speak_worker(text: str) -> None:
    """Run pyttsx3 in a separate process."""

    import pyttsx3

    engine = pyttsx3.init()

    engine.setProperty("rate", 190)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()


def stop_speaking() -> None:
    """Stop the currently running IGRIS speech process."""

    global speech_process

    # First try the local process reference.
    if speech_process is not None:

        try:
            if speech_process.is_alive():
                speech_process.terminate()
                speech_process.join(timeout=1)
        except Exception as error:
            print("Local speech stop error:", error)

        speech_process = None

    # Then check the shared PID file.
    try:

        if SPEECH_PID_FILE.exists():

            pid_text = SPEECH_PID_FILE.read_text(
                encoding="utf-8"
            ).strip()

            if pid_text:

                pid = int(pid_text)

                if pid != multiprocessing.current_process().pid:

                    try:
                        import os
                        import signal

                        os.kill(
                            pid,
                            signal.SIGTERM
                        )

                    except ProcessLookupError:
                        pass

                    except Exception as error:
                        print(
                            "Shared speech stop error:",
                            error
                        )

            SPEECH_PID_FILE.unlink(
                missing_ok=True
            )

    except Exception as error:
        print(
            "Speech PID error:",
            error
        )


def speak(text: str) -> None:
    """Start speech without blocking IGRIS."""

    global speech_process

    if not text:
        return

    stop_speaking()

    speech_process = multiprocessing.Process(
        target=_speak_worker,
        args=(text,),
        daemon=True
    )

    speech_process.start()

    try:
        SPEECH_PID_FILE.write_text(
            str(speech_process.pid),
            encoding="utf-8"
        )
    except Exception as error:
        print(
            "Speech PID write error:",
            error
        )


if __name__ == "__main__":

    print("Speaking...")

    speak(
        "Hello sir. This is the IGRIS speech interruption test."
    )

    input(
        "Press Enter to stop speech..."
    )

    stop_speaking()

    print("Speech stopped.")