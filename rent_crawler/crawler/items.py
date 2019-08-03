import scrapy


class RentObjectItem(scrapy.Item):
    url = scrapy.Field()
    short_title = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    # district = scrapy.Field()
