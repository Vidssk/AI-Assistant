from brain import ask_model
import webbrowser
from urllib.parse import quote_plus

class WebSearchManager:

    def search(self, query):

        print(f"Searching web for: {query}")

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        webbrowser.open(url)

        return f"Opened search for {query}"

    def summarize(self, query, results):

        prompt = f"""
        Query:
        {query}

        Results:
        {results}

        Summarize the answer.
        """

        return ask_model(prompt)

    def open_result(self, url):
        pass

    def research(self, topic):
        pass

if __name__ == "__main__":
    manager = WebSearchManager()
    result = manager.search("What is the capital of France?")
    print(result)