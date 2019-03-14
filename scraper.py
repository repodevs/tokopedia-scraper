import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'}

    def getPage(self, url):
        """ Get Page from given url

        :param url: url to get
        :return: BeautifulSoup object or None
        """
        try:
            req = self.session.get(url, headers=self.headers)
        except Exception as e:
            print(e)
            return None
        bs = BeautifulSoup(req.text, "html.parser")
        return bs

    def openURL(self, url):
        """Open URL as python requests."""
        try:
            req = self.session.get(url, headers=self.headers)
        except Exception as e:
            req = None
            print(f"[-] Error when opening URL: {e}")
        finally:
            return req
