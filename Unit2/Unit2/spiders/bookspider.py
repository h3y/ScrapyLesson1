import scrapy


def rating_to_integer(rating):
    rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return rating_dict[rating]


class BookSpider(scrapy.Spider):
    name = "book"

    def start_requests(self):

        urls = [
            'http://books.toscrape.com/'
        ]
        requests = []
        for url in urls:
            requests.append(scrapy.Request(url=url, callback=self.parse))
        return requests

    def parse_book_pages(self, response):
        product = response.xpath("//div[contains(@class,'product_main')]")
        rating_value = product.xpath(".//p[contains(@class, 'star-rating')]/@class") \
            .get().replace("star-rating", "").strip()
        return {
            'title': product.xpath(".//h1/text()").get(),
            'rating': int(rating_to_integer(rating_value)),
            'price': float(product.xpath('.//p[@class="price_color"]/text()').re_first(r"(\d+.\d+)")),
            'stock': int(''.join(product.xpath('.//p[@class="instock availability"]/text()').re(r'\d+'))),
            'coverUrl': response.urljoin(product.xpath('.//div[@id="product_gallery"]//img/@src').get())
        }

    def parse(self, response, **kwargs):
        book_page_links = response.xpath('//h3/a')
        yield from response.follow_all(book_page_links, self.parse_book_pages)

        next_page = response.xpath('//li[@class="next"]/a')
        yield from response.follow_all(next_page, self.parse)
