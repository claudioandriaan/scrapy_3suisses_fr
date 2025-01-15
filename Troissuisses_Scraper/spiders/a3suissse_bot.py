import scrapy
from Troissuisses_Scraper.items import TroissuissesScraperItem
import logging

logging.basicConfig(level=logging.DEBUG)

class A3suissesBotSpider(scrapy.Spider):
    name = "3suisses_bot"
    start_urls = [
        "https://www.3suisses.fr/C-6176038-canapes--fauteuils.htm?page=1"
    ]

    def parse(self, response):
        product_links = response.css('div.item__content-top a::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.css('a.pagination__link.pagination__link--next::attr(href)').get()
        logging.debug(f"Next page: {next_page}")

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = TroissuissesScraperItem()
        name_parts = response.css('#product__infos h1::text').getall()
        name = ''.join(part.strip() for part in name_parts if part.strip())
        item['name'] = name
        item['price'] = response.css('.product__offer p.product__price span.dyn_prod_price::text').get()

        dispo = response.css('#product__infos .instock::text').getall()
        avail = ''.join(part.strip() for part in dispo if part.strip())                
        item['availability'] = avail

        item['delivery_time'] = response.css('.instock b span.dyn_time_fret::text').get()
        image_urls = response.css('#product__thumb-3su li a::attr(href)').getall()
        item['image_url'] = ["https://www.3suisses.fr" + url for url in image_urls]
        item['product_url'] = response.url
        yield item
