import scrapy

class TroissuissesScraperItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    delivery_time = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
