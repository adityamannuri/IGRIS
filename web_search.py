import webbrowser
from urllib.parse import quote_plus

from ddgs import DDGS


# ---------------------------------
# GOOGLE SEARCH
# ---------------------------------

def search_web(query: str) -> str:
    """
    Open a Google search for the given query.
    """

    query = query.strip()

    if not query:
        return "What would you like me to search for sir?"

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    try:
        webbrowser.open(search_url)
    except Exception as error:
        print("Browser error:", error)
        return "Sorry sir, I couldn't open the web browser."

    return f"Searching the web for {query}."


# ---------------------------------
# GET WEB RESULTS
# ---------------------------------

def get_web_results(
    query: str,
    max_results: int = 3
) -> list[dict]:
    """
    Retrieve web search results safely.

    This does not open the browser.
    """

    query = query.strip()

    if not query:
        return []

    try:
        results = list(
            DDGS().text(
                query,
                max_results=max_results
            )
        )

        return results

    except Exception as error:
        print("Web search error:", error)
        return []


# ---------------------------------
# EXTRACT TOP RESULT
# ---------------------------------

def tell_about(query: str) -> str:
    """
    Extract a short explanation from the top web result.
    """

    query = query.strip()

    if not query:
        return "What would you like me to tell you about?"

    results = get_web_results(
        query,
        max_results=3
    )

    if not results:
        return (
            f"I couldn't find reliable web information "
            f"about {query}."
        )

    top_result = results[0]

    title = str(
        top_result.get("title", "")
    ).strip()

    description = str(
        top_result.get("body", "")
    ).strip()

    if not title:
        title = "Web result"

    if description:
        words = description.split()

        # Keep the extracted result short.
        short_description = " ".join(
            words[:45]
        )

        return (
            f"{title}. "
            f"{short_description}."
        )

    return (
        f"I found a web result about {query}, "
        f"but it did not contain a useful description."
    )


# ---------------------------------
# TEST
# ---------------------------------

if __name__ == "__main__":

    response = tell_about(
        "neural networks"
    )

    print("I.G.R.I.S.:")
    print(response)