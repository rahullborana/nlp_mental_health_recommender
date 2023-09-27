# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class MentalHealthItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        self._values[key] = value
    pass
