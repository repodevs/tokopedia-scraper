import csv
from scraper import Scraper

# Default HEADERS
HEADERS = {
    'origin': 'https://www.tokopedia.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://www.tokopedia.com/p/laptop-aksesoris/laptop',
    'authority': 'ace.tokopedia.com'
}


class TokopediaData:
    def __init__(self, productId=None, title=None, description=None, price=0):
        self.id = productId
        self.title = title
        self.description = description
        self.price = price

    def display(self):
        print(f"ProductID: {self.id}")
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Price: {self.price}")

    def toList(self):
        data = [
            self.id,
            self.title,
            self.description,
            self.price
        ]
        return data

    def toDict(self):
        data_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price
        }
        return data_dict


class TokopediaScraper(Scraper):
    def __init__(self, headers=HEADERS, debug=False):
        super(TokopediaScraper, self).__init__()
        self.headers = {**self.headers, **headers}
        self.url_products = [
            'https://www.tokopedia.com/bennykoicikarang/lenovo-yoga-900',
            'https://www.tokopedia.com/toptech/hp-14-cm0091au-amd-a4-9125-ssd-128gb-4gb-win10-joy-2'
        ]
        self.debug = debug
        self.data_detail_products = []

    def getDataByClass(self, content, name, as_text=True):
        """Get Data by Class Name
        """
        data = content.find(attrs={'class': name})
        if as_text and data:
            return data.text.strip()
        return data

    def getDataByProp(self, content, name, as_text=True, strip=True):
        """Get Data by Prop Name
        """
        data = content.find(attrs={'itemprop': name})
        resp = None
        if data:
            if as_text and strip:
                resp = data.text.strip()
            elif as_text and not strip:
                content = "".join([str(item).strip() for item in data.contents])
                resp = content
            else:
                resp = data
        return resp

    def getDataByAttr(self, content, attr={}, type='value', default=None):
        """ Get Data by Attr """
        data = content.find(attrs=attr)
        resp = default
        if data:
            if type == 'value':
                resp = data['value']
            elif type == 'text':
                resp = data.text.strip()
            else:
                resp = data
        return resp

    def getDataValue(self, content, name, selector=getDataByProp, as_text=True, strip=True):
        """Get Value Data.
        """
        # TODO: Add option to use `selector` so it's make more flexible
        data = self.getDataByProp(content, name, as_text, strip)
        return data

    def getListUrl(self, offset=0, limit=100):
        """Get List URLs from default category.

        :param offset: Offset of category page
        :param limit: Limit data to show
        :return: list of (cleaned) product url
        """
        url_category = f"https://ace.tokopedia.com/search/product/v3?scheme=https&device=desktop&related=true&start={offset}&ob=23&source=directory&st=product&identifier=laptop-aksesoris_laptop&sc=289&rows={limit}&unique_id=7164647f8d9d4c9798da21c416b76558&safe_search=false"
        req = self.openURL(url_category)
        urls = []
        if req:
            result = req.json()
            products = result.get('data').get('products')
            for product in products:
                product_url = product.get('url')
                if product_url:
                    cleaned_url = product_url.split('?')[0]
                    urls.append(cleaned_url)
        return urls

    def setListUrl(self, urls):
        """Set List of URL Product to scrape """
        if isinstance(urls, list) or isinstance(urls, tuple):
            self.url_products = urls
        else:
            print("[-] URL is not valid list or tuple!")
            # Set to empty if urls not valid
            self.url_products = []

    def extractProductDetail(self, url):
        soup = self.getPage(url)
        tokped = TokopediaData()
        tokped.id = self.getDataByAttr(soup, attr={'name': 'product_id'}, default=0)
        tokped.title = self.getDataValue(soup, 'name')
        tokped.description = self.getDataValue(soup, 'description', strip=False)
        tokped.price = self.getDataByAttr(soup, {'id': 'product_price_int'})

        if self.debug:
            tokped.display()

        return tokped

    def run(self):
        """Run Scraper """
        products = []
        for url in self.url_products:
            product = self.extractProductDetail(url)
            products.append(product.toList())
        self.data_detail_products = products

    def saveData(self, path='data_products.csv'):
        """Save data products to file """
        with open(path, 'w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(['id', 'product_id', 'title', 'description', 'price'])
            index = 0
            for data in self.data_detail_products:
                index += 1
                writer.writerow([index, data[0], data[1], data[2], data[3]])

            print(f"Data saved to `{path}`")
