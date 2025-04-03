import scrapy

class TagalogSpider(scrapy.Spider):
    name = "tagalog"
    allowed_domains = ["tagalog.pinoydictionary.com"]
    start_urls = ["https://tagalog.pinoydictionary.com/list/a/"]

    def parse(self, response):
        # Follow all pagination + letter links
        page_links = response.xpath('//a[contains(@href, "/list/")]/@href').getall()
        for link in page_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(url=absolute_url, callback=self.parse)

        # Scrape word entries from this page
        yield from self.parse_entry(response)

    def parse_entry(self, response):
        for group in response.xpath('//div[@class="word-group"]'):
            tagalog = group.xpath('.//div[@class="word"]/h2[@class="word-entry"]/a/text()').get()
            english = group.xpath('.//div[@class="definition"]/p/text()').get()
            if tagalog and english:
                yield {
                    "tagalog": tagalog,
                    "english": english
                }
