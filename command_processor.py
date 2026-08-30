from datetime import datetime
import subprocess
import webbrowser
from web_search import search_web
from ai_brain import ask_brain
from creator_profile import CREATOR_PROFILE

def process_command(command: str) -> str:
    """
    Process a spoken command and return I.G.R.I.S.'s response.
    """

    command = command.lower().strip()

        # -----------------------------
    # SLEEP / STOP LISTENING
    # -----------------------------
    sleep_phrases = (
        "go to sleep",
        "sleep igris",
        "sleep now",
        "stop listening",
        "stop listening igris",
        "shut down listening",
        "shutdown listening",
        "you can sleep",
        "go to sleep buddy",
        "ok buddy go to sleep now",
        "that's all",
    )

    if any(phrase in command for phrase in sleep_phrases):
        return "__SLEEP__"

    # -----------------------------
    # TIME
    # -----------------------------
    if "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    # -----------------------------
    # DATE
    # -----------------------------
    if "date" in command or "today" in command:
        current_date = datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {current_date}."

    # -----------------------------
    # OPEN CHROME / EDGE
    # -----------------------------
    if "open chrome" in command:
        subprocess.Popen(
            ["cmd", "/c", "start", "", "chrome"],
            shell=False
        )
        return "Opening Chrome."

    if "open edge" in command or "open microsoft edge" in command:
        subprocess.Popen(
            ["cmd", "/c", "start", "", "msedge"],
            shell=False
        )
        return "Opening Microsoft Edge."

    # -----------------------------
    # OPEN VS CODE
    # -----------------------------
    if "open vs code" in command or "open vscode" in command:
        subprocess.Popen(
            ["cmd", "/c", "start", "", "code"],
            shell=False
        )
        return "Opening Visual Studio Code."
    # -----------------------------
    # IGRIS / CREATOR IDENTITY
    # -----------------------------
    if (
        "what is your name" in command
        or "what's your name" in command
    ):
        return (
            "My full name is Integrated Guardian Responsive Intelligence System."
        )

    if (
        "who are you" in command
    ):
        return (
            "I am I.G.R.I.S., your personal AI assistant."
        )

    if (
        "who is your creator" in command
        or "who created you" in command
        or "who made you" in command
        or "who is created you" in command
    ):
        return (
            f"My creator is {CREATOR_PROFILE['name']}, "
            f"the {CREATOR_PROFILE['role']}."
        )

    if (
        "what is my name" in command
    ):
        return (
            f"Your name is {CREATOR_PROFILE['name']}."
        )

    if (
        "what am i studying" in command
        or "what do i study" in command
        or "which course am i studying" in command
    ):
        return (
            f"You are studying {CREATOR_PROFILE['education']}."
        )

    if (
        "which year am i in" in command
        or "what year am i in" in command
        or "which standard am i in" in command
    ):
        return (
            f"You are in your {CREATOR_PROFILE['year']}."
        )

    if (
        "what is my project" in command
        or "tell me about my project" in command
    ):
        return (
            f"Your project is {CREATOR_PROFILE['project']}."
        )

    # -----------------------------
    # WEB SEARCH - IGRIS V1.5
    # -----------------------------
    search_triggers = (
        "search for ",
        "search ",
        "look up ",
        "find information about ",
        "find info about ",
        "search the web for ",
    )

    for trigger in search_triggers:

        if command.startswith(trigger):

            query = command[len(trigger):].strip()

            if query:
                return search_web(query)

            return "What would you like me to search for sir?"

    # -----------------------------
    # GREETING
    # -----------------------------
    if "hello" in command or "hi igris" in command:
        return "Hello sir. How May i Help you."
    
    # -----------------------------
    # PLAY MUSIC
    # -----------------------------
    if command.startswith("play "):
        song = command[5:].strip()

        if not song:
            return "What song would you like me to play sir?"

        youtube_query = song.replace(" ", "+")

        webbrowser.open(
            "https://www.youtube.com/results?search_query="
            + youtube_query
    )

        return f"Searching for {song}."


    # -----------------------------
    # AI BRAIN - IGRIS V2
    # -----------------------------
    return ask_brain(command)


    if __name__ == "__main__":

        while True:

            user_command = input("Command: ")

            response = process_command(
                user_command
            )

            print("I.G.R.I.S.:", response)

            if response == "__SLEEP__":
                break