import requests
from bs4 import BeautifulSoup
from yahoosearchengine import yahoo_search
from langchain.agents import tool

data = []
def smart_scrape(url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "DNT": "1",  # Do Not Track
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
            "Cache-Control": "no-cache",
        }

        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # Try to get titles, headlines, paragraphs
        headlines = soup.find_all(["h1", "h2", "h3"], limit=20)
        paragraphs = soup.find_all("p", limit=20)
        #
        for h in headlines:
            data.append("📰 " + h.get_text(strip=True))
        for p in paragraphs:
            data.append("📄 " + p.get_text(strip=True))


        return "\n".join(data)

@tool
def get_data(querry:str):
    """
    This function Provides Data Using web search and scraping.
    :param querry: String to be searched on web.
    :return: String of data
    """
    global data
    data = []
    urls = yahoo_search(querry)
    for url in urls:
        try:
            smart_scrape(url)
        except Exception as e:
            print(e)
    return "\t".join(data)

# print(get_data("india and pakistan war"))
# print(smart_scrape("https://www.hindustantimes.com/world-news/us-news/tiktoker-khabane-khaby-lame-arrested-by-ice-being-held-at-henderson-detention-center-nevada-report-101749255132720.html"))