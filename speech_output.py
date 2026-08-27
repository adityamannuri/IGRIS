import pyttsx3


def speak(text: str) -> None:
    """Speak the supplied text aloud."""
    engine = pyttsx3.init()

    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Hello sir. IGRIS is online.")