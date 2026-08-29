import webbrowser
from urllib.parse import quote_plus
from ddgs import DDGS


def search_web(query: str) -> str:
    """
    Open the web browser and search for the query.
    """

    query = query.strip()

    if not query:
        return "What would you like me to search for sir?"

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    webbrowser.open(search_url)

    return f"Searching the web for {query}."


def tell_about(query: str) -> str:
    """
    Search the web and return a short explanation
    from the top result.
    """

    query = query.strip()

    if not query:
        return "What would you like me to tell you about?"

    try:
        results = list(
            DDGS().text(
                query,
                max_results=1
            )
        )

        if not results:
            return f"I couldn't find information about {query}."

        top_result = results[0]

        title = top_result.get("title", "")
        description = top_result.get("body", "")

        if description:
            words = description.split()
            short_description = " ".join(words[:35])

            return f"{title}. {short_description}."

        return f"I found information about {query}, but no short description was available."

    except Exception as error:
        print("Tell about error:", error)
        return "Sorry sir, I couldn't get that information right now."


if __name__ == "__main__":

    response = tell_about("neural networks")

    print("I.G.R.I.S.:")
    print(response)