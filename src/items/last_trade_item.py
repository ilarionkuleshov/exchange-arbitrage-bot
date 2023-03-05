from scrapy import Item, Field


class LastTradeItem(Item):
    market_id = Field()
    price = Field()
    status = Field()
