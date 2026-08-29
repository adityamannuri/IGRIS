import ollama


MODEL_NAME = "gemma3:4b"


def ask_brain(question: str) -> str:
    """
    Send a question to IGRIS's local AI brain.
    """

    question = question.strip()

    if not question:
        return "I need something to think about."

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are I.G.R.I.S., a personal desktop AI assistant. "
                        "Answer clearly, naturally, and concisely. "
                        "Keep answers short unless the user asks for detail."
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        return response["message"]["content"].strip()

    except Exception as error:
        print("AI brain error:", error)
        return "Sorry sir, my AI brain is unavailable right now."


if __name__ == "__main__":

    answer = ask_brain(
        "Explain neural networks in two sentences."
    )

    print("I.G.R.I.S.:")
    print(answer)