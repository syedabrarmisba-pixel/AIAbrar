
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def web_search(query, max_results=5):

    try:

        url = (
            "https://html.duckduckgo.com/html/?q="
            + quote(query)
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return "Web search available nahi hai."

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for result in soup.select(
            ".result"
        )[:max_results]:

            title_element = result.select_one(
                ".result__title"
            )

            snippet_element = result.select_one(
                ".result__snippet"
            )

            link_element = result.select_one(
                ".result__a"
            )

            if not title_element:
                continue

            title = title_element.get_text(
                " ",
                strip=True
            )

            snippet = ""

            if snippet_element:
                snippet = snippet_element.get_text(
                    " ",
                    strip=True
                )

            link = ""

            if link_element:
                link = link_element.get(
                    "href",
                    ""
                )

            results.append({
                "title": title,
                "snippet": snippet,
                "link": link
            })

        if not results:
            return "Koi search result nahi mila."

        output = "Web Search Results:\n\n"

        for index, item in enumerate(
            results,
            start=1
        ):

            output += (
                f"{index}. {item['title']}\n"
                f"{item['snippet']}\n"
                f"{item['link']}\n\n"
            )

        return output.strip()

    except Exception as e:

        print(
            "WEB SEARCH ERROR:",
            e
        )

        return (
            "Web search mein problem aa gayi."
        )


if __name__ == "__main__":

    query = input(
        "Search kya karna hai: "
    )

    print()

    print(
        web_search(query)
    )
