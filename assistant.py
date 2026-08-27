import os

from openai import OpenAI


SYSTEM_INSTRUCTIONS = """
You are I.G.R.I.S., a futuristic desktop AI assistant.

Your personality:
- Calm
- Helpful
- Clear
- Concise
- Natural
- Professional

You are answering the user's spoken requests.
Do not claim to have performed an action unless the program actually performed it.
For now, you only generate a natural-language response.
"""


def ask_igris(user_text: str) -> str:
    """Send the user's request to the AI and return its response."""

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set."
        )

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.5",
        instructions=SYSTEM_INSTRUCTIONS,
        input=user_text,
    )

    return response.output_text.strip()


if __name__ == "__main__":
    question = input("You: ")

    try:
        answer = ask_igris(question)
        print("I.G.R.I.S.:", answer)

    except Exception as error:
        print("I.G.R.I.S. error:", error)