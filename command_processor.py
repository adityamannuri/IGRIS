from datetime import datetime
import subprocess
import webbrowser


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
    # WEB SEARCH
    # -----------------------------
    if command.startswith("search for "):

        query = command.replace(
            "search for ",
            "",
            1
        ).strip()

        if query:
            webbrowser.open(
                "https://www.google.com/search?q="
                + query.replace(" ", "+")
            )

            return f"Searching for {query}."

    # -----------------------------
    # GREETING
    # -----------------------------
    if "hello" in command or "hi igris" in command:
        return "Hello sir. How May i Help you."

    # -----------------------------
    # NAME
    # -----------------------------
    if (
        "what is your name" in command
        or "what's your name" in command
        or "who are you" in command
):
        return "My full name is Integrated Guardian Responsive Intelligence System."
    
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
    # UNKNOWN
    # -----------------------------
    return "Sorry Sir, I didn't understand that command."

if __name__ == "__main__":

    while True:

        user_command = input("Command: ")

        response = process_command(
            user_command
        )

        print("I.G.R.I.S.:", response)

        if response == "__SLEEP__":
            break