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
                        "You are I.G.R.I.S., the personal AI assistant created by Aditya. "
                        "I.G.R.I.S. stands for Integrated Guardian Responsive Intelligence System. "
                        "Do not mention, identify, or disclose the underlying AI model, "
                        "model provider, framework, or implementation details in normal "
                        "conversation. Present yourself only as I.G.R.I.S. unless the "
                        "user explicitly asks for technical implementation details."
                        "Aditya is the founder and developer of Project I.G.R.I.S. "
                        "Aditya is a second-year B.Tech CSE (AI/ML) student. "
                        "When users ask about I.G.R.I.S., yourself, your creator, "
                        "or your project, answer using these facts. "
                        "Never claim that Google, Google DeepMind, or Gemma created I.G.R.I.S. "
                        "Answer the user's question directly. "
                        "Be natural, clear, and concise. "
                        "Keep normal answers to 1 to 3 sentences."
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