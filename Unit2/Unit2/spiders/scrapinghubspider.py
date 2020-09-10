import scrapy


class BookSpider(scrapy.Spider):
    name = "scrapinghub"

    def start_requests(self):

        urls = [
            'https://blog.scrapinghub.com/'
        ]
        requests = []
        for url in urls:
            requests.append(scrapy.Request(url=url, callback=self.parse))
        return requests

    def parse_post(self, response):
        post_tags = response.xpath('//div[@class="post-topic"]/a/text()').getall()
        if post_tags is not None:
            yield {
                'postTitle': response.xpath('//span[@id="hs_cos_wrapper_name"]/text()').get(),
                'url': response.xpath('//a[@class="hs-featured-image-link"]/@href').get(),
                'authorName': response.xpath('//span[@class="author"]/a/text()').get(),
                'postTags': post_tags
            }

    def parse(self, response, **kwargs):
        post_page_links = response.xpath('//a[@class="hs-featured-image-link"]')
        yield from response.follow_all(post_page_links, self.parse_post)

        next_page = response.xpath('//a[@class="next-posts-link"]')
        yield from response.follow_all(next_page, self.parse)
