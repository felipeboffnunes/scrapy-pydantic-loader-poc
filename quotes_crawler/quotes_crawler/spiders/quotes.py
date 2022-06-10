from typing import Generator

import scrapy
from scrapy import Request
from scrapy.http import Response

from quotes_crawler.items import Quote, Tag, QuoteLoader


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    custom_settings = Quote.build_spidermon_base_monitor()

    def parse(self, response: Response, **kwargs) -> Generator[Request | Quote, None, None]:
        for idx, quote in enumerate(response.css(".quote")):
            # tags = []
            # for tag_idx, tag in enumerate(quote.css(".tag *::text").getall()):
            #     tags.append(Tag.construct(**{"idx": tag_idx, "tag": tag}))

            quote_loader = QuoteLoader(response=response, selector=quote)
            quote_loader.add_css("quote", ".text::text")
            quote_loader.add_css("author", ".author::text")
            quote_loader.add_css("author_url", ".author ~ a::attr(href)")
            quote_loader.add_css("tags", ".tag *::text")
            quote_loader.add_value("idx", idx)
            item = quote_loader.load_item()
            yield item

        yield scrapy.Request(
            response.urljoin(response.css(".next a::attr(href)").get())
        )
