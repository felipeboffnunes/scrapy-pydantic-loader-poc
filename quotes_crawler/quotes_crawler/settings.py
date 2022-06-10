BOT_NAME = "quotes_crawler"

SPIDER_MODULES = ["quotes_crawler.spiders"]
NEWSPIDER_MODULE = "quotes_crawler.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 800
}

SPIDERMON_ENABLED = True

EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}