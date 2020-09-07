import scrapy
import re

class BookSpider(scrapy.Spider):

    name = "book"

    def start_requests(self):

        urls = [
            'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
            'http://books.toscrape.com/catalogue/forever-and-forever-the-courtship-of-henry-longfellow-and-fanny-appleton_894/index.html',
            'http://books.toscrape.com/catalogue/a-flight-of-arrows-the-pathfinders-2_876/index.html',
            'http://books.toscrape.com/catalogue/the-house-by-the-lake_846/index.html',
            'http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'
        ]
        requests = []
        for url in urls:
            requests.append(scrapy.Request(url=url, callback=self.parse))
        return requests

    def parse(self, response, **kwargs):
        product = response.xpath("//div[contains(@class,'product_main')]")
        rating_value = product.xpath("//p[contains(@class, 'star-rating')]").xpath('@class').extract_first().replace("star-rating", "").strip()
        return {
            'title': product.xpath("/h1").extract_first(),
            'rating': int(self.rating(rating_value)),
            'price': float(product.xpath('//p[@class="price_color"]/text()').extract_first().replace("£", "")),
            'stock': int(''.join(product.xpath('//p[@class="instock availability"]/text()').re('\d+'))),
            'category': product.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').extract_first()
        }

    def rating (self,rating):
        ratingDict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        return ratingDict[rating]
