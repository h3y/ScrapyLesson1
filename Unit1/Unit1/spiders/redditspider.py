import scrapy


class RedditSpider(scrapy.Spider):
    name = "reddit"

    def start_requests(self):
        urls = [
            'https://www.reddit.com/r/programming/',
            'https://www.reddit.com/r/Python/'
        ]
        requests = []
        for url in urls:
            requests.append(scrapy.Request(url=url, callback=self.parse))
        return requests

    def parse(self, response, **kwargs):
        # reddit list
        for post in response.xpath("//div[@class='rpBJOHq2PR60pnwJlUyP0']//div"):
            yield {
                'title': post.xpath(".//h3[@class='_eYtD2XCVieq6emjKBH3m']/text()").extract_first(),
                'url': post.xpath(".//a[@class='SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE']/@href").extract_first(),
                'username': post.xpath("//a[@class='_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE']/text()").extract_first(),
                'userUrl': post.xpath("//a[@class='_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE']/@href").extract_first(),
                'score': post.xpath('//div[@class="_1rZYMD_4xY3gRcSS3p8ODO"]/text()').re('\d+'),
                'time': ''
            }