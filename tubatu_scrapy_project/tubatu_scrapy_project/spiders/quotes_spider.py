import scrapy


class QuotesSpider(scrapy.Spider):
    name = "tubatu"


    start_urls = [
        'https://xiaoguotu.to8to.com/pic_space2?page=1',
    ]

    def start_requests(self):
        urls = [
            'https://www.to8to.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)