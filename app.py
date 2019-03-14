from tokopedia import TokopediaScraper


if __name__ == '__main__':
    ts = TokopediaScraper(debug=False)
    default_urls = ts.getListUrl(offset=0, limit=10)
    ts.setListUrl(default_urls)
    ts.run()
    ts.saveData()
