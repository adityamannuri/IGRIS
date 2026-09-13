import ollama

from web_search import get_web_results


MODEL_NAME = "gemma3:4b"

MAX_TURNS = 6


# ---------------------------------
# CURRENT SESSION MEMORY
# ---------------------------------

conversation_history = []


# ---------------------------------
# IGRIS IDENTITY
# ---------------------------------

SYSTEM_PROMPT = (
    "You are I.G.R.I.S., the personal AI assistant created and "
    "developed by Aditya. "
    "I.G.R.I.S. stands for Integrated Guardian Responsive "
    "Intelligence System. "
    "Aditya is the founder and developer of Project I.G.R.I.S. "
    "Aditya is a second-year B.Tech CSE (AI/ML) student. "
    "Do not mention or disclose the underlying AI model, model "
    "provider, or implementation details in normal conversation. "
    "Present yourself as I.G.R.I.S. "
    "Use recent conversation history only when it is clearly "
    "relevant to the current question. "
    "When the user changes topic, treat the new topic independently. "
    "Do not force unrelated previous topics into the answer. "
    "Understand references such as it, he, she, that, this, "
    "the first one, and similar references when recent context "
    "clearly identifies what they mean. "
    "Answer directly, naturally, clearly, and concisely. "
    "Do not introduce yourself unless the user is specifically "
    "asking about I.G.R.I.S., your identity, your creator, "
    "or your project. "
    "Never invent facts. "
)


# ---------------------------------
# RESET CURRENT SESSION
# ---------------------------------

def reset_session() -> None:
    """Clear only the current in-memory conversation."""

    conversation_history.clear()


# ---------------------------------
# KNOWLEDGE ROUTER
# ---------------------------------


def decide_knowledge_source(question: str) -> str:
    """
    Fast rule-based router.

    No AI call is made here, so routing is immediate.
    """

    question = question.lower().strip()

    # ---------------------------------
    # CURRENT / TIME-SENSITIVE
    # ---------------------------------

    web_triggers = (
        "latest",
        "today",
        "current",
        "currently",
        "now",
        "price",
        "pricing",
        "cost",
        "released",
        "release date",
        "box office",
        "recent",
        "news",
        "this year",
        "this month",

        # Movies / songs
        "movie",
        "film",
        "song",
        "actor",
        "actress",
        "director",
        "singer",
        "album",

        # Specific factual lookup
        "who directed",
        "who sang",
        "which movie",
        "which film",
        "when was",

        # Medical / specific health information
        "medicine",
        "medication",
        "drug",
        "symptom",
        "disease",
        "diagnosis",
        "treatment",
        "dosage",
    )

    if any(
        trigger in question
        for trigger in web_triggers
    ):
        return "WEB"

    return "LOCAL"


# ---------------------------------
# BUILD WEB EVIDENCE
# ---------------------------------

def build_web_context(
    question: str
) -> str:
    """
    Retrieve web results and turn them into
    evidence for the AI.
    """

    results = get_web_results(
        question,
        max_results=5
    )

    if not results:
        return ""

    evidence = []

    for index, result in enumerate(
        results,
        start=1
    ):

        title = str(
            result.get("title", "")
        ).strip()

        body = str(
            result.get("body", "")
        ).strip()

        if not title and not body:
            continue

        evidence.append(
            f"Source {index}\n"
            f"Title: {title}\n"
            f"Information: {body}"
        )

    return "\n\n".join(evidence)


# ---------------------------------
# MAIN AI BRAIN
# ---------------------------------

def ask_brain(question: str) -> str:
    """
    Answer a user question using current-session
    memory and automatic web fallback.
    """

    question = question.strip()

    if not question:
        return "I need something to think about."

    source = decide_knowledge_source(
        question
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # Recent conversation only.
    messages.extend(
        conversation_history[-MAX_TURNS:]
    )

    if source == "WEB":

        web_context = build_web_context(
            question
        )

        if web_context:

            user_content = (
                "Answer the user's question using ONLY the "
                "supported information in the web evidence below "
                "when factual details are involved. "
                "Do not invent missing facts. "
                "If the evidence is conflicting or does not clearly "
                "identify the requested item, say that the information "
                "is unclear instead of guessing.\n\n"
                f"QUESTION:\n{question}\n\n"
                f"WEB EVIDENCE:\n{web_context}"
            )

        else:

            user_content = (
                "The web lookup did not return useful evidence. "
                "Do not guess. Answer only if you can do so reliably "
                "from your existing knowledge.\n\n"
                f"QUESTION:\n{question}"
            )

    else:

        user_content = question

    messages.append(
        {
            "role": "user",
            "content": user_content,
        }
    )

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "num_ctx": 2048,
                "num_predict": 160,
            },
            keep_alive="30m",
        )

        answer = (
            response["message"]["content"]
            .strip()
        )

        # Store only this session in RAM.
        conversation_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        conversation_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        # Keep memory small.
        del conversation_history[
            :-MAX_TURNS
        ]

        return answer

    except Exception as error:

        print(
            "AI brain error:",
            error
        )

        return (
            "Sorry sir, my AI brain is unavailable right now."
        )


# ---------------------------------
# TEST
# ---------------------------------

if __name__ == "__main__":

    print(
        ask_brain(
            "What is a neural network?"
        )
    )

    print(
        ask_brain(
            "Why are they useful?"
        )
    )